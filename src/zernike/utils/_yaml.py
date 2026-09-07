""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import yaml
from pathlib import Path
from typing import Any

from zernike.utils.log_handler import create


LOGGER = create("yaml")


def read(
        dir: Path, *, global_outdir_name: str
) -> dict[str, Any]:
    """
    """
    LOGGER.info(f"reading `{dir.name}`")

    try:
        with open(f"{dir}", 'r') as file:
            yaml_command = yaml.safe_load(file)

    except:
        LOGGER.error(
            f"could not read `{dir.name}`\n"
        )

        raise
