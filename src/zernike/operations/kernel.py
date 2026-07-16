""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from numpy.typing import NDArray
from scipy.optimize import curve_fit

from zernike.operations.aberration import Aberration
from zernike.utils.txt import read_data


class Kernel:
    """
    """

    def __init__(
            self, j_list: list[int], kernel_path: Path
    ):
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
        # if kernels already estimated
        if self.fitted_kernel is not None:
            return

        # 1- compute & flatten/transpose all aberrations
        aberrations = self.compute_aberrations()

        flattened_aberrations = np.asarray([
            aberration.flatten()
            for aberration in aberrations
        ]).T

        # if `scipy.optimize.curve_fit` requested
        if curvefit:
            # 2a.1- define a wrapper function, passing all `weights`
            # together with a `_dummy` as required by `curve_fit`
            def wrapper(
                    _dummy: NDArray, *weights: float
            ) -> NDArray:
                """
                """
                return flattened_aberrations @ np.asarray(weights)

            # 2a.2- constryct xy domain as required by `curve_fit`
            x_meshed, y_meshed = np.meshgrid(
                self.aberration_list[0].dim_0_array,
                self.aberration_list[0].dim_1_array
            )

            xy = np.vstack((
                x_meshed.flatten(), y_meshed.flatten()
            ))

            # 2a.3- compute weights
            self.weights, _ = curve_fit(
                wrapper, xy, self.real_kernel.flatten(),
                p0=np.ones(len(self.j_list))
            )

        # if `numpy.linalg.lstsq` requested
        else:
            # 2b.1- compute weights
            self.weights, *_ = np.linalg.lstsq(
                flattened_aberrations, self.real_kernel.flatten(),
                rcond=None
            )

        # 3- reconstruct & store the fitted beam
        fitted_kernel_flat = flattened_aberrations @ self.weights

        self.fitted_kernel = fitted_kernel_flat.reshape(
            self.real_kernel.shape
        )
        self.residual_kernel = (
            self.real_kernel - self.fitted_kernel
        )


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
            type == "fitted_kernel" and 
            self.fitted_kernel is None
        ) or (
            type == "residual_kernel" and 
            self.residual_kernel is None
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
            if n < 0:
                raise ValueError(
                    f"`n` must be non-negative; got n={n}"
                )

            j_min = n * (n + 1) // 2 + 1
            j_max = (n + 1) * (n + 2) // 2

            j_list.extend(
                range(j_min, j_max + 1)
            )

        return cls(j_list, kernel_path)


def compare_curve_fit_and_lstsq(
        j_list: list[int], kernel_path: Path
) -> None:
    """
    """
    k_curve_fit = Kernel(j_list, kernel_path)
    k_lstsq = Kernel(j_list, kernel_path)

    k_curve_fit.estimate(curvefit=True)
    k_lstsq.estimate()

    # print comparison
    print("\n`scipy.optimize.curve_fit` weights:")
    print(k_curve_fit.weights)

    print("`numpy.linalg.lstsq` weights:")
    print(k_lstsq.weights)

    print("\ndifference:")
    print(k_curve_fit.weights - k_lstsq.weights)
