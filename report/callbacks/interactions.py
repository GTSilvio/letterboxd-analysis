from dash import Input, Output, dash_table
from report.data_loader import load_stats, load_diary
from report.layout.components import header_component, average_movies_per_month, demographic_charts, get_available_years
from pathlib import Path
from report.callbacks.charts import create_weekly_distribution, create_monthly_distribution, create_ratings_distribution

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
    #USER DROPDOWN → YEAR DROPDOWN UPDATE
    #------------------------------
    @app.callback(
        [Output("year-dropdown", "options"), Output("year-dropdown", "value")],
        Input("user-dropdown", "value"),
    )
    def update_year_options(selected_user):
        if not selected_user:
            return [], None
        
        available_years = get_available_years(selected_user)
        options = [{"label": y, "value": y} for y in available_years]
        value = available_years[0] if available_years else None
        return options, value

    #------------------------------
    #USER & YEAR DROPDOWN → HEADER UPDATE
    #------------------------------
    @app.callback(
        Output("header-container", "children"),
        [Input("user-dropdown", "value"), Input("year-dropdown", "value"), Input("movie-filter", "value")],
    )
    def update_header(selected_user, selected_year, movie_filter):
        if not selected_user or not selected_year:
            return "Select a user and year to begin"

        full_stats = (movie_filter == "full")
        stats = load_stats(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=int(selected_year),
            full_stats=full_stats,
        )

        return header_component(stats)
    
    @app.callback(
        Output("average-per-month", "children"),
        [Input("user-dropdown", "value"), Input("year-dropdown", "value"), Input("movie-filter", "value")],
    )
    def update_average_per_month(selected_user, selected_year, movie_filter):
        if not selected_user or not selected_year:
            return "Select a user and year to begin"

        full_stats = (movie_filter == "full")
        stats = load_stats(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=int(selected_year),
            full_stats=full_stats,
        )

        return average_movies_per_month(stats)
    
    @app.callback(
        Output("demographic-charts", "children"),
        [Input("user-dropdown", "value"), Input("year-dropdown", "value"), Input("movie-filter", "value")],
    )
    def update_demographic_charts(selected_user, selected_year, movie_filter):
        if not selected_user or not selected_year:
            return "Select a user and year to begin"

        full_stats = (movie_filter == "full")
        stats = load_stats(
            cache_dir=str(CACHE_DIR),
            profile=selected_user,
            year=int(selected_year),
            full_stats=full_stats,
        )

        return demographic_charts(stats)