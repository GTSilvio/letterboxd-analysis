from dash import html

def header_component(stats: dict):

    return html.Div(
        [
            html.H1(
                f"{stats['info']['year']}",
                style={"fontSize": "144px", "marginBottom": "10px"}
            ),
            html.P(f"User: {stats['info']['display_name']}", style={"fontSize": "18px", "textAlign": "center"}),

            html.P(
                f"{stats['stats']['yearly_movie_count']} Movies"
                f"{stats['stats']['yearly_review']} Reviews"
                f"{stats['stats']['yearly_like']} Likes"
                f"{round((stats['stats']['yearly_minutes_watched']/60), 1)} Hours"
                   )

            
        ],
        
        style={
            "backgroundColor": "#2b2b2b",  # dark background
            "color": "white",              # white text
            "fontSize": "18px",            # make all stats paragraph-sized
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