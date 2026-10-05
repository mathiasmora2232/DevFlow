# DevFlow CLI

## Install

```bash
python -m pip install -e .
```

## Commands

```bash
devflow /nuevo-proyecto
devflow /detectar
devflow /auditar
devflow /puntuar
devflow /revisar-stack
devflow /planificar "Agregar autenticación" --type feature --priority high \
  --acceptance "Login válido retorna sesión" \
  --acceptance "Credenciales inválidas no filtran información"
devflow /traza
devflow /estado
devflow /doctor
devflow /docs
devflow /secretos
```

English aliases are also accepted:

```bash
devflow init
devflow detect
devflow audit
devflow score
devflow stack-review
devflow plan "..."
devflow trace
devflow status
```

## Current audit mode

v0.2 implements a conservative **static audit**. It can score repository evidence, but it intentionally returns `N/A` or low confidence for things that require runtime proof.

`server_load` stays `N/A` until future runtime/k6/Grafana adapters provide evidence.

## Safety

The v0.2 CLI does not deploy, push, mutate infrastructure, or execute production load tests. Those workflows remain skills/policies until explicit adapters are added.

## Doctor

```bash
devflow /doctor
devflow /doctor --strict
```

Revisa Python, Git, repositorio, `.devflow.yml`, permisos de escritura, espacio libre y herramientas relevantes del stack. Menos de 1 GB libre es blocker; menos de 5 GB genera warning.

## Documentation audit

```bash
devflow /docs
devflow /docs --min-score 80
```

Evalúa README, setup, arquitectura, API, variables de entorno, despliegue y pruebas según aplicabilidad.

## Secrets scan

```bash
devflow /secretos
devflow /secretos --fail-on high
```

Busca patrones de credenciales y archivos sensibles. Los valores se redactan en consola/reportes. `--fail-on` permite usarlo como quality gate en CI.
