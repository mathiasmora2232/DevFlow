from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from .config import load_config
from .detector import detect_stack
from .utils import git_info, now_iso


def _tool(name: str) -> bool:
    return shutil.which(name) is not None


def doctor_project(root: Path) -> dict:
    detected = detect_stack(root)
    config = load_config(root)
    git = git_info(root)
    total, used, free = shutil.disk_usage(root)
    free_gb = round(free / (1024 ** 3), 2)

    checks: list[dict] = []

    def add(name: str, ok: bool, required: bool, detail: str, weight: int = 10) -> None:
        checks.append({
            "name": name,
            "ok": bool(ok),
            "required": required,
            "detail": detail,
            "weight": weight,
        })

    add("python", sys.version_info >= (3, 10), True, f"{sys.version.split()[0]} @ {sys.executable}", 15)
    add("git", _tool("git"), True, "available" if _tool("git") else "not found in PATH", 15)
    add("git_repository", git.get("revision") != "unknown", False, f"branch={git.get('branch')} revision={git.get('revision')}", 8)
    add("devflow_config", bool(config), False, ".devflow.yml found" if config else ".devflow.yml missing; run /nuevo-proyecto", 10)
    add("writable", os.access(root, os.W_OK), True, str(root), 10)
    disk_ok = free_gb >= 1.0
    disk_detail = f"{free_gb} GB free"
    if free_gb < 1.0:
        disk_detail += " — critical: free space below 1 GB"
    elif free_gb < 5.0:
        disk_detail += " — warning: low free space"
    add("disk_space", disk_ok, True, disk_detail, 15)

    backend = detected.get("backend")
    frontend = detected.get("frontend")
    infra = set(detected.get("infra", []))
    obs = set(detected.get("observability", []))

    stack_tools: list[tuple[str, str, bool]] = []
    if backend == "fastapi":
        stack_tools += [("ruff", "Python linting", False), ("pytest", "Python tests", False)]
    elif backend == "go":
        stack_tools += [("go", "Go toolchain", True)]
    elif backend == "nodejs" or frontend in {"nextjs", "react", "angular", "javascript"}:
        stack_tools += [("node", "Node.js runtime", True), ("npm", "Node package manager", False)]
    elif backend == "quarkus":
        stack_tools += [("java", "Java runtime", True), ("mvn", "Maven", False)]
    elif backend == "php":
        stack_tools += [("php", "PHP runtime", True), ("composer", "Composer", False)]

    if "docker" in infra:
        stack_tools.append(("docker", "Docker", False))
    if "k6" in obs:
        stack_tools.append(("k6", "Load testing", False))

    seen: set[str] = set()
    for tool, purpose, required in stack_tools:
        if tool in seen:
            continue
        seen.add(tool)
        add(f"tool:{tool}", _tool(tool), required, purpose, 5 if not required else 8)

    denom = sum(c["weight"] for c in checks)
    points = sum(c["weight"] for c in checks if c["ok"])
    readiness = round((points / denom) * 100, 1) if denom else 0.0

    blockers = [c for c in checks if c["required"] and not c["ok"]]
    warnings = [c for c in checks if not c["required"] and not c["ok"]]
    if 1.0 <= free_gb < 5.0:
        warnings.append({"name": "disk_space_low", "detail": f"Only {free_gb} GB free", "required": False, "ok": False, "weight": 0})

    return {
        "generated_at": now_iso(),
        "root": str(root),
        "readiness_score": readiness,
        "ready": not blockers,
        "free_disk_gb": free_gb,
        "detected_stack": detected,
        "checks": checks,
        "blockers": blockers,
        "warnings": warnings,
    }


def doctor_markdown(result: dict) -> str:
    lines = [
        "# DevFlow Doctor", "",
        f"- Generated: {result['generated_at']}",
        f"- Readiness: **{result['readiness_score']}/100**",
        f"- Ready: **{'yes' if result['ready'] else 'no'}**",
        f"- Free disk: **{result['free_disk_gb']} GB**", "",
        "## Checks", "",
        "| Check | Status | Required | Detail |",
        "|---|---|---|---|",
    ]
    for c in result["checks"]:
        status = "PASS" if c["ok"] else "FAIL" if c["required"] else "WARN"
        lines.append(f"| {c['name']} | {status} | {'yes' if c['required'] else 'no'} | {str(c['detail']).replace('|','\\|')} |")
    lines += ["", "## Blockers", ""]
    if result["blockers"]:
        lines += [f"- {c['name']}: {c['detail']}" for c in result["blockers"]]
    else:
        lines.append("- None")
    lines += ["", "## Warnings", ""]
    if result["warnings"]:
        lines += [f"- {c['name']}: {c['detail']}" for c in result["warnings"]]
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)
