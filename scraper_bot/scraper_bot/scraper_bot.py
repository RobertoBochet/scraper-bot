import logging
from asyncio import gather, sleep

from scraper_bot.cache import Cache
from scraper_bot.notifications import NotificationsManager
from scraper_bot.scraper import Scraper
from scraper_bot.settings import Settings

_LOGGER = logging.getLogger(__package__)


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

        self._cache = Cache(str(settings.redis))

    async def _run(self) -> None:
        tasks_results = await self._scraper.run()

        new_entries = await self._cache.filter_exists(
            *[t for r in tasks_results for t in r], to_id=lambda x: str(hash(x))
        )

        if len(new_entries):
            _LOGGER.info(f"Found {len(new_entries)} new entries")

            await self._notificationsManager.notify(*new_entries)

            await gather(*(self._cache.add(str(hash(e))) for e in new_entries))
        else:
            _LOGGER.info("No new entry was found, skip notifications")

    async def run_once(self) -> None:
        await self._run()

    async def run(self) -> None:
        _LOGGER.info(f"Start schedule with interval of {self._settings.interval}")

        while True:
            _LOGGER.info("Starting new iteration")
            await self._run()
            _LOGGER.info(f"Waiting {self._settings.interval} for the next iteration")
            await sleep(self._settings.interval.total_seconds())
