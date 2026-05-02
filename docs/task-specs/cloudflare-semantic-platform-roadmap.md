# Cloudflare Semantic Platform Roadmap

## Goal

Build AI Fund's visualization and data platform around:

- Cloudflare Pages for the frontend
- SQLPrism in the browser for SQL-to-Vega-Lite translation
- Python FastAPI in Cloudflare Containers for tabular data serving
- R2 + Parquet for analytical data
- D1 for operational relational metadata
- Workers AI for Cloudflare-native model inference experiments

## Task Breakdown

### CF-001: Define Semantic Dataset Contracts

Deliverables:

- `market_bars` schema
- `market_snapshots` schema
- `agent_runs` schema
- `agent_decisions` schema
- sample rows for local development
- docs describing public vs private datasets

Acceptance:

- schemas are documented
- sample data can support at least two chart queries
- no account/order/position data is included in public fixtures

### CF-002: Add SQLPrism Frontend Visualization Prototype

Deliverables:

- add SQLPrism dependency to `apps/web`
- add curated SQL examples
- generate Vega-Lite specs on the frontend
- render at least one chart with fixture rows

Acceptance:

- `npm run build` passes
- research page renders a chart from SQL + rows
- backend is not required for the prototype

### CF-003: Add Python Query API Skeleton

Deliverables:

- add `services/api` FastAPI app
- add `/health`
- add `/query`
- add SQL validation module
- add DuckDB-backed local Parquet fixture querying

Acceptance:

- only `SELECT` queries are accepted
- allowlisted tables/columns are enforced
- response returns `{ columns, rows, meta }`
- Python tests cover accepted and rejected SQL

### CF-004: Add R2/Parquet Warehouse Layout

Deliverables:

- define R2 object key layout
- define Parquet partitioning strategy
- add local writer utilities
- document raw vs normalized artifact locations

Acceptance:

- local artifacts mirror the intended R2 layout
- DuckDB can query generated Parquet
- D1 is not used for high-volume market bars

### CF-005: Add D1 Operational Metadata Schema

Deliverables:

- dataset manifests
- ingestion jobs
- saved queries
- chart definitions
- agent run index
- audit log tables

Acceptance:

- schema is documented
- migration files exist
- D1 stores metadata only, not the market-data warehouse

### CF-006: Add Moomoo Kline/Snapshot Ingestion

Deliverables:

- ingestion script for kline data
- ingestion script for snapshot data
- normalized `market_bars` writer
- normalized `market_snapshots` writer

Acceptance:

- scripts can run against OpenD in simulated/safe mode
- output matches semantic schema
- raw payload and normalized output are separated
- no live trading action is involved

### CF-007: Containerize Python API

Deliverables:

- Dockerfile for `services/api`
- Cloudflare Container notes/config
- local container run command
- environment variable contract

Acceptance:

- API runs locally in Docker
- `/query` works against local fixture data
- container disk is documented as cache/scratch only

### CF-008: Add Workers AI Provider Experiment

Deliverables:

- provider config for Workers AI
- one smoke test prompt
- TradingAgents compatibility notes
- cost and model-quality observations

Acceptance:

- no hosted inference is used without explicit approval
- smoke test can be run manually
- docs compare Workers AI with Thunder/Ollama

## Human-Gated Tasks

These require explicit user input:

- creating paid Cloudflare resources beyond already-approved Pages usage
- connecting R2/D1 production resources
- deploying Cloudflare Containers
- running Workers AI workloads beyond free/smoke tests
- logging into Moomoo/OpenD
- enabling live trading
