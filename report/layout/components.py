from dash import dcc, html, Input, Output
import os
from pathlib import Path



#----------------------------------------------------Helper-Functions----------------------------------------------------



def get_available_users():
    """Get list of available users from cache directory."""
    cache_dir = Path(__file__).resolve().parent.parent.parent / "cache"
    if cache_dir.exists():
        return [d.name for d in cache_dir.iterdir() if d.is_dir()]
    return ["gsilvio"]  # fallback if cache doesn't exist



def stat_box(number, label):
    return html.Div(
        [
            html.Div(str(number), style={
                "fontSize": "32px",      # bigger number
                "fontWeight": "bold",
                "marginBottom": "5px",
            }),
            html.Div(label, style={
                "fontSize": "16px",
                "opacity": 0.8,
            })
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "padding": "10px",
            "minWidth": "120px",
        }
    )



#----------------------------------------------------Layout-Functions----------------------------------------------------




def user_selection():
    available_users = get_available_users()
    
    return html.Div(
        [
            dcc.Dropdown(
                id="user-dropdown",
                options=[{"label": u, "value": u} for u in available_users],
                value=available_users[0],
                clearable=False,
            ),

            dcc.RadioItems(
                id="movie-filter",
                options=[
                    {"label": "All", "value": "all"},
                    {"label": "Full Movies Only", "value": "full"},
                ],
                value="all",
                labelStyle={
                    "display": "inline-block",
                    "marginRight": "15px",
                    "color": "white",
                },
            ),
        ],
        style={"marginBottom": "20px"}
    )

    
def header_component(stats: dict):

    return html.Div(
        [
            html.H1(
                f"{stats['info']['year']}",
                style={"fontSize": "144px", "marginBottom": "10px", "textAlign": "center"}
            ),

            html.P(
                f"{stats['info']['display_name']}'s Letterboxd Wrapped {stats['info']['year']}\n",
                style={"fontSize": "18px", "textAlign": "center"}
            ),

            # ---- NEW STAT BOX ROW ----
            html.Div(
                [
                    stat_box(stats['stats']['yearly_movie_count'], "Movies"),
                    stat_box(stats['stats']['yearly_review'], "Reviews"),
                    stat_box(stats['stats']['yearly_like'], "Likes"),
                    stat_box(round((stats['stats']['yearly_minutes_watched']/60), 1), "Hours"),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-around",
                    "textAlign": "center",
                    "marginTop": "20px",
                    "padding": "10px 0",
                }
            )
        ],
        
        style={
            "backgroundColor": "#2b2b2b",
            "color": "white",
            "fontSize": "18px",
            "padding": "20px",
            "borderRadius": "8px",
        }
    )

"""
def highest_rated_films(stats: dict):

    return html.Div(
        [
            html.P(
                f'{stats[]}'
            )
        ]
    )
"""



def ratings_distribution_chart():
    """Component for the ratings distribution histogram."""
    return html.Div([
        html.H2("Movie Ratings Distribution", style={"textAlign": "center", "marginBottom": "20px"}),
        dcc.Graph(id="ratings-chart"),
    ])



def monthly_movies_chart():
    """Component for the clickable monthly movies histogram."""
    return html.Div([
        html.H2("Movies Watched by Month", style={"textAlign": "center", "marginBottom": "20px"}),
        dcc.Graph(id="rating-distribution"),
        html.Div(id="movies-list", style={
            "marginTop": "20px", 
            "padding": "10px",
            "backgroundColor": "#2b2b2b",
            "borderRadius": "5px",
            "minHeight": "100px"
        })
    ])


