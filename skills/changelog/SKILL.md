---
name: changelog
description: Mantiene changelog de cambios visibles/relevantes de producto.
---

# changelog

## Flujo

1. Incluye Added/Changed/Fixed/Deprecated/Removed/Security.
2. No agregues debugging, investigación o mecánica interna de PR.
3. Relaciona release cuando aplique.

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
