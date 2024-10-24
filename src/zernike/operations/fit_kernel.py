from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from zernike.operations.aberration import Aberration


class FitKernel:
    """
    """

    def __init__(
            self, j_list: list[int]

    ):
        """
        """
        self.j_list = j_list

        dim = np.linspace(
            -0.5 * np.sqrt(2.),
            0.5 * np.sqrt(2.) + 0.01,
            200
        )

        self.aberration_list = [
            Aberration(j, dim, dim, "cartesian")
            for j in j_list
        ]


    def compute(self) -> None:
        """
        """
        for item in self.aberration_list:
            item.compute()

        return np.asarray([
            item.data
            for item in self.aberration_list
        ])


    def show_sum(self) -> None:
        """
        """
        plt.figure(figsize=(15, 15))
        ax = plt.subplot()
        ax.set_aspect("equal")
        plt.title(f"summation of j={self.j_list} aberrations")

        c = plt.pcolormesh(
            self.aberration_list[0].meshed_arrays[0],
            self.aberration_list[0].meshed_arrays[1],
            np.sum(self.compute(), axis=0),
            shading="auto", cmap="hot_r"
        )
        plt.colorbar(c)
        plt.show()


    def show_averaged_sum(self) -> None:
        """
        """
        plt.figure(figsize=(15, 15))
        ax = plt.subplot()
        ax.set_aspect("equal")
        plt.title(f"summation of j={self.j_list} aberrations")

        c = plt.pcolormesh(
            self.aberration_list[0].meshed_arrays[0],
            self.aberration_list[0].meshed_arrays[1],
            np.sum(self.compute(), axis=0) / len(self.j_list),
            shading="auto", cmap="hot_r"
        )
        plt.colorbar(c)
        plt.show()
