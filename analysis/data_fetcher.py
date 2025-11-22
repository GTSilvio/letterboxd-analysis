import concurrent.futures
from letterboxdpy.user import User
from utils.data_access import DataAccess
from datetime import date

class DiaryFetcher:
    """Fetches a user’s diary data for a given year (in parallel)."""

    MONTHS = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    def __init__(self, username: str, year: int, trace: bool = True, force_refresh = False):
        self.username = username
        self.year = year
        self.trace = trace
        self.diary_data = {}
        self.data_access = DataAccess()
        self.user_instance = User(username) if force_refresh == True else None
        

    def _fetch_month(self, month_index: int, force_refresh = False) -> tuple:
        """Fetch a single month safely (for threading)."""
        filename = f"diary_data_{self.username}_{self.year}.json"

        if force_refresh == True:
            try:
                data = self.user_instance.get_diary_month(self.year, month_index)
                if self.trace:
                    print(f"Fetched month {month_index} ({self.MONTHS[month_index - 1]})")
                return self.MONTHS[month_index - 1], data
            except Exception as e:
                if self.trace:
                    print(f"Error fetching month {month_index}: {e}")
                return self.MONTHS[month_index - 1], {"count": 0, "entries": {}}
        else:
            try:
                # Load the cached full diary file and extract the requested month
                full = self.data_access.load_json(self.username, self.year, filename)
                month_name = self.MONTHS[month_index - 1]
                if full and isinstance(full, dict) and month_name in full:
                    return month_name, full[month_name]
                else:
                    return month_name, {"count": 0, "entries": {}}
            except Exception as e:
                if self.trace:
                    print(f"Error fetching month {month_index}: {e}")
                return self.MONTHS[month_index - 1], {"count": 0, "entries": {}}

    def fetch(self, force_refresh=False):
        filename = f"diary_data_{self.username}_{self.year}.json"

        # Try cache first
        if not force_refresh:
            cached = self.data_access.load_json(self.username, self.year, filename)
            if cached:
                self.diary_data = cached
                if self.trace:
                    print(f"Loaded cached diary data for {self.username} {self.year}")
                return self.diary_data

        # Fetch all 12 months concurrently
        # If force_refresh is requested, create a User instance so threads can call the API
        if force_refresh and self.user_instance is None:
            self.user_instance = User(self.username)

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(self._fetch_month, i + 1, force_refresh) for i in range(12)]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is None:
                    # Defensive: ensure we don't crash if a worker returned None
                    continue
                month_name, data = result
                self.diary_data[month_name] = data

        # Create a list of entries with their dates for sorting
        all_entries = []
        for month_data in self.diary_data.values():
            for entry_id, entry in month_data["entries"].items():
                d = entry["date"]
                entry_date = date(self.year, d["month"], d["day"])
                all_entries.append((entry_date, entry_id, entry))

        # Sort entries by date
        all_entries.sort(key=lambda x: x[0])

        # Rebuild diary data structure with chronologically sorted entries
        sorted_data = {}
        for entry_date, entry_id, entry in all_entries:
            month_name = self.MONTHS[entry_date.month - 1]
            if month_name not in sorted_data:
                sorted_data[month_name] = {"count": 0, "entries": {}}
            sorted_data[month_name]["entries"][entry_id] = entry
            sorted_data[month_name]["count"] = len(sorted_data[month_name]["entries"])

        self.diary_data = sorted_data
        self.data_access.save_json(self.username, self.year, filename, self.diary_data)
        if self.trace:
            print(f"Saved full diary data to cache for {self.username} {self.year}")
        return self.diary_data
