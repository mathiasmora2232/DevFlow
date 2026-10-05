from pathlib import Path

from devflow.findings import (
    normalize_legacy_finding,
    reconcile_findings,
    save_findings,
    stable_fingerprint,
    update_finding_status,
)


def test_fingerprint_is_stable_and_line_independent():
    one = stable_fingerprint("a", "rule", "repo", "file.py|symbol", "file.py")
    two = stable_fingerprint("a", "rule", "repo", "file.py|symbol", "file.py")
    assert one == two


def test_legacy_finding_normalization_ignores_dynamic_counts_in_rule():
    a = normalize_legacy_finding(
        {"category": "code_quality", "severity": "low", "message": "Se detectaron 21 marcadores TODO.", "evidence": "repository search"},
        "demo",
    )
    b = normalize_legacy_finding(
        {"category": "code_quality", "severity": "low", "message": "Se detectaron 24 marcadores TODO.", "evidence": "repository search"},
        "demo",
    )
    assert a["fingerprint"] == b["fingerprint"]


def test_reconcile_marks_missing_active_finding_fixed():
    current = normalize_legacy_finding(
        {"category": "security", "severity": "high", "message": "Bad thing", "evidence": "app.py"},
        "demo",
    )
    merged, stats = reconcile_findings([current], [])
    assert merged[0]["status"] == "fixed"
    assert stats["fixed"] == 1


def test_reconcile_reopens_closed_finding_as_regression():
    finding = normalize_legacy_finding(
        {"category": "security", "severity": "high", "message": "Bad thing", "evidence": "app.py"},
        "demo",
    )
    finding["status"] = "closed"
    current = normalize_legacy_finding(
        {"category": "security", "severity": "high", "message": "Bad thing", "evidence": "app.py"},
        "demo",
    )
    merged, stats = reconcile_findings([finding], [current])
    assert merged[0]["status"] == "open"
    assert merged[0]["regressed"] is True
    assert stats["regressed"] == 1


def test_update_finding_status_persists_waiver(tmp_path: Path):
    finding = normalize_legacy_finding(
        {"category": "security", "severity": "low", "message": "Known issue", "evidence": "app.py"},
        "demo",
    )
    save_findings(tmp_path, [finding])
    updated = update_finding_status(tmp_path, finding["id"], "accepted_risk", "temporary", "Mathias", "2026-12-01")
    assert updated["waiver"]["reason"] == "temporary"
    assert updated["status"] == "accepted_risk"


def test_reconcile_reopens_fixed_finding_as_regression():
    finding = normalize_legacy_finding(
        {"category": "security", "severity": "high", "message": "Bad thing", "evidence": "app.py"},
        "demo",
    )
    finding["status"] = "fixed"
    current = normalize_legacy_finding(
        {"category": "security", "severity": "high", "message": "Bad thing", "evidence": "app.py"},
        "demo",
    )
    merged, stats = reconcile_findings([finding], [current])
    assert merged[0]["status"] == "open"
    assert merged[0]["regressed"] is True
    assert stats["regressed"] == 1
