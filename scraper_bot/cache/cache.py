from asyncio import gather
from typing import Callable, TypeVar

from redis.asyncio import StrictRedis

T = TypeVar("T")


class Cache:
    redis: StrictRedis

    def __init__(self, redis: str = "redis://127.0.0.1/0"):
        self.redis = StrictRedis.from_url(redis)

    async def exists(self, entry: str) -> bool:
        return await self.redis.exists(entry) != 0

    async def add(self, entry: str) -> None:
        await self.redis.set(entry, "@")

    async def _none_if_exists(self, entry: str, value: T) -> T | None:
        if not await self.exists(entry):
            return value
        return None

    async def filter_exists(self, *entries: T, to_id: Callable[[T], str]) -> list[T]:
        return [v for v in await gather(*(self._none_if_exists(to_id(e), e) for e in entries)) if v is not None]
