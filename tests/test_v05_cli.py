from pathlib import Path

import yaml

from devflow.cli import main


def test_validate_and_config_migrate_cli(tmp_path: Path):
    legacy = {
        "version": 1,
        "project": {"name": "Demo", "slug": "demo", "stage": "mvp", "criticality": "medium"},
    }
    (tmp_path / ".devflow.yml").write_text(yaml.safe_dump(legacy), encoding="utf-8")
    assert main(["validate", "--target", str(tmp_path)]) == 0
    assert main(["config", "migrate", "--target", str(tmp_path), "--check"]) == 0
    assert main(["config", "migrate", "--target", str(tmp_path)]) == 0
    assert main(["validate", "--target", str(tmp_path)]) == 0


def test_findings_cli_after_audit(tmp_path: Path):
    (tmp_path / "requirements.txt").write_text("fastapi\n", encoding="utf-8")
    (tmp_path / "app.py").write_text('password = "this-is-a-long-demo-secret"\n', encoding="utf-8")
    assert main(["init", "--target", str(tmp_path), "--non-interactive", "--name", "Demo"]) == 0
    assert main(["audit", "--target", str(tmp_path)]) == 0
    assert (tmp_path / "ops" / "findings.json").exists()
    assert main(["findings", "list", "--target", str(tmp_path)]) == 0


def test_gate_cli_reports_unknown_without_runtime_evidence(tmp_path: Path):
    assert main(["init", "--target", str(tmp_path), "--non-interactive", "--name", "Demo", "--stage", "production"]) == 0
    assert main(["audit", "--target", str(tmp_path)]) == 0
    assert main(["gate", "production", "--target", str(tmp_path)]) == 8
