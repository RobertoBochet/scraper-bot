from logging import Logger, getLogger

from playwright_stealth import stealth_async

from scraper_bot.settings.task import TaskSettings

from .browser_manager import BrowserManager
from .scraper_task_result import ScraperTaskResult


class ScraperTask:
    def __init__(self, settings: TaskSettings, browser_manager: BrowserManager):
        self._settings = settings
        self._browser_manager = browser_manager

    @property
    def settings(self) -> TaskSettings:
        return self._settings

    @property
    def name(self) -> str:
        return self._settings.name

    @property
    def _logger(self) -> Logger:
        return getLogger(f"{__name__}.{self.name}")

    async def run(self) -> ScraperTaskResult:
        self._logger.info("Starting scraper task")

        async with self._browser_manager.launch_browser() as browser:
            page = await browser.new_page()

            if self._browser_manager.stealth_enabled:
                await stealth_async(page)

            await page.goto(str(self.settings.url))

            # TODO add support for waitingForTarget

            data: str | list[str] | dict | list[dict] = await page.evaluate(self.settings.target)

            # TODO add support for nextPageTarget

        if not isinstance(data, list):
            data = list(data)

        data = [{"value": d} if isinstance(d, str) else d for d in data]

        self._logger.info(f"Scraper task retrieves {len(data)} entities")

        if not len(data):
            self._logger.warning("Scraper task retrieve zero elements, maybe some error?")

        self._logger.info("End scraper task")

        return ScraperTaskResult(data=data, task=self)
