""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from datetime import datetime
from pathlib import Path

from zernike.utils.log_handler import create


LOGGER = create("outtree")


def make_global_outdir(
        parent_dir: Path, *, return_name: bool=False
) -> str | None:
    """
    """
    LOGGER.info("generating outputs' directory")

    outdir = parent_dir / (
        datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )
    )

    outdir.mkdir(parents=True, exist_ok=True)

    if return_name:
        return outdir.name
