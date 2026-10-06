# DevFlow Core — Implementation Status

> Resumen corto. Para alcance global, fases, matriz de capacidades y Definition of Done, ver [`DEVFLOW_ROADMAP.md`](./DEVFLOW_ROADMAP.md).

## v0.5 implemented

- 25 canonical skills.
- CLI package `devflow`.
- Spanish slash-style aliases and English aliases.
- `/nuevo-proyecto`: interactive/non-interactive project initialization.
- `/detectar`: conservative stack detection.
- `/auditar`: evidence-aware static audit and Markdown/JSON reports.
- `/puntuar`: Project Health, Stack Fit and Evidence Confidence.
- `/revisar-stack`: stack alignment/proportionality report.
- `/planificar`: persistent work IDs + backlog/trace update.
- `/traza`: Git snapshot synchronization.
- `/estado`: concise project state.
- `/doctor`: environment/tooling/disk readiness.
- `/docs`: documentation coverage score/report.
- `/secretos`: redacted secret scanning + CI threshold.
- Expanded automated test suite covering CLI, config migrations, findings, gates, providers, sync/idempotency and regressions.
- StellarCode MCP client and project binding.
- `/stellar-status`: authenticated identity, project role and permissions.
- `devflow stellar-login`: web-approved device login (Google/GitHub/password+MFA on StellarCode), agent two-step mode (`--no-wait --json` / `--wait`), local 0600 credential store outside the repo; `stellar-auth`, `stellar-logout`.
- `devflow inicio`: session bootstrap (config, binding, auth) with agent login protocol and optional Claude Code SessionStart hook (`--install-hook`).
- `/kanban`: shared task board read/move operations.
- Project discovery, role listing, member/role management and project decisions via StellarCode MCP.
- `/planificar --stellar`: remote-first backlog creation.
- `/traza --stellar`: local Git + remote Kanban snapshot.
- `/siguiente`: next actionable task from the shared backlog.
- CI workflow for automated Python tests.
- Regression protection against stack detection from documentation-only mentions.
- Canonical domain models for Project, Repository, WorkItem, Finding, Evidence, Decision, Risk, Release, Deployment, Environment and Principal.
- Finding lifecycle with stable fingerprints, persistence, reconciliation, regression detection and waivers.
- `/findings` CLI for finding lifecycle management.
- Config schema v2 with `devflow /validar`, `config show` and `config migrate --check`.
- Provider capability protocol + normalized result/error contracts + registry.
- Sync conflicts, authority model, event model and persistent idempotency store.
- Deterministic quality gates and operational profiles via `devflow /gate`.
- Principal model supports users and service accounts.
- Versioned JSON schemas for config, findings, audit, sync, provider and gate outputs.

## Intentionally not claimed as implemented yet

- Runtime server load scoring.
- Production health verification.
- Lighthouse integration.
- k6 execution adapter.
- Grafana/Prometheus ingestion.
- GitHub Actions live state ingestion.
- Cloudflare/Kubernetes live operations.
- Additional live provider/MCP adapters beyond StellarCode.
- Language-specific dead-code analyzers.
- Production deploy automation.

Those capabilities require adapters/live evidence and remain approval-gated where consequential.


## Next architectural milestone

### v0.6 Analyzers

Use the v0.5 contracts to implement stack-specific analyzers. Every analyzer must emit canonical findings with stable fingerprints, evidence and confidence.

First wave:

- FastAPI/Python;
- Node/Next/React;
- Angular;
- PostgreSQL;
- Docker;
- GitHub Actions.

Do not bypass config schema, provider capabilities, finding reconciliation or gate policy.
