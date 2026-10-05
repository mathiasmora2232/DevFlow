---
name: auditar-proyecto
description: Ejecuta una auditoría integral del repositorio y genera Project Health, Stack Fit y Evidence Confidence con evidencia trazable.
---

# /auditar

## Ejecución

```bash
devflow /auditar --target .
```

## Salidas

```text
ops/reports/audit-YYYYMMDD-HHMMSS.json
ops/reports/audit-YYYYMMDD-HHMMSS.md
ops/reports/latest.json
ops/reports/latest.md
```

## Flujo

1. Leer `.devflow.yml`.
2. Detectar stack y tipo de proyecto.
3. Ejecutar análisis estático conservador.
4. Evaluar categorías aplicables del Project Health Score.
5. Marcar `N/A` cuando no exista evidencia razonable o una categoría no aplique.
6. Calcular Stack Fit por separado.
7. Calcular Evidence Confidence.
8. Aplicar caps por hallazgos críticos de seguridad.
9. Generar hallazgos con severidad + evidencia.
10. Sincronizar `ops/TRACE.md`.

## Restricción crítica

La auditoría estática **no puede** probar carga real, disponibilidad de producción ni seguridad completa.

`server_load` debe permanecer `N/A` hasta contar con métricas/runtime/k6/Grafana u otra evidencia equivalente.

## Futuras extensiones

El mismo resultado JSON será consumido por analizadores específicos y MCP/adapters de runtime sin cambiar el contrato del skill.
