import multiprocessing.context
import os
import signal
import sys
from enum import Enum
from multiprocessing import Pool
from typing import Optional

import docker_build.utils as utils
import typer
from docker_build.images import (
    build_image,
    docker_tag,
    find_images,
    scan_image,
    sort_images,
    update_scanner,
    upload_tags,
)
from docker_build.validation import validate

from settings import conf


class Platform(str, Enum):
    LINUX_AMD64 = "linux/amd64"
    LINUX_ARM64 = "linux/arm64"


build_cli = typer.Typer()
upload_cli = typer.Typer()
scan_cli = typer.Typer()
list_cli = typer.Typer()
docker_username_cli = typer.Typer()


def init_pool(logger_, env):
    utils.logger = logger_
    os.environ.update(env)


@build_cli.command(help="Build docker images")
def build(
    parallel: int = typer.Option(1), platform: Optional[Platform] = typer.Option(None)
):
    platform = platform.value if platform else None
    images = find_images()
    validate(images)
    sorted_images = sort_images(images)

    if parallel == 1:
        for image, version in sorted_images:
            build_image(image, version, platform=platform)
    else:
        utils.logger.info(f"Building images in {parallel} threads")
        utils.logger.remove()
        utils.logger.add(sys.stderr, enqueue=True, level="INFO")

        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        with Pool(
            parallel, initializer=init_pool, initargs=(utils.logger, os.environ)
        ) as pool:
            signal.signal(signal.SIGINT, original_sigint_handler)

            def _build_images(_images):
                res = pool.starmap_async(
                    build_image,
                    [(image, version, False, platform) for image, version in _images],
                )
                while True:
                    try:
                        # Have a timeout to be non-blocking for signals
                        res.get(3)
                        break
                    except multiprocessing.context.TimeoutError:
                        pass

            priority = [img.split("/", maxsplit=1) for img in conf.PRIORITY_BUILDS]
            rest = [
                (image, version)
                for image, version in sorted_images
                if f"{image}/{version}" not in conf.PRIORITY_BUILDS
            ]

            try:
                utils.logger.info("Building {c} priority images", c=len(priority))
                _build_images(priority)

                utils.logger.info("Building remaining {c} images", c=len(rest))
                _build_images(rest)

                pool.close()
            except KeyboardInterrupt:
                utils.logger.error("Caught KeyboardInterrupt, terminating workers")
                pool.terminate()
                raise


@upload_cli.command(help="Upload docker tags")
def upload():
    images = find_images()
    validate(images)
    for image, versions in images.items():
        for version in versions:
            upload_tags(image, version)


@scan_cli.command(help="Scan docker images")
def scan():
    update_scanner()
    images = find_images()
    vuln_images = []
    for image, versions in images.items():
        for version in versions:
            if not scan_image(image, version):
                vuln_images.append(docker_tag(image, version))

    if vuln_images:
        utils.logger.error("Some images have vulnerabilities!")
        for img in vuln_images:
            print(f" - {img}")

        raise typer.Exit(code=1)


@list_cli.command(help="List unique docker images managed by this tool")
def list():
    images = find_images()
    for image, versions in images.items():
        for version in versions:
            print(docker_tag(image, version))


@docker_username_cli.command(help="Get the configured Docker username")
def docker_username():
    print(conf.DOCKER_USER)
