from __future__ import annotations

import re
from pathlib import Path

from .utils import iter_project_files, read_text, relative, now_iso

PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    ("private_key", "critical", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("github_token", "critical", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{30,}\b")),
    ("aws_access_key", "critical", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("google_api_key", "high", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("stripe_live_secret", "critical", re.compile(r"\bsk_live_[0-9A-Za-z]{20,}\b")),
    ("generic_secret_assignment", "high", re.compile(r"(?i)\b(api[_-]?key|secret|access[_-]?token|auth[_-]?token|password|passwd)\b\s*[:=]\s*['\"]([^'\"\n]{12,})['\"]")),
]

SENSITIVE_FILENAMES = {
    ".env": "high",
    "id_rsa": "critical",
    "id_ed25519": "critical",
    "service-account.json": "critical",
    "service_account.json": "critical",
}


def _redact(value: str) -> str:
    if len(value) <= 8:
        return "***"
    return value[:4] + "…" + value[-4:]


def scan_secrets(root: Path) -> dict:
    findings: list[dict] = []
    scanned_files = 0

    for p in iter_project_files(root, max_file_bytes=1_000_000):
        rel = relative(p, root)
        lower = rel.lower()
        if lower.startswith(("ops/reports/", "docs/", "skills/", "templates/", "examples/")):
            continue
        scanned_files += 1

        name = p.name.lower()
        if name in SENSITIVE_FILENAMES or p.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
            sev = SENSITIVE_FILENAMES.get(name, "high")
            if name.endswith(".example") or "sample" in name:
                sev = "low"
            findings.append({
                "id": "sensitive_file",
                "severity": sev,
                "file": rel,
                "line": None,
                "preview": "sensitive filename",
                "message": "Archivo potencialmente sensible presente en el árbol de trabajo; confirmar que no contenga credenciales versionadas.",
            })

        text = read_text(p, 1_000_000)
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pid, severity, pattern in PATTERNS:
                m = pattern.search(line)
                if not m:
                    continue
                if any(token in lower for token in ["test", "fixture", "mock"]):
                    effective = "medium" if severity in {"critical", "high"} else severity
                else:
                    effective = severity
                value = m.group(0)
                findings.append({
                    "id": pid,
                    "severity": effective,
                    "file": rel,
                    "line": line_no,
                    "preview": _redact(value),
                    "message": "Posible secreto detectado. Rotar si es real y mover a un secret store/variable de entorno.",
                })

    severity_rank = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    findings.sort(key=lambda f: (-severity_rank.get(f["severity"], 0), f["file"], f.get("line") or 0))
    deductions = {"critical": 40, "high": 20, "medium": 8, "low": 2}
    score = max(0, 100 - sum(deductions.get(f["severity"], 0) for f in findings))

    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in ["critical", "high", "medium", "low"]}
    return {
        "generated_at": now_iso(),
        "root": str(root),
        "scanned_files": scanned_files,
        "secret_hygiene_score": score,
        "counts": counts,
        "findings": findings,
    }


def secrets_markdown(result: dict) -> str:
    lines = [
        "# Secrets Scan", "",
        f"- Generated: {result['generated_at']}",
        f"- Files scanned: {result['scanned_files']}",
        f"- Secret Hygiene Score: **{result['secret_hygiene_score']}/100**", "",
        "## Summary", "",
    ]
    for sev in ["critical", "high", "medium", "low"]:
        lines.append(f"- {sev}: {result['counts'][sev]}")
    lines += ["", "## Findings", ""]
    if not result["findings"]:
        lines.append("- No likely secrets detected by the built-in patterns.")
    else:
        for f in result["findings"]:
            loc = f"{f['file']}:{f['line']}" if f.get("line") else f["file"]
            lines.append(f"- **{f['severity'].upper()} · {f['id']}** — `{loc}` — `{f['preview']}`")
    lines += ["", "> Values are intentionally redacted. A clean scan is not proof that no secrets exist; use provider-native scanners/Semgrep/Trivy/Gitleaks in deeper modes.", ""]
    return "\n".join(lines)


def should_fail(result: dict, threshold: str) -> bool:
    if threshold == "never":
        return False
    rank = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    required = rank[threshold]
    return any(rank.get(f["severity"], 0) >= required for f in result["findings"])
