---
name: stellarcode-sync
description: Usa StellarCode MCP como fuente operacional compartida para identidad, Kanban, backlog y sincronización de DevFlow.
---

# StellarCode Sync

## Principios

- StellarCode MCP es la fuente operacional compartida.
- Git es la fuente de evidencia técnica.
- DevFlow contiene reglas y orquesta el flujo.
- El token del usuario nunca se guarda en `.devflow.yml`.
- El servidor MCP aplica RBAC; el cliente no es una frontera de seguridad.
- Backlog sync es `remote_first`: una tarea remota debe existir antes de reflejarse localmente.

## Login y binding

Antes de cualquier operación remota: `devflow inicio` (o `devflow stellar-auth`). Si no hay sesión, aplicar el skill [`stellar-login`](../stellar-login/SKILL.md): el agente genera el enlace con `devflow stellar-login --no-wait --json`, se lo muestra a la persona (login con Google en la web + aprobar) y espera con `devflow stellar-login --wait`.

```bash
devflow stellar-login --project-id 10   # login web + bind en un paso (terminal interactiva)
devflow stellar-bind --project-id 10    # solo bind, si ya hay sesión
```

CI / service accounts: exportar `STELLARCODE_TOKEN` (o la variable de `stellarcode.auth.token_env`); tiene prioridad sobre la credencial del login web.

## Errores de autenticación

| Mensaje | Acción |
|---|---|
| `Not logged in to StellarCode` | protocolo `stellar-login` |
| `StellarCode session expired` | protocolo `stellar-login` (el token dura ≤ 24 h) |
| `401`/`403` en una tool MCP con sesión válida | falta de permiso RBAC: informar, no reintentar |

## Uso

```bash
devflow /stellar-status
devflow /kanban
devflow /planificar "Trabajo" --stellar
devflow /traza --stellar
devflow /siguiente
```
