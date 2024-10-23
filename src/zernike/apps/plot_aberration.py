import argparse
import sys

from zernike.operations.pipeline import (
    plot_aberration
)


def main() -> int:
    """
    Pipeline entry point.
    """
    args = parse_args()

    plot_aberration(
        j=args.j, radius_max=args.max_radius, radius_step=args.radius_step, 
        num_angles=args.num_angles
    )

    return 0


def parse_args() -> argparse.Namespace:
    """
    Parses command line arguments.

    cmd Arguments
    -------------
    j: int
        order of the Zernike polynomial.

    --max_radius (optional): float
        maximum radius to be included in the plot
        (defaults to 1.0).

    --num_angles (optional): int
        number of angles to be computed between 0 deg and 360 deg
        (defaults to 100).

    --radius_step (optional): float
        numerical step in the radius domain
        (defaults to 0.01).

    Returns
    -------
    argparse.Namespace class instance enclosing the parsed
    cmd arguments.
    """
    parser = argparse.ArgumentParser(
        description="Zernike aberration plots",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'j',
        type=int,
        help="order of the Zernike polynomial",
    )
    parser.add_argument(
        "--max_radius",
        type=float,
        default=1.,
        help="maximum radius to be included in the plot",
    )
    parser.add_argument(
        "--num_angles",
        type=int,
        default=500,
        help="number of angles to be computed between 0 deg and 360 deg",
    )
    parser.add_argument(
        "--radius_step",
        type=float,
        default=0.01,
        help="numerical step in the radius domain",
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
