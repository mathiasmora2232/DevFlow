# Changelog

## [Unreleased]

### Added

- DevFlow CLI v0.4.
- StellarCode MCP integration with secure project binding.
- `/stellar-status`, `/kanban`, `/siguiente`, `stellar-bind`, `/planificar --stellar` and `/traza --stellar`.
- Remote-first backlog synchronization.
- JWT token lookup via environment variable only; tokens are never stored in project config.
- GitHub Actions CI for DevFlow tests.

- DevFlow CLI v0.3.
- `/doctor`: readiness de entorno, tooling y espacio libre.
- `/docs`: auditoría de documentación con score y quality gate opcional.
- `/secretos`: escaneo de secretos con redacción y `--fail-on` para CI.

- DevFlow CLI v0.2 (`devflow`).
- Spanish slash-style CLI aliases and English aliases.
- Interactive/non-interactive `/nuevo-proyecto` initialization.
- Automatic stack detection for FastAPI, Go, Node.js, Quarkus, PHP, Angular, Next.js, React, PostgreSQL, MariaDB, SQLite and core infra signals.
- Static `/auditar` engine with evidence-aware Project Health scoring.
- `/puntuar` with Health, Stack Fit and Evidence Confidence.
- `/revisar-stack` report and proportionality warnings.
- `/planificar` persistent work IDs and backlog/trace entries.
- `/traza` Git snapshot synchronization.
- `/estado` summary command.
- Automated tests for detection, scoring, trace IDs, initialization and audit generation.
- Conservative `N/A` handling for runtime server load without evidence.
- DevFlow workflow model, scorecards, stack catalog, templates, Codex/Claude adapters and MCP roadmap.
