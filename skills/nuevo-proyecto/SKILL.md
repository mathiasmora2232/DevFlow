---
name: nuevo-proyecto
description: Inicializa o adopta un proyecto mediante descubrimiento, clasificación y sincronización obligatoria con StellarCode Studio.
---

# /nuevo-proyecto

## Objetivo

Registrar correctamente un proyecto en DevFlow + StellarCode Studio y elegir la ruta de descubrimiento según el tipo de trabajo.

StellarCode es el hub operacional del proyecto. El archivo local `.devflow.yml` es configuración local, no el registro maestro.

## Clasificación inicial obligatoria

### Ownership

```text
internal
external_client
```

Si es `external_client`, resolver/vincular el cliente en StellarCode.

### Engagement type

```text
greenfield
migration
refactor
modernization
maintenance
audit_only
```

No usar un flujo único para todos.

## Resolución del nombre

Prioridad:

1. nombre explícito del usuario;
2. binding StellarCode existente;
3. metadata del repo;
4. nombre del repo/carpeta;
5. pedir corrección solo si sigue ambiguo.

La inferencia se presenta como propuesta, no como verdad.

## Ruta greenfield

```text
identidad
→ ownership/client
→ engagement=greenfield
→ objetivos
→ alcance
→ restricciones
→ propuesta de stack
→ aprobación
→ proyecto StellarCode
→ fases
→ backlog inicial
→ config/repo
```

En un proyecto realmente nuevo primero se diseña el stack y la arquitectura proporcional al alcance.

## Ruta existing system

Para migration/refactor/modernization/maintenance:

```text
identidad
→ ownership/client
→ engagement
→ detectar repo real
→ barrido de descubrimiento
→ stack real
→ arquitectura actual
→ security/secrets/config
→ dependencies/tests/db
→ infra/CI/docs/observability
→ scores/findings
→ snapshot StellarCode
→ objetivos/target state
→ fases
→ backlog propuesto
```

No preguntar manualmente datos que el repositorio/providers puedan demostrar.

## Initial discovery bundle

Ejecutar o preparar:

- doctor;
- stack detection;
- audit general;
- security;
- secret hygiene;
- config/env metadata;
- dependencies;
- architecture;
- code quality;
- testing;
- database;
- DevOps/CI;
- documentation;
- observability/resilience;
- SEO/accessibility cuando aplique;
- performance estática;
- runtime evidence si hay providers.

## Sync obligatorio

Sincronizar a StellarCode mediante MCP:

- Project;
- Client/internal ownership;
- engagement type;
- repositories;
- detected stack;
- architecture summary;
- environments;
- config variable metadata;
- infrastructure inventory;
- audit runs;
- scores;
- findings;
- risks;
- decisions;
- phases;
- objectives;
- backlog proposals;
- evidence;
- time-tracking policy.

Si MCP no está disponible, marcar `sync_status=pending`; no declarar onboarding completo.

## Reglas

- Evidencia > suposición.
- Existing system: current state antes de target state.
- Greenfield: definir objetivos/constraints antes del stack.
- No guardar secretos.
- No crear backlog masivo sin aprobación.
- No considerar un proyecto gestionado si nunca fue vinculado al Hub.
