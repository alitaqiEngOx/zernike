""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import contextlib
import contextvars
import logging
import sys
import time
import traceback
import warnings


@contextlib.contextmanager
def warning_scope(*, logger: logging.Logger):
    """
    """
    token = _warning_logger.set(logger)
    yield
    _warning_logger.reset(token)


def create(
        name: str, *, header_footer: bool=False
    ) -> logging.Logger:
    """
    Generates a new `logging.Logger` class instance.

    Arguments
    ---------
    name: `str`
        name given to the new class instance.

    header_footer: `bool=False`
        if `True`, treats the logger as a 
        header/footer.

    Returns
    -------
    New `logging.logger` class instance.
    """
    while len(name) < 10:
        name += ' '

    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    if header_footer:
        formatter = logging.Formatter('')

    else:
        formatter = logging.Formatter(
            " +| %(name)s [%(asctime)s -"
            " %(levelname)s]: %(message)s"
        )

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def customise_runtime_warnings(
        *, logger: logging.Logger
) -> None:
    """
    """
    global _default_warning_logger
    _default_warning_logger = logger

    def show_warning(
            message, category, filename, lineno, file=None,
            line=None
    ) -> None:
        """
        """
        logger.warning("▼▼▼ Runtime warning ▼▼▼\n")

        warning_logger = create(
            "warning", header_footer=True
        )

        warning_logger.warning(
            f"{category.__name__}: {message}\n"
        )

        warning_logger.warning("────── WARNING LOC ──────\n")
        warning_logger.warning(
            f'File "{filename}", line {lineno}\n'
        )

        if line is not None:
            logger.warning(f"    {line.strip()}\n")

        warning_logger.warning("────── END WARNING ──────\n")

    warnings.showwarning = show_warning

    # Show RuntimeWarnings whenever they occur
    warnings.simplefilter("always", RuntimeWarning)


def enter_pipeline(name: str) -> logging.Logger:
    """
    """
    header_logger = create("header", header_footer=True)

    header_logger.info(
        "\n========= ZERNIKE =========\n"
    )

    header_logger.info(
        " * Author: A. Taqi;"
        " alitaqi94.developer@gmail.com\n"
    )

    header_logger.info(" * All Rights Reserved\n")

    logger = create(name)

    return logger


def exit_pipeline(
        *, start_time: float,
        logger: logging.Logger | None=None,
        success: bool | None=None,
        error: BaseException | None=None
) -> None:
    """
    Exits the pipeline gracefully.

    Arguments
    ---------
    logger: `logging.Logger` (optional)
        logger object to exit the pipeline with.

    success: `bool` (optional)
        if `True`, the pipeline declares a successful 
        run as it ends the job, but declares a failed 
        run if `False` and neutral (e.g., --help) exit 
        if `None`.

    error: `BaseException` (optional)
        if provided, the pipeline logs the exception and
        declares a failed run.
    """
    footer_logger = create(
        "footer", header_footer=True
    )

    # neutral exit (e.g., parser called with `--help` tag)
    if success is None and error is None:
        footer_logger.info(
            "\n========= ZERNIKE =========\n"
        )

        return

    logger = (
        footer_logger if logger is None
        else logger
    )

    # error repoted -> pipeline MUST fail
    if error is not None:
        logger.error("▼▼▼ Exception occurred ▼▼▼\n")

        exception_logger = create(
            "exception", header_footer=True
        )

        exception_logger.error(
            f"{type(error).__name__}: {error}\n"
        )

        exception_logger.error("─────── TRACEBACK ───────\n")

        exception_logger.error(
            "".join(
                traceback.format_exception(
                    type(error),
                    error,
                    error.__traceback__,
                )
            )
        )

        exception_logger.error("───── END TRACEBACK ─────\n")

        logger.info("Pipeline run - ❌ FAILURE")
        logger.info("Exiting pipeline")
        logger.info(
            f"Full time = "
            f"{round(time.time() - start_time, 3)} s"
        )

        footer_logger.info(
            "\n========= ZERNIKE =========\n"
        )

        if isinstance(error, SystemExit):
            exit_code = (
                error.code
                if isinstance(error.code, int)
                else 1
            )

            if exit_code == 0:
                exit_code = 1

            sys.exit(exit_code)

        sys.exit(1)

    # success/failure reported and no error given
    if success:
        logger.info(f"Pipeline run - ✅ SUCCESS")

    else:
        logger.info("Pipeline run - ❌ FAILURE")

    logger.info(f"Exiting pipeline")
    logger.info(
        f"Full time ="
        f" {round(time.time() - start_time, 3)} s"
    )

    footer_logger.info(
        "\n========= ZERNIKE =========\n"
    )

    if not success:
        sys.exit(1)


_warning_logger: contextvars.ContextVar[
    logging.Logger | None
] = contextvars.ContextVar(
    "warning_logger",
    default=None,
)

_default_warning_logger: logging.Logger | None=None