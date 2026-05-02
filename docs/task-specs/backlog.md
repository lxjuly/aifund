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

### TA-008: Pivot broker integration from Alpaca to Moomoo OpenAPI

- Status: `Ready`
- Goal: replace Alpaca as the default broker target for new execution work
- Done when:
  - Moomoo adapter interface is designed
  - OpenD runtime assumptions are documented
  - existing Alpaca adapter is retained only as optional/historical
  - simulated trading remains the default execution path

### TA-009: Scaffold Cloudflare Pages public website

- Status: `Done`
- Goal: create the first public AI Fund website under `apps/web`
- Done when:
  - site can build locally
  - Cloudflare Pages deployment notes exist
  - first pages avoid regulated fund-offering language
  - disclosure page exists

Note: the initial Astro scaffold and Cloudflare Pages docs are in place. Local build verification still needs dependency installation in an environment with working npm registry access.

### TA-010: Verify and polish the Cloudflare Pages website

- Status: `Ready`
- Depends on: `TA-009`
- Goal: install web dependencies, verify the Astro build, and refine the first pass UI
- Done when:
  - `npm install` completes under `apps/web`
  - `npm run build` passes
  - homepage, methodology, research, and disclosures pages are visually reviewed
  - no upstream TradingAgents visual assets are used

### TA-011: Add SQLPrism semantic visualization layer

- Status: `Ready`
- Depends on: `TA-009`
- Goal: use SQLPrism to turn curated SQL over AI Fund datasets into Vega-Lite charts
- Done when:
  - initial market/run dataset schemas are represented as sample JSON
  - at least one SQLPrism query generates a Vega-Lite spec
  - the research page renders a chart from SQLPrism output
  - Moomoo/OpenD remains behind ingestion, not directly exposed to the public site

### TA-012: Define Cloudflare-native semantic platform

- Status: `Ready`
- Depends on: `TA-011`
- Goal: define the Cloudflare-native backend/storage plan for SQLPrism visualization and Moomoo ingestion
- Done when:
  - Cloudflare Pages, Containers, Workers AI, R2, and D1 responsibilities are documented
  - R2/Parquet vs D1 persistence split is documented
  - Python API query contract is documented
  - detailed task roadmap exists

### TA-013: Define semantic dataset contracts

- Status: `Ready`
- Depends on: `TA-012`
- Goal: define schemas and sample rows for the initial semantic datasets
- Done when:
  - `market_bars`, `market_snapshots`, `agent_runs`, and `agent_decisions` schemas exist
  - sample rows support chart prototyping
  - public/private dataset boundaries are explicit

### TA-014: Add SQLPrism frontend chart prototype

- Status: `Done`
- Depends on: `TA-013`
- Goal: use SQLPrism on the frontend to turn SQL into Vega-Lite and render fixture-backed charts
- Done when:
  - SQLPrism is available to `apps/web`
  - research page renders at least one Vega-Lite chart
  - frontend sends no direct Moomoo/OpenD requests

### TA-015: Add Python semantic query API skeleton

- Status: `Ready`
- Depends on: `TA-013`
- Goal: add a FastAPI query service that validates SQL and returns tabular rows only
- Done when:
  - `/health` and `/query` exist
  - DuckDB queries local fixtures
  - read-only allowlisted SQL is enforced
  - Python tests cover accepted and rejected SQL

### TA-016: Build Moomoo market-data ingestion

- Status: `Ready`
- Depends on: `TA-015`
- Goal: ingest Moomoo snapshot/kline data into normalized AI Fund datasets
- Done when:
  - OpenD assumptions are documented
  - ingestion supports `market_bars` and `market_snapshots`
  - generated artifacts match the SQLPrism semantic dataset schema
  - no account/order/position data is published publicly

## Waiting On Human

### TH-001: External runtime troubleshooting

- Status: `Waiting on Human`
- Goal: resolve issues that require actions inside Thunder Compute or operator-managed terminals

### TH-002: Paid infrastructure changes

- Status: `Waiting on Human`
- Goal: any action that creates or materially changes recurring spend

### TH-003: Moomoo account and OpenD setup

- Status: `Waiting on Human`
- Goal: actions requiring Moomoo account login, API agreements, OpenD login, or trade unlock credentials
