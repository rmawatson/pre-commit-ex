from __future__ import annotations

import argparse
import contextlib
import logging
from collections.abc import Generator

from pre_commit import color
from pre_commit import output

logger = logging.getLogger('pre_commit')

LOG_LEVEL_COLORS = {
    'DEBUG': '',
    'INFO': '',
    'WARNING': color.YELLOW,
    'ERROR': color.RED,
}


class LoggingHandler(logging.Handler):
    def __init__(self, use_color: bool) -> None:
        super().__init__()
        self.use_color = use_color

    def emit(self, record: logging.LogRecord) -> None:
        level_msg = color.format_color(
            f'[{record.levelname}]',
            LOG_LEVEL_COLORS[record.levelname],
            self.use_color,
        )
        output.write_line(f'{level_msg} {record.getMessage()}')


def add_log_level_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR'),
        help='Set the log level (default: %(default)s).',
    )


@contextlib.contextmanager
def logging_handler(use_color: bool, level: int = logging.INFO) -> Generator[None]:
    handler = LoggingHandler(use_color)
    logger.addHandler(handler)
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.removeHandler(handler)
