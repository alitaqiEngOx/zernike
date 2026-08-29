""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys
import time
from pathlib import Path

from zernike.operations.pipeline import plot_aberration
from zernike.utils import log_handler


def main() -> int:
    """
    Pipeline entry point.
    """
    # start timer
    start_time = time.time()

    # activate logger
    main_logger = log_handler.enter_pipeline("main")

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

        plot_aberration(Path(args.config))

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

    cmd Arguments
    -------------
    --config (optional): str
        path to your `.yml` configuration file.

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
        "--config",
        type=str,
        default=str(
            Path(__file__).parents[3] /
            "data" / "plot_default.yml"
        ),
        help="path to your `.yml` configuration file"
    )

    #parser.add_argument(
    #    "--basis",
    #    type=str,
    #    default="real",
    #    choices=["complex", "real"],
    #    help="Plot basis: `complex` or `real`"
    #)
    #parser.add_argument(
    #    "--coords_type",
    #    type=str,
    #    default="polar",
    #    choices=["cartesian", "polar"],
    #    help="`cartesian` or `polar`"
    #)
    #parser.add_argument(
    #    "--dim_0",
    #    type=float,
    #    nargs=3,
    #    default=None,
    #    help="minimum, maximum and step in dimension 0"
    #)
    #parser.add_argument(
    #    "--dim_1",
    #    type=float,
    #    nargs=3,
    #    default=None,
    #    help="minimum, maximum and step in dimension 1"
    #)
    #parser.add_argument(
    #    '--j',
    #    type=int,
    #    default=None,
    #    help="Zernike polynomial via `j`"
    #)
    #parser.add_argument(
    #    '--mn',
    #    type=int,
    #    nargs=2,
    #    default=None,
    #    help="Zernike polynomial via `m` and `n`"
    #)

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
