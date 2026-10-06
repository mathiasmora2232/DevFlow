# DevFlow CLI

## Install

```bash
python -m pip install -e .
```

## Commands

```bash
devflow /nuevo-proyecto
devflow /detectar
devflow /auditar
devflow /puntuar
devflow /revisar-stack
devflow /planificar "Agregar autenticación" --type feature --priority high \
  --acceptance "Login válido retorna sesión" \
  --acceptance "Credenciales inválidas no filtran información"
devflow /traza
devflow /estado
devflow /doctor
devflow /docs
devflow /secretos
```

English aliases are also accepted:

```bash
devflow init
devflow detect
devflow audit
devflow score
devflow stack-review
devflow plan "..."
devflow trace
devflow status
```

## Current audit mode

v0.5 keeps a conservative **static audit**. It can score repository evidence, but it intentionally returns `N/A` or low confidence for things that require runtime proof.

`server_load` stays `N/A` until future runtime/k6/Grafana adapters provide evidence.

## Safety

The v0.5 CLI does not deploy, push, mutate infrastructure, or execute production load tests. Those workflows remain skills/policies until explicit adapters are added.

## Doctor

```bash
devflow /doctor
devflow /doctor --strict
```

Revisa Python, Git, repositorio, `.devflow.yml`, permisos de escritura, espacio libre y herramientas relevantes del stack. Menos de 1 GB libre es blocker; menos de 5 GB genera warning.

## Documentation audit

```bash
devflow /docs
devflow /docs --min-score 80
```

Evalúa README, setup, arquitectura, API, variables de entorno, despliegue y pruebas según aplicabilidad.

## Secrets scan

```bash
devflow /secretos
devflow /secretos --fail-on high
```

Busca patrones de credenciales y archivos sensibles. Los valores se redactan en consola/reportes. `--fail-on` permite usarlo como quality gate en CI.

## StellarCode MCP

Vincula un repo local al proyecto operativo en StellarCode:

### Login

```bash
devflow inicio                         # estado de config, vínculo y sesión al arrancar
devflow stellar-login                  # enlace + código; abre el navegador; inicia sesión con Google y aprueba
devflow stellar-login --project-id 10  # login + stellar-bind
devflow stellar-auth                   # sesión válida y vencimiento (exit 6 si no hay)
devflow stellar-logout                 # borra la credencial local
devflow inicio --install-hook          # SessionStart hook de Claude Code en .claude/settings.json
```

Agentes (sin terminal visible para la persona):

```bash
devflow stellar-login --no-wait --json   # devuelve login_url + user_code; mostrar el enlace en el chat
devflow stellar-login --wait --timeout 540
```

El login usa el flujo de aprobación de StellarCode (`/api/mcp-connect`): la persona entra en la web (Google, GitHub o correo + MFA) y aprueba; el CLI recibe un token MCP de ≤ 24 h guardado en `~/.devflow/stellar.env` (permisos 600, mismo formato que `npm run devflow:login` de StellarCode Studio). Solo administradores pueden aprobar.

CI / service accounts siguen usando una variable de entorno, que tiene prioridad sobre la credencial local:

```bash
devflow stellar-bind --project-id 10
export STELLARCODE_TOKEN="..."      # PowerShell: $env:STELLARCODE_TOKEN="..."
```

Comandos:

```bash
devflow /stellar-status
devflow /proyectos
devflow /roles
devflow /miembros
devflow /miembros add --user-id 7 --role developer
devflow /miembros role --user-id 7 --role reviewer
devflow /miembros remove --user-id 7
devflow /kanban
devflow /kanban move --task-id 184 --status review
devflow /decision
devflow /decision add --title "Usar PostgreSQL" --decision "Mantener PostgreSQL como base principal"
devflow /planificar "Agregar historial" --stellar
devflow /traza --stellar
devflow /siguiente
```

El sync de backlog es `remote_first`: DevFlow crea/actualiza primero StellarCode y luego persiste la traza local. El token nunca se escribe en `.devflow.yml`.


## v0.5 Foundations

### Config

```bash
devflow /validar
devflow config show
devflow config migrate --check
devflow config migrate
```

La migración v1→v3 crea backup local y nunca mueve credenciales crudas a YAML.

### Findings

```bash
devflow /findings
devflow findings list --status open
devflow findings status --id FND-... --status acknowledged
devflow findings status --id FND-... --status accepted_risk --reason "temporary" --approved-by "owner" --expires-at 2026-12-01
```

`/auditar` reconcilia automáticamente findings contra `ops/findings.json`.

### Quality gates

```bash
devflow /gate pull_request
devflow /gate production --tests --build --rollback --healthcheck --verified-ci
```

Un resultado `unknown` significa que falta evidencia obligatoria; no se trata como `pass`.


## Foundations v0.5

### Config validation and migration

```bash
devflow /validar
devflow config show
devflow config migrate --check
devflow config migrate
```

Schema v3 adds explicit project `ownership`, `engagement` and optional `client_id` on top of the v2 foundations. Migration creates a backup before mutating the config and never persists raw StellarCode credentials.

### Finding lifecycle

```bash
devflow /auditar
devflow /findings
devflow /findings list --severity high
devflow /findings status --id FND-... --status acknowledged
devflow /findings status --id FND-... --status accepted_risk --reason "temporary" --approved-by "owner" --expires-at 2026-12-01
```

Findings use stable fingerprints and persist in `ops/findings.json`. Repeated audits reconcile new, persistent, fixed and regressed findings instead of recreating the same issue every time.

### Quality gates

```bash
devflow /gate pull_request
devflow /gate production --tests --build --rollback --healthcheck --verified-ci
```

Gate results are deterministic and separate measurement (scores), policy (gate) and execution approval.
