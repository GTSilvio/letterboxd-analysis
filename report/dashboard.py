# report/dashboard.py

from dash import Dash
from report.data_loader import load_stats
from report.layout.main_layout import create_layout
from report.callbacks.charts import register_chart_callbacks
from report.callbacks.interactions import register_interaction_callbacks
from pathlib import Path

class CreateDashboard:
    """
    Main Dash dashboard class.

    Usage:
        dashboard = CreateDashboard(user="gsilvio", year=2025, report=True)
        dashboard.run_dashboard()
    """

    def __init__(self, user: str, year: int, report: bool = True):
        self.user = user
        self.year = year
        self.report = report

        # Determine base path for cache
        # Assumes letterboxd_analysis/cache/ is a sibling to report/
        self.cache_dir = Path(__file__).resolve().parent.parent / "cache"

    def run_dashboard(self):
        """
        Load stats JSON, build the layout, register callbacks, and run Dash.
        """
        # Load stats dynamically based on user and year
        stats = load_stats(
            cache_dir=str(self.cache_dir),
            profile=self.user,
            year=self.year
        )

        # Create Dash app
        app = Dash(__name__)
        app.layout = create_layout(stats)

        # Register callbacks
        register_chart_callbacks(app, stats)
        register_interaction_callbacks(app, stats)

        # Run locally for debugging only
        if self.report:
            # Uncomment below for local testing
            # app.run(debug=True, host="0.0.0.0", port=8050)
            pass

        return app  # Return app object so Render can use it
