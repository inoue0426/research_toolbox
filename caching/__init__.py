from .file_cache import JSONFileCache
from .lookup import cached_lookup


def open_cache(path=".cache"):
    """Open or create a JSON-backed cache directory."""
    return JSONFileCache(path)

__all__ = ["JSONFileCache", "cached_lookup", "open_cache"]
