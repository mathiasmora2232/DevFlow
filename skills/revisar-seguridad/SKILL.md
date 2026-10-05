---
name: revisar-seguridad
description: Revisa seguridad de código, dependencias, configuración e infraestructura.
---

# revisar-seguridad

## Flujo

1. Revisa authn/authz, inputs, secrets, inyección, SSRF, uploads/path traversal si aplican.
2. Revisa CORS/CSRF/sesiones/headers según arquitectura.
3. Revisa dependencias y logging sensible.
4. Revisa permisos de DB e infraestructura.
5. Clasifica hallazgos y registra en ops/SECURITY.md.
6. Declara alcance y limitaciones.

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
