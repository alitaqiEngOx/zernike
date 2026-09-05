""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys
import time
from pathlib import Path

from zernike.operations.pipeline import kernel_from_npz
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

        #kernel_from_npz(
        #    Path(args.path), show_info=args.show_info,
        #    key=args.key, index=args.index,
        #    save_as=Path(args.save_as)
        #)

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
        description="Extracts kernel from `.npz`",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--config",
        type=str,
        default=str(
            Path(__file__).parents[3] /
            "data" / "extract_default.yml"
        ),
        help="path to your `.yml` configuration file"
    )

    #parser.add_argument(
    #    "path",
    #    type=str,
    #    help="`.npz` path"
    #)
    #parser.add_argument(
    #    "--key",
    #    type=str,
    #    default=None,
    #    help="`.npz` array key to extract from"
    #)
    #parser.add_argument(
    #    "--index",
    #    nargs='+',
    #    default=None,
    #    help="position indices for the kernel to be extracted"
    #)
    #parser.add_argument(
    #    "--save_as",
    #    type=str,
    #    default=None,
    #    help="output filename & path"
    #)
    #parser.add_argument(
    #    "--show_info",
    #    action="store_true",
    #    help="display keys & shapes of your `.npz`"
    #)

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
