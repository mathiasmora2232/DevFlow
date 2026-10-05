from pathlib import Path
from devflow.trace import ensure_ops, next_work_id, add_work


def test_work_ids_increment(tmp_path: Path):
    ensure_ops(tmp_path)
    first = next_work_id(tmp_path, "DEV")
    add_work(tmp_path, first, "One", "feature", "medium", "One", [])
    second = next_work_id(tmp_path, "DEV")
    assert first != second
    assert second.endswith("002")
