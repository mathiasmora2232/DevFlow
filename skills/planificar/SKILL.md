---
name: planificar
description: Convierte una necesidad en un work item persistente con ID, prioridad, alcance y criterios de aceptación verificables.
---

# /planificar

## Ejecución

```bash
devflow /planificar "Agregar autenticación" \
  --type feature \
  --priority high \
  --description "Agregar login seguro para clientes" \
  --acceptance "Credenciales válidas permiten autenticación" \
  --acceptance "Credenciales inválidas no filtran información"
```

## Resultado

- Genera ID `DEV-YYYYMMDD-NNN` usando el prefijo configurado.
- Agrega el trabajo a `ops/TRACE.md`.
- Agrega una entrada en `ops/BACKLOG.md`.
- Estado inicial: `planned`.

## Antes de planificar

Para cambios no triviales considerar:

- problema;
- alcance/no alcance;
- dependencias;
- riesgo;
- seguridad;
- datos/migraciones;
- observabilidad;
- aceptación;
- pruebas;
- deploy/rollback si aplica.

## Regla de proporcionalidad

No convertir un cambio trivial en un documento ceremonial. La planificación debe reducir riesgo o ambigüedad, no generar burocracia.
