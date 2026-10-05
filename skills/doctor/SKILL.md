---
name: doctor
description: Diagnostica si el entorno local está listo para trabajar con DevFlow y el stack detectado.
---

# /doctor

## Ejecución

```bash
devflow /doctor --target .
devflow /doctor --strict --target .
```

## Revisa

- Python runtime;
- Git;
- repositorio Git;
- `.devflow.yml`;
- permisos de escritura;
- espacio libre;
- tooling relevante según stack detectado.

Menos de 1 GB libre es blocker. Menos de 5 GB genera warning.

`--strict` devuelve código distinto de cero si existe un blocker, útil en automatización.
