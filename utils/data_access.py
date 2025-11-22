import json
from pathlib import Path
from typing import Any


class DataAccess:
    """Simple helper for reading/writing JSON cache files.

    Files are stored under the repository root `cache/<user>/<year>/` by default.
    """

    def __init__(self, base_dir: Path | None = None):
        if base_dir is None:
            self.base = Path(__file__).resolve().parents[0]
        else:
            self.base = Path(base_dir)

        self.cache_root = self.base / "cache"

    def _make_cache_path(self, user: str, year: int, filename: str) -> Path:
        target_dir = self.cache_root / str(user) / str(year)
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir / filename

    def save_json(self, user: str, year: int, filename: str, data: Any) -> str:
        path = self._make_cache_path(user, year, filename)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        return str(path)

    def load_json(self, user: str, year: int, filename: str) -> Any:
        path = self.cache_root / str(user) / str(year) / filename
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return None
import os
import json

class DataAccess:
    """Handles caching, file I/O, and directory management."""

    def __init__(self, base_cache_dir="cache"):
        self.base_cache_dir = base_cache_dir
        os.makedirs(self.base_cache_dir, exist_ok=True)

    def _get_cache_path(self, user: str, year: int, filename: str) -> str:
        path = os.path.join(self.base_cache_dir, user, str(year))
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, filename)

    def save_json(self, user: str, year: int, filename: str, data: dict) -> str:
        path = self._get_cache_path(user, year, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return path

    def load_json(self, user: str, year: int, filename: str):
        path = self._get_cache_path(user, year, filename)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)