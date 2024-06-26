#!/usr/bin/env python3
import asyncio
import json
import logging.config
from argparse import ArgumentParser
from asyncio import CancelledError, create_task
from signal import SIGINT

from pydantic import ValidationError

from . import ScraperBot, __version__
from .logging import setup_default_logger
from .settings import Settings


def main() -> int:
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
        "-d",
        "--daemonize",
        action="store_true",
        dest="daemonize",
        help="run the scraper as a daemon instead run only once",
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

    cli_override_settings = {}

    if args.get("show_config_schema"):
        print(json.dumps(Settings.model_json_schema(), indent=2))
        return 0

    if config_path := args.get("config_path"):
        Settings.set_settings_path(config_path)
        LOGGER.info(f"Using config file '{config_path}'")

    if args.get("daemonize"):
        cli_override_settings["daemonize"] = True

    try:
        settings = Settings(**cli_override_settings)
    except ValidationError as e:
        LOGGER.critical(f"Configuration issue: {e}")
        return 1

    # creates an instance of ScraperBot
    bot = ScraperBot(settings)

    LOGGER.info("bot_scraper is ready to start")

    if not settings.daemonize:
        asyncio.run(bot.run_once())
        return 0

    async def daemonize():
        LOGGER.info("Starting daemon")
        task = create_task(bot.run())

        task.get_loop().add_signal_handler(SIGINT, task.cancel)

        try:
            await task
        except CancelledError:
            LOGGER.info("Daemon has been stopped")

    # starts bot as daemon
    asyncio.run(daemonize())
    return 0


if __name__ == "__main__":
    exit(main())
