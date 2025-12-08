from dash import html

from dash import html

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
            html.P(f"{stats['stats']['yearly_movie_count']} Movies"),
            html.P(f"{stats['stats']['yearly_review']} Reviews"),
            html.P(f"{stats['stats']['yearly_like']} Likes"),
            html.P(f"{round((stats['stats']['yearly_minutes_watched']/60), 1)} Hours"),
            """