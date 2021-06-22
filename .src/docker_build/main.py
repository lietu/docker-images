from typing import List

import typer
from docker_build.images import find_images, build_image, upload_tags
from docker_build.validation import validate

cli = typer.Typer()


@cli.command(help="Build docker images")
def build():
    images = find_images()
    validate(images)
    for image, versions in images.items():
        for version in versions:
            build_image(image, version)


@cli.command(help="Upload docker tags")
def upload():
    images = find_images()
    validate(images)
    for image, versions in images.items():
        for version in versions:
            upload_tags(image, version)
