""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from numpy.typing import NDArray
from scipy.optimize import curve_fit

from zernike.operations.aberration import Aberration
from zernike.utils.conversions import mn_to_j
from zernike.utils.txt import read_data


class Kernel:
    """
    """

    def __init__(self, j_list: list[int], kernel_path: Path):
        """
        """
        self.j_list = j_list

        if kernel_path.suffix == ".txt":
            self.real_kernel = read_data(kernel_path)

        else:
            self.real_kernel = np.load(kernel_path)

        # temporary code
        self.real_kernel = np.absolute(self.real_kernel)
        self.fitted_kernel = None
        self.residual_kernel = None
        self.weights = None

        dim = np.linspace(
            -0.5 * np.sqrt(2.),
            0.5 * np.sqrt(2.),
            self.real_kernel.shape[0]
        )

        self.aberration_list = [
            Aberration(j, dim, dim, "cartesian")
            for j in j_list
        ]


    def compute_aberrations(
            self, *, xy: tuple[NDArray] | None=None 
    ) -> NDArray:
        """
        """
        for item in self.aberration_list:
            item.compute(xy=xy)

        return np.asarray([
            item.data
            for item in self.aberration_list
        ])


    def estimate(self, *, curvefit: bool=False) -> None:
        """
        """
        # kernels already estimated
        if self.fitted_kernel is not None:
            return

        # compute all aberrations & flatten/transpose them     
        aberrations = self.compute_aberrations()

        flattened_aberrations = np.asarray([
            aberration.flatten()
            for aberration in aberrations
        ]).T

        # use `scipy.optimize.curve_fit`
        if curvefit:
            # define a wrapper function, passing all `weights`
            # together with a `_dummy` as required by `curve_fit`
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
            self.weights, _ = curve_fit(
                wrapper, xy, self.real_kernel.flatten(),
                p0=np.ones(len(self.j_list))
            )

        # use `numpy.linalg.lstsq`
        else:
            # compute weights
            self.weights, *_ = np.linalg.lstsq(
                flattened_aberrations, self.real_kernel.flatten(),
                rcond=None
            )

        # reconstruct & return the fitted beam
        fitted_kernel_flat = flattened_aberrations @ self.weights

        self.fitted_kernel = fitted_kernel_flat.reshape(
            self.real_kernel.shape
        )
        self.residual_kernel = (
            self.real_kernel - self.fitted_kernel
        )


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


    def show(self, type: str="real_kernel") -> None:
        """
        """
        # filter incorrect entries
        if type not in [
            "real_kernel", "fitted_kernel", "residual_kernel"
        ]:
            raise ValueError(
                "`type` must be either `real_kernel`, `fitted_kernel` "
                "or `residual_kernel`"
            )

        if (
            type == "fitted_kernel" and self.fitted_kernel is None
        ) or (
            type == "residual_kernel" and self.residual_kernel is None
        ):
            raise TypeError("kernel has not yet been fitted")

        # plot
        plt.figure(figsize=(15, 15))
        ax = plt.subplot()
        ax.set_aspect("equal")

        norm = Normalize(
            vmin = np.min(self.real_kernel),
            vmax = np.max(self.real_kernel)
        )

        plt.title(f"{type.replace('_', ' ')}")

        if type == "real_kernel":
            x = self.real_kernel

        elif type == "fitted_kernel":
            x = self.fitted_kernel

        else:
            x = self.residual_kernel

        c = plt.imshow(x, cmap="hot_r", norm=norm)

        plt.colorbar(c)
        plt.show()

        #else:
        #    if plot == "aberration_sum":
        #        plt.title(f"summation of j={self.j_list} aberrations")

        #        c = plt.pcolormesh(
        #            self.aberration_list[0].meshed_arrays[0],
        #            self.aberration_list[0].meshed_arrays[1],
        #            np.sum(self.compute_aberrations(), axis=0),
        #            shading="auto", cmap="hot_r"
        #        )

        #    elif plot == "avg_aberration_sum":
        #        plt.title(f"averaged summation of j={self.j_list} aberrations")

        #        c = plt.pcolormesh(
        #            self.aberration_list[0].meshed_arrays[0],
        #            self.aberration_list[0].meshed_arrays[1],
        #            np.sum(self.compute_aberrations(), axis=0) / len(self.j_list),
        #            shading="auto", cmap="hot_r"
        #        )


    def show_weights(self) -> None:
        """
        """
        if self.weights is None:
            raise TypeError("kernel has not yet been fitted")

        plt.figure(figsize=(12, 6))
        ax = plt.subplot()

        ax.bar(self.j_list, self.weights)
        ax.axhline(0., linewidth=1.)

        ax.set_xlabel("j")
        ax.set_ylabel("weight")
        ax.set_title("Fitted Zernike weights")

        ax.set_xticks(self.j_list)
        ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()
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
