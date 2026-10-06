# DevFlow — Codex Adapter

Use the canonical skills in `/skills`.

Before significant work:
1. Run `devflow inicio` and read `.devflow.yml`. If there is no StellarCode session, follow `skills/stellar-login/SKILL.md` (show the person the `login_url` from `devflow stellar-login --no-wait --json`, then `devflow stellar-login --wait`).
2. Select the matching skill from `skills/`.
3. Read only the supporting files needed by that skill.
4. Use Git and generated evidence as source of truth.
5. Update trace after meaningful mutating work.

Never claim CI, deploy, production health, security or load results without evidence.

Production/destructive actions remain approval-gated according to `.devflow.yml`.
