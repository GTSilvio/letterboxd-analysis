from dash import Input, Output, dcc, html
import plotly.express as px
import plotly.graph_objects as go

"""
charts.py

Responsible for:
- Creating chart callbacks (histograms, pie charts, bar charts).
- Returning figures based on stats.
"""

def register_chart_callbacks(app, stats, diary_data):
    """
    Registers all chart-related callbacks.

    Parameters
    ----------
    app : Dash
        Dash app instance
    stats : dict
        Stats loaded from JSON
    diary_data : dict
        Diary data loaded from JSON (organized by month)
    """

    # Convert monthly counts to lists for histogram
    months = list(stats["stats"]["monthly_movie_count"].keys())
    counts = list(stats["stats"]["monthly_movie_count"].values())

    @app.callback(
        Output("rating-distribution", "figure"),
        Input("rating-distribution", "id")   # Dummy input to trigger render
    )
    def render_rating_distribution(_):
        # Create histogram with clickable bars
        fig = go.Figure(
            data=[go.Bar(
                x=months,
                y=counts,
                customdata=months,  # Pass month names for click detection
                hovertemplate="<b>%{x}</b><br>Movies: %{y}<extra></extra>"
            )]
        )
        fig.update_layout(
            title="Movies Watched Per Month",
            xaxis_title="Month",
            yaxis_title="Count",
            showlegend=False
        )
        return fig

    @app.callback(
        Output("movies-list", "children"),
        Input("rating-distribution", "clickData")
    )
    def show_clicked_month_movies(clickData):
        """Display movies from the clicked month."""
        if not clickData:
            return "Click on a month to see the movies watched that month."
        
        # Extract month name from click data
        clicked_month = clickData["points"][0]["x"]
        
        # Get movies for that month
        if clicked_month not in diary_data:
            return f"No data for {clicked_month}"
        
        month_entries = diary_data[clicked_month]["entries"]
        
        # Build a list of movies
        movies_html = [f"<h4>Movies watched in {clicked_month}:</h4>"]
        for entry in month_entries.values():
            rating = entry["actions"]["rating"]
            rating_str = f" ⭐ {rating}/10" if rating else " (No rating)"
            movies_html.append(f"<div>• {entry['name']}{rating_str}</div>")
        
        return movies_html

