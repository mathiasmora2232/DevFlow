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


def stellar_config(root: Path, require_project: bool = True) -> dict[str, Any]:
    cfg = load_config(root)
    stellar = cfg.get("stellarcode", {}) if cfg else {}
    if not stellar.get("enabled"):
        raise StellarError("StellarCode integration is disabled. Run `devflow stellar-bind --project-id <id>`.")
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


def call_tool(root: Path, tool: str, arguments: dict[str, Any] | None = None, require_project: bool = True) -> dict[str, Any]:
    stellar = stellar_config(root, require_project=require_project)
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
