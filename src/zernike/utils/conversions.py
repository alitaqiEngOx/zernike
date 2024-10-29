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


def j_to_mn(j: int) -> tuple[int, int]:
    """
    """
    n = int(
        np.floor(
            (np.sqrt(2. * j - 1.) + 0.5) - 1.
        )

    )

    if n % 2 == 0:
        m = int(
            2. * np.floor(
                0.25 * (2. * j + 1. - n * (n + 1.))
            )
        )

    else:
        m = int(
                2. * np.floor(
                0.25 * (2. * (j + 1.) - n * (n + 1.))
            ) - 1.
        )

    return m, n


def mn_to_j(m: int, n:int) -> list[int]:
    """
    """
    if m == 0:
        return [int(0.5 * n * (n + 1.) + 1.)]

    j = int(0.5 * n * (n + 1.) + m)
    return [j, j + 1]
