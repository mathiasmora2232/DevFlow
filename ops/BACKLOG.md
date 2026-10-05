# Backlog

> Execution-oriented backlog. Global scope/version truth lives in `DEVFLOW_ROADMAP.md`.

## P0 — StellarCode v2 rollout

- Apply the database migration with an explicit backup/recovery plan.
- Roll out MCP v2 with writes initially disabled.
- Validate real-user identity.
- Validate owner/developer/viewer authorization.
- Validate denied actions.
- Inspect MCP audit entries.
- Enable writes after read/RBAC verification.
- Retire legacy shared-secret access after clients migrate.

## P1 — DevFlow v0.6 Analyzers

First wave:
- FastAPI/Python analyzer.
- Node/Next/React analyzer.
- Angular analyzer.
- PostgreSQL analyzer.
- Docker analyzer.
- GitHub Actions analyzer.
- Analyzer registry/plugin architecture.
- Canonical Finding output only.
- Stable fingerprints from every analyzer.
- Evidence/confidence per finding.
- False-positive regression fixtures.

Second wave:
- Go.
- Quarkus.
- PHP.
- MariaDB/SQLite.
- Kubernetes/k3s.
- SEO/accessibility.
- Dead-code adapters.
- Duplication analyzers.

## P2 — DevFlow v0.7 GitHub / CI

- GitHub provider.
- PR read/create/review.
- CI/check ingestion.
- Evidence normalization.
- WorkItem ↔ PR linking.
- Event deduplication.
- StellarCode sync.
- Release metadata.

## P3 — DevFlow v0.8 Release / Deploy

- Release model/provider execution.
- Deploy provider abstraction.
- Rollback.
- Migration awareness.
- Staging preflight.
- Production verification.
- Post-deploy evidence.

## P4 — DevFlow v0.9 Runtime / Observability / OAuth

- k6.
- Grafana/Prometheus.
- Sentry.
- Docker runtime.
- Kubernetes/k3s runtime.
- Cloudflare.
- OAuth 2.1 interactive authorization.
- Scoped automation identities.

## Later / post-v1

- Baselines and history.
- Architecture/impact analysis.
- Repository hygiene.
- Dependency intelligence.
- DB/API audits.
- Resilience/cost analysis.
- Controlled automated remediation.
- Optional dashboard only if it adds value beyond Git/Markdown/StellarCode.
