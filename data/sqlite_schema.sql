PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS watched_roots (
    id INTEGER PRIMARY KEY,
    root_path TEXT NOT NULL UNIQUE,
    label TEXT,
    enabled INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS folders (
    id INTEGER PRIMARY KEY,
    root_id INTEGER,
    folder_path TEXT NOT NULL UNIQUE,
    folder_name TEXT NOT NULL,
    parent_path TEXT,
    canonical_name TEXT,
    file_count INTEGER,
    dominant_types_json TEXT,
    dominant_tags_json TEXT,
    summary_text TEXT,
    route_suggestion TEXT,
    confidence REAL,
    needs_review INTEGER NOT NULL DEFAULT 0,
    last_seen_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (root_id) REFERENCES watched_roots(id)
);

CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    root_id INTEGER,
    folder_id INTEGER,
    file_path TEXT NOT NULL UNIQUE,
    file_name TEXT NOT NULL,
    extension TEXT,
    mime_guess TEXT,
    size_bytes INTEGER,
    sha256 TEXT,
    quick_hash TEXT,
    content_hash TEXT,
    structure_hash TEXT,
    semantic_signature_json TEXT,
    modified_at TEXT,
    discovered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    parser_used TEXT,
    parser_version TEXT,
    title_guess TEXT,
    text_preview TEXT,
    summary_text TEXT,
    tags_json TEXT,
    rename_suggestion TEXT,
    route_suggestion TEXT,
    confidence REAL,
    needs_review INTEGER NOT NULL DEFAULT 0,
    deleted_flag INTEGER NOT NULL DEFAULT 0,
    archived_flag INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (root_id) REFERENCES watched_roots(id),
    FOREIGN KEY (folder_id) REFERENCES folders(id)
);

CREATE INDEX IF NOT EXISTS idx_files_folder_id ON files(folder_id);
CREATE INDEX IF NOT EXISTS idx_files_extension ON files(extension);
CREATE INDEX IF NOT EXISTS idx_files_sha256 ON files(sha256);
CREATE INDEX IF NOT EXISTS idx_files_quick_hash ON files(quick_hash);
CREATE INDEX IF NOT EXISTS idx_files_content_hash ON files(content_hash);
CREATE INDEX IF NOT EXISTS idx_files_structure_hash ON files(structure_hash);
CREATE INDEX IF NOT EXISTS idx_files_needs_review ON files(needs_review);

CREATE TABLE IF NOT EXISTS file_versions (
    id INTEGER PRIMARY KEY,
    file_id INTEGER NOT NULL,
    sha256 TEXT,
    quick_hash TEXT,
    content_hash TEXT,
    structure_hash TEXT,
    semantic_signature_json TEXT,
    size_bytes INTEGER,
    modified_at TEXT,
    parser_used TEXT,
    text_preview TEXT,
    summary_text TEXT,
    tags_json TEXT,
    confidence REAL,
    captured_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(id)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    root_id INTEGER,
    file_id INTEGER,
    folder_id INTEGER,
    event_type TEXT NOT NULL,
    source_path TEXT,
    target_path TEXT,
    payload_json TEXT,
    status TEXT NOT NULL DEFAULT 'queued',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TEXT,
    FOREIGN KEY (root_id) REFERENCES watched_roots(id),
    FOREIGN KEY (file_id) REFERENCES files(id),
    FOREIGN KEY (folder_id) REFERENCES folders(id)
);

CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at);

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    lane TEXT NOT NULL,
    item_type TEXT NOT NULL,
    item_id INTEGER,
    event_id INTEGER,
    purpose TEXT,
    status TEXT NOT NULL DEFAULT 'queued',
    priority INTEGER NOT NULL DEFAULT 50,
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 3,
    worker_name TEXT,
    claim_token TEXT,
    payload_json TEXT,
    error_text TEXT,
    queued_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    claimed_at TEXT,
    heartbeat_at TEXT,
    finished_at TEXT,
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE INDEX IF NOT EXISTS idx_jobs_status_lane ON jobs(status, lane);
CREATE INDEX IF NOT EXISTS idx_jobs_priority ON jobs(priority);

CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY,
    file_id INTEGER,
    folder_id INTEGER,
    action_type TEXT NOT NULL,
    source_path TEXT,
    target_path TEXT,
    initiated_by TEXT,
    approval_mode TEXT,
    approved_by TEXT,
    status TEXT NOT NULL DEFAULT 'queued',
    details_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    executed_at TEXT,
    FOREIGN KEY (file_id) REFERENCES files(id),
    FOREIGN KEY (folder_id) REFERENCES folders(id)
);

CREATE TABLE IF NOT EXISTS api_runs (
    id INTEGER PRIMARY KEY,
    job_id INTEGER,
    provider TEXT NOT NULL,
    model TEXT,
    purpose TEXT,
    request_hash TEXT,
    input_ref TEXT,
    output_ref TEXT,
    output_json TEXT,
    cost_estimate_usd REAL,
    status TEXT NOT NULL DEFAULT 'queued',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

CREATE TABLE IF NOT EXISTS review_queue (
    id INTEGER PRIMARY KEY,
    item_type TEXT NOT NULL,
    item_id INTEGER NOT NULL,
    review_reason TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'medium',
    status TEXT NOT NULL DEFAULT 'open',
    assigned_to TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_review_queue_status ON review_queue(status);

CREATE TABLE IF NOT EXISTS similarity_edges (
    id INTEGER PRIMARY KEY,
    left_file_id INTEGER NOT NULL,
    right_file_id INTEGER NOT NULL,
    match_type TEXT NOT NULL,
    score REAL NOT NULL,
    evidence_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (left_file_id) REFERENCES files(id),
    FOREIGN KEY (right_file_id) REFERENCES files(id)
);

CREATE INDEX IF NOT EXISTS idx_similarity_left ON similarity_edges(left_file_id);
CREATE INDEX IF NOT EXISTS idx_similarity_right ON similarity_edges(right_file_id);
CREATE INDEX IF NOT EXISTS idx_similarity_type ON similarity_edges(match_type);

CREATE VIRTUAL TABLE IF NOT EXISTS file_search USING fts5(
    file_path,
    title_guess,
    summary_text,
    text_preview,
    tags_text
);
