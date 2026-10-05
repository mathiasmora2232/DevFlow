---
name: preparar-pr
description: Prepara una rama para PR con validación técnica, seguridad y trazabilidad.
---

# preparar-pr

## Flujo

1. Audita diff y archivos accidentales.
2. Busca secrets y cambios no relacionados.
3. Ejecuta quality gates configurados.
4. Revisa migraciones, compatibilidad, docs y changelog.
5. Genera resumen, validación, riesgos, deploy y rollback.
6. Crea PR solo si está autorizado.

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
