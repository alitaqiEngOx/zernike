import math
from dataclasses import dataclass
from typing import Optional

import numpy as np
from numpy.typing import NDArray


@dataclass
class Zernike:
    """
    """

    j: int
    """ """

    radius_array: NDArray
    """ """

    angle_array: NDArray
    """ """

    z: Optional[NDArray] = None
    """ """

    @property
    def m(self) -> int:
        """
        Computes non-negative integer `m`.

        Returns
        -------
        `m`.

        Raises
        ------
        ValueError
        """
        if self.n % 2 == 0:
            m = 2. * np.floor(
                0.25 * (2. * self.j + 1. - self.n * (self.n + 1.))
            )
        
        else:
            m = 2. * np.floor(
                0.25 * (2. * (self.j + 1.) - self.n * (self.n + 1.))
            ) - 1.

        if self.n - m < 0:
            raise ValueError("`n - m` cannot be negative")

        if (self.n - m) % 2 != 0:
            raise ValueError("`n - m` cannot be odd")
        
        return int(m)


    @property
    def n(self) -> int:
        """
        Computes non-negative integer `n`.

        Returns
        -------
        `n`.

        Raises
        ------
        ValueError
        """
        n = np.floor(
            (np.sqrt(2. * self.j - 1.) + 0.5) - 1.
        )

        if n < 0:
            raise ValueError("`n` cannot be negative")

        return int(n)
    

    def R(self, radius: NDArray) -> NDArray:
        """
        Computes `R` at a given radius value.

        Returns
        -------
        `R`.
        """        
        output = 0

        for s in range(int(0.5 * (self.n - self.m) + 1)):
            factor = (
                ((-1.)**s) * 
                math.factorial(self.n - s)
            ) / (
                math.factorial(s) * 
                math.factorial(int(((self.n + self.m) / 2) - s)) * 
                math.factorial(int(((self.n - self.m) / 2) - s))
            )

            output += factor * radius**(self.n - (2. * s))

        return output


    def compute(self) -> NDArray:
        """
        """
        radius_array_meshed, angle_array_meshed = np.meshgrid(
            self.radius_array, self.angle_array
        )

        r = self.R(radius_array_meshed)

        if self.m == 0:
            return np.sqrt(self.n + 1.) * r

        if self.j % 2 == 0:
            return np.sqrt(2. * (self.n + 1.)) * r * np.cos(self.m * angle_array_meshed)

        return np.sqrt(2. * (self.n + 1.)) * r * np.sin(self.m * angle_array_meshed)