from __future__ import annotations

import re
from pathlib import Path
from .utils import git_info, now_iso, today_compact, replace_markdown_field

TRACE_TEMPLATE = """# Project Trace

## Snapshot

- Last sync:
- Branch:
- Revision:
- Environment:
- Overall status:

## Active

## Pending

## Blocked

## Recently completed

## Validation

## Risks

## Next actions
"""

BACKLOG_TEMPLATE = """# Backlog

## Now

## Next

## Later
"""


def ensure_ops(root: Path) -> None:
    ops = root / "ops"
    ops.mkdir(parents=True, exist_ok=True)
    if not (ops / "TRACE.md").exists(): (ops / "TRACE.md").write_text(TRACE_TEMPLATE, encoding="utf-8")
    if not (ops / "BACKLOG.md").exists(): (ops / "BACKLOG.md").write_text(BACKLOG_TEMPLATE, encoding="utf-8")
    if not (ops / "RISKS.md").exists(): (ops / "RISKS.md").write_text("# Risks\n", encoding="utf-8")
    if not (ops / "SECURITY.md").exists(): (ops / "SECURITY.md").write_text("# Security Findings\n", encoding="utf-8")
    if not (ops / "RELEASES.md").exists(): (ops / "RELEASES.md").write_text("# Releases\n", encoding="utf-8")
    if not (root / "CHANGELOG.md").exists(): (root / "CHANGELOG.md").write_text("# Changelog\n\n## [Unreleased]\n", encoding="utf-8")


def sync_trace(root: Path, environment: str = "local") -> dict:
    ensure_ops(root)
    path = root / "ops" / "TRACE.md"
    text = path.read_text(encoding="utf-8")
    git = git_info(root)
    text = replace_markdown_field(text, "Last sync", now_iso())
    text = replace_markdown_field(text, "Branch", str(git["branch"]))
    text = replace_markdown_field(text, "Revision", str(git["revision"]))
    text = replace_markdown_field(text, "Environment", environment)
    text = replace_markdown_field(text, "Overall status", "working-tree-dirty" if git.get("dirty") else "clean-or-unknown")
    path.write_text(text, encoding="utf-8")
    return git


def next_work_id(root: Path, prefix: str = "DEV") -> str:
    ensure_ops(root)
    text = (root / "ops" / "TRACE.md").read_text(encoding="utf-8")
    date = today_compact()
    pat = re.compile(rf"\b{re.escape(prefix)}-{date}-(\d{{3}})\b")
    nums = [int(m.group(1)) for m in pat.finditer(text)]
    return f"{prefix}-{date}-{(max(nums) + 1 if nums else 1):03d}"


def add_work(root: Path, wid: str, title: str, kind: str, priority: str, description: str, acceptance: list[str]) -> None:
    ensure_ops(root)
    trace = root / "ops" / "TRACE.md"
    block = f"""

### {wid} — {title}

- Status: `planned`
- Type: `{kind}`
- Priority: `{priority}`
- Started: {now_iso()}
- Updated: {now_iso()}

#### Goal

{description or title}

#### Acceptance criteria

""" + ("\n".join(f"- {a}" for a in acceptance) if acceptance else "- TODO: definir criterios verificables") + "\n\n#### Evidence\n\n- Pending\n"
    trace.write_text(trace.read_text(encoding="utf-8").rstrip() + block + "\n", encoding="utf-8")
    backlog = root / "ops" / "BACKLOG.md"
    with backlog.open("a", encoding="utf-8") as fh:
        fh.write(f"\n- [ ] **{wid}** `{priority}` `{kind}` — {title}\n")
