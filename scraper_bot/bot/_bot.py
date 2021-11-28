from __future__ import annotations

import logging

import telegram

_LOGGER = logging.getLogger(__package__)


class Bot(telegram.Bot):
    chats: list[str | int]

    def __init__(self, token: str, chats: list[str | int], **kwargs):
        super(Bot, self).__init__(token, **kwargs)
        self.chats = chats

    def send_found(self, entry: str) -> None:
        _LOGGER.info(f"Sent entry {entry}")
        for c in self.chats:
            self.send_message(c, entry)

    @classmethod
    def make(cls, config: dict) -> Bot:
        return cls(**config)
