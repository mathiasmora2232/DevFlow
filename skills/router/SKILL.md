---
name: router
description: Enruta comandos e intención hacia el skill canónico correcto.
---

# router

## Flujo

1. Identifica la intención principal.
2. Usa `docs/COMMANDS.md` para comandos explícitos.
3. Si varias skills aplican, selecciona una primaria y encadena solo las necesarias.
4. No ejecutes deploy, migraciones destructivas o carga productiva como efecto secundario de una consulta.

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
