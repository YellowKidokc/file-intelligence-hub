# Hash Strategy

## Why one hash is not enough

A single file checksum only answers one question:

"Are these bytes identical?"

That is useful, but it is not enough for this system.

You also care about:

- same document exported in different formats
- same article wrapped in different HTML shells
- same content with small edits
- same folder structure after moves/renames
- large-file identity without reading every byte every time

So the hub should use a hash family, not a single hash.

## MDA hash

I am interpreting "MDA hash" here as:

`Multi-Dimensional Artifact hash`

That means every file can carry several identity surfaces.

## Recommended layers

### 1. Byte hash

- field: `sha256`
- purpose: exact identity
- best for: true duplicates, integrity checks, ledger certainty

### 2. Quick hash

- field: `quick_hash`
- purpose: cheap sampled identity for large files
- best for: fast scans, first-pass dedupe, watcher workloads

This already matches the direction in your existing `filetagger.py`.

### 3. Content hash

- field: `content_hash`
- purpose: normalized textual identity
- best for: same meaning across minor formatting changes

This matches the good idea already present in
`D:\DONT TOUCH BOOT UP\filetagger\salvaged\fingerprint.py`.

### 4. Structure hash

- field: `structure_hash`
- purpose: article/body/layout identity after shell stripping
- best for: HTML pages where wrappers change but the article remains the same

Examples:

- strip header/nav/footer
- normalize headings
- hash main content blocks

### 5. Semantic signature

- field: `semantic_signature_json`
- purpose: near-duplicate comparison
- best for: "same paper, revised wording"

First candidate:

- MinHash signature from shingles

Later candidate:

- embedding vectors stored elsewhere, with lightweight references in SQLite

## Match types

The system should distinguish these match classes:

- `exact_bytes`
- `same_quick_hash`
- `same_content`
- `same_structure`
- `near_duplicate_semantic`

That is why `similarity_edges` belongs in the ledger.

## Where to use each layer

### Watcher

Use:

- quick hash
- size
- modified time

### Local classifier

Use:

- content hash
- structure hash for HTML/Markdown-like sources

### Duplicate finder

Use:

- exact byte hash first
- content/structure hash second
- semantic signature third

### Review GUI

Show:

- why two files were considered related
- which hash layers matched
- confidence

## Practical policy

The system should not compute every expensive layer every time.

Suggested order:

1. size + modified time
2. quick hash
3. sha256 when needed
4. content hash when extractable
5. structure hash for structured documents
6. semantic signature for review-grade comparisons

That keeps the local agent light while still giving the hub real teeth.
