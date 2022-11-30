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

cli = typer.Typer()


@cli.command(help="Build docker images")
def build():
    images = find_images()
    validate(images)
    for image, version in sort_images(images):
        build_image(image, version)


@cli.command(help="Upload docker tags")
def upload():
    images = find_images()
    validate(images)
    for image, versions in images.items():
        for version in versions:
            upload_tags(image, version)


@cli.command(help="List unique docker images managed by this tool")
def list():
    images = find_images()
    for image, versions in images.items():
        for version in versions:
            print(docker_tag(image, version))


@cli.command(help="Get the configured Docker username")
def docker_username():
    print(conf.DOCKER_USER)
