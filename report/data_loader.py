import json
from pathlib import Path
from typing import Optional

"""
data_loader.py

Responsible for:
- Loading the stats.json file created by the analysis code.
- Providing helper functions to access or preprocess the data.
"""

def load_stats(
    stats_path: Optional[str] = None,
    cache_dir: str = "../cache",
    profile: Optional[str] = None,
    year: Optional[int] = None,
) -> dict:
    """Load the stats JSON.

    Behavior:
    - If `stats_path` is provided, it's resolved relative to this file and loaded.
    - Otherwise the function searches the `cache_dir` (relative to the package)
      for files matching `*_stats.json`.
    - If `profile` is provided the search is scoped to `cache/<profile>/` and if
      `year` is also provided it will prefer the exact file
      `<profile>/<year>/<profile>_<year>_stats.json`.

    Parameters
    ----------
    stats_path : Optional[str]
        Explicit path to the stats JSON (relative to this module). If given,
        this path is used directly.
    cache_dir : str
        Relative path to the cache directory (default: `../cache`).
    profile : Optional[str]
        Optional profile (user) name to scope the search.
    year : Optional[int]
        Optional year to further scope the search when `profile` is provided.

    Returns
    -------
    dict
        Parsed statistics.
    """
    base = Path(__file__).resolve().parent

    if stats_path:
        stats_file = base / stats_path
        if not stats_file.exists():
            raise FileNotFoundError(f"Specified stats_path not found: {stats_file}")
    else:
        cache_base = base / cache_dir
        if not cache_base.exists():
            raise FileNotFoundError(f"Cache directory not found: {cache_base}")

        # If profile+year specified, prefer the well-known filename layout
        if profile:
            if year:
                candidate = cache_base / profile / str(year) / f"{profile}_{year}_stats.json"
                if candidate.exists():
                    stats_file = candidate
                else:
                    raise FileNotFoundError(
                        f"No stats file for profile='{profile}' year={year} at {candidate}"
                    )
            else:
                profile_dir = cache_base / profile
                if not profile_dir.exists():
                    raise FileNotFoundError(f"Profile cache directory not found: {profile_dir}")

                matches = list(profile_dir.rglob(f"{profile}_*_stats.json"))
                if not matches:
                    raise FileNotFoundError(f"No stats files found for profile: {profile}")

                stats_file = max(matches, key=lambda p: p.stat().st_mtime)
        else:
            # No profile specified: search the whole cache for any *_stats.json
            matches = list(cache_base.rglob("*_stats.json"))
            if not matches:
                raise FileNotFoundError(f"No stats files found under cache: {cache_base}")

            # If more than one, pick the most recently modified
            stats_file = max(matches, key=lambda p: p.stat().st_mtime)

    with open(stats_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data
