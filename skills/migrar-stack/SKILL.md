---
name: migrar-stack
description: Diseña una migración de stack segura, incremental y justificable.
---

# migrar-stack

## Flujo

1. Lee templates/MIGRATION_PLAN.md.
2. Inventaría estado actual y objetivo.
3. Explica beneficio esperado y caso para no migrar.
4. Analiza contratos, datos, auth, CI/CD, infra y observabilidad.
5. Elige estrategia: strangler, vertical slices, paralelo o big bang justificado.
6. Define fases, pruebas, cutover, recovery y Go/No-Go.
7. Prioriza migración incremental cuando sea viable.

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
