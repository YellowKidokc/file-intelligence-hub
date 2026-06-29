# Automation Schema

## Goal

This hub is file-first. The system should react to files and folders entering the
workspace, classify them, log what happened, and only escalate to heavier
workers or API calls when needed.

The design rule is simple:

- local watchers detect
- local parsers extract
- local classifiers tag
- the ledger remembers
- the GUI approves risky actions
- Excel reports what happened

## Core lanes

The system is split into 12 lanes:

1. `watch`
2. `event_log`
3. `route`
4. `file_classify`
5. `folder_summarize`
6. `rename`
7. `tag`
8. `verify`
9. `api_enrich`
10. `search_index`
11. `export_import`
12. `audit_retry`

Each lane can be implemented by a lightweight local worker or by the central hub.

## Event lifecycle

Every item moves through the same coarse lifecycle:

1. Detect a file or folder change
2. Create an immutable event row
3. Snapshot file metadata
4. Decide the route
5. Run local extraction/classification
6. Escalate to API enrichment only if required
7. Generate rename/tag/move suggestions
8. Auto-apply safe actions or queue risky ones
9. Update indexes and audit exports
10. Close the job with success/failure state

## Event types

The first event vocabulary should stay small and stable:

- `created`
- `modified`
- `renamed`
- `moved`
- `copied`
- `deleted`
- `archived`
- `restored`
- `scan_requested`
- `reindex_requested`
- `api_requested`
- `api_completed`
- `api_failed`
- `manual_review_requested`
- `manual_review_completed`

## Action verbs

These are the operator verbs the GUI or automation can trigger:

- `detect`
- `snapshot`
- `classify`
- `summarize`
- `tag`
- `rename`
- `route`
- `move`
- `copy`
- `archive`
- `delete`
- `restore`
- `queue`
- `claim`
- `retry`
- `fail`
- `verify`
- `confirm`
- `index`
- `export`
- `import`
- `sync`
- `notify`
- `close`

## Trust zones

Not every decision should be handled the same way.

### Zone 1: Auto-safe

These can run automatically when confidence is high:

- metadata extraction
- MIME/type guessing
- hash generation
- text extraction
- deterministic tagging
- low-risk index updates

### Zone 2: Auto-with-thresholds

These can run automatically until they cross a threshold:

- rename batches
- move batches
- archive batches
- delete batches

Threshold defaults live in `config/preferences.example.json`.

### Zone 3: Manual review

These should always hit the review queue:

- low-confidence rename suggestions
- destructive actions over threshold
- unknown file families
- conflicting folder summaries
- API responses that disagree with local classifiers

## Worker model

Use small workers with one job each:

- `watcher`
- `classifier`
- `folder-summarizer`
- `api-runner`
- `indexer`
- `audit-exporter`

The central hub coordinates them with SQLite and a job queue.

## Resource gates

Local automation should respect machine load:

- pause heavy work above configured CPU threshold
- pause heavy work above configured memory threshold
- continue logging lightweight file events even under load
- drain queued jobs later when the system cools down

This gives you "always aware" without "always loud."

## Local vs central responsibilities

### Local agent

- watch folders
- compute file hashes
- compute MDA hash layers as needed
- extract text
- guess type
- write sidecars
- enqueue jobs
- perform small deterministic actions

### Central hub

- SQLite ledger
- job orchestration
- API enrichment
- conflict resolution
- cross-folder search
- network-wide audit exports

## Sidecar design

Use separate sidecars for files and folders.

### File sidecar

Suggested pattern:

`filename.ext.fmeta.md`

Suggested contents:

- file identity
- tags
- summary
- rename suggestion
- confidence
- parser trace
- verification notes

### Folder sidecar

Suggested pattern:

`_folder.meta.md`

Suggested contents:

- folder purpose
- dominant themes
- dominant file types
- suggested canonical name
- route destination
- review notes

## API policy

API calls are for ambiguity, enrichment, and comparison. They are not the first
line of defense.

Good API uses:

- unknown extensions
- semantic title cleanup
- folder naming suggestions
- summary generation
- conflict arbitration between local models
- external knowledge lookup for rare formats

Bad API uses:

- every file, every time
- work that a deterministic parser already solved
- destructive actions without review

## GUI role

The GUI is the operator cockpit.

It should make these tasks fast:

- approve rename suggestions
- inspect extracted text
- review tags
- search by extension, tag, folder, or confidence
- bulk move/copy/archive
- inspect failures
- retry jobs

## Excel role

Excel is the audit and reporting layer.

It should answer:

- what changed
- what got classified
- what failed
- what needed review
- how API vs local outputs compared

## First build order

1. Finalize SQLite schema
2. Finalize folder config contract
3. Run parser/import bake-off
4. Build event logger
5. Build review queue
6. Build GUI screens
7. Add API enrichment lane
8. Add Excel export views
