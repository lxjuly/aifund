# AIfund Architecture

AIfund is organized around a governed execution boundary for autonomous financial research agents.

The core thesis is simple:

```text
agent tool access is not enough;
agent intent must be mediated before execution.
```

Most agent systems secure the protocol or tool call. AIfund focuses on the transition from agent intent to executable plan.

## Execution lifecycle

```text
User / Portfolio Strategist Intent
        |
        v
Semantic Planner
        |
        v
Virtual Metadata Catalog
        |
        v
Policy and Capability Checks
        |
        v
Speculative Dry Run
        |
        v
Approved Execution
        |
        v
Recommendation + Provenance Trace
```

## Key components

### 1. Semantic catalog

The semantic catalog defines the controlled vocabulary of the system:

- entities: company, security, sector, portfolio, earnings report, news item
- metrics: revenue growth, momentum score, volatility, drawdown, sentiment score
- relationships: company -> sector, security -> company, report -> company
- policies: which agents can access which semantic objects and actions

Agents should reason over semantic objects, not arbitrary raw tables or tools.

### 2. Semantic planner

The planner converts a high-level intent into a structured execution plan.

Example intent:

```text
Analyze NVDA using fundamentals, momentum, and recent news.
```

Example plan:

```yaml
intent: analyze_security
subject: NVDA
required_entities:
  - company
  - security
  - earnings_report
  - news_item
required_metrics:
  - revenue_growth
  - momentum_score
  - sentiment_score
agents:
  - fundamental_agent
  - technical_agent
  - sentiment_agent
```

### 3. Policy mediation

Before execution, the plan is checked against explicit policies.

Policy examples:

- sentiment agents may read news and sentiment metrics, but not portfolio holdings
- risk agents may read portfolio exposure and volatility metrics
- trader agents may propose recommendations, but not execute real trades
- all plans must produce a provenance trace

### 4. Speculative dry run

The dry-run layer simulates what the plan would touch before allowing real execution.

The first implementation is a Python simulation over the virtual metadata catalog. The research direction is a WASM/WASI sandbox that provides deterministic, capability-limited speculative execution.

Dry-run output should include:

- semantic entities touched
- metrics touched
- agents invoked
- policy checks
- estimated risk level
- provenance skeleton
- approval/denial status

### 5. Governed execution

Only approved plans are allowed to invoke tools, datasets, models, or agent workflows.

The long-term design goal is to separate:

```text
reasoning
planning
validation
execution
provenance
```

instead of letting agents directly call external tools.

## MVP design

The first MVP intentionally avoids heavy infrastructure. It uses:

- YAML for semantic metadata
- Python dataclasses for plans and traces
- simple policy checks
- simulated dry runs
- existing TradingAgents workflows as the execution substrate

This keeps the system small while proving the architecture.

## Future direction

Planned extensions:

- SQLGlot-based query and expression planning
- WASM/WASI sandbox for deterministic dry runs
- lineage graph for recommendations and agent outputs
- experiment tracking for strategy versions and agent configurations
- risk-aware portfolio recommendation evaluation
- semantic policy enforcement for multi-agent workflows
