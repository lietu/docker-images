from typing import Dict, List

from docker_build.images import docker_tag, get_config
from loguru import logger


def validate(images: Dict[str, List[str]]):
    for image in images.keys():
        tags = {}
        for version in images[image]:
            name = f"{image}/{version}"
            logger.debug("Validating {name}", name=name)
            _validate_version(image, version)
            _tags = _get_tags(image, version)

            # Check tags are unique
            for tag in _tags:
                if tag in tags.keys():
                    src = tags[tag]
                    raise ValueError(
                        f"{name} trying to redefine {tag} already defined in {src}"
                    )
                tags[tag] = name
                logger.debug("{name} has tag {tag}", name=name, tag=tag)


def _validate_version(image: str, version: str):
    pass


def _get_tags(image: str, version: str):
    tags = [docker_tag(image, version)]
    config = get_config(image, version)
    tags += [docker_tag(image, tag) for tag in config.tags]
    return tags
