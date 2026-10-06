# Changelog

## [Unreleased]

### Added

- `devflow stellar-login`: StellarCode login through the web approval flow (Google sign-in supported) with an agent-friendly two-step mode (`--no-wait --json`, then `--wait`); token stored in `~/.devflow/stellar.env` (0600), compatible with StellarCode Studio `npm run devflow:login`.
- `devflow stellar-auth`, `devflow stellar-logout` and `devflow inicio` (session bootstrap, `--install-hook` for a Claude Code SessionStart hook).
- StellarCode token resolution now falls back to the local login store after `token_env`, `STELLARCODE_TOKEN` and `STELLAR_MCP_TOKEN`.
- `stellar-login` skill with the agent login protocol; router and `stellarcode-sync` skills route auth failures to it.

- DevFlow CLI v0.5 Foundations.
- Canonical domain contracts and service-account-ready Principal model.
- Persistent Finding lifecycle with stable fingerprints, reconciliation, regressions and waivers.
- `/findings` lifecycle command.
- Config schema v2, `/validar`, `config show` and config migration framework.
- Provider capability abstraction, normalized errors/results and registry.
- Sync authority/conflict model, event contract and idempotency store.
- Deterministic quality gates/profiles through `/gate`.
- Versioned JSON schemas for machine-readable contracts.

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
