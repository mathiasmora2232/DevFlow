---
name: postmortem
description: Genera postmortem técnico sin buscar culpables.
---

# postmortem

## Flujo

1. Construye timeline basado en evidencia.
2. Describe impacto, detección, respuesta y recuperación.
3. Identifica causas técnicas y sistémicas.
4. Define acciones preventivas verificables con owner/prioridad.
5. Evita acciones vagas como 'tener más cuidado'.

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
