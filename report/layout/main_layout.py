from dash import html, dcc
from .components import header_component, user_selection

def create_layout(stats: dict):

    return html.Div(
        [
            user_selection(),
            header_component(stats),

            # You can add more components below
            # dcc.Graph(id="rating-distribution"),
            # html.Div(id="rating-table-output"),
        ],

        style={
            "backgroundColor": "#2b2b2b", 
            "minHeight": "100vh",
            #"display": "flex",
            "flexDirection": "column",     # << important
            "alignItems": "center",        # center content horizontally
            "color": "white",
            "padding": "20px",
        }
    )
