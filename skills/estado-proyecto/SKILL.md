---
name: estado-proyecto
description: Resume el estado técnico y operativo actual con evidencia.
---

# estado-proyecto

## Flujo

1. Lee configuración y trazabilidad.
2. Inspecciona Git, tests/CI disponibles y releases cuando haya acceso.
3. Resume activo, pendiente, bloqueado, riesgos y validaciones.
4. Separa hechos de inferencias.
5. Propón máximo 5 siguientes acciones priorizadas.

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
