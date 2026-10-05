# StellarCode Hub Contract

StellarCode Studio is the mandatory operational hub for DevFlow-managed projects.

DevFlow can continue to perform local analysis offline, but a project is not considered fully managed/synchronized until it is bound to StellarCode MCP.

## 1. Responsibility split

### DevFlow

- discover;
- analyze;
- score;
- normalize;
- plan;
- validate;
- orchestrate;
- produce evidence.

### StellarCode Studio

- canonical project registry;
- client ownership;
- project lifecycle;
- repositories;
- phases/objectives;
- backlog/Kanban;
- members/roles;
- findings mirror/index;
- audit snapshots;
- infrastructure inventory;
- stack inventory;
- environment/config metadata;
- risks;
- decisions;
- evidence;
- time tracking;
- activity/audit history.

### Git/providers

Remain authoritative for their own technical facts.

## 2. Mandatory synchronization families

All DevFlow auditors and discovery modules should support synchronization into StellarCode.

Capability families:

```text
project.*
client.*
repository.*
discovery.*
stack.*
architecture.*
environment.*
config.*
infra.*
audit.*
finding.*
score.*
risk.*
decision.*
phase.*
objective.*
task.*
evidence.*
time.*
```

## 3. Initial MCP capabilities target

Read:

```text
project.read
client.read
repository.read
discovery.read
stack.read
environment.read
config.read
infra.read
audit.read
finding.read
score.read
phase.read
objective.read
task.read
evidence.read
time.read
```

Write:

```text
project.create
project.update
client.link
repository.link
discovery.create
discovery.complete
stack.sync
architecture.sync
environment.sync
config.sync_metadata
infra.sync
audit.publish
finding.sync
score.publish
risk.create
decision.create
phase.manage
objective.manage
task.create
task.update
evidence.create
time.start
time.stop
time.create
time.correct
```

## 4. Audit synchronization

Every audit should be able to publish a normalized run.

```text
AuditRun
  id
  project_id
  repository_id?
  audit_type
  devflow_version
  started_at
  completed_at
  status
  score?
  confidence?
  findings[]
  evidence[]
  missing_evidence[]
```

Examples of audit_type:

```text
security
secrets
architecture
dependencies
database
devops
docs
seo
accessibility
performance
resilience
full
```

Markdown reports are secondary human-readable artifacts. Structured MCP data is the operational source.

## 5. Findings

DevFlow owns fingerprint/reconciliation logic.

StellarCode stores the synchronized operational representation:

```text
finding_id
fingerprint
rule_id
category
severity
confidence
status
repository
location
first_seen
last_seen
waiver
linked_work_items[]
```

Synchronization must be idempotent by fingerprint/project/repository.

## 6. Stack inventory

Stack detection should publish structured components.

```text
StackComponent
  category
  technology
  version?
  source
  evidence
  confidence
```

Examples:

```text
backend / fastapi
frontend / angular
database / postgresql
container / docker
ci / github-actions
edge / cloudflare
orchestration / k3s
monitoring / grafana
```

Do not store only a free-text stack description.

## 7. Configuration metadata

Only names and state, never secret values.

```text
ConfigVariable
  name
  environment
  required
  secret
  source
  configured
  last_observed_at
```

## 8. Infrastructure health

Infrastructure auditing should eventually publish resources and health observations.

```text
InfrastructureResource
  provider
  type
  external_id
  environment
  state
  health
  metadata
  observed_at
```

Examples:

- VPS;
- Docker service;
- pod/deployment;
- DB instance;
- tunnel;
- worker;
- bucket;
- queue;
- monitoring service.

Health observations require provider/runtime evidence.

## 9. Migration/refactor data

For existing systems StellarCode should preserve both:

```text
current_state
target_state
```

This prevents migration planning from overwriting the discovered reality.

Store:

- current stack;
- target stack;
- migration strategy;
- delta;
- risks;
- phases;
- cutover plan;
- rollback plan.

## 10. Project creation/adoption

The MCP should distinguish:

```text
ownership:
  internal
  external_client

engagement:
  greenfield
  migration
  refactor
  modernization
  maintenance
  audit_only
```

A repo that already exists may still be a new project **inside the Hub**.

## 11. Time tracking

Time tracking is mandatory for managed work and belongs operationally to StellarCode.

Every TimeSession/TimeEntry must link to:

- project;
- principal;
- work item when applicable;
- category;
- timestamps;
- billable flag;
- source;
- audit history.

Corrections are append/audit operations, not silent destructive edits.

## 12. Offline mode

DevFlow may run local audits without StellarCode availability.

In that case:

```text
sync_status = pending
```

When connectivity returns, structured results should be synchronized idempotently.

Offline mode must not be confused with a fully managed project state.

## 13. Rule

If a piece of information is important enough to influence planning, health, scope, permissions, time or delivery, it should have a structured StellarCode representation instead of living only in a Markdown report.
