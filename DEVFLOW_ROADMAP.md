# DevFlow — Master Roadmap

> Fuente global de verdad sobre el alcance, estado y evolución de DevFlow.
>
> Última consolidación: 2026-10-04
>
> Regla: si este archivo contradice un README, backlog o documento de fase más antiguo, este archivo tiene prioridad para el estado global. Los documentos específicos siguen siendo la fuente detallada de cada área.

---

## 1. Visión

DevFlow es un sistema operativo de ingeniería reutilizable para trabajar con distintos proyectos, repositorios y agentes de código bajo un mismo modelo de:

```text
Contexto
  ↓
Diagnóstico
  ↓
Plan
  ↓
Ejecución
  ↓
Validación
  ↓
Revisión
  ↓
Integración
  ↓
Deploy
  ↓
Verificación
  ↓
Evidencia / Traza
  ↓
Siguiente acción
```

Su objetivo no es reemplazar GitHub, CI/CD, observabilidad, tickets o infraestructura.

DevFlow debe:

- definir cómo se trabaja;
- mantener reglas y quality gates;
- detectar y auditar proyectos;
- convertir hallazgos en trabajo trazable;
- conectar agentes y herramientas con una fuente operacional compartida;
- exigir evidencia antes de afirmar que algo está sano, desplegado o verificado;
- evitar sobrearquitectura y migraciones injustificadas.

---

## 2. Arquitectura global

```text
                     ┌──────────────────────────┐
                     │ ChatGPT / Codex / Claude │
                     │ otros agentes de código  │
                     └────────────┬─────────────┘
                                  │
                                  ▼
                         ┌────────────────┐
                         │    DevFlow     │
                         │ Skills + CLI   │
                         │ Rules + Scores │
                         └───────┬────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               │                 │                 │
               ▼                 ▼                 ▼
        Static Analyzers      Git / CI        StellarCode MCP
        local evidence     technical truth    operational state
                                                  │
                                                  ▼
                                  Projects / Kanban / Backlog
                                  Members / Roles / Decisions
                                  Risks / Evidence / Activity
                                                  │
                                                  ▼
                                             PostgreSQL
```

### Responsabilidades

**DevFlow Core**
- reglas;
- skills;
- perfiles;
- scorecards;
- planificación;
- auditoría;
- routing;
- approval gates;
- CLI;
- adapters.

**Git / GitHub**
- código;
- ramas;
- commits;
- PRs;
- releases;
- CI;
- evidencia técnica.

**StellarCode MCP**
- identidad real;
- RBAC;
- proyectos;
- backlog;
- Kanban;
- miembros;
- roles;
- riesgos;
- decisiones;
- evidencia operacional;
- actividad;
- estado compartido entre agentes.

---

## 3. Principios no negociables

1. Evidencia > suposición.
2. Merge != deploy.
3. Deploy != verified.
4. Verified != closed si quedan pendientes.
5. Un score sin evidencia suficiente debe ser N/A o tener baja confianza.
6. Project Health y Stack Fit son conceptos distintos.
7. No migrar solo porque otra tecnología sea preferida.
8. MVP y costo/beneficio antes de Kubernetes, microservicios o complejidad prematura.
9. Acciones destructivas o de producción requieren aprobación.
10. Tokens y secretos no se guardan en `.devflow.yml`, Markdown ni trazas.
11. La memoria del chat nunca es la fuente de verdad.
12. El MCP aplica permisos server-side; ocultar botones/tools en un cliente no es seguridad.
13. Git es evidencia técnica; StellarCode es estado operacional.
14. Backlog remoto usa estrategia `remote_first`.
15. Una auditoría no crea decenas de tareas automáticamente sin aprobación.
16. Findings tienen identidad estable; no se recrean como problemas nuevos en cada scan.
17. Scores, gates y approvals son conceptos separados.
18. Project y Repository no son sinónimos; un proyecto puede abarcar múltiples repos.
19. Integraciones escribibles deben ser idempotentes y registrar request/event identity.
20. Config, findings, sync results y provider outputs deben evolucionar con schema/version explícita.

---

# 4. Estado ejecutivo

## DevFlow Core

| Área | Estado | Nota |
|---|---|---|
| Skills base | ✅ Implementado | 25+ skills canónicas |
| CLI base | ✅ Implementado | v0.5 |
| Inicialización | ✅ Implementado | interactiva y no interactiva |
| Stack detection | ✅ Implementado | conservador |
| Auditoría estática | ✅ Implementado | con evidencia y N/A |
| Project Health | ✅ Implementado | 0–100 |
| Stack Fit | ✅ Implementado | separado de Health |
| Evidence Confidence | ✅ Implementado | 0–100 |
| Doctor | ✅ Implementado | entorno/tooling/disco |
| Docs audit | ✅ Implementado | score + reporte |
| Secret scan | ✅ Implementado | redacción + fail thresholds |
| Trace | ✅ Implementado | Git + local ops |
| Planning | ✅ Implementado | IDs + backlog + trace |
| StellarCode binding | ✅ Implementado | v0.4 |
| Kanban compartido | ✅ Implementado | lectura + movimientos |
| Miembros / roles | ✅ Implementado | vía MCP |
| Decisiones | ✅ Implementado | vía MCP |
| Remote-first planning | ✅ Implementado | `/planificar --stellar` |
| Runtime observability | ❌ Pendiente | requiere adapters |
| Production verification | ❌ Pendiente | requiere runtime evidence |
| Deploy automation | ❌ Pendiente | approval-gated |
| Domain contracts | ✅ Implementado | modelos canónicos + tests |
| Finding lifecycle/fingerprints | ✅ Implementado | persistencia + reconciliación + waivers |
| Config schema/migrations | ✅ Implementado | schema v2 + validate + migrate |
| Provider capability layer | ✅ Implementado | protocol + registry + normalized results/errors |
| Sync/conflict/idempotency | ✅ Implementado | authority/conflicts/events/idempotency |
| Quality gates/profiles | ✅ Implementado | deterministic gate engine |
| Deep framework analyzers | 📐 Diseñado | v0.6 |
| GitHub/CI ingestion | ❌ Pendiente | v0.7 |
| Cost analysis | ❌ Pendiente | futuro |
| Auto-remediation | ❌ Pendiente | futuro |

## StellarCode MCP v2

| Área | Estado | Nota |
|---|---|---|
| Endpoint MCP | ✅ Implementado | servidor existente evolucionado |
| Usuario real | ✅ Implementado | JWT StellarCode |
| Project membership | ✅ Implementado | `project_members` |
| RBAC por proyecto | ✅ Implementado | server-side |
| Roles | ✅ Implementado | owner/admin/manager/developer/reviewer/viewer |
| Permisos atómicos | ✅ Implementado | matriz persistente + fallback |
| Gestión de miembros | ✅ Implementado | add/change/remove |
| Audit log MCP | ✅ Implementado | user/project/client/request |
| Project decisions | ✅ Implementado | ADR-style |
| Protección task assignment | ✅ Implementado | requiere `task.assign` |
| Protección status change | ✅ Implementado | requiere `task.change_status` |
| Legacy shared secret | 🚧 Transición | deshabilitable |
| OAuth 2.1 interactivo | ❌ Pendiente | JWT manual/env funciona hoy |
| Migración BD producción | ⏳ Pendiente rollout | no ejecutada desde DevFlow |
| Deploy producción | ⏳ Pendiente rollout | no ejecutado automáticamente |
| MCP writes producción | ⏳ Pendiente rollout | deben habilitarse luego de validar |

---

# 5. Matriz global de capacidades

Leyenda:

- ✅ operativo
- 🚧 parcial
- 📐 diseñado/skill
- ❌ pendiente
- N/A no corresponde

| Capability | Skill | CLI | StellarCode MCP | Runtime/Provider | Estado |
|---|---:|---:|---:|---:|---|
| Nuevo proyecto | ✅ | ✅ | 🚧 | N/A | ✅ |
| Estado proyecto | ✅ | ✅ | ✅ | 🚧 | 🚧 |
| Stack detection | ✅ | ✅ | N/A | local | ✅ |
| Doctor | ✅ | ✅ | N/A | local | ✅ |
| Docs audit | ✅ | ✅ | N/A | local | ✅ |
| Secret scanning | ✅ | ✅ | N/A | local | ✅ |
| Planificación | ✅ | ✅ | ✅ | N/A | ✅ |
| Backlog / Kanban | ✅ | ✅ | ✅ | StellarCode | ✅ |
| Siguiente acción | ✅ | ✅ | ✅ | StellarCode | ✅ |
| Trace | ✅ | ✅ | ✅ | Git + StellarCode | ✅ |
| Finding lifecycle | ✅ | ✅ | N/A | DevFlow local | ✅ |
| Config validation/migration | ✅ | ✅ | N/A | local | ✅ |
| Quality gates | ✅ | ✅ | N/A | evidence-driven | ✅ |
| Provider capability contract | ✅ | N/A | N/A | core abstraction | ✅ |
| Sync/idempotency primitives | ✅ | N/A | N/A | core abstraction | ✅ |
| Auditoría general | ✅ | ✅ | 🚧 | local | 🚧 |
| Project Health | ✅ | ✅ | N/A | local evidence | ✅ |
| Stack Fit | ✅ | ✅ | N/A | local evidence | ✅ |
| Evidence Confidence | ✅ | ✅ | N/A | local evidence | ✅ |
| Seguridad | ✅ | 🚧 | 🚧 | partial static | 🚧 |
| SEO | ✅ | 🚧 | N/A | ❌ Lighthouse | 🚧 |
| Performance | ✅ | 🚧 | 🚧 | ❌ runtime | 🚧 |
| Calidad de código | ✅ | 🚧 | N/A | ❌ deep analyzers | 🚧 |
| Código muerto | ✅ | ❌ | N/A | ❌ language adapters | 📐 |
| Deuda técnica | ✅ | ❌ | 🚧 | N/A | 📐 |
| Revisar stack | ✅ | ✅ | N/A | local | ✅ |
| Migrar stack | ✅ | ❌ | 🚧 | N/A | 📐 |
| PR preparation | ✅ | ❌ | ❌ | ❌ GitHub adapter | 📐 |
| PR review | ✅ | ❌ | ❌ | ❌ GitHub adapter | 📐 |
| Release | ✅ | ❌ | 🚧 | ❌ provider | 📐 |
| Deploy | ✅ | ❌ | ❌ | ❌ provider | 📐 |
| Verify production | ✅ | ❌ | ❌ | ❌ runtime | 📐 |
| Incident | ✅ | ❌ | 🚧 | ❌ live providers | 📐 |
| Postmortem | ✅ | ❌ | 🚧 | N/A | 📐 |
| Miembros | ✅ | ✅ | ✅ | StellarCode | ✅ |
| Roles / permisos | ✅ | ✅ | ✅ | StellarCode | ✅ |
| Decisiones | ✅ | ✅ | ✅ | StellarCode | ✅ |
| Riesgos | ✅ | 🚧 | ✅ | StellarCode | 🚧 |
| Evidencia | ✅ | 🚧 | ✅ | StellarCode/Git | 🚧 |
| GitHub CI state | 📐 | ❌ | ❌ | ❌ | ❌ |
| k6 | 📐 | ❌ | ❌ | ❌ | ❌ |
| Grafana/Prometheus | 📐 | ❌ | ❌ | ❌ | ❌ |
| Cloudflare | 📐 | ❌ | ❌ | ❌ | ❌ |
| Docker live state | 📐 | ❌ | ❌ | ❌ | ❌ |
| Kubernetes/k3s live state | 📐 | ❌ | ❌ | ❌ | ❌ |
| Cost analysis | ❌ | ❌ | ❌ | ❌ | ❌ |
| Auto-remediation | ❌ | ❌ | ❌ | ❌ | ❌ |

---

# 6. Comandos operativos actuales

## Core local

```bash
devflow /nuevo-proyecto
devflow /detectar
devflow /doctor
devflow /docs
devflow /secretos
devflow /auditar
devflow /puntuar
devflow /revisar-stack
devflow /planificar "..."
devflow /traza
devflow /estado
```

## StellarCode MCP

```bash
devflow stellar-bind --project-id <id>

devflow /stellar-status
devflow /proyectos
devflow /roles
devflow /miembros
devflow /kanban
devflow /decision

devflow /planificar "..." --stellar
devflow /traza --stellar
devflow /siguiente
```

## Seguridad de credenciales

El JWT del usuario se obtiene desde:

```text
STELLARCODE_TOKEN
```

No se persiste el valor del token en el repositorio.

---

# 7. Modelo de seguridad StellarCode MCP

## Identidad

```text
Real user
   │
   ▼
StellarCode JWT
   │
   ▼
MCP
   │
   ├── user_id
   ├── global role
   ├── client
   └── request_id
```

## Autorización

```text
user
  ↓
project_members
  ↓
project role
  ↓
atomic permissions
  ↓
tool authorization
```

## Roles actuales

| Rol | Objetivo |
|---|---|
| owner | control total |
| admin | administración completa del proyecto |
| manager | planificación, asignación, fases, riesgos y releases |
| developer | ejecución técnica y actualización de trabajo |
| reviewer | revisión, evidencia y transiciones autorizadas |
| viewer | solo lectura |

## Permisos atómicos

Familias actuales:

```text
project.*
task.*
members.*
phase.*
evidence.*
risk.*
decision.*
release.*
ticket.*
```

El MCP debe autorizar cada operación en el servidor.

---

# 8. Fuente de verdad

## Git

Fuente principal para:

- archivos;
- código;
- commits;
- ramas;
- PRs;
- CI;
- releases;
- diff;
- evidencia técnica.

## StellarCode

Fuente principal para:

- proyectos;
- miembros;
- roles;
- backlog;
- tareas;
- Kanban;
- riesgos;
- decisiones;
- actividad;
- estado operacional compartido.

## DevFlow files

Fuente local para:

- configuración;
- trace local;
- reportes;
- scorecards;
- auditorías;
- reglas;
- planes.

Archivos clave:

```text
.devflow.yml
ops/TRACE.md
ops/BACKLOG.md
ops/RISKS.md
ops/SECURITY.md
ops/RELEASES.md
ops/STELLAR.md
ops/reports/
CHANGELOG.md
DEVFLOW_ROADMAP.md
```

---

# 9. Fases y versiones

## v0.1 — Foundation ✅

Entregado:

- skills;
- filosofía;
- scorecards;
- stack catalog;
- templates;
- trace model;
- approval gates;
- adapters iniciales.

## v0.2 — CLI base ✅

Entregado:

- package Python;
- init;
- detect;
- audit;
- score;
- stack review;
- plan;
- trace;
- status;
- tests.

## v0.3 — Readiness y hygiene ✅

Entregado:

- doctor;
- docs audit;
- secret scan;
- fail thresholds;
- reportes persistentes;
- CI coverage inicial.

## v0.4 — StellarCode Operations Layer ✅ código / ⏳ rollout productivo

Entregado en código:

- cliente MCP;
- project binding;
- JWT desde env;
- MCP real-user identity;
- RBAC;
- roles;
- permissions;
- members;
- Kanban;
- decisions;
- remote-first plan;
- Stellar trace snapshot;
- next task;
- MCP activity audit.

Pendiente para completar rollout:

- ejecutar migración de BD en el entorno real;
- desplegar StellarCode MCP v2 a producción;
- probar identidad real contra `api.stellarcodelabs.lat/mcp`;
- validar roles con al menos owner/developer/viewer;
- activar writes de forma controlada;
- retirar shared secret legacy.

## v0.5 — Foundations ✅ ✅

Objetivo cumplido: estabilizar los contratos internos antes de multiplicar analyzers/providers.

Entregado:

- modelos canónicos para Project, Repository, WorkItem, Finding, Evidence, Decision, Risk, Release, Deployment, Environment y Principal;
- Finding lifecycle;
- fingerprint estable;
- reconciliación entre auditorías;
- config schema formal;
- `devflow validate`;
- framework de migración de config;
- provider/capability contract;
- sync results + conflictos + idempotencia;
- quality gate engine;
- perfiles operativos;
- principal model compatible con usuarios y automation identities;
- schema/version metadata en outputs críticos.

Documentos canónicos:

- `docs/DOMAIN_MODEL.md`;
- `docs/FINDING_LIFECYCLE.md`;
- `docs/PROVIDER_CONTRACT.md`;
- `docs/SYNC_MODEL.md`;
- `docs/CONFIG_AND_VERSIONING.md`;
- `docs/QUALITY_GATES.md`.

### Definition of Done v0.5 ✅

- contratos representados en código y tests;
- fingerprint de findings determinístico;
- auditorías pueden reconciliar findings históricos;
- `.devflow.yml` se valida contra schema/version;
- config antigua puede migrarse de forma controlada;
- provider interface no depende de GitHub/StellarCode específicos;
- conflictos de sync son visibles y no se pisan silenciosamente;
- writes repetidos pueden deduplicarse por idempotency key;
- gates producen `pass/warn/blocked/unknown`;
- tests cubren casos felices, conflictos y regresiones.

## v0.6 — Framework analyzers

Objetivo: hacer que `/auditar` use analizadores específicos que emitan el Finding contract v0.5.

Primera ola:

- FastAPI/Python;
- Node.js;
- Next.js/React;
- Angular;
- PostgreSQL;
- Docker;
- GitHub Actions.

Segunda ola:

- Go;
- Quarkus;
- PHP;
- MariaDB;
- SQLite;
- Kubernetes/k3s;
- SEO/accessibility.

Tooling a integrar progresivamente:

- Ruff;
- mypy;
- Bandit;
- pip-audit;
- ESLint;
- TypeScript;
- npm audit;
- Semgrep;
- Trivy;
- duplication scanners;
- dead-code adapters.

### Definition of Done v0.6

- analyzer registry/plugin architecture;
- detector selecciona analyzers aplicables;
- findings normalizados;
- stable fingerprints;
- evidence/confidence por finding;
- false-positive regression tests;
- historical reconciliation;
- tool failures no se confunden con findings.

## v0.7 — GitHub / CI / PR

Implementar provider GitHub sobre el capability contract.

Comandos objetivo:

```text
/pr
/review-pr
```

Debe cubrir:

- repository/branch state;
- PR create/read/review;
- diff inspection;
- CI/check state;
- evidence ingestion;
- task ↔ PR linking;
- release metadata;
- idempotent event ingestion;
- sync a StellarCode.

No convertir GitHub en dependencia obligatoria del core.

## v0.8 — Release / Deploy / Rollback

Implementar provider-neutral:

```text
/release
/deploy
/verificar-prod
/rollback
```

Providers iniciales previstos:

- GitHub Actions;
- SSH/custom command;
- Docker;
- Kubernetes/k3s.

Requisitos:

- approval gates;
- commit/version objetivo;
- preflight;
- migration awareness;
- rollback reference;
- smoke tests;
- post-deploy evidence;
- Deployment separado de Release.

## v0.9 — Runtime / Observability / OAuth

Integraciones:

- k6;
- Grafana;
- Prometheus;
- Netdata;
- Sentry;
- Docker runtime state;
- Kubernetes/k3s state;
- Cloudflare;
- health endpoints;
- OAuth 2.1 interactivo completo para StellarCode;
- scoped automation identities.

Performance modes:

```text
static
local_benchmark
staging_load
production_observe
```

Nunca ejecutar carga contra producción sin autorización explícita.

## v1.0 — Engineering Operating System estable

DevFlow 1.0 se considera alcanzado cuando este flujo puede funcionar end-to-end:

```bash
devflow /nuevo-proyecto
devflow /doctor
devflow /auditar
devflow /planificar "Nueva funcionalidad" --stellar

# implementación mediante agente

devflow /pr
devflow /review-pr
devflow /release
devflow /deploy production
devflow /verificar-prod
devflow /estado
devflow /siguiente
```

con:

- identidad real;
- backlog compartido;
- evidencia Git/CI;
- quality gates;
- deploy controlado;
- runtime evidence;
- audit trail;
- rollback;
- actualización automática del estado.

---

# 10. Features posteriores a v1.0

## Baselines / history

```text
/baseline
/comparar
/health-history
```

Comparar:

- auditorías;
- scores;
- findings;
- dependencias;
- performance;
- deuda;
- arquitectura.

## Architecture intelligence

```text
/arquitectura
/impacto
```

Objetivos:

- mapa de módulos;
- dependencias;
- ciclos;
- hotspots;
- blast radius;
- contratos afectados.

## Repository hygiene

```text
/repo-hygiene
/dependencias
```

Incluir:

- ramas obsoletas;
- archivos grandes;
- binarios;
- TODOs;
- dependencias abandonadas;
- upgrades;
- archivos accidentales.

## Data / APIs

```text
/db-audit
/api-audit
```

## Operations

```text
/observabilidad
/resiliencia
/costos
/release-readiness
/mvp-check
/production-check
```

## Decision records

Extender:

```bash
devflow /decision add ...
```

para generación/sync de ADR local + StellarCode.

## Automated remediation

Flujo futuro:

```text
AUDIT
  ↓
FINDING
  ↓
PLAN
  ↓
FIX
  ↓
VALIDATE
  ↓
RE-AUDIT
```

Comandos previstos:

```text
/explain <finding>
/fix <finding>
```

Nunca ejecutar fixes de alto riesgo sin revisión/aprobación.

---

# 11. Perfiles operativos previstos

DevFlow no debe aplicar el mismo estándar a todo proyecto.

Perfiles propuestos:

```text
prototype
mvp
production
enterprise
legacy-modernization
external-audit
high-security
high-traffic
```

Ejemplo:

```yaml
profile: mvp
```

Los perfiles alterarán:

- severidad;
- quality gates;
- evidencia requerida;
- minimum scores;
- tooling obligatorio;
- observabilidad;
- deploy constraints.

---

# 12. Quality gates previstos

Ejemplo objetivo:

```yaml
gates:
  pull_request:
    minimum_health: 70
    critical_security: 0

  staging:
    tests_required: true
    build_required: true

  production:
    minimum_health: 80
    critical_security: 0
    high_security: 0
    rollback_required: true
    healthcheck_required: true
```

Comando futuro:

```bash
devflow gate production
```

---

# 13. Rollout pendiente de StellarCode MCP v2

El código está integrado, pero rollout productivo debe realizarse de forma controlada.

Orden recomendado:

1. Backup de DB.
2. Deploy con writes deshabilitados.
3. Ejecutar migration `202610040001_mcp_rbac_v2`.
4. Verificar tablas/índices/roles.
5. Probar `get_mcp_identity` con usuario real.
6. Probar `list_my_projects`.
7. Verificar owner.
8. Verificar developer.
9. Verificar viewer.
10. Confirmar que una acción prohibida retorna 403/error MCP.
11. Revisar audit log.
12. Habilitar `MCP_ALLOW_WRITES=true`.
13. Probar creación/movimiento de tarea.
14. Probar gestión de miembros con owner/admin.
15. Probar DevFlow `/planificar --stellar`.
16. Deshabilitar legacy shared secret cuando todos los clientes estén migrados.

---

# 14. Riesgos conocidos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Scores con falsa precisión | Alto | Evidence Confidence + N/A |
| MCP con permisos excesivos | Crítico | RBAC server-side |
| Token filtrado | Crítico | env-only + secret scanning |
| Backlog contaminado por auditorías | Medio | explicit approval + remote-first |
| Sobrearquitectura | Alto | perfiles + Stack Fit + proportionality |
| Load test dañino | Crítico | approval gate + non-prod default |
| Rollout RBAC rompa clientes legacy | Alto | transición controlada |
| Docs desactualizadas | Medio | este roadmap como fuente global |
| Chat se convierta en fuente de verdad | Alto | Git + StellarCode + ops files |

---

# 15. Definition of Done global

Una capability DevFlow se considera **implementada** solo cuando:

- existe contrato claro;
- existe implementación;
- tiene CLI/tool/provider cuando aplica;
- tiene pruebas;
- tiene documentación;
- respeta RBAC/approval gates;
- genera evidencia;
- maneja errores;
- no expone secretos;
- no afirma más de lo que puede demostrar.

Una capability que solo tiene skill/diseño debe marcarse como **📐 diseñada**, no como implementada.

---

# 16. Próximas prioridades

## P0 — Completar rollout StellarCode v2

- migration real;
- deploy controlado;
- pruebas RBAC owner/developer/viewer;
- writes;
- retiro gradual del shared secret legacy.

## P1 — v0.6 Analyzers ← siguiente

- FastAPI/Python;
- Node/Next/React;
- Angular;
- PostgreSQL;
- Docker;
- GitHub Actions;
- analyzer registry;
- canonical Finding output;
- luego Go/Quarkus/PHP y resto del catálogo.

## P2 — v0.7 GitHub / CI / PR

- GitHub provider;
- PR read/create/review;
- checks/CI ingestion;
- evidence ingestion;
- task linking;
- event deduplication;
- StellarCode sync;
- release metadata.

## P3 — v0.8 Release / Deploy / Rollback

- release provider flow;
- staging preflight;
- deploy;
- rollback;
- migration awareness;
- post-deploy verification/evidence.

## P4 — v0.9 Runtime / Observability / OAuth

- k6;
- Grafana/Prometheus;
- Sentry;
- Docker;
- k3s/Kubernetes;
- Cloudflare;
- OAuth interactive;
- scoped automation identities.

---

# 17. Archivos relacionados

Este archivo contiene el **estado global**.

Documentos especializados:

- `README.md` — introducción y uso rápido.
- `IMPLEMENTATION_STATUS.md` — inventario corto de implementación.
- `ops/BACKLOG.md` — trabajo operativo inmediato.
- `docs/MCP_ROADMAP.md` — detalle específico del ecosistema MCP.
- `docs/DOMAIN_MODEL.md` — entidades y ownership canónico.
- `docs/FINDING_LIFECYCLE.md` — identidad, fingerprint y estados de findings.
- `docs/PROVIDER_CONTRACT.md` — interfaz/capabilities de providers.
- `docs/SYNC_MODEL.md` — autoridad, conflictos e idempotencia.
- `docs/CONFIG_AND_VERSIONING.md` — schema y compatibilidad.
- `docs/QUALITY_GATES.md` — profiles, gates y approvals.
- `docs/CLAUDE_HANDOFF.md` — secuencia recomendada para continuar desarrollo con Claude.
- `docs/COMMANDS.md` — routing de comandos.
- `docs/CLI.md` — uso del CLI.
- `scorecards/` — reglas de scoring.
- `skills/` — comportamiento canónico de cada skill.

Cuando cambie una capability importante, actualizar:

1. `DEVFLOW_ROADMAP.md`;
2. el documento especializado correspondiente;
3. `CHANGELOG.md` si es release-facing.

---

# 18. North Star

DevFlow llega a su objetivo cuando cualquier agente autorizado puede entrar a cualquier proyecto vinculado y responder con evidencia:

```text
¿Qué existe?
¿Qué está pasando?
¿Qué está mal?
¿Qué falta?
¿Qué puedo tocar?
¿Qué no puedo tocar?
¿Qué se hizo?
¿Quién lo hizo?
¿Qué evidencia existe?
¿Qué está en producción?
¿Está verificado?
¿Cuál es la siguiente acción?
```

sin depender de recordar conversaciones anteriores y sin romper los límites de seguridad, costo o complejidad del proyecto.
