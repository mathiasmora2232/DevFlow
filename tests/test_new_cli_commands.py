from pathlib import Path

from devflow.cli import main


def test_docs_and_secrets_cli_create_reports(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo\nSetup and testing.\n" * 20, encoding="utf-8")
    assert main(["/docs", "--target", str(tmp_path)]) == 0
    assert (tmp_path / "ops" / "reports" / "docs-latest.json").exists()
    assert main(["/secretos", "--target", str(tmp_path)]) == 0
    assert (tmp_path / "ops" / "reports" / "secrets-latest.json").exists()
