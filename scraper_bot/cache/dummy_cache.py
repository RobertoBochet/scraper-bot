from logging import getLogger
from typing import Callable, TypeVar

from .cache import Cache as CacheInterface

T = TypeVar("T")


_LOGGER = getLogger(__package__)


class DummyCache(CacheInterface):
    def __init__(self):
        _LOGGER.warning("DummyCache initialized, cache will not be persistent")

    async def exists(self, entry: str) -> False:
        return False

    async def add(self, entry: str) -> None:
        return None

    async def filter_exists(self, *entries: T, to_fingerprint: Callable[[T], str]) -> list[T]:
        return [*entries]

    async def close(self) -> None:
        return None

    async def check(self) -> None:
        return None
