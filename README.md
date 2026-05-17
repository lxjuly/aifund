# AIfund

**AIfund is a governed semantic execution platform for autonomous financial intelligence agents.**

This project explores how multi-agent financial research systems can move beyond direct tool calling into a safer execution model:

```text
agent intent
  -> semantic planning
  -> policy-aware validation
  -> speculative dry-run
  -> governed execution
  -> lineage-backed recommendation
```

The goal is not to build a black-box trading bot. The goal is to build a platform substrate for trusted financial research agents: semantic catalogs, policy mediation, provenance, experimentation, and eventually WASM-based execution sandboxes that can validate agent-generated plans before they touch real data or trading workflows.

> Research and educational use only. This repository is not financial, investment, or trading advice.

## Why this exists

Most AI trading demos follow a simple pattern:

```text
LLM -> market data tools -> buy/sell recommendation
```

That architecture is hard to trust. It does not explain which entities were used, which policies applied, which datasets were touched, whether the plan was semantically valid, or how downstream agents should trust the result.

AIfund is designed around a different boundary:

```text
intent -> governed execution plan
```

The platform direction is inspired by data platforms, semantic layers, query planners, policy engines, and runtime isolation systems.

## Target architecture

```text
                    Portfolio Strategist
                             |
                    semantic task planning
                             |
        +--------------------+--------------------+
        |                    |                    |
 Fundamental Agent     Sentiment Agent      Technical Agent
        |                    |                    |
        +--------------------+--------------------+
                             |
                   Semantic Execution Layer
                             |
                  SQL / logical plan compiler
                             |
                Policy, lineage, and cost checks
                             |
              WASM speculative dry-run sandbox
                             |
                    Approved execution
                             |
             Financial datasets / tools / cache
                             |
             Recommendation + provenance output
```

## MVP roadmap

### 1. Semantic catalog

Define financial entities, metrics, relationships, and agent permissions as explicit metadata.

```text
semantic/
  entities.yaml
  metrics.yaml
  policies.yaml
  catalog.py
```

### 2. Governed runtime

Introduce a lightweight planning and validation layer between agents and execution.

```text
runtime/
  planner.py
  policy_checker.py
  dry_run.py
  execution_trace.py
```

### 3. Speculative execution

Dry-run agent-generated plans against a virtual metadata catalog before real execution. The first version is a Python simulation; the intended research direction is a WASM/WASI sandbox for deterministic, capability-limited execution.

### 4. Recommendation and experimentation loop

Track strategy versions, agent configurations, features, recommendations, outcomes, and risk metrics so the system becomes an experimentation platform rather than a one-off prediction demo.

### 5. Lineage and provenance

Every recommendation should be explainable through an execution trace:

```text
recommendation
  -> strategist agent
  -> analyst agents
  -> semantic entities and metrics
  -> datasets and source tools
  -> policy checks
```

## Current foundation

This repository currently builds on the open-source TradingAgents framework, which provides a multi-agent financial trading workflow with analyst, researcher, trader, risk, and portfolio-manager roles. AIfund extends that base toward governed semantic execution and trusted agent runtime infrastructure.

## Upstream attribution

This project is derived from [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents), an Apache-2.0 licensed multi-agent LLM financial trading framework.

If you use the upstream TradingAgents work, please cite:

```bibtex
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework},
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138},
}
```

## Installation

```bash
uv sync
uv run python -m cli.main analyze
```

For the original TradingAgents CLI and package usage, see the upstream project documentation.
