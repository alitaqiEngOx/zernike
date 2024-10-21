import numpy as np


def cartesian_to_polar(
        x: float, y: float
) -> tuple[float, float]:
    """
    Converts Cartesian coordinates to polar coordinates.

    Arguments
    ---------
    x: float
        horizontal coordinate.
    
    y: float
        vertical coordinate.

    Returns
    -------
    Tuple bearing polar coordinates (r, theta - in radians).
    """
    return np.sqrt(x**2. + y**2.), np.arctan2(y, x)


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
