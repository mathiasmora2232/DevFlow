---
name: deploy
description: Prepara o ejecuta un despliegue respetando ambientes y approval gates.
---

# deploy

## Flujo

1. Confirma versión/commit objetivo.
2. Ejecuta preflight.
3. Comprueba migrations/backups/rollback si aplica.
4. Producción requiere aprobación por defecto.
5. Registra resultado.
6. Encadena verificar-produccion después del deploy.

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
