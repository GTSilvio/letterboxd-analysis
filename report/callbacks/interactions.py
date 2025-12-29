from dash import Input, Output, dash_table
from report.data_loader import load_stats, load_diary
from report.layout.components import header_component
from pathlib import Path

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

    # ------------------------------
    # USER DROPDOWN → HEADER UPDATE
    # ------------------------------
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

        return header_component(stats)
