---
name: incidente
description: Gestiona un incidente priorizando estabilización, evidencia y mínimo blast radius.
---

# incidente

## Flujo

1. Registra síntomas, timestamps e impacto.
2. Estabiliza antes de refactorizar.
3. Identifica mitigación mínima.
4. Valida hotfix.
5. Despliega bajo política.
6. Verifica recuperación.
7. Genera seguimiento para root cause.

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
