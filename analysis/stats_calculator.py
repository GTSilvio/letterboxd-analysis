from letterboxdpy.user import User
from datetime import date
import calendar

class StatsCalculator:
    """Calculates stats like movie counts, rewatches, reviews, and ratings."""

    all_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    full_movie = 75

    def __init__(self, diary_data: dict, master_list: dict, cast_list: dict, director_list: dict, year: int, user: str):
        self.diary_data = diary_data or {}
        self.master_list = master_list or {}
        self.cast_list = cast_list or {}
        self.director_list = director_list or {}
        self.year = year
        self.user = user
        self.user_info = User(self.user)
        self.stats = {}

    def add_months(self, keys=all_months, default_value=0):
        return {key: default_value for key in keys}

    def compute(self):



        #---------------------------------------Counts---------------------------------------



        #Monthly movie counts (safe with missing months)
        monthly_counts = {}
        full_monthly_counts = {}

        #add all the months to the counts dictionary
        monthly_counts = self.add_months()
        full_monthly_counts = self.add_months()

        #loop to count all the movies in the master list
        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]
            monthly_counts[month_name] = monthly_counts.get(month_name, 0) + 1

            if int(movie_data['runtime']) >= self.full_movie:
                month_name = self.all_months[movie_data['date']['month'] - 1]
                full_monthly_counts[month_name] = full_monthly_counts.get(month_name, 0) + 1

        #sum the months to get yearly total
        yearly_count = sum(monthly_counts.values())
        full_yearly_count = sum(full_monthly_counts.values())

        #average per month
        average_count_monthly = round((yearly_count / 12), 1)
        full_average_count_monthly = round((full_yearly_count / 12), 1)

        #average per week
        average_count_weekly = round((yearly_count / 52), 1)
        full_average_count_weekly = round((full_yearly_count / 52), 1)



        #---------------------------------------Rewatches---------------------------------------



        #Rewatches per month and total
        monthly_rewatch = {}

        #add all the months to the rewatches dictionary
        monthly_rewatch = self.add_months()

        #loop to rewatches all the rewatches in the master list
        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]
            if movie_data['rewatched'] == True:
                monthly_rewatch[month_name] = monthly_rewatch.get(month_name, 0) + 1
            else:
                pass

        #sum the months to get yearly totals
        total_rewatch = sum(monthly_rewatch.values())

        #% Rewatches
        percent_rewatches = round((total_rewatch/yearly_count), 2)




        #---------------------------------------Reviewed---------------------------------------

       

        #Reviewed per month and total
        monthly_review = {}

        #add all the months to the reviews dictionary
        monthly_review = self.add_months()

        #loop through to add all the reviews to dictionary
        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]
            if movie_data['reviewed'] == True:
                monthly_review[month_name] = monthly_review.get(month_name, 0) + 1
            else:
                pass

        #sum the months to get yearly totals
        total_review = sum(monthly_review.values())

        #percent reviewed
        percent_reviewed = round((total_review/yearly_count), 2)



        #---------------------------------------Likes---------------------------------------

        

        #Likes per month and total
        monthly_like = {}
        total_like = 0

        #add all the months to the monthly dictionary
        monthly_like = self.add_months()

        #loop through to add all the likes to dictionary
        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]
            if movie_data['liked'] == True:
                monthly_like[month_name] = monthly_like.get(month_name, 0) + 1
            else:
                pass

        #sum the months to get yearly totals
        total_like = sum(monthly_like.values())

        #percent liked
        percent_liked = round( (total_like/yearly_count) ,2)


        #---------------------------------------Ratings---------------------------------------

        

        #Ratings distribution year (1-10)
        yearly_rating_count = {float(i/2): 0 for i in range(1, 11)}
        monthly_rating_count = {}

        #Rating distribution for each month
        for month_num in self.all_months:
            monthly_rating_count[month_num] = {float(i/2): 0 for i in range(1, 11)}
        
        #Loop through each month
        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]
            
            #loop through and count each rating value per month
            if movie_data['rating'] != "null" and movie_data['rating'] != None:
                rating = float(movie_data['rating'])
                monthly_rating_count[month_name][rating] += 1

        #loop through each month and then each rating adding the total for each to the yearly total
        for month in monthly_rating_count:
            for rating in yearly_rating_count:
                yearly_rating_count[rating] += monthly_rating_count[month][rating]
        
        #Rating averages
        def average_from_counts(counts_dict):
            total_votes = sum(counts_dict.values())
            if total_votes == 0:
                return 0.0
            total_score = sum(r * c for r, c in counts_dict.items())
            return round(total_score / total_votes, 1)

        monthly_avg = {m: average_from_counts(c) for m, c in monthly_rating_count.items()}
        yearly_avg = average_from_counts(yearly_rating_count)



        #---------------------------------------Watch-Time---------------------------------------



        #establish varaibles yearly
        yearly_watch_hours = 0
        average_movie_legnth_y = 0

        #establish variables monthly
        monthly_watch_hours = {}
        average_movie_legnth_m = {}

        #add all the months to the watch time dictionary
        monthly_watch_hours = self.add_months()
        average_movie_legnth_m = self.add_months()

        for movie_num, movie_data in self.master_list.items():
            month_name = self.all_months[movie_data['date']['month'] - 1]
            if movie_data['runtime'] != 'null':
                monthly_watch_hours[month_name] += int(movie_data['runtime'])

        for month in monthly_watch_hours:
            average_movie_legnth_m[month] = round(((monthly_watch_hours[month] / monthly_counts[month]) if monthly_counts[month] != 0 else 0), 1)

        for month in monthly_watch_hours:
            yearly_watch_hours += monthly_watch_hours[month]

        average_movie_legnth_y = round(((yearly_watch_hours / yearly_count) if yearly_count != 0 else 0), 1)



        #---------------------------------------Number-Movies---------------------------------------


        
        #X movie watched
        x_movie_watched = {}
   

        x_movie_watched['1'] = self.master_list['1']['name']

        #loop through to add all the X movie to dictionary
        for movie_num, movie_data in self.master_list.items():
            if int(movie_num) % 25 == 0:
                x_movie_watched[movie_num] = movie_data['name']

        x_movie_watched['last'] = self.master_list[str(len(self.master_list))]['name']
        
            

        #---------------------------------------Top-Ratings---------------------------------------



        #Top Rated Movies
        Top_movies = {}
        highestrating = 0

        for movie_num, movie_data in self.master_list.items():
            if movie_data['rating'] != 'null' and movie_data['rating'] != None:
                if movie_data['rating'] > highestrating:
                    highestrating = movie_data['rating']
        
        for movie_num, movie_data in self.master_list.items():
            if movie_data['rating'] != 'null' and movie_data['rating'] != None and movie_data['rating'] == highestrating:
                Top_movies[movie_num] = movie_data['name']



        #---------------------------------------Top-Actor---------------------------------------

    

        #Top Actor
        top_actor = {}

        self.cast_list = dict(sorted(self.cast_list.items(), key=lambda x: x[1]["appearances"], reverse=True))

        for actor_slug, actor_data in list(self.cast_list.items())[:10]:
            top_actor[actor_data['name']] = actor_data['appearances']



        #---------------------------------------Top-Director---------------------------------------
        


        #Top Director
        top_director = {}

        self.director_list = dict(sorted(self.director_list.items(), key=lambda x: x[1]["appearances"], reverse=True))

        for director_slug, director_data in list(self.director_list.items())[:10]:
            top_director[director_data['name']] = director_data['appearances']

        
        
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



        #Create a dictionary to store movies per week
        weekly_movies = {}

        for num in range(52):
            weekly_movies[f'week {num+1}'] = []

        #Loop through all movies
        for key, movie in self.master_list.items():
            d = movie["date"]
            movie_date = date(d["year"], d["month"], d["day"])

            #Get ISO week number (1–52)
            week_number = movie_date.isocalendar()[1]

            #Add movie key to the corresponding week
            weekly_movies[f"week {week_number}"].append(str(key))



        #---------------------------------------Number-of-Watches-per-Day---------------------------------------



        # Create a dictionary to store movies per day
        daily_movies = {}

        # Determine if the year is a leap year
        # You should base this on the movies you're processing — for example the earliest movie:
        sample_year = next(iter(self.master_list.values()))['date']['year']

        days_in_year = 366 if calendar.isleap(sample_year) else 365

        # Create the correct number of days
        for num in range(days_in_year):
            daily_movies[f'day {num+1}'] = []

        # Loop through all movies
        for key, movie in self.master_list.items():
            d = movie['date']
            movie_date = date(d['year'], d['month'], d['day'])

            # tm_yday gives 1–365 or 1–366 automatically
            day_number = movie_date.timetuple().tm_yday

            # Add movie key to the corresponding day
            daily_movies[f'day {day_number}'].append(str(key))



        #---------------------------------------Watches-per-Week-Day---------------------------------------


        #refrence dictionary
        days_of_week = {0: "Monday",1: "Tuesday",2: "Wednesday",3: "Thursday",4: "Friday",5: "Saturday",6: "Sunday"}

        #Create a dictionary to store movies per day of the week
        days_of_the_week = {'Monday': [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}

        #loop through all movies
        for key, movie in self.master_list.items():
            d = movie['date']
            movie_date = date(d['year'], d['month'], d['day'])

            # Get day of the week (0=Monday, 6=Sunday)
            weekday_name = days_of_week[movie_date.weekday()]

            days_of_the_week[weekday_name].append(str(key))



        #---------------------------------------Genre---------------------------------------



        #Genere Dictionary
        genre_dict = {}

        for movie_num, movie_data in self.master_list.items():
            if movie_data['genres'] != []:
                for genre in movie_data['genres']:
                    if genre not in genre_dict:
                        genre_dict[genre] = []
                        genre_dict[genre].append(str(movie_num))
                    else:
                        genre_dict[genre].append(str(movie_num))

        #sort the dictionary by value
        genre_dict = dict(sorted(genre_dict.items(), key=lambda item: len(item[1]), reverse=True))



        #---------------------------------------Country---------------------------------------



        #country Dictionary
        country_dict = {}

        for movie_num, movie_data in self.master_list.items():
            if movie_data['country'] != []:
                for country in movie_data['country']:
                    if country not in country_dict:
                        country_dict[country] = []
                        country_dict[country].append(str(movie_num))
                    else:
                        country_dict[country].append(str(movie_num))

        #sort the dictionary by value
        country_dict = dict(sorted(country_dict.items(), key=lambda item: len(item[1]), reverse=True))



        #---------------------------------------Language---------------------------------------



        #language Dictionary
        language_dict = {}

        for movie_num, movie_data in self.master_list.items():
            if movie_data['language'] != []:
                for language in movie_data['language']:
                    if language not in language_dict:
                        language_dict[language] = []
                        language_dict[language].append(str(movie_num))
                    else:
                        language_dict[language].append(str(movie_num))

        #sort the dictionary by value
        language_dict = dict(sorted(language_dict.items(), key=lambda item: len(item[1]), reverse=True))

        for language in language_dict:
            templist = []
            for num in language_dict[language]:
                if num not in templist:
                    templist.append(num)
            language_dict[language] = templist
                


        #---------------------------------------Studio---------------------------------------



        #studios Dictionary
        studio_dict = {}

        for movie_num, movie_data in self.master_list.items():
            if movie_data['studio'] != []:
                for studio in movie_data['studio']:
                    if studio not in studio_dict:
                        studio_dict[studio] = []
                        studio_dict[studio].append(str(movie_num))
                    else:
                        studio_dict[studio].append(str(movie_num))
        
        #sort the dictionary by value
        studio_dict = dict(sorted(studio_dict.items(), key=lambda item: len(item[1]), reverse=True))



        #---------------------------------------Themes---------------------------------------



        #Themes


        
        #---------------------------------------Nanogenres---------------------------------------



        #Nanogenres



        #---------------------------------------Release-Year---------------------------------------


        
        #Release Year
        release_dict = {}

        for movie_num, movie_data in self.master_list.items():
            if movie_data['released'] != []:
                release_dict[movie_num] = movie_data['released']

        #% in current year
        current_year_counter = 0

        for movie_num, release_year in release_dict.items():
            if release_year == self.year:
                current_year_counter += 1

        percent_current_year = round((current_year_counter / yearly_count), 2)



        #---------------------------------------Rarest/popular---------------------------------------



        #Rarest Movie
        rarest = {}
        popular = {}

        for movie_num, movie_data in self.master_list.items():
            rarest[movie_num] = movie_data["popularity"]["members"]

        rarest = dict(sorted(rarest.items(), key=lambda item: int(item[1]), reverse=False))
        popular = dict(sorted(rarest.items(), key=lambda item: int(item[1]), reverse=True))



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
                if int(self.master_list[movie]['runtime']) >= self.full_movie:
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
                if int(self.master_list[movie]['runtime']) >= self.full_movie:
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

        self.stats['stats'] = {
            "monthly_movie_count": monthly_counts,
            "full_monthly_movie_count": full_monthly_counts,
            "yearly_movie_count": yearly_count,
            "full_yearly_movie_count": full_yearly_count,
            "average_count_monthly": average_count_monthly,
            "full_average_count_monthly": full_average_count_monthly,
            "average_count_weekly": average_count_weekly,
            "full_average_count_weekly": full_average_count_weekly,
            "monthly_rewatch": monthly_rewatch,
            "yearly_rewatch": total_rewatch,
            "percent_rewatches": percent_rewatches,
            "monthly_review": monthly_review,
            "yearly_review": total_review,
            "percent_review": percent_reviewed,
            "monthly_like": monthly_like,
            "yearly_like": total_like,
            "percent_liked": percent_liked,
            "yearly_rating_count": yearly_rating_count,
            "monthly_rating_count": monthly_rating_count,
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
            "country": country_dict,
            "language": language_dict,
            "studio": studio_dict,
            "releases": release_dict,
            "percent_current_years": percent_current_year,
            "rarest_movies": rarest,
            "popular_movies": popular,
            "most_movies_daily": most_movies_daily,
            "most_full_movies_daily": most_full_movies_daily,
            "most_movies_weekly": most_movies_weekly,
            "most_full_movies_weekly": most_full_movies_weekly,
            "consecutive_days": consecutive_days,
            "longest_daily_streak": longest_daily_streak,
            "consecutive_weeks": consecutive_weeks,
            "longest_weekly_streak": longest_weekly_streak
        }

        return self.stats