# Local Verification Workflow

## Goal

Verify as much of the TradingAgents execution path locally as possible before spending money on AWS.

The recommended backend path is now:

- Thunder Compute `ollama` template
- local TradingAgents process
- forwarded Ollama endpoint on `localhost:11434`

## Recommended setup file

Start from:

- `.env.local.example`
- `docs/task-specs/uv-usage.md` for `uv` commands
- `docs/task-specs/thunder-ollama-workflow.md` for the recommended serving path

Copy the values you need into `.env.local` or `.env`, then fill in:

- `TRADINGAGENTS_BACKEND_URL`
- `TRADINGAGENTS_DEEP_MODEL`
- `TRADINGAGENTS_QUICK_MODEL`
- your provider key if needed

For the recommended Thunder + Ollama path, you normally do not need an OpenAI API key.

## Components covered locally

- non-interactive TradingAgents execution CLI
- environment-driven config loading
- parser, policy, runner, replay, and replay-capture harnesses
- paper-trading path in dry-run mode

## CLI commands

Interactive analysis:

```bash
python -m cli.main analyze
uv run python -m cli.main analyze
```

Non-interactive execution dry run:

```bash
python -m cli.main exec paper NVDA 2026-04-24
uv run python -m cli.main exec paper NVDA 2026-04-24
```

Non-interactive execution with order submission:

```bash
python -m cli.main exec paper NVDA 2026-04-24 --submit-orders
uv run python -m cli.main exec paper NVDA 2026-04-24 --submit-orders
```

Inspect a saved log and get the replay capture command:

```bash
python -m cli.main exec from-log /path/to/full_states_log_2026-04-24.json
uv run python -m cli.main exec from-log /path/to/full_states_log_2026-04-24.json
```

## Environment variables

LLM/model settings:

- `TRADINGAGENTS_LLM_PROVIDER`
- `TRADINGAGENTS_BACKEND_URL`
- `TRADINGAGENTS_DEEP_MODEL`
- `TRADINGAGENTS_QUICK_MODEL`
- `TRADINGAGENTS_OUTPUT_LANGUAGE`
- `TRADINGAGENTS_RESEARCH_DEPTH`
- `TRADINGAGENTS_RISK_DEPTH`

Execution/risk settings:

- `TRADINGAGENTS_ALLOWED_SYMBOLS`
- `TRADINGAGENTS_MIN_CONFIDENCE`
- `TRADINGAGENTS_MAX_NOTIONAL_USD`
- `TRADINGAGENTS_MAX_PORTFOLIO_ALLOCATION_PCT`
- `TRADINGAGENTS_MAX_TOTAL_EXPOSURE_PCT`
- `TRADINGAGENTS_MAX_SPREAD_PCT`
- `TRADINGAGENTS_ALLOW_SHORT`
- `TRADINGAGENTS_ALLOW_FRACTIONAL`
- `TRADINGAGENTS_BLOCK_PDT`
- `TRADINGAGENTS_SUBMIT_ORDERS`

Moomoo OpenAPI settings:

- `MOOMOO_OPEND_HOST`
- `MOOMOO_OPEND_PORT`
- `MOOMOO_TRADING_ENV`
- `MOOMOO_TRADING_MARKET`
- `MOOMOO_SECURITY_FIRM`
- `MOOMOO_ACCOUNT_ID`
- `MOOMOO_UNLOCK_PASSWORD`

## Recommended local path

1. create and connect to a Thunder Compute `ollama` instance
2. start from `.env.local.example` and fill in the model endpoint settings
3. run `python -m cli.main exec paper SYMBOL DATE` in dry-run mode
4. inspect the saved TradingAgents log
5. capture the result into the replay corpus with `scripts/capture_replay_case.py`
6. run `uv run python scripts/run_harnesses.py`

Broker-connected paper/simulated execution is a later step. The default local verification path should work before connecting Moomoo OpenD or submitting any broker-side order.
