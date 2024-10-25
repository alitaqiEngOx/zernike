from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

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

        dim = np.linspace(
            -0.5 * np.sqrt(2.),
            0.5 * np.sqrt(2.) + 0.01,
            200
        )

        self.aberration_list = [
            Aberration(j, dim, dim, "cartesian")
            for j in j_list
        ]


    def compute_aberrations(self) -> None:
        """
        """
        for item in self.aberration_list:
            item.compute()

        return np.asarray([
            item.data
            for item in self.aberration_list
        ])


    def show(self, plot="kernel") -> None:
        """
        """
        plt.figure(figsize=(15, 15))
        ax = plt.subplot()
        ax.set_aspect("equal")

        if plot == "kernel":
            plt.title(f"sampled data")

            c = plt.imshow(self.kernel)
            plt.axis("off")

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
