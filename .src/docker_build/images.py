import time
from datetime import timedelta
from pathlib import Path
from typing import Dict, List, Optional

import humanize
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


class ImageConf:
    priority: int
    image: list[str]

    def __init__(self, priority: int, image: list[str]):
        self.priority = priority
        self.image = image

    def __repr__(self):
        return f"<{':'.join(self.image)} @ {self.priority} prio>"


def sort_images(images_: Dict[str, List[str]]) -> List[ImageConf]:
    images = []
    for image, versions in images_.items():
        for version in versions:
            images.append(f"{image}/{version}")
    images.sort()
    for image_or_list in conf.PRIORITY_BUILDS:
        if isinstance(image_or_list, str):
            try:
                images.remove(image_or_list)
            except ValueError:
                logger.error(
                    "{image} found in PRIORITY_BUILDS is incorrect", image=image_or_list
                )
                raise
        else:
            for _img in image_or_list:
                try:
                    images.remove(_img)
                except ValueError:
                    logger.error(
                        "{image} found in PRIORITY_BUILDS is incorrect", image=_img
                    )
                    raise

    priority = 1
    result = []
    for image_or_list in conf.PRIORITY_BUILDS:
        if isinstance(image_or_list, str):
            try:
                result.append(
                    ImageConf(
                        priority=priority, image=image_or_list.split("/", maxsplit=1)
                    )
                )
            except ValueError:
                logger.error(
                    "{image} found in PRIORITY_BUILDS is incorrect", image=image_or_list
                )
                raise
        else:
            for _img in image_or_list:
                try:
                    result.append(
                        ImageConf(priority=priority, image=_img.split("/", maxsplit=1))
                    )
                except ValueError:
                    logger.error(
                        "{image} found in PRIORITY_BUILDS is incorrect", image=_img
                    )
                    raise
        priority += 1

    result += [
        ImageConf(priority=priority, image=img.split("/", maxsplit=1)) for img in images
    ]

    return result


def build_image(image: str, version: str, verbose=True, platform: Optional[str] = None):
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

    if platform:
        cmd += ["--platform", platform]

    start = time.perf_counter()
    run(cmd, verbose=verbose)
    end = time.perf_counter()
    if not verbose:
        logger.info(
            "Built {name} in {elapsed}",
            name=name,
            elapsed=humanize.precisedelta(timedelta(seconds=end - start)),
        )


def build_image_multiplatform(
    image: str, version: str, platforms: List[str], verbose=True
):
    name = f"{image}/{version}"

    logger.info("Building {name}", name=name)

    localhost_tag = f"{conf.LOCAL_REGISTRY}/{image}:{version}"
    build_cmd = [
        "docker",
        "buildx",
        "build",
        "--platform",
        ",".join(platforms),
        name,
        "-t",
        localhost_tag,
        "--build-arg",
        f"LOCAL_REGISTRY={conf.LOCAL_REGISTRY}/",
        "--network=host",
        "--push",  # push to localhost registry
    ]

    start = time.perf_counter()
    run(build_cmd, verbose=verbose)
    end = time.perf_counter()
    if not verbose:
        logger.info(
            "Built {name} in {elapsed}",
            name=name,
            elapsed=humanize.precisedelta(timedelta(seconds=end - start)),
        )


def upload_tags_from_local_registry(images: Dict[str, List[str]]):
    # local docker registry runs by HTTP, so we state it in regctl
    run(["regctl", "registry", "set", "--tls", "disabled", conf.LOCAL_REGISTRY])
    for image, versions in images.items():
        for version in versions:
            config = get_config(image, version)
            localhost_tag = f"{conf.LOCAL_REGISTRY}/{image}:{version}"
            tags = [docker_tag(image, tag) for tag in config.tags]
            tags.append(docker_tag(image, version))
            for tag in tags:
                run(["regctl", "image", "copy", localhost_tag, tag], verbose=True)


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


def update_scanner():
    logger.info("Updating trivy database")
    run(["trivy", "image", "--download-db-only"])


def scan_image(image: str, version: str) -> bool:
    try:
        run(
            [
                "trivy",
                "image",
                "--skip-update",
                "--severity",
                "HIGH,CRITICAL",
                "--exit-code",
                "1",
                "--timeout",
                "7m",
                f"{docker_image(image)}:{version}",
            ],
            cwd=f"{image}/{version}",
        )
        return True
    except Exception:
        logger.error(
            "{image}:{version} has vulnerabilities!", image=image, version=version
        )
        return False
