---
name: auditar-proyecto
description: Ejecuta auditorías normalizadas, genera findings/evidence/scores y publica el resultado estructurado en StellarCode Studio.
---

# /auditar

## Objetivo

Auditar con evidencia y alimentar el estado técnico compartido del proyecto.

El Markdown es un artefacto humano. El resultado estructurado sincronizado con StellarCode es el estado operacional.

## Flujo

1. Resolver project/repository binding.
2. Leer `.devflow.yml`.
3. Detectar stack/tipo.
4. Ejecutar analyzers aplicables.
5. Emitir canonical Findings.
6. Reconciliar fingerprints/historial.
7. Calcular Project Health.
8. Calcular Stack Fit por separado.
9. Calcular Evidence Confidence.
10. Registrar missing evidence / N/A.
11. Persistir reportes locales.
12. Publicar AuditRun + findings + scores + evidence al MCP.
13. Actualizar trace/sync status.

## AuditRun remoto

Publicar conceptualmente:

```text
audit_id
project_id
repository_id?
audit_type
devflow_version
started_at
completed_at
status
score?
confidence?
findings[]
evidence[]
missing_evidence[]
```

## Auditorías especializadas

Security, secrets, docs, SEO, performance, database, dependencies, DevOps, architecture, code quality y futuras auditorías deben usar el mismo contrato y sincronizar al Hub.

## Restricciones

- No afirmar runtime health sin runtime evidence.
- No subir secretos; variables/config se sincronizan solo como metadata.
- No crear tareas automáticamente por cada finding.
- Si StellarCode no está disponible, guardar localmente y dejar sync pendiente.
- Los writes remotos deben ser idempotentes.
