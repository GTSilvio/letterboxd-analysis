from dash import Input, Output
import plotly.graph_objects as go
from report.data_loader import load_stats, load_diary
from pathlib import Path



#--------------------------------------------------------------------------------------------------------------------------



def create_horizontal_bar_chart(data_dict, max_items=10, height=250):
    if not data_dict:
        return go.Figure()

    counted_items = {
        key: len(value) if isinstance(value, (list, tuple, set)) else value
        for key, value in data_dict.items()
    }

    sorted_items = sorted(
        counted_items.items(),
        key=lambda x: x[1],
        reverse=True
    )[:max_items]

    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color="#717171",
            hovertemplate="%{y}: %{x}<extra></extra>",
        )
    )

    fig.update_layout(
        height=height,
        autosize=True,
        margin=dict(l=80, r=8, t=8, b=8),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=14),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, autorange="reversed"),
    )

    return fig

def create_pie_chart(data_dict, title="", max_items=10, colors=None):
    """
    Create a pie chart from a data dictionary.
    
    Parameters:
    - data_dict: Dictionary where keys are labels and values are either counts or lists
    - title: Chart title
    - max_items: Maximum number of items to show
    - colors: Optional list of colors for the pie slices
    """
    if not data_dict:
        return go.Figure()

    # Count items (handle both count values and list lengths)
    counted_items = {
        key: len(value) if isinstance(value, (list, tuple, set)) else value
        for key, value in data_dict.items()
    }

    # Sort by count descending and take top items
    sorted_items = sorted(
        counted_items.items(),
        key=lambda x: x[1],
        reverse=True
    )[:max_items]

    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    # Default color scheme if none provided
    if colors is None:
        colors = [
            '#3A606E', '#4D6E76', '#607B7D', '#718580',
            '#828E82', '#969E88', '#AAAE8E', '#C5C7B7',
            '#D3D4CC', '#E0E0E0'
        ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
                marker=dict(colors=colors[:len(labels)]),
                sort=False,
            )
        ]
    )

    fig.update_layout(
        title=title,
        showlegend=True,
        legend=dict(
            title="Categories",
            traceorder="normal",
            itemclick=False,
            itemdoubleclick=False,
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
    )

    return fig

#--------------------------------------------------------------------------------------------------------------------------



"""
charts.py

Responsible for:
- Creating chart figures
- Registering callbacks that update charts
"""

CACHE_DIR = Path(__file__).resolve().parents[2] / "cache"

# --------------------------------------------------
# CALLBACK REGISTRATION
# --------------------------------------------------

def register_chart_callbacks(app, stats, diary_data):
    """
    Registers all chart-related callbacks.

    Parameters
    ----------
    app : Dash
        Dash application instance
    stats : dict
        Precomputed statistics
    diary_data : dict
        Diary entries grouped by month
    """

    # --------------------------------------------------
    # Monthly distribution (bar chart)
    # --------------------------------------------------

    @app.callback(
        Output("rating-distribution", "figure"),
        [Input("user-dropdown", "value"), Input("year-dropdown", "value"), Input("movie-filter", "value")],
    )
    def render_monthly_distribution(selected_user, selected_year, movie_filter):
        if not selected_user or not selected_year:
            return {}
        
        full_stats = (movie_filter == "full")
        diary = load_diary(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=int(selected_year),
        )
        return create_monthly_distribution(diary)
    
    @app.callback(
        Output("weekly-distribution", "figure"),
        [Input("user-dropdown", "value"), Input("year-dropdown", "value"), Input("movie-filter", "value")],
    )
    def render_weekly_distribution(selected_user, selected_year, movie_filter):
        if not selected_user or not selected_year:
            return {}
        
        full_stats = (movie_filter == "full")
        stats = load_stats(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=int(selected_year),
            full_stats=full_stats,
        )
        return create_weekly_distribution(stats)
        

    # --------------------------------------------------
    # Movie list when clicking a bar
    # --------------------------------------------------
    """
    @app.callback(
        Output("movies-list", "children"),
        Input("rating-distribution", "clickData")
    )
    def show_movies_for_month(clickData):
        if not clickData:
            return "Click on a month to see the movies watched."

        month = clickData["points"][0]["x"]

        if month not in diary_data:
            return f"No data for {month}"

        entries = diary_data[month]["entries"]

        return [
            f"{entry['name']} ({entry['actions'].get('rating', 'NR')})"
            for entry in entries.values()
        ]"""
    

    # --------------------------------------------------
    # Ratings distribution chart
    # --------------------------------------------------

    @app.callback(
        Output("ratings-chart", "figure"),
        [Input("user-dropdown", "value"), Input("year-dropdown", "value"), Input("movie-filter", "value")],
    )
    def render_ratings_distribution(selected_user, selected_year, movie_filter):
        if not selected_user or not selected_year:
            return {}
        
        diary = load_diary(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=int(selected_year),
        )
        return create_ratings_distribution(diary)
    
    @app.callback(
        Output("ratings-pie", "figure"),
        [Input("user-dropdown", "value"), Input("year-dropdown", "value"), Input("movie-filter", "value")],
    )
    def render_ratings_pie(selected_user, selected_year, movie_filter):
        if not selected_user or not selected_year:
            return {}
        
        diary = load_diary(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=int(selected_year),
        )
        return create_ratings_piechart(diary)


# --------------------------------------------------
# FIGURE BUILDERS (Pure Functions)
# --------------------------------------------------

def create_monthly_distribution(diary_data):
    """Bar chart showing movies watched per month."""

    # All months in order
    all_months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
    
    # Get counts for existing months, 0 for missing months
    counts = [diary_data.get(month, {"count": 0})["count"] for month in all_months]

    fig = go.Figure(
        data=[
            go.Bar(
                x=all_months,
                y=counts,
                marker_color="#717171", #'#357f4e',
                hovertemplate="<b>%{x}</b><br>Movies: %{y}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Movies Watched Per Month",
        xaxis_title="Month",
        yaxis_title="Count",
        showlegend=False,
        bargap=0,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        font_color='white',  # White text for dark backgrounds        
        xaxis=dict(showticklabels=True),  # Hide x-axis labels    
        yaxis=dict(showticklabels=True, showgrid=False),  # Hide y-axis numbers and grid
    )

    return fig

def create_weekly_distribution(data):
    """Bar chart showing movies watched per week."""

    #Extract weekly data from stats
    weekly_data = data.get("stats", {}).get("num_per_week", {})
    
    # Create all 52 weeks, filling with 0s for missing weeks
    all_weeks = [f"week {i}" for i in range(1, 54)]
    #weekly_date = [data.get("stats", {}).get("weeks list", {}) for i in range(1, 54)]
    counts = [len(weekly_data.get(week, [])) for week in all_weeks]

    fig = go.Figure(
        data=[
            go.Bar(
                x=all_weeks,
                y=counts,
                marker_color="#717171",
                hovertemplate="<b>%{x}</b><br>Movies: %{y}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Movies Watched Per Week",
        xaxis_title="Week",
        yaxis_title="Count",
        showlegend=False,
        bargap=0,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        font_color='white',  # White text for dark backgrounds        
        xaxis=dict(showticklabels=False),  # Hide x-axis labels    
        yaxis=dict(showticklabels=True, showgrid=False),  # Hide y-axis numbers and grid
    )

    return fig

def create_ratings_distribution(diary_data):
    """Bar chart of movie ratings."""

    ratings = [
        entry["actions"]["rating"]
        for month in diary_data.values()
        for entry in month["entries"].values()
        if entry["actions"]["rating"] is not None
    ]

    if not ratings:
        # Still show all rating bins even with no data
        all_ratings = list(range(1, 11))
        counts = [0] * 10
        display_labels = ['⯨','★','★⯨','★★','★★⯨','★★★','★★★⯨','★★★★','★★★★⯨','★★★★★']
    else:
        # Count occurrences of each rating
        rating_counts = {}
        for rating in ratings:
            rating_counts[rating] = rating_counts.get(rating, 0) + 1

        # All possible ratings 1-10
        all_ratings = list(range(1, 11))
        counts = [rating_counts.get(r, 0) for r in all_ratings]
        display_labels = ['⯨','★','★⯨','★★','★★⯨','★★★','★★★⯨','★★★★','★★★★⯨','★★★★★']

    fig = go.Figure(
        data=[
            go.Bar(
                x=display_labels,
                y=counts,
                marker_color="#717171", #'#357f4e',
                hovertemplate="<b>Rating %{x}</b><br>Movies: %{y}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Rating Distribution",
        xaxis_title="Rating",
        yaxis_title="Count",
        showlegend=False,
        bargap=0,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        font_color='white',  # White text for dark backgrounds
        xaxis=dict(showticklabels=True),  # Hide x-axis labels
        yaxis=dict(showticklabels=True, showgrid=False),  # Hide y-axis numbers and grid
    )

    return fig

def create_ratings_piechart(diary_data):
    """Create a pie chart showing movie ratings in descending star order."""

    # Extract ratings from diary data
    ratings = [
        entry["actions"]["rating"]
        for month in diary_data.values()
        for entry in month["entries"].values()
        if entry["actions"]["rating"] is not None
    ]

    # Define star labels in ascending order (used for mapping)
    star_labels = ['⯨','★','★⯨','★★','★★⯨','★★★','★★★⯨','★★★★','★★★★⯨','★★★★★']
    rating_values = list(range(1, 11))

    # Count ratings
    rating_counts = {r: 0 for r in rating_values}
    for r in ratings:
        rating_counts[r] += 1

    # Pair labels with counts
    combined = list(zip(star_labels, rating_values))
    counts = [rating_counts[r] for r in rating_values]

    # Remove zero-count ratings
    filtered = [(label, count) for label, count in zip(star_labels, counts) if count > 0]

    # Handle case where no ratings exist
    if not filtered:
        filtered_labels = ["No Ratings"]
        filtered_counts = [1]
    else:
        # Map stars to numeric values for sorting
        star_to_value = {
            '★★★★★': 5,
            '★★★★⯨': 4.5,
            '★★★★': 4,
            '★★★⯨': 3.5,
            '★★★': 3,
            '★★⯨': 2.5,
            '★★': 2,
            '★⯨': 1.5,
            '★': 1,
            '⯨': 0.5,
        }

        # Sort descending by rating
        filtered.sort(key=lambda x: star_to_value[x[0]], reverse=True)

        filtered_labels = [x[0] for x in filtered]
        filtered_counts = [x[1] for x in filtered]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=filtered_labels,
                values=filtered_counts,
                sort=False,  # VERY IMPORTANT: preserves order
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>Movies: %{value}<br>%{percent}<extra></extra>",
                marker=dict(
                    colors=[
                        '#3A606E', '#4D6E76', '#607B7D', '#718580',
                        '#828E82', '#969E88', '#AAAE8E', '#C5C7B7',
                        '#D3D4CC', '#E0E0E0'
                    ]
                )
            )
        ]
    )

    fig.update_layout(
        title="Rating Distribution",
        showlegend=True,
        legend=dict(
            title="Ratings",
            traceorder="normal",  # respect order in data
            itemclick=False,
            itemdoubleclick=False,
            #width = 500
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
    )

    return fig

def create_day_of_week(stats, hovered_index=None):
    full_days = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    short_labels = ["M", "T", "W", "T", "F", "S", "S"]

    day_data = stats.get("stats", {}).get("days_of_the_week", {})
    counts = [len(day_data.get(day, [])) for day in full_days]

    colors = [
        "#3A606E" if i == hovered_index else "#717171"
        for i in range(len(full_days))
    ]

    fig = go.Figure(
        go.Bar(
            x=full_days,
            y=counts,
            text=short_labels,
            textposition="inside",
            insidetextanchor="start",
            textfont=dict(size=12, color="white"),
            marker_color=colors,
            hovertemplate="%{x}: %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        height=120,
        autosize=True,
        margin=dict(l=6, r=6, t=6, b=6),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=10),
        bargap=0,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    )

    return fig

def create_genre_chart(stats,genre: bool=True):
    if genre:
        this = "genres"
    else:
        this = "genre_averages"
    #"genres"
    #"genre_averages"
    return create_horizontal_bar_chart(stats["stats"][this],)


def create_country_chart(stats,country: bool=True):
    if country:
        this = "country"
    else:
        this = "country_averages"
    #"country"
    #"country_averages"
    return create_horizontal_bar_chart(stats["stats"][this],)


def create_language_chart(stats,language: bool=True):
    if language:
        this = "language"
    else:
        this = "language_averages"
    #"language"
    #"language_averages"
    return create_horizontal_bar_chart(stats["stats"][this],)

def create_2025_pie(stats):
    current_year = int(stats["info"]["year"])

    current_year_movies = round(stats.get('stats', {}).get("percent_current_years", 0) * len(stats.get('stats', {}).get("yearly_movie_count", 1)),0)
    total_movies = round(len(stats.get('stats', {}).get("yearly_movie_count", 1)) - current_year_movies,0)

    data = [
        current_year_movies,
        total_movies
    ]

    labels = [str(current_year), "Older"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=data,
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
                sort=False,
                marker=dict(
                    colors=[
                        '#3A606E',
                        '#717171'
                    ]
                )
            )
        ]
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
    )

    return fig

def rewatches_pie(stats):
    rewatches = stats.get("stats", {}).get("yearly_rewatch", {})
    watches = stats.get("stats", {}).get("yearly_movie_count", {})
    data = [
        (len(watches) - len(rewatches)),
        len(rewatches)
    ]

    labels = ["New Watches", "Rewatched"]
    
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=data,
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
                sort=False,
                marker=dict(
                    colors=[
                        '#3A606E',
                        '#717171'
                    ]
                )
            )
        ]
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
    )

    return fig

def review_pie(stats):
    reviews = stats.get("stats", {}).get("yearly_review", {})
    watches = stats.get("stats", {}).get("yearly_movie_count", {})
    data = [
        len(reviews),
        (len(watches) - len(reviews)),
    ]

    labels = ["Reviewed", "Unreviewed"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=data,
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
                sort=False,
                marker=dict(
                    colors=[
                        '#3A606E',
                        '#717171'
                    ]
                )
            )
        ]
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
    )

    return fig