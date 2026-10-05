from pathlib import Path
from devflow.detector import detect_stack


def test_detect_fastapi_postgres_docker(tmp_path: Path):
    (tmp_path / "requirements.txt").write_text("fastapi\npsycopg[binary]\n", encoding="utf-8")
    (tmp_path / "Dockerfile").write_text("FROM python:3.12", encoding="utf-8")
    got = detect_stack(tmp_path)
    assert got["backend"] == "fastapi"
    assert got["database"] == "postgresql"
    assert "docker" in got["infra"]

def test_documentation_mentions_do_not_define_runtime_stack(tmp_path: Path):
    (tmp_path / "README.md").write_text(
        "Future ideas: PostgreSQL, k3s, Kubernetes, Grafana, Sentry, k6, FastAPI.",
        encoding="utf-8",
    )
    got = detect_stack(tmp_path)
    assert got["backend"] == "none"
    assert got["database"] == "none"
    assert got["infra"] == []
    assert got["observability"] == []
