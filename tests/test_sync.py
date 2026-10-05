from pathlib import Path

from devflow.sync import IdempotencyStore, detect_conflict


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
