#!/usr/bin/env python3
import argparse
import logging.config
import signal
import sys

from pydantic import ValidationError

from . import ScraperBot, __version__
from .logging import setup_default_logger
from .settings import Settings


def main() -> int:
    signal.signal(signal.SIGINT, lambda: sys.exit(3))

    # loads logger config
    setup_default_logger()

    LOGGER = logging.getLogger(__package__)

    # gets inline arguments
    parser = argparse.ArgumentParser(prog="bot_scraper")

    parser.add_argument(
        "-c",
        "--config",
        dest="config_path",
        help="configuration file path",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"bot_scraper {__version__}",
    )

    # parses args
    args = vars(parser.parse_args())

    if config_path := args.get("config_path"):
        Settings.set_settings_path(config_path)
        LOGGER.info(f"Using config file '{config_path}'")

    try:
        settings = Settings()
    except ValidationError as e:
        LOGGER.critical(f"Configuration issue: {e}")
        return 1

    # creates an instance of ScraperBot
    bot = ScraperBot(**settings.model_dump())

    LOGGER.info("bot_scraper is ready to start")

    # starts bot
    bot.start()

    return 0


if __name__ == "__main__":
    sys.exit(main())
