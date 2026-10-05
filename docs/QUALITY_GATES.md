# Quality Gates and Profiles

Quality gates turn DevFlow recommendations into deterministic policy.

## Goals

- same input + same evidence = same gate result;
- separate recommendations from blockers;
- adapt standards to project stage;
- never gate on unavailable evidence unless policy explicitly requires that evidence.

## Profiles

Implemented canonical profiles:

```text
prototype
mvp
production
enterprise
legacy-modernization
external-audit
high-security
high-traffic
```

Profiles define defaults; projects may override explicitly.

## Gate types

Implemented gate types:

```text
pull_request
staging
production
release
```

Current command:

```bash
devflow gate production
```

## Example

```yaml
profile: production

gates:
  pull_request:
    minimum_health: 70
    critical_security: 0
    tests_required: true

  staging:
    build_required: true
    tests_required: true

  production:
    minimum_health: 80
    critical_security: 0
    high_security: 0
    rollback_required: true
    healthcheck_required: true
    verified_ci_required: true
```

## Gate result

```text
gate
result: pass | warn | blocked | unknown
checks[]
evidence[]
missing_evidence[]
timestamp
```

## Rules

- `unknown` is not automatically `pass`;
- a prototype should not inherit enterprise requirements accidentally;
- a production profile may block when mandatory evidence is missing;
- accepted-risk findings must respect waiver expiry/scope;
- critical security findings may cap Project Health according to scorecard policy;
- production operations remain approval-gated even when the gate passes.

## Separation of concerns

```text
Score = measurement
Gate = policy decision
Approval = permission to execute consequential action
```

Do not merge these concepts.
