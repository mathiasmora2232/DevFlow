from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from . import __version__
from .utils import now_iso


class SyncStatus(str, Enum):
    CLEAN = "clean"
    CHANGED = "changed"
    CONFLICT = "conflict"
    PARTIAL = "partial"
    FAILED = "failed"


AUTHORITY = {
    "source_code": "git",
    "git_state": "git",
    "work_item": "stellarcode",
    "members": "stellarcode",
    "roles": "stellarcode",
    "audit_reports": "devflow",
    "findings": "devflow",
    "runtime_health": "runtime",
    "deploy_state": "deployment",
    "config": "devflow",
}


@dataclass(slots=True)
class SyncConflict:
    field: str
    local_value: Any
    remote_value: Any
    authority: str
    recommended_resolution: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SyncResult:
    status: str
    schema: str = "devflow.sync-result"
    schema_version: int = 1
    devflow_version: str = __version__
    changes: list[dict[str, Any]] = field(default_factory=list)
    conflicts: list[dict[str, Any]] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    source_versions: dict[str, str] = field(default_factory=dict)
    timestamp: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def authority_for(domain: str) -> str:
    return AUTHORITY.get(domain, "manual")


def detect_conflict(field: str, local_value: Any, remote_value: Any, authority: str) -> SyncConflict | None:
    if local_value == remote_value:
        return None
    resolution = f"use_{authority}" if authority in {"git", "stellarcode", "runtime", "deployment", "devflow"} else "manual_review"
    return SyncConflict(field, local_value, remote_value, authority, resolution)


class IdempotencyStore:
    def __init__(self, root: Path):
        self.path = root / "ops" / "idempotency.json"

    def _load(self) -> dict[str, dict[str, Any]]:
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("entries"), dict):
                return data["entries"]
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError) as exc:
            raise ValueError(f"Unable to read idempotency store {self.path}: {exc}") from exc

    def seen(self, key: str) -> bool:
        return key in self._load()

    def register(self, key: str, metadata: dict[str, Any] | None = None) -> bool:
        data = self._load()
        if key in data:
            return False
        data[key] = {"registered_at": now_iso(), "metadata": metadata or {}}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema": "devflow.idempotency",
            "schema_version": 1,
            "devflow_version": __version__,
            "entries": data,
        }
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self.path)
        return True


@dataclass(slots=True)
class Event:
    event_id: str
    provider: str
    event_type: str
    project_id: str
    resource_type: str
    resource_id: str
    occurred_at: str
    received_at: str = field(default_factory=now_iso)
    payload_hash: str = ""
    evidence: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_payload(
        cls,
        *,
        event_id: str,
        provider: str,
        event_type: str,
        project_id: str,
        resource_type: str,
        resource_id: str,
        occurred_at: str,
        payload: Any,
    ) -> "Event":
        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
        return cls(
            event_id=event_id,
            provider=provider,
            event_type=event_type,
            project_id=project_id,
            resource_type=resource_type,
            resource_id=resource_id,
            occurred_at=occurred_at,
            payload_hash=hashlib.sha256(raw).hexdigest(),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
