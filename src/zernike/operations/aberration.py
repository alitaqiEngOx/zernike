""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import math
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from zernike.utils.conversions import (
    cartesian_to_polar, j_to_mn, mn_to_j
)


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

    coords_type: str="polar"
    """ """

    basis: str="real"
    """ """

    data: NDArray | None=None
    """ """


    def __post_init__(self) -> None:
        """
        """
        if self.j < 1:
            raise ValueError(
                f"`j` must be >= 1; got j={self.j}"
            ) 


    @property
    def m(self) -> int:
        """
        Computes `m` from Noll index `j`.

        Returns
        -------
        `m`.
        """
        m, _ = j_to_mn(self.j)
        return m


    @property
    def n(self) -> int:
        """
        Computes `n` from Noll index `j`.

        Returns
        -------
        `n`.
        """
        _, n = j_to_mn(self.j)
        return n


    @property
    def meshed_arrays(self) -> tuple[NDArray, NDArray]:
        """
        """
        return np.meshgrid(
            self.dim_0_array, self.dim_1_array
        )


    def R(
            self, radius: float | NDArray
    ) -> float | NDArray:
        """
        Computes `R` at a given radius value.

        Returns
        -------
        `R`.
        """
        n = self.n
        m_abs = abs(self.m)   
        output = 0.

        for s in range(int(0.5 * (n - m_abs) + 1)):
            factor = (
                ((-1.)**s) * 
                math.factorial(n - s)
            ) / (
                math.factorial(s) * 
                math.factorial(int(((n + m_abs) / 2) - s)) * 
                math.factorial(int(((n - m_abs) / 2) - s))
            )

            output += factor * radius**(n - (2. * s))

        return output


    def compute(
            self, *, xy: tuple[NDArray, NDArray] | None=None
    ) -> None:
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

        if self.basis == "complex":
            pass

        else:
            n = self.n
            m = self.m
            R = self.R(r_meshed)

            if m == 0:
                self.data = np.sqrt(self.n + 1.) * R

            elif m > 0:
                self.data = (
                    np.sqrt(2. * (n + 1.)) * R *
                    np.cos(abs(m) * theta_meshed)
                )

            else:
                self.data = (
                    np.sqrt(2. * (n + 1.)) * R *
                    np.sin(abs(m) * theta_meshed)
                )


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
            plt.title(
                f"j={self.j}; mn=({self.m}; {self.n}) - polar"
            )

            c = plt.pcolormesh(
                dim_1_meshed, dim_0_meshed, self.data, 
                shading="auto", cmap="hot_r"
            )

        # cartesian frame
        elif self.coords_type.lower() == "cartesian":
            ax = plt.subplot()
            ax.set_aspect("equal")
            plt.title(
                f"j={self.j}; mn=({self.m}; {self.n}) - cartesian"
            )

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


    @classmethod
    def via_mn(
        cls, mn: tuple[int],
        dim_0_array: NDArray,
        dim_1_array: NDArray,
        coords_type: str="polar",
        basis: str="real",
        data: NDArray | None=None
    ):
        """
        """
        m, n = mn
        j = mn_to_j(m, n)

        return cls(
            j, dim_0_array, dim_1_array,
            coords_type, basis, data
        )
