import json
from pathlib import Path
from typing import Any


class DataAccess:
    """Simple helper for reading/writing JSON cache files.

    Files are stored under the repository root `cache/<user>/<year>/` by default.
    The repository root is assumed to be the parent of the `analysis` directory.
    """

    def __init__(self, base_dir: Path | None = None):
        # Default base dir is the project root (parent of this `analysis` folder)
        if base_dir is None:
            # __file__ -> .../analysis/utils/data_access.py
            # parents[1] -> .../letterboxd_analysis
            self.base = Path(__file__).resolve().parents[1]
        else:
            self.base = Path(base_dir)

        self.cache_root = self.base / "cache"

    def _make_cache_path(self, user: str, year: int, filename: str) -> Path:
        target_dir = self.cache_root / str(user) / str(year)
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir / filename

    def save_json(self, user: str, year: int, filename: str, data: Any) -> str:
        """Save `data` as JSON to cache and return the saved path as a string."""
        path = self._make_cache_path(user, year, filename)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        return str(path)

    def load_json(self, user: str, year: int, filename: str) -> Any:
        """Load JSON from cache if present, otherwise return None."""
        path = self.cache_root / str(user) / str(year) / filename
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return None
