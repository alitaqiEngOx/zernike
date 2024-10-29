import numpy as np
from pathlib import Path

from zernike.operations.aberration import Aberration
from zernike.operations.fit_kernel import FitKernel


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


def estimate_beam(*, j_list: list[int], kernel_path: Path) -> None:
    """
    """
    f = FitKernel(j_list, kernel_path)
    f.show("kernel")
    f.show("avg_aberration_sum")

    # fit data to aberration
    params, covariance = f.fit_data()

    aberration_data_list = f.compute_aberrations()

    aberration_data_list = np.asarray([
        item * param
        for item, param in zip(aberration_data_list, params)
    ])

    # temporary code
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
    plt.colorbar(c)
    plt.show()
