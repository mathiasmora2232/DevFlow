from pathlib import Path

from devflow.docs_audit import audit_docs


def test_docs_audit_recognizes_core_docs(tmp_path: Path):
    (tmp_path / "README.md").write_text(
        "# Demo\n\nInstallation and setup instructions. Architecture modules. "
        "Environment variables use .env.example. Testing with pytest.\n" * 6,
        encoding="utf-8",
    )
    (tmp_path / ".env.example").write_text("DATABASE_URL=example\n", encoding="utf-8")
    result = audit_docs(tmp_path)
    assert result["documentation_score"] >= 60
    env = next(c for c in result["checks"] if c["id"] == "environment")
    assert env["passed"] is True
