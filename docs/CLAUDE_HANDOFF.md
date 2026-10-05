# Claude Development Handoff

This document is the recommended starting point when continuing DevFlow with Claude Code or another coding agent.

## Read order

Before implementing a release, read:

1. `DEVFLOW_ROADMAP.md`
2. `CLAUDE.md`
3. `docs/DOMAIN_MODEL.md`
4. `docs/FINDING_LIFECYCLE.md`
5. `docs/PROVIDER_CONTRACT.md`
6. `docs/SYNC_MODEL.md`
7. `docs/CONFIG_AND_VERSIONING.md`
8. `docs/QUALITY_GATES.md`
9. the relevant `skills/*/SKILL.md`
10. `ops/BACKLOG.md`

## Current baseline

DevFlow main is v0.5 foundations-level capability.

Already present:

- CLI core;
- static audit/scoring;
- doctor/docs/secrets;
- StellarCode MCP client;
- project binding;
- real-user identity/RBAC implemented server-side in StellarCode;
- Kanban/members/roles/decisions;
- remote-first planning;
- trace sync;
- automated CI.

Do not reimplement these under new names without a migration reason.

## Recommended release sequence

### v0.5 — Foundations ✅

Implemented:

- canonical domain types/schemas;
- finding lifecycle, fingerprinting and reconciliation;
- config schema plus `validate`;
- config migration framework;
- provider/capability abstraction and registry;
- sync conflict/idempotency/event model;
- policy/gate engine;
- user/service-account-ready principal model;
- machine-readable schemas and tests.

Do not rebuild these under alternate abstractions unless a migration is explicitly designed.

### v0.6 — Analyzers ← next

Implement plugin/registry architecture and high-value analyzers first:

- FastAPI/Python;
- Node/Next/React;
- Angular;
- PostgreSQL;
- Docker;
- GitHub Actions.

Then:

- Go;
- Quarkus;
- PHP;
- MariaDB/SQLite;
- Kubernetes/k3s.

Every finding must emit the canonical Finding contract with stable fingerprint.

### v0.7 — GitHub / CI / PR

Implement provider integration:

- repository state;
- PR create/read/review;
- CI/check status;
- evidence ingestion;
- task/PR linking;
- release metadata.

### v0.8 — Release / Deploy

Implement provider-neutral:

- release;
- deployment;
- rollback;
- preflight;
- migration awareness;
- post-deploy smoke checks.

No production write may bypass approval policy.

### v0.9 — Runtime / Observability / OAuth

Implement:

- k6;
- Grafana/Prometheus;
- Sentry;
- Docker/k3s/Kubernetes state;
- Cloudflare;
- OAuth 2.1 interactive flow;
- scoped automation identities.

### v1.0 — End-to-end stable flow

Target:

```text
detect
→ audit
→ finding lifecycle
→ plan
→ StellarCode work item
→ implement
→ test
→ PR
→ CI
→ release
→ deploy
→ verify
→ evidence
→ close
```

## Development rules

- Work in a feature branch.
- Keep commits coherent.
- Add or adjust tests with behavior.
- Update `DEVFLOW_ROADMAP.md` when a capability status changes.
- Update `IMPLEMENTATION_STATUS.md` for the short current-state view.
- Update `CHANGELOG.md` for release-facing changes.
- Update specialized docs when contracts change.
- Do not mark a capability implemented because a skill exists.
- Do not fabricate CI/runtime/deployment evidence.
- Keep provider-specific code behind adapters/contracts.
- Never store credentials in YAML or Markdown.
- Avoid destructive migrations without explicit approval.
- Never deploy production just because implementation is complete.

## Release checklist

For each version:

1. Scope matches roadmap.
2. Contracts are documented before or with implementation.
3. Tests pass.
4. CLI help/docs match behavior.
5. No stale version labels remain.
6. No secrets are committed.
7. Backward compatibility and migrations are considered.
8. Findings/provider outputs are versioned if their schema changes.
9. PR describes implemented vs intentionally deferred work.
10. Production rollout is separate from code merge unless explicitly requested.

## Definition of done for agent work

A task is not done until:

- code exists;
- tests cover expected behavior;
- errors are handled;
- docs are updated;
- no security boundary was moved client-side;
- evidence is available;
- remaining limitations are explicit.

## What not to build yet

Unless required by the active release:

- a large web dashboard;
- plugin marketplace;
- AI prediction layer;
- broad cloud cost engine;
- mass auto-fix;
- dozens of low-value providers;
- microservice decomposition.

Prefer completing the end-to-end engineering loop first.
