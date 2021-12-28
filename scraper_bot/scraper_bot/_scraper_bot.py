from __future__ import annotations

import logging
import os
import time

import jsonschema
import yaml
from ischedule import run_pending

from ..bot import Bot
from ..cache import Cache
from ..exceptions import ConfigError
from ._config_schema import CONFIG_SCHEMA
from ._task import Task

_LOGGER = logging.getLogger(__package__)


class ScraperBot:
    bot: Bot
    tasks: list[Task]
    cache: Cache

    def __init__(self, bot: dict, tasks: list, redis: str = None):
        self.bot = Bot.make(bot)

        self.tasks = [Task.make(c, on_find=self._on_find) for c in tasks]

        self.cache = Cache(
            redis if redis is not None else os.getenv("SB_REDIS")
        )

    def _setup_tasks(self) -> None:
        for t in self.tasks:
            t.schedule()

        _LOGGER.info("Setup schedule")

    def start(self) -> None:
        self._setup_tasks()

        _LOGGER.info("Start schedule")

        while True:
            run_pending()
            time.sleep(1)

    def _on_find(self, *entries: str) -> None:
        new_entries = list(filter(lambda e: not self.cache.exists(e), entries))

        _LOGGER.info(f"Found {len(new_entries)} new entries")

        for n in new_entries:
            self.bot.send_found(n)
            self.cache.add(n)

    @classmethod
    def make(cls, config: dict) -> ScraperBot:
        try:
            jsonschema.validators.validate(config, CONFIG_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            _LOGGER.critical(e)
            raise ConfigError(e) from e

        return cls(**config)

    @classmethod
    def make_from_config(cls, config_file: str) -> ScraperBot:
        with open(config_file) as f:
            return cls.make(yaml.safe_load(f))
