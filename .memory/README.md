# AIfund Project Memory

This `.memory/` directory is AIfund's own organizational memory, kept inside the
AIfund repository the way `.git` keeps version history.

It uses the Chronelle ontology. Chronelle defines the shared ontology, its own
memory, and shared tooling; each project owns and stores its own memory here.

AIfund is a TradingAgents-based research and paper-trading system. The decision
engine is the TradingAgents debate graph. Execution, broker access, and risk
controls live in a separate execution layer. The near-term goal is a reliable,
low-cost paper-trading workflow rather than production trading.

## Layout

- `goals/` — intended states
- `constraints/` — boundaries on possible action
- `assumptions/` — beliefs being relied upon
- `questions/` — unresolved inquiries
- `alternatives/` — options under consideration
- `decisions/` — chosen directions
- `episodes/` — bounded units of meaningful activity
- `transitions/` — explicit, append-only state changes
- `plans/` — task-planning projection over this memory

## Conventions

Primitives carry `id`, `type`, and `status` frontmatter. Transitions are
append-only and reference the Episode that produced them. Cross-links use
`[[id]]`. Current project state is derivable by replaying transitions; episodes
group them into human-legible memory.

When a Decision embeds a belief or a boundary, capture it alongside the Decision:
record the belief as an Assumption and the boundary as a Constraint, and link them
with `[[id]]`. This keeps the implicit drivers of the system explicit and
challengeable, and avoids the assumption and constraint debt found in the
backfill episode.

Mirrors AIfund's steering docs (`AGENTS.md`, `WORKFLOW.md`,
`docs/task-specs/backlog.md`) so humans and agents share one memory across
sessions.

Source repository: `lxjuly/aifund`.
