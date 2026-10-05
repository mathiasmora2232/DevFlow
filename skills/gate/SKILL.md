---
name: gate
description: Evalúa quality gates deterministas separados de scores y approvals.
---

# /gate

## Objetivo

Convertir evidencia y política en una decisión reproducible.

## Comando

```bash
devflow /gate pull_request
devflow /gate production --tests --build --rollback --healthcheck --verified-ci
```

## Resultados

```text
pass
warn
blocked
unknown
```

## Reglas

- `unknown` no significa `pass`.
- Score = medición.
- Gate = decisión de política.
- Approval = permiso para ejecutar una acción.
- Un gate aprobado nunca elimina un approval gate de producción.
- La falta de evidencia obligatoria produce `unknown` o bloqueo según política, nunca evidencia inventada.
