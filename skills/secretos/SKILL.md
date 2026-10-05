---
name: secretos
description: Busca posibles secretos y archivos sensibles en el árbol de trabajo sin imprimir credenciales completas.
---

# /secretos

## Ejecución

```bash
devflow /secretos --target .
devflow /secretos --fail-on high --target .
```

## Busca

- claves privadas;
- tokens GitHub;
- access keys AWS;
- API keys Google;
- secretos Stripe live;
- asignaciones genéricas de password/token/secret;
- `.env`, claves y certificados sensibles.

## Reglas

- Redactar siempre el valor encontrado.
- Nunca copiar secretos completos al reporte.
- Un scan limpio no demuestra ausencia total de secretos.
- Para modo profundo futuro integrar Gitleaks/Semgrep/Trivy/provider secret scanning.
