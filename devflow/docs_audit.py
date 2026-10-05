from __future__ import annotations

import re
from pathlib import Path

from .detector import detect_stack
from .utils import iter_project_files, read_text, relative, now_iso


def audit_docs(root: Path) -> dict:
    detected = detect_stack(root)
    files = list(iter_project_files(root))
    rels = [relative(p, root) for p in files]
    lower = [r.lower() for r in rels]

    readmes = [p for p in files if p.name.lower() == "readme.md"]
    readme_text = "\n".join(read_text(p, 300_000) for p in readmes)
    docs_text = "\n".join(read_text(p, 300_000) for p in files if relative(p, root).lower().startswith("docs/") or p.suffix.lower() == ".md")
    corpus = (readme_text + "\n" + docs_text).lower()

    checks: list[dict] = []

    def add(cid: str, weight: int, passed: bool, evidence: str, recommendation: str, applicable: bool = True) -> None:
        checks.append({
            "id": cid,
            "weight": weight,
            "passed": bool(passed),
            "applicable": applicable,
            "evidence": evidence,
            "recommendation": recommendation,
        })

    has_readme = bool(readmes) and len(readme_text.strip()) >= 120
    add("readme", 20, has_readme, ", ".join(relative(p, root) for p in readmes) or "missing", "Crear README con propósito, ejecución y contexto del proyecto.")

    setup = bool(re.search(r"\b(install|installation|setup|getting started|inicio|instalaci[oó]n|requisitos|requirements)\b", corpus))
    add("setup", 15, setup, "setup/install section detected" if setup else "not detected", "Documentar requisitos e instrucciones reproducibles de instalación/arranque.")

    architecture_files = [r for r in lower if any(k in r for k in ["architecture", "arquitectura", "adr", "decision", "diagram"])]
    architecture = bool(architecture_files) or bool(re.search(r"\b(architecture|arquitectura|componentes|modules|m[oó]dulos)\b", corpus))
    add("architecture", 15, architecture, ", ".join(architecture_files[:5]) or "not detected", "Documentar arquitectura, límites, módulos y decisiones relevantes.")

    backend_present = detected.get("backend") != "none"
    api_docs_files = [r for r in lower if any(k in r for k in ["openapi", "swagger", "api.md", "endpoints"])]
    api_docs = bool(api_docs_files) or bool(re.search(r"\b(openapi|swagger|endpoint|api routes|rutas api)\b", corpus))
    add("api", 15, api_docs, ", ".join(api_docs_files[:5]) or "not detected", "Documentar endpoints/contratos o enlazar OpenAPI/Swagger.", applicable=backend_present)

    env_files = [r for r in lower if Path(r).name in {".env.example", ".env.sample", "env.example", "example.env"}]
    env_docs = bool(env_files) or bool(re.search(r"\b(environment variables|variables de entorno|\.env|env vars)\b", corpus))
    add("environment", 15, env_docs, ", ".join(env_files[:5]) or "not detected", "Documentar variables de entorno sin incluir secretos.")

    infra_present = bool(detected.get("infra"))
    deploy_files = [r for r in lower if any(k in r for k in ["deploy", "deployment", "runbook", "operations", "ops/"])]
    deploy_docs = bool(deploy_files) or bool(re.search(r"\b(deploy|deployment|despliegue|rollback|production|producci[oó]n)\b", corpus))
    add("deployment", 15, deploy_docs, ", ".join(deploy_files[:5]) or "not detected", "Documentar despliegue, ambiente objetivo y rollback.", applicable=infra_present)

    testing = bool(re.search(r"\b(test|tests|testing|pytest|vitest|jest|mvn test|go test|pruebas)\b", corpus))
    add("testing", 10, testing, "testing instructions detected" if testing else "not detected", "Documentar cómo ejecutar las pruebas y quality gates.")

    applicable = [c for c in checks if c["applicable"]]
    total_weight = sum(c["weight"] for c in applicable)
    passed_weight = sum(c["weight"] for c in applicable if c["passed"])
    score = round((passed_weight / total_weight) * 100, 1) if total_weight else 0.0
    findings = [
        {"severity": "medium" if c["weight"] >= 15 else "low", "category": "documentation", "id": c["id"], "message": c["recommendation"], "evidence": c["evidence"]}
        for c in applicable if not c["passed"]
    ]

    return {
        "generated_at": now_iso(),
        "root": str(root),
        "documentation_score": score,
        "checks": checks,
        "findings": findings,
        "detected_stack": detected,
    }


def docs_markdown(result: dict) -> str:
    lines = [
        "# Documentation Review", "",
        f"- Generated: {result['generated_at']}",
        f"- Documentation Score: **{result['documentation_score']}/100**", "",
        "## Checks", "",
        "| Area | Result | Evidence |",
        "|---|---|---|",
    ]
    for c in result["checks"]:
        if not c["applicable"]:
            status = "N/A"
        else:
            status = "PASS" if c["passed"] else "MISSING"
        lines.append(f"| {c['id']} | {status} | {str(c['evidence']).replace('|','\\|')} |")
    lines += ["", "## Recommendations", ""]
    if result["findings"]:
        lines += [f"- **{f['id']}** — {f['message']}" for f in result["findings"]]
    else:
        lines.append("- No documentation gaps detected by this static review.")
    lines.append("")
    return "\n".join(lines)
