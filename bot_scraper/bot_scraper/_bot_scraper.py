from __future__ import annotations

import yaml
from ischedule import run_loop

from ..cache import Cache
from ._task import Task


class BotScraper:
    tasks: list[Task]
    cache: Cache

    def __init__(self, bot: dict, tasks: list):
        self.tasks = [Task.make(c) for c in tasks]

        self.cache = Cache()

    def _setup_tasks(self) -> None:
        for t in self.tasks:
            t.schedule()

    def start(self) -> None:
        self._setup_tasks()

        run_loop()

    def _on_find(self) -> None:
        pass

    @classmethod
    def make(cls, config: dict) -> BotScraper:
        return cls(**config)

    @classmethod
    def make_from_config(cls, config_file: str) -> BotScraper:
        with open(config_file) as f:
            return cls.make(yaml.safe_load(f))
