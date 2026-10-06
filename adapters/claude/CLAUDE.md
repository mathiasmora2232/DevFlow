# DevFlow — Claude Code Adapter

The canonical engineering workflows live under `/skills`.

Map user slash commands to the corresponding skill described in `docs/COMMANDS.md`.

Read `.devflow.yml` before project-specific workflow decisions.
Persist state in Git-tracked operational files.
Do not rely on chat history as the only project state.

At session start run `devflow inicio`. If it reports no StellarCode session, follow `skills/stellar-login/SKILL.md`: run `devflow stellar-login --no-wait --json`, show the person the `login_url` as a link (Google sign-in + approve), then `devflow stellar-login --wait --timeout 540`. Never ask for tokens in chat.

Respect approval gates for shared/destructive/production actions.
