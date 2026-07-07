""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import numpy as np
from pathlib import Path

from zernike.operations.aberration import Aberration
from zernike.operations.fit_kernel import FitKernel
from zernike.utils.conversions import (
    j_to_mn, mn_to_j
)


def convert(
        *, j: int | None=None, mn: list[int] | None=None
) -> None:
    """
    """
    if (j is None and mn is None) or\
    (j is not None and mn is not None):
        raise ValueError(
            "provide either `j` or `mn`"
        )

    if j is None:
        j = mn_to_j(mn[0], mn[1])
        for idx, item in enumerate(j):
            print(f"j[{idx}] = {item}")

        return

    m, n = j_to_mn(j)
    print(f"m = {m}; n = {n}")


def estimate_beam(
        kernel_path: Path, *, j_list: list[str] | None=None,
        n_list: list[str] | None=None
) -> None:
    """
    """
    if (j_list is None and n_list is None) or\
    (j_list is not None and n_list is not None):
        raise ValueError(
            "provide either `j` or `mn`"
        )

    if j_list is None:
        f = FitKernel.via_n(n_list, kernel_path)

    else:
        f = FitKernel(j_list, kernel_path)

    f.show("kernel")

    # fit aberrations to kernel
    weights, fitted_kernel, residual_kernel = f.fit_data()

    # temporary for plotting
    import matplotlib.pyplot as plt

    # fitted kernel
    plt.figure(figsize=(15, 15))
    ax = plt.subplot()
    ax.set_aspect("equal")

    c = plt.pcolormesh(
        f.aberration_list[0].meshed_arrays[0],
        f.aberration_list[0].meshed_arrays[1],
        fitted_kernel,
        shading="auto", cmap="hot_r"
    )

    plt.title("fitted")
    plt.colorbar(c)
    plt.show()

    # residual kernel
    plt.figure(figsize=(15, 15))
    ax = plt.subplot()
    ax.set_aspect("equal")

    c = plt.pcolormesh(
        f.aberration_list[0].meshed_arrays[0],
        f.aberration_list[0].meshed_arrays[1],
        residual_kernel,
        shading="auto", cmap="hot_r"
    )

    plt.title("residual")
    plt.colorbar(c)
    plt.show()

    # weights
    plt.figure(figsize=(12, 6))
    ax = plt.subplot()

    ax.bar(f.j_list, weights)
    ax.axhline(0., linewidth=1.)

    ax.set_xlabel("j")
    ax.set_ylabel("weight")
    ax.set_title("Fitted Zernike weights")

    ax.set_xticks(f.j_list)
    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()


def plot_aberration(
        *, j: int, dim_0: list[float], dim_1: list[float],
        coords_type: str="polar"
) -> None:
    """
    Principal function in the pipeline executing the desired functionality.

    Arguments
    ---------
    j: int
        order of the Zernike polynomial.

    dim_0: list[float]
        minimum, maximum, and step in dimension 0.

    dim_1: list[float]
        minimum, maximum, and step in dimension 0.

    coords:_type str (optional)
        `polar` or `cartesian`.
    """
    for dim in [dim_0, dim_1]:
        if dim[0] >= dim[1]:
            raise ValueError(
                f"maximum value in {dim} cannot be smaller than or equal to "
                "minimum value"
            )

        if dim[2] > dim[1] - dim[0]:
            raise ValueError(
                "step value in {dim} cannot be larger than the difference "
                "between maximum and minimum values"
            )

    if coords_type.lower() == "polar":
        dim_0[0] = max(dim_0[0], 0.)
        dim_1[0] = max(dim_1[0], 0.)
        dim_1[1] = min(dim_1[1], 2. * np.pi)

    z = Aberration(
        j,
        np.arange(dim_0[0], dim_0[1] + dim_0[2], dim_0[2]),
        np.arange(dim_1[0], dim_1[1] + dim_1[2], dim_1[2]),
        coords_type=coords_type
    )
    z.show()
