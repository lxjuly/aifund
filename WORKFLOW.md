---
project: TradingAgents
status_source: repo
default_mode: autonomous
human_handoff_states:
  - Human Review
  - Waiting on Secrets
  - Waiting on Budget Approval
  - Waiting on Runtime Validation
concurrency_guidance:
  max_parallel_tracks: 3
runtime_policy:
  prefer_local_verification: true
  prefer_low_cost_backends: true
  default_serving_path: thunder_ollama
  default_execution_mode: alpaca_paper
---

# TradingAgents Workflow

## Objective

Advance TradingAgents toward a reliable, low-cost paper-trading workflow with:

- TradingAgents as the decision engine
- Thunder Compute + Ollama as the recommended model-serving path
- Alpaca paper trading as the default execution environment
- harnesses and replay fixtures as the safety layer for autonomous development

## Current System Boundaries

- Do not enable live trading by default.
- Do not require paid AWS infrastructure unless explicitly approved.
- Prefer Thunder Compute over AWS for model-serving experiments.
- Prefer local dry runs before any broker submission.
- Keep execution controls outside the debate graph.

## Default Agent Behavior

- Work autonomously on routine implementation, testing, docs, and refactors.
- Prefer reversible, low-cost changes.
- Keep progress flowing without waiting on human confirmation for small decisions.
- When blocked, improve the repository so the same class of blocker is less likely next time.

## Ask For Human Input Only When

- a choice materially increases recurring spend
- a secret, credential, or account action is required
- a destructive or hard-to-reverse action is needed
- live trading might be enabled or broker behavior changes materially
- a runtime failure requires operator action on external infrastructure

## Success Criteria For Near-Term Work

The near-term goal is not “production trading.” It is:

1. get reliable real TradingAgents runs against the Thunder + Ollama backend
2. capture real outputs into replay fixtures
3. keep parser, policy, and orchestration harnesses green
4. make paper-trading runs repeatable from local commands

## Working Loop

For any task, prefer this loop:

1. inspect the relevant docs/code/tests
2. implement the smallest high-leverage improvement
3. run the narrowest useful verification
4. update docs or fixtures if behavior changed
5. hand off only if human action is genuinely required

## Preferred Verification Order

1. unit or harness tests
2. replay fixtures
3. local dry-run execution
4. real remote model invocation
5. broker-connected paper mode

## Backlog Source

Use `docs/task-specs/backlog.md` as the current prioritized work queue when no explicit task is provided.
