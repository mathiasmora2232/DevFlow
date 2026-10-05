# DevFlow Core

**DevFlow Core** es un sistema operativo de ingeniería basado en Skills, configuración y evidencia.

Su objetivo no es imponer un framework ni reemplazar GitHub/Jira/CI/CD. Su objetivo es que cualquier agente de código (Codex, Claude Code u otro) pueda trabajar con un **modelo estable de planificación, ejecución, revisión y cierre**, independientemente del proyecto.

Pensado para reutilizarse en SmartAhorra, SmartISP, Sonora y futuros proyectos.

> **Estado global:** ver [`DEVFLOW_ROADMAP.md`](./DEVFLOW_ROADMAP.md). Ese archivo concentra lo implementado, lo parcial, lo pendiente, la matriz CLI/Skill/MCP/runtime y el camino hasta v1.0.

## Idea central

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

DevFlow separa tres cosas que no deben mezclarse:

1. **Project Health Score (0–100)**: qué tan sano está técnicamente el proyecto.
2. **Stack Fit Score (0–100)**: qué tanto se alinea con el stack y forma de trabajo configurados.
3. **Evidence Confidence (0–100)**: qué tan confiable es la evaluación según la evidencia realmente disponible.

Un proyecto puede ser sano y no usar tu stack favorito. Eso no debe penalizar su calidad técnica.

## Principios

- Evidencia > suposición.
- Producción no se declara sana porque el deploy terminó.
- Merge no significa deploy.
- Deploy no significa verificación.
- No migrar tecnología solo por moda o preferencia.
- MVP y costo/beneficio antes de sobrearquitectura.
- Escalar cuando haya señales reales.
- Cambios pequeños, verificables y reversibles.
- Acciones destructivas o de producción requieren aprobación.
- La memoria del chat nunca es la fuente de verdad del proyecto.
- Git + archivos operativos = trazabilidad.
- Si no hay evidencia para una métrica, se reporta `N/A` o baja confianza; no se inventa.

## Comandos canónicos

| Comando | Objetivo |
|---|---|
| `/nuevo-proyecto` | Wizard para definir arquitectura, stack y estándares iniciales |
| `/estado` | Resumen ejecutivo del estado técnico y operativo |
| `/doctor` | Diagnosticar entorno, herramientas y espacio libre |
| `/docs` | Auditar calidad/cobertura de documentación |
| `/secretos` | Detectar posibles secretos con salida redactada |
| `/planificar` | Convertir una necesidad en plan ejecutable |
| `/ejecutar` | Implementar trabajo aprobado |
| `/auditar` | Auditoría integral con score 0–100 |
| `/puntuar` | Recalcular scorecards a partir de evidencia |
| `/revisar-stack` | Evaluar calidad, adecuación y alineación del stack |
| `/migrar-stack` | Diseñar migración segura entre stacks |
| `/seguridad` | Revisión de seguridad |
| `/seo` | Revisión SEO/técnica web |
| `/performance` | Rendimiento frontend/backend/infra |
| `/calidad-codigo` | Complejidad, duplicación, mantenibilidad y malas prácticas |
| `/codigo-muerto` | Detectar código posiblemente no utilizado |
| `/deuda-tecnica` | Inventariar y priorizar deuda |
| `/pr` | Preparar PR |
| `/review-pr` | Revisar PR |
| `/release` | Preparar release |
| `/deploy` | Ejecutar/preparar despliegue según política |
| `/verificar-prod` | Verificar producción con evidencia |
| `/incidente` | Flujo de incidente/hotfix |
| `/postmortem` | Análisis posterior sin culpas |
| `/traza` | Sincronizar actividad, pendientes y evidencia |
| `/changelog` | Mantener cambios release-facing |
| `/siguiente` | Determinar la siguiente acción de mayor impacto |
| `/stellar-status` | Ver identidad, rol y permisos efectivos del MCP |
| `/kanban` | Leer/mover tareas del Kanban compartido en StellarCode |

Los comandos son alias humanos. La lógica real vive en `skills/*/SKILL.md`.

## Stack base soportado

### Backend
- FastAPI
- Go
- Node.js
- Java + Quarkus
- PHP
- Otro

### Frontend
- Angular
- Next.js
- React
- JavaScript/TypeScript
- Tailwind CSS
- Otro

### Datos
- PostgreSQL
- MariaDB
- SQLite
- Otro

### DevOps / Infra
- Ubuntu Server
- Docker
- Cloudflare
- Kubernetes
- k3s
- GitHub Actions
- CI/CD configurable

### Observabilidad / pruebas
- Grafana
- Prometheus
- Netdata
- Sentry
- k6

## Adopción

Cada proyecto debe tener un archivo `.devflow.yml` derivado de `config/project.example.yml`.

Los skills son globales. La configuración decide cómo se comportan en cada proyecto.

## Fases

### v0.1
Skills + reglas + scorecards + plantillas + configuración.

### v0.2
CLI para inicialización, auditoría estática y reportes.

### v0.3
CLI ampliado con Doctor, auditoría de documentación y escaneo de secretos; adaptadores Codex / Claude Code continúan evolucionando.

### v0.4
Integración operacional con StellarCode MCP: identidad real, RBAC por proyecto, Kanban compartido, miembros, roles, decisiones y planificación remote-first.

Las integraciones GitHub/CI/CD, Cloudflare, Kubernetes, Grafana y otros providers siguen en roadmap.

Ver `DEVFLOW_ROADMAP.md` y `docs/MCP_ROADMAP.md`.

## CLI ejecutable (v0.4)

Instalación local:

```bash
python -m pip install -e .
```

Flujo base:

```bash
devflow /nuevo-proyecto
devflow /auditar
devflow /puntuar
devflow /revisar-stack
devflow /planificar "Nueva implementación"
devflow /traza
devflow /estado
devflow /doctor
devflow /docs
devflow /secretos
devflow stellar-bind --project-id 10
devflow /stellar-status
devflow /proyectos
devflow /roles
devflow /miembros
devflow /kanban
devflow /decision
devflow /planificar "Nueva implementación" --stellar
devflow /traza --stellar
devflow /siguiente
```

La v0.2 realiza auditoría estática conservadora. Datos de carga real y salud de producción permanecen `N/A` hasta que existan adaptadores runtime/MCP con evidencia.

## StellarCode MCP

DevFlow v0.4 puede usar `https://api.stellarcodelabs.lat/mcp` como capa operacional compartida. El JWT del usuario se obtiene desde la variable de entorno `STELLARCODE_TOKEN`; nunca se persiste en `.devflow.yml`.

La seguridad real vive en StellarCode: usuario autenticado + membresía del proyecto + rol + permiso atómico. Git continúa siendo la fuente de evidencia técnica y StellarCode el estado vivo del backlog/Kanban.
