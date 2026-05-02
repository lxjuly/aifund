# Harness Engineering for TradingAgents

## Goal

Build small, mechanical feedback loops that let agents modify this repository safely and autonomously.

This follows the approach described in OpenAI's "Harness engineering: leveraging Codex in an agent-first world" post:

- keep the repository legible
- encode constraints mechanically
- use the knowledge base as the system of record
- prefer narrow harnesses that catch regressions early

Source:
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)

## Principles

- Start with the highest-leverage failure surfaces, not broad end-to-end automation first.
- Prefer deterministic harnesses over subjective prompts where possible.
- Keep fixtures versioned in-repo so agents can reason over them directly.
- Use harnesses as acceptance criteria for future autonomous changes.
- Add narrow, composable checks before adding expensive live integrations.

## Initial Harness Set

### 1. Signal parser harness

Purpose:
- verify that the final portfolio-manager prose is converted into a stable `TradeIntent`

Checks:
- rating extraction
- action normalization
- confidence extraction when present
- thesis excerpt generation
- rejection when no supported rating exists

### 2. Risk policy harness

Purpose:
- ensure the execution gate remains conservative and predictable

Checks:
- allowlist enforcement
- confidence threshold enforcement
- no-short behavior
- max exposure enforcement
- hold behavior

### 3. Runner dry-run harness

Purpose:
- validate the orchestration from graph output to policy decision to broker submission

Checks:
- approved buy path submits an order
- hold path does not submit an order
- unconfigured path fails closed

### 4. Replay harness

Purpose:
- replay archived final portfolio-manager decisions through the same parser, policy, and runner path

Checks:
- realistic decision text still parses correctly
- policy outcomes stay stable for known cases
- runner behavior remains aligned with expected order/no-order outcomes

### 5. Replay capture harness

Purpose:
- make it cheap to turn a real TradingAgents output into a versioned replay fixture

Checks:
- capture from a saved log JSON works
- capture from a raw text file works
- generated fixtures remain compatible with the replay harness schema

## Why these harnesses first

These cover the first irreversible boundary:

- LLM output becomes structured intent
- structured intent becomes permissioned execution
- execution orchestrator decides whether a broker call happens

This is the narrowest place where a mistake can turn model slop into a real trade, so it deserves the earliest mechanical harness coverage.

## Near-Term Extensions

- fixture-based replay harness for archived final decisions
- quote/spread harness with realistic market snapshots
- Moomoo OpenAPI adapter response-shape harness with recorded OpenD/SDK payloads
- scheduled paper-trading replay harness using a fixed symbol/date matrix
- docs freshness checks for execution architecture and live-trading boundaries
