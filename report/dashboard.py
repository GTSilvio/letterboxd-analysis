# report/dashboard.py

import os
from pathlib import Path
from dash import Dash
from report.data_loader import load_stats, load_diary
from report.layout.main_layout import create_layout
from report.callbacks.charts import register_chart_callbacks
from report.callbacks.interactions import register_interaction_callbacks

"""
Render-Ready Dashboard

- Reads defaults from environment variables:
    LETTERBOXD_USER (default: "gsilvio")
    LETTERBOXD_YEAR (default: 2025)
- Loads the corresponding stats JSON
- Builds layout and registers callbacks
- Exposes `server` for Gunicorn deployment
"""

# Read defaults from environment variables
USER = os.getenv("LETTERBOXD_USER", "paytonnriley") #currently where I swap the user need to make this more dynamic
YEAR = int(os.getenv("LETTERBOXD_YEAR", 2025))

# Determine cache directory relative to this file
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"

# Load stats JSON
stats = load_stats(
    cache_dir=str(CACHE_DIR),
    profile=USER,
    year=YEAR
)

# Load diary data JSON
diary_data = load_diary(
    cache_dir=str(CACHE_DIR),
    profile=USER,
    year=YEAR
)

# Create Dash app
app = Dash(__name__)
app.layout = create_layout()

# Register callbacks
register_chart_callbacks(app, stats, diary_data)
register_interaction_callbacks(app, stats, diary_data)

# Expose server for Render / Gunicorn
server = app.server

# Optional: allow running locally for testing
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
