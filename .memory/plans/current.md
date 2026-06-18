---
id: aifund-current-plan
type: plan
status: active
projection: task-planning
---

# AIfund Current Plan

This plan is a projection over AIfund project memory. It ports
`docs/task-specs/backlog.md` into task records grounded in memory primitives.

## Active

### Resolve the Robinhood MCP question

- id: resolve-adopt-robinhood-mcp
- status: active
- why: Robinhood shipped an agentic trading MCP and the steward asked whether
  AIfund can use it. The choice is open and affects broker and data strategy.
- next action: Choose between the read-only and live-broker alternatives. The
  read-only path is recommended first because it respects safety boundaries and
  needs no account action.
- related memory:
  - question: adopt-robinhood-mcp
  - alternative: robinhood-mcp-readonly-source
  - alternative: robinhood-mcp-live-broker
  - constraint: execution-safety-boundaries

## Proposed

### Capture first real run into replay fixtures

- id: capture-first-replay-fixture
- status: blocked
- why: Replay fixtures are the safety layer for autonomous work (backlog TA-002).
- next action: Locate the real TradingAgents log from a successful run and run
  `capture_replay_case.py`. Blocked: needs the Thunder + Ollama runtime and `uv`,
  neither available on the current machine.
- related memory:
  - goal: reliable-low-cost-paper-trading
  - decision: thunder-ollama-serving

### Design the Moomoo OpenAPI broker adapter

- id: design-moomoo-adapter
- status: proposed
- why: Moomoo simulated is the default broker but no adapter exists yet (backlog
  TA-008).
- next action: Design the Moomoo adapter interface against the existing broker
  shape (`get_account`, `get_positions`, `submit_order`); document OpenD runtime
  assumptions.
- related memory:
  - decision: moomoo-simulated-default-broker
  - decision: execution-outside-debate-graph

### Verify the Cloudflare Pages web build

- id: verify-web-build
- status: proposed
- why: The Astro scaffold exists but the build is unverified (backlog TA-010).
  npm is available on the current machine, so this is unblocked here.
- next action: Run `npm install` and `npm run build` under `apps/web`; fix
  errors; sanity-check pages.
- related memory:
  - decision: cloudflare-pages-public-site

## Done

### Bootstrap AIfund project memory

- id: bootstrap-aifund-project-memory
- status: done
- why: AIfund needed shared organizational memory under the Chronelle ontology.
- related memory:
  - episode: bootstrap-aifund-project-memory
  - episode: investigate-robinhood-mcp
