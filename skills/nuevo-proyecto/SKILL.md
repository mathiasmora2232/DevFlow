---
name: nuevo-proyecto
description: Inicializa un proyecto nuevo o adopta DevFlow en uno existente mediante detección de stack, wizard y configuración persistida.
---

# /nuevo-proyecto

## Objetivo

Crear `.devflow.yml` y la estructura `ops/` sin adivinar arquitectura ni sobrescribir estado existente.

## Ejecución preferida

```bash
devflow /nuevo-proyecto --target .
```

Para automatización no interactiva:

```bash
devflow /nuevo-proyecto --target . --non-interactive \
  --name "Proyecto" --stage mvp --backend fastapi \
  --frontend nextjs --database postgresql
```

## Flujo operativo

1. Ejecutar primero detección del repositorio.
2. Si el repo existe, usar los valores detectados como defaults, no como verdades absolutas.
3. Preguntar únicamente datos no inferibles: etapa, criticidad, tráfico, presupuesto y decisiones de stack.
4. Evaluar proporcionalidad: advertir sobre microservicios/Kubernetes/k3s prematuros en prototipos/MVP lean.
5. Crear `.devflow.yml`.
6. Crear `ops/TRACE.md`, `BACKLOG.md`, `RISKS.md`, `SECURITY.md`, `RELEASES.md` y `CHANGELOG.md` solo si faltan.
7. Sincronizar la traza con Git.
8. No sobrescribir `.devflow.yml` salvo solicitud explícita `--force`.

## Estándares disponibles

Backend: FastAPI, Go, Node.js, Java/Quarkus, PHP, otro/ninguno.

Frontend: Angular, Next.js, React, JavaScript/TypeScript, Tailwind como styling.

Datos: PostgreSQL, MariaDB, SQLite.

Infra: Ubuntu Server, Docker, Cloudflare, Kubernetes, k3s, GitHub Actions.

Observabilidad/performance: Grafana, Prometheus, Netdata, Sentry, k6.

## Salida esperada

- Configuración reproducible.
- Stack detectado + stack elegido.
- Advertencias de sobrearquitectura cuando haya evidencia.
- Traza inicial.

## Reglas

- Evidencia > suposición.
- `[Inferencia]` para conclusiones no confirmadas.
- No recomendar Kubernetes por defecto.
- No almacenar secretos.
