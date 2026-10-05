---
name: puntuar-proyecto
description: Publica o recalcula los scores del proyecto a partir de evidencia de auditoría sin convertir desconocidos en aprobados.
---

# /puntuar

## Ejecución

```bash
devflow /puntuar --target .
```

Forzar auditoría fresca:

```bash
devflow /puntuar --target . --refresh
```

## Scores

### Project Health Score
Calidad técnica del proyecto usando pesos renormalizados cuando una categoría es `N/A`.

### Stack Fit Score
Alineación del stack con estándares/preferencias y adecuación al contexto.

### Evidence Confidence
Confianza de la evaluación. Un Health alto con Confidence bajo no debe presentarse como conclusión fuerte.

## Reglas

- No asignar 100 a categorías desconocidas.
- No penalizar como mala calidad una tecnología solo por no ser preferida.
- Hallazgo crítico de seguridad puede limitar el Health global.
- Performance/runtime sin medición debe mantener confianza baja o `N/A`.
