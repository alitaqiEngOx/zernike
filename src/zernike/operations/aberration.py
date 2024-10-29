import math
from dataclasses import dataclass
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from zernike.utils.conversions import cartesian_to_polar


@dataclass
class Aberration:
    """
    """

    j: int
    """ """

    dim_0_array: NDArray
    """ """

    dim_1_array: NDArray
    """ """

    coords_type: str = "polar"
    """ """

    data: Optional[NDArray] = None
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


    @property
    def meshed_arrays(self) -> tuple[NDArray, NDArray]:
        """
        """
        return np.meshgrid(
            self.dim_0_array, self.dim_1_array
        )


    def R(self, radius: float) -> float:
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


    def compute(self, *, xy: Optional[tuple[NDArray]]=None) -> None:
        """
        """
        if xy is None:
            # polar frame
            if self.coords_type.lower() == "polar":
                r_meshed, theta_meshed = self.meshed_arrays

            # cartesian frame
            elif self.coords_type.lower() == "cartesian":
                x_meshed, y_meshed = self.meshed_arrays
                r_meshed_ravelled, theta_meshed_ravelled = cartesian_to_polar(
                    x_meshed.ravel(), y_meshed.ravel()
                )

                r_meshed = r_meshed_ravelled.reshape(
                    self.dim_1_array.shape[0], self.dim_0_array.shape[0]
                )
                theta_meshed = theta_meshed_ravelled.reshape(
                    self.dim_1_array.shape[0], self.dim_0_array.shape[0]
                )

            # unsupported frames
            else:
                raise ValueError(
                    f"unsupported coordinate type '{self.coords_type}'"
                )

        else:
            x_meshed_ravelled, y_meshed_ravelled = xy

            r_meshed_ravelled, theta_meshed_ravelled = cartesian_to_polar(
                x_meshed_ravelled, y_meshed_ravelled
            )

            r_meshed = r_meshed_ravelled.reshape(
                self.dim_1_array.shape[0], self.dim_0_array.shape[0]
            )
            theta_meshed = theta_meshed_ravelled.reshape(
                self.dim_1_array.shape[0], self.dim_0_array.shape[0]
            )

        if self.m == 0:
                self.data = np.sqrt(self.n + 1.) * self.R(r_meshed)

        else:
            if self.j % 2 == 0:
                self.data = np.sqrt(2. * (self.n + 1.)) *\
                    self.R(r_meshed) *\
                        np.cos(self.m * theta_meshed)

            else:
                self.data = np.sqrt(2. * (self.n + 1.)) *\
                    self.R(r_meshed) *\
                        np.sin(self.m * theta_meshed)


    def show(self) -> None:
        """
        """
        if self.data is None:
            self.compute()

        dim_0_meshed, dim_1_meshed = self.meshed_arrays
        plt.figure(figsize=(15, 15))

        # polar frame
        if self.coords_type.lower() == "polar":
            plt.subplot(projection="polar")
            plt.title(f"j = {self.j}")

            c = plt.pcolormesh(
                dim_1_meshed, dim_0_meshed, self.data, 
                shading="auto", cmap="hot_r"
            )

        # cartesian frame
        elif self.coords_type.lower() == "cartesian":
            ax = plt.subplot()
            ax.set_aspect("equal")
            plt.title(f"j = {self.j} - Cartesian")

            c = plt.pcolormesh(
                dim_0_meshed, dim_1_meshed, self.data, 
                shading="auto", cmap="hot_r"
            )

        # unsupported frames
        else:
            raise ValueError(
                f"unsupported coordinate type '{self.coords_type}'"
            )

        plt.colorbar(c)
        plt.show()
