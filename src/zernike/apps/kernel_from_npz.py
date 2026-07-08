""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys
from pathlib import Path

from zernike.utils.npz import NPZ


def main() -> int:
    """
    """
    args = parse_args()

    npz = NPZ(Path(args.path))

    if args.show_info:
        info = [
            item.split(':', maxsplit=1)
            for item in npz.keys_and_shapes
        ]

        key_width = max(
            len(key) for key, _ in info
        )

        print(f"{'key':<{key_width}} : shape")

        for key, shape in info:
            print(f"{key:<{key_width}} : {shape}")

    if args.save_as:
        npz.dump(
            Path(args.save_as), key=args.key,
            index=args.index
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
        nargs='*',
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
