""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path

import numpy as np


class NPZ:
    """"""

    def __init__(self, path: Path) -> None:
        """
        """
        self.path = path
        self._keys: list[str] | None=None
        self._keys_and_shapes: list[str] | None=None


    @property
    def keys(self) -> list[str]:
        """
        """
        if not self._keys:
            _ = self.keys_and_shapes

        return self._keys


    @property
    def keys_and_shapes(self) -> list[str]:
        """
        """
        if not self._keys_and_shapes:
            with np.load(self.path) as archive:
                self._keys = list(archive.files)

                self._keys_and_shapes = [
                    f"{key}:{archive[key].shape}"
                    for key in self._keys
                ]

        return self._keys_and_shapes


    def extract(
            self, key: str, index: list[str], *,
            outname: Path
    ) -> None:
        """
        """
        if key not in self.keys:
            raise KeyError(
                f"array {key!r} does not exist "
                f"in {self.path}; available arrays "
                f"are {self.keys}"
            )

        numpy_idx = tuple(
            parse_index(value)
            for value in index
        )

        with np.load(self.path) as archive:
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
