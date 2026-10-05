from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from . import __version__
from .findings import waiver_active
from .utils import now_iso


PROFILES: dict[str, dict[str, dict[str, Any]]] = {
    "prototype": {
        "pull_request": {"critical_security": 0},
        "production": {"critical_security": 0},
    },
    "mvp": {
        "pull_request": {"minimum_health": 60, "critical_security": 0},
        "production": {"minimum_health": 70, "critical_security": 0, "tests_required": True},
    },
    "production": {
        "pull_request": {"minimum_health": 70, "critical_security": 0, "tests_required": True},
        "staging": {"tests_required": True, "build_required": True},
        "production": {
            "minimum_health": 80,
            "critical_security": 0,
            "high_security": 0,
            "tests_required": True,
            "build_required": True,
            "rollback_required": True,
            "healthcheck_required": True,
            "verified_ci_required": True,
        },
        "release": {"tests_required": True, "build_required": True},
    },
    "enterprise": {
        "pull_request": {"minimum_health": 80, "critical_security": 0, "high_security": 0, "tests_required": True},
        "production": {
            "minimum_health": 85,
            "critical_security": 0,
            "high_security": 0,
            "tests_required": True,
            "build_required": True,
            "rollback_required": True,
            "healthcheck_required": True,
            "verified_ci_required": True,
        },
    },
    "legacy-modernization": {
        "pull_request": {"minimum_health": 55, "critical_security": 0},
        "production": {"critical_security": 0, "tests_required": True},
    },
    "external-audit": {},
    "high-security": {
        "pull_request": {"critical_security": 0, "high_security": 0, "tests_required": True},
        "production": {"minimum_health": 85, "critical_security": 0, "high_security": 0, "verified_ci_required": True},
    },
    "high-traffic": {
        "production": {"minimum_health": 80, "critical_security": 0, "tests_required": True, "healthcheck_required": True},
    },
}


@dataclass(slots=True)
class GateCheck:
    name: str
    result: str
    expected: Any = None
    actual: Any = None
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class GateResult:
    gate: str
    result: str
    schema: str = "devflow.gate-result"
    schema_version: int = 1
    devflow_version: str = __version__
    checks: list[dict[str, Any]] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def gate_policy(config: dict[str, Any], gate: str) -> dict[str, Any]:
    profile = config.get("profile") or config.get("project", {}).get("stage") or "mvp"
    base = dict(PROFILES.get(profile, PROFILES["mvp"]).get(gate, {}))
    base.update(config.get("gates", {}).get(gate, {}))
    return base


def evaluate_gate(gate: str, config: dict[str, Any], audit: dict[str, Any] | None, evidence: dict[str, bool] | None = None) -> GateResult:
    policy = gate_policy(config, gate)
    evidence = evidence or {}
    checks: list[GateCheck] = []
    missing: list[str] = []

    if "minimum_health" in policy:
        health = audit.get("project_health_score") if audit else None
        if health is None:
            checks.append(GateCheck("minimum_health", "unknown", policy["minimum_health"], None, "health evidence unavailable"))
            missing.append("project_health")
        else:
            checks.append(GateCheck("minimum_health", "pass" if health >= policy["minimum_health"] else "blocked", policy["minimum_health"], health))

    findings = audit.get("findings", []) if audit else []
    for severity_key, severity in (("critical_security", "critical"), ("high_security", "high")):
        if severity_key in policy:
            count = sum(
                1
                for f in findings
                if f.get("category") == "security"
                and f.get("severity") == severity
                and f.get("status", "open") not in {"fixed", "verified", "closed", "false_positive", "suppressed"}
                and not waiver_active(f)
            )
            checks.append(GateCheck(severity_key, "pass" if count <= int(policy[severity_key]) else "blocked", policy[severity_key], count))

    evidence_map = {
        "tests_required": "tests",
        "build_required": "build",
        "rollback_required": "rollback",
        "healthcheck_required": "healthcheck",
        "verified_ci_required": "verified_ci",
    }
    for rule, key in evidence_map.items():
        if policy.get(rule):
            value = evidence.get(key)
            if value is None:
                checks.append(GateCheck(rule, "unknown", True, None, f"missing evidence: {key}"))
                missing.append(key)
            else:
                checks.append(GateCheck(rule, "pass" if value else "blocked", True, value))

    states = [c.result for c in checks]
    if "blocked" in states:
        result = "blocked"
    elif "unknown" in states:
        result = "unknown"
    elif not checks:
        result = "warn"
    else:
        result = "pass"

    return GateResult(gate, result, [c.to_dict() for c in checks], [], missing)
