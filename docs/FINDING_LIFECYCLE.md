# Finding Lifecycle

Findings are durable technical issues, not disposable lines in an audit report.

## Goals

- avoid recreating the same problem on every audit;
- compare audits over time;
- distinguish new, persistent, resolved and regressed problems;
- allow explicit false positives and accepted risks;
- optionally create backlog work without polluting the Kanban.

## Canonical statuses

```text
open
acknowledged
planned
in_progress
fixed
verified
closed

accepted_risk
false_positive
suppressed
```

Recommended transition:

```text
detected
   ↓
open
   ↓
acknowledged
   ↓
planned
   ↓
in_progress
   ↓
fixed
   ↓
verified
   ↓
closed
```

Side exits:

```text
open/acknowledged → false_positive
open/acknowledged → accepted_risk
open/acknowledged → suppressed
closed            → open          # regression
```

## Stable fingerprint

Every analyzer finding must have a deterministic fingerprint.

Recommended input:

```text
analyzer_id
rule_id
repository_identity
normalized_file_path
normalized_symbol_or_location
normalized_evidence_key
```

Hash the normalized values. Do not include transient text such as timestamps, absolute machine paths or line numbers when line drift would create duplicates.

Example:

```text
sha256("python.fastapi|SEC-CORS-001|backend|app/main.py|FastAPI()|allow_origins=*")
```

## Audit reconciliation

Given previous findings and a new audit:

1. Same fingerprint seen again → update `last_seen_at`, preserve identity/history.
2. New fingerprint → create finding with `open`.
3. Previous open fingerprint absent → mark candidate `fixed`, not immediately `closed`.
4. Verification confirms absence → `verified` then `closed`.
5. Closed fingerprint reappears → reopen and mark `regressed=true`.

## Severity

Recommended canonical values:

```text
critical
high
medium
low
info
```

Severity and confidence are independent.

A high-severity low-confidence finding should not be silently treated as confirmed.

## Confidence

```text
0–100
```

Suggested source tiers:

- 95–100: authoritative runtime/provider fact or deterministic parser;
- 80–94: strong static evidence;
- 60–79: heuristic with contextual support;
- <60: weak inference; normally not a blocking gate without corroboration.

## Backlog conversion

An audit must never blindly create one task per finding.

Flow:

```text
audit
  ↓
findings
  ↓
deduplicate
  ↓
rank by severity/confidence/impact
  ↓
propose work items
  ↓
human/agent approval
  ↓
create StellarCode tasks
```

A WorkItem may reference one or many findings.

## Waivers

Accepted risks and suppressions require metadata:

```yaml
finding: FND-...
status: accepted_risk
reason: "..."
approved_by: "..."
expires_at: 2026-12-01
scope: project
```

Expired waivers return to review.

## Verification evidence

A finding can only be `verified` when evidence exists, e.g.:

- analyzer no longer reproduces;
- test proves behavior;
- dependency scan is clean;
- runtime metric confirms recovery;
- configuration provider confirms state.

"Changed the code" is not sufficient verification.

## History

Future baseline/history commands should be able to report:

```text
New findings       2
Persistent         7
Resolved           5
Regressed          1
Accepted risk      3
False positive     1
```
