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
                marker_color='#357f4e',  # Blue bars
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
        display_labels = ['⯨','★','★⯨','★★','★★⯨','★★★','★★★⯨','★★★★','★★★★⯨','★★★★★','★★★★★']
    else:
        # Count occurrences of each rating
        rating_counts = {}
        for rating in ratings:
            rating_counts[rating] = rating_counts.get(rating, 0) + 1

        # All possible ratings 1-10
        all_ratings = list(range(1, 11))
        counts = [rating_counts.get(r, 0) for r in all_ratings]
        display_labels = ['⯨','★','★⯨','★★','★★⯨','★★★','★★★⯨','★★★★','★★★★⯨','★★★★★','★★★★★']

    fig = go.Figure(
        data=[
            go.Bar(
                x=all_ratings,
                y=counts,
                marker_color='#357f4e',  # Orange bars
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
        xaxis=dict(
            tickmode='array',
            tickvals=all_ratings,
            ticktext=display_labels,  # Show stars on x-axis
        ),
    )

    return fig
