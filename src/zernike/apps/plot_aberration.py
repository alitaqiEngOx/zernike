""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys

from zernike.operations.pipeline import plot_aberration


def main() -> int:
    """
    Pipeline entry point.
    """
    args = parse_args()

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
    --coords_type (optional): str
        `polar` or `cartesian`.
        (defaults to `polar`).

    --dim_0 (optional): float
        minimum, maximum, and step in dimension 0.
        (defaults to `None`).

    --dim_1 (optional): float
        minimum, maximum, and step in dimension 1.
        (defaults to `None`).

    --j: (optional) int
        order of the Zernike polynomial via `j`.
        (defaults to `None`).

    --mn: (optional) int
        order of the Zernike polynomial via `m` and `n`.
        (defaults to `None`).

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
        "--coords_type",
        type=str,
        default="polar",
        help="`polar` or `cartesian`",
    )
    parser.add_argument(
        "--dim_0",
        type=float,
        nargs=3,
        default=None,
        help="minimum, maximum and step in dimension 0",
    )
    parser.add_argument(
        "--dim_1",
        type=float,
        nargs=3,
        default=None,
        help="minimum, maximum and step in dimension 1",
    )
    parser.add_argument(
        '--j',
        type=int,
        default=None,
        help="Zernike polynomial via `j`",
    )
    parser.add_argument(
        '--mn',
        type=int,
        nargs=2,
        default=None,
        help="Zernike polynomial via `m` and `n`",
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
