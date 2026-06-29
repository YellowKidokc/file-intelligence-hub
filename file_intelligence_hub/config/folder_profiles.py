"""Centralized folder profile loading and matching.

Folder-specific behavior belongs here, not in scripts scattered through watched folders.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_PROFILE_PATH = Path("config/folder_profiles.json")


@dataclass(frozen=True)
class FolderProfile:
    path: str = "*"
    folder_role: str = "general"
    watch_enabled: bool = True
    review_only: bool = True
    protected: bool = False
    parser_preferences: list[str] = field(default_factory=list)
    routing_hints: dict[str, Any] = field(default_factory=dict)
    thresholds: dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any], defaults: "FolderProfile | None" = None) -> "FolderProfile":
        base = defaults or cls()
        return cls(
            path=str(data.get("path", base.path)),
            folder_role=str(data.get("folder_role", base.folder_role)),
            watch_enabled=bool(data.get("watch_enabled", base.watch_enabled)),
            review_only=bool(data.get("review_only", base.review_only)),
            protected=bool(data.get("protected", base.protected)),
            parser_preferences=list(data.get("parser_preferences", base.parser_preferences)),
            routing_hints=dict(data.get("routing_hints", base.routing_hints)),
            thresholds=dict(data.get("thresholds", base.thresholds)),
        )

    def to_payload(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "folder_role": self.folder_role,
            "watch_enabled": self.watch_enabled,
            "review_only": self.review_only,
            "protected": self.protected,
            "parser_preferences": self.parser_preferences,
            "routing_hints": self.routing_hints,
            "thresholds": self.thresholds,
        }


class FolderProfileRegistry:
    def __init__(self, default: FolderProfile | None = None, profiles: list[FolderProfile] | None = None) -> None:
        self.default = default or FolderProfile()
        self.profiles = profiles or []

    @classmethod
    def load(cls, path: str | Path = DEFAULT_PROFILE_PATH) -> "FolderProfileRegistry":
        config_path = Path(path)
        if not config_path.exists():
            return cls()
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        default = FolderProfile.from_dict(raw.get("defaults", {}))
        profiles = [FolderProfile.from_dict(item, default) for item in raw.get("profiles", [])]
        return cls(default, profiles)

    def enabled_roots(self) -> list[Path]:
        return [Path(profile.path) for profile in self.profiles if profile.watch_enabled and profile.path != "*"]

    def match(self, file_path: str | Path) -> FolderProfile:
        candidate = Path(file_path).resolve()
        best: tuple[int, FolderProfile] | None = None
        for profile in self.profiles:
            root = Path(profile.path).expanduser().resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                continue
            score = len(root.parts)
            if best is None or score > best[0]:
                best = (score, profile)
        return best[1] if best else self.default
