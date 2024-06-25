import logging
import sys
from functools import lru_cache
from logging import Formatter

from termcolor import colored

_package_name = __package__.partition(".")[0]


class CustomFormatter(Formatter):
    _format = "%(asctime)sZ [%(levelname)s] %(name)s: %(message)s"

    @lru_cache
    def get_format(self, level: int) -> str:
        match level:
            case logging.DEBUG:
                return colored(f"{self._format} (%(filename)s:%(lineno)d)", "grey")
            case logging.INFO:
                return colored(self._format, "white")
            case logging.WARNING:
                return colored(self._format, "yellow")
            case logging.ERROR:
                return colored(self._format, "red")
            case logging.CRITICAL:
                return colored(self._format, "red", attrs=["bold"])
            case _:
                return colored(self._format, "white")

    def format(self, record) -> str:
        log_fmt = self.get_format(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_default_logger(level: str | int = logging.INFO) -> None:
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(CustomFormatter())
    handler.setLevel(level)
    logging.root.addHandler(handler)
    logging.root.setLevel(level)

    for logger in [v for k, v in logging.root.manager.loggerDict.items() if k.startswith(f"{_package_name}.")]:
        logger.disabled = False
