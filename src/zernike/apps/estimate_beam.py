""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys
import time
from pathlib import Path

from zernike.operations.pipeline import estimate_beam
from zernike.utils import log_handler


def main() -> int:
    """
    Pipeline entry point.
    """
    # start timer
    start_time = time.time()

    # activate logger
    main_logger = log_handler.enter_pipeline("estimate")

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

        # ----------------------------------------
        # 2. PIPELINE
        # ----------------------------------------
        main_logger.info("Entering pipeline\n")

        estimate_beam(
            Path(args.sampled_data_path),
            j_list=args.j, n_list=args.n
        )

        # ----------------------------------------
        # 3. SUCCESSFUL EXIT
        # ----------------------------------------
        log_handler.exit_pipeline(
            start_time=start_time, logger=main_logger,
            success=True
        )

        return 0

    except (Exception, SystemExit) as exc:
        # ----------------------------------------
        # 4. ERROR HANDLING
        # ----------------------------------------
        log_handler.exit_pipeline(
            start_time=start_time, logger=main_logger,
            error=exc
        )


def parse_args() -> argparse.Namespace:
    """
    Parses command line arguments.

    --j (optional): int
        orders of Zernike polynomials via `j` (as many as desired).

    --n (optional): int
        order of Zernike polynomials via `n` 
        (as many as desired - will include all `m`).

    --sampled_data_path (optional): str
        `.txt` file or `.npy` binary bearing the sampled data.

    cmd Arguments
    -------------
    """
    parser = argparse.ArgumentParser(
        description="Estimates beam data with Zernike polynomials",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--j",
        type=int,
        default=None,
        nargs='*',
        help="Zernike polynomials via `j` (as many as desired)"
    )
    parser.add_argument(
        "--n",
        type=int,
        default=None,
        nargs='*',
        help=(
            "Zernike polynomials via `n` (as many as desired "
            "- will include all `m`)"
        )
    )
    parser.add_argument(
        "--sampled_data_path",
        type=str,
        default=(
            f"{Path(__file__).parents[3].joinpath('data', 'sampled_beam.txt')}"
        ),
        help=(
            "`.txt` file or `.npy` binary bearing the sampled data."
        )
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
