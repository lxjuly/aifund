# AIfund

**AIfund is a governed recommendation and analytics platform for autonomous financial intelligence agents.**

This project explores how multi-agent financial research systems can move beyond direct tool calling into a safer execution model:

```text
agent intent
  -> semantic planning
  -> policy-aware validation
  -> speculative dry-run
  -> governed execution
  -> lineage-backed recommendation
```

The goal is not to build a black-box trading bot.

The goal is to build a platform substrate for trusted financial intelligence systems:
- semantic catalogs
- policy mediation
- recommendation pipelines
- provenance and lineage
- experimentation loops
- governed execution runtimes
- eventually WASM-based execution sandboxes

> Research and educational use only. This repository is not financial, investment, or trading advice.

---

## Why this exists

Most AI trading demos follow a simple pattern:

```text
LLM -> market data tools -> buy/sell recommendation
```

That architecture is difficult to trust because it does not explain:
- which entities were used
- which policies applied
- which datasets were touched
- whether the plan was semantically valid
- how downstream systems should trust the output

AIfund is designed around a different boundary:

```text
intent -> governed execution plan
```

The platform direction is inspired by:
- recommendation systems
- semantic layers
- governed analytics platforms
- query planners
- policy engines
- runtime isolation systems

---

## Architecture

See:

- [docs/architecture-diagram.md](docs/architecture-diagram.md)

Core concepts:

```text
Portfolio Mixer
  -> candidate retrieval
  -> multi-agent signal generation
  -> semantic validation
  -> policy-aware dry run
  -> ranking and selection
  -> recommendation provenance
```

---

## Multi-agent philosophy

Agents in AIfund are not intended to directly execute trades.

Instead, agents act as:

```text
specialized semantic signal generators
```

Examples:
- Fundamental Agent
- Sentiment Agent
- Technical Agent
- Risk Agent
- Portfolio Strategist

Agents generate structured signals which are then:
- validated through semantic policies
- enriched with metadata
- ranked and filtered
- traced through provenance
- evaluated through experimentation loops

This architecture separates:

```text
reasoning
selection
execution
```

instead of collapsing them into a single LLM interaction.

---

## Governed research demo

A minimal governed recommendation flow is available in:

```text
examples/governed_research_demo.py
```

The current demo shows:

```text
intent
  -> semantic plan
  -> governed dry run
  -> recommendation selection
  -> provenance trace
```

Run locally:

```bash
python examples/governed_research_demo.py
```

---

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

### 3. Recommendation pipeline

Build a recommendation system inspired by production ranking and experimentation platforms.

```text
candidate retrieval
  -> feature hydration
  -> ranking
  -> filtering
  -> selection
```

### 4. Experimentation and feedback

Track:
- strategy versions
- recommendation outcomes
- portfolio risk
- hit rate
- drawdown
- agent configurations

so the system evolves into an experimentation platform rather than a one-off prediction demo.

### 5. Speculative execution research

Dry-run agent-generated plans against a virtual metadata catalog before real execution.

The initial implementation is Python-based; the longer-term research direction explores WASM/WASI-based capability-limited execution.

---

## Current foundation

This repository currently builds on the open-source TradingAgents framework, which provides a multi-agent financial trading workflow with analyst, researcher, trader, risk, and portfolio-manager roles.

AIfund extends that foundation toward:
- governed semantic execution
- recommendation infrastructure
- experimentation systems
- trusted analytical workflows
- intelligent platform runtime concepts

---

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

---

## Installation

```bash
uv sync
python examples/governed_research_demo.py
```

For the original TradingAgents CLI and package usage, see the upstream project documentation.
