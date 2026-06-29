# Architecture

## Principle

Keep the heavy intelligence split across layers:

1. Local watcher
2. Local parser / classifier
3. API enrichment
4. SQLite ledger
5. GUI review / confirmation

## Why GUI first

The GUI should be the active operator surface for:

- rename suggestions
- move/copy/archive decisions
- search across tags/types/extensions
- confirmation for destructive thresholds
- review of low-confidence classifications

Excel is still useful, but mostly for:

- audit exports
- score summaries
- comparison tables
- bulk review after the fact

## Hub spots

This repo groups the core "hub spots":

- `scripts/` - test runners and bootstrap tools
- `bakeoff/` - compare parsers and classify outputs
- `gui/` - specs for the rename/search/review surface
- `config/` - shared schemas and example preferences
- `data/` - SQLite and temporary artifacts
