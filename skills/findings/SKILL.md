---
name: findings
description: Administra el lifecycle de hallazgos técnicos con identidad estable, reconciliación y waivers explícitos.
---

# /findings

## Objetivo

Evitar que cada auditoría produzca hallazgos desechables o duplicados.

## Comandos

```bash
devflow /findings
devflow findings list --status open
devflow findings status --id FND-... --status acknowledged
devflow findings status --id FND-... --status accepted_risk --reason "..." --approved-by "..."
```

## Reglas

- Todo finding debe tener `fingerprint` estable.
- Un finding ausente en una auditoría pasa a `fixed`, no directamente a `closed`.
- Un finding fixed/verified/closed que reaparece se reabre como regresión.
- `accepted_risk`, `suppressed` y `false_positive` requieren decisión explícita.
- Waivers deben admitir expiración.
- Auditorías no crean tareas remotas automáticamente.
