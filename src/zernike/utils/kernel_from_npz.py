""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path

import numpy as np


def extract(
        path: Path, index: list[str],
        key: str="beam", *, outname: Path
) -> None:
    """
    """
    with np.load(path) as archive:
        if key not in archive.files:
            raise KeyError(
                f"array {key!r} does not exist in {path}; "
                f"available arrays are {archive.files}"
            )

        numpy_idx = tuple(
            parse_index(value)
            for value in index
        )

        try:
            kernel = archive[key][numpy_idx]

        except IndexError as error:
            raise IndexError(
                f"index {index!r} is invalid for array "
                f"{key!r} with shape {archive[key].shape}"
            ) from error

    np.save(outname, kernel)


def parse_index(value: str) -> int | slice:
    """
    """
    if ':' not in value:
        try:
            return int(value)

        except ValueError as error:
            raise ValueError(
                f"unsupported index {value!r}"
            ) from error

    parts = value.split(':')

    if len(parts) > 3:
        raise ValueError(
            f"invalid index component {value!r}"
        )

    parsed = []
    for part in parts:
        part = part.strip()

        if part:
            try:
                parsed.append(int(part))

            except ValueError as error:
                raise ValueError(
                    f"invalid index component {value!r}"
                ) from error

        else:
            parsed.append(None)

    while len(parsed) < 3:
        parsed.append(None)

    if parsed[2] == 0:
        raise ValueError(
            f"slice step cannot be zero in index {value!r}"
        )

    return slice(*parsed)
