""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import ast
import struct
import shutil
import tempfile
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
        if self._keys is None:
            _ = self.keys_and_shapes

        assert self._keys is not None
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
        outname.parent.mkdir(
            parents=True, exist_ok=True
        )
        # -------------------------------------------------
        # case 1:
        # no key is provided
        #
        # action: copy the full `.npz` unchanged
        #
        # this does not load anything into memory
        # -------------------------------------------------
        if key is None:
            if index is not None:
                raise ValueError(
                    "`index` cannot be provided "
                    "when `key` is `None`"
                )

            if outname.suffix != ".npz":
                outname = Path(f"{outname}.npz")

            shutil.copy2(self.path, outname)
            return

        # validate key
        if key not in self.keys:
            raise KeyError(
                f"array {key!r} does not exist in {self.path}; "
                f"available arrays are {self.keys}"
            )

        # -------------------------------------------------
        # case 2:
        # key is provided, but no index is provided
        #
        # action: extract the `.npy` array directly
        #
        # this does not load anything into memory
        # -------------------------------------------------
        if index is None:
            if outname.suffix != ".npy":
                outname = Path(f"{outname}.npy")

            with zipfile.ZipFile(self.path, 'r') as archive:
                with archive.open(f"{key}.npy", 'r') as source:
                    with open(outname, 'wb') as destination:
                        shutil.copyfileobj(
                            source, destination,
                            length=16 * 1024 * 1024
                        )

            return

        # -------------------------------------------------
        # case 3:
        # key and index are both provided
        #
        # action: extract only a chunk
        #
        # this generates a temporary `.npy` of the
        # key to load from it
        # -------------------------------------------------
        if index == []:
            raise ValueError("`index` cannot be empty")

        numpy_idx = tuple(
            parse_index(value) for value in index
        )

        if outname.suffix != ".npy":
            outname = Path(f"{outname}.npy")

        with tempfile.TemporaryDirectory(
            dir=outname.parent
        ) as temp_dir:
            temp_path = Path(temp_dir) / f"{key}.npy"

            # stream the requested `.npy` to disk (no RAM)
            with zipfile.ZipFile(self.path, 'r') as archive:
                with archive.open(f"{key}.npy", 'r') as source:
                    with open(temp_path, 'wb') as destination:
                        shutil.copyfileobj(
                            source, destination,
                            length=16 * 1024 * 1024
                        )

            # memory-map `temp_path` & extract data
            array = np.load(
                temp_path, mmap_mode='r', allow_pickle=False
            )

            try:
                kernel = np.array(
                    array[numpy_idx], copy=True
                )

            except (IndexError, ValueError) as error:
                raise IndexError(
                    f"index {index!r} is invalid for array "
                    f"{key!r} with shape {array.shape}"
                ) from error

            finally:
                del array

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


def read_npy_shape(file: BinaryIO) -> tuple[int, ...]:
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
