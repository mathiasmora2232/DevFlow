---
name: calidad-codigo
description: Analiza legibilidad, complejidad, duplicación, consistencia, errores y mantenibilidad.
---

# calidad-codigo

## Flujo

1. Detecta hotspots y funciones/componentes excesivamente complejos.
2. Busca lógica duplicada y abstrae solo cuando haya beneficio claro.
3. Evalúa manejo de errores, typing, naming y convenciones.
4. Prioriza problemas que aumentan costo de cambio o riesgo.

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
