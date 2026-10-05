from devflow.gates import evaluate_gate


def config(profile="production"):
    return {
        "schema_version": 2,
        "profile": profile,
        "project": {"name": "Demo", "slug": "demo", "stage": "production", "criticality": "high"},
    }


def audit(health=90, findings=None):
    return {"project_health_score": health, "findings": findings or []}


def test_production_gate_passes_with_required_evidence():
    result = evaluate_gate(
        "production",
        config(),
        audit(),
        {"tests": True, "build": True, "rollback": True, "healthcheck": True, "verified_ci": True},
    )
    assert result.result == "pass"


def test_production_gate_is_unknown_when_evidence_missing():
    result = evaluate_gate("production", config(), audit(), {})
    assert result.result == "unknown"
    assert "tests" in result.missing_evidence


def test_gate_blocks_open_critical_security():
    findings = [{"category": "security", "severity": "critical", "status": "open"}]
    result = evaluate_gate(
        "production",
        config(),
        audit(findings=findings),
        {"tests": True, "build": True, "rollback": True, "healthcheck": True, "verified_ci": True},
    )
    assert result.result == "blocked"


def test_closed_security_finding_does_not_block():
    findings = [{"category": "security", "severity": "critical", "status": "closed"}]
    result = evaluate_gate(
        "production",
        config(),
        audit(findings=findings),
        {"tests": True, "build": True, "rollback": True, "healthcheck": True, "verified_ci": True},
    )
    assert result.result == "pass"
