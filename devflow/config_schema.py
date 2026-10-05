from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

CURRENT_SCHEMA_VERSION = 2

ALLOWED_STAGES = {"prototype", "mvp", "growth", "production", "legacy"}
ALLOWED_CRITICALITY = {"low", "medium", "high", "critical"}
ALLOWED_PROFILES = {
    "prototype", "mvp", "production", "enterprise",
    "legacy-modernization", "external-audit", "high-security", "high-traffic",
}


def config_schema_version(data: dict[str, Any]) -> int:
    if "schema_version" in data:
        return int(data.get("schema_version") or 0)
    if "version" in data:
        return int(data.get("version") or 1)
    return 1


def validate_config(data: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not isinstance(data, dict):
        return [{"path": "$", "message": "config must be a mapping"}]

    version = config_schema_version(data)
    if version not in {1, CURRENT_SCHEMA_VERSION}:
        errors.append({"path": "schema_version", "message": f"unsupported schema version {version}"})

    project = data.get("project")
    if not isinstance(project, dict):
        errors.append({"path": "project", "message": "project section is required"})
        return errors

    for key in ("name", "slug", "stage", "criticality"):
        if not project.get(key):
            errors.append({"path": f"project.{key}", "message": "required"})

    if project.get("stage") and project["stage"] not in ALLOWED_STAGES:
        errors.append({"path": "project.stage", "message": f"invalid stage: {project['stage']}"})
    if project.get("criticality") and project["criticality"] not in ALLOWED_CRITICALITY:
        errors.append({"path": "project.criticality", "message": f"invalid criticality: {project['criticality']}"})

    profile = data.get("profile") or project.get("stage")
    if profile and profile not in ALLOWED_PROFILES and profile not in ALLOWED_STAGES:
        errors.append({"path": "profile", "message": f"unknown profile: {profile}"})

    stellar = data.get("stellarcode", {})
    if stellar and not isinstance(stellar, dict):
        errors.append({"path": "stellarcode", "message": "must be a mapping"})
    elif stellar.get("enabled"):
        if not stellar.get("mcp_url"):
            errors.append({"path": "stellarcode.mcp_url", "message": "required when enabled"})
        auth = stellar.get("auth", {})
        if "token" in auth:
            errors.append({"path": "stellarcode.auth.token", "message": "raw tokens must not be stored in config"})
        if auth.get("mode") == "bearer" and not auth.get("token_env"):
            errors.append({"path": "stellarcode.auth.token_env", "message": "required for bearer auth"})

    gates = data.get("gates", {})
    if gates and not isinstance(gates, dict):
        errors.append({"path": "gates", "message": "must be a mapping"})

    return errors


def migrate_config(data: dict[str, Any], target_version: int = CURRENT_SCHEMA_VERSION) -> dict[str, Any]:
    source_version = config_schema_version(data)
    if source_version > target_version:
        raise ValueError(f"cannot migrate config backwards from {source_version} to {target_version}")
    migrated = deepcopy(data)

    if source_version == 1 and target_version >= 2:
        migrated.pop("version", None)
        migrated["schema_version"] = 2
        project = migrated.setdefault("project", {})
        migrated.setdefault("profile", project.get("stage") or "mvp")
        migrated.setdefault("providers", {})
        migrated.setdefault("gates", {})
        source_version = 2

    if source_version != target_version:
        raise ValueError(f"no migration path from {config_schema_version(data)} to {target_version}")
    return migrated


def migrate_config_file(root: Path, check: bool = False) -> dict[str, Any]:
    path = root / ".devflow.yml"
    if not path.exists():
        raise FileNotFoundError(".devflow.yml not found")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    migrated = migrate_config(data)
    changed = migrated != data
    if changed and not check:
        backup = root / ".devflow.yml.v1.bak"
        if not backup.exists():
            backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        path.write_text(yaml.safe_dump(migrated, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return {"changed": changed, "from": config_schema_version(data), "to": CURRENT_SCHEMA_VERSION, "config": migrated}


def config_summary(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": config_schema_version(data),
        "project": data.get("project", {}),
        "profile": data.get("profile") or data.get("project", {}).get("stage"),
        "providers": sorted((data.get("providers") or {}).keys()),
        "stellarcode_enabled": bool(data.get("stellarcode", {}).get("enabled")),
        "gates": sorted((data.get("gates") or {}).keys()),
    }
