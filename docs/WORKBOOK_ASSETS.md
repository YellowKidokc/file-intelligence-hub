# Workbook Assets

## Purpose

These workbook assets are part of the design surface for the hub. They should be
treated as first-class architecture artifacts, not loose attachments.

## Files

### 1. Folder symptom registry with API architecture

Path:

`C:\Users\David\Documents\Codex\2026-06-29\he\outputs\api-architecture\folder_symptom_registry_with_api_architecture.xlsx`

What it contains:

- original symptom registry
- detection functions
- severity scale
- added `API Architecture` sheet

The `API Architecture` sheet includes:

- hub intake channels
- watcher event channels
- review queue channels
- rename/routing/archive channels
- convert/combine channels
- duplicate channels
- folder health channels
- rules and boundaries channels
- worker and node heartbeat/sync channels
- AI/Llama and external API channels
- ledger/search/export/publish/rollback/learning/resource channels
- version 1 build order

### 2. First-run question registry

Path:

`\\192.168.2.50\h_hp\Desktop\pof_first_run_question_registry.xlsx`

What it contains:

- onboarding questions
- policy outputs
- severity scale
- source notes

Its job is to turn first-run questions into enforceable policy.

## Why these matter

The symptom registry answers:

- what is wrong with this folder?
- what can detect it?
- what is the risk?

The first-run registry answers:

- what kind of system is this?
- what is protected?
- what can be automated?
- what requires approval?

Together they form:

- folder health intelligence
- onboarding/boundary intelligence

## Expected next workbook sheets

Likely next additions:

- `Folder Structure`
- `Intelligence System`
- `Workers + Python Files`
- `Folder Profiles`
- `Approval Threshold Matrix`

## Repo note

If these workbook files get copied into the repo later, keep the docs here as
the human-readable map so agents do not need to rediscover their purpose.
