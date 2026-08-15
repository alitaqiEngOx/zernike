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
        "\n===== BioWave-Extract =====\n"
    )

    header_logger.info(
        " * Author: A. Taqi;"
        " alitaqi94.developer@gmail.com\n"
    )

    header_logger.info(" * All Rights Reserved\n")

    logger = create(name)

    return logger


_warning_logger: contextvars.ContextVar[
    logging.Logger | None
] = contextvars.ContextVar(
    "warning_logger",
    default=None,
)

_default_warning_logger: logging.Logger | None=None