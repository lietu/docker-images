from subprocess import check_call  # nosec
from typing import List

from loguru import logger


def run(cmd: List[str]):
    logger.debug("Executing: {cmd}", cmd=" ".join(cmd))
    check_call(cmd)
