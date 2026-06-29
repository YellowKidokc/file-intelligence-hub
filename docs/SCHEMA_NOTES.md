# Schema Notes

These are the first entities we expect to support:

## File record

- path
- filename
- extension
- size
- sha256
- quick_hash
- content_hash
- structure_hash
- semantic_signature
- mime_guess
- parser_used
- text_preview
- title_guess
- tags
- rename_suggestion
- confidence
- needs_review

## Folder record

- folder_path
- folder_name
- file_count
- dominant_types
- dominant_tags
- summary
- rename_suggestion
- route_suggestion
- confidence

## Action record

- action_type
- source_path
- target_path
- status
- approved_by
- executed_at

## API job

- job_id
- item_type
- item_id
- purpose
- status
- attempts
- payload_hash
- created_at
- heartbeat_at
- finished_at

## Hash family

One file should not have just one hash if we care about duplicates, versions,
and semantic sameness.

Recommended hash layers:

- `sha256` - exact byte identity
- `quick_hash` - fast sampled identity for large files
- `content_hash` - normalized text identity
- `structure_hash` - stripped-layout / article-structure identity
- `semantic_signature` - MinHash or embedding-based near-duplicate signature

This is the practical version of an MDA hash: a multi-dimensional artifact hash.
