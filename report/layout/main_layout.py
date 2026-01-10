from dash import html, dcc
from .components import header_component, percent_heading, user_selection, monthly_movies_chart, ratings_distribution_chart, demographic_radio

def create_layout():

    return html.Div(
        [
            user_selection(),

            #Stores selected user globally
            dcc.Store(id="selected-user"),

            #This is where the header will be injected
            html.Div(id="header-container"),

            #Ratings distribution chart
            dcc.Graph(id="ratings-chart", config={'displayModeBar': False}),

            #Ratings distribution Pie Chart
            dcc.Graph(id="ratings-pie", config={'displayModeBar': False}),

            #Monthly movies watched
            dcc.Graph(id="rating-distribution", config={'displayModeBar': False}),

            #Weekly movies watched
            dcc.Graph(id="weekly-distribution", config={'displayModeBar': False}),

            #html stats showing average per month and week etc
            html.Div(id="average-per-month"),

            #graphs for genrea country languages
            html.Div(
                [
                    demographic_radio(),
                    html.Div(id="demographic-charts"),
                ]
            ),

            #graphs for percent breakdowns
            html.Div(
                [
                    percent_heading(),
                    html.Div(id="percent-charts"),
                ]
            ),


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
