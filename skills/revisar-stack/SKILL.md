---
name: revisar-stack
description: Evalúa el stack detectado contra el estándar DevFlow, el contexto del proyecto y el costo de cambio sin confundir preferencia con calidad.
---

# /revisar-stack

## Ejecución

```bash
devflow /revisar-stack --target .
```

Genera:

```text
ops/reports/stack-review.md
```

## Evaluar

- alineación personal;
- familiaridad del equipo;
- project fit;
- costo operativo;
- velocidad de entrega;
- soporte/ecosistema;
- costo de migración;
- flexibilidad futura.

## Recomendaciones válidas

- `keep`
- `keep_with_improvements`
- `evaluate_partial_migration`
- `migration_candidate`

## Reglas

- Project Health y Stack Fit nunca se mezclan.
- No migrar solo porque exista una alternativa preferida.
- En MVP lean, advertir sobre infraestructura sobredimensionada.
- Si se recomienda migración, encadenar `/migrar-stack` antes de ejecutar cambios.
