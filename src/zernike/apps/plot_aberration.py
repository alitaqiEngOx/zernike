import argparse
import sys

import numpy as np

from zernike.operations.pipeline import plot_aberration


def main() -> int:
    """
    Pipeline entry point.
    """
    args = parse_args()

    if args.coords_type.lower() == "cartesian" and\
    args.dim_0 == [0., 1., 0.01] and\
    args.dim_1 == [0., 2. * np.pi, 0.01]:
        args.dim_0 = [
            -0.5 * np.sqrt(2.), 0.5 * np.sqrt(2.), 0.01
        ]
        args.dim_1 = args.dim_0

    plot_aberration(
        j=args.j, dim_0=args.dim_0, dim_1=args.dim_1,
        coords_type=args.coords_type
    )

    return 0


def parse_args() -> argparse.Namespace:
    """
    Parses command line arguments.

    cmd Arguments
    -------------
    j: int
        order of the Zernike polynomial.

    --coords_type (optional): str
        `polar` or `cartesian`.
        (defaults to `polar`).

    --dim_0 (optional): float
        minimum, maximum, and step in dimension 0.
        (defaults to [0., 1., 0.01] if --coords_type is `polar`
        and [-0.5 * np.sqrt(2.), -0.5 * np.sqrt(2.), 0.01] 
        if --coords_type is `cartesian`).

    --dim_1 (optional): float
        minimum, maximum, and step in dimension 1.
        (defaults to [0., 2. * np.pi, 0.01] if --coords_type is `polar`
        and [-0.5 * np.sqrt(2.), -0.5 * np.sqrt(2.), 0.01] 
        if --coords_type is `cartesian`).

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
        "--coords_type",
        type=str,
        default="polar",
        help="`polar` or `cartesian`",
    )
    parser.add_argument(
        "--dim_0",
        type=float,
        nargs=3,
        default=[0., 1., 0.01],
        help="minimum, maximum, and step in dimension 0",
    )
    parser.add_argument(
        "--dim_1",
        type=float,
        nargs=3,
        default=[0., 2. * np.pi, 0.01],
        help="minimum, maximum, and step in dimension 1",
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
