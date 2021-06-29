from pathlib import Path
from typing import Dict, List

from docker_build.utils import run
from loguru import logger
from pydantic import BaseModel
from yaml import load

from settings import conf

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Config(BaseModel):
    tags: List[str]


def find_images() -> Dict[str, List[str]]:
    result = {}

    images = [
        p.name for p in Path(".").iterdir() if p.is_dir() and not p.name.startswith(".")
    ]

    for image in images:
        versions = [
            p.name
            for p in Path(image).iterdir()
            if p.is_dir() and not p.name.startswith(".")
        ]
        result[image] = versions

    return result


def sort_images(images_: Dict[str, List[str]]) -> List[List[str]]:
    images = []
    for image, versions in images_.items():
        for version in versions:
            images.append(f"{image}/{version}")
    images.sort()
    for img in conf.PRIORITY_BUILDS:
        try:
            images.remove(img)
        except ValueError:
            logger.error("{image} found in PRIORITY_BUILDS is incorrect", image=img)
            raise

    images = conf.PRIORITY_BUILDS + images
    return [img.split("/", maxsplit=1) for img in images]


def build_image(image: str, version: str):
    config = get_config(image, version)
    name = f"{image}/{version}"
    tag = docker_tag(image, version)

    logger.info("Building {name}", name=name)

    # Full commandline with all tags in one
    cmd = ["docker", "build", name, "-t", tag]
    for tag in config.tags:
        full_name = docker_tag(image, tag)
        cmd += ["-t", full_name]

    # make it possible to reuse this image in other local builds
    cmd += ["-t", docker_tag(image, tag=version, local=True)]

    run(cmd)


def upload_tags(image: str, version: str):
    name = f"{image}/{version}"
    logger.info("Uploading tags for {name}", name=name)

    # --all-tags added in Docker 20.10.0
    run(["docker", "push", "--all-tags", docker_image(image)])


def docker_image(image: str) -> str:
    return f"{conf.DOCKER_USER}/{image}"


def docker_tag(image: str, tag: str, local: bool = False) -> str:
    if not local:
        return f"{docker_image(image)}:{tag}"
    return f"{image}:{tag}"


def get_config(image: str, version: str) -> Config:
    config_path = f"{image}/{version}/config.yaml"
    config_text = Path(config_path).read_text(encoding="utf-8")
    config = load(config_text, Loader=Loader)
    return Config(**config)
