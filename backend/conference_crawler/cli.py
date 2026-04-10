from __future__ import annotations

import argparse

from loguru import logger

from .config import CrawlerSettings
from .logging_utils import setup_logging
from .pipeline import ConferenceCrawlerPipeline


DEFAULT_VENUES = ["AAAI", "ACL", "EMNLP"]
DEFAULT_YEARS = [2023, 2024, 2025]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Conference metadata crawler for AAAI/ACL/EMNLP.")
    parser.add_argument("--log-level", default="INFO", help="File log level, e.g. INFO or DEBUG.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common_arguments(target: argparse.ArgumentParser) -> None:
        target.add_argument("--venues", nargs="+", default=DEFAULT_VENUES, help="Venues to crawl.")
        target.add_argument("--years", nargs="+", type=int, default=DEFAULT_YEARS, help="Years to crawl.")

    crawl_parser = subparsers.add_parser("crawl-official", help="Fetch metadata from official sources only.")
    add_common_arguments(crawl_parser)

    enrich_parser = subparsers.add_parser("enrich", help="Enrich existing records with OpenAlex and Semantic Scholar.")
    enrich_parser.add_argument("--limit", type=int, default=None, help="Optional limit for enrichment workload.")
    add_common_arguments(enrich_parser)

    export_parser = subparsers.add_parser("export", help="Export SQLite records to partitioned parquet.")
    add_common_arguments(export_parser)

    run_all_parser = subparsers.add_parser("run-all", help="Official crawl, enrichment, and parquet export.")
    add_common_arguments(run_all_parser)
    run_all_parser.add_argument("--enrich-limit", type=int, default=None, help="Optional limit for enrichment workload.")

    subparsers.add_parser("stats", help="Refresh coverage report and print a sample record.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    settings = CrawlerSettings()
    log_path = setup_logging(settings.data_dir / "logs", args.command, log_level=args.log_level)
    pipeline = ConferenceCrawlerPipeline(settings)

    try:
        logger.warning("Running command={} log_path={}", args.command, log_path)
        if args.command == "crawl-official":
            pipeline.crawl_official(args.venues, args.years)
        elif args.command == "enrich":
            pipeline.enrich(venues=args.venues, years=args.years, limit=args.limit)
        elif args.command == "export":
            pipeline.export(venues=args.venues, years=args.years)
        elif args.command == "run-all":
            pipeline.run_all(args.venues, args.years, enrich_limit=args.enrich_limit)
        elif args.command == "stats":
            pipeline.state.write_coverage_report(settings.reports_dir / "coverage_report.csv")
            papers = pipeline.state.iter_papers()
            if papers:
                sample = papers[0]
                logger.info("Sample paper: {} {} {}", sample.venue, sample.year, sample.title)
            logger.info("Coverage report written to {}", settings.reports_dir / "coverage_report.csv")
        else:
            parser.error(f"Unknown command: {args.command}")
    finally:
        pipeline.close()
