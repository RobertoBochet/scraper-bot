from functools import cached_property
from logging import getLogger
from pathlib import Path
from sqlite3 import OperationalError
from typing import Callable, TypeVar

from diskcache import Cache
from pydantic_core import Url

from ..utilities.disk_cache_dsn import DiskCacheDsn
from .cache import Cache as CacheInterface
from .exceptions import CacheConnectionError

T = TypeVar("T")


_LOGGER = getLogger(__package__)


class DiskCache(CacheInterface):
    def __init__(self, dsn: str | Path | DiskCacheDsn):
        if isinstance(dsn, Url):
            dsn = dsn.path
        self._dsn = dsn

    @cached_property
    def _disk_cache(self) -> Cache:
        return Cache(self._dsn)

    async def exists(self, entry: str) -> bool:
        return entry in self._disk_cache

    async def add(self, entry: str) -> None:
        self._disk_cache.add(entry, "@")

    async def filter_exists(self, *entries: T, to_fingerprint: Callable[[T], str]) -> list[T]:
        return [e for e in entries if to_fingerprint(e) not in self._disk_cache]

    async def close(self):
        try:
            self._disk_cache.close()
        except OperationalError:
            pass

    async def check(self) -> None:
        try:
            self._disk_cache.check()
        except OperationalError:
            _LOGGER.error("Connection error while checking disk cache")
            raise CacheConnectionError
