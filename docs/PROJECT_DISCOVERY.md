# Project Discovery and Adoption Flow

DevFlow must treat project onboarding as a discovery workflow, not as a simple config wizard.

StellarCode Studio is the operational center of every project. DevFlow discovers, audits and structures information; StellarCode stores and exposes the shared project state through MCP.

## 1. First question: who owns the project?

Every project must be classified by ownership.

```text
project_owner_type:
  internal
  external_client
```

### internal

The project belongs to the operator/team itself.

Examples:
- SmartAhorra
- DevFlow
- internal tools

### external_client

The project belongs to a client.

Required additional information:

```text
client_id
client_name
commercial_context?
primary_contact?
```

Client identity lives in StellarCode, not in local DevFlow files when a canonical client record already exists.

## 2. Second question: what kind of work is this?

Every project must declare an engagement type.

```text
greenfield
migration
refactor
modernization
maintenance
audit_only
```

### greenfield

A genuinely new system.

Discovery focuses on:

- objectives;
- users;
- scope;
- constraints;
- architecture;
- stack selection;
- phases;
- environments;
- delivery plan.

### migration

An existing system moves technology, infrastructure or architecture.

Discovery focuses on:

- current system inventory;
- target system;
- data;
- contracts;
- authentication;
- integrations;
- dependencies;
- migration strategy;
- cutover;
- rollback.

### refactor / modernization

Existing code remains the product/system, but DevFlow/StellarCode treats it as a newly onboarded project.

Example: SmartISP.

Discovery focuses first on reality:

- repository inventory;
- current stack;
- architecture;
- dependencies;
- security;
- secrets/configuration;
- database;
- infrastructure;
- CI/CD;
- documentation;
- health/debt;
- runtime evidence if available.

Only after current-state discovery should the target architecture or modernization plan be defined.

### maintenance

Existing system with bounded ongoing work.

### audit_only

Assessment without assuming implementation ownership.

## 3. Project identity

Initial name resolution:

1. explicit user-provided name;
2. existing StellarCode project binding;
3. repository metadata;
4. root folder/repository name;
5. ask/correct only if ambiguity remains.

DevFlow may infer a proposed name, but the operator can correct it before remote creation.

## 4. Canonical onboarding modes

### Mode A — greenfield

```text
identify
→ classify owner/client
→ classify engagement=greenfield
→ define objectives
→ define scope
→ define constraints
→ propose stack
→ approve stack
→ create StellarCode project
→ define phases
→ seed backlog
→ create repo/config
→ start execution
```

### Mode B — existing system

```text
identify repo/project
→ classify owner/client
→ classify migration/refactor/modernization/maintenance
→ full discovery scan
→ detect real stack
→ detect architecture
→ audit security/secrets/config
→ audit DB/infra/CI/docs/tests
→ calculate health/fit/confidence
→ push discovery snapshot to StellarCode
→ define objectives/target state
→ define phases
→ propose backlog
→ approve work
```

The existing codebase is the evidence. Do not ask the user to manually describe information that can be discovered reliably.

## 5. Initial discovery sweep

For an existing system, the initial sweep should collect as much reliable project context as possible.

### Repository

- remote/provider;
- default branch;
- languages;
- frameworks;
- package managers;
- lock files;
- monorepo/workspace layout;
- application entrypoints;
- test layout.

### Stack

- backend;
- frontend;
- database;
- cache;
- queues;
- storage;
- auth;
- build tooling;
- reverse proxy;
- containers;
- orchestration;
- CI/CD;
- monitoring/observability.

The detected stack must be synchronized to StellarCode as structured data, not only embedded in an audit Markdown file.

## 6. Initial audit bundle

The onboarding sweep should orchestrate the relevant audits automatically.

Minimum bundle for an existing repository:

```text
doctor
stack detection
security
secret hygiene
environment/config inventory
dependencies
architecture
code quality
testing
database
DevOps/CI
documentation
observability
resilience
SEO/accessibility when applicable
performance static evidence
runtime evidence when connected
```

Each auditor must emit:

- canonical findings;
- evidence;
- score/category status where applicable;
- confidence;
- unknown/missing evidence;
- sync payload for StellarCode.

## 7. Environment/config inventory

DevFlow must identify configuration surfaces without exposing secret values.

Examples:

- .env files;
- env examples;
- process environment names;
- Docker/Compose variables;
- CI variables references;
- Kubernetes Secrets/ConfigMaps references;
- Cloudflare bindings;
- database connection variable names;
- third-party integration variable names.

StellarCode should receive metadata such as:

```text
VARIABLE_NAME
scope/environment
required?
source
secret=true|false
configured=true|false|unknown
```

Never push the raw secret value.

## 8. Infrastructure discovery

When providers are available, DevFlow should map:

- environments;
- hosts/VPS;
- Docker services;
- Kubernetes/k3s clusters;
- Cloudflare zones/tunnels/workers;
- databases;
- storage;
- CI/CD;
- observability providers;
- deployment paths;
- health endpoints.

Without runtime/provider evidence, fields remain unknown instead of inferred.

## 9. StellarCode synchronization

StellarCode is mandatory for managed projects.

The initial onboarding should create/update:

```text
Project
Client / internal ownership
Repositories
Engagement type
Detected stack
Architecture summary
Environments
Infrastructure inventory
Configuration-variable inventory
Scores
Findings
Risks
Decisions
Phases
Objectives
Backlog proposals
Evidence
Audit snapshots
Time-tracking policy
```

The MCP is the canonical transport for these operations.

## 10. Discovery snapshot

Each full onboarding/re-discovery should create a versioned snapshot:

```text
discovery_id
project_id
repository revisions
started_at
completed_at
DevFlow version
detected stack
environment inventory
infra inventory
audit summary
findings summary
scores
missing evidence
```

This enables future comparisons after migrations/refactors.

## 11. Phases and objectives

Phases are not identical for every engagement.

### Greenfield example

```text
Discovery
Foundation
MVP
Validation
Production
Growth
```

### Refactor example

```text
Discovery / Baseline
Stabilization
Security & Debt
Architecture Refactor
Migration slices
Validation
Production hardening
```

### Migration example

```text
Current-state inventory
Target architecture
Compatibility
Migration preparation
Parallel run
Cutover
Verification
Decommission
```

DevFlow should propose phases based on engagement type, but StellarCode stores the approved phase plan.

## 12. Backlog generation

Audits may propose backlog items, but creation remains controlled.

```text
findings
→ group/deduplicate
→ prioritize
→ propose work
→ approve
→ create StellarCode tasks
```

A single work item may resolve multiple findings.

## 13. Re-discovery

Discovery is not one-time.

Run again after meaningful events:

- major refactor;
- migration;
- provider change;
- new repository;
- environment change;
- production launch;
- major incident.

The new snapshot must be comparable with the previous one.
