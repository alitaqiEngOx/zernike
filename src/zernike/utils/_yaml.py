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

    yaml_command_str = yaml.dump(
        yaml_command, sort_keys=False
    )

    yaml_command_str = yaml_command_str.replace(
        "$INPUT_DATADIR", f"{dir.parent}"
    )

    yaml_command_str = yaml_command_str.replace(
        "$GLOBAL_OUTDIR", 
        f"{dir.parent / global_outdir_name}"
    )

    return yaml.safe_load(yaml_command_str)
