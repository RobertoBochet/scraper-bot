#!/usr/bin/env python3
import asyncio
import json
from argparse import ArgumentParser
from asyncio import AbstractEventLoop, new_event_loop
from logging import DEBUG, INFO, getLogger
from signal import SIGINT

import black
from pydantic import ValidationError

from . import ScraperBot, __version__
from .logging import setup_default_logger
from .settings import Settings


def main() -> int:
    # gets inline arguments
    parser = ArgumentParser(prog="bot_scraper")

    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Increase logging verbosity")

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
        version=f"scraper-bot {__version__}",
    )

    # parses args
    args = vars(parser.parse_args())

    # loads logger config
    setup_default_logger(DEBUG if args.get("verbose", None) else INFO)

    logger = getLogger(__package__)

    cli_override_settings = {}

    if args.get("show_config_schema"):
        print(json.dumps(Settings.model_json_schema(), indent=2))
        return 0

    if config_path := args.get("config_path"):
        Settings.set_settings_path(config_path)
        logger.info(f"Using config file '{config_path}'")

    try:
        settings = Settings(**cli_override_settings)
    except ValidationError as e:
        logger.critical(f"Configuration issue: {e}")
        return 1

    logger.debug(black.format_str(repr(settings), mode=black.FileMode(line_length=60)))

    # creates an instance of ScraperBot
    bot = ScraperBot(settings)

    logger.info("Scraper bot is ready to start")

    async def clean_loop(loop: AbstractEventLoop):
        await asyncio.gather(
            *(t.cancel() for t in asyncio.all_tasks() if t is not asyncio.current_task()), return_exceptions=True
        )
        loop.stop()

    loop = new_event_loop()
    loop.add_signal_handler(SIGINT, lambda: asyncio.create_task(clean_loop(loop)))

    if not settings.interval:
        task = loop.create_task(bot.run_once())
    else:
        task = loop.create_task(bot.run())

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        logger.info("Scraper bot has been stopped")
        if not settings.daemonize:
            return 1
    finally:
        loop.close()

    return 0


if __name__ == "__main__":
    exit(main())
