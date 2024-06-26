from contextlib import asynccontextmanager
from logging import getLogger

from playwright.async_api import Browser, Error, async_playwright

from scraper_bot.settings.browser import BrowserSettings

_LOGGER = getLogger(__name__)


class BrowserManager:
    def __init__(self, settings: BrowserSettings):
        self._settings = settings

    @asynccontextmanager
    async def launch_browser(self) -> Browser:
        async with async_playwright() as pw:
            browser_types = [
                next((b for b in [pw.firefox, pw.chromium, pw.webkit] if b.name == i)) for i in self._settings.type
            ]

            for browser_type in browser_types:
                try:
                    browser = await browser_type.launch(headless=self._settings.headless)
                except Error as e:
                    _LOGGER.debug(e)
                    _LOGGER.warning(f"{browser_type.name} not available")
                    continue

                _LOGGER.info(f"Use {browser.browser_type.name}")

                try:
                    yield browser
                finally:
                    await browser.close()

                break

    @property
    def stealth_enabled(self) -> bool:
        return self._settings.stealthEnabled
