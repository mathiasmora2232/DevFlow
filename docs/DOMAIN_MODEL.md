# DevFlow Domain Model

> Implemented in DevFlow v0.5. This document remains the canonical behavioral contract.

> Canonical conceptual model for DevFlow. This document defines names, identities and ownership boundaries before implementation details.

## Core entities

### Project

Represents one product/system/business initiative. A project can own one or many repositories.

Required conceptual fields:

```text
id
slug
name
stage
criticality
profile
status
repositories[]
environments[]
members[]
```

A Project is **not** the same thing as a Git repository.

### Repository

Technical source attached to a project.

```text
id
project_id
provider
owner
name
default_branch
local_path?
remote_url?
role
```

Examples of `role`:

```text
frontend
backend
admin
mobile
infra
worker
monorepo
other
```

### WorkItem

Canonical unit of planned work.

```text
id
external_id?
project_id
title
description
type
priority
status
owner?
acceptance_criteria[]
dependencies[]
evidence[]
source
created_at
updated_at
```

Canonical statuses:

```text
backlog
ready
in_progress
validation
review
deployed
verified
closed
blocked
cancelled
```

Provider-specific statuses must map into these values instead of leaking throughout the core.

### Finding

A technical issue discovered by an analyzer, provider or human review.

```text
id
fingerprint
project_id
repository_id?
category
rule_id
severity
confidence
status
title
description
evidence[]
location?
recommendation?
first_seen_at
last_seen_at
resolved_at?
source
```

Finding lifecycle is defined in `docs/FINDING_LIFECYCLE.md`.

### Evidence

A fact supporting a state, claim, finding or transition.

```text
id
type
source
subject_type
subject_id
uri?
file?
line?
commit_sha?
timestamp
metadata
confidence
```

Examples:

- Git commit;
- test result;
- CI check;
- analyzer match;
- deployment record;
- healthcheck;
- metric snapshot;
- screenshot/manual verification;
- MCP activity entry.

Evidence must not contain raw secrets.

### Decision

Architecture/product/operational decision.

```text
id
project_id
title
context
decision
consequences
status
created_by
created_at
supersedes?
```

Statuses:

```text
proposed
accepted
superseded
rejected
```

### Risk

```text
id
project_id
title
description
probability
impact
severity
status
owner?
mitigation?
evidence[]
```

### Release

```text
id
project_id
version
commit_sha
status
changes[]
artifacts[]
created_at
```

### Deployment

A release being applied to one environment.

```text
id
release_id
environment_id
provider
status
started_at
completed_at?
verification_status
rollback_reference?
evidence[]
```

Important:

```text
merged != deployed
deployed != verified
verified != closed
```

### Environment

```text
id
project_id
name
kind
criticality
provider_refs
```

Typical `kind`:

```text
local
development
staging
production
```

### Member / Principal

A human or service identity that acts through DevFlow/StellarCode.

```text
principal_type = user | service_account
principal_id
project_role
permissions[]
```

The MCP server is authoritative for project authorization.

### Provider

External system adapter. Contract defined in `docs/PROVIDER_CONTRACT.md`.

## Ownership boundaries

| Concept | Canonical owner |
|---|---|
| Source code / commits / branches | Git provider |
| Project operational state | StellarCode |
| DevFlow local config | `.devflow.yml` |
| Static reports | DevFlow local files |
| Runtime metrics | Runtime provider |
| Identity / project RBAC | StellarCode MCP |
| Secrets | Secret manager / environment, never DevFlow files |

## Stable identifiers

Never use titles as identities.

Recommended forms:

```text
DEV-YYYYMMDD-NNN      work item
FND-<rule>-<hash>     finding display ID
fingerprint           stable machine identity for a finding
ADR-NNNN              optional local decision reference
```

Remote IDs must be stored as references, not replace local/canonical identity automatically.

## Rule

Before adding a new DevFlow object type, determine whether it is:

1. a new domain entity;
2. a provider-specific representation of an existing entity;
3. evidence;
4. metadata.

Do not create duplicate concepts for provider convenience.
