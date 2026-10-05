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

## Binding

```bash
devflow stellar-bind --project-id 10
```

Luego exportar un JWT real de StellarCode:

```bash
export STELLARCODE_TOKEN="..."
```

PowerShell:

```powershell
$env:STELLARCODE_TOKEN="..."
```

## Uso

```bash
devflow /stellar-status
devflow /kanban
devflow /planificar "Trabajo" --stellar
devflow /traza --stellar
devflow /siguiente
```
