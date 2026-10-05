# DevFlow Core — Implementation Status

> Resumen corto. Para alcance global, fases, matriz de capacidades y Definition of Done, ver [`DEVFLOW_ROADMAP.md`](./DEVFLOW_ROADMAP.md).

## v0.4 implemented

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
- 13 automated tests.
- StellarCode MCP client and project binding.
- `/stellar-status`: authenticated identity, project role and permissions.
- `/kanban`: shared task board read/move operations.
- Project discovery, role listing, member/role management and project decisions via StellarCode MCP.
- `/planificar --stellar`: remote-first backlog creation.
- `/traza --stellar`: local Git + remote Kanban snapshot.
- `/siguiente`: next actionable task from the shared backlog.
- CI workflow for automated Python tests.
- Regression protection against stack detection from documentation-only mentions.

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

### v0.5 Foundations

Documented contracts ready for implementation:

- `docs/DOMAIN_MODEL.md`
- `docs/FINDING_LIFECYCLE.md`
- `docs/PROVIDER_CONTRACT.md`
- `docs/SYNC_MODEL.md`
- `docs/CONFIG_AND_VERSIONING.md`
- `docs/QUALITY_GATES.md`
- `docs/CLAUDE_HANDOFF.md`

v0.5 should implement these foundations before expanding framework analyzers at scale.

Key targets:

- canonical domain models;
- finding fingerprint/lifecycle/reconciliation;
- config validation and migrations;
- provider capability abstraction;
- sync conflicts and idempotency;
- quality gates/profiles;
- versioned machine-readable contracts.
