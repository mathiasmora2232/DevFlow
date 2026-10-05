---
name: sincronizar-traza
description: Sincroniza Git, DevFlow y StellarCode sin colapsar estados técnicos y operacionales.
---

# /traza

## Fuentes

- Git: branch/commit/working tree.
- StellarCode: project/work item/phase/time/operational status.
- Runtime provider: deploy/health cuando exista.
- DevFlow: findings/audits/gates/local reports.

## Invariantes

```text
merged != deployed
deployed != verified
verified != closed
```

## Sync

Actualizar el snapshot local y publicar los cambios estructurados correspondientes al Hub.

Si existe conflicto, reportar:

```text
field
local_value
remote_value
authority
recommended_resolution
```

No sobrescribir conflictos ambiguos silenciosamente.

## Time tracking

La traza puede referenciar sesiones/entradas de tiempo, pero StellarCode es la fuente operacional de TimeSession/TimeEntry.

## Offline

Si MCP no responde:

```text
sync_status=pending
```

La operación local puede continuar, pero no se declara sincronizada.
