# uv Usage

## Goal

Use `uv` as the default local runner for TradingAgents development, harnesses, and the local execution workflow.

## Initial setup

From the project root:

```bash
cd /Users/youmiss/workplace/TradingAgents
uv sync
```

## Recommended environment setup

Start from:

```bash
cp .env.local.example .env.local
```

Then fill in at least:

- `TRADINGAGENTS_BACKEND_URL`
- `TRADINGAGENTS_DEEP_MODEL`
- `TRADINGAGENTS_QUICK_MODEL`
- your provider key if needed

If you follow the recommended Thunder path, see:

- `docs/task-specs/thunder-ollama-workflow.md`

## Common commands

Interactive CLI:

```bash
uv run python -m cli.main analyze
```

Non-interactive dry-run execution:

```bash
uv run python -m cli.main exec paper NVDA 2026-04-24
```

Execution with broker submission:

```bash
uv run python -m cli.main exec paper NVDA 2026-04-24 --submit-orders
```

Inspect a saved TradingAgents log:

```bash
uv run python -m cli.main exec from-log /path/to/full_states_log_2026-04-24.json
```

Run harnesses:

```bash
uv run python scripts/run_harnesses.py
```

Capture a replay case from a saved log:

```bash
uv run python scripts/capture_replay_case.py --source-log /path/to/full_states_log_2026-04-24.json
```

Capture a replay case from a plain text file:

```bash
uv run python scripts/capture_replay_case.py \
  --source-text /path/to/final_trade_decision.txt \
  --symbol NVDA \
  --trade-date 2026-04-24
```

## Notes

- Run all commands from the project root unless you know you need a different working directory.
- `uv run` uses the environment created by `uv sync`, so you do not need to activate a separate virtualenv manually.
- The recommended low-cost path is: Thunder `ollama` instance, dry-run execution, inspect logs, capture replay cases, then run harnesses.
