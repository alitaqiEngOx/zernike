import numpy as np
from pathlib import Path

from zernike.operations.aberration import Aberration
from zernike.operations.fit_kernel import FitKernel


def plot_aberration(
        *, j: int, radius_max: float, radius_step: float, num_angles: int
) -> None:
    """
    Principal function in the pipeline executing the desired functionality.

    Arguments
    ---------
    j: int
        order of the Zernike polynomial.

    radius_max: float
        maximum radius to be included in the plot.

    radius_step: float
        numerical step in the radius domain.

    num_angles: int
        number of angles to be computed between 0 deg and 360 deg.
    """
    radius_array = np.arange(0., radius_max + radius_step, radius_step)
    angle_array = np.linspace(0., 2.*np.pi, num_angles)

    z = Aberration(j, radius_array, angle_array)
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