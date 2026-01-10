from letterboxdpy.user import User
from datetime import date, timedelta
import calendar

class StatsCalculator:
    """Calculates stats like movie counts, rewatches, reviews, and ratings."""

    all_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    months_abreivated = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    full_movie = 75

    def __init__(self, diary_data: dict, master_list: dict, cast_list: dict, director_list: dict, year: int, user: str, full_cast_list: dict = None, full_director_list: dict = None):
        self.diary_data = diary_data or {}
        self.master_list = master_list or {}
        self.cast_list = cast_list or {}
        self.director_list = director_list or {}
        self.full_cast_list = full_cast_list or {}
        self.full_director_list = full_director_list or {}
        self.year = year
        self.user = user
        self.user_info = User(self.user)
        self.stats = {}
        self.full_stats = {}

    def add_months(self, keys=all_months, default_value=[]):
        return {key: default_value for key in keys}

    def compute(self):

        def get_top_people_from_master(master_list: dict, key: str, min_runtime: int | None = None, top_n: int = 10,):
            """
            key: 'cast' or 'directors'
            min_runtime: minimum runtime for "full" movies, or None for all
            """

            counts = {}

            for movie in master_list.values():
                runtime = movie.get("runtime")

                if min_runtime is not None:
                    if runtime == "null" or int(runtime) < min_runtime:
                        continue
                    
                people = movie.get(key, [])
                for person in people:
                    counts[person] = counts.get(person, 0) + 1

            return dict(
                sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
            )

        def _format_week_label(start: date, end: date) -> str:
            if start.month == end.month:
                return f"{start.strftime('%b')} {start.day}–{end.day}"
            return f"{start.strftime('%b')} {start.day}–{end.strftime('%b')} {end.day}"

        def build_weeks(year: int):
        
            start_of_year = date(year, 1, 1)
            end_of_year = date(year, 12, 31)

            weeks = []
            week_number = 1

            # ---- WEEK 1: Jan 1 → first Saturday ----
            days_until_saturday = (5 - start_of_year.weekday()) % 7
            first_week_end = start_of_year + timedelta(days=days_until_saturday)

            weeks.append({
                f"week {week_number}": _format_week_label(start_of_year, first_week_end)
            })

            week_number += 1
            current_start = first_week_end + timedelta(days=1)

            # ---- FOLLOWING WEEKS: Sunday → Saturday ----
            while current_start <= end_of_year:
                current_end = min(current_start + timedelta(days=6), end_of_year)

                weeks.append({
                    f"week {week_number}": _format_week_label(current_start, current_end)
                })

                current_start = current_end + timedelta(days=1)
                week_number += 1

            return weeks



        #---------------------------------------Counts---------------------------------------



        #Monthly movie counts (safe with missing months)
        monthly_counts = {}
        full_monthly_counts = {}

        #add all the months to the counts dictionary
        monthly_counts = self.add_months()
        full_monthly_counts = self.add_months()

        #yearly Count and yearly full conut
        yearly_count = []
        full_yearly_count = []

        #loop to count all the movies in the master list
        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]

            yearly_count.append(movie_num)

            if monthly_counts.get(month_name) is None:
                monthly_counts[month_name] = []
                monthly_counts[month_name].append(movie_num)

            elif monthly_counts.get(month_name) is not None:
                monthly_counts[month_name].append(movie_num)

            if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:

                full_yearly_count.append(movie_num)

                if full_monthly_counts.get(month_name) is None:
                    full_monthly_counts[month_name] = []
                    full_monthly_counts[month_name].append(movie_num)
                
                elif full_monthly_counts.get(month_name) is not None:
                    full_monthly_counts[month_name].append(movie_num)

        #average per month
        average_count_monthly = round((len(yearly_count) / 12), 1)
        full_average_count_monthly = round((len(full_yearly_count) / 12), 1)

        #average per week
        average_count_weekly = round((len(yearly_count) / 52), 1)
        full_average_count_weekly = round((len(full_yearly_count) / 52), 1)



        #---------------------------------------Rewatches---------------------------------------



        #Rewatches per month and total
        monthly_rewatch = {}
        full_monthly_rewatch = {}

        #add all the months to the rewatches dictionary
        monthly_rewatch = self.add_months()
        full_monthly_rewatch = self.add_months()

        #rewatches and yearly rewatches
        total_rewatch = []
        full_total_rewatch = []

        #loop to rewatches all the rewatches in the master list
        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]            

            if movie_data['rewatched'] == True:
                total_rewatch.append(movie_num)

                if monthly_rewatch.get(month_name) is None:
                    monthly_rewatch[month_name] = []
                    monthly_rewatch[month_name].append(movie_num)

                elif monthly_rewatch.get(month_name) is not None:
                    monthly_rewatch[month_name].append(movie_num)

                if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:

                    full_total_rewatch.append(movie_num)
                    
                    if full_monthly_rewatch.get(month_name) is None:
                        full_monthly_rewatch[month_name] = []
                        full_monthly_rewatch[month_name].append(movie_num)

                    elif full_monthly_rewatch.get(month_name) is not None:
                        full_monthly_rewatch[month_name].append(movie_num)
            else:
                pass

        #% Rewatches
        percent_rewatches = round((len(total_rewatch)/len(yearly_count)), 2)
        full_percent_rewatches = round((len(full_total_rewatch)/len(full_yearly_count)), 2)



        #---------------------------------------Reviewed---------------------------------------

       

        #Reviewed per month and total
        monthly_review = {}
        full_monthly_review = {}

        #add all the months to the reviews dictionary
        monthly_review = self.add_months()
        full_monthly_review = self.add_months()

        #reviews and full reviews
        total_review = []
        full_total_review = []

        #loop through to add all the reviews to dictionary
        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]

            if movie_data['reviewed'] == True:
                total_review.append(movie_num)

                if monthly_review.get(month_name) is None:
                    monthly_review[month_name] = []
                    monthly_review[month_name].append(movie_num)

                elif monthly_review.get(month_name) is not None:
                    monthly_review[month_name].append(movie_num)

                if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:
                    full_total_review.append(movie_num)

                    if full_monthly_review.get(month_name) is None:
                        full_monthly_review[month_name] = []
                        full_monthly_review[month_name].append(movie_num)

                    elif full_monthly_review.get(month_name) is not None:
                        full_monthly_review[month_name].append(movie_num)
            else:
                pass

        #percent reviewed
        percent_reviewed = round((len(total_review)/len(yearly_count)), 2)
        full_percent_reviewed = round((len(full_total_review)/len(full_yearly_count)), 2)



        #---------------------------------------Likes---------------------------------------

        

        #Likes per month and total
        monthly_like = {}
        full_monthly_like = {}

        #add all the months to the monthly dictionary
        monthly_like = self.add_months()
        full_monthly_like = self.add_months()

        #likes and full likes
        total_like = []
        full_total_like = []

        #loop through to add all the likes to dictionary
        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]
            
            if movie_data['liked'] == True:
                total_like.append(movie_num)

                if monthly_like.get(month_name) is None:
                    monthly_like[month_name] = []
                    monthly_like[month_name].append(movie_num)

                elif monthly_like.get(month_name) is not None:
                    monthly_like[month_name].append(movie_num)

                if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:
                    full_total_like.append(movie_num)

                    if full_monthly_like.get(month_name) is None:
                        full_monthly_like[month_name] = []
                        full_monthly_like[month_name].append(movie_num)

                    elif full_monthly_like.get(month_name) is not None:
                        full_monthly_like[month_name].append(movie_num)

            else:
                pass

        #percent liked
        percent_liked = round( (len(total_like)/len(yearly_count)) ,2)
        full_percent_liked = round( (len(full_total_like)/len(full_yearly_count)) ,2)



        #---------------------------------------Ratings---------------------------------------

        

        #Ratings distribution year (1-10) - lists of movie nums
        yearly_rating_movies = {float(i/2): [] for i in range(1, 11)}
        full_yearly_rating_movies = {float(i/2): [] for i in range(1, 11)}

        #Rating distribution for each month - lists
        monthly_rating_movies = {}
        full_monthly_rating_movies = {}

        for month_num in self.all_months:
            monthly_rating_movies[month_num] = {float(i/2): [] for i in range(1, 11)}
            full_monthly_rating_movies[month_num] = {float(i/2): [] for i in range(1, 11)}
        
        #Loop through movies for all
        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]
            
            if movie_data['rating'] not in ("null", None):
                rating = float(movie_data['rating'])
                monthly_rating_movies[month_name][rating].append(movie_num)

        #Aggregate to yearly
        for month in monthly_rating_movies:
            for rating in yearly_rating_movies:
                yearly_rating_movies[rating].extend(monthly_rating_movies[month][rating])
        
        #Rating averages
        def average_from_movies(movies_dict):
            total_votes = sum(len(lst) for lst in movies_dict.values())
            if total_votes == 0:
                return 0.0
            total_score = sum(r * len(lst) for r, lst in movies_dict.items())
            return round(total_score / total_votes, 1)

        monthly_avg = {m: average_from_movies(c) for m, c in monthly_rating_movies.items()}
        yearly_avg = average_from_movies(yearly_rating_movies)        
        
        #For full movies
        for movie_num, movie_data in self.master_list.items():
            if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:
                month_name = self.all_months[movie_data['date']['month'] - 1]
                if movie_data['rating'] not in ("null", None):
                    rating = float(movie_data['rating'])
                    full_monthly_rating_movies[month_name][rating].append(movie_num)

        for month in full_monthly_rating_movies:
            for rating in full_yearly_rating_movies:
                full_yearly_rating_movies[rating].extend(full_monthly_rating_movies[month][rating])

        full_monthly_avg = {m: average_from_movies(c) for m, c in full_monthly_rating_movies.items()}
        full_yearly_avg = average_from_movies(full_yearly_rating_movies)



        #---------------------------------------Watch-Time---------------------------------------



        #establish varaibles yearly
        yearly_watch_hours = 0
        full_yearly_watch_hours = 0
        average_movie_legnth_y = 0
        full_average_movie_legnth_y = 0

        #establish variables monthly
        monthly_watch_hours = {}
        full_monthly_watch_hours = {}
        average_movie_legnth_m = {}
        full_average_movie_legnth_m = {}

        #add all the months to the watch time dictionary
        monthly_watch_hours = self.add_months(default_value=0)
        full_monthly_watch_hours = self.add_months(default_value=0)
        average_movie_legnth_m = self.add_months(default_value=0)
        full_average_movie_legnth_m = self.add_months(default_value=0)

        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]
            if movie_data['runtime'] != 'null':
                monthly_watch_hours[month_name] += int(movie_data['runtime'])
                if int(movie_data['runtime']) >= self.full_movie:
                    full_monthly_watch_hours[month_name] += int(movie_data['runtime'])

        for month in monthly_watch_hours:
            average_movie_legnth_m[month] = round(((monthly_watch_hours[month] / len(monthly_counts[month])) if len(monthly_counts[month]) != 0 else 0), 1)
            full_average_movie_legnth_m[month] = round(((full_monthly_watch_hours[month] / len(full_monthly_counts[month])) if len(full_monthly_counts[month]) != 0 else 0), 1)

        for month in monthly_watch_hours:
            yearly_watch_hours += monthly_watch_hours[month]
            full_yearly_watch_hours += full_monthly_watch_hours[month]

        average_movie_legnth_y = round(((yearly_watch_hours / len(yearly_count)) if len(yearly_count) != 0 else 0), 1)
        full_average_movie_legnth_y = round(((full_yearly_watch_hours / len(full_yearly_count)) if len(full_yearly_count) != 0 else 0), 1)



        #---------------------------------------Number-Movies---------------------------------------


        
        #X movie watched
        x_movie_watched = {}
        full_x_movie_watched = {}

        x_movie_watched['1'] = self.master_list['1']['name']

        #loop through to add all the X movie to dictionary
        for movie_num, movie_data in self.master_list.items():
            if int(movie_num) % 25 == 0:
                x_movie_watched[movie_num] = movie_data['name']

        x_movie_watched['last'] = self.master_list[str(len(self.master_list))]['name']

        # For full, filter master_list to full movies, then pick same logic
        full_master_list = {k: v for k, v in self.master_list.items() if v['runtime'] != 'null' and int(v['runtime']) >= self.full_movie}
        if full_master_list:
            full_x_movie_watched['1'] = full_master_list['1']['name'] if '1' in full_master_list else None
            for movie_num in full_master_list:
                if int(movie_num) % 25 == 0:
                    full_x_movie_watched[movie_num] = full_master_list[movie_num]['name']
            last_key = str(len(full_master_list))
            if last_key in full_master_list:
                full_x_movie_watched['last'] = full_master_list[last_key]['name']
        
            

        #---------------------------------------Top-Ratings---------------------------------------



        #Top Rated Movies
        Top_movies = {}
        full_Top_movies = {}
        highestrating = 0
        full_highestrating = 0

        for movie_num, movie_data in self.master_list.items():
            if 'rating' in movie_data and movie_data['rating'] != 'null' and movie_data['rating'] != None:
                if movie_data['rating'] > highestrating:
                    highestrating = movie_data['rating']
        
        for movie_num, movie_data in self.master_list.items():
            if 'rating' in movie_data and movie_data['rating'] != 'null' and movie_data['rating'] != None and movie_data['rating'] == highestrating:
                Top_movies[movie_num] = movie_data['name']

        for movie_num, movie_data in self.master_list.items():
            if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie and 'rating' in movie_data and movie_data['rating'] != 'null' and movie_data['rating'] != None:
                if movie_data['rating'] > full_highestrating:
                    full_highestrating = movie_data['rating']
        
        for movie_num, movie_data in self.master_list.items():
            if int(movie_data['runtime']) >= self.full_movie and 'rating' in movie_data and movie_data['rating'] != 'null' and movie_data['rating'] != None and movie_data['rating'] == full_highestrating:
                full_Top_movies[movie_num] = movie_data['name']



        #---------------------------------------Top-Actor---------------------------------------

    

        top_actor = {
            data["name"]: data["appearances"]
            for _, data in sorted(
                self.cast_list.items(),
                key=lambda x: x[1]["appearances"],
                reverse=True
            )[:10]
        }

        full_top_actor = {
            data["name"]: data["appearances"]
            for _, data in sorted(
                self.full_cast_list.items(),
                key=lambda x: x[1]["appearances"],
                reverse=True
            )[:10]
        }   



        #---------------------------------------Top-Director---------------------------------------
        


        top_director = {
            data["name"]: data["appearances"]
            for _, data in sorted(
                self.director_list.items(),
                key=lambda x: x[1]["appearances"],
                reverse=True
            )[:10]
        }

        full_top_director = {
            data["name"]: data["appearances"]
            for _, data in sorted(
                self.full_director_list.items(),
                key=lambda x: x[1]["appearances"],
                reverse=True
            )[:10]
        }

        
        
        #---------------------------------------List-Multi-Watches---------------------------------------



        #Multiple Watches List
        multiwatches = {}
        multiwatches_helper = {}

        for movie_num, moive_data in self.master_list.items():
            if moive_data['slug'] not in multiwatches_helper:
                multiwatches_helper[moive_data['slug']] = []
                multiwatches_helper[moive_data['slug']].append(str(movie_num))
            else:
                multiwatches_helper[moive_data['slug']].append(str(movie_num))

        for key, data in multiwatches_helper.items():
            if len(data) > 1:
                multiwatches[key] = data



        #---------------------------------------Number-of-Watches-per-Week---------------------------------------



        #Create Weekly Dates
        weekly_dates = build_weeks(self.year)


        """Finish coding the rest of this adding the movies and such and return weekly_dates to the stats to be refrenced for graphics and such"""

        weekly_ranges = {}

        for week_dict in weekly_dates:
            for week_label, range_label in week_dict.items():
                start_str, end_str = range_label.split("–")

                MONTH_MAP = {
                    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
                    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
                    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
                }

                start_month_str, start_day = start_str.split()
                start_month = MONTH_MAP[start_month_str]
                start_day = int(start_day)

                if " " in end_str:
                    end_month_str, end_day = end_str.split()
                    end_month = MONTH_MAP[end_month_str]
                    end_day = int(end_day)
                else:
                    end_month = start_month
                    end_day = int(end_str)

                weekly_ranges[week_label] = (
                    date(self.year, start_month, start_day),
                    date(self.year, end_month, end_day),
                )

        weekly_movies = {week: [] for week in weekly_ranges}
        full_weekly_movies = {week: [] for week in weekly_ranges}

        for key, movie_data in self.master_list.items():
            d = movie_data["date"]
            movie_date = date(d["year"], d["month"], d["day"])

            for week, (start, end) in weekly_ranges.items():
                if start <= movie_date <= end:
                    weekly_movies[week].append(str(key))

                    if (
                        movie_data["runtime"] != "null"
                        and int(movie_data["runtime"]) >= self.full_movie
                    ):
                        full_weekly_movies[week].append(str(key))
                    break



        #---------------------------------------Number-of-Watches-per-Day---------------------------------------



        # Create a dictionary to store movies per day
        daily_movies = {}
        full_daily_movies = {}

        # Determine if the year is a leap year
        # You should base this on the movies you're processing — for example the earliest movie:
        sample_year = next(iter(self.master_list.values()))['date']['year']

        days_in_year = 366 if calendar.isleap(sample_year) else 365

        # Create the correct number of days
        for num in range(days_in_year):
            daily_movies[f'day {num+1}'] = []
            full_daily_movies[f'day {num+1}'] = []

        # Loop through all movies
        for key, movie in self.master_list.items():
            d = movie['date']
            movie_date = date(d['year'], d['month'], d['day'])

            # tm_yday gives 1–365 or 1–366 automatically
            day_number = movie_date.timetuple().tm_yday

            # Add movie key to the corresponding day
            daily_movies[f'day {day_number}'].append(str(key))
            if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:
                full_daily_movies[f'day {day_number}'].append(str(key))



        #---------------------------------------Watches-per-Week-Day---------------------------------------


        #refrence dictionary
        days_of_week = {0: "Monday",1: "Tuesday",2: "Wednesday",3: "Thursday",4: "Friday",5: "Saturday",6: "Sunday"}

        #Create a dictionary to store movies per day of the week
        days_of_the_week = {'Monday': [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}
        full_days_of_the_week = {'Monday': [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}

        #loop through all movies
        for key, movie in self.master_list.items():
            d = movie['date']
            movie_date = date(d['year'], d['month'], d['day'])

            # Get day of the week (0=Monday, 6=Sunday)
            weekday_name = days_of_week[movie_date.weekday()]

            days_of_the_week[weekday_name].append(str(key))
            if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:
                full_days_of_the_week[weekday_name].append(str(key))



        #---------------------------------------Genre---------------------------------------



        #Genere Dictionary
        genre_dict = {}
        full_genre_dict = {}
        genre_averages = {}
        full_genre_averages = {}

        for movie_num, movie_data in self.master_list.items():
            if 'genres' in movie_data and movie_data['genres'] != []:
                for genre in movie_data['genres']:
                    if genre not in genre_dict:
                        genre_dict[genre] = []
                        genre_dict[genre].append(str(movie_num))
                    else:
                        genre_dict[genre].append(str(movie_num))

                    if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:
                        if genre not in full_genre_dict:
                            full_genre_dict[genre] = []
                            full_genre_dict[genre].append(str(movie_num))
                        else:
                            full_genre_dict[genre].append(str(movie_num))

        #sort the dictionary by value
        genre_dict = dict(sorted(genre_dict.items(), key=lambda item: len(item[1]), reverse=True))
        full_genre_dict = dict(sorted(full_genre_dict.items(), key=lambda item: len(item[1]), reverse=True))

        #Get averages for each genere
        for genere, movie_genre_list in genre_dict.items():
            genre_total = 0
            genre_num = 0
            full_genre_total = 0
            full_genre_num = 0

            for movie_num in movie_genre_list:
                if movie_num in self.master_list and 'rating' in self.master_list[movie_num]:
                    rating = self.master_list[movie_num]['rating']
                    if rating != 'null' and rating != None:
                        genre_total += float(rating)
                        genre_num += 1
                        if self.master_list[movie_num]["runtime"] != "null" and int(self.master_list[movie_num]["runtime"]) >= self.full_movie:
                            full_genre_total += float(rating)
                            full_genre_num += 1

            if genre_num >= 4:
                genre_averages[genere] = round(genre_total / genre_num, 2)
            else:
                pass

            if full_genre_num >= 4:
                full_genre_averages[genere] = round(full_genre_total / full_genre_num, 2)
            else:
                pass

        #---------------------------------------Country---------------------------------------



        #country Dictionary
        country_dict = {}
        full_country_dict = {}

        for movie_num, movie_data in self.master_list.items():
            if 'country' in movie_data and movie_data['country'] != []:
                for country in movie_data['country']:
                    if country not in country_dict:
                        country_dict[country] = []
                        country_dict[country].append(str(movie_num))
                    else:
                        country_dict[country].append(str(movie_num))

                    if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:
                        if country not in full_country_dict:
                            full_country_dict[country] = []
                            full_country_dict[country].append(str(movie_num))
                        else:
                            full_country_dict[country].append(str(movie_num))

        #sort the dictionary by value
        country_dict = dict(sorted(country_dict.items(), key=lambda item: len(item[1]), reverse=True))
        full_country_dict = dict(sorted(full_country_dict.items(), key=lambda item: len(item[1]), reverse=True))

        #Get averages for each country
        country_averages = {}
        full_country_averages = {}

        for country, movie_country_list in country_dict.items():
            country_total = 0
            country_num = 0
            full_country_total = 0
            full_country_num = 0

            for movie_num in movie_country_list:
                if movie_num in self.master_list and 'rating' in self.master_list[movie_num]:
                    rating = self.master_list[movie_num]['rating']
                    if rating != 'null' and rating != None:
                        country_total += float(rating)
                        country_num += 1
                        if self.master_list[movie_num]["runtime"] != "null" and int(self.master_list[movie_num]["runtime"]) >= self.full_movie:
                            full_country_total += float(rating)
                            full_country_num += 1

            if country_num >= 4:
                country_averages[country] = round(country_total / country_num, 2)

            if full_country_num > 4:
                full_country_averages[country] = round(full_country_total / full_country_num, 2)



        #---------------------------------------Language---------------------------------------



        #language Dictionary
        language_dict = {}
        full_language_dict = {}

        for movie_num, movie_data in self.master_list.items():
            if 'language' in movie_data and movie_data['language'] != []:
                for language in movie_data['language']:
                    if language not in language_dict:
                        language_dict[language] = []
                        language_dict[language].append(str(movie_num))
                    else:
                        language_dict[language].append(str(movie_num))

                    if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:
                        if language not in full_language_dict:
                            full_language_dict[language] = []
                            full_language_dict[language].append(str(movie_num))
                        else:
                            full_language_dict[language].append(str(movie_num))

        #sort the dictionary by value
        language_dict = dict(sorted(language_dict.items(), key=lambda item: len(item[1]), reverse=True))
        full_language_dict = dict(sorted(full_language_dict.items(), key=lambda item: len(item[1]), reverse=True))

        for language in language_dict:
            templist = []
            for num in language_dict[language]:
                if num not in templist:
                    templist.append(num)
            language_dict[language] = templist

        for language in full_language_dict:
            templist = []
            for num in full_language_dict[language]:
                if num not in templist:
                    templist.append(num)
            full_language_dict[language] = templist
                

        #Get averages for each language
        language_averages = {}
        full_language_averages = {}

        for language, movie_language_list in language_dict.items():
            language_total = 0
            language_num = 0
            full_language_total = 0
            full_language_num = 0

            for movie_num in movie_language_list:
                if movie_num in self.master_list and 'rating' in self.master_list[movie_num]:
                    rating = self.master_list[movie_num]['rating']
                    if rating != 'null' and rating != None:
                        language_total += float(rating)
                        language_num += 1
                        if self.master_list[movie_num]["runtime"] != "null" and int(self.master_list[movie_num]["runtime"]) >= self.full_movie:
                            full_language_total += float(rating)
                            full_language_num += 1

            if language_num >= 4:
                language_averages[language] = round(language_total / language_num, 2)

            if full_language_num > 4:
                full_language_averages[language] = round(full_language_total / full_language_num, 2)
                


        #---------------------------------------Studio---------------------------------------



        #studios Dictionary
        studio_dict = {}
        full_studio_dict = {}

        for movie_num, movie_data in self.master_list.items():
            if 'studio' in movie_data and movie_data['studio'] != []:
                for studio in movie_data['studio']:
                    if studio not in studio_dict:
                        studio_dict[studio] = []
                        studio_dict[studio].append(str(movie_num))
                    else:
                        studio_dict[studio].append(str(movie_num))
                    
                    if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:
                        if studio not in full_studio_dict:
                            full_studio_dict[studio] = []
                            full_studio_dict[studio].append(str(movie_num))
                        else:
                            full_studio_dict[studio].append(str(movie_num))
        
        #sort the dictionary by value
        studio_dict = dict(sorted(studio_dict.items(), key=lambda item: len(item[1]), reverse=True))
        full_studio_dict = dict(sorted(full_studio_dict.items(), key=lambda item: len(item[1]), reverse=True))

        #Get averages for each studio
        studio_averages = {}
        full_studio_averages = {}

        for studio, movie_studio_list in studio_dict.items():
            studio_total = 0
            studio_num = 0
            full_studio_total = 0
            full_studio_num = 0

            for movie_num in movie_studio_list:
                if movie_num in self.master_list and 'rating' in self.master_list[movie_num]:
                    rating = self.master_list[movie_num]['rating']
                    if rating != 'null' and rating != None:
                        studio_total += float(rating)
                        studio_num += 1
                        if self.master_list[movie_num]["runtime"] != "null" and int(self.master_list[movie_num]["runtime"]) >= self.full_movie:
                            full_studio_total += float(rating)
                            full_studio_num += 1

            if studio_num >= 4:
                studio_averages[studio] = round(studio_total / studio_num, 2)

            if full_studio_num >= 4:
                full_studio_averages[studio] = round(full_studio_total / full_studio_num, 2)



        #---------------------------------------Themes---------------------------------------



        #Themes


        
        #---------------------------------------Nanogenres---------------------------------------



        #Nanogenres



        #---------------------------------------Release-Year---------------------------------------


        
        #Release Year
        release_dict = {}
        full_release_dict = {}

        for movie_num, movie_data in self.master_list.items():

            runtime = movie_data.get("runtime")

            if 'released' in movie_data and movie_data['released'] != []:

                if movie_data['released'] not in release_dict:
                    release_dict[movie_data['released']] = []
                    release_dict[movie_data['released']].append(str(movie_num))
                else:
                    release_dict[movie_data['released']].append(str(movie_num))

                if runtime != 'null' and int(runtime) >= self.full_movie:

                    if movie_data['released'] not in full_release_dict:
                        full_release_dict[movie_data['released']] = []
                        full_release_dict[movie_data['released']].append(str(movie_num))
                    else:
                        full_release_dict[movie_data['released']].append(str(movie_num))

        #% in current year
        current_year_counter = 0
        full_current_year_counter = 0

        for release_year, movie_list in release_dict.items():
            for movie_num in movie_list:
                runtime = self.master_list[movie_num].get("runtime")
                if release_year == self.year:
                    current_year_counter += 1
    
                    if runtime != 'null' and int(runtime) >= self.full_movie:
                        full_current_year_counter += 1

        percent_current_year = round((current_year_counter / len(yearly_count)), 2)
        full_percent_current_year = round((full_current_year_counter / len(full_yearly_count)), 2)



        #---------------------------------------Rarest/popular---------------------------------------



        #Rarest Movie
        rarest = {}
        popular = {}
        full_rarest = {}
        full_popular = {}

        for movie_num, movie_data in self.master_list.items():
            if "popularity" in movie_data and "members" in movie_data["popularity"]:
                rarest[movie_num] = movie_data["popularity"]["members"]
                if movie_data['runtime'] != 'null' and int(movie_data['runtime']) >= self.full_movie:
                    full_rarest[movie_num] = movie_data["popularity"]["members"]

        rarest = dict(sorted(rarest.items(), key=lambda item: int(item[1]), reverse=False))
        popular = dict(sorted(rarest.items(), key=lambda item: int(item[1]), reverse=True))
        full_rarest = dict(sorted(full_rarest.items(), key=lambda item: int(item[1]), reverse=False))
        full_popular = dict(sorted(full_rarest.items(), key=lambda item: int(item[1]), reverse=True))



        #---------------------------------------Most-Movies-in-a-Day---------------------------------------



        #Most Movies in a Day
        most_movies_daily = {}
        most_full_movies_daily = {}

        most_daily = 0
        for day, day_list in daily_movies.items():
            if len(day_list) > most_daily:
                most_daily = len(day_list)
                most_movies_daily = {}
                most_movies_daily[day] = day_list

            elif len(day_list) == most_daily:
                most_movies_daily[day] = day_list
        

        #Most Full Movies in a Day
        most_full_daily = 0
        for day, day_list in daily_movies.items():
            num_today = 0
            for movie in day_list:
                if self.master_list[movie]['runtime'] != 'null' and int(self.master_list[movie]['runtime']) >= self.full_movie:
                    num_today += 1
            
            if num_today > most_full_daily:
                most_full_daily = num_today
                most_full_movies_daily = {}
                most_full_movies_daily[day] = day_list

            elif num_today == most_full_daily:
                most_full_movies_daily[day] = day_list

        
        #most movies in a week
        most_movies_weekly = {}
        most_full_movies_weekly = {}

        most_weekly = 0
        for week, week_list in weekly_movies.items():
            if len(week_list) > most_weekly:
                most_weekly = len(week_list)
                most_movies_weekly = {}
                most_movies_weekly[week] = week_list

            elif len(week_list) == most_weekly:
                most_movies_weekly[week] = week_list
        

        #Most Full Movies in a week
        most_full_weekly = 0
        for week, week_list in weekly_movies.items():
            num_weekly = 0
            for movie in week_list:
                if self.master_list[movie]['runtime'] != 'null' and int(self.master_list[movie]['runtime']) >= self.full_movie:
                    num_weekly += 1
            
            if num_weekly > most_full_weekly:
                most_full_weekly = num_weekly
                most_full_movies_weekly = {}
                most_full_movies_weekly[week] = week_list

            elif num_weekly == most_full_weekly:
                most_full_movies_weekly[week] = week_list

        #---------------------------------------Movie-Streak---------------------------------------



        #Consecutive Days
        consecutive_days = {}
        longest_daily_streak = {}
        day_streak_streak = 1  # moved above loop

        for day, day_list in daily_movies.items():
            # skip if this day is already part of a streak
            if any(day in days for days in consecutive_days.values()):
                continue
            
            day_numbers = int(day.replace("day ", ""))
            day_num_streak = 0
            day_list_streak = []

            while True:
                next_key = f"day {day_numbers + day_num_streak}"
                next_day_movies = daily_movies.get(next_key)

                if next_day_movies and len(next_day_movies) > 0:
                    day_list_streak.append(next_key)
                    day_num_streak += 1
                else:
                    break
                
            if len(day_list_streak) > 1:
                consecutive_days[f"streak {day_streak_streak}"] = day_list_streak
                day_streak_streak += 1

        longest = 0
        for daily_streaks_num, daily_streak_values in consecutive_days.items():
            if len(daily_streak_values) > longest:
                longest = len(daily_streak_values)
                longest_daily_streak = {}
                longest_daily_streak[daily_streaks_num] = daily_streak_values
            elif len(daily_streak_values) == longest:
                longest_daily_streak[daily_streaks_num] = daily_streak_values
                    
        #Consecutive Weeks
        consecutive_weeks = {}
        longest_weekly_streak = {}
        week_streak_streak = 1  # moved above loop

        for week, week_list in weekly_movies.items():
            # skip if this week is already part of a streak
            if any(week in weeks for weeks in consecutive_weeks.values()):
                continue
            
            week_numbers = int(week.replace("week ", ""))
            week_num_streak = 0
            week_list_streak = []

            while True:
                next_key = f"week {week_numbers + week_num_streak}"
                next_week_movies = weekly_movies.get(next_key)

                if next_week_movies and len(next_week_movies) > 0:
                    week_list_streak.append(next_key)
                    week_num_streak += 1
                else:
                    break
                
            if len(week_list_streak) > 1:
                consecutive_weeks[f"streak {week_streak_streak}"] = week_list_streak
                week_streak_streak += 1

        longestW = 0
        for weekly_streaks_num, weekly_streak_values in consecutive_weeks.items():
            if len(weekly_streak_values) > longestW:
                longestW = len(weekly_streak_values)
                longest_weekly_streak = {}
                longest_weekly_streak[weekly_streaks_num] = weekly_streak_values
            elif len(weekly_streak_values) == longestW:
                longest_weekly_streak[weekly_streaks_num] = weekly_streak_values



        #---------------------------------------List---------------------------------------

        ###

        self.stats['info'] = {
            "username": self.user,
            "display_name": self.user_info.display_name,
            "year": self.year,
            "avatar_info": self.user_info.avatar,
            "favorites": self.user_info.favorites
            }
        
        self.full_stats['info'] = {
            "username": self.user,
            "display_name": self.user_info.display_name,
            "year": self.year,
            "avatar_info": self.user_info.avatar,
            "favorites": self.user_info.favorites
            }

        self.stats['stats'] = {
            "monthly_movie_count": monthly_counts,
            "yearly_movie_count": yearly_count,
            "average_count_monthly": average_count_monthly,
            "average_count_weekly": average_count_weekly,
            "monthly_rewatch": monthly_rewatch,
            "yearly_rewatch": total_rewatch,
            "percent_rewatches": percent_rewatches,
            "monthly_review": monthly_review,
            "yearly_review": total_review,
            "percent_review": percent_reviewed,
            "monthly_like": monthly_like,
            "yearly_like": total_like,
            "percent_liked": percent_liked,
            "yearly_rating_movies": yearly_rating_movies,
            "monthly_rating_movies": monthly_rating_movies,
            "monthly_rating_average": monthly_avg,
            "yearly_rating_average": yearly_avg,
            "yearly_minutes_watched": yearly_watch_hours,
            "yearly_average_legnth": average_movie_legnth_y,
            "monthly_minutes_watched": monthly_watch_hours,
            "average_minutes_watched_monthly": average_movie_legnth_m,
            "X_movie_watched": x_movie_watched,
            "top_movies": Top_movies,
            "top_actors_10": top_actor,
            "top_directors_10": top_director,
            "multiwatches": multiwatches,
            "num_per_week": weekly_movies,
            "num_per_day": daily_movies,
            "days_of_the_week": days_of_the_week,
            "genres": genre_dict,
            "genre_averages": genre_averages,
            "country": country_dict,
            "country_averages": country_averages,
            "language": language_dict,
            "language_averages": language_averages,
            "studio": studio_dict,
            "studio_averages": studio_averages,
            "releases": release_dict,
            "percent_current_years": percent_current_year,
            "rarest_movies": rarest,
            "popular_movies": popular,
            "most_movies_daily": most_movies_daily,
            "most_movies_weekly": most_movies_weekly,
            "consecutive_days": consecutive_days,
            "longest_daily_streak": longest_daily_streak,
            "consecutive_weeks": consecutive_weeks,
            "longest_weekly_streak": longest_weekly_streak,
            "weeks list": weekly_dates
        }

        self.full_stats['stats'] = {
            "monthly_movie_count": full_monthly_counts,
            "yearly_movie_count": full_yearly_count,
            "average_count_monthly": full_average_count_monthly,
            "average_count_weekly": full_average_count_weekly,
            "monthly_rewatch": full_monthly_rewatch,
            "yearly_rewatch": full_total_rewatch,
            "percent_rewatches": full_percent_rewatches,
            "monthly_review": full_monthly_review,
            "yearly_review": full_total_review,
            "percent_review": full_percent_reviewed,
            "monthly_like": full_monthly_like,
            "yearly_like": full_total_like,
            "percent_liked": full_percent_liked,
            "yearly_rating_movies": full_yearly_rating_movies,
            "monthly_rating_movies": full_monthly_rating_movies,
            "monthly_rating_average": full_monthly_avg,
            "yearly_rating_average": full_yearly_avg,
            "yearly_minutes_watched": full_yearly_watch_hours,
            "yearly_average_legnth": full_average_movie_legnth_y,
            "monthly_minutes_watched": full_monthly_watch_hours,
            "average_minutes_watched_monthly": full_average_movie_legnth_m,
            "X_movie_watched": full_x_movie_watched,
            "top_movies": full_Top_movies,
            "top_actors_10": full_top_actor,
            "top_directors_10": full_top_director,
            "multiwatches": multiwatches,
            "num_per_week": full_weekly_movies,
            "num_per_day": full_daily_movies,
            "days_of_the_week": full_days_of_the_week,
            "genres": full_genre_dict,
            "genre_averages": full_genre_averages,
            "country": full_country_dict,
            "country_averages": full_country_averages,
            "language": full_language_dict,
            "language_averages": full_language_averages,
            "studio": full_studio_dict,
            "studio_averages": full_studio_averages,
            "releases": full_release_dict,
            "percent_current_years": full_percent_current_year,
            "rarest_movies": full_rarest,
            "popular_movies": full_popular,
            "most_movies_daily": most_full_movies_daily,
            "most_movies_weekly": most_full_movies_weekly,
            "consecutive_days": consecutive_days,
            "longest_daily_streak": longest_daily_streak,
            "consecutive_weeks": consecutive_weeks,
            "longest_weekly_streak": longest_weekly_streak,
            "weeks list": weekly_dates
        }

        return self.stats