from pathlib import Path

from devflow.secrets_scan import scan_secrets, secrets_markdown, should_fail


def test_secret_scan_redacts_detected_token(tmp_path: Path):
    token = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    (tmp_path / "app.py").write_text(f'TOKEN = "{token}"\n', encoding="utf-8")
    result = scan_secrets(tmp_path)
    assert result["counts"]["critical"] >= 1
    report = secrets_markdown(result)
    assert token not in report
    assert should_fail(result, "critical") is True
