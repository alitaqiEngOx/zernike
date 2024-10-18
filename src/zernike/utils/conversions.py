import numpy as np


def polar_to_cartesian(
        r: float, theta: float
) -> tuple[float, float]:
    """
    Converts polar coordinates to Cartesian coordinates.

    Arguments
    ---------
    r: float
        radius.
    
    theta: float
        angle (in radians).

    Returns
    -------
    Tuple bearing Cartesian coordinates (x, y).
    """
    return r * np.cos(theta), r * np.sin(theta)