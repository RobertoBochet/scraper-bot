from asyncio import gather
from logging import getLogger

from scraper_bot.settings.browser import BrowserSettings
from scraper_bot.settings.task import TaskSettings

from .browser_manager import BrowserManager
from .scraper_task import ScraperTask
from .scraper_task_result import ScraperTaskResult

_LOGGER = getLogger(__package__)


class Scraper:
    _tasks: list[ScraperTask] = []

    def __init__(self, browser_settings: BrowserSettings):
        self._browser_manager = BrowserManager(browser_settings)

    def add_task(self, *tasks: TaskSettings) -> list[ScraperTask]:
        for t in tasks:
            self._tasks.append(ScraperTask(t, browser_manager=self._browser_manager))
            _LOGGER.info(f"Created task {t.name}")
        return self._tasks

    @property
    def tasks(self) -> list[ScraperTask]:
        return self._tasks

    async def run(self) -> tuple[ScraperTaskResult, ...]:
        return await gather(*(t.run() for t in self._tasks))
