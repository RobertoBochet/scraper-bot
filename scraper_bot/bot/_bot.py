from __future__ import annotations

import telegram


class Bot(telegram.Bot):
    chats: list[str | int]

    def __init__(self, token: str, chats: list[str | int], **kwargs):
        super(Bot, self).__init__(token, **kwargs)
        self.chats = chats

    def send_found(self, element: str):
        for c in self.chats:
            self.send_message(c, element)

    @classmethod
    def make(cls, config: dict) -> Bot:
        return cls(**config)
