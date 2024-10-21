import numpy as np

from operations.zernike import Zernike


def run(
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

    x_array = np.arange(-1., 1.01, 0.01)
    y_array = x_array

    z = Zernike(j, x_array, y_array, coords_type="cartesian")
    z.show()
