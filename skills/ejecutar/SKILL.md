---
name: ejecutar
description: Implementa un trabajo aprobado siguiendo el plan y calidad configurada.
---

# ejecutar

## Flujo

1. Resuelve el work ID.
2. Inspecciona solo contexto relevante.
3. Implementa el cambio más pequeño completo.
4. Agrega/actualiza pruebas.
5. Ejecuta quality gates configurados.
6. Actualiza trace y pendientes.
7. Detente antes de acciones remotas o producción si requieren aprobación.

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
