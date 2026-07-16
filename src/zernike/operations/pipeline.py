""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import numpy as np
from pathlib import Path

from zernike.operations.aberration import Aberration
from zernike.operations.kernel import Kernel
from zernike.utils.conversions import (
    j_to_mn, mn_to_j
)


def convert(
        *, j: int | None=None,
        mn: list[int] | None=None
) -> None:
    """
    """
    if (j is None and mn is None) or\
    (j is not None and mn is not None):
        raise ValueError(
            "provide either `j` or `mn`"
        )

    if j is None:
        j = mn_to_j(mn[0], mn[1])
        print(f"j = {j}")
        return

    m, n = j_to_mn(j)
    print(f"m = {m}; n = {n}")


def estimate_beam(
        kernel_path: Path, *,
        j_list: list[str] | None=None,
        n_list: list[str] | None=None
) -> None:
    """
    """
    # filter out incorrect entries
    if (j_list is None and n_list is None) or\
    (j_list is not None and n_list is not None):
        raise ValueError(
            "provide either `j` or `mn`"
        )

    # define kernel in memory
    if j_list is None:
        k = Kernel.via_n(n_list, kernel_path)

    else:
        k = Kernel(j_list, kernel_path)

    # fit aberrations to kernel
    k.estimate()

    # show outputs
    k.show()
    k.show("fitted_kernel")
    k.show("residual_kernel")

    # show weights
    k.show_weights()


def plot_aberration(
        *, j: int,
        dim_0: list[float], dim_1: list[float],
        coords_type: str="polar"
) -> None:
    """
    Principal function in the pipeline executing the desired functionality.

    Arguments
    ---------
    j: int
        order of the Zernike polynomial.

    dim_0: list[float]
        minimum, maximum, and step in dimension 0.

    dim_1: list[float]
        minimum, maximum, and step in dimension 0.

    coords:_type str (optional)
        `polar` or `cartesian`.
    """
    for dim in [dim_0, dim_1]:
        if dim[0] >= dim[1]:
            raise ValueError(
                f"`dim[0] >= dim[1]` not allowed; got {dim}"
            )

        if dim[2] > dim[1] - dim[0]:
            raise ValueError(
                f"`dim[3] > dim[1] - dim[2]` not allowed; got {dim}"
            )

    if coords_type.lower() == "polar":
        dim_0[0] = max(dim_0[0], 0.)
        dim_1[0] = max(dim_1[0], 0.)
        dim_1[1] = min(dim_1[1], 2. * np.pi)

    z = Aberration(
        j,
        np.arange(dim_0[0], dim_0[1] + dim_0[2], dim_0[2]),
        np.arange(dim_1[0], dim_1[1] + dim_1[2], dim_1[2]),
        coords_type=coords_type
    )
    z.show()
