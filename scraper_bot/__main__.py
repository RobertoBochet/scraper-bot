#!/usr/bin/env python3
import json
import logging.config
import signal
import sys
from argparse import ArgumentParser

from pydantic import ValidationError

from . import ScraperBot, __version__
from .logging import setup_default_logger
from .settings import Settings


def main() -> int:
    signal.signal(signal.SIGINT, lambda: sys.exit(0))

    # loads logger config
    setup_default_logger()

    LOGGER = logging.getLogger(__package__)

    # gets inline arguments
    parser = ArgumentParser(prog="bot_scraper")

    parser.add_argument(
        "-c",
        "--config",
        dest="config_path",
        help="configuration file path",
    )

    parser.add_argument(
        "--config-schema",
        action="store_true",
        dest="show_config_schema",
        help="show config json schema and exit",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"bot_scraper {__version__}",
    )

    # parses args
    args = vars(parser.parse_args())

    if args.get("show_config_schema"):
        print(json.dumps(Settings.model_json_schema(), indent=2))
        return 0

    if config_path := args.get("config_path"):
        Settings.set_settings_path(config_path)
        LOGGER.info(f"Using config file '{config_path}'")

    try:
        settings = Settings()
    except ValidationError as e:
        LOGGER.critical(f"Configuration issue: {e}")
        return 1

    # creates an instance of ScraperBot
    bot = ScraperBot(settings)

    LOGGER.info("bot_scraper is ready to start")

    # starts bot
    bot.start()

    return 0


if __name__ == "__main__":
    sys.exit(main())
