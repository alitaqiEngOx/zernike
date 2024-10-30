import argparse
import sys

from zernike.operations.pipeline import convert


def main() -> int:
    """
    Pipeline entry point.
    """
    args = parse_args()

    if args.j is None and args.mn is None:
        raise ValueError(
            "expected either `j` or `mn` but got neither"
        )

    elif args.j is not None and args.mn is not None:
        raise ValueError(
            "expected either `j` or `mn` but got both"
        )

    if args.j is None:
        convert(mn=args.mn)

    else:
        convert(j=args.j)

    return 0


def parse_args() -> argparse.Namespace:
    """
    Parses command line arguments.

    cmd Arguments
    -------------
    --j (optional): int
        order of the Zernike polynomial via `j`.

    --mn (optional): int
        order of the Zernike polynomial via `m` & `n`.

    Returns
    -------
    argparse.Namespace class instance enclosing the parsed
    cmd arguments.
    """
    parser = argparse.ArgumentParser(
        description="j <--> m/n converter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--j",
        type=int,
        default=None,
        help="`j` (Noll indexing scheme)",
    )
    parser.add_argument(
        "--mn",
        type=int,
        default=None,
        nargs=2,
        help="`m` & `n` (Noll indexing scheme)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
