from dataclasses import dataclass
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from zernike.operations.zernike import Zernike


@dataclass
class FitKernel:
    """
    """

    j_list: list[int]
    """ """

    data_list: Optional[list[NDArray]] = None
    """ """


    @property
    def aberration_object_list(self) -> list[Zernike]:
        """
        """
        dim = np.linspace(
            -0.5 * np.sqrt(2.),
            0.5 * np.sqrt(2.) + 0.01,
            200
        )

        return [
            Zernike(j, dim, dim, "cartesian")
            for j in self.j_list
        ]


    def compute(self) -> None:
        """
        """
        for item in self.aberration_object_list:
            item.compute()
        
        self.data_list = [
            item.data 
            for item in self.aberration_object_list
        ]


    def show_sum(self) -> None:
        """
        """


            