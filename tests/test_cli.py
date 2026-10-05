from pathlib import Path
from devflow.cli import main


def test_init_non_interactive(tmp_path: Path):
    rc = main(["/nuevo-proyecto", "--target", str(tmp_path), "--non-interactive", "--name", "Demo", "--backend", "fastapi", "--database", "postgresql"])
    assert rc == 0
    assert (tmp_path / ".devflow.yml").exists()
    assert (tmp_path / "ops" / "TRACE.md").exists()


def test_audit_after_init(tmp_path: Path):
    (tmp_path / "requirements.txt").write_text("fastapi\npsycopg\n", encoding="utf-8")
    assert main(["init", "--target", str(tmp_path), "--non-interactive", "--name", "Demo"]) == 0
    assert main(["audit", "--target", str(tmp_path)]) == 0
    assert (tmp_path / "ops" / "reports" / "latest.json").exists()
