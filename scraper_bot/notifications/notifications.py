from logging import getLogger
from typing import Any

from apprise import Apprise

from scraper_bot.settings.settings import NotificationChannel, NotificationsSettings

_LOGGER = getLogger(__name__)


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

    def notify(self, entity: dict[str, Any]) -> None:
        for c in self.channels:
            if not self._apprise.notify(
                body=c.message_template.render(**entity), title=c.title, body_format=c.format, tag=c.tag
            ):
                _LOGGER.error(f"Failed to notify {c.uri}")
