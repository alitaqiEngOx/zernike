from pathlib import Path

import numpy as np
from numpy.typing import NDArray


def read_data(dir: Path) -> NDArray:
    """
    """
    with open(f"{dir}", 'r') as file:
        data = file.readlines()

    return np.asarray([
        item.strip().split()
        for item in data
        if item.strip()[0] != '#'
    ])
