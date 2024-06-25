from __future__ import annotations

import logging
import time

from ischedule import run_pending

from ..cache import Cache
from ..notifications.notifications import NotificationsManager
from ..settings import Settings
from ._task import Task

_LOGGER = logging.getLogger(__package__)


class ScraperBot:
    notificationsManager: NotificationsManager
    tasks: list[Task]
    cache: Cache

    def __init__(self, settings: Settings):
        self.notificationsManager = NotificationsManager(settings.notifications)

        self.tasks = [Task(**c.model_dump(), on_find=self._on_find) for c in settings.tasks]

        self.cache = Cache(str(settings.redis))

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
            self.notificationsManager.notify({"url": n})
            self.cache.add(n)
