from pathlib import Path

from devflow.doctor import doctor_project


def test_doctor_reports_disk_and_python(tmp_path: Path):
    result = doctor_project(tmp_path)
    assert 0 <= result["readiness_score"] <= 100
    assert result["free_disk_gb"] >= 0
    names = {c["name"] for c in result["checks"]}
    assert "python" in names
    assert "disk_space" in names
