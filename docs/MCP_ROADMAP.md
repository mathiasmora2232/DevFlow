# MCP Roadmap

## Decisión

MCP no es el core. Es una capa opcional de herramientas vivas. Desde v0.4 StellarCode MCP es la primera integración operacional oficial de DevFlow.

El core debe poder razonar y operar sobre archivos locales/Git sin MCP.

## ¿Cuándo agregar MCP?

Cuando sea necesario consultar o ejecutar acciones fuera del repositorio:

- GitHub/GitLab/Gitea;
- GitHub Actions/CI;
- Cloudflare;
- VPS/SSH abstraído;
- Docker;
- Kubernetes/k3s;
- Grafana/Prometheus;
- Sentry;
- bases de datos;
- gestores de tickets.

## Recursos deseables

- repositorio;
- PRs;
- issues;
- workflows;
- releases;
- deployments;
- entornos;
- métricas;
- alertas;
- logs;
- inventario de infraestructura.

## Tools deseables

### Read-only
- `get_project_state`
- `get_ci_state`
- `get_deployment_state`
- `get_metrics`
- `get_alerts`
- `get_k8s_health`

### Shared reversible
- `create_branch`
- `create_pr`
- `comment_pr`
- `trigger_staging`

### Production / approval-gated
- `deploy_production`
- `rollback_production`
- `apply_migration`
- `restart_service`
- `modify_dns`
- `modify_kubernetes`

## Seguridad

El MCP debe implementar scopes y approval gates. Nunca usar una tool de producción como efecto secundario de un skill de lectura.

## StellarCode v0.4

Implementado:

- binding por `project_id`;
- JWT real vía variable de entorno;
- identidad MCP;
- RBAC por proyecto;
- Kanban compartido;
- planificación remote-first;
- snapshot de traza;
- siguiente acción desde backlog vivo;
- activity/audit log por usuario, cliente y request.

Pendiente después del v0.4:

- OAuth 2.1 interactivo completo para clientes que no acepten bearer token manual;
- GitHub/CI como evidencia automática;
- Grafana/k6/Cloudflare/k3s runtime adapters.
