from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncIterator

from playwright.async_api import Browser, Error, async_playwright

from scraper_bot.settings.browser import BrowserSettings

from .exceptions import NoBrowserAvailable

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

            _LOGGER.debug(browser_types)

            browser: Browser | None = None

            for browser_type in browser_types:
                try:
                    browser = await browser_type.launch(headless=self._settings.headless)
                except Error as e:
                    _LOGGER.debug(e)
                    _LOGGER.warning(f"Impossible to run {browser_type.name}")
                    continue

            if browser is None:
                _LOGGER.error(
                    "No browser available. "
                    "Did you remember to install one with `playwright install --with-deps firefox`?"
                )
                raise NoBrowserAvailable()

            _LOGGER.info(f"Use {browser.browser_type.name}")

            try:
                yield browser
                return
            finally:
                await browser.close()
                _LOGGER.debug("Close browser")

    @property
    def stealth_enabled(self) -> bool:
        return self._settings.stealthEnabled
