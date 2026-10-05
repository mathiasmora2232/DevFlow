# Configuration, Schema and Compatibility

DevFlow configuration is an API. It must evolve without silently breaking existing projects.

## Current state

Early configs use:

```yaml
version: 1
```

Future development must formalize this as a schema version rather than treating YAML shape as implicit.

## Target format

```yaml
schema_version: 2

project:
  ...

profile: mvp

providers:
  ...

gates:
  ...

stellarcode:
  ...
```

## Required commands

Target for the next foundation release:

```bash
devflow validate
devflow config migrate
devflow config show
```

### validate

Checks:

- schema version;
- required fields;
- unknown/deprecated keys;
- value types;
- incompatible options;
- provider references;
- approval/gate configuration.

It must not mutate the file.

### config migrate

- reads old version;
- produces deterministic migration;
- preserves unknown safe metadata when possible;
- creates backup/diff;
- never migrates credentials into config;
- supports `--check` before mutation.

## Compatibility policy

Before v1.0:

- breaking changes are allowed only with migration support;
- one previous schema version should remain readable where feasible;
- CLI deprecations should warn before removal.

At v1.0:

- config schema has explicit compatibility policy;
- provider contracts are versioned;
- StellarCode MCP contract has a declared version;
- reports/findings include schema/version metadata.

## Report versioning

JSON outputs should eventually include:

```json
{
  "schema": "devflow.audit",
  "schema_version": 1,
  "devflow_version": "0.x.y"
}
```

The same principle applies to findings, sync results and provider evidence.

## MCP compatibility

DevFlow must not assume one StellarCode tool response shape forever.

Maintain:

- MCP server version;
- capability discovery;
- optional feature checks;
- backwards-compatible fields when practical.

If a capability is unavailable, report `UNSUPPORTED_CAPABILITY` rather than guessing.
