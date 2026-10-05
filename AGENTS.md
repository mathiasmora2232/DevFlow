# DevFlow Core Agent Instructions

This repository is the canonical source for reusable engineering workflow skills and DevFlow implementation.

## Read order

Before changing architecture or version scope, read:

1. `DEVFLOW_ROADMAP.md`
2. `docs/DOMAIN_MODEL.md`
3. `docs/FINDING_LIFECYCLE.md`
4. `docs/PROVIDER_CONTRACT.md`
5. `docs/SYNC_MODEL.md`
6. `docs/CONFIG_AND_VERSIONING.md`
7. `docs/QUALITY_GATES.md`
8. relevant `skills/*/SKILL.md`
9. `ops/BACKLOG.md`

Agent-specific continuation guidance lives in `docs/CLAUDE_HANDOFF.md`.

## Rules

- Keep skills provider-neutral.
- Use providers/adapters as capability boundaries.
- Use evidence rather than assumptions.
- Separate Project Health, Stack Fit and Evidence Confidence.
- Findings must have stable identity/fingerprint and lifecycle.
- Separate measurement (score), policy (gate) and execution permission (approval).
- Never fabricate runtime, CI, deployment, security, SEO or load-test evidence.
- Never persist raw credentials in config, reports or Markdown.
- Preserve server-side RBAC for StellarCode.
- Preserve approval gates for production/destructive/shared actions.
- Treat Git as technical truth and StellarCode as shared operational truth.
- Do not silently resolve sync conflicts when authority is ambiguous.
- Keep local/offline DevFlow functionality independent from MCP availability.

## Documentation discipline

A capability is not implemented merely because a skill or design document exists.

When implementation status changes, update:

- `DEVFLOW_ROADMAP.md`;
- `IMPLEMENTATION_STATUS.md`;
- the specialized contract doc;
- `CHANGELOG.md` if user/release-facing.
