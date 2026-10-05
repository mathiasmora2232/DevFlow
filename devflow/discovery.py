from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from . import __version__
from .audit import audit_project
from .config import load_config
from .detector import detect_stack
from .secrets_scan import scan_secrets
from .utils import git_info, iter_project_files, now_iso, read_text, relative

ENV_PATTERNS = (
    re.compile(r"\bprocess\.env\.([A-Z][A-Z0-9_]{2,})\b"),
    re.compile(r"\bimport\.meta\.env\.([A-Z][A-Z0-9_]{2,})\b"),
    re.compile(r"\bos\.getenv\(\s*['\"]([A-Z][A-Z0-9_]{2,})['\"]"),
    re.compile(r"\bos\.environ\[\s*['\"]([A-Z][A-Z0-9_]{2,})['\"]\s*\]"),
    re.compile(r"\bgetenv\(\s*['\"]([A-Z][A-Z0-9_]{2,})['\"]"),
)
SECRET_NAME = re.compile(r"(SECRET|TOKEN|PASSWORD|PASSWD|PRIVATE|CREDENTIAL|API_KEY|ACCESS_KEY|DATABASE_URL|DSN)", re.I)


def infer_engagement(root: Path, detected: dict[str, Any]) -> str:
    has_stack = any([
        detected.get("backend") not in {None, "none"},
        detected.get("frontend") not in {None, "none"},
        detected.get("database") not in {None, "none"},
        bool(detected.get("infra")),
    ])
    has_runtime_files = any(True for _ in iter_project_files(root, max_file_bytes=100_000))
    return "refactor" if has_stack or has_runtime_files else "greenfield"


def config_metadata(root: Path) -> list[dict[str, Any]]:
    found: dict[tuple[str, str], dict[str, Any]] = {}

    def add(name: str, source: str, configured: bool | None, environment: str = "unknown") -> None:
        key = (name, environment)
        item = found.setdefault(key, {
            "name": name,
            "environment": environment,
            "required": None,
            "secret": bool(SECRET_NAME.search(name)),
            "configured": configured,
            "sources": [],
        })
        if source not in item["sources"]:
            item["sources"].append(source)
        if configured is True:
            item["configured"] = True

    for path in iter_project_files(root, max_file_bytes=1_000_000):
        rel = relative(path, root)
        text = read_text(path, 1_000_000)
        lower_name = path.name.lower()

        if lower_name.startswith(".env"):
            is_example = any(token in lower_name for token in ("example", "sample", "template"))
            env_name = "unknown"
            parts = lower_name.split(".")
            if len(parts) >= 3 and parts[-1] not in {"example", "sample", "template"}:
                env_name = parts[-1]
            for line in text.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                name = stripped.split("=", 1)[0].strip()
                if re.fullmatch(r"[A-Z][A-Z0-9_]{2,}", name):
                    add(name, rel, False if is_example else True, env_name)

        for pattern in ENV_PATTERNS:
            for match in pattern.finditer(text):
                add(match.group(1), rel, None)

    return sorted(found.values(), key=lambda x: (x["environment"], x["name"]))


def stack_inventory(detected: dict[str, Any]) -> list[dict[str, Any]]:
    evidence = detected.get("evidence", {}) or {}
    items: list[dict[str, Any]] = []

    def add(category: str, technology: str | None, evidence_key: str) -> None:
        if not technology or technology == "none":
            return
        ev = list(evidence.get(evidence_key, []) or [])
        items.append({
            "category": category,
            "technology": technology,
            "version": None,
            "source": "repository",
            "evidence": ev,
            "confidence": 90 if ev else 60,
        })

    add("backend", detected.get("backend"), "backend")
    add("frontend", detected.get("frontend"), "frontend")
    add("database", detected.get("database"), "database")
    for technology in detected.get("infra", []) or []:
        items.append({
            "category": "infrastructure",
            "technology": technology,
            "version": None,
            "source": "repository",
            "evidence": list(evidence.get("infra", []) or []),
            "confidence": 85,
        })
    for technology in detected.get("observability", []) or []:
        items.append({
            "category": "observability",
            "technology": technology,
            "version": None,
            "source": "repository",
            "evidence": list(evidence.get("observability", []) or []),
            "confidence": 85,
        })
    return items


def infrastructure_inventory(detected: dict[str, Any]) -> list[dict[str, Any]]:
    resources = []
    evidence = detected.get("evidence", {}) or {}
    for technology in detected.get("infra", []) or []:
        resources.append({
            "provider": technology if technology == "cloudflare" else "unknown",
            "type": technology,
            "environment": "unknown",
            "state": "detected",
            "health": "unknown",
            "source": "repository",
            "evidence": list(evidence.get("infra", []) or []),
        })
    database = detected.get("database")
    if database and database != "none":
        resources.append({
            "provider": "unknown",
            "type": "database",
            "technology": database,
            "environment": "unknown",
            "state": "detected",
            "health": "unknown",
            "source": "repository",
            "evidence": list(evidence.get("database", []) or []),
        })
    return resources


def discover_project(root: Path, *, run_audit: bool = True) -> dict[str, Any]:
    config = load_config(root)
    detected = detect_stack(root)
    git = git_info(root)
    project = config.get("project", {}) if config else {}
    ownership = project.get("ownership") or "internal"
    engagement = project.get("engagement") or infer_engagement(root, detected)

    audit = audit_project(root, config) if run_audit and config else None
    secrets = scan_secrets(root)

    snapshot = {
        "schema": "devflow.discovery",
        "schema_version": 1,
        "devflow_version": __version__,
        "generated_at": now_iso(),
        "project": {
            "name": project.get("name") or root.name,
            "slug": project.get("slug") or root.name,
            "ownership": ownership,
            "engagement": engagement,
            "client_id": project.get("client_id"),
            "stage": project.get("stage"),
            "type": project.get("type") or detected.get("project_type"),
        },
        "repository": {
            "root": str(root),
            "branch": git.get("branch"),
            "revision": git.get("revision"),
            "dirty": git.get("dirty"),
        },
        "detected_stack": detected,
        "stack_components": stack_inventory(detected),
        "config_metadata": config_metadata(root),
        "infrastructure": infrastructure_inventory(detected),
        "secret_hygiene": {
            "score": secrets.get("secret_hygiene_score"),
            "counts": secrets.get("counts", {}),
            "findings": [
                {
                    "id": f.get("id"),
                    "severity": f.get("severity"),
                    "file": f.get("file"),
                    "line": f.get("line"),
                    "preview": f.get("preview"),
                }
                for f in secrets.get("findings", [])
            ],
        },
        "audit_summary": None if audit is None else {
            "project_health_score": audit.get("project_health_score"),
            "stack_fit_score": audit.get("stack_fit_score"),
            "evidence_confidence": audit.get("evidence_confidence"),
            "finding_count": len(audit.get("findings", [])),
            "unknowns": audit.get("unknowns", []),
        },
        "audit": audit,
        "missing_evidence": [],
    }

    if not snapshot["infrastructure"]:
        snapshot["missing_evidence"].append("hosting/infrastructure provider")
    if not project.get("ownership"):
        snapshot["missing_evidence"].append("project ownership confirmation")
    if engagement in {"migration", "refactor", "modernization"}:
        snapshot["missing_evidence"].append("target state / desired outcome")
    return snapshot


def write_discovery(root: Path, snapshot: dict[str, Any]) -> tuple[Path, Path]:
    out = root / "ops" / "discovery"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "latest.json"
    md_path = out / "latest.md"
    json_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(discovery_markdown(snapshot), encoding="utf-8")
    return json_path, md_path


def discovery_markdown(snapshot: dict[str, Any]) -> str:
    p = snapshot["project"]
    repo = snapshot["repository"]
    audit = snapshot.get("audit_summary") or {}
    lines = [
        "# DevFlow Discovery Snapshot", "",
        f"- Project: **{p.get('name')}**",
        f"- Ownership: **{p.get('ownership')}**",
        f"- Engagement: **{p.get('engagement')}**",
        f"- Revision: **{repo.get('revision')}**",
        f"- Generated: {snapshot.get('generated_at')}", "",
        "## Stack", "",
    ]
    if snapshot["stack_components"]:
        for item in snapshot["stack_components"]:
            lines.append(f"- {item['category']}: **{item['technology']}** (confidence {item['confidence']}%)")
    else:
        lines.append("- No runtime stack detected.")

    lines += ["", "## Configuration metadata", ""]
    if snapshot["config_metadata"]:
        for item in snapshot["config_metadata"]:
            state = "configured" if item["configured"] is True else "template" if item["configured"] is False else "referenced"
            lines.append(f"- `{item['name']}` — {state}; secret={str(item['secret']).lower()}")
    else:
        lines.append("- No environment-variable metadata detected.")

    lines += ["", "## Audit baseline", ""]
    if audit:
        lines += [
            f"- Technical Health: **{audit.get('project_health_score')}**",
            f"- Stack Fit: **{audit.get('stack_fit_score')}**",
            f"- Evidence Confidence: **{audit.get('evidence_confidence')}**",
            f"- Findings: **{audit.get('finding_count')}**",
        ]
    else:
        lines.append("- Audit not executed.")

    lines += ["", "## Missing evidence", ""]
    if snapshot["missing_evidence"]:
        lines += [f"- {item}" for item in snapshot["missing_evidence"]]
    else:
        lines.append("- None")
    lines += ["", "> Secret values are never included in discovery output.", ""]
    return "\n".join(lines)
