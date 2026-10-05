from pathlib import Path

import yaml

from devflow.stellar import bind_project, choose_next_task


def test_bind_project_does_not_store_token(tmp_path: Path):
    (tmp_path / ".devflow.yml").write_text(
        yaml.safe_dump({"version": 1, "project": {"name": "Demo"}}),
        encoding="utf-8",
    )
    bind_project(tmp_path, 42)
    cfg = yaml.safe_load((tmp_path / ".devflow.yml").read_text(encoding="utf-8"))
    assert cfg["stellarcode"]["project_id"] == 42
    assert cfg["stellarcode"]["auth"]["token_env"] == "STELLARCODE_TOKEN"
    assert "token" not in cfg["stellarcode"]["auth"]


def test_choose_next_task_prefers_in_progress_then_priority():
    tasks = [
        {"id": 1, "status": "pending", "priority": "critical"},
        {"id": 2, "status": "in_progress", "priority": "medium"},
        {"id": 3, "status": "in_progress", "priority": "high"},
        {"id": 4, "status": "blocked", "priority": "critical"},
    ]
    assert choose_next_task(tasks)["id"] == 3
