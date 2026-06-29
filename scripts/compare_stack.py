from __future__ import annotations

import importlib
import json
import platform
from pathlib import Path


PACKAGES = [
    ("docling", "docling"),
    ("tika", "tika"),
    ("fastembed", "fastembed"),
    ("openai", "openai"),
    ("watchdog", "watchdog"),
    ("psutil", "psutil"),
    ("aiosqlite", "aiosqlite"),
    ("fitz", "PyMuPDF"),
    ("bs4", "beautifulsoup4"),
    ("lxml", "lxml"),
    ("filetype", "filetype"),
    ("openpyxl", "openpyxl"),
    ("pandas", "pandas"),
    ("docx", "python-docx"),
]


def detect_package(module_name: str, label: str) -> dict:
    try:
        mod = importlib.import_module(module_name)
        version = getattr(mod, "__version__", None) or getattr(mod, "version", None) or "unknown"
        return {"package": label, "module": module_name, "installed": True, "version": str(version)}
    except Exception as exc:
        return {"package": label, "module": module_name, "installed": False, "error": str(exc)}


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    rows = [detect_package(module, label) for module, label in PACKAGES]
    summary = {
        "repo": str(repo),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": rows,
    }
    out_dir = repo / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "stack_compare.json"
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"\nWrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
