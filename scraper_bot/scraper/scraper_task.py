from logging import Logger, getLogger

from playwright.async_api import Error, Page
from playwright_stealth import stealth_async

from scraper_bot.settings.task import TaskSettings

from .browser_manager import BrowserManager
from .exceptions import InvalidJSONError, TargetScriptError
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
            page: Page = await browser.new_page()

            if self._browser_manager.stealth_enabled:
                await stealth_async(page)

            response = await page.goto(str(self.settings.url))

            match await response.header_value("Content-Type"):
                case "application/json":
                    self._logger.info("Got JSON response")
                    try:
                        content = await response.json()
                    except Error as e:
                        self._logger.error("Invalid JSON error")
                        self._logger.debug(e)
                        raise InvalidJSONError()
                case _:
                    content = await response.text()

            # TODO add support for waitingForTarget

            self._logger.info("Starting target script evaluated")
            try:
                data: str | list[str] | dict | list[dict] = await page.evaluate(self.settings.script, content)
            except Error as e:
                self._logger.error("Target script error")
                self._logger.debug(e)
                raise TargetScriptError()

            self._logger.info("Target script evaluated")

            self._logger.debug(data)

            # TODO add support for nextPageTarget

        self._logger.info("Completed scraping")

        if not isinstance(data, list):
            data = list(data)

        data = [{"value": d} if isinstance(d, str) else d for d in data]

        self._logger.info(f"Scraper task retrieves {len(data)} entities")

        if not len(data):
            self._logger.warning("Scraper task retrieve zero elements, maybe some error?")

        self._logger.info("End scraper task")

        return ScraperTaskResult(data=data, task=self)
