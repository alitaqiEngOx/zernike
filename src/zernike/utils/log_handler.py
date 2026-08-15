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


_warning_logger: contextvars.ContextVar[
    logging.Logger | None
] = contextvars.ContextVar(
    "warning_logger",
    default=None,
)

_default_warning_logger: logging.Logger | None=None