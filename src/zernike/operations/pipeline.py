import numpy as np
from pathlib import Path

from zernike.operations.zernike import Zernike
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

    z = Zernike(j, radius_array, angle_array)
    z.show()


def estimate_beam(*, j_list: list[int], data_path: Path) -> None:
    """
    """
    f = FitKernel(j_list)
    f.show_sum()
