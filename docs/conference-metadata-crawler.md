# Conference Metadata Crawler

## Scope

- Venues: `AAAI`, `ACL`, `EMNLP`
- Years: `2023`, `2024`, `2025`
- Output: partitioned `Parquet`

## Pipeline

1. `crawl-official`
   - `ACL` / `EMNLP`: discover volume pages from ACL Anthology venue pages, then parse official volume XML.
   - `AAAI`: discover issues from the AAAI OJS archive, then parse article pages.
2. `enrich`
   - OpenAlex first, then Semantic Scholar for missing `abstract` / `arxiv_id`.
3. `export`
   - Export SQLite staging data into `data/conference_metadata/parquet/papers/venue=<VENUE>/year=<YEAR>/papers.parquet`

## Commands

```bash
python -m backend.conference_crawler crawl-official --venues AAAI ACL EMNLP --years 2023 2024 2025
python -m backend.conference_crawler enrich
python -m backend.conference_crawler export --venues AAAI ACL EMNLP --years 2023 2024 2025
python -m backend.conference_crawler run-all --venues AAAI ACL EMNLP --years 2023 2024 2025
```

## PowerShell wrapper

```powershell
.\scripts\run_conference_crawler.ps1 -Command crawl-official
.\scripts\run_conference_crawler.ps1 -Command enrich -EnrichLimit 500
.\scripts\run_conference_crawler.ps1 -Command export
```

## Logs and progress

- Console progress uses `tqdm`
- Detailed logs are written to `data/conference_metadata/logs/`
- AAAI article-level failures are logged and skipped so a single broken request does not stop the whole batch

## Files

- SQLite state: `data/conference_metadata/state/crawl_state.db`
- Coverage report: `data/conference_metadata/reports/coverage_report.csv`
- Parquet dataset: `data/conference_metadata/parquet/papers/`
