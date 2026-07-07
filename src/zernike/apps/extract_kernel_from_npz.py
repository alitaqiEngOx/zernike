""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys


def main() -> int:
    """
    """
    args = parse_args()

    return 0

def parse_args() -> argparse.Namespace:
    """
    """
    parser = argparse.ArgumentParser(
        description="Extracts kernel from `.npz`",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--path",
        type=int,
        help="`.npz` path"
    )
    parser.add_argument(
        "--index",
        nargs='*',
        help="position indices for the kernel to be extracted"
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())