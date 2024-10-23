import argparse
import sys
from pathlib import Path


def main() -> int:
    """
    Pipeline entry point.
    """
    args = parse_args()

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
        help="Zernike polynomials (as many as desired)",
    )
    parser.add_argument(
        "--sampled_data_path",
        type=int,
        default=f"{Path(__file__).parents[3].joinpath('data', 'sampled_beam.txt')}"
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
