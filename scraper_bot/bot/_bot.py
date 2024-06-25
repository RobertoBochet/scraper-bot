import logging
from typing import Self

from telegram import Bot as _Bot
from telegram.error import BadRequest, Forbidden

_LOGGER = logging.getLogger(__package__)


class Bot(_Bot):
    _chats: list[str | int]

    def __init__(self, token: str, chats: list[str | int], **kwargs):
        super(Bot, self).__init__(token, **kwargs)
        self._chats = chats

    def send_found(self, entry: str) -> None:
        _LOGGER.info(f"Sent entry {entry}")
        for c in self._chats:
            try:
                self.send_message(c, entry)
            except Forbidden:
                _LOGGER.warning(f"Bot is not longer enabled for chat {c}")
            except BadRequest:
                _LOGGER.warning(f"Chat {c} not found")

    @classmethod
    def make(cls, config: dict) -> Self:
        return cls(**config)
