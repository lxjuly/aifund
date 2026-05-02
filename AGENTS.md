# AGENTS.md

## Purpose

This project hosts the TradingAgents research framework plus the execution-layer work needed for paper trading and tightly controlled live trading.

## Default Operating Mode

Operate autonomously by default.

- Execute tasks end-to-end without asking for confirmation on routine implementation details.
- Make reasonable decisions when the tradeoffs are small, reversible, or low-cost.
- Prefer concrete progress over open-ended discussion.
- Provide concise progress updates while working.

## Ask The User Before

- creating or modifying paid cloud resources that can materially increase spend
- choosing infrastructure, model, or vendor options with meaningful recurring cost impact
- using, rotating, or requesting secrets, credentials, or account access
- enabling live trading or changing anything that could place real-money trades
- taking destructive or hard-to-reverse actions
- making major architecture changes that would be expensive to unwind

## Working Norms

- Keep `TradingAgents` as the decision engine.
- Keep execution, broker access, and risk controls separate from the debate graph.
- Prefer small, reviewable changes.
- Default to Yahoo/yfinance for research unless a task explicitly upgrades the data source.
- Default to Moomoo OpenAPI paper/simulated trading before any live-trading changes.
- Prefer low-cost and reversible defaults for infrastructure.
- Prefer Infrastructure as Code over one-off console setup when practical.
- Document material design decisions in `docs/system-specs/` or `docs/task-specs/`.

## Project Layout

- `tradingagents/`: upstream framework and local extensions
- `examples/`: runnable examples and operator entrypoints
- `docs/system-specs/`: durable architecture and system design notes
- `docs/task-specs/`: narrower implementation tasks and work packages
- `tests/`: regression tests and fixture-driven harnesses
- `scripts/`: local automation entrypoints such as harness runners

## Current Direction

- Support a custom OpenAI-compatible model endpoint
- Parse final trade decisions into a structured trade intent
- Apply a hard risk-policy layer before any broker call
- Start with Moomoo OpenAPI paper/simulated trading and small-notional guardrails
- Publish the public website on Cloudflare Pages by default.
- Use harnesses to guard the parser, policy, and orchestration boundaries

## Safety Boundaries

- Treat paper trading as the default environment.
- Do not enable live broker execution by default.
- Keep strict sizing, exposure, and allowlist controls in the execution layer.
- Do not store secrets in source files.
- Prefer SSM or Secrets Manager for cloud-side secret delivery.
