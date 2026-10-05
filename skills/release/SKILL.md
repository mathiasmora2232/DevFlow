---
name: release
description: Prepara una release con versión, changelog, quality gates y readiness.
---

# release

## Flujo

1. Define contenido de release.
2. Confirma checks obligatorios.
3. Revisa migrations/rollback.
4. Actualiza changelog y release record.
5. Publica solo bajo política/autorización.

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
