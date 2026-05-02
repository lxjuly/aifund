# Harness Rollout

## Objective

Add the first mechanical harnesses for the execution layer so future agent work has fast local feedback.

## Scope

- fixture-driven signal parser harness
- fixture-driven risk policy harness
- broker-free runner dry-run harness
- replay corpus for archived final decisions
- capture script for turning real outputs into replay fixtures
- a small harness runner script
- system-spec documentation for harness philosophy and scope

## Done Criteria

- harness tests run with `python -m unittest`
- fixtures are stored in-repo
- no live APIs are required
- failures are specific enough to guide the next agent iteration

## Follow-Up Work

- fold harness execution into CI
- add recorded fixture sets from real TradingAgents outputs
- add a paper-trading replay harness that loads archived decisions from disk
