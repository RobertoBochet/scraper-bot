import logging
from typing import Callable

from ischedule import schedule

from ..scraper import Scraper

_LOGGER = logging.getLogger(__package__)


class Task(Scraper):
    name: str
    interval: int

    def __init__(
        self,
        url: str,
        target: str,
        on_find: Callable[[...], None],
        interval: int = 60 * 60,
        name: str = "generic-task",
    ):
        super().__init__(url, target, on_find)
        self.name = name
        self.interval = interval

        _LOGGER.info(f"Created task {self.name}")

    def schedule(self):
        schedule(self.run, interval=self.interval)

        _LOGGER.info(f"Scheduled task {self.name}")

    @classmethod
    def make(cls, config: dict):
        return cls(**config)
