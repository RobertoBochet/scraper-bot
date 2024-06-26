from asyncio import gather
from logging import getLogger
from typing import Any

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

    async def _notify(self, channel: NotificationChannel, entity: dict[str, Any]) -> None:
        result = await self._apprise.async_notify(
            body=channel.message_template.render(**entity),
            title=channel.title,
            body_format=channel.format,
            tag=channel.tag,
        )
        if not result:
            _LOGGER.error(f"Failed to notify {channel.uri}")

    async def notify(self, *entity: dict[str, Any]) -> None:
        _LOGGER.info(f"Notifying {len(entity)} entities to {len(self._channels)} channels")
        await gather(*(self._notify(c, e) for c in self.channels for e in entity))
        _LOGGER.info("Notifying completed")
