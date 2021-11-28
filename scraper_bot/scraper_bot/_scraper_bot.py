from __future__ import annotations

import yaml
from ischedule import run_loop

from ..bot import Bot
from ..cache import Cache
from ._task import Task


class ScraperBot:
    bot: Bot
    tasks: list[Task]
    cache: Cache

    def __init__(self, bot: dict, tasks: list):
        self.bot = Bot.make(bot)

        self.tasks = [Task.make(c, on_find=self._on_find) for c in tasks]

        self.cache = Cache()

    def _setup_tasks(self) -> None:
        for t in self.tasks:
            t.schedule()

    def start(self) -> None:
        self._setup_tasks()

        run_loop()

    def _on_find(self, *entries: str) -> None:
        new_entries = filter(lambda e: not self.cache.exists(e), entries)

        for n in new_entries:
            self.bot.send_found(n)
            self.cache.add(n)

    @classmethod
    def make(cls, config: dict) -> ScraperBot:
        return cls(**config)

    @classmethod
    def make_from_config(cls, config_file: str) -> ScraperBot:
        with open(config_file) as f:
            return cls.make(yaml.safe_load(f))
