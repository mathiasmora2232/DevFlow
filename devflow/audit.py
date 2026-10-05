from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Callable

from .detector import detect_stack, _runtime_candidate
from .scoring import weighted_score, evidence_confidence, cap_for_critical_security
from .stackfit import evaluate_stack_fit
from .utils import iter_project_files, read_text, relative, now_iso


def _category(cid: str, score, confidence: int, evidence=None, findings=None, applicable=True):
    return {
        "id": cid, "score": score, "confidence": confidence, "applicable": applicable,
        "evidence": evidence or [], "findings": findings or [],
    }


def _scan(root: Path):
    files = list(iter_project_files(root))
    # Analysis text is restricted to runtime/config evidence. Documentation, skills,
    # templates and reports remain available for structural checks but do not alter
    # code/security/performance signals merely by mentioning a technology/pattern.
    texts = []
    for p in files:
        rel = relative(p, root)
        if _runtime_candidate(rel, p):
            texts.append((p, read_text(p, 400_000)))
    return files, texts


def audit_project(root: Path, config: dict) -> dict:
    detected = detect_stack(root)
    files, texts = _scan(root)
    rels = [relative(p, root) for p in files]
    rel_lower = [r.lower() for r in rels]
    joined = "\n".join(t for _, t in texts[:600])
    joined_lower = joined.lower()
    findings = []
    categories = []

    # Security
    sec_score = 90
    sec_conf = 55
    sec_ev = []
    secret_patterns = [
        ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
        ("generic_secret", re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"\n]{12,}")),
    ]
    for p, txt in texts:
        rel = relative(p, root)
        if any(x in rel.lower() for x in ["example", "sample", "template", "test", "fixture"]):
            continue
        for kind, pat in secret_patterns:
            if pat.search(txt):
                sec_score -= 30
                findings.append({"severity": "critical" if kind == "private_key" else "high", "category": "security", "message": f"Posible secreto expuesto en {rel}", "evidence": rel})
                sec_ev.append(rel)
                break
    if any(r == ".env" or r.endswith("/.env") for r in rel_lower):
        sec_score -= 15
        findings.append({"severity": "high", "category": "security", "message": "Archivo .env presente en el árbol analizado; confirmar que no esté versionado con secretos.", "evidence": ".env"})
        sec_ev.append(".env")
    if re.search(r"allow_origins\s*=\s*\[?['\"]\*", joined, re.I) or re.search(r"Access-Control-Allow-Origin.{0,20}\*", joined, re.I):
        sec_score -= 10
        findings.append({"severity": "medium", "category": "security", "message": "CORS wildcard detectado; validar si es intencional.", "evidence": "repository search"})
        sec_ev.append("CORS wildcard")
    categories.append(_category("security", max(0, sec_score), sec_conf, sec_ev))

    # Architecture
    source_files = [p for p in files if p.suffix.lower() in {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".php"}]
    large = []
    for p in source_files:
        lines = read_text(p).count("\n") + 1
        if lines > 700:
            large.append((relative(p, root), lines))
    arch = 88 - min(24, len(large) * 4)
    if large:
        findings.append({"severity": "medium", "category": "architecture", "message": f"{len(large)} archivos fuente superan 700 líneas; revisar hotspots antes de dividir por reflejo.", "evidence": ", ".join(x[0] for x in large[:5])})
    categories.append(_category("architecture", max(0, arch), 45, [f"source_files={len(source_files)}", f"large_files={len(large)}"]))

    # Code quality
    todo_count = len(re.findall(r"(?i)\bTODO\b|\bFIXME\b|\bHACK\b", joined))
    quality = 88 - min(20, todo_count // 5)
    lint_markers = [x for x in rel_lower if any(k in x for k in ["eslint", "ruff", "flake8", "checkstyle", "golangci", "phpstan", "pint.json"])]
    if lint_markers: quality += 5
    if todo_count > 20:
        findings.append({"severity": "low", "category": "code_quality", "message": f"Se detectaron {todo_count} marcadores TODO/FIXME/HACK.", "evidence": "repository search"})
    categories.append(_category("code_quality", min(100, max(0, quality)), 50, lint_markers[:5] + [f"todo_fixme_hack={todo_count}"]))

    # Maintainability
    has_readme = any(Path(r).name.lower() == "readme.md" for r in rels)
    has_docs = any(r.startswith("docs/") for r in rel_lower)
    maintain = 68 + (12 if has_readme else 0) + (10 if has_docs else 0) - min(15, len(large) * 2)
    categories.append(_category("maintainability", min(100, maintain), 55, [f"README={has_readme}", f"docs={has_docs}"]))

    # Duplication approximate by repeated normalized non-trivial lines
    normalized = []
    for p, txt in texts:
        if p.suffix.lower() not in {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".php"}:
            continue
        for line in txt.splitlines():
            s = re.sub(r"\s+", " ", line.strip())
            if len(s) >= 45 and not s.startswith(("//", "#", "*", "import ", "from ")):
                normalized.append(s)
    counts = Counter(normalized)
    dup_lines = sum(c - 1 for c in counts.values() if c >= 3)
    dup_ratio = dup_lines / max(1, len(normalized))
    dup_score = max(35, round(100 - min(60, dup_ratio * 250), 1))
    categories.append(_category("duplication", dup_score, 40, [f"approx_duplicate_ratio={dup_ratio:.3f}"]))

    # Dead code: unknown without language analyzers
    categories.append(_category("dead_code", None, 15, ["No language-specific dead-code analyzer executed"]))

    # Testing
    test_files = [r for r in rel_lower if re.search(r"(^|/)(test|tests|spec|__tests__)(/|$)|\.(test|spec)\.", r)]
    if source_files:
        ratio = len(test_files) / max(1, len(source_files))
        test_score = min(95, 45 + ratio * 220)
        if not test_files:
            test_score = 30
            findings.append({"severity": "high", "category": "testing", "message": "No se detectaron archivos de prueba.", "evidence": "repository tree"})
        categories.append(_category("testing", round(test_score, 1), 55, [f"test_files={len(test_files)}", f"source_files={len(source_files)}"]))
    else:
        categories.append(_category("testing", None, 10, ["No source files detected"]))

    # Performance static
    perf_ev = []
    perf_score = 70
    if "cache" in joined_lower or "redis" in joined_lower:
        perf_score += 8; perf_ev.append("cache/redis references")
    if re.search(r"select\s+\*", joined_lower):
        perf_score -= 5; perf_ev.append("SELECT * patterns")
    categories.append(_category("performance", perf_score, 30, perf_ev or ["static-only review"]))

    # Runtime load deliberately unknown
    categories.append(_category("server_load", None, 0, ["Runtime/load metrics not provided"]))

    # SEO/accessibility
    web_app = detected.get("frontend") != "none"
    if web_app:
        seo = 50; seo_ev=[]
        if any("sitemap" in r for r in rel_lower): seo += 12; seo_ev.append("sitemap")
        if any(Path(r).name == "robots.txt" for r in rel_lower): seo += 10; seo_ev.append("robots.txt")
        if re.search(r"<title>|metadata\s*=|generateMetadata|react-helmet", joined, re.I): seo += 12; seo_ev.append("metadata/title")
        if re.search(r"canonical|application/ld\+json", joined, re.I): seo += 8; seo_ev.append("canonical/structured data")
        categories.append(_category("seo", min(100, seo), 45, seo_ev))
        a11y = 65
        if re.search(r"aria-|<label|alt=", joined, re.I): a11y += 10
        categories.append(_category("accessibility", min(100, a11y), 25, ["static semantic scan"]))
    else:
        categories.append(_category("seo", None, 100, ["N/A: no frontend detected"], applicable=False))
        categories.append(_category("accessibility", None, 100, ["N/A: no frontend detected"], applicable=False))

    # Database
    if detected.get("database") != "none":
        db = 65; db_ev=[f"detected={detected['database']}"]
        if any("migration" in r for r in rel_lower): db += 12; db_ev.append("migrations")
        if re.search(r"create\s+index|index\s*\(", joined, re.I): db += 8; db_ev.append("index definitions")
        categories.append(_category("database", min(100, db), 45, db_ev))
    else:
        categories.append(_category("database", None, 25, ["No database detected"], applicable=False))

    # DevOps
    infra = set(detected.get("infra", []))
    devops = 45; dev_ev=[]
    for token, pts in [("github-actions",20),("docker",15),("cloudflare",5),("kubernetes",5),("k3s",5)]:
        if token in infra: devops += pts; dev_ev.append(token)
    categories.append(_category("devops", min(100, devops), 60, dev_ev))

    # Observability
    obs = detected.get("observability", [])
    obs_score = 35 + min(55, len(obs) * 13)
    categories.append(_category("observability", obs_score, 50, obs))

    # Resilience
    resilience = 55
    res_ev=[]
    for term, pts in [("timeout",10),("retry",8),("health",7),("circuit",5),("backup",5)]:
        if term in joined_lower: resilience += pts; res_ev.append(term)
    categories.append(_category("resilience", min(100, resilience), 30, res_ev))

    # Dependencies
    lockfiles = [r for r in rel_lower if Path(r).name in {"package-lock.json","pnpm-lock.yaml","yarn.lock","poetry.lock","uv.lock","go.sum","composer.lock"}]
    dep_score = 85 if lockfiles else 60
    categories.append(_category("dependencies", dep_score, 45, lockfiles[:5]))

    # Documentation
    doc_score = 45 + (30 if has_readme else 0) + (20 if has_docs else 0)
    categories.append(_category("documentation", min(100, doc_score), 80, [f"README={has_readme}", f"docs={has_docs}"]))

    health = weighted_score(categories)
    health = cap_for_critical_security(health, findings)
    confidence = evidence_confidence(categories)
    stack_fit = evaluate_stack_fit(detected, config)

    for c in categories:
        for f in c.get("findings", []):
            findings.append(f)

    return {
        "generated_at": now_iso(), "mode": "static", "root": str(root),
        "detected_stack": detected,
        "project_health_score": health,
        "stack_fit_score": stack_fit["score"],
        "evidence_confidence": confidence,
        "categories": categories,
        "findings": findings,
        "stack_fit": stack_fit,
        "unknowns": [c["id"] for c in categories if c.get("score") is None and c.get("applicable", True)],
    }
