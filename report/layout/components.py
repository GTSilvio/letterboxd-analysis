from dash import html

"""
components.py

Responsible for:
- Small reusable UI components (header, cards, stat boxes, etc.)
"""

def header_component(stats: dict):
    """
    Top header with basic stats displayed.

    Example output:
        User: John (2024)
        123 reviews
    """
    return html.Div([
        html.H1(f"{stats["info"]["year"]}"),
        html.P(f"User: {stats["info"]['display_name']}"),
        html.P(f"{stats["stats"]['yearly_movie_count']} Movies"),
        html.P(f"{stats["stats"]['yearly_review']} Reviews"),
        html.P(f"{stats["stats"]['yearly_like']} Likes"),
        html.P(f"{round((stats["stats"]['yearly_minutes_watched']/60), 1)} Hours"),
    ])
