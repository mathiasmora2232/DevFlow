from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any

import yaml

from .config import load_config


class StellarError(RuntimeError):
    pass


def stellar_config(root: Path, require_project: bool = True, allow_disabled: bool = False) -> dict[str, Any]:
    cfg = load_config(root)
    stellar = cfg.get("stellarcode", {}) if cfg else {}
    if not stellar.get("enabled") and not allow_disabled:
        raise StellarError("StellarCode integration is disabled. Run `devflow stellar-bind --project-id <id>` or `devflow stellar-adopt`.")
    if not stellar.get("mcp_url"):
        raise StellarError("stellarcode.mcp_url is missing in .devflow.yml")
    if require_project and not stellar.get("project_id"):
        raise StellarError("stellarcode.project_id is missing. Run `devflow stellar-bind --project-id <id>`.")
    return stellar


def stellar_token(stellar: dict[str, Any]) -> str:
    env_name = stellar.get("auth", {}).get("token_env") or "STELLARCODE_TOKEN"
    token = os.getenv(env_name, "").strip()
    if not token:
        raise StellarError(f"Missing StellarCode access token in environment variable {env_name}.")
    return token


async def _call_tool_async(url: str, token: str, tool: str, arguments: dict[str, Any], client_name: str) -> dict[str, Any]:
    try:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
    except ImportError as exc:
        raise StellarError("Python package `mcp` is required. Reinstall DevFlow v0.4+ with `pip install -e .`.") from exc

    headers = {
        "Authorization": f"Bearer {token}",
        "X-MCP-Client": client_name,
        "X-Request-Id": f"devflow-{os.getpid()}-{tool}",
    }

    try:
        async with streamablehttp_client(url, headers=headers) as streams:
            read_stream, write_stream = streams[0], streams[1]
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(tool, arguments=arguments)
    except Exception as exc:
        raise StellarError(f"StellarCode MCP call failed for {tool}: {exc}") from exc

    if getattr(result, "isError", False):
        message = "MCP tool returned an error"
        content = getattr(result, "content", None) or []
        if content and getattr(content[0], "text", None):
            message = content[0].text
        raise StellarError(message)

    structured = getattr(result, "structuredContent", None)
    if structured is not None:
        return structured

    content = getattr(result, "content", None) or []
    for item in content:
        text = getattr(item, "text", None)
        if text:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {"text": text}
    return {}


def call_tool(root: Path, tool: str, arguments: dict[str, Any] | None = None, require_project: bool = True, allow_disabled: bool = False) -> dict[str, Any]:
    stellar = stellar_config(root, require_project=require_project, allow_disabled=allow_disabled)
    token = stellar_token(stellar)
    client_name = stellar.get("client_name") or "devflow-cli"
    return asyncio.run(_call_tool_async(stellar["mcp_url"], token, tool, arguments or {}, client_name))


def bind_project(root: Path, project_id: int, mcp_url: str | None = None, token_env: str = "STELLARCODE_TOKEN") -> Path:
    path = root / ".devflow.yml"
    cfg = load_config(root)
    if not cfg:
        raise StellarError("No .devflow.yml found. Run `devflow /nuevo-proyecto` first.")

    cfg["stellarcode"] = {
        **cfg.get("stellarcode", {}),
        "enabled": True,
        "mcp_url": mcp_url or cfg.get("stellarcode", {}).get("mcp_url") or "https://api.stellarcodelabs.lat/mcp",
        "project_id": int(project_id),
        "client_name": cfg.get("stellarcode", {}).get("client_name") or "devflow-cli",
        "auth": {
            "mode": "bearer",
            "token_env": token_env,
        },
        "sync": {
            "backlog": "remote_first",
            "trace": True,
            "evidence": True,
            "decisions": True,
            "risks": True,
            **cfg.get("stellarcode", {}).get("sync", {}),
        },
    }
    path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def choose_next_task(tasks: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [t for t in tasks if t.get("status") in {"in_progress", "pending", "ready", "review"}]
    if not candidates:
        return None
    status_rank = {"in_progress": 0, "review": 1, "ready": 2, "pending": 3}
    priority_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    candidates.sort(
        key=lambda t: (
            status_rank.get(t.get("status"), 9),
            priority_rank.get(t.get("priority"), 9),
            t.get("due_date") or "9999-12-31",
            t.get("id") or 0,
        )
    )
    return candidates[0]


def write_stellar_snapshot(root: Path, payload: dict[str, Any]) -> Path:
    ops = root / "ops"
    ops.mkdir(parents=True, exist_ok=True)
    path = ops / "STELLAR.md"
    identity = payload.get("identity", {})
    tasks = payload.get("tasks", [])
    counts: dict[str, int] = {}
    for task in tasks:
        counts[task.get("status") or "unknown"] = counts.get(task.get("status") or "unknown", 0) + 1

    lines = [
        "# StellarCode Snapshot",
        "",
        f"- User: {identity.get('user', {}).get('name') or identity.get('user', {}).get('email') or 'unknown'}",
        f"- Project ID: {identity.get('project_id') or 'unknown'}",
        f"- Project role: {identity.get('project_role') or identity.get('user', {}).get('global_role') or 'unknown'}",
        f"- Client: {identity.get('client') or 'unknown'}",
        "",
        "## Kanban",
        "",
    ]
    if counts:
        lines.extend(f"- {status}: {count}" for status, count in sorted(counts.items()))
    else:
        lines.append("- No tasks")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


async def _list_tools_async(url: str, token: str, client_name: str) -> list[str]:
    try:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
    except ImportError as exc:
        raise StellarError("Python package `mcp` is required. Reinstall DevFlow with `pip install -e .`.") from exc

    headers = {
        "Authorization": f"Bearer {token}",
        "X-MCP-Client": client_name,
        "X-Request-Id": f"devflow-{os.getpid()}-list-tools",
    }
    try:
        async with streamablehttp_client(url, headers=headers) as streams:
            read_stream, write_stream = streams[0], streams[1]
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.list_tools()
    except Exception as exc:
        raise StellarError(f"StellarCode MCP list_tools failed: {exc}") from exc
    return sorted(tool.name for tool in getattr(result, "tools", []) or [])


def list_tools(root: Path, require_project: bool = False) -> list[str]:
    stellar = stellar_config(root, require_project=require_project)
    token = stellar_token(stellar)
    return asyncio.run(_list_tools_async(
        stellar["mcp_url"],
        token,
        stellar.get("client_name") or "devflow-cli",
    ))


def capability_matrix(tool_names: list[str] | set[str]) -> dict[str, dict[str, Any]]:
    tools = set(tool_names)

    def state(native: set[str], bridge: set[str] | None = None) -> str:
        if native and native.issubset(tools):
            return "native"
        if bridge and bridge.issubset(tools):
            return "bridge"
        return "missing"

    return {
        "project": {"state": state({"create_project", "get_project"}), "required": ["create_project", "get_project"]},
        "kanban": {"state": state({"list_project_tasks", "create_roadmap_task", "update_task"}), "required": ["list_project_tasks", "create_roadmap_task", "update_task"]},
        "phases": {"state": state({"get_project_plan", "create_project_phase"}), "required": ["get_project_plan", "create_project_phase"]},
        "evidence": {"state": state({"add_project_evidence"}), "required": ["add_project_evidence"]},
        "risks": {"state": state({"add_project_risk"}), "required": ["add_project_risk"]},
        "decisions": {"state": state({"list_project_decisions", "add_project_decision"}), "required": ["list_project_decisions", "add_project_decision"]},
        "discovery": {"state": state({"sync_discovery_bundle"}, {"add_project_evidence"}), "required": ["sync_discovery_bundle"]},
        "stack": {"state": state({"sync_stack"}, {"add_project_evidence"}), "required": ["sync_stack"]},
        "audits": {"state": state({"sync_audit_bundle"}, {"add_project_evidence"}), "required": ["sync_audit_bundle"]},
        "infrastructure": {"state": state({"sync_infrastructure"}, {"add_project_evidence"}), "required": ["sync_infrastructure"]},
        "time_tracking": {"state": state({"start_time", "stop_time", "create_time_entry", "list_time_entries"}), "required": ["start_time", "stop_time", "create_time_entry", "list_time_entries"]},
    }


def adopt_project(
    root: Path,
    *,
    client_id: int | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    cfg = load_config(root)
    if not cfg:
        raise StellarError("No .devflow.yml found. Run `devflow /nuevo-proyecto` first.")
    project = cfg.get("project", {})
    ownership = project.get("ownership") or "internal"
    resolved_client = client_id if client_id is not None else project.get("client_id")
    if ownership == "external_client" and not resolved_client:
        raise StellarError("External-client adoption requires --client-id or project.client_id.")

    result = call_tool(
        root,
        "create_project",
        {
            "title": project.get("name") or root.name,
            "description": description or f"Adopted by DevFlow ({project.get('engagement', 'greenfield')}).",
            **({"client_id": int(resolved_client)} if resolved_client else {}),
            "status": "pending",
            "project_type": project.get("type") or "unknown",
        },
        require_project=False,
        allow_disabled=True,
    )
    remote = result.get("project") or {}
    project_id = remote.get("id") or result.get("project_id")
    if not project_id:
        raise StellarError(f"create_project did not return a project id: {result}")
    bind_project(root, int(project_id))
    return {"project_id": int(project_id), "project": remote}


def discovery_sync_plan(tool_names: list[str] | set[str]) -> dict[str, Any]:
    matrix = capability_matrix(tool_names)
    return {
        "matrix": matrix,
        "native": sorted(k for k, v in matrix.items() if v["state"] == "native"),
        "bridge": sorted(k for k, v in matrix.items() if v["state"] == "bridge"),
        "missing": sorted(k for k, v in matrix.items() if v["state"] == "missing"),
    }


def sync_discovery(root: Path, snapshot: dict[str, Any], *, dry_run: bool = False) -> dict[str, Any]:
    tools = list_tools(root, require_project=True)
    plan = discovery_sync_plan(tools)
    stellar = stellar_config(root)
    project_id = int(stellar["project_id"])

    if dry_run:
        return {"status": "dry_run", "project_id": project_id, **plan}

    if "sync_discovery_bundle" in tools:
        payload = {
            "project_id": project_id,
            "schema_version": snapshot.get("schema_version", 1),
            "discovery": snapshot,
        }
        result = call_tool(root, "sync_discovery_bundle", payload)
        return {"status": "synced", "project_id": project_id, "transport": "structured_bundle", "result": result, **plan}

    if "add_project_evidence" not in tools:
        return {
            "status": "pending",
            "project_id": project_id,
            "reason": "StellarCode MCP has no discovery bundle tool or evidence bridge.",
            **plan,
        }

    audit = snapshot.get("audit_summary") or {}
    project = snapshot.get("project") or {}
    stack = snapshot.get("stack_components") or []
    stack_text = ", ".join(f"{x.get('category')}={x.get('technology')}" for x in stack) or "none detected"
    note = "\n".join([
        "DevFlow discovery compatibility snapshot",
        f"ownership={project.get('ownership')}",
        f"engagement={project.get('engagement')}",
        f"revision={(snapshot.get('repository') or {}).get('revision')}",
        f"stack={stack_text}",
        f"technical_health={audit.get('project_health_score')}",
        f"stack_fit={audit.get('stack_fit_score')}",
        f"evidence_confidence={audit.get('evidence_confidence')}",
        f"findings={audit.get('finding_count')}",
        "Structured discovery/stack/audit sync is pending MCP v3 capabilities.",
    ])
    result = call_tool(root, "add_project_evidence", {
        "project_id": project_id,
        "title": f"DevFlow Discovery — {snapshot.get('generated_at')}",
        "kind": "note",
        "note": note,
    })
    return {
        "status": "partial",
        "project_id": project_id,
        "transport": "evidence_bridge",
        "evidence_id": result.get("evidence_id"),
        "pending_domains": plan["bridge"] + plan["missing"],
        **plan,
    }
