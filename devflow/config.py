from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml

from .utils import slugify

DEFAULT_CONFIG = {
    "schema_version": 2,
    "project": {
        "name": "Project",
        "slug": "project",
        "stage": "mvp",
        "type": "fullstack",
        "criticality": "medium",
        "expected_traffic": "unknown",
        "budget_profile": "lean",
    },
    "profile": "mvp",
    "providers": {},
    "gates": {},
    "preferences": {
        "philosophy": "simple-first",
        "prefer_incremental_scaling": True,
        "avoid_premature_microservices": True,
        "avoid_premature_kubernetes": True,
    },
    "stack": {
        "backend": {"primary": "none", "alternatives": ["fastapi", "go", "nodejs", "quarkus", "php"]},
        "frontend": {"primary": "none", "alternatives": ["angular", "nextjs", "react", "javascript"], "styling": ["tailwind"]},
        "database": {"primary": "none", "alternatives": ["postgresql", "mariadb", "sqlite"]},
        "infrastructure": {"os": "ubuntu-server", "container": "none", "edge": "none", "orchestration": "none"},
        "ci_cd": {"provider": "none"},
        "observability": {"metrics": [], "load_testing": []},
    },
    "commands": {
        "install": "", "lint": "", "format_check": "", "typecheck": "", "test": "",
        "test_integration": "", "build": "", "security_scan": "", "dead_code_scan": "",
        "duplication_scan": "", "load_test": "",
    },
    "audit": {"profile": "fullstack", "minimum_confidence_to_publish_score": 50, "require_evidence": True, "allow_na": True},
    "approvals": {
        "create_remote_branch": False, "create_pr": False, "staging_deploy": False,
        "production_deploy": True, "production_load_test": True, "destructive_db_change": True,
        "force_push": True, "dns_change": True, "shared_infrastructure_change": True,
    },
    "stellarcode": {
        "enabled": False,
        "mcp_url": "https://api.stellarcodelabs.lat/mcp",
        "project_id": None,
        "client_name": "devflow-cli",
        "auth": {"mode": "bearer", "token_env": "STELLARCODE_TOKEN"},
        "sync": {"backlog": "remote_first", "trace": True, "evidence": True, "decisions": True, "risks": True},
    },
    "trace": {"enabled": True, "timezone": "America/Guayaquil", "id_prefix": "DEV"},
}


def load_config(root: Path) -> dict[str, Any]:
    path = root / ".devflow.yml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(".devflow.yml debe contener un objeto YAML")
    return data


def save_config(root: Path, data: dict[str, Any], overwrite: bool = False) -> Path:
    path = root / ".devflow.yml"
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} ya existe")
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def build_config(name: str, detected: dict, answers: dict) -> dict:
    cfg = yaml.safe_load(yaml.safe_dump(DEFAULT_CONFIG))
    cfg["project"].update({
        "name": name,
        "slug": slugify(name),
        "stage": answers.get("stage", "mvp"),
        "type": answers.get("type", detected.get("project_type", "fullstack")),
        "criticality": answers.get("criticality", "medium"),
        "expected_traffic": answers.get("traffic", "unknown"),
        "budget_profile": answers.get("budget", "lean"),
    })
    stage = answers.get("stage", "mvp")
    cfg["profile"] = {
        "prototype": "prototype",
        "mvp": "mvp",
        "growth": "production",
        "production": "production",
        "legacy": "legacy-modernization",
    }.get(stage, "mvp")
    cfg["stack"]["backend"]["primary"] = answers.get("backend") or detected.get("backend", "none")
    cfg["stack"]["frontend"]["primary"] = answers.get("frontend") or detected.get("frontend", "none")
    cfg["stack"]["database"]["primary"] = answers.get("database") or detected.get("database", "none")
    infra = detected.get("infra", [])
    cfg["stack"]["infrastructure"]["container"] = "docker" if "docker" in infra else "none"
    cfg["stack"]["infrastructure"]["edge"] = answers.get("edge") or ("cloudflare" if "cloudflare" in infra else "none")
    cfg["stack"]["infrastructure"]["orchestration"] = answers.get("orchestration") or ("k3s" if "k3s" in infra else "kubernetes" if "kubernetes" in infra else "none")
    cfg["stack"]["ci_cd"]["provider"] = "github-actions" if "github-actions" in infra else "none"
    obs = detected.get("observability", [])
    cfg["stack"]["observability"]["metrics"] = [x for x in obs if x in {"grafana", "prometheus", "netdata", "sentry"}]
    cfg["stack"]["observability"]["load_testing"] = ["k6"] if "k6" in obs else []
    return cfg
