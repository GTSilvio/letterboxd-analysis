from dash import Input, Output, dash_table
from report.data_loader import load_stats, load_diary
from report.layout.components import header_component, averge_movies_per_month,demographic_charts
from pathlib import Path
from report.callbacks.charts import create_day_of_week, create_monthly_distribution, create_ratings_distribution

"""
interactions.py

Responsible for:
- Handling interactive features like clicking pie chart slices.
- Handling user selection and dynamic layout updates.
"""

CACHE_DIR = Path(__file__).resolve().parents[2] / "cache"


def register_interaction_callbacks(app, stats, diary_data):
    """
    Registers callbacks for interactive elements.
    """

    # ------------------------------
    # Rating chart interaction (DISABLED - now using monthly histogram)
    # ------------------------------
    """
    @app.callback(
        Output("rating-table-output", "children"),
        Input("rating-distribution", "clickData")
    )
    def show_movies_from_rating(clickData):
        if clickData is None:
            return "Click a bar to see movies from that rating."

        clicked_rating = clickData["points"][0]["x"]

        movies = [
            m for m in stats["movies"]
            if m["rating"] == clicked_rating
        ]

        return dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in movies[0].keys()],
            data=movies
        )"""
    
    #------------------------------
    #Hover interaction
    #------------------------------

    #@app.callback(
    #Output("average-per-day-of-week", "figure"),
    #Input("average-per-day-of-week", "hoverData"),
    #)
    #def update_day_chart(hoverData):
    #    hovered_index = None
    #
    #    if hoverData and "points" in hoverData:
    #        hovered_index = hoverData["points"][0]["pointIndex"]
    #
    #    return create_day_of_week(stats, hovered_index)


    #------------------------------
    #USER DROPDOWN → HEADER UPDATE
    #------------------------------
    @app.callback(
        Output("header-container", "children"),
        Input("user-dropdown", "value"),
    )
    def update_header(selected_user):
        if not selected_user:
            return "Select a user to begin"

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

        return header_component(stats)
    
    @app.callback(
        Output("average-per-month", "children"),
        Input("user-dropdown", "value"),
    )
    def update_average_per_month(selected_user):
        if not selected_user:
            return "Select a user to begin"

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

        return averge_movies_per_month(stats)
    
    @app.callback(
        Output("demographic-charts", "children"),
        Input("user-dropdown", "value"),
    )
    def update_average_per_month(selected_user):
        if not selected_user:
            return "Select a user to begin"

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

        return demographic_charts(stats)