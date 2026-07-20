""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import numpy as np
from pathlib import Path

from zernike.operations.aberration import Aberration
from zernike.operations.kernel import Kernel
from zernike.utils.conversions import (
    j_to_mn, mn_to_j
)
from zernike.utils.npz import NPZ


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


def plot_aberration(
        *, j: int | None=None,
        mn: tuple[int] | None=None,
        dim_0: list[float] | None=None,
        dim_1: list[float] | None=None,
        coords_type: str="polar",
        basis: str="real"
) -> None:
    """
    Principal function in the pipeline executing
    the desired functionality.

    Arguments
    ---------
    j: int (optional)
        order of Zernike polynomial via `j`.

    mn: tuple[int] (optional)
        order of Zernike polynomial via `m` & `n`.

    dim_0: list[float] (optional)
        minimum, maximum and step in dimension 0.

    dim_1: list[float] (optional)
        minimum, maximum and step in dimension 1.

    coords_type: str (optional)
        `polar` or `cartesian`.

    basis: str (optional)
        `complex` or `real`.
    """
    # filter out incorrect entries
    if (
        (j is None and mn is None) or
        (j is not None and mn is not None)
    ):
        raise ValueError(
            "provide either `j` or `mn`"
        )

    # define coordinates
    if coords_type.lower() == "cartesian":
        if dim_0 is None:
            dim_0 = [
                -0.5 * np.sqrt(2.),
                0.5 * np.sqrt(2.), 0.01
            ]

        if dim_1 is None:
            dim_1 = dim_0.copy()

    elif coords_type.lower() == "polar":
        if dim_0 is None:
            dim_0 = [0., 1., 0.01]

        if dim_1 is None:
            dim_1 = [0., 2. * np.pi, 0.01]

    else:
        raise ValueError(
            "`coords_type` must either be `cartesian` "
            f"or `polar; got {coords_type}`"
        )

    for dim in [dim_0, dim_1]:
        if dim[0] >= dim[1]:
            raise ValueError(
                f"`dim[0] >= dim[1]` not allowed; got {dim}"
            )

        if dim[2] > dim[1] - dim[0]:
            raise ValueError(
                f"`dim[2] > dim[1] - dim[0]` not allowed; got {dim}"
            )

    if coords_type.lower() == "polar":
        dim_0[0] = max(dim_0[0], 0.)
        dim_1[0] = max(dim_1[0], 0.)
        dim_1[1] = min(dim_1[1], 2. * np.pi)

    # define and plot aberration
    if j:
        z = Aberration(
            j,
            np.arange(dim_0[0], dim_0[1] + dim_0[2], dim_0[2]),
            np.arange(dim_1[0], dim_1[1] + dim_1[2], dim_1[2]),
            coords_type=coords_type
        )

    else:
        z = Aberration.via_mn(
            mn,
            np.arange(dim_0[0], dim_0[1] + dim_0[2], dim_0[2]),
            np.arange(dim_1[0], dim_1[1] + dim_1[2], dim_1[2]),
            coords_type=coords_type
        )

    z.show()
