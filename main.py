import argparse
from analysis.orchestrator import LetterboxdAnalysis
from report.dashboard import app

def main():
    parser = argparse.ArgumentParser(description="Analyze your Letterboxd data")
    parser.add_argument("--user", required=True, help="Letterboxd username")
    parser.add_argument("--year", type=int, default=2025, help="Year to analyze")
    parser.add_argument("--force-refresh", action="store_true", help="Force API refresh")
    parser.add_argument("--summary-only", action="store_true", help="Skip detailed output")
    parser.add_argument("--report", action="store_true", help="produces online report")
    parser.add_argument("--trace", action="store_true", help="Enable detailed tracing output")

    args = parser.parse_args()

    analysis = LetterboxdAnalysis(args.user, args.year, trace=args.trace)
    analysis.run(force_refresh=args.force_refresh, summary_only=args.summary_only)

    
    if args.report:
        app.run(debug=True, host="0.0.0.0", port=8050)

    

if __name__ == "__main__":
    main()

    """
    To Run Type ctrl + `
    Then paste: python main.py --user spookusweenie --year 2025 --trace --force-refresh --report
    --user:          is required;       type in your python username
    --year:          is not required;   will default to 2025
    --force-refresh: is not requred;    just will update the saved data
    --summary-only:  is not required;   skips detailed master list output
    --trace:         is not requred;    adds trace back allowing you to see how long things are taking
    ★⯨
    Usernames:
    gsilvio
    paytonnriley
    spookusweenie
    bonnegarcons
    """