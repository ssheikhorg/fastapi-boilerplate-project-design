from typing import Protocol, Any


class BaseBackend(Protocol):
    async def get(self, key: str) -> Any:
        ...

    async def set(self, key: str, value: str, timeout: int = None) -> None:
        ...

    async def delete(self, key: str) -> None:
        ...

    async def incr(self, key: str) -> int:
        ...
