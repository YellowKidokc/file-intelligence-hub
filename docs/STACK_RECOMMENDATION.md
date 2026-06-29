# Stack Recommendation

## What we installed

The first bake-off environment installed cleanly and the import probe passed for:

- Docling
- Apache Tika
- FastEmbed
- OpenAI SDK
- watchdog
- psutil
- aiosqlite
- PyMuPDF
- BeautifulSoup
- lxml
- filetype
- openpyxl
- pandas
- python-docx

Probe output was written to:

`data/stack_compare.json`

## What we learned immediately

The full environment works, but it is not lightweight.

Measured virtual environment size after install:

- about `1.48 GB`

That means the "install everything and compare it" plan is viable, but the
"ship every watcher with every heavy dependency" plan is not.

## Recommended split

Use a two-tier stack.

### Tier A: thin local core

This should live on every local machine that watches folders:

- `watchdog`
- `psutil`
- `aiosqlite`
- `filetype`
- `PyMuPDF`
- `beautifulsoup4`
- `lxml`
- `openpyxl`
- `pandas`
- `python-docx`

Role:

- watch folders
- compute metadata
- extract text
- detect type
- write sidecars
- enqueue jobs
- perform deterministic tagging

### Tier B: heavy enrichment

This should live in the hub or on selected machines only:

- `docling`
- `fastembed`
- `tika`
- `openai`

Role:

- harder document extraction
- semantic comparison
- external knowledge lookups
- ambiguity resolution
- naming refinement
- folder summarization

## Specific package notes

### Docling

Strong candidate for rich document extraction, but it pulled in large
dependencies including `torch`, `torchvision`, `opencv_python`,
`onnxruntime`, and related model/runtime packages.

Interpretation:

- good hub candidate
- bad default watcher dependency

### Apache Tika

Good interoperability option, especially when you want broad file-family
coverage and are willing to treat it as a specialized extractor instead of the
default path for every file.

### FastEmbed

Good candidate for local semantic ranking and nearest-neighbor style matching,
but belongs closer to the hub than to tiny per-folder agents.

### OpenAI SDK

Best used as an arbitration and enrichment layer, not the first classifier.

## Recommended deployment shape

### Desktop / laptop agent

- watcher
- local extraction
- sidecar writing
- queue publishing
- review GUI

### Synology / forge-hub

- central FastAPI service
- SQLite ledger
- API orchestration
- heavy extractor lane
- search/index lane
- scheduled exports

## Bottom line

The right shape is not one monster install everywhere.

The right shape is:

- small local agents
- one heavier central hub
- GUI for day-to-day operation
- Excel for audit and reporting
