import multiprocessing.context
import signal
import sys
from argparse import ArgumentParser
from multiprocessing import Pool
import os

import typer

import docker_build.utils as utils
from docker_build.images import (
    build_image,
    docker_tag,
    find_images,
    sort_images,
    upload_tags,
    update_scanner,
    scan_image,
)
from docker_build.validation import validate
from settings import conf

cli = typer.Typer()


def init_pool(logger_, env):
    utils.logger = logger_
    os.environ.update(env)


@cli.command(help="Build docker images")
def build():
    ap = ArgumentParser()
    ap.add_argument("--parallel", type=int, default=1)
    opts = ap.parse_args()

    images = find_images()
    validate(images)
    sorted_images = sort_images(images)

    if opts.parallel == 1:
        for image, version in sorted_images:
            build_image(image, version)
    else:
        utils.logger.info(f"Building images in {opts.parallel} threads")
        utils.logger.remove()
        utils.logger.add(sys.stderr, enqueue=True, level="INFO")

        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        with Pool(opts.parallel, initializer=init_pool, initargs=(utils.logger, os.environ)) as pool:
            signal.signal(signal.SIGINT, original_sigint_handler)

            def _build_images(_images):
                res = pool.starmap_async(build_image, [
                    (image, version, False) for image, version in _images
                ])
                while True:
                    try:
                        # Have a timeout to be non-blocking for signals
                        res.get(3)
                        break
                    except multiprocessing.context.TimeoutError:
                        pass

            priority = [img.split("/", maxsplit=1) for img in conf.PRIORITY_BUILDS]
            rest = [(image, version) for image, version in sorted_images if
                    f"{image}/{version}" not in conf.PRIORITY_BUILDS]

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


@cli.command(help="Upload docker tags")
def upload():
    images = find_images()
    validate(images)
    for image, versions in images.items():
        for version in versions:
            upload_tags(image, version)


@cli.command(help="Scan docker images")
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


@cli.command(help="List unique docker images managed by this tool")
def list():
    images = find_images()
    for image, versions in images.items():
        for version in versions:
            print(docker_tag(image, version))


@cli.command(help="Get the configured Docker username")
def docker_username():
    print(conf.DOCKER_USER)
