# Codex Online Handoff

## What this repo is

This repo is the sandbox and control-plane design space for a file-first
automation system.

The main idea is:

- folders are locations
- watchers are sensors
- the hub is the brain
- workers are the hands
- SQLite is the ledger
- the GUI is the human control layer

The system should not scatter active automation scripts into every folder.
Instead, it should centralize logic in the hub while keeping per-folder behavior
configurable.

## Core architecture settled so far

### Main hub

The main hub should own:

- rule evaluation
- confidence gating
- job creation and queueing
- worker dispatch
- approval and review gating
- AI arbitration
- folder profile interpretation
- learning/preferences
- ledger truth
- export/report generation

### Central nodes

Machines such as a Synology, desktop, or laptop can run node agents.

Nodes should do:

- local folder watching
- local event capture
- lightweight extraction
- local fallback queueing
- sync to hub when online

Nodes should not become independent truth authorities unless the primary hub is
down and a failover rule explicitly allows it.

### Folders

Folders are not little servers.

Folders may contain:

- files
- optional sidecars
- optional folder config
- optional folder marker files

Folders should not be required to contain:

- SQLite databases
- active watcher code
- mover scripts
- AI scripts

## Design philosophy

The system should:

- observe first
- log everything
- propose before acting
- require approval for risky/bulk actions
- learn from edits and rejections
- preserve originals during conversion
- never auto-delete by default

## Risk posture

Safe defaults:

- read-only first-run
- auto scan: yes
- auto tag: yes
- auto summarize: yes
- stage rename: yes
- stage move: yes
- stage archive: yes
- auto rename: no
- auto move: no
- auto archive: no
- auto delete: never

## Current workbook assets already created

1. `folder_symptom_registry_with_api_architecture.xlsx`
   - added `API Architecture` sheet
   - captures hub channels, node channels, worker/API lanes, review lanes,
     ledger/export/publish/rollback channels, and a version 1 build order

2. `pof_first_run_question_registry.xlsx`
   - first-run question registry
   - boundary-setting interview logic
   - policy outputs mapping
   - onboarding questions produce enforceable policy

## What Codex Online should understand

This is not just a file sorter. It is a file operations consultant system.

It needs to understand:

- user boundaries
- protected paths/categories
- canonical destinations
- intake hubs
- review-only zones
- project-root danger
- duplicate and version drift
- conversion safety
- publish boundaries

## Existing docs in this repo worth reading first

- `docs/ARCHITECTURE.md`
- `docs/AUTOMATION_SCHEMA.md`
- `docs/HASH_STRATEGY.md`
- `docs/SCHEMA_NOTES.md`
- `docs/STACK_RECOMMENDATION.md`
- `docs/RESEARCH_NOTES.md`
- `docs/SCRIPT_OUTLINE_METHOD.md`
- `docs/WORKBOOK_ASSETS.md`

## High-priority next work

1. Turn the agreed architecture into a literal v1 repo tree
2. Define exact Python entrypoints and build order
3. Define folder profiles and example configs
4. Define the intelligence system sheet and/or doc
5. Merge any additional GPT findings into the same map instead of branching
6. Build the first working path:
   - watcher event
   - job creation
   - review queue
   - rename suggestion
   - rename apply
   - ledger write

## Non-goals for now

- no wild per-folder automation engines
- no SQLite in every folder
- no auto-delete default
- no letting API calls directly mutate files without hub interpretation

## One-line mental model

Every automation action becomes a job.
Every risky job becomes a review card.
Every approval or correction teaches the system.
