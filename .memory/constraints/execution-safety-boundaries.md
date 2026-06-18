---
id: execution-safety-boundaries
type: constraint
status: active
---

# Execution Safety Boundaries

These boundaries bound all AIfund execution work.

- Paper and simulated trading are the default environment.
- Live broker execution is not enabled by default.
- Execution, broker access, and risk controls stay separate from the debate
  graph.
- A hard risk-policy layer applies before any broker call.
- Strict sizing, exposure, and allowlist controls live in the execution layer.
- Prefer local dry runs before any broker submission.
- Prefer low-cost, reversible infrastructure.
- Secrets never live in source; prefer SSM or Secrets Manager for cloud-side
  delivery.

Crossing any boundary requires explicit human approval.
