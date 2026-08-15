""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys
import time

from zernike.operations.pipeline import convert
from zernike.utils import log_handler


def main() -> int:
    """
    Pipeline entry point.
    """
    # start timer
    start_time = time.time()

    # activate logger
    main_logger = log_handler.enter_pipeline("convert")

    # customise runtime warning logs
    log_handler.customise_runtime_warnings(
        logger=main_logger
    )

    try:
        # ----------------------------------------
        # 1. PARSE CLI ARGUMENTS
        # ----------------------------------------
        try:
            args = parse_args()

        # parser raises `SystemExit(0)` for `--help`
        except SystemExit as exc:
            if exc.code == 0:
                log_handler.exit_pipeline(
                    start_time=start_time
                )

                return 0

            raise

    except:
        pass

    
    
    
    
  

    convert(j=args.j, mn=args.mn)

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
