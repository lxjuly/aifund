# Replay Capture Workflow

## Purpose

Turn real TradingAgents portfolio-manager outputs into replay fixtures with minimal manual editing.

## Script

Use:

- `scripts/capture_replay_case.py`

## Supported inputs

- a saved TradingAgents log JSON containing `company_of_interest`, `trade_date`, and `final_trade_decision`
- a plain text file containing only the final decision text

## Example commands

From the project root:

```bash
python3 scripts/capture_replay_case.py \
  --source-text /path/to/final_trade_decision.txt \
  --symbol NVDA \
  --trade-date 2026-04-20
```

```bash
python3 scripts/capture_replay_case.py \
  --source-log ~/.tradingagents/logs/NVDA/TradingAgentsStrategy_logs/full_states_log_2026-04-20.json
```

## Defaults

The script generates:

- a default conservative account snapshot
- a default risk policy template
- an allowlist containing the captured symbol
- an expected parser outcome
- an inferred expected approval or rejection outcome based on the current risk policy

## After capture

1. inspect the appended case in `tests/harness_fixtures/replay_cases.json`
2. tighten the policy or positions if you want the replay to model a more specific scenario
3. run `python3 scripts/run_harnesses.py`
