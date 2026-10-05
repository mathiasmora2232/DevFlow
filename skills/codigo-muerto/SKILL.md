---
name: codigo-muerto
description: Detecta código posiblemente no utilizado y prepara eliminación segura.
---

# codigo-muerto

## Flujo

1. Usa herramientas del stack cuando estén disponibles.
2. Contrasta imports/exports/rutas/config/reflection antes de declarar muerto.
3. Clasifica como confirmed, probable o uncertain.
4. No elimines código dinámico/reflection-based sin evidencia suficiente.
5. Propón eliminación en cambios pequeños.

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
