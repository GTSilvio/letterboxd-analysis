from dash import Input, Output, dash_table, html, callback

"""
interactions.py

Responsible for:
- Handling interactive features like clicking pie chart slices.
- Updating tables or other components when interactions occur.
"""

def register_interaction_callbacks(app, stats):
    """
    Registers callbacks for interactive elements (click events).
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
        )
