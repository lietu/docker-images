import multiprocessing.context
import signal
import sys
from argparse import ArgumentParser
from multiprocessing import Pool

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


def set_logger(logger_):
    utils.logger = logger_


@cli.command(help="Build docker images")
def build():
    ap = ArgumentParser()
    ap.add_argument("--parallel", type=int, default=1)
    opts = ap.parse_args()

    images = find_images()
    validate(images)

    if opts.parallel == 1:
        for image, version in sort_images(images):
            build_image(image, version)
    else:
        utils.logger.info(f"Building images in {opts.parallel} threads")
        utils.logger.remove()
        utils.logger.add(sys.stderr, enqueue=True, level="INFO")

        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        with Pool(opts.parallel, initializer=set_logger, initargs=(utils.logger,)) as pool:
            signal.signal(signal.SIGINT, original_sigint_handler)

            try:
                res = pool.starmap_async(build_image, [
                    (image, version, False) for image, version in sort_images(images)
                ])
                while True:
                    try:
                        res.get(3)
                        # Have a timeout to be non-blocking for signals
                        # Returns when completed
                        pool.close()
                        break
                    except multiprocessing.context.TimeoutError:
                        continue
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
