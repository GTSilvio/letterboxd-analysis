from dash import Dash
from .data_loader import load_stats
from .layout.main_layout import create_layout
from .callbacks.charts import register_chart_callbacks
from .callbacks.interactions import register_interaction_callbacks

"""
dashboard.py

To Run:
python -m report.dashboard

This is the main entry point of your Dash application.
It:
- Loads JSON stats using data_loader
- Builds the layout
- Registers all callbacks
- Runs the server when executed directly
"""
class create_dashboard:

    def __init__(self, user: str, year: int, report: bool):
        self.user = user
        self.year = year
        self.report = report

    def run_dashboard(self):

        stats = load_stats()

        app = Dash(__name__)
        app.layout = create_layout(stats)

        # Register callback groups
        register_chart_callbacks(app, stats)
        register_interaction_callbacks(app, stats)

        app.run(debug=True)
