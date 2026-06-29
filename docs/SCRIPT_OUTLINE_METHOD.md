# Script Outline Method

## Goal

Another Codex should be able to outline scripts methodically instead of
free-styling helpers all over the filesystem.

The right way to outline each script is:

1. define its lane
2. define its inputs
3. define its outputs
4. define its safety checks
5. define its ledger effects
6. define its approval impact
7. define its failure behavior

## Lanes

Every script belongs to one lane:

- `watch`
- `event_log`
- `route`
- `file_classify`
- `folder_summarize`
- `rename`
- `tag`
- `verify`
- `api_enrich`
- `search_index`
- `export_import`
- `audit_retry`

Do not create scripts outside these lanes unless the need is explicit.

## Standard outline for every script

Every Python file should be outlined like this before implementation:

### 1. Purpose

What exactly is this script responsible for?

Example:

`rename_worker.py` generates and applies approved renames.

### 2. Trigger

What starts it?

Examples:

- watcher event
- API job
- GUI action
- scheduled scan
- retry queue

### 3. Inputs

What does it receive?

Examples:

- file path
- folder path
- job payload
- folder profile
- rules
- hashes
- extracted text

### 4. Outputs

What does it produce?

Examples:

- suggested filename
- moved file
- converted output
- review item
- duplicate group
- ledger row

### 5. Safety gates

What must it check before acting?

Examples:

- protected path?
- project root?
- low confidence?
- over threshold?
- delete-like operation?
- overwrite collision?

### 6. Ledger effects

What must be written to SQLite?

Examples:

- event row
- job row
- action row
- before/after hashes
- approval state
- rollback info

### 7. GUI impact

Does this create:

- nothing
- a passive status
- a review card
- an approval-required job

### 8. Failure behavior

If it fails, what happens?

Examples:

- retry
- mark terminal failure
- create review item
- leave source untouched
- write error log

## Standard Python parts by layer

### API layer

- route registration
- payload validation
- auth/permissions later
- call into job manager

### Core layer

- job manager
- dispatcher
- review gate
- resource gate
- preferences

### Worker layer

- execute one action family
- never silently skip ledger writes

### Adapter layer

- one adapter per outside tool/provider
- no business policy inside adapters

### Storage layer

- repository-style DB access
- schema/migrations
- no direct SQL scattered everywhere

## Naming convention

Prefer predictable names:

- `*_worker.py`
- `*_adapter.py`
- `*_repo.py`
- `routes_*.py`
- `*_rules.py`
- `*_profile.py`

This keeps the tree understandable for humans and agents.

## Build order

Scripts should be built in this order:

1. `storage/db.py`
2. `storage/job_repo.py`
3. `core/job_manager.py`
4. `watchers/event_normalizer.py`
5. `api/routes_jobs.py`
6. `rules/thresholds.py`
7. `core/review_gate.py`
8. `workers/hash_worker.py`
9. `workers/classify_worker.py`
10. `workers/rename_worker.py`
11. `workers/review_worker.py`
12. `gui/review_queue.py`

That gives a working control loop early.

## First working loop to target

The first end-to-end flow should be:

1. watcher sees file
2. watcher sends normalized event
3. job is created
4. hash/classify run
5. rename suggestion is generated
6. review gate decides whether approval is needed
7. GUI shows card
8. approved rename executes
9. ledger records before/after

## Do not do this

- do not place active Python scripts in every watched folder
- do not invent new job payload shapes for every feature
- do not let adapters decide policy
- do not let workers bypass review gate
- do not let destructive actions bypass ledger writes

## Desired result

Another Codex should be able to pick one lane, outline one script, and know
exactly where it belongs and how it interacts with the rest of the system.
