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
        html.H1(f"Letterboxd Report for {stats["info"]["display_name"]}"),
        html.P(f"Year: {stats["info"]['year']}"),
        html.P(f"Total Reviews: {stats["stats"]['yearly_movie_count']}")
    ])
