from dash import html, dcc
from .components import header_component

"""
main_layout.py

Responsible for:
- Creating the full Dash page layout.
- Structuring the page (header, charts, tables, etc.).
- Importing reusable UI components.
"""

def create_layout(stats: dict):
    """
    Build and return the main layout for the dashboard.

    Parameters
    ----------
    stats : dict
        Stats loaded from data_loader.load_stats()

    Returns
    -------
    Dash layout object
    """
    return html.Div([
        header_component(stats),

        html.H2("Your Dashboard")],

        style={
        "backgroundColor": "#2b2b2b",  # dark full-page background
        "minHeight": "100vh",          # ensure it covers the full viewport
        "display": "flex",
        "color": "white",              # text color everywhere
        "padding": "20px",
        }


        #dcc.Graph(id="rating-distribution"),
        #html.Div(id="rating-table-output"),  # Table updates when chart clicked
    )
