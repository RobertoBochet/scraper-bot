from pydantic_core import Url

from .cache import Cache
from .disk_cache import DiskCache
from .dummy_cache import DummyCache
from .redis_cache import RedisCache


def make_cache(cache_uri: Url | None) -> Cache:
    if cache_uri is None:
        return DummyCache()

    match cache_uri.scheme:
        case "redis" | "rediss":
            return RedisCache(cache_uri)
        case "diskcache":
            return DiskCache(cache_uri)

    raise NotImplementedError
