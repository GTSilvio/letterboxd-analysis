from dash import dcc, html, Input, Output
import os
from pathlib import Path
from report.callbacks.charts import create_2025_pie, create_day_of_week, create_genre_chart, create_country_chart, create_language_chart, review_pie, rewatches_pie


#----------------------------------------------------Helper-Functions----------------------------------------------------



def get_available_users():
    """Get list of available users from cache directory."""
    cache_dir = Path(__file__).resolve().parent.parent.parent / "cache"
    if cache_dir.exists():
        return [d.name for d in cache_dir.iterdir() if d.is_dir()]
    return ["gsilvio"]  # fallback if cache doesn't exist

def get_available_years(user):
    """Get list of available years for a specific user from cache directory."""
    cache_dir = Path(__file__).resolve().parent.parent.parent / "cache" / user
    if cache_dir.exists():
        years = [d.name for d in cache_dir.iterdir() if d.is_dir()]
        return sorted(years, reverse=True)  # Sort descending (newest first)
    return []



def stat_box(number, label):
    return html.Div(
        [
            html.Div(str(number), style={
                "fontSize": "clamp(20px, 4vw, 32px)",
                "fontWeight": "bold",
            }),
            html.Div(label, style={
                "fontSize": "clamp(12px, 2.5vw, 16px)",
                "opacity": 0.8,
                "textAlign": "center",
            })
        ],
        style={
            "flex": "1 1 160px",     # responsive width
            "maxWidth": "240px",
            "textAlign": "center",
            "padding": "10px",
        }
    )


def stat_chart(fig, label, height="120px"):
    return html.Div(
        [
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False},
                style={"width": "100%", "height": height},
            ),
            html.Div(label, style={"fontSize": "14px", "opacity": 0.8}),
        ],
        style={
            "flex": "1 1 220px",
            "maxWidth": "400px",
            "minWidth": "180px",
            "alignItems": "center",
        }
    )




#----------------------------------------------------Layout-Functions----------------------------------------------------




def user_selection():
    available_users = get_available_users()
    default_user = available_users[0] if available_users else None
    available_years = get_available_years(default_user) if default_user else []
    
    return html.Div(
        [
            dcc.Dropdown(
                id="user-dropdown",
                options=[{"label": u, "value": u} for u in available_users],
                value=default_user,
                clearable=False,
                style={"flex": "1"},
            ),

            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": y, "value": y} for y in available_years],
                value=available_years[0] if available_years else None,
                clearable=False,
                style={"flex": "1"},
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
        style={"marginBottom": "20px", "display": "flex", "gap": "10px", "alignItems": "center"}
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
                style={"fontSize": "36px", "textAlign": "center"}
            ),

            # ---- NEW STAT BOX ROW ----
            html.Div(
                [
                    stat_box(len(stats['stats']['yearly_movie_count']), "Movies"),
                    stat_box(len(stats['stats']['yearly_review']), "Reviews"),
                    stat_box(len(stats['stats']['yearly_rewatch']), "Rewatches"),
                    stat_box(len(stats['stats']['yearly_like']), "Likes"),
                    stat_box(round((stats['stats']['yearly_minutes_watched']/60), 1), "Hours"),
                ],
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": "12px",
                    "justifyContent": "space-between",
                    "textAlign": "center",
                    "marginTop": "20px",
                    #"padding": "10px 0",
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

def average_movies_per_month(stats: dict):

    return html.Div(
        [
            
            # ---- NEW STAT BOX ROW ----
            html.Div(
                [
                    stat_box(len(stats['stats']['yearly_movie_count']), "Movies Watched This Year"),
                    stat_box(stats['stats']['average_count_monthly'], "Average per Month"),
                    stat_box(stats['stats']['average_count_weekly'], "Average per Week"),
                    stat_chart(create_day_of_week(stats),"", height="120px"),

                ],
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": "12px",
                    "justifyContent": "space-between",
                    "textAlign": "center",
                    "marginTop": "20px",
                    #"padding": "10px 0",
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

def demographic_radio():
    return html.Div(
        [
            html.P(
                "Genres, Countries, & Languages",
                style={
                    "fontSize": "24px",
                    "marginBottom": "10px",
                },
            ),
            dcc.RadioItems(
                id="most-highest",
                options=[
                    {"label": "Most Watched", "value": "most"},
                    {"label": "Highest Rated", "value": "highest"},
                ],
                value="most",
                labelStyle={
                    "display": "inline-block",
                    "marginRight": "15px",
                    "color": "white",
                },
            ),
        ],
        style={
            "display": "flex",
            "color": "white",
            "justifyContent": "space-between",
            "alignItems": "center",
            "marginBottom": "10px",
            "borderBottom": "3px solid #555",
            "paddingBottom": "10px",
        },
    )


def demographic_charts(stats: dict, most_highest: bool = True):
    return html.Div(
        [
            
            # ---- NEW STAT BOX ROW ----
            html.Div(
                [
                    stat_chart(create_genre_chart(stats, most_highest), "", height="250px"),
                    stat_chart(create_country_chart(stats, most_highest), "", height="250px"),
                    stat_chart(create_language_chart(stats, most_highest), "", height="250px"),
                ],
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": "12px",
                    "justifyContent": "space-between",
                    "marginBottom": "20px",
                    "height": "250px",
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

def percent_heading():
    return html.Div(
        [
            html.P(
                "Breakdown",
                style={
                    "fontSize": "24px",
                    "marginBottom": "10px",
                },
            ),
        ],
        style={
            "display": "flex",
            "color": "white",
            "justifyContent": "space-between",
            "alignItems": "center",
            "marginBottom": "10px",
            "borderBottom": "3px solid #555",
            "paddingBottom": "10px",
        },
    )

def percent_charts(stats):
    return html.Div(
        [
            
            # ---- NEW STAT BOX ROW ----
            
            html.Div(
                [
                    stat_chart(create_2025_pie(stats), "", height="400px"),
                    stat_chart(rewatches_pie(stats), "", height="400px"),
                    stat_chart(review_pie(stats), "", height="400px"),
                ],
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": "12px",
                    "justifyContent": "space-between",
                    "marginBottom": "20px",
                    "height": "400px",
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
        dcc.Graph(
            id="rating-distribution",
            config={
                'displayModeBar': False,  # Hide toolbar
                'scrollZoom': False,      # Disable scroll-to-zoom
                'doubleClick': False      # Disable double-click zoom
            }
        ),
        html.Div(id="movies-list", style={
            "marginTop": "20px", 
            "padding": "10px",
            "backgroundColor": "#2b2b2b",
            "borderRadius": "5px",
            "minHeight": "100px"
        })
    ])


