from redis import StrictRedis


class Cache:
    redis: StrictRedis

    def __init__(self, redis: str = "redis://127.0.0.1/0"):
        self.redis = StrictRedis.from_url(redis)

    def exists(self, entry: str) -> bool:
        return self.redis.exists(entry)

    def add(self, entry: str) -> None:
        self.redis.set(entry, "@")
