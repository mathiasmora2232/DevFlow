# DevFlow Core — Implementation Status

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
- 10 automated tests.
- StellarCode MCP client and project binding.
- `/stellar-status`: authenticated identity, project role and permissions.
- `/kanban`: shared task board read/move operations.
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
- MCP server.
- Language-specific dead-code analyzers.
- Production deploy automation.

Those capabilities require adapters/live evidence and remain approval-gated where consequential.
