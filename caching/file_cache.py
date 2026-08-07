"""Small JSON file cache with collision-resistant keys and a dict-like API."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Callable, TypeVar

T = TypeVar("T")
_MISSING = object()


class JSONFileCache:
    """Store JSON-serializable values as one file per cache key."""

    def __init__(self, cache_dir: str | Path = ".cache") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _digest(key: str) -> str:
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def path_for(self, key: str) -> Path:
        return self.cache_dir / f"{self._digest(str(key))}.json"

    def contains(self, key: str) -> bool:
        return self.path_for(key).exists()

    def get(self, key: str, default: Any = None) -> Any:
        path = self.path_for(key)
        if not path.exists():
            return default
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def set(self, key: str, value: Any) -> Any:
        target = self.path_for(key)
        fd, tmp_name = tempfile.mkstemp(dir=self.cache_dir, suffix=".json.tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(value, handle, ensure_ascii=False, indent=2)
            os.replace(tmp_name, target)
        except Exception:
            try:
                os.unlink(tmp_name)
            except FileNotFoundError:
                pass
            raise
        return value

    def get_or_set(self, key: str, fetcher: Callable[[], T], *, cache_none: bool = True) -> T:
        value = self.get(key, _MISSING)
        if value is not _MISSING:
            return value
        value = fetcher()
        if value is not None or cache_none:
            self.set(key, value)
        return value

    def delete(self, key: str) -> bool:
        path = self.path_for(key)
        if not path.exists():
            return False
        path.unlink()
        return True

    def clear(self) -> None:
        for path in self.cache_dir.glob("*.json"):
            path.unlink()

    def __contains__(self, key: object) -> bool:
        return self.contains(str(key))

    def __getitem__(self, key: str) -> Any:
        value = self.get(key, _MISSING)
        if value is _MISSING:
            raise KeyError(key)
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        if not self.delete(key):
            raise KeyError(key)

    def __len__(self) -> int:
        return sum(1 for _ in self.cache_dir.glob("*.json"))
