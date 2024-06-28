from asyncio import Semaphore, gather
from logging import getLogger
from typing import Any

from aiolimiter import AsyncLimiter
from apprise import Apprise

from scraper_bot.settings.notifications import (
    NotificationChannel,
    NotificationsSettings,
)

_LOGGER = getLogger(__package__)


class NotificationsManager:
    _apprise: Apprise
    _channels: list[NotificationChannel]

    def __init__(self, settings: NotificationsSettings):
        self._apprise = Apprise()

        self._channels = settings.channels

        for c in self.channels:
            self._apprise.add(c.uri, tag=c.tag)
            _LOGGER.info(f"Added notification channel {c.uri}")

    @property
    def channels(self) -> list[NotificationChannel]:
        return self._channels

    async def _notify(
        self, channel: NotificationChannel, entity: dict[str, Any], limiter: AsyncLimiter | Semaphore
    ) -> bool:
        async with limiter:
            result = await self._apprise.async_notify(
                body=channel.message_template.render(**entity),
                title=channel.title,
                body_format=channel.format,
                tag=channel.tag,
            )
            if result is False:
                _LOGGER.error(f"Failed to notify {channel.uri}")

        return result is not False

    async def notify(self, *entity: dict[str, Any]) -> None:
        _LOGGER.info(f"Notifying {len(entity)} entities to {len(self._channels)} channels")
        results = await gather(*(self._notify(c, e, limiter=c.rate_limiter) for c in self.channels for e in entity))
        success_notifications_count = len(list((True for r in results if r)))
        if success_notifications_count > len(results):
            _LOGGER.warning(
                f"Only {success_notifications_count} notifications of {len(results)} are completed successfully"
            )
        _LOGGER.info("Notifying completed")
