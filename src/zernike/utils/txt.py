""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path

import numpy as np
from numpy.typing import NDArray


def read_data(dir: Path) -> NDArray:
    """
    """
    with open(f"{dir}", 'r') as file:
        data = file.readlines()
    
    data = [
        item.strip().replace(', ', ' ')\
            .replace(' ,', ' ').replace(',', ' ')\
                .replace(' , ', ' ').split()
        for item in data
        if len(item.strip()) > 0
    ]
    data = [
        [float(entry) for entry in item]
        for item in data
        if item[0] != '#'

    ]

    return np.asarray(data)


def dump_npz_info(
        outname: Path, info: list[list[str]]
) -> None:
    """
    """
    lines = [
        "========= ZERNIKE =========\n",
        (
            "* Author: A. Taqi; "
            "alitaqi94.developer@gmail.com\n"
        ),
        "* All Rights Reserved\n\n",
        "### Header info for ``",
    ]
