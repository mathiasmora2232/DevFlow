---
name: revisar-performance
description: Evalúa rendimiento con separación explícita entre análisis estático y medición runtime.
---

# revisar-performance

## Flujo

1. Determina modo: static, local_benchmark, staging_load o production_observe.
2. Revisa bundle/rendering/queries/caching/concurrencia según stack.
3. Usa métricas runtime si están disponibles.
4. Usa k6 solo en entorno autorizado y con límites.
5. Pruebas de carga contra producción requieren aprobación explícita.
6. Reporta throughput, latencia, errores y saturación cuando se midan.

## Reglas compartidas

- Leer `.devflow.yml` cuando exista.
- Evidencia > suposición.
- Marcar `[Inferencia]` cuando una conclusión no esté confirmada.
- No declarar tests/CI/deploy/producción/seguridad/performance como exitosos sin evidencia.
- Mantener `ops/TRACE.md` después de trabajo significativo.
- Respetar approval gates.
- No guardar secretos en Markdown.
- Preferir soluciones simples y proporcionales.
- Evitar sobrearquitectura.
- Distinguir salud técnica de alineación personal de stack.
