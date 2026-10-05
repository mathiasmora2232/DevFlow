from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

CURRENT_SCHEMA_VERSION = 3

ALLOWED_STAGES = {"prototype", "mvp", "growth", "production", "legacy"}
ALLOWED_CRITICALITY = {"low", "medium", "high", "critical"}
ALLOWED_OWNERSHIP = {"internal", "external_client"}
ALLOWED_ENGAGEMENT = {"greenfield", "migration", "refactor", "modernization", "maintenance", "audit_only"}
ALLOWED_PROFILES = {
    "prototype", "mvp", "production", "enterprise",
    "legacy-modernization", "external-audit", "high-security", "high-traffic",
}
DEFAULT_PROFILE_BY_STAGE = {
    "prototype": "prototype",
    "mvp": "mvp",
    "growth": "production",
    "production": "production",
    "legacy": "legacy-modernization",
}


def default_profile_for_stage(stage: str | None) -> str:
    return DEFAULT_PROFILE_BY_STAGE.get(str(stage or "mvp"), "mvp")


ALLOWED_TOP_LEVEL = {
    "version", "schema_version", "profile", "project", "providers", "gates",
    "preferences", "stack", "commands", "audit", "approvals", "stellarcode", "trace",
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

    for key in data:
        if key not in ALLOWED_TOP_LEVEL:
            errors.append({"path": key, "message": "unknown top-level key"})

    version = config_schema_version(data)
    if version not in {1, 2, CURRENT_SCHEMA_VERSION}:
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
    if project.get("ownership") and project["ownership"] not in ALLOWED_OWNERSHIP:
        errors.append({"path": "project.ownership", "message": f"invalid ownership: {project['ownership']}"})
    if project.get("engagement") and project["engagement"] not in ALLOWED_ENGAGEMENT:
        errors.append({"path": "project.engagement", "message": f"invalid engagement: {project['engagement']}"})

    profile = data.get("profile")
    if profile and profile not in ALLOWED_PROFILES:
        errors.append({"path": "profile", "message": f"unknown profile: {profile}"})

    stellar = data.get("stellarcode", {})
    if stellar and not isinstance(stellar, dict):
        errors.append({"path": "stellarcode", "message": "must be a mapping"})
    elif stellar.get("enabled"):
        if not stellar.get("mcp_url"):
            errors.append({"path": "stellarcode.mcp_url", "message": "required when enabled"})
        auth = stellar.get("auth", {})
        forbidden = [key for key in auth if str(key).lower() in {"token", "secret", "password", "access_token"}]
        if forbidden:
            errors.append({
                "path": f"stellarcode.auth.{forbidden[0]}",
                "message": "raw credentials must not be stored in config; use token_env",
            })
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
        stage = str(project.get("stage") or "mvp")
        profile = {
            "prototype": "prototype",
            "mvp": "mvp",
            "growth": "production",
            "production": "production",
            "legacy": "legacy-modernization",
        }.get(stage, "mvp")
        migrated.setdefault("profile", profile)
        migrated.setdefault("providers", {})
        migrated.setdefault("gates", {})
        stellar = migrated.setdefault("stellarcode", {})
        if isinstance(stellar, dict):
            auth = stellar.setdefault("auth", {})
            if isinstance(auth, dict):
                for key in ("token", "secret", "password", "access_token"):
                    auth.pop(key, None)
                auth.setdefault("mode", "bearer")
                auth.setdefault("token_env", "STELLARCODE_TOKEN")
        source_version = 2

    if source_version == 2 and target_version >= 3:
        migrated["schema_version"] = 3
        project = migrated.setdefault("project", {})
        project.setdefault("ownership", "internal")
        project.setdefault("engagement", "modernization" if project.get("stage") == "legacy" else "greenfield")
        project.setdefault("client_id", None)
        source_version = 3

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
    diff = config_diff_text(data, migrated)
    backup = None
    if changed and not check:
        backup = root / f".devflow.yml.v{config_schema_version(data)}.bak"
        if not backup.exists():
            backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        path.write_text(yaml.safe_dump(migrated, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return {
        "changed": changed,
        "from": config_schema_version(data),
        "to": CURRENT_SCHEMA_VERSION,
        "config": migrated,
        "diff": diff,
        "backup": str(backup) if backup else None,
    }


def config_summary(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": config_schema_version(data),
        "project": data.get("project", {}),
        "profile": data.get("profile") or default_profile_for_stage(data.get("project", {}).get("stage")),
        "providers": sorted((data.get("providers") or {}).keys()),
        "stellarcode_enabled": bool(data.get("stellarcode", {}).get("enabled")),
        "gates": sorted((data.get("gates") or {}).keys()),
    }


def config_diff_text(before: dict[str, Any], after: dict[str, Any]) -> str:
    import difflib
    old = yaml.safe_dump(before, sort_keys=False, allow_unicode=True).splitlines(keepends=True)
    new = yaml.safe_dump(after, sort_keys=False, allow_unicode=True).splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            old,
            new,
            fromfile=".devflow.yml",
            tofile=".devflow.yml (migrated)",
        )
    )
