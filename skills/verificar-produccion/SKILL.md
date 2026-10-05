---
name: verificar-produccion
description: Comprueba que la versión desplegada funciona realmente en producción.
---

# verificar-produccion

## Flujo

1. Confirma commit/version.
2. Revisa health checks.
3. Ejecuta smoke tests autorizados.
4. Revisa logs/métricas/alertas disponibles.
5. Valida migrations cuando aplique.
6. Solo marca verified con evidencia.

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
