# Sync, Conflict and Idempotency Model

> Implemented in DevFlow v0.5. This document remains the canonical behavioral contract.

DevFlow spans local files, Git and StellarCode. Synchronization must be explicit and deterministic.

## Source authority by domain

| Domain | Authority |
|---|---|
| Source code | Git |
| Commit / branch / PR state | Git provider |
| Work item / Kanban status | StellarCode |
| Project members / roles | StellarCode |
| Local audit reports | DevFlow |
| Finding identity/history | DevFlow canonical model; optionally mirrored remotely |
| Runtime health | runtime provider |
| Deploy state | deployment provider |
| Local config | `.devflow.yml` |

## Remote-first backlog

For a StellarCode-enabled project:

```text
request to create work
  ↓
create remote WorkItem
  ↓
remote success
  ↓
persist external reference locally
  ↓
trace
```

If remote creation fails, do not pretend the task exists locally as synchronized work.

## Conflict example

```text
ops/TRACE.md:       in_progress
StellarCode:        review
GitHub PR:          merged
Production:         old release
```

Interpretation:

- task status authority → StellarCode says `review`;
- integration evidence → GitHub says merged;
- deployment authority → production provider says not deployed;
- local trace is stale and should be reconciled.

Do not collapse these into one status.

## Sync result

Every sync should conceptually produce:

```text
status:
  clean | changed | conflict | partial | failed

changes[]
conflicts[]
evidence[]
source_versions{}
timestamp
```

## Conflict handling

A conflict must state:

```text
field
local_value
remote_value
authority
recommended_resolution
```

Automatic resolution is allowed only when authority is unambiguous and the action is non-destructive.

## Idempotency

All write-capable integrations should support an idempotency identity.

Preferred keys:

```text
request_id
event_id
operation_id
external_ref
```

Examples include a webhook delivery ID, CI run ID, MCP request ID, DevFlow work ID or deployment ID.

Repeating the same event must not create duplicate evidence, tasks or decisions.

## Event model

Future event ingestion should normalize:

```text
event_id
provider
event_type
project_id
resource_type
resource_id
occurred_at
received_at
payload_hash
evidence
```

## Sync safety

- reads may run automatically;
- reversible shared writes follow project policy;
- consequential sync actions require approval;
- audit scans do not auto-create backlog by default;
- conflicts never get silently overwritten;
- credential material must not enter sync metadata.

## Offline behavior

DevFlow core must remain useful without StellarCode:

- audit;
- score;
- doctor;
- docs;
- secrets;
- local trace;
- local plan.

Remote-dependent commands must fail clearly, never fabricate success.


## v0.5 implementation

Implemented in `devflow.sync`:

- source authority map;
- SyncConflict / SyncResult;
- deterministic conflict detection;
- local IdempotencyStore;
- normalized Event model with deterministic payload hashing.

Provider-specific event ingestion and remote conflict resolution remain future work.
