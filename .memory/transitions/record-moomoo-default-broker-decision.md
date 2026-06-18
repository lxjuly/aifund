---
id: record-moomoo-default-broker-decision
type: transition
episode: bootstrap-aifund-project-memory
operation: create
target_type: decision
target_id: moomoo-simulated-default-broker
---

# Record Moomoo Default Broker Decision

## Rationale

The broker direction had pivoted from Alpaca to Moomoo OpenAPI simulated, but
this was not recorded as a decision with provenance.

## Before

The pivot lived in `SESSION_HANDOFF.md` and the backlog (TA-008) only.

## After

AIfund records Moomoo OpenAPI simulated as the default broker, superseding
Alpaca, with simulated trading as the default execution path.

## Evidence

- `docs/system-specs/moomoo-openapi.md`
- `docs/task-specs/backlog.md` (TA-008)
- `.memory/decisions/moomoo-simulated-default-broker.md`
