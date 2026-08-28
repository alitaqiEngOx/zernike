""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import shlex
import yaml
from pathlib import Path
from typing import Any

import numpy as np

from zernike.operations.aberration import Aberration
from zernike.operations.kernel import Kernel
from zernike.utils.conversions import (
    j_to_mn, mn_to_j
)
from zernike.utils.log_handler import create
from zernike.utils.npz import NPZ


LOGGER = create("pipeline")


def convert(
        *, j: int | None=None,
        mn: list[int] | None=None
) -> None:
    """
    """
    # filter out incorrect entries
    if (
        (j is None and mn is None) or
        (j is not None and mn is not None)
    ):
        raise ValueError(
            "provide either `j` or `mn`"
        )

    if j is None:
        j = mn_to_j(mn[0], mn[1])
        print(f"j = {j}")
        return

    m, n = j_to_mn(j)
    print(f"m = {m}; n = {n}")


def estimate_beam(
        kernel_path: Path, *,
        j_list: list[str] | None=None,
        n_list: list[str] | None=None
) -> None:
    """
    """
    # filter out incorrect entries
    if (
        (j_list is None and n_list is None) or
        (j_list is not None and n_list is not None)
    ):
        raise ValueError(
            "provide either `j` or `n`"
        )

    # load kernel in memory
    if j_list is None:
        k = Kernel.via_n(n_list, kernel_path)

    else:
        k = Kernel(j_list, kernel_path)

    # fit aberrations to kernel
    k.estimate()

    # show outputs
    k.show()
    k.show("fitted_kernel")
    k.show("residual_kernel")

    # show weights
    k.show_weights()


def kernel_from_npz(
        npz_path: Path, *, show_info: bool=False,
        key: str | None=None,
        index: list[str] | None=None,
        save_as: Path | None=None
) -> None:
    """
    """
    npz = NPZ(npz_path)

    if show_info:
        info = [
            item.split(':', maxsplit=1)
            for item in npz.keys_and_shapes
        ]

        key_width = max(
            len(key) for key, _ in info
        )

        print(f"{'key':<{key_width}} : shape")

        for key, shape in info:
            print(f"{key:<{key_width}} : {shape}")

        return

    if save_as is None:
        raise ValueError(
            "provide either `show_info=True` or `save_as` path"
        )

    npz.dump(
        save_as, key=key, index=index
    )


def plot_aberration(config: Path) -> None:
    """
    Principal aberration plotting function.

    Arguments
    ---------
    config: pathlib.Path
        path to the configuration file.
    """
    def adjust(arr: str, *, label: str) -> list[int]:
        """
        """
        try:
            params = shlex.split(arr)

        except:
            LOGGER.error(
                f"bad `{label}` definition "
                f"for `{key}`"
            )

            raise

        if len(params) != 3:
            LOGGER.error(
                f"bad `{label}` definition for "
                f"`{key}`"
            )

            raise ValueError(
                f"expected `{label}` comprising 3 "
                f"values under `{key}`, got ({arr})"
            )

        arr_int = []

        for param in params:
            if not param.replace('-', '').isdigit():
                LOGGER.error(
                    f"bad `{label}` definition for "
                    f"`{key}`"
                )

                raise ValueError(
                    "expected digits for `mn` under "
                    f"`{key}`, got ({arr})"
                )

            arr_int.append(int(param))

        return arr_int

    # ----------------------------------------
    # 1. READ `.yml` AND LOOP THROUGH ENTRIES
    # ----------------------------------------
    config_dict = read_yaml(config)

    for key, value in config_dict.items():
        # ----------------------------------------
        # 2. DEFINE PARAMETERS/COORDINATES
        # ----------------------------------------
        j = value["j"]
        mn = value["mn"]
        basis = value["basis"]
        coords_type = value["coords_type"]
        dim_0 = value["dim_0"]
        dim_1 = value["dim_1"]

        # filter out unsupported entries
        if (
            (j is None and mn is None) or
            (j is not None and mn is not None)
        ):
            LOGGER.error(
                "bad `{key}` definition"
            )

            raise ValueError(
                "expected either `j` or `mn` "
                f"under `{key}`"
            )

        # assert/adjust dimensions
        if mn is not None:
            mn = adjust(mn, label="mn")

        if coords_type.lower() == "cartesian":
            if dim_0 is None:
                dim_0 = [
                    -0.5 * np.sqrt(2.),
                    0.5 * np.sqrt(2.), 0.01
                ]

            else:
                dim_0 = adjust(dim_0, label="dim_0")

            if dim_1 is None:
                dim_1 == dim_0.copy()

            else:
                dim_1 = adjust(dim_1, label="dim_1")

        elif coords_type.lower() == "polar":
            if dim_0 is None:
                dim_0 = [0., 1., 0.01]

            else:
                dim_0 = adjust(dim_0, label="dim_0")

            if dim_1 is None:
                dim_1 = [0., 2. * np.pi, 0.01]

            else:
                dim_1 = adjust(dim_1, label="dim_1")

        else:
            raise ValueError(
                "`coords_type` must either be `cartesian` "
                f"or `polar; got {coords_type}`"
            )

        for dim in [dim_0, dim_1]:
            if dim[0] >= dim[1]:
                raise ValueError(
                    "`dim[0] >= dim[1]` not allowed; "
                    f"got {dim}"
                )

            if dim[2] > dim[1] - dim[0]:
                raise ValueError(
                    "`dim[2] > dim[1] - dim[0]` not "
                    f"allowed; got {dim}"
                )

        if coords_type.lower() == "polar":
            dim_0[0] = max(dim_0[0], 0.)
            dim_1[0] = max(dim_1[0], 0.)
            dim_1[1] = min(dim_1[1], 2. * np.pi)

        
        
        

        # ----------------------------------------
        # 3. DEFINE/PLOT ABERRATION
        # ----------------------------------------
        if j:
            z = Aberration(
                j,
                np.arange(dim_0[0], dim_0[1] + dim_0[2], dim_0[2]),
                np.arange(dim_1[0], dim_1[1] + dim_1[2], dim_1[2]),
                coords_type, basis
            )

        else:
            z = Aberration.via_mn(
                mn,
                np.arange(dim_0[0], dim_0[1] + dim_0[2], dim_0[2]),
                np.arange(dim_1[0], dim_1[1] + dim_1[2], dim_1[2]),
                coords_type, basis
            )

        z.show()


def read_yaml(dir: Path) -> dict[str, Any]:
    """
    """
    LOGGER.info(f"reading `{dir.name}`")

    try:
        with open(f"{dir}", 'r') as file:
            return yaml.safe_load(file)

    except Exception:
        LOGGER.error(
            f"could not read file: {dir.name}\n"
        )

        raise
