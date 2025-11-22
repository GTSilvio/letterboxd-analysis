from dash import Input, Output
import plotly.express as px

"""
charts.py

Responsible for:
- Creating chart callbacks (histograms, pie charts, bar charts).
- Returning figures based on stats.
"""

def register_chart_callbacks(app, stats):
    """
    Registers all chart-related callbacks.

    Parameters
    ----------
    app : Dash
        Dash app instance
    stats : dict
        Stats loaded from JSON
    """

    @app.callback(
        Output("rating-distribution", "figure"),
        Input("rating-distribution", "id")   # Dummy input to trigger render
    )
    def render_rating_distribution(_):
        # Example histogram
        return px.histogram(
            x=stats["ratings"],
            nbins=10,
            title="Rating Distribution"
        )
