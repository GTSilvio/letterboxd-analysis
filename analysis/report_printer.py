import json
from utils.data_access import DataAccess


class ReportPrinter:
    """Handles formatted output of results."""

    def __init__(self, stats: dict, user: str, year: int, master_list: dict):
        self.stats = stats or {}
        self.user = user
        self.year = year
        self.master_list = master_list or {}

    def print_summary(self):
        """print(f"\n===== Letterboxd Summary for {self.user} ({self.year}) =====\n")
        print(f"Total Movies Watched: {self.stats.get('yearly_movie_count')}")
        print(f"Total Rewatches: {self.stats.get('yearly_rewatch')}")
        print(f"Total Reviews: {self.stats.get('yearly_review')}")
        print(f"Total Likes: {self.stats.get('yearly_like')}")
        print(f'Total Minutes Watched: {self.stats.get('yearly_minutes_watched')}')
        print(f'Average Legnth of Movies Watched: {self.stats.get('yearly_average_legnth')}')

        print('\n')

        print("Movies Watched Per Month:")
        for month, count in self.stats.get('monthly_movie_count', {}).items():
            print(f"  {month}: {count}")

        print(f'\nNumber of Movies Watched This Year: {self.stats.get("yearly_movie_count")}')
        print(f'Average Movies Watched per Month: {self.stats.get("average_count_monthly")}')
        print(f'Average Movies Watched per Week: {self.stats.get("average_count_weekly")}')
        

        print("\nRewatches Per Month:")
        for month, count in self.stats.get('monthly_rewatch', {}).items():
            print(f"  {month}: {count}")

        print("\nReviews Per Month:")
        for month, count in self.stats.get('monthly_review', {}).items():
            print(f"  {month}: {count}")

        print("\nLikes Per Month:")
        for month, count in self.stats.get('monthly_like', {}).items():
            print(f"  {month}: {count}")

        print("\nRating Averages (Monthly):")
        for month, avg in self.stats.get('monthly_rating_average', {}).items():
            print(f"  {month}: {avg}")

        print(f"\nYearly Average Rating: {self.stats.get('yearly_rating_average')}")

        print("\nMinutes Watched Per Month:")
        for month, minutes in self.stats.get('monthly_minutes_watched', {}).items():
            print(f"  {month}: {minutes}")

        print("\nAverage Movie Length (Monthly):")
        for month, avg_len in self.stats.get('average_minutes_watched_monthly', {}).items():
            print(f"  {month}: {avg_len}")

        print('\nX Movies Watched: ')
        for num, movie in self.stats.get('X_movie_watched', {}).items():
            print(f'  {num}: {movie}')

        print('\nTop Movies Watched: ')
        for num, movie in self.stats.get('top_movies', {}).items(): 
            print(f'  {num}: {movie}')

        print('\nmultiwatched Movies: ')
        for slug, movie in self.stats.get('multiwatches', {}).items():
            for movie_num, movie_data in self.master_list.items():
                if slug == movie_data['slug']:
                    movie_name = movie_data['name']
                    pass
            print(f'  {movie_name}: {movie}')

        print('\nMost Watched Actors: ')
        for actor, num in self.stats.get('top_actors_10', {}).items(): 
            print(f'  {actor}: {num}')

        print('\nMost Watched Director: ')
        for director, num in self.stats.get('top_directors_10', {}).items(): 
            print(f'  {director}: {num}')

        print('\nMovies Watched per Week: ')
        for week, num in self.stats.get('num_per_week', {}).items(): 
            print(f'  {week}: {num}')

        print('\nMovies Watched per Day: ')
        for day, num in self.stats.get('num_per_day', {}).items(): 
            print(f'  {day}: {num}')

        print('\nMovies Watched per Weekday: ')
        for day, num in self.stats.get('days_of_the_week', {}).items(): 
            print(f'  {day}: {num}')
        print("\n")
        for day, num in self.stats.get('days_of_the_week', {}).items():
            print(f' {day}: {len(num)}')

        print('\nGenres: ')
        #for genre, num in self.stats.get('genres', {}).items():
        #    print(f'  {genre}: {num}')
        #print("\n")
        for genre, num in self.stats.get('genres', {}).items():
            print(f' {genre}: {len(num)}')

        print('\nCountries: ')
        #for country, num in self.stats.get('country', {}).items(): 
        #    print(f'  {country}: {num}')
        #print("\n")
        for country, num in self.stats.get('country', {}).items():
            print(f' {country}: {len(num)}')

        print('\nLanguage: ')
        for language, num in self.stats.get('language', {}).items(): 
            print(f'  {language}: {num}')
        print("\n")
        for language, num in self.stats.get('language', {}).items():
            print(f' {language}: {len(num)}')

        print('\nStudio: ')
        #for studio, num in self.stats.get('studio', {}).items(): 
        #    print(f'  {studio}: {num}')
        #print("\n")
        #for studio, num in self.stats.get('studio', {}).items():
        #    print(f' {studio}: {len(num)}')

        print('\nRelease Years: ')
        for num, year in self.stats.get('releases', {}).items(): 
            print(f'  {num}: {year}')
        print("\n")
        print(f'Percent Warched in {self.year}: {(self.stats.get('percent_current_years'))*100}%')

        print('\nRarest Movies: ')
        for num, movie in self.stats.get('rarest_movies', {}).items(): 
            print(f'  {num}: {movie}')

        print('\nPopular Movies: ')
        for num, movie in self.stats.get('popular_movies', {}).items(): 
            print(f'  {num}: {movie}')

        print('\nMost Movies Watched Daily: ')
        for day, movies in self.stats.get('most_movies_daily', {}).items(): 
            print(f'  {day}: {movies}')

        print('\nMost Full Movies Watched Daily: ')
        for day, movies in self.stats.get('most_full_movies_daily', {}).items(): 
            print(f'  {day}: {movies}')

        print('\nMost Movies Watched Weekly: ')
        for week, movies in self.stats.get('most_movies_weekly', {}).items(): 
            print(f'  {week}: {movies}')

        print('\nMost Full Movies Watched Weekly: ')
        for week, movies in self.stats.get('most_full_movies_weekly', {}).items(): 
            print(f'  {week}: {movies}')

        print('\nConsecutive Days: ')
        for streak, days in self.stats.get('consecutive_days', {}).items(): 
            print(f'  {streak}: {days}')
        
        print(f"\nLongest Daily streak: {self.stats.get('longest_daily_streak', {}).items()}")

        print('\nConsecutive Weeks: ')
        for streak, weeks in self.stats.get('consecutive_weeks', {}).items(): 
            print(f'  {streak}: {weeks}')

        print(f"\nLongest Weekly streak: {self.stats.get('longest_weekly_streak', {}).items()}")"""
        
        # Export stats to JSON file for downstream use
        try:
            self.export_stats_json()
        except Exception:
            # Defensive: don't crash the printer if saving fails
            pass

    def export_stats_json(self, path: str | None = None):
        """Write self.stats to the user's cache using DataAccess. If `path` is
        provided it will be used as a literal filename (saved into cwd). Otherwise
        we save into the cache directory under cache/<user>/<year>/<user>_<year>_stats.json.
        Returns the saved path on success.
        """
        filename = path or f"{self.user}_{self.year}_stats.json"
        try:
            if path:
                # Write directly to the provided path
                with open(filename, "w", encoding="utf-8") as fh:
                    json.dump(self.stats, fh, ensure_ascii=False, indent=2)
                print(f"Saved stats JSON to {filename}")
                return filename
            else:
                da = DataAccess()
                saved_path = da.save_json(self.user, self.year, filename, self.stats)
                print(f"Saved stats JSON to {saved_path}")
                return saved_path
        except Exception as e:
            print(f"Error saving stats JSON to {filename}: {e}")
            return None
        
