# Command Router

Los slash commands son la interfaz humana/canónica. El CLI v0.5 acepta directamente varios de ellos como argumentos (`devflow /auditar`).

## Operativos en CLI v0.5

| Comando | Alias CLI | Skill |
|---|---|---|
| `/nuevo-proyecto` | `init` | `nuevo-proyecto` |
| `/estado` | `status` | `estado-proyecto` |
| `/planificar` | `plan` | `planificar` |
| `/auditar` | `audit` | `auditar-proyecto` |
| `/puntuar` | `score` | `puntuar-proyecto` |
| `/revisar-stack` | `stack-review` | `revisar-stack` |
| `/traza` | `trace` | `sincronizar-traza` |
| `/detectar` | `detect` | detector interno |
| `/doctor` | `doctor` | `doctor` |
| `/docs` | `docs` | `docs` |
| `/secretos` | `secrets` | `secretos` |
| `/stellar-status` | `stellar-status` | `stellarcode-sync` |
| `/proyectos` | `stellar-projects` | `stellarcode-sync` |
| `/roles` | `roles` | `stellarcode-sync` |
| `/miembros` | `members` | `stellarcode-sync` |
| `/decision` | `decision` | `stellarcode-sync` |
| `/kanban` | `kanban` | `stellarcode-sync` |
| `/siguiente` | `next` | `siguiente-accion` |
| `/validar` | `validate` | `configuracion` |
| `/findings` | `findings` | `findings` |
| `/gate` | `gate` | `gate` |

## Skills disponibles; automatización CLI/provider pendiente

| Comando | Skill |
|---|---|
| `/ejecutar` | `ejecutar` |
| `/migrar-stack` | `migrar-stack` |
| `/seguridad` | `revisar-seguridad` |
| `/seo` | `revisar-seo` |
| `/performance` | `revisar-performance` |
| `/calidad-codigo` | `calidad-codigo` |
| `/codigo-muerto` | `codigo-muerto` |
| `/deuda-tecnica` | `deuda-tecnica` |
| `/pr` | `preparar-pr` |
| `/review-pr` | `revisar-pr` |
| `/release` | `release` |
| `/deploy` | `deploy` |
| `/verificar-prod` | `verificar-produccion` |
| `/incidente` | `incidente` |
| `/postmortem` | `postmortem` |
| `/changelog` | `changelog` |
| `/siguiente` | `siguiente-accion` |

La lógica canónica siempre vive en `skills/*/SKILL.md`; el CLI y futuros MCP/adapters son ejecutores, no fuentes de reglas duplicadas.
