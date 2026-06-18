---
id: execution-outside-debate-graph
type: decision
status: accepted
---

# Keep Execution Outside The Debate Graph

Execution controls, broker access, and risk policy live outside the
TradingAgents debate graph.

The graph produces a decision. A separate execution layer parses it into a
structured trade intent, applies a hard risk policy, and only then may submit to
a broker.

This keeps the decision engine independent of broker choice and keeps safety
controls in one auditable place.
