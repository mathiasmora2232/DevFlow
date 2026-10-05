from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingStatus(str, Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    FIXED = "fixed"
    VERIFIED = "verified"
    CLOSED = "closed"
    ACCEPTED_RISK = "accepted_risk"
    FALSE_POSITIVE = "false_positive"
    SUPPRESSED = "suppressed"


class PrincipalType(str, Enum):
    USER = "user"
    SERVICE_ACCOUNT = "service_account"


class ProjectOwnership(str, Enum):
    INTERNAL = "internal"
    EXTERNAL_CLIENT = "external_client"


class EngagementType(str, Enum):
    GREENFIELD = "greenfield"
    MIGRATION = "migration"
    REFACTOR = "refactor"
    MODERNIZATION = "modernization"
    MAINTENANCE = "maintenance"
    AUDIT_ONLY = "audit_only"


@dataclass(slots=True)
class Evidence:
    type: str
    source: str
    subject_type: str = ""
    subject_id: str = ""
    uri: str | None = None
    file: str | None = None
    line: int | None = None
    commit_sha: str | None = None
    timestamp: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    confidence: int = 100

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Finding:
    id: str
    fingerprint: str
    project_id: str
    category: str
    rule_id: str
    severity: str
    confidence: int
    status: str
    title: str
    description: str
    evidence: list[dict[str, Any]] = field(default_factory=list)
    repository_id: str | None = None
    location: dict[str, Any] | None = None
    recommendation: str | None = None
    first_seen_at: str | None = None
    last_seen_at: str | None = None
    resolved_at: str | None = None
    source: str = "devflow"
    regressed: bool = False
    waiver: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Principal:
    principal_type: str
    principal_id: str
    display_name: str | None = None
    project_role: str | None = None
    permissions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Project:
    id: str
    slug: str
    name: str
    stage: str
    criticality: str
    profile: str = "mvp"
    status: str = "active"
    repositories: list[str] = field(default_factory=list)
    environments: list[str] = field(default_factory=list)
    ownership: str = "internal"
    engagement: str = "greenfield"
    client_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Repository:
    id: str
    project_id: str
    provider: str
    owner: str
    name: str
    default_branch: str = "main"
    role: str = "other"
    remote_url: str | None = None
    local_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class WorkItem:
    id: str
    project_id: str
    title: str
    description: str = ""
    type: str = "task"
    priority: str = "medium"
    status: str = "backlog"
    owner: str | None = None
    acceptance_criteria: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    external_id: str | None = None
    source: str = "devflow"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Decision:
    id: str
    project_id: str
    title: str
    decision: str
    context: str | None = None
    consequences: str | None = None
    status: str = "accepted"
    created_by: str | None = None
    created_at: str | None = None
    supersedes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Risk:
    id: str
    project_id: str
    title: str
    description: str
    probability: str = "medium"
    impact: str = "medium"
    severity: str = "medium"
    status: str = "open"
    owner: str | None = None
    mitigation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Release:
    id: str
    project_id: str
    version: str
    commit_sha: str
    status: str = "prepared"
    changes: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    created_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Deployment:
    id: str
    release_id: str
    environment_id: str
    provider: str
    status: str
    verification_status: str = "unknown"
    started_at: str | None = None
    completed_at: str | None = None
    rollback_reference: str | None = None
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Environment:
    id: str
    project_id: str
    name: str
    kind: str
    criticality: str = "medium"
    provider_refs: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class StackComponent:
    category: str
    technology: str
    version: str | None = None
    source: str = "repository"
    evidence: list[str] = field(default_factory=list)
    confidence: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class TimeEntry:
    id: str
    project_id: str
    principal_id: str
    started_at: str
    ended_at: str
    duration_seconds: int
    work_item_id: str | None = None
    category: str = "development"
    description: str = ""
    billable: bool = True
    source: str = "devflow"
    corrected_from: str | None = None
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
