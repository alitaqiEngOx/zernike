import numpy as np
from pathlib import Path
from typing import Optional

from zernike.operations.aberration import Aberration
from zernike.operations.fit_kernel import FitKernel
from zernike.utils.conversions import (
    j_to_mn, mn_to_j
)


def convert(
        *, j: Optional[int]=None, mn: Optional[list[int]]=None
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
        print(f"j = {j}")
        return

    m, n = j_to_mn(j)
    print(f"m = {m}; n = {n}")


def estimate_beam(*, j_list: list[int], kernel_path: Path) -> None:
    """
    """
    f = FitKernel(j_list, kernel_path)
    f.show("kernel")

    # fit data to aberration
    params, covariance = f.fit_data()

    aberration_data_list = f.compute_aberrations()

    aberration_data_list = np.asarray([
        item * param
        for item, param in zip(aberration_data_list, params)
    ])

    # temporary code
    print(f"mean_diff = {np.mean(np.sum(aberration_data_list, axis=0) - f.kernel)}")
    print(f"std_diff = {np.std(np.sum(aberration_data_list, axis=0) - f.kernel)}")

    import matplotlib.pyplot as plt

    plt.figure(figsize=(15, 15))
    ax = plt.subplot()
    ax.set_aspect("equal")
    c = plt.pcolormesh(
        f.aberration_list[0].meshed_arrays[0],
        f.aberration_list[0].meshed_arrays[1],
        np.sum(aberration_data_list, axis=0),
        shading="auto", cmap="hot_r"
    )
    plt.colorbar(c)
    plt.show()

    plt.figure(figsize=(15, 15))
    ax = plt.subplot()
    ax.set_aspect("equal")
    c = plt.pcolormesh(
        f.aberration_list[0].meshed_arrays[0],
        f.aberration_list[0].meshed_arrays[1],
        np.sum(aberration_data_list, axis=0) - f.kernel,
        shading="auto", cmap="hot_r"
    )
    plt.title("difference")
    plt.colorbar(c)
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
