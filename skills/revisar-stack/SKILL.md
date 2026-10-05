---
name: revisar-stack
description: Detecta y evalúa el stack real, distingue current/target state y sincroniza el inventario estructurado con StellarCode Studio.
---

# /revisar-stack

## Objetivo

Representar el stack real del proyecto con evidencia antes de recomendar cambios.

## Existing systems

Primero publicar el current state:

```text
category
technology
version?
source
evidence
confidence
```

Categorías típicas:

- backend;
- frontend;
- database;
- cache;
- queue;
- storage;
- auth;
- build;
- container;
- orchestration;
- CI/CD;
- edge;
- monitoring.

Luego evaluar:

- project fit;
- team familiarity;
- operating cost;
- delivery speed;
- ecosystem;
- migration cost;
- future flexibility.

## Migration / modernization

Nunca sobrescribir current state con target state.

StellarCode debe mantener:

```text
current_stack
target_stack
delta
strategy
risks
phases
```

## Recomendaciones válidas

- keep
- keep_with_improvements
- evaluate_partial_migration
- migration_candidate

## Reglas

- Project Health != Stack Fit.
- No migrar por preferencia.
- Repo evidence antes de input manual.
- Publicar stack inventory estructurado al MCP.
