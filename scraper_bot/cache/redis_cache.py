from asyncio import gather
from logging import getLogger
from typing import Callable, TypeVar

from pydantic_core import Url
from redis.asyncio import ConnectionError, StrictRedis

from .cache import Cache
from .exceptions import CacheConnectionError

T = TypeVar("T")

_LOGGER = getLogger(__package__)


class RedisCache(Cache):
    def __init__(self, redis: str | Url):
        self.redis = StrictRedis.from_url(str(redis))

    async def exists(self, entry: str) -> bool:
        return await self.redis.exists(entry) != 0

    async def add(self, entry: str) -> None:
        await self.redis.set(entry, "@")

    async def _none_if_exists(self, entry: str, value: T) -> T | None:
        if not await self.exists(entry):
            return value
        return None

    async def filter_exists(self, *entries: T, to_fingerprint: Callable[[T], str]) -> list[T]:
        return [
            v for v in await gather(*(self._none_if_exists(to_fingerprint(e), e) for e in entries)) if v is not None
        ]

    async def close(self):
        try:
            await self.redis.close()
        except (OSError, ConnectionError):
            pass

    async def check(self) -> None:
        try:
            await self.redis.ping()
        except (OSError, ConnectionError):
            _LOGGER.error("Connection error while checking redis database")
            raise CacheConnectionError
