---
name: docs
description: Audita si el proyecto documenta lo necesario para ser entendido, ejecutado, operado y mantenido.
---

# /docs

## Ejecución

```bash
devflow /docs --target .
devflow /docs --min-score 80 --target .
```

## Revisa

- README;
- instalación/setup;
- arquitectura;
- API/OpenAPI cuando aplica;
- variables de entorno;
- despliegue/rollback cuando aplica;
- ejecución de pruebas.

Las áreas no aplicables son N/A y no penalizan el score.
