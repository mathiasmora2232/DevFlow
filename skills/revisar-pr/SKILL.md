---
name: revisar-pr
description: Revisa PR por correctitud, seguridad, mantenibilidad, pruebas y operación.
---

# revisar-pr

## Flujo

1. Inspecciona diff y contexto relevante.
2. Clasifica blocker/high/medium/low/suggestion.
3. Prioriza bugs, regresiones, seguridad y operación.
4. Evita ruido de estilo que ya cubren herramientas.

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
