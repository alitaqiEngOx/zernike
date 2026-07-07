from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from scipy.optimize import curve_fit

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


    def fit_data(
            self, *, curvefit: bool=False
    ) -> tuple[NDArray, NDArray, NDArray]:
        """
        """
        # compute all aberrations & flatten/transpose them     
        aberrations = self.compute_aberrations()

        flattened_aberrations = np.asarray([
            aberration.flatten()
            for aberration in aberrations
        ]).T

        # use `scipy.optimize.curve_fit`
        if curvefit:
            # define a wrapper function, passing all `weights` together
            # with a `_dummy` as required by `curve_fit`
            def wrapper(
                    _dummy: NDArray, *weights: float
            ) -> NDArray:
                """
                """
                return flattened_aberrations @ np.asarray(weights)

            # constryct xy domain as required by `curve_fit`
            x_meshed, y_meshed = np.meshgrid(
                self.aberration_list[0].dim_0_array,
                self.aberration_list[0].dim_1_array
            )

            xy = np.vstack((
                x_meshed.flatten(), y_meshed.flatten()
            ))

            # compute weights
            weights, _ = curve_fit(
                wrapper, xy, self.kernel.flatten(),
                p0=np.ones(len(self.j_list))
            )

        # use `numpy.linalg.lstsq`
        else:
            # compute weights
            weights, *_ = np.linalg.lstsq(
                flattened_aberrations, self.kernel.flatten(),
                rcond=None
            )

        # reconstruct & return the fitted beam
        fitted_kernel_flat = flattened_aberrations @ weights
        fitted_kernel = fitted_kernel_flat.reshape(self.kernel.shape)
        residual_kernel = self.kernel - fitted_kernel

        return weights, fitted_kernel, residual_kernel


    def compare_curve_fit_and_lstsq(self) -> None:
        """
        """
        result_curve_fit = self.fit_data(curvefit=True)
        result_lstsq = self.fit_data()      

        # print comparison
        print("\ncurve_fit weights:")
        print(result_curve_fit[0])

        print("Linear least-squares weights:")
        print(result_lstsq[0])

        print("\nDifference:")
        print(result_curve_fit[0] - result_lstsq[0])


    def show(self, plot="kernel") -> None:
        """
        """
        plt.figure(figsize=(15, 15))
        ax = plt.subplot()
        ax.set_aspect("equal")

        if plot == "kernel":
            plt.title(f"kernel")

            c = plt.imshow(self.kernel, cmap="hot_r", vmin=0., vmax=1.)

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
