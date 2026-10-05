---
name: siguiente-accion
description: Determina la próxima acción de mayor valor a partir del estado del proyecto.
---

# siguiente-accion

## Flujo

1. Considera blockers, riesgos, dependencias, valor, esfuerzo y criticidad.
2. Prioriza trabajo que desbloquea otros.
3. Propón una acción principal y hasta dos alternativas.
4. No inventes urgencia.

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
