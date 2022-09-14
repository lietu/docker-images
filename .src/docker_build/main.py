from enum import Enum
from typing import Optional

import typer
from docker_build.images import (
    build_image,
    docker_tag,
    find_images,
    sort_images,
    upload_tags,
)
from docker_build.validation import validate

from settings import conf


class Platform(str, Enum):
    LINUX_AMD64 = "linux/amd64"
    LINUX_ARM64 = "linux/arm64"


build = typer.Typer()
upload = typer.Typer()
list = typer.Typer()
docker_username = typer.Typer()


@build.command(help="Build docker images")
def _build(platform: Optional[Platform] = typer.Option(None)):
    platform = platform.value if platform else None
    images = find_images()
    validate(images)
    for image, version in sort_images(images):
        build_image(image, version, platform)


@upload.command(help="Upload docker tags")
def _upload():
    images = find_images()
    validate(images)
    for image, versions in images.items():
        for version in versions:
            upload_tags(image, version)


@list.command(help="List unique docker images managed by this tool")
def _list():
    images = find_images()
    for image, versions in images.items():
        for version in versions:
            print(docker_tag(image, version))


@docker_username.command(help="Get the configured Docker username")
def _docker_username():
    print(conf.DOCKER_USER)
