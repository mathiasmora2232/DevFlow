from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .domain import Finding, FindingStatus
from .utils import now_iso, slugify


ACTIVE_STATUSES = {
    FindingStatus.OPEN.value,
    FindingStatus.ACKNOWLEDGED.value,
    FindingStatus.PLANNED.value,
    FindingStatus.IN_PROGRESS.value,
    FindingStatus.FIXED.value,
    FindingStatus.ACCEPTED_RISK.value,
    FindingStatus.SUPPRESSED.value,
}


def _normalize_rule_text(message: str) -> str:
    text = message.lower().strip()
    text = re.sub(r"\b\d+\b", "{n}", text)
    text = re.sub(r"[^a-z0-9áéíóúñ{}]+", "-", text)
    return text.strip("-")[:80] or "finding"


def _evidence_key(raw: Any) -> str:
    if isinstance(raw, str):
        value = raw.replace("\\", "/").strip()
        return re.sub(r":\d+$", "", value)
    if isinstance(raw, dict):
        file = str(raw.get("file") or raw.get("path") or "")
        symbol = str(raw.get("symbol") or raw.get("key") or "")
        return f"{file}|{symbol}".strip("|")
    return ""


def stable_fingerprint(
    analyzer_id: str,
    rule_id: str,
    repository_identity: str,
    location_key: str = "",
    evidence_key: str = "",
) -> str:
    raw = "|".join([
        analyzer_id.strip().lower(),
        rule_id.strip().lower(),
        repository_identity.strip().lower(),
        location_key.strip().lower(),
        evidence_key.strip().lower(),
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def display_id(rule_id: str, fingerprint: str) -> str:
    rule = slugify(rule_id).upper().replace("-", "_")[:24]
    return f"FND-{rule}-{fingerprint[:8].upper()}"


def normalize_legacy_finding(raw: dict[str, Any], project_slug: str, repository_identity: str = "default") -> dict[str, Any]:
    message = str(raw.get("message") or raw.get("title") or "Finding").strip()
    category = str(raw.get("category") or "general")
    severity = str(raw.get("severity") or "info").lower()
    rule_id = str(raw.get("rule_id") or f"{category}.{_normalize_rule_text(message)}")
    evidence_value = raw.get("evidence")
    ev_key = _evidence_key(evidence_value)
    location = raw.get("location")
    if not location and isinstance(evidence_value, str) and "/" in evidence_value and len(evidence_value) < 260:
        location = {"file": evidence_value.replace("\\", "/")}
    location_key = ""
    if isinstance(location, dict):
        location_key = "|".join(str(location.get(k) or "") for k in ("file", "symbol"))
    fp = stable_fingerprint("static-core", rule_id, repository_identity, location_key, ev_key)
    now = now_iso()
    evidence = raw.get("evidence_items")
    if not isinstance(evidence, list):
        evidence = [{"type": "static", "source": "devflow", "value": evidence_value}] if evidence_value else []
    finding = Finding(
        id=display_id(rule_id, fp),
        fingerprint=fp,
        project_id=project_slug,
        repository_id=repository_identity,
        category=category,
        rule_id=rule_id,
        severity=severity,
        confidence=int(raw.get("confidence", 70)),
        status=str(raw.get("status") or FindingStatus.OPEN.value),
        title=str(raw.get("title") or message),
        description=message,
        evidence=evidence,
        location=location,
        recommendation=raw.get("recommendation"),
        first_seen_at=raw.get("first_seen_at") or now,
        last_seen_at=now,
        resolved_at=raw.get("resolved_at"),
        source=str(raw.get("source") or "devflow.static-core"),
        regressed=bool(raw.get("regressed", False)),
        waiver=raw.get("waiver"),
    )
    return finding.to_dict()


def findings_store_path(root: Path) -> Path:
    return root / "ops" / "findings.json"


def load_findings(root: Path) -> list[dict[str, Any]]:
    path = findings_store_path(root)
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if isinstance(payload, dict):
        return list(payload.get("findings", []))
    return payload if isinstance(payload, list) else []


def save_findings(root: Path, findings: list[dict[str, Any]]) -> Path:
    path = findings_store_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "devflow.findings",
        "schema_version": 1,
        "generated_at": now_iso(),
        "findings": findings,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def reconcile_findings(
    previous: list[dict[str, Any]],
    current: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    now = now_iso()
    old_by_fp = {f.get("fingerprint"): dict(f) for f in previous if f.get("fingerprint")}
    seen: set[str] = set()
    merged: list[dict[str, Any]] = []
    stats = {"new": 0, "persistent": 0, "fixed": 0, "regressed": 0}

    for new in current:
        fp = new["fingerprint"]
        seen.add(fp)
        old = old_by_fp.get(fp)
        if not old:
            stats["new"] += 1
            merged.append(new)
            continue

        item = {**old, **new}
        item["first_seen_at"] = old.get("first_seen_at") or new.get("first_seen_at")
        previous_status = old.get("status", FindingStatus.OPEN.value)
        if previous_status in {FindingStatus.CLOSED.value, FindingStatus.VERIFIED.value}:
            item["status"] = FindingStatus.OPEN.value
            item["resolved_at"] = None
            item["regressed"] = True
            stats["regressed"] += 1
        else:
            item["status"] = previous_status
            item["regressed"] = bool(old.get("regressed", False))
            stats["persistent"] += 1
        item["last_seen_at"] = now
        merged.append(item)

    for fp, old in old_by_fp.items():
        if fp in seen:
            continue
        item = dict(old)
        if item.get("status") in ACTIVE_STATUSES and item.get("status") not in {
            FindingStatus.ACCEPTED_RISK.value,
            FindingStatus.SUPPRESSED.value,
        }:
            item["status"] = FindingStatus.FIXED.value
            item["resolved_at"] = now
            stats["fixed"] += 1
        merged.append(item)

    merged.sort(key=lambda f: (f.get("severity", "info"), f.get("category", ""), f.get("id", "")))
    return merged, stats


def update_finding_status(
    root: Path,
    finding_id: str,
    status: str,
    reason: str | None = None,
    approved_by: str | None = None,
    expires_at: str | None = None,
) -> dict[str, Any] | None:
    findings = load_findings(root)
    found = None
    for item in findings:
        if item.get("id") != finding_id and item.get("fingerprint") != finding_id:
            continue
        item["status"] = status
        if status in {FindingStatus.CLOSED.value, FindingStatus.VERIFIED.value}:
            item["resolved_at"] = now_iso()
        if status in {FindingStatus.ACCEPTED_RISK.value, FindingStatus.SUPPRESSED.value, FindingStatus.FALSE_POSITIVE.value}:
            item["waiver"] = {
                "reason": reason or "",
                "approved_by": approved_by or "",
                "expires_at": expires_at,
            }
        found = item
        break
    if found:
        save_findings(root, findings)
    return found
