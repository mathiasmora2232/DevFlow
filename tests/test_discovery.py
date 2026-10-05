from pathlib import Path

from devflow.cli import main
from devflow.discovery import config_metadata, discover_project, infer_engagement


def test_existing_repo_defaults_to_refactor(tmp_path: Path):
    (tmp_path / "package.json").write_text('{"dependencies":{"next":"16.0.0","express":"5.0.0"}}', encoding="utf-8")
    assert infer_engagement(tmp_path, {"backend": "nodejs", "frontend": "nextjs", "database": "none", "infra": []}) == "refactor"


def test_config_metadata_never_contains_values(tmp_path: Path):
    (tmp_path / ".env").write_text("DATABASE_URL=postgres://secret-user:secret-pass@db/demo\nPUBLIC_URL=https://example.test\n", encoding="utf-8")
    (tmp_path / "app.js").write_text("const token = process.env.BREVO_API_KEY;\n", encoding="utf-8")
    items = config_metadata(tmp_path)
    rendered = str(items)
    assert "DATABASE_URL" in rendered
    assert "BREVO_API_KEY" in rendered
    assert "secret-pass" not in rendered
    assert "postgres://" not in rendered


def test_discovery_writes_baseline(tmp_path: Path):
    (tmp_path / "requirements.txt").write_text("fastapi\n", encoding="utf-8")
    assert main(["init", "--target", str(tmp_path), "--non-interactive", "--name", "Demo", "--engagement", "refactor"]) == 0
    assert main(["discover", "--target", str(tmp_path), "--no-audit"]) == 0
    assert (tmp_path / "ops" / "discovery" / "latest.json").exists()
    snapshot = discover_project(tmp_path, run_audit=False)
    assert snapshot["project"]["engagement"] == "refactor"
    assert any(x["technology"] == "fastapi" for x in snapshot["stack_components"])
