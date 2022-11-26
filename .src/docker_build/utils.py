from subprocess import PIPE, STDOUT, check_call  # nosec
from subprocess import run as sp_run  # nosec
from typing import List

from loguru import logger


def run(cmd: List[str], verbose=True, cwd=None):
    logger.debug("Executing: {cmd}", cmd=" ".join(cmd))
    if verbose:
        check_call(cmd, cwd=cwd)
    else:
        result = sp_run(cmd, stdout=PIPE, stderr=STDOUT, cwd=cwd)
        if result.returncode > 0:
            logger.error(
                "{cmd} exited with code {code}",
                cmd=" ".join(cmd),
                code=result.returncode,
            )
            logger.error(result.stdout.decode("utf-8"))
            raise Exception(f"Failed to run {cmd}")
