"""Small JSON file cache with collision-resistant cache keys."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


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

    def set(self, key: str, value: Any) -> None:
        """Write atomically to reduce the chance of partially written cache files."""
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

    def delete(self, key: str) -> bool:
        path = self.path_for(key)
        if not path.exists():
            return False
        path.unlink()
        return True
