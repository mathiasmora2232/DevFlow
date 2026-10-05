from __future__ import annotations

import json
import re
from pathlib import Path
from .utils import iter_project_files, read_text, relative

NON_RUNTIME_PREFIXES = (
    "docs/", "skills/", "templates/", "scorecards/", "stacks/", "ops/",
    "examples/", "adapters/", ".github/issue_template/",
)
RUNTIME_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".php", ".sql", ".env", ".properties", ".yml", ".yaml", ".toml", ".xml", ".json"}


def _json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _runtime_candidate(rel: str, p: Path) -> bool:
    lower = rel.lower()
    if lower == ".devflow.yml" or lower.startswith(NON_RUNTIME_PREFIXES):
        return False
    if p.suffix.lower() in RUNTIME_SUFFIXES:
        return True
    return p.name in {"Dockerfile", "requirements.txt", "go.mod", "package.json", "composer.json", "pom.xml"}


def detect_stack(root: Path) -> dict:
    backend = "none"
    frontend = "none"
    database = "none"
    infra: set[str] = set()
    observability: set[str] = set()
    evidence: dict[str, list[str]] = {"backend": [], "frontend": [], "database": [], "infra": [], "observability": []}

    package_paths = [p for p in root.rglob("package.json") if "node_modules" not in p.parts and not any(part in {"examples","templates"} for part in p.parts)]
    dep_names: set[str] = set()
    for package_path in package_paths[:30]:
        package = _json(package_path)
        deps = {}
        deps.update(package.get("dependencies", {}) or {})
        deps.update(package.get("devDependencies", {}) or {})
        dep_names |= {str(k).lower() for k in deps}

    if "next" in dep_names:
        frontend = "nextjs"; evidence["frontend"].append("package.json: next")
    elif "@angular/core" in dep_names:
        frontend = "angular"; evidence["frontend"].append("package.json: @angular/core")
    elif "react" in dep_names:
        frontend = "react"; evidence["frontend"].append("package.json: react")
    elif package_paths:
        frontend = "javascript"; evidence["frontend"].append("package.json")

    if any(x in dep_names for x in {"express", "fastify", "koa", "@nestjs/core", "hono"}):
        backend = "nodejs"; evidence["backend"].append("package.json: backend framework")

    py_sources = []
    for filename in ["requirements.txt", "pyproject.toml"]:
        for p in root.rglob(filename):
            rel = relative(p, root)
            if not rel.lower().startswith(NON_RUNTIME_PREFIXES):
                py_sources.append(read_text(p))
    py_blob = "\n".join(py_sources).lower()
    if "fastapi" in py_blob:
        backend = "fastapi"; evidence["backend"].append("Python dependency: fastapi")

    go_mods = [p for p in root.rglob("go.mod") if not relative(p, root).lower().startswith(NON_RUNTIME_PREFIXES)]
    if go_mods:
        backend = "go"; evidence["backend"].append(relative(go_mods[0], root))

    poms = [p for p in root.rglob("pom.xml") if not relative(p, root).lower().startswith(NON_RUNTIME_PREFIXES)]
    for p in poms:
        if "quarkus" in read_text(p).lower():
            backend = "quarkus"; evidence["backend"].append(f"{relative(p,root)}: quarkus"); break

    composers = [p for p in root.rglob("composer.json") if not relative(p, root).lower().startswith(NON_RUNTIME_PREFIXES)]
    if composers:
        backend = "php"; evidence["backend"].append(relative(composers[0], root))

    runtime_texts: list[tuple[str, str]] = []
    for p in iter_project_files(root, max_file_bytes=300_000):
        rel = relative(p, root)
        lower = rel.lower()
        if not _runtime_candidate(rel, p):
            continue
        txt = read_text(p, 200_000).lower()
        runtime_texts.append((rel, txt))

        # Infrastructure must be evidenced by actual config/path conventions.
        if p.name == "Dockerfile" or re.search(r"(^|/)(docker-compose|compose)\.ya?ml$", lower):
            infra.add("docker"); evidence["infra"].append(rel)
        if lower.startswith(".github/workflows/"):
            infra.add("github-actions"); evidence["infra"].append(rel)
        if p.name.lower() in {"wrangler.toml", "wrangler.json", "wrangler.jsonc"}:
            infra.add("cloudflare"); evidence["infra"].append(rel)
        if ("k8s/" in lower or "kubernetes/" in lower or "helm/" in lower or p.name.lower() in {"deployment.yaml","deployment.yml","statefulset.yaml","statefulset.yml"}) and ("apiversion:" in txt or "kind:" in txt):
            infra.add("kubernetes"); evidence["infra"].append(rel)
        if (p.suffix.lower() in {".sh", ".yml", ".yaml"} or "k3s" in lower) and re.search(r"\bk3s\b", txt):
            infra.add("k3s"); evidence["infra"].append(rel)

        # Observability requires dependency/config evidence, not prose mentions.
        filename = p.name.lower()
        for obs in ["grafana", "prometheus", "netdata"]:
            if obs in filename or f"/{obs}/" in lower:
                observability.add(obs); evidence["observability"].append(f"{rel}: config")
        if "sentry" in dep_names or re.search(r"\bsentry[_-]?sdk\b|@sentry/", txt):
            observability.add("sentry"); evidence["observability"].append(f"{rel}: sentry dependency/config")
        if filename.startswith("k6") or re.search(r"from ['\"]k6|import .* from ['\"]k6", txt):
            observability.add("k6"); evidence["observability"].append(f"{rel}: k6 script")

    corpus = "\n".join(txt for _, txt in runtime_texts[:500])
    if re.search(r"postgresql://|postgres://|\bpsycopg\b|\basyncpg\b|org\.postgresql|\bpg\b", corpus):
        database = "postgresql"; evidence["database"].append("runtime/config references PostgreSQL")
    elif re.search(r"mariadb://|mysql://|\bmariadb\b|\bmysql2?\b", corpus):
        database = "mariadb"; evidence["database"].append("runtime/config references MariaDB/MySQL")
    elif re.search(r"sqlite://|\bsqlite3?\b", corpus):
        database = "sqlite"; evidence["database"].append("runtime/config references SQLite")

    if backend != "none" and frontend != "none": project_type = "fullstack"
    elif backend != "none": project_type = "backend"
    elif frontend != "none": project_type = "frontend"
    else: project_type = "unknown"

    # Deduplicate evidence while preserving order.
    for key, values in evidence.items():
        evidence[key] = list(dict.fromkeys(values))

    return {
        "backend": backend, "frontend": frontend, "database": database,
        "infra": sorted(infra), "observability": sorted(observability),
        "project_type": project_type, "evidence": evidence,
    }
