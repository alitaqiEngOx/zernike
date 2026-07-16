""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys
from pathlib import Path

from zernike.operations.pipeline import kernel_from_npz


def main() -> int:
    """
    """
    args = parse_args()

    kernel_from_npz(
        Path(args.path), show_info=args.show_info,
        key=args.key, index=args.index,
        save_as=Path(args.save_as)
    )

    return 0


def parse_args() -> argparse.Namespace:
    """
    """
    parser = argparse.ArgumentParser(
        description="Extracts kernel from `.npz`",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "path",
        type=str,
        help="`.npz` path"
    )
    parser.add_argument(
        "--key",
        type=str,
        default=None,
        help="`.npz` array key to extract from"
    )
    parser.add_argument(
        "--index",
        nargs='+',
        default=None,
        help="position indices for the kernel to be extracted"
    )
    parser.add_argument(
        "--save_as",
        type=str,
        default=None,
        help="output filename & path"
    )
    parser.add_argument(
        "--show_info",
        action="store_true",
        help="display keys & shapes of your `.npz`"
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
