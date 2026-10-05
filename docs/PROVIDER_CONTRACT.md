# Provider Contract

Providers connect DevFlow to external systems without contaminating core logic with provider-specific branches.

## Design rule

Avoid provider checks scattered through the core:

```python
if provider == "github":
    ...
elif provider == "gitlab":
    ...
```

Core code should request capabilities. A provider declares what it supports.

## Conceptual interface

```text
Provider
  id
  version
  capabilities()

  connect()
  health()

  read(operation, input)
  execute(operation, input, approval_context?)
  evidence(operation, result)
```

Implementation may use typed Python protocols/classes, but semantics must remain provider-neutral.

## Capability naming

Use namespaced atomic capabilities.

```text
git.repo.read
git.branch.read
git.branch.create
git.pr.read
git.pr.create
git.pr.comment

ci.status.read
ci.run.trigger

release.read
release.create

deploy.read
deploy.execute
deploy.rollback

metrics.read
logs.read
alerts.read

infra.container.read
infra.container.restart

infra.k8s.read
infra.k8s.modify

dns.read
dns.modify

db.schema.read
db.migration.apply
```

## Capability classes

### Read-only

Safe by default when credentials permit it.

Examples:

```text
git.pr.read
ci.status.read
metrics.read
logs.read
```

### Shared reversible

Changes shared state but is normally recoverable.

Examples:

```text
git.branch.create
git.pr.create
git.pr.comment
ci.run.trigger
```

### Consequential / approval-gated

Examples:

```text
deploy.execute
deploy.rollback
db.migration.apply
infra.k8s.modify
dns.modify
infra.container.restart
```

Approval gates live in DevFlow policy and must also respect provider-side authorization.

## Normalized result

```text
ok
provider
operation
resource_id?
timestamp
data
evidence[]
request_id?
error?
```

Raw provider payload may be attached as metadata, but core logic should consume normalized fields.

## Normalized errors

```text
AUTHENTICATION_FAILED
FORBIDDEN
NOT_FOUND
CONFLICT
RATE_LIMITED
TIMEOUT
PROVIDER_UNAVAILABLE
INVALID_INPUT
APPROVAL_REQUIRED
UNSUPPORTED_CAPABILITY
```

Do not hide provider failures behind a generic error.

## Security

- credentials come from environment or secret manager;
- never persist raw tokens in DevFlow files;
- use least privilege;
- service identities require scoped permissions;
- production actions require both DevFlow approval and provider authorization;
- sanitize provider output before writing reports or logs.

## Initial provider priority

1. GitHub;
2. StellarCode;
3. k6;
4. Grafana/Prometheus;
5. Docker;
6. Cloudflare;
7. Kubernetes/k3s;
8. Sentry;
9. DB;
10. custom SSH.

StellarCode already exists as an operational MCP integration. Future refactoring may place it behind this capability model without breaking its current public behavior.
