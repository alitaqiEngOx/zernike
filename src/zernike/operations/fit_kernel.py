from dataclasses import dataclass

import numpy as np

from zernike.operations.zernike import Zernike


@dataclass
class FitKernel:
    """
    """

    j_list: list[int]
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
    
    def compute_sum(self) -> None:
        """
        """
        for item in self.aberration_object_list:
            item.compute()
        
        return [
            item.data 
            for item in self.aberration_object_list
        ]
            