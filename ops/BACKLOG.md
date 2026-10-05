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

## P1 — DevFlow v0.5 Foundations

- Implement canonical domain models from `docs/DOMAIN_MODEL.md`.
- Implement Finding model.
- Stable finding fingerprint.
- Audit reconciliation: new/persistent/fixed/regressed.
- Finding waiver metadata and expiry.
- Formal config schema.
- `devflow validate`.
- Config migration framework and `devflow config migrate --check`.
- Provider/capability interface.
- Normalized provider errors/results.
- SyncResult model.
- Conflict detection.
- Idempotency/event primitives.
- Quality gate engine.
- Operational profiles.
- Principal model ready for user/automation identity.
- Add schema/version metadata to machine-readable outputs.
- Expand tests around conflicts, migrations and false positives.

## P2 — DevFlow v0.6 Analyzers

First wave:
- FastAPI/Python.
- Node/Next/React.
- Angular.
- PostgreSQL.
- Docker.
- GitHub Actions.

Second wave:
- Go.
- Quarkus.
- PHP.
- MariaDB/SQLite.
- Kubernetes/k3s.
- SEO/accessibility.
- Dead-code adapters.
- Duplication analyzers.

## P3 — DevFlow v0.7 GitHub / CI

- GitHub provider.
- PR read/create/review.
- CI/check ingestion.
- Evidence normalization.
- WorkItem ↔ PR linking.
- Event deduplication.
- StellarCode sync.
- Release metadata.

## P4 — DevFlow v0.8/v0.9 Operations

- Release/deploy/rollback providers.
- Production verification.
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
