#!/usr/bin/env python3
import argparse
import logging
import logging.config
import sys
from pathlib import Path

import yaml

from . import __version__
from .bot_scraper import BotScraper
from .exceptions import ConfigError

_LOGGER_CONFIG_PATH = (Path(__file__).parent / ".." / "logger.yaml").resolve()
_LOGGER = logging.getLogger(__package__)


def main() -> int:
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
        default="/etc/bot-scraper/config.yaml",
        help="configuration file path",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="bot_scraper {}".format(__version__),
    )

    # parses args
    args = vars(parser.parse_args())

    # creates an instance of BotScraper
    try:
        bot = BotScraper.make_from_config(args["config_path"])
    except ConfigError:
        _LOGGER.critical("Configuration issue: I give up")
        return 1

    _LOGGER.info("bot_scraper is ready to start")

    # starts bot
    bot.start()

    return 0


if __name__ == "__main__":
    sys.exit(main())
