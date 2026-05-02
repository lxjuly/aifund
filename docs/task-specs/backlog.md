# Backlog

## Purpose

This is the lightweight, repo-local backlog for Symphony-style autonomous work.

Each task should be treated as a deliverable. Agents should pick from the highest-priority unblocked task first.

## Status Meanings

- `Ready`: unblocked and safe to work autonomously
- `Waiting on Human`: needs user action such as secrets, spending, or runtime intervention
- `Done`: completed enough for current goals

## Priority Queue

### TA-001: Complete first successful real dry-run execution

- Status: `Ready`
- Goal: run `uv run python -m cli.main exec paper SYMBOL DATE` successfully against Thunder + Ollama
- Done when:
  - a real run completes
  - a TradingAgents log is written
  - execution summary is captured

### TA-002: Capture first real output into replay fixtures

- Status: `Ready`
- Depends on: `TA-001`
- Goal: append a real `final_trade_decision` to `tests/harness_fixtures/replay_cases.json`
- Done when:
  - `capture_replay_case.py` is used on a real log
  - replay harness remains green

### TA-003: Tune split-model configuration for speed

- Status: `Ready`
- Goal: use a smaller quick model and a stronger deep model to reduce runtime
- Done when:
  - the recommended config is documented
  - at least one faster real run is validated

### TA-004: Improve runtime observability for local execution

- Status: `Ready`
- Goal: make long-running `exec paper` runs easier to inspect
- Candidate work:
  - progress logging
  - step timing summaries
  - clearer saved-log locations

### TA-005: Harden the replay corpus with multiple real symbols

- Status: `Ready`
- Goal: build a small corpus from multiple real runs rather than synthetic examples only
- Done when:
  - at least 3 real replay cases exist

### TA-006: Polish paper-trading operator workflow

- Status: `Ready`
- Goal: make paper-trading usage simple and documented
- Candidate work:
  - cleaner CLI output
  - optional summary file export
  - env validation checks before run

### TA-007: Evaluate whether AWS docs should be archived or deprioritized

- Status: `Ready`
- Goal: reduce confusion now that Thunder + Ollama is the recommended path
- Candidate work:
  - mark AWS/NIM docs as historical
  - move them under an archive section

## Waiting On Human

### TH-001: External runtime troubleshooting

- Status: `Waiting on Human`
- Goal: resolve issues that require actions inside Thunder Compute or operator-managed terminals

### TH-002: Paid infrastructure changes

- Status: `Waiting on Human`
- Goal: any action that creates or materially changes recurring spend
