from dash import html, dcc
from .components import header_component, user_selection, monthly_movies_chart, ratings_distribution_chart

def create_layout():

    return html.Div(
        [
            user_selection(),

            #Stores selected user globally
            dcc.Store(id="selected-user"),

            #This is where the header will be injected
            html.Div(id="header-container"),

            #Ratings distribution chart
            dcc.Graph(id="rating-distribution",
                      config={'displayModeBar': False}),

            #Ratings Chart
            dcc.Graph(id="ratings-chart",
                      config={'displayModeBar': False})
        ],

        style={
            "backgroundColor": "#2b2b2b", 
            "minHeight": "100vh",
            #"display": "flex",
            "flexDirection": "column",     # << important
            "alignItems": "center",        # center content horizontally
            #"color": "white",
            "padding": "20px",
        }
    )
