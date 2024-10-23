import argparse
import sys
from pathlib import Path

from zernike.operations.pipeline import estimate_beam


def main() -> int:
    """
    Pipeline entry point.
    """
    args = parse_args()

    estimate_beam(j=args.j, data_path=args.sampled_data_path)

    print(args.j)

    return 0


def parse_args() -> argparse.Namespace:
    """
    Parses command line arguments.

    j: int
        orders of Zernike polynomials (as many as desired).

    --sampled_data_path (optional): str
        `.txt` file bearing the sampled data.

    cmd Arguments
    -------------
    """
    parser = argparse.ArgumentParser(
        description="Estimates beam data with Zernike polynomials",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'j',
        type=int,
        nargs='*',
        help="Zernike polynomials (as many as desired)"
    )
    parser.add_argument(
        "--sampled_data_path",
        type=str,
        default=f"{Path(__file__).parents[3].joinpath('data', 'sampled_beam.txt')}",
        help="`.txt` file bearing the sampled data"
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
