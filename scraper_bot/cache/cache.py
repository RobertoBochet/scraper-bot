from abc import ABC
from typing import Callable, TypeVar

T = TypeVar("T")


class Cache(ABC):
    async def exists(self, entry: str) -> bool:
        pass

    async def add(self, entry: str) -> None:
        pass

    async def filter_exists(self, *entries: T, to_fingerprint: Callable[[T], str]) -> list[T]:
        pass

    async def check(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def __aenter__(self):
        await self.check()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
