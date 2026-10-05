---
name: configuracion
description: Valida y migra .devflow.yml preservando compatibilidad, seguridad y trazabilidad.
---

# /validar y config

## Objetivo

Tratar la configuración DevFlow como un contrato versionado.

## Comandos

```bash
devflow /validar
devflow config show
devflow config migrate --check
devflow config migrate
```

## Reglas

- `validate` nunca modifica archivos.
- Migraciones deben ser deterministas.
- Antes de escribir una migración se genera backup local.
- Nunca migrar secretos a YAML.
- Configuración desconocida o incompatible debe reportarse explícitamente.
- La versión actual es `schema_version: 2`.
