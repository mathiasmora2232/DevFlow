---
name: revisar-seo
description: Audita SEO técnico y preparación para indexación de aplicaciones web.
---

# revisar-seo

## Flujo

1. Verifica indexabilidad, robots, sitemap, canonical y metadata.
2. Revisa HTML semántico y structured data cuando aplique.
3. Revisa enlaces, redirects, estados HTTP y duplicación.
4. Incorpora Core Web Vitals solo con evidencia.
5. Marca N/A para apps no públicas o no indexables intencionalmente.

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
