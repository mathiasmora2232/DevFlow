from pathlib import Path

from devflow.sync import Event, IdempotencyStore, detect_conflict


def test_conflict_uses_declared_authority():
    conflict = detect_conflict("status", "in_progress", "review", "stellarcode")
    assert conflict is not None
    assert conflict.authority == "stellarcode"
    assert conflict.recommended_resolution == "use_stellarcode"


def test_same_value_has_no_conflict():
    assert detect_conflict("status", "review", "review", "stellarcode") is None


def test_idempotency_store_rejects_duplicate(tmp_path: Path):
    store = IdempotencyStore(tmp_path)
    assert store.register("evt-1", {"provider": "github"}) is True
    assert store.register("evt-1", {"provider": "github"}) is False
    assert store.seen("evt-1") is True


def test_event_payload_hash_is_deterministic():
    one = Event.from_payload(
        event_id="evt-1",
        provider="github",
        event_type="pull_request",
        project_id="demo",
        resource_type="pr",
        resource_id="12",
        occurred_at="2026-10-04T00:00:00Z",
        payload={"b": 2, "a": 1},
    )
    two = Event.from_payload(
        event_id="evt-1",
        provider="github",
        event_type="pull_request",
        project_id="demo",
        resource_type="pr",
        resource_id="12",
        occurred_at="2026-10-04T00:00:00Z",
        payload={"a": 1, "b": 2},
    )
    assert one.payload_hash == two.payload_hash
