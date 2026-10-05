from pathlib import Path

import yaml

from devflow.config_schema import migrate_config, migrate_config_file, validate_config


def legacy_config():
    return {
        "version": 1,
        "project": {
            "name": "Demo",
            "slug": "demo",
            "stage": "mvp",
            "criticality": "medium",
        },
        "stellarcode": {"enabled": False},
    }


def test_migrate_v1_to_v3():
    migrated = migrate_config(legacy_config())
    assert migrated["schema_version"] == 3
    assert "version" not in migrated
    assert migrated["profile"] == "mvp"
    assert migrated["providers"] == {}
    assert migrated["gates"] == {}\n    assert migrated["project"]["ownership"] == "internal"\n    assert migrated["project"]["engagement"] == "greenfield"\n

def test_validation_rejects_raw_stellar_token():
    cfg = migrate_config(legacy_config())
    cfg["stellarcode"] = {
        "enabled": True,
        "mcp_url": "https://example.test/mcp",
        "auth": {"mode": "bearer", "token": "dont-store-me", "token_env": "TOKEN"},
    }
    errors = validate_config(cfg)
    assert any(e["path"] == "stellarcode.auth.token" for e in errors)


def test_migration_check_does_not_modify_file(tmp_path: Path):
    path = tmp_path / ".devflow.yml"
    path.write_text(yaml.safe_dump(legacy_config()), encoding="utf-8")
    before = path.read_text(encoding="utf-8")
    result = migrate_config_file(tmp_path, check=True)
    assert result["changed"] is True
    assert path.read_text(encoding="utf-8") == before


def test_migration_writes_backup(tmp_path: Path):
    path = tmp_path / ".devflow.yml"
    path.write_text(yaml.safe_dump(legacy_config()), encoding="utf-8")
    migrate_config_file(tmp_path)
    assert (tmp_path / ".devflow.yml.v1.bak").exists()
    assert yaml.safe_load(path.read_text(encoding="utf-8"))["schema_version"] == 3


def test_validation_rejects_invalid_engagement():
    cfg = migrate_config(legacy_config())
    cfg["project"]["engagement"] = "rewrite_everything"
    errors = validate_config(cfg)
    assert any(e["path"] == "project.engagement" for e in errors)
