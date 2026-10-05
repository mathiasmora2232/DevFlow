from devflow.stellar import capability_matrix, discovery_sync_plan


def test_capability_matrix_reuses_existing_stellar_v2_surface():
    tools = {
        "create_project", "get_project",
        "list_project_tasks", "create_roadmap_task", "update_task",
        "get_project_plan", "create_project_phase",
        "add_project_evidence", "add_project_risk",
        "list_project_decisions", "add_project_decision",
    }
    matrix = capability_matrix(tools)
    assert matrix["project"]["state"] == "native"
    assert matrix["kanban"]["state"] == "native"
    assert matrix["phases"]["state"] == "native"
    assert matrix["discovery"]["state"] == "bridge"
    assert matrix["audits"]["state"] == "bridge"
    assert matrix["time_tracking"]["state"] == "missing"


def test_v3_capabilities_upgrade_bridge_to_native():
    tools = {
        "create_project", "get_project", "add_project_evidence",
        "sync_discovery_bundle", "sync_stack", "sync_audit_bundle", "sync_infrastructure",
        "start_time", "stop_time", "create_time_entry", "list_time_entries",
    }
    plan = discovery_sync_plan(tools)
    assert "discovery" in plan["native"]
    assert "stack" in plan["native"]
    assert "audits" in plan["native"]
    assert "infrastructure" in plan["native"]
    assert "time_tracking" in plan["native"]
