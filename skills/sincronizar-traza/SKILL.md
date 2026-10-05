---
name: sincronizar-traza
description: Sincroniza el snapshot operativo con el estado verificable de Git sin asumir merge, deploy o producción verificada.
---

# /traza

## Ejecución

```bash
devflow /traza --target . --environment local
```

Actualiza en `ops/TRACE.md`:

- timestamp;
- branch;
- revision;
- environment;
- estado básico del working tree.

## Invariantes

```text
merged != deployed
deployed != verified
verified != closed si quedan pendientes
```

## Próxima fase

Cuando existan adaptadores GitHub/CI/MCP, este skill incorporará PRs, workflows, releases y deployments como evidencia adicional manteniendo el mismo archivo de estado.
