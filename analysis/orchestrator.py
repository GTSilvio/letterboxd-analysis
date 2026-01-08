from .data_fetcher import DiaryFetcher
from .movie_master_builder import MovieMasterListBuilder
from .stats_calculator import StatsCalculator
from .report_printer import ReportPrinter

class LetterboxdAnalysis:
    """Orchestrates the entire Letterboxd data analysis pipeline."""

    def __init__(self, user: str, year: int, trace: bool = True):
        self.user = user
        self.year = year
        self.trace = trace

    def run(self, force_refresh: bool = False, summary_only: bool = False):
        fetcher = DiaryFetcher(self.user, self.year, trace=self.trace)
        diary_data = fetcher.fetch(force_refresh=force_refresh)

        builder = MovieMasterListBuilder(self.user, self.year, diary_data, trace=self.trace)
        # MovieMasterListBuilder.build() returns (master_list, cast_list, director_list, full_cast_list, full_director_list)
        master_list, cast_list, director_list, full_cast_list, full_director_list = builder.build(force_refresh=force_refresh)

        calculator = StatsCalculator(diary_data, master_list, cast_list, director_list, self.year, self.user, full_cast_list, full_director_list)
        stats = calculator.compute()
        full_stats = calculator.full_stats

        printer = ReportPrinter(stats, self.user, self.year, master_list, full_stats)
        printer.print_summary()

        """
        #jank but works I guess
        if not summary_only:
            print("\n--- Master Movie List Preview (first 5 entries) ---")
            for k, v in list(master_list.items())[:5]:
                print(v.get("name") or v.get("title") or "<unknown>")
                """