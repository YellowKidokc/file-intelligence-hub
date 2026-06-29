# Research Notes

These are the external references informing the first hub design.

## Filesystem watching

- Watchdog docs:
  https://python-watchdog.readthedocs.io/

Reason used here:

- event-driven folder watching is better than brute-force rescans for day-to-day work

## SQLite durability

- SQLite WAL:
  https://sqlite.org/wal.html
- SQLite FTS5:
  https://www.sqlite.org/fts5.html

Reason used here:

- WAL is the right default for an active local ledger
- FTS5 gives us fast text search over extracted text, summaries, and tags

## OpenAI enrichment lanes

- File Search in the Responses API:
  https://developers.openai.com/api/docs/guides/tools-file-search
- Batch API:
  https://developers.openai.com/api/docs/guides/batch

Reason used here:

- File Search is a good fit for knowledge-backed enrichment and retrieval
- Batch is a good fit for large delayed jobs where cost matters more than immediacy

## How these shape the hub

The resulting design choice is:

- event-driven local detection
- SQLite with WAL for durable local state
- FTS5 for search
- API enrichment as a later lane, not the first lane
- GUI for operation, Excel for audit
