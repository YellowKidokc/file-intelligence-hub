# File Intelligence Hub

Central sandbox for the file-first automation stack.

This repo is the bake-off and packaging home for:

- local file parsers
- local embeddings / search helpers
- API enrichment
- watcher / router / ledger utilities
- GUI-facing review workflows

The goal is not to pick one giant brain on day one.
The goal is to package several strong components in one place, run them against the
same folders/files, and learn which combination is best.

## Current recommendation

Primary interaction surface:

- GUI for rename / search / move / review / confirmation

Secondary audit surfaces:

- SQLite for durable truth
- Excel for human-readable reporting

In other words:

- GUI = operating console
- SQLite = memory
- Excel = reports

## Stack under test

Local / Python:

- Docling
- Apache Tika (Python client)
- FastEmbed
- PyMuPDF
- BeautifulSoup + lxml
- watchdog
- psutil
- aiosqlite

API / external:

- OpenAI SDK

## Repo layout

```text
file-intelligence-hub/
  bakeoff/          parser and workflow comparisons
  config/           hub config examples
  data/             local SQLite + temporary outputs
  docs/             architecture, schema, decisions
  gui/              GUI-facing specs and later app code
  scripts/          bootstrap, tests, comparisons
  requirements.txt
```

## Quick start

From PowerShell:

```powershell
cd "D:\DONT TOUCH BOOT UP\file-intelligence-hub"
.\scripts\bootstrap_hub.ps1
```

Then run:

```powershell
.\.venv\Scripts\python.exe .\scripts\compare_stack.py
```

## First implementation targets

1. Get all candidate libraries installed in one clean environment.
2. Verify imports and versions.
3. Compare extraction on a small sample folder.
4. Decide what belongs in:
   - local watcher
   - local classifier
   - API enrichment
   - GUI review
5. Lock the schema before building the big automations.
