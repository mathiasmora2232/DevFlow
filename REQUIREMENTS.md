# Requirements — DevFlow Core

## Objetivo

Crear un repositorio global de Skills que represente el modelo personal de trabajo del propietario del repositorio y pueda aplicarse a múltiples proyectos.

Debe estandarizar:

- planificación;
- pensamiento técnico;
- ejecución;
- revisión;
- PR;
- despliegues;
- producción;
- seguridad;
- SEO;
- rendimiento;
- calidad;
- arquitectura;
- deuda técnica;
- trazabilidad;
- migración de stack;
- evaluación de proyectos existentes;
- inicialización de proyectos nuevos.

## Requisito funcional 1 — Modelo operativo global

Todos los flujos deben respetar:

1. Entender contexto.
2. Identificar objetivo real.
3. Detectar restricciones.
4. Evaluar estado actual.
5. Elegir solución proporcional al problema.
6. Priorizar MVP/tiempo/costo cuando aplique.
7. Planificar.
8. Ejecutar cambios pequeños.
9. Validar.
10. Revisar impacto.
11. Integrar.
12. Desplegar bajo política.
13. Verificar.
14. Documentar evidencia.
15. Recomendar siguiente acción.

## Requisito funcional 2 — Comandos en español

La interfaz humana debe priorizar comandos claros en español:

`/nuevo-proyecto`, `/estado`, `/planificar`, `/ejecutar`, `/auditar`,
`/puntuar`, `/revisar-stack`, `/migrar-stack`, `/seguridad`, `/seo`,
`/performance`, `/calidad-codigo`, `/codigo-muerto`, `/deuda-tecnica`,
`/pr`, `/review-pr`, `/release`, `/deploy`, `/verificar-prod`,
`/incidente`, `/postmortem`, `/traza`, `/changelog`, `/siguiente`.

No es obligatorio traducir términos técnicos universalmente entendidos: PR, deploy, backend, frontend, stack, CI/CD, etc.

## Requisito funcional 3 — Wizard `/nuevo-proyecto`

Debe preguntar solo lo que no pueda inferir.

### Identidad
- nombre;
- tipo: frontend/backend/fullstack/API/mobile/infra/monorepo;
- nuevo o existente;
- MVP/prototipo/producción;
- criticidad;
- tráfico esperado;
- presupuesto/limitaciones.

### Backend
Opciones:
- FastAPI;
- Go;
- Node.js;
- Java Quarkus;
- PHP;
- ninguno;
- otro.

### Frontend
Opciones:
- Angular;
- Next.js;
- React;
- JavaScript/TypeScript;
- Tailwind CSS;
- ninguno;
- otro.

### Base de datos
- PostgreSQL;
- MariaDB;
- SQLite;
- ninguna;
- otra.

### Infra / DevOps
- Ubuntu Server;
- Docker;
- Cloudflare;
- Kubernetes;
- k3s;
- GitHub Actions;
- otro CI/CD;
- ninguno inicialmente.

### Observabilidad / performance
- Grafana;
- Prometheus;
- Netdata;
- Sentry;
- k6;
- ninguno inicialmente.

El wizard debe advertir si la arquitectura parece sobredimensionada para el alcance.

## Requisito funcional 4 — Auditoría 0–100

Debe producir:

- Project Health Score;
- Stack Fit Score;
- Evidence Confidence;
- score por categoría;
- hallazgos;
- severidad;
- evidencia;
- recomendaciones;
- Quick Wins;
- prioridades Now / Next / Later.

### Categorías mínimas

- seguridad;
- arquitectura;
- calidad de código;
- mantenibilidad;
- repetición/duplicación;
- código muerto;
- malas prácticas;
- pruebas;
- performance;
- carga;
- SEO;
- accesibilidad;
- base de datos;
- DevOps/CI/CD;
- observabilidad;
- resiliencia;
- documentación;
- dependencias;
- configuración/secrets.

Una categoría no aplicable debe ser `N/A` y sus pesos deben renormalizarse.

## Requisito funcional 5 — Evidencia

Cada puntuación debe indicar evidencia.

Ejemplos:
- archivo/línea;
- resultado de linter;
- tests;
- coverage;
- reporte SAST;
- dependencias;
- Lighthouse;
- k6;
- métricas Grafana;
- CI;
- configuración de servidor;
- logs.

No inferir carga real de servidor solo leyendo código.

Performance soporta cuatro modos:

1. `static`
2. `local_benchmark`
3. `staging_load`
4. `production_observe`

Las pruebas de carga contra producción requieren aprobación explícita y límites definidos.

## Requisito funcional 6 — Stack Fit

El análisis de stack debe responder:

- qué stack existe;
- qué tan alineado está;
- qué partes son adecuadas aunque no coincidan con preferencias;
- qué partes sí generan deuda/riesgo;
- costo de mantener;
- costo de migrar;
- beneficio esperado;
- recomendación: mantener / modernizar gradualmente / migrar.

Nunca recomendar migración solo porque una tecnología no sea preferida.

## Requisito funcional 7 — Migración de stack

`/migrar-stack` debe producir:

- inventario actual;
- objetivo;
- delta;
- dependencias;
- riesgos;
- compatibilidad;
- datos;
- autenticación;
- contratos API;
- CI/CD;
- infraestructura;
- observabilidad;
- fases;
- estrategia strangler/vertical slice/big bang cuando corresponda;
- pruebas;
- cutover;
- rollback;
- criterios Go/No-Go;
- costo/esfuerzo relativo;
- trazabilidad.

## Requisito funcional 8 — Trazabilidad

Mantener:

- `ops/TRACE.md`;
- `ops/BACKLOG.md`;
- `ops/RISKS.md`;
- `ops/DECISIONS.md`;
- `ops/SECURITY.md`;
- `ops/RELEASES.md`;
- `CHANGELOG.md`.

No mezclar actividad interna con changelog del producto.

## Requisito funcional 9 — PR / Deploy

PR debe revisar:

- diff;
- secretos;
- tests;
- lint;
- build;
- compatibilidad;
- DB;
- seguridad;
- documentación;
- changelog;
- impacto de deploy;
- rollback.

Deploy debe diferenciar:

`merged != deployed != verified != closed`

Producción y cambios destructivos requieren aprobación por defecto.

## Requisito funcional 10 — Reutilización

El sistema debe ser útil para:

- SmartAhorra;
- SmartISP;
- Sonora;
- nuevos proyectos;
- legacy;
- proyectos de terceros.

No codificar reglas específicas de un proyecto dentro del core.

## Requisito no funcional

- Markdown-first.
- YAML para configuración.
- Git como audit trail.
- Sin base de datos en v1.
- Sin UI en v1.
- Sin dependencia obligatoria de MCP.
- Cross-platform cuando haya scripts.
- Extensible por perfiles.
- Idempotente.
- Seguro por defecto.
