import math

import matplotlib.pyplot as plt
import numpy as np


def n_and_m(j: int) -> tuple[int, int]:
    """
    Computes non-negative integers `n` and `m` from `j`.

    Arguments
    ---------
    j: int
        order of the Zernike polynomial.

    Returns
    -------
    values for `n` and `m`

    Raises
    ------
    ValueError 
    """
    n = np.floor(
        (np.sqrt(2. * j - 1.) + 0.5) - 1.
    )

    if n < 0:
        raise ValueError("`n` cannot be negative")

    if n % 2 == 0:
        m = 2. * np.floor(
            0.25 * (2. * j + 1. - n * (n + 1.))
        )
    
    else:
        m = 2. * np.floor(
            0.25 * (2. * (j + 1.) - n * (n + 1.))
        ) - 1.

    if n - m < 0:
        raise ValueError("`n - m` cannot be negative")

    if (n - m) % 2 != 0:
        raise ValueError("`n - m` cannot be odd")

    return int(n), int(m)


def R(rho: float, n: int, m: int) -> float:
    """
    Computes `R`.

    Arguments
    ---------
    rho: float
        radius value.

    n: int
        value for `n`.

    m: int
        value for `m`.

    Returns
    -------
    value for `R`.
    """
    output = 0

    for s in range(int(0.5 * (n - m) + 1)):
        factor = (
            ((-1.)**s) * 
            math.factorial(n - s)
        ) / (
            math.factorial(s) * 
            math.factorial(int(((n + m) / 2) - s)) * 
            math.factorial(int(((n - m) / 2) - s))
        )

        output += factor * rho**(n - (2. * s))

    return output


def Z(rho: float, theta: float, *, j: int) -> float:
    """
    Computes the Zernike polynomial value at given radius and angle positions.

    Arguments
    ---------
    rho: float
        radius value.

    theta: float
        angle value (in radians).

    j: int
        order of the Zernike polynomial.

    Returns
    -------
    value for `R`.
    """
    n, m = n_and_m(j)
    r = R(rho, n, m)
    
    if m == 0:
        return np.sqrt(n + 1.) * r
    
    if j % 2 == 0:
        return np.sqrt(2. * (n + 1.)) * r * np.cos(m * theta)
    
    return np.sqrt(2. * (n + 1.)) * r * np.sin(m * theta)


def run(
        *, j: int, rho: float, rho_step: float, num_theta: int
) -> None:
    """
    Principal function in the pipeline executing the desired functionality.

    Arguments
    ---------
    j: int
        order of the Zernike polynomial.

    rho: float
        maximum radius to be included in the plot.

    rho_step: float
        numerical step in the radius domain.

    num_theta: int
        number of angles to be computed between 0 deg and 360 deg.
    """
    rho_array = np.arange(0., rho + rho_step, rho_step)
    theta_array = np.linspace(0., 2.*np.pi, num_theta)

    Rho, Theta = np.meshgrid(rho_array, theta_array)

    z = Z(Rho, Theta, j=j)

    plt.figure(figsize=(15, 15))
    plt.subplot(projection="polar")
    c = plt.pcolormesh(Theta, Rho, z, shading="auto", cmap="hot_r")
    plt.colorbar(c)
    plt.title(f"j = {j}")
    plt.show()