from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from scipy.optimize import curve_fit

from zernike.operations.aberration import Aberration
from zernike.utils.txt import read_data


class FitKernel:
    """
    """

    def __init__(self, j_list: list[int], kernel_path: Path):
        """
        """
        self.j_list = j_list

        if kernel_path.suffix == ".txt":
            self.kernel = read_data(kernel_path)

        else:
            self.kernel = np.load(kernel_path)

        # temporary code
        self.kernel = np.absolute(self.kernel)

        dim = np.linspace(
            -0.5 * np.sqrt(2.),
            0.5 * np.sqrt(2.),
            self.kernel.shape[0]
        )

        self.aberration_list = [
            Aberration(j, dim, dim, "cartesian")
            for j in j_list
        ]


    def compute_aberrations(
            self, *, xy: Optional[tuple[NDArray]]=None 
    ) -> NDArray:
        """
        """
        for item in self.aberration_list:
            item.compute(xy=xy)

        return np.asarray([
            item.data
            for item in self.aberration_list
        ])


    def fit_data(self) -> tuple[NDArray]:
        """
        """
        def wrapper(xy, *args) -> NDArray:
            """
            """
            data_list = self.compute_aberrations(xy=xy)

            data_list = np.asarray([
                item * arg
                for item, arg in zip(data_list, args)
            ])

            return np.sum(data_list, axis=0).flatten()

        x_meshed, y_meshed = np.meshgrid(
            self.aberration_list[0].dim_0_array,
            self.aberration_list[0].dim_1_array
        )

        return curve_fit(
            wrapper,
            np.vstack((x_meshed.flatten(), y_meshed.flatten())), 
            self.kernel.flatten(), 
            p0=np.ones(len(self.j_list))
        )


    def show(self, plot="kernel") -> None:
        """
        """
        plt.figure(figsize=(15, 15))
        ax = plt.subplot()
        ax.set_aspect("equal")

        if plot == "kernel":
            plt.title(f"sampled data")

            c = plt.imshow(self.kernel, cmap="hot_r")

        else:
            if plot == "aberration_sum":
                plt.title(f"summation of j={self.j_list} aberrations")

                c = plt.pcolormesh(
                    self.aberration_list[0].meshed_arrays[0],
                    self.aberration_list[0].meshed_arrays[1],
                    np.sum(self.compute_aberrations(), axis=0),
                    shading="auto", cmap="hot_r"
                )

            elif plot == "avg_aberration_sum":
                plt.title(f"averaged summation of j={self.j_list} aberrations")

                c = plt.pcolormesh(
                    self.aberration_list[0].meshed_arrays[0],
                    self.aberration_list[0].meshed_arrays[1],
                    np.sum(self.compute_aberrations(), axis=0) / len(self.j_list),
                    shading="auto", cmap="hot_r"
                )

        plt.colorbar(c)
        plt.show()
