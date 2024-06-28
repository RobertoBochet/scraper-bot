from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncIterator

from playwright.async_api import Browser, Error, async_playwright

from scraper_bot.settings.browser import BrowserSettings

_LOGGER = getLogger(__name__)


class BrowserManager:
    def __init__(self, settings: BrowserSettings):
        self._settings = settings

    @asynccontextmanager
    async def launch_browser(self) -> AsyncIterator[Browser]:
        async with async_playwright() as pw:
            browser_types = [
                next((b for b in [pw.firefox, pw.chromium, pw.webkit] if b.name == i)) for i in self._settings.type
            ]

            _LOGGER.info(browser_types)

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
                    _LOGGER.debug("Close browser")

                break

    @property
    def stealth_enabled(self) -> bool:
        return self._settings.stealthEnabled
