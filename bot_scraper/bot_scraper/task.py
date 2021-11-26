import logging

from ischedule import schedule

from ..scraper import Scraper

_LOGGER = logging.getLogger(__package__)


class Task:
    name: str
    interval: int
    scraper: Scraper

    def __init__(
        self, interval: int = 60 * 60, name: str = "generic-task", **kwargs
    ):
        self.name = name
        self.interval = interval
        self.scraper = Scraper(**kwargs, on_find=self._on_find)

        _LOGGER.info(f"Created task {self.name}")

    def schedule(self):
        schedule(self._work, interval=self.interval)

        _LOGGER.info(f"Scheduled task {self.name}")

    def _work(self):
        self.scraper.run()

    def _on_find(self, *args: list[str]):
        print(args)

    @classmethod
    def make(cls, config: dict):
        return cls(**config)
