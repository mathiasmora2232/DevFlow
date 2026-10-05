from __future__ import annotations

import hashlib
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Iterable

SKIP_DIRS = {
    ".git", ".idea", ".vscode", "node_modules", "vendor", "dist", "build",
    ".next", ".nuxt", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", "coverage", ".coverage", "target", "bin", "obj",
}
TEXT_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".php", ".html",
    ".css", ".scss", ".md", ".yml", ".yaml", ".json", ".toml", ".xml",
    ".env", ".txt", ".sql", ".sh", ".properties", ".conf", ".pem", ".key",
}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def today_compact() -> str:
    return datetime.now().astimezone().strftime("%Y%m%d")


def safe_run(args: list[str], cwd: Path, timeout: int = 20) -> tuple[int, str]:
    try:
        cp = subprocess.run(
            args, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, check=False
        )
        output = (cp.stdout or "") + (cp.stderr or "")
        return cp.returncode, output.strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, str(exc)


def git_info(root: Path) -> dict:
    info = {"branch": "unknown", "revision": "unknown", "dirty": None}
    rc, out = safe_run(["git", "rev-parse", "--is-inside-work-tree"], root)
    if rc != 0 or out.strip() != "true":
        return info
    rc, out = safe_run(["git", "branch", "--show-current"], root)
    if rc == 0 and out:
        info["branch"] = out.strip()
    rc, out = safe_run(["git", "rev-parse", "--short", "HEAD"], root)
    if rc == 0 and out:
        info["revision"] = out.strip()
    rc, out = safe_run(["git", "status", "--porcelain"], root)
    if rc == 0:
        info["dirty"] = bool(out.strip())
    return info


def iter_project_files(root: Path, max_file_bytes: int = 1_000_000) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".terraform")]
        base = Path(current)
        for name in files:
            p = base / name
            try:
                if p.stat().st_size > max_file_bytes:
                    continue
            except OSError:
                continue
            if p.suffix.lower() in TEXT_SUFFIXES or name.startswith(".env") or name in {
                "Dockerfile", "Makefile", "Procfile", "requirements.txt", "go.mod",
                "package.json", "composer.json", "pom.xml", "gradlew", "mvnw",
            }:
                yield p


def read_text(path: Path, limit: int = 1_000_000) -> str:
    try:
        data = path.read_bytes()[:limit]
        return data.decode("utf-8", errors="ignore")
    except OSError:
        return ""


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9áéíóúñ]+", "-", value)
    value = value.strip("-")
    replacements = str.maketrans("áéíóúñ", "aeioun")
    return value.translate(replacements) or "project"


def stable_hash(values: list[str]) -> str:
    raw = "\n".join(values).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12]


def replace_markdown_field(text: str, label: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^- {re.escape(label)}:\s*.*$")
    line = f"- {label}: {value}"
    if pattern.search(text):
        return pattern.sub(line, text, count=1)
    return text
