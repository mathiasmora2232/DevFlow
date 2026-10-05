from devflow.domain import Finding, Principal


def test_domain_finding_serializes():
    finding = Finding(
        id="FND-X",
        fingerprint="abc",
        project_id="demo",
        category="security",
        rule_id="SEC-1",
        severity="high",
        confidence=90,
        status="open",
        title="Demo",
        description="Demo finding",
    )
    data = finding.to_dict()
    assert data["fingerprint"] == "abc"
    assert data["status"] == "open"


def test_principal_supports_service_account():
    principal = Principal("service_account", "ci-bot", permissions=["ci.status.read"])
    assert principal.to_dict()["principal_type"] == "service_account"
