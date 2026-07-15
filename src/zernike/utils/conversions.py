""" Licensed under the same terms as described in the main 
licensing script of this repository. """

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
    # check `j`
    if j < 1:
        raise ValueError(
            f"j must be positive; got j={j}"
        )

    # compute `n`
    n = int(
        np.floor(
            (np.sqrt(2. * j - 1.) + 0.5) - 1.
        )
    )

    # compute `m`
    if n % 2 == 0:
        m_abs = int(
            2. * np.floor(
                0.25 * (2. * j + 1. - n * (n + 1.))
            )
        )

    else:
        m_abs = int(
                2. * np.floor(
                0.25 * (2. * (j + 1.) - n * (n + 1.))
            ) - 1.
        )

    # sanity checks
    if n - m_abs < 0:
        raise ValueError("`n - |m|` cannot be negative")

    if (n - m_abs) % 2 != 0:
        raise ValueError("`n - |m|` cannot be odd")

    if j % 2 != 0:
        return -m_abs, n

    return m_abs, n


def mn_to_j(m: int, n:int) -> int:
    """
    """
    # check `n`
    if n < 0:
        raise ValueError(
            f"`n` must be positive; got n={n}"
        )

    # check valid Zernike pair
    if n - abs(m) < 0:
        raise ValueError("`n - |m|` cannot be negative")

    if (n - abs(m)) % 2 != 0:
        raise ValueError("`n - |m|` cannot be odd")

    # radial mode (|m| = 0)
    if m == 0:
        return int(0.5 * n * (n + 1.0) + 1.0)

    # first possible j for this |m|
    j = int(0.5 * n * (n + 1.0) + abs(m))

    # +ve m means cosine mode -> j is even
    if m > 0:
        if j % 2 == 0:
            return j

        return j + 1

    # -ve m means sine mode -> j is odd
    if j % 2 != 0:
        return j

    return j + 1
