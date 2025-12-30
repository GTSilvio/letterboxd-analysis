from dash import Input, Output
import plotly.graph_objects as go
from report.data_loader import load_stats, load_diary
from pathlib import Path


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
        Input("user-dropdown", "value"),
    )
    def render_monthly_distribution(selected_user):
        stats = load_stats(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=2025,
        )

        diary = load_diary(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=2025,
            )
        return create_monthly_distribution(diary)
    
    @app.callback(
        Output("weekly-distribution", "figure"),
        Input("user-dropdown", "value"),
    )
    def render_weekly_distribution(selected_user):
        stats = load_stats(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=2025,
        )

        diary = load_diary(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=2025,
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
        Input("user-dropdown", "value"),
    )
    def render_ratings_distribution(selected_user):
        stats = load_stats(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=2025,
        )

        diary = load_diary(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=2025,
            )
        return create_ratings_distribution(diary)
    
    @app.callback(
        Output("ratings-pie", "figure"),
        Input("user-dropdown", "value"),
    )
    def render_ratings_pie(selected_user):
        stats = load_stats(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=2025,
        )

        diary = load_diary(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=2025,
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
    all_weeks = [f"week {i}" for i in range(1, 53)]
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
                x=all_ratings,
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
    """Pie chart of movie ratings."""

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

    # Filter out zero counts for cleaner pie chart
    filtered_labels = [display_labels[i] for i, count in enumerate(counts) if count > 0]
    filtered_counts = [count for count in counts if count > 0]

    if not filtered_counts:
        # If no ratings, show a single slice
        filtered_labels = ['No Ratings']
        filtered_counts = [1]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=filtered_labels,
                values=filtered_counts,
                marker_colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#ff99cc','#99ccff','#ffff99','#cc99ff','#99ffff','#ffb366'],
                hovertemplate="<b>%{label}</b><br>Movies: %{value}<extra></extra>",
                textinfo='percent',
                textfont_size=12,
            )
        ]
    )

    fig.update_layout(
        title="Rating Pie Chart",
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        font_color='white',  # White text for dark backgrounds
    )

    return fig