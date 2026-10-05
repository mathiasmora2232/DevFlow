# DevFlow Core — Claude Instructions

This repository is the canonical source for DevFlow engineering workflows.

## Start here

Read in this order before implementing a new DevFlow version:

1. `DEVFLOW_ROADMAP.md`
2. `docs/CLAUDE_HANDOFF.md`
3. `docs/DOMAIN_MODEL.md`
4. `docs/FINDING_LIFECYCLE.md`
5. `docs/PROVIDER_CONTRACT.md`
6. `docs/SYNC_MODEL.md`
7. `docs/CONFIG_AND_VERSIONING.md`
8. `docs/QUALITY_GATES.md`
9. relevant `skills/*/SKILL.md`
10. `ops/BACKLOG.md`

Use `docs/COMMANDS.md` for slash-command routing.

## Sources of truth

- `DEVFLOW_ROADMAP.md`: global scope/status/version plan.
- `skills/*/SKILL.md`: canonical workflow behavior.
- `.devflow.yml`: project-specific policy/configuration.
- Git: technical evidence.
- StellarCode: shared operational state.
- Runtime providers: runtime evidence.

Conversation memory is never a source of truth.

## Engineering rules

- Evidence over assumptions.
- Keep Project Health, Stack Fit and Evidence Confidence separate.
- Preserve provider-neutral core logic.
- Use capability/provider adapters rather than scattered provider conditionals.
- Findings require stable fingerprints and lifecycle reconciliation.
- Scores, gates and approvals are different concepts.
- Never fabricate runtime, CI, deployment, security or performance evidence.
- Never store access credentials in repository config or Markdown.
- Preserve server-side RBAC; client-side hiding is not authorization.
- Production/destructive/shared consequential operations remain approval-gated.
- Merge != deploy != verified != closed.
- Keep DevFlow usable offline for local analysis.

## Development workflow

- Work on a feature branch.
- Follow the active version scope in `DEVFLOW_ROADMAP.md`.
- Add tests with behavior changes.
- Run the complete test suite before PR.
- Update docs in the same PR when contracts change.
- Update `IMPLEMENTATION_STATUS.md` when capability status changes.
- Update `CHANGELOG.md` for release-facing behavior.
- Do not mark designed functionality as implemented.

## Current recommended next version

**v0.5 Foundations is implemented. The next milestone is v0.6 Analyzers.**

Build v0.6 on top of the v0.5 contracts:

1. analyzer registry/plugin architecture;
2. FastAPI/Python analyzer;
3. Node/Next/React analyzer;
4. Angular analyzer;
5. PostgreSQL analyzer;
6. Docker analyzer;
7. GitHub Actions analyzer;
8. then Go/Quarkus/PHP and the remaining catalog.

Every analyzer must emit canonical Findings with stable fingerprints, evidence and confidence.

## Production

Code completion does not authorize deployment.

Do not deploy, run destructive DB migrations, enable production writes, change DNS or mutate shared infrastructure unless explicitly authorized.
