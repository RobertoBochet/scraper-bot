#!/usr/bin/env python3
import argparse
import logging
import logging.config
import signal
import sys
from pathlib import Path

import yaml

from . import ScraperBot, __version__
from .exceptions import ConfigError

_LOGGER_CONFIG_PATH = (Path(__file__).parent / "logger.yaml").resolve()
_LOGGER = logging.getLogger(__package__)


def main() -> int:
    signal.signal(signal.SIGINT, lambda: sys.exit(3))

    # loads logger config
    try:
        with open(_LOGGER_CONFIG_PATH) as f:
            logging.config.dictConfig(yaml.safe_load(f))
    except FileNotFoundError:
        _LOGGER.critical("Logger configuration not found")
        return 2

    # gets inline arguments
    parser = argparse.ArgumentParser(prog="bot_scraper")

    parser.add_argument(
        "-c",
        "--config",
        dest="config_path",
        default="/etc/scraperbot/config.yaml",
        help="configuration file path",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="bot_scraper {}".format(__version__),
    )

    # parses args
    args = vars(parser.parse_args())

    # creates an instance of ScraperBot
    try:
        bot = ScraperBot.make_from_config(args["config_path"])
    except ConfigError:
        _LOGGER.critical("Configuration issue: I give up")
        return 1

    _LOGGER.info("bot_scraper is ready to start")

    # starts bot
    bot.start()

    return 0


if __name__ == "__main__":
    sys.exit(main())
