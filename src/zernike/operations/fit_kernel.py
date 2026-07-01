from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from zernike.operations.aberration import Aberration
from zernike.utils.conversions import mn_to_j
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


    def fit_data(self) -> tuple[NDArray, NDArray, NDArray]:
        """
        """
        # 1- compute all aberrations (list of 2D arrays)
        data_list = self.compute_aberrations()

        # 2-
        #   a- flatten all 2D aberration arrays
        #   b- group them in a list
        #   c- apply the transpose of this list to turn rows
        #      into lists of aberration magnitudes at respective
        #      pixels
        A = np.asarray([
            aberration.flatten()
            for aberration in data_list
        ]).T

        # 3- flatten the real beam/kernel, 
        #    filtering out ingalid pixels
        B = self.kernel.flatten()

        mask = np.isfinite(B) & np.all(np.isfinite(A), axis=1)

        A_fit = A[mask, :]
        B_fit = B[mask]

        # 4- solve the linear least-squares problem
        weights, residuals, rank, singular_values = np.linalg.lstsq(
            A_fit, B_fit, rcond=None
        )

        # 5- reconstruct the fitted beam
        fitted_flat = np.full(
            B.shape, np.nan, dtype=np.result_type(A, B, float)
        )
        fitted_flat[mask] = A_fit @ weights
        fitted_kernel = fitted_flat.reshape(self.kernel.shape)

        residual_kernel = self.kernel - fitted_kernel

        return weights, fitted_kernel, residual_kernel

        #def wrapper(_xy, *weights) -> NDArray:
        #    """
        #    """
        #    weighted_data = np.asarray([
        #        aberration * weight
        #        for aberration, weight in zip(data_list, weights)
        #    ])

        #    return np.sum(weighted_data, axis=0).flatten()

        #x_meshed, y_meshed = np.meshgrid(
        #    self.aberration_list[0].dim_0_array,
        #    self.aberration_list[0].dim_1_array
        #)

        #xy = np.vstack(
        #    x_meshed.flatten(), y_meshed.flatten()
        #)

        #data_list = self.compute_aberrations(xy=xy)

        #return curve_fit(
        #    wrapper,
        #    xy, 
        #    self.kernel.flatten(), 
        #    p0=np.ones(len(self.j_list))
        #)


    def show(self, plot="kernel") -> None:
        """
        """
        plt.figure(figsize=(15, 15))
        ax = plt.subplot()
        ax.set_aspect("equal")

        if plot == "kernel":
            plt.title(f"kernel")

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


    @classmethod
    def via_n(cls, n_list: list[int], kernel_path: Path):
        """
        """
        j_list = []
        for n in n_list:
            if n % 2 == 0:
                m_list = [
                    m for m in range(n + 1) if m % 2 == 0
                ]

            else:
                m_list = [
                    m for m in range(n + 1) if m % 2 != 0
                ]

            for m in m_list:
                for item in mn_to_j(m, n):
                    j_list.append(item)

        return cls(j_list, kernel_path)
