""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import ast
import struct
import shutil
import zipfile
from pathlib import Path
from typing import BinaryIO

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
        if self._keys_and_shapes is None:
            with zipfile.ZipFile(self.path, 'r') as archive:
                members = [
                    name
                    for name in archive.namelist()
                    if name.endswith(".npy")
                ]

                self._keys = [
                    name.removesuffix(".npy")
                    for name in members
                ]

                self._keys_and_shapes = []
                for key, member in zip(self._keys, members):
                    with archive.open(member, "r") as file:
                        shape = read_npy_shape(file)

                    self._keys_and_shapes.append(
                        f"{key}:{shape}"
                    )

        assert self._keys_and_shapes is not None
        return self._keys_and_shapes


    def dump(
            self, outname: Path, *,
            key: str | None=None, 
            index: list[str] | None=None
    ) -> None:
        """
        """
        # no `key`
        if key is None:
            if index is not None:
                raise ValueError(
                    "`index` cannot be provided "
                    "when `key` is `None`"
                )

            shutil.copy2(self.path, outname)
            return

        # `key` but no `index`
        if key not in self.keys:
            raise KeyError(
                f"array {key!r} does not exist in {self.path}; "
                f"available arrays are {self.keys}"
            )

        if index is None:
            with np.load(self.path) as archive:
                np.save(outname, archive[key])
                return

        # `key` and `index`
        numpy_idx = tuple(
            parse_index(value) for value in index
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


def read_npy_shape(file: BinaryIO) -> tuple[int]:
    """
    """
    version = np.lib.format.read_magic(file)

    if version == (1, 0):
        header_length = struct.unpack(
            "<H", file.read(2)
        )[0]

        encoding = "latin1"

    elif version in ((2, 0), (3, 0)):
        header_length = struct.unpack(
            "<I", file.read(4)
        )[0]

        encoding = (
            "utf-8" if version == (3, 0)
            else "latin1"
        )

    else:
        raise ValueError(
            f"unsupported NPY version {version}"
        )

    header = file.read(header_length).decode(encoding)
    metadata = ast.literal_eval(header)

    return tuple(metadata["shape"])
