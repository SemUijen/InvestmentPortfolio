"""Gold layer application entry point."""

from .pipelines.enrich_daily_results import main as enrich_daily_results_pipeline


def main() -> None:
    """Run gold layer pipelines."""
    enrich_daily_results_pipeline()


if __name__ == "__main__":
    main()
