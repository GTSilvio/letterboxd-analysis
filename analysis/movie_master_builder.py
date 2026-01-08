from letterboxdpy.movie import Movie
from utils.data_access import DataAccess
import concurrent.futures


class MovieMasterListBuilder:
    """Builds a detailed list of movies and related metadata (parallel fetching)."""

    def __init__(self, username: str, year: int, diary_data: dict, trace: bool = True):
        self.username = username
        self.year = year
        self.diary_data = diary_data or {}
        self.trace = trace
        self.data_access = DataAccess()

        self.master_list = {}
        self.cast_list = {}
        self.director_list = {}
        self.full_cast_list = {}
        self.full_director_list = {}

    # ---------------------------------------------------------
    # Fetch movie + member stats safely in a worker thread
    # ---------------------------------------------------------
    def _fetch_movie_details(self, entry):
        slug = entry.get("slug")
        name = entry.get("name")

        try:
            movie_details = Movie(slug)
            members = movie_details.pages.members.get_watchers_stats()

            return slug, {
                "movie": movie_details,
                "members": members
            }

        except Exception as e:
            if self.trace:
                print(f"Error fetching '{name}' ({slug}): {e}")

            return slug, {
                "movie": None,
                "members": None
            }

    # ---------------------------------------------------------
    # Build full master + cast + director lists
    # ---------------------------------------------------------
    def build(self, force_refresh=False):

        cache_master = f"{self.username}_{self.year}_master.json"
        cache_cast = f"{self.username}_{self.year}_cast.json"
        cache_director = f"{self.username}_{self.year}_director.json"
        cache_full_cast = f"{self.username}_{self.year}_full_cast.json"
        cache_full_director = f"{self.username}_{self.year}_full_director.json"

        # -----------------------------------------------------
        # Try loading from cache first
        # -----------------------------------------------------
        if not force_refresh:

            cached_master = self.data_access.load_json(self.username, self.year, cache_master)
            cached_cast = self.data_access.load_json(self.username, self.year, cache_cast)
            cached_director = self.data_access.load_json(self.username, self.year, cache_director)
            cached_full_cast = self.data_access.load_json(self.username, self.year, cache_full_cast)
            cached_full_director = self.data_access.load_json(self.username, self.year, cache_full_director)

            if cached_master and cached_cast and cached_director and cached_full_cast and cached_full_director:
                self.master_list = cached_master
                self.cast_list = cached_cast
                self.director_list = cached_director
                self.full_cast_list = cached_full_cast
                self.full_director_list = cached_full_director

                if self.trace:
                    print(f"Loaded all cached list for {self.username} {self.year}")

                return self.master_list, self.cast_list, self.director_list, self.full_cast_list, self.full_director_list

        # -----------------------------------------------------
        # Gather all diary entries
        # -----------------------------------------------------
        all_entries = []
        for month_data in self.diary_data.values():
            all_entries.extend(month_data.get("entries", {}).values())

        # -----------------------------------------------------
        # Fetch movie details in parallel
        # -----------------------------------------------------
        # Fetch all movie details in parallel
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(self._fetch_movie_details, e) for e in all_entries]

            for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
                slug, details = future.result()
                results[slug] = details

                # ⬇️ THIS is the correct place for the trace print
                if self.trace and i % 10 == 0:
                    print(f"Fetched details for {i} movies...")

        # -----------------------------------------------------
        # Build master, cast, and director dictionaries
        # -----------------------------------------------------
        movie_num = 1

        for entry in all_entries:
            slug = entry.get("slug")
            name = entry.get("name")

            details_block = results.get(slug, {})
            movie_details = details_block.get("movie")
            details = movie_details.details
            members = details_block.get("members")

            # Skip movies that failed to fetch
            if not movie_details:
                continue

            # Extract fields safely
            studios = [s['name'] for s in details if s['type'] == 'studio']
            countries = [c['name'] for c in details if c['type'] == 'country']
            languages = [l['name'] for l in details if l['type'] == 'language']
            themes = [t['name'] for t in details if t['type'] == 'theme']

            # Build master record
            rating_val = entry.get("actions", {}).get("rating")
            record = {
                "name": name,
                "slug": slug,
                "rating": float(rating_val / 2) if rating_val is not None else None,
                "rewatched": bool(entry.get("actions", {}).get("rewatched")),
                "reviewed": bool(entry.get("actions", {}).get("reviewed")),
                "liked": bool(entry.get("actions", {}).get("liked")),
                "date": entry.get("date"),
                "released": movie_details.year,
                "runtime": getattr(movie_details, "runtime", None),
                "popularity": members,
                "average rating": movie_details.rating,
                "genres": [g.get("name") for g in getattr(movie_details, "genres", []) if g.get("type") == "genre"],
                #"themes": themes,
                "country": countries,
                "language": languages,
                "studio": studios
            }

            self.master_list[str(movie_num)] = record
            movie_num += 1
            if self.trace and movie_num % 10 == 0:
                print(f"Fetched details for {movie_num} movies...")

            # -------------------------------------------------
            # CAST LIST
            # -------------------------------------------------
            for member in getattr(movie_details, "cast", []):
                cast_slug = member.get("slug")
                cast_name = member.get("name")
                role = member.get("role_name")

                if not cast_slug or not cast_name:
                    continue

                if cast_slug not in self.cast_list:
                    self.cast_list[cast_slug] = {
                        "name": cast_name,
                        "slug": cast_slug,
                        "appearances": 0,
                        "roles": [],
                    }

                self.cast_list[cast_slug]["appearances"] += 1
                self.cast_list[cast_slug]["roles"].append((slug, role))

                # Add to full_cast_list if runtime >= 75
                if record.get("runtime") != 'null' and record.get("runtime") and int(record.get("runtime")) >= 75:
                    if cast_slug not in self.full_cast_list:
                        self.full_cast_list[cast_slug] = {
                            "name": cast_name,
                            "slug": cast_slug,
                            "appearances": 0,
                            "roles": [],
                        }
                    self.full_cast_list[cast_slug]["appearances"] += 1
                    self.full_cast_list[cast_slug]["roles"].append((slug, role))

            # -------------------------------------------------
            # DIRECTOR LIST
            # -------------------------------------------------
            crew = getattr(movie_details, "crew", {})
            directors = crew.get("director", [])
            if isinstance(directors, dict):
                directors = [directors]

            for director in directors:
                dir_slug = director.get("slug")
                dir_name = director.get("name")

                if not dir_slug or not dir_name:
                    continue

                if dir_slug not in self.director_list:
                    self.director_list[dir_slug] = {
                        "name": dir_name,
                        "slug": dir_slug,
                        "appearances": 0,
                        "movies": [],
                    }

                self.director_list[dir_slug]["appearances"] += 1
                self.director_list[dir_slug]["movies"].append(slug)

                # Add to full_director_list if runtime >= 75
                if record.get("runtime") != 'null' and record.get("runtime") and int(record.get("runtime")) >= 75:
                    if dir_slug not in self.full_director_list:
                        self.full_director_list[dir_slug] = {
                            "name": dir_name,
                            "slug": dir_slug,
                            "appearances": 0,
                            "movies": [],
                        }
                    self.full_director_list[dir_slug]["appearances"] += 1
                    self.full_director_list[dir_slug]["movies"].append(slug)

        # -----------------------------------------------------
        # Sort cast & director lists
        # -----------------------------------------------------
        self.cast_list = dict(sorted(self.cast_list.items(), key=lambda x: x[1]["appearances"], reverse=True))
        self.director_list = dict(sorted(self.director_list.items(), key=lambda x: x[1]["appearances"], reverse=True))
        self.full_cast_list = dict(sorted(self.full_cast_list.items(), key=lambda x: x[1]["appearances"], reverse=True))
        self.full_director_list = dict(sorted(self.full_director_list.items(), key=lambda x: x[1]["appearances"], reverse=True))

        # -----------------------------------------------------
        # Save to cache
        # -----------------------------------------------------
        self.data_access.save_json(self.username, self.year, cache_master, self.master_list)
        self.data_access.save_json(self.username, self.year, cache_cast, self.cast_list)
        self.data_access.save_json(self.username, self.year, cache_director, self.director_list)
        self.data_access.save_json(self.username, self.year, cache_full_cast, self.full_cast_list)
        self.data_access.save_json(self.username, self.year, cache_full_director, self.full_director_list)

        if self.trace:
            print(f"Saved all data lists for {self.username} {self.year}")

        return self.master_list, self.cast_list, self.director_list, self.full_cast_list, self.full_director_list
