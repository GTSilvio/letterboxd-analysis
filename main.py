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
    Things to do:
    1. verify that movies are added in the right order
        1.1 if they are yippee all good (I dont think this is the case)
        1.2 if they aren't figure out if it is systamatic (I have a feeling it is adding them in reversed order for each day)
            1.2.1 edit code to make it work properly if its systamatic
        1.3 if its not systamatic then find a different way to put them in the right order or just give up :(
    2. make sure all charts are using stats if possible
        2.1 see if I can combine outputs and also possible with extra inputs (I think its possible)
    3. clean up code
        3.1 idk what needs to get done but it looks bad (probably look at what is on get hub for rendere and try to replicate)
    4. fix style
        4.1 use Letterboxd green and colors and style instead of the blue and stuff (not necessary but should get a consistent style)
            4.1.1 On the world map that same green is becoming a different color which is annoying need to fix that so all the greens look like the same color
        4.2 make it so that it works on phones and any screen size 
            4.2.1 maybe can get what size the screen is and then have everything be relative from there
        4.3 add little graphic flairs to make it look nice and stuff (will probably be many images)
    5. create a file that will download images for actors, directors, movies etc for each person and add them to their cache

    To Run Type ctrl + `
    Then paste: python main.py --user gsilvio --year 2025 --trace --report --force-refresh 
    --user:          is required;       type in your python username
    --year:          is not required;   will default to 2025
    --force-refresh: is not requred;    just will update the saved data
    --summary-only:  is not required;   skips detailed master list output
    --trace:         is not requred;    adds trace back allowing you to see how long things are taking
    --report:        is not required;    opens the online report dashboard
    ★⯨
    Usernames:
    gsilvio
    paytonnriley
    spookusweenie
    bonnegarcons
    """