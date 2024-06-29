from asyncio import gather, sleep
from logging import getLogger

from scraper_bot.cache import Cache, make_cache
from scraper_bot.cache.exceptions import CacheError
from scraper_bot.notifications import NotificationsManager
from scraper_bot.scraper import Scraper
from scraper_bot.settings import Settings

_LOGGER = getLogger(__package__)


class ScraperBot:
    _settings: Settings
    _notificationsManager: NotificationsManager
    _scraper: Scraper
    _cache: Cache

    def __init__(self, settings: Settings):
        self._settings = settings

        self._notificationsManager = NotificationsManager(self._settings.notifications)

        self._scraper = Scraper(browser_settings=self._settings.browser)
        self._scraper.add_task(*self._settings.tasks)

        self._cache = make_cache(settings.cache)

    async def _run(self) -> int:
        try:
            await self._cache.check()
        except CacheError:
            _LOGGER.critical("Cache unavailable")
            return 1

        tasks_results = await self._scraper.run()

        new_entries = await self._cache.filter_exists(
            *[t for r in tasks_results for t in r], to_fingerprint=lambda x: str(hash(x))
        )

        if len(new_entries):
            _LOGGER.info(f"Found {len(new_entries)} new entries")

            await self._notificationsManager.notify(*new_entries)

            await gather(*(self._cache.add(str(hash(e))) for e in new_entries))
        else:
            _LOGGER.info("No new entry was found, skip notifications")

        return 0

    async def run_once(self) -> int:
        try:
            return await self._run()
        finally:
            await self.close()

    async def run(self) -> int:
        _LOGGER.info(f"Start schedule with interval of {self._settings.interval}")

        while True:
            _LOGGER.info("Starting new iteration")
            r = await self._run()
            if r != 0:
                return r
            await self.close()

            _LOGGER.info(f"Waiting {self._settings.interval} for the next iteration")
            await sleep(self._settings.interval.total_seconds())

    async def close(self) -> None:
        await self._cache.close()
