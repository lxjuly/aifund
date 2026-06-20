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

### Capture the NVDA run into replay fixtures

- id: capture-nvda-replay
- status: proposed
- why: The NVDA run produced a real full-states log; backlog TA-002 wants a real
  replay fixture, and this unblocks it.
- next action: Run
  `uv run python scripts/capture_replay_case.py --source-log ~/.tradingagents/logs/NVDA/TradingAgentsStrategy_logs/full_states_log_2026-06-17.json`
  then re-run the harness suite.
- related memory:
  - episode: run-nvda-research-pass
  - goal: reliable-low-cost-paper-trading

### Wire the discovery shortlist into research (funnel stage two)

- id: wire-discovery-into-research
- status: proposed
- why: The screener shortlists candidates but nothing yet feeds them into the
  debate graph. Closing the funnel makes "what to buy" end-to-end.
- next action: Take the top-N shortlist from `screen_candidates.py` and run the
  research graph per name, then rank the resulting buy decisions. Needs a model
  backend (Anthropic key or Thunder + Ollama).
- related memory:
  - goal: equity-discovery
  - decision: discovery-funnel-multifactor-screener
  - decision: anthropic-research-backend

### Broaden and harden the screener

- id: broaden-screener
- status: proposed
- why: The first screen uses a curated 30-name universe and best-effort
  fundamentals.
- next action: Support a larger universe (for example index membership), add
  liquidity filters, and make value/quality fetch more robust.
- related memory:
  - decision: discovery-funnel-multifactor-screener

### Wire Robinhood quotes into pre-trade context

- id: wire-robinhood-quotes
- status: proposed
- why: `RobinhoodQuoteSource` exists but nothing consumes it yet; the risk policy
  already accepts a `QuoteSnapshot` for spread checks.
- next action: Optionally feed `RobinhoodQuoteSource.get_quote` into the runner's
  pre-trade quote, behind config, defaulting off. Add a real MCP caller only with
  steward approval (account setup).
- related memory:
  - decision: adopt-robinhood-mcp-readonly
  - decision: execution-outside-debate-graph

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

### Run the first Anthropic-backed research pass

- id: run-anthropic-research-pass
- status: done
- why: Proving a real deep-research run on a reachable backend was the milestone
  for the near-term goal.
- related memory:
  - episode: run-nvda-research-pass
  - decision: anthropic-research-backend

### Build the discovery screener

- id: build-discovery-screener
- status: done
- why: TradingAgents analyzes a given ticker but could not surface candidates;
  the steward wanted to try the "what to buy" use case.
- related memory:
  - goal: equity-discovery
  - decision: discovery-funnel-multifactor-screener
  - episode: build-discovery-screener

### Build the Robinhood read-only data source

- id: build-robinhood-readonly-source
- status: done
- why: The Robinhood MCP question resolved to a read-only data source, which
  needed an implementation.
- related memory:
  - episode: build-robinhood-readonly-source
  - decision: adopt-robinhood-mcp-readonly

### Resolve the Robinhood MCP question

- id: resolve-adopt-robinhood-mcp
- status: done
- why: The choice of whether and how to use Robinhood's MCP was open and affected
  broker and data strategy.
- related memory:
  - decision: adopt-robinhood-mcp-readonly
  - episode: resolve-robinhood-mcp-question
  - question: adopt-robinhood-mcp

### Bootstrap AIfund project memory

- id: bootstrap-aifund-project-memory
- status: done
- why: AIfund needed shared organizational memory under the Chronelle ontology.
- related memory:
  - episode: bootstrap-aifund-project-memory
  - episode: investigate-robinhood-mcp
