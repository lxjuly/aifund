# Thunder Compute + Ollama Workflow

## Goal

Run TradingAgents locally while using a Thunder Compute GPU instance as the model backend through the `ollama` template.

## Why this is the recommended path

- cheaper than the AWS `g6e` path we evaluated
- no custom NIM setup required
- Thunder already provides an `ollama` template
- local verification stays the same: TradingAgents runs on your machine and talks to `localhost`

## Recommended instance choice

Start with:

- mode: `prototyping`
- GPU: `A100 80GB`
- template: `ollama`

Move to `production` only if you hit compatibility issues or need stricter CUDA behavior.

## Thunder setup

1. Create an instance with the `ollama` template.
2. Connect to the instance using the Thunder VS Code extension or CLI.
3. Start the service on the instance:

```bash
start-ollama
```

4. Once connected, the Ollama API should be available locally at:

```text
http://localhost:11434
```

## Local TradingAgents setup

Start from:

```bash
cp .env.local.example .env.local
```

Recommended values:

- `TRADINGAGENTS_LLM_PROVIDER=ollama`
- `TRADINGAGENTS_BACKEND_URL=http://localhost:11434/v1`
- `TRADINGAGENTS_DEEP_MODEL=<your model name>`
- `TRADINGAGENTS_QUICK_MODEL=<your model name>`

## Local run commands

Dry-run execution:

```bash
uv run python -m cli.main exec paper NVDA 2026-04-24
```

Inspect a saved TradingAgents log:

```bash
uv run python -m cli.main exec from-log /path/to/full_states_log_2026-04-24.json
```

Capture a real run into the replay corpus:

```bash
uv run python scripts/capture_replay_case.py --source-log /path/to/full_states_log_2026-04-24.json
```

Run harnesses:

```bash
uv run python scripts/run_harnesses.py
```

## Notes

- Thunder bills per minute while the instance runs.
- Delete the instance when done to stop billing.
- If you want to preserve the environment, create a snapshot before deleting it.
