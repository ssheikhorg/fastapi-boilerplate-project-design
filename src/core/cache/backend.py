"""Redis client module."""
from typing import Any

from .redis import redis
from .base import BaseBackend


class RedisBackend(BaseBackend):
    """Redis backend."""

    def __init__(self):
        self.redis = redis

    async def get(self, key: str) -> Any:
        return self.redis.get(key)

    async def set(self, key: str, value: str = "1", timeout: int = None) -> None:
        if timeout:
            self.redis.set(name=key, value=value, ex=timeout)
        else:
            self.redis.set(name=key, value=value)

    async def delete(self, key: str) -> None:
        self.redis.delete(key)

    async def incr(self, key: str) -> int:
        return self.redis.incr(key)
