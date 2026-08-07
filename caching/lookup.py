"""Generic cache-through lookup pattern."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol, TypeVar

T = TypeVar("T")
_MISSING = object()


class CacheLike(Protocol):
    def get(self, key: str, default: Any = None) -> Any: ...
    def set(self, key: str, value: Any) -> Any: ...


def cached_lookup(
    cache: CacheLike,
    key: str,
    fetcher: Callable[[], T],
    *,
    cache_none: bool = True,
) -> T:
    """Return cached value, otherwise call ``fetcher`` and cache its result.

    A private sentinel distinguishes a missing key from a cached ``None`` value.
    This is useful for expensive API/database lookups where a negative lookup is
    itself worth caching.
    """
    value = cache.get(key, _MISSING)
    if value is not _MISSING:
        return value

    value = fetcher()
    if value is not None or cache_none:
        cache.set(key, value)
    return value
