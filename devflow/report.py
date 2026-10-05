from __future__ import annotations

from pathlib import Path
from .utils import now_iso


def audit_markdown(result: dict) -> str:
    def fmt(v): return "N/A" if v is None else f"{v:.1f}" if isinstance(v, float) else str(v)
    lines = [
        "# Project Audit", "",
        f"- Generated: {result.get('generated_at')}",
        f"- Mode: `{result.get('mode')}`",
        f"- Project Health Score: **{fmt(result.get('project_health_score'))}/100**",
        f"- Stack Fit Score: **{fmt(result.get('stack_fit_score'))}/100**",
        f"- Evidence Confidence: **{fmt(result.get('evidence_confidence'))}/100**", "",
        "## Scorecard", "",
        "| Category | Score | Confidence | Evidence |",
        "|---|---:|---:|---|",
    ]
    for c in result.get("categories", []):
        ev = "; ".join(c.get("evidence", [])[:3]).replace("|", "\\|")
        lines.append(f"| {c['id']} | {fmt(c.get('score'))} | {c.get('confidence',0)} | {ev} |")
    lines += ["", "## Findings", ""]
    fs = sorted(result.get("findings", []), key=lambda x: {"critical":0,"high":1,"medium":2,"low":3}.get(x.get("severity"),4))
    if not fs:
        lines.append("No static findings recorded.")
    for f in fs:
        lines.append(f"- **{f.get('severity','info').upper()} · {f.get('category')}** — {f.get('message')} ({f.get('evidence','')})")
    lines += ["", "## Unknowns / missing evidence", ""]
    unknowns = result.get("unknowns", [])
    if unknowns:
        for u in unknowns: lines.append(f"- {u}")
    else:
        lines.append("- None")
    lines += ["", "## Stack review", "", f"Recommendation: `{result.get('stack_fit',{}).get('recommendation','unknown')}`", ""]
    for w in result.get("stack_fit", {}).get("warnings", []):
        lines.append(f"- ⚠ {w}")
    lines += ["", "> Static analysis cannot prove production health, real server load, or complete security. Add runtime evidence before making those claims.", ""]
    return "\n".join(lines)


def stack_review_markdown(detected: dict, fit: dict) -> str:
    lines = ["# Stack Review", "", f"Generated: {now_iso()}", "", f"**Stack Fit Score: {fit['score']}/100**", "", f"Recommendation: `{fit['recommendation']}`", "", "## Components", "", "| Component | Actual | Score | Assessment |", "|---|---|---:|---|"]
    for c in fit["components"]:
        lines.append(f"| {c['component']} | {c['actual']} | {c['score'] if c['score'] is not None else 'N/A'} | {c['reason']} |")
    lines += ["", "## Infrastructure detected", ""]
    lines.append(", ".join(detected.get("infra", [])) or "None detected")
    lines += ["", "## Warnings", ""]
    if fit["warnings"]:
        lines.extend(f"- {w}" for w in fit["warnings"])
    else:
        lines.append("- No proportionality warnings.")
    lines += ["", "> Stack Fit is not Project Health. A non-preferred technology can still be the correct technology for a healthy project.", ""]
    return "\n".join(lines)
