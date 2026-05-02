# Cloudflare Native Platform

## Recommendation

Use Cloudflare as the default production platform, with Python reserved for backend and agent orchestration.

## Target Architecture

```text
Cloudflare Pages
  -> Astro frontend
  -> SQLPrism in browser
  -> Vega-Lite rendering

Cloudflare Container
  -> Python FastAPI backend
  -> SQL validation
  -> DuckDB query engine
  -> TradingAgents orchestration later

Cloudflare R2
  -> raw Moomoo payloads
  -> normalized Parquet datasets
  -> TradingAgents logs
  -> report artifacts

Cloudflare D1
  -> dataset manifests
  -> ingestion job state
  -> saved queries
  -> chart definitions
  -> agent run index
  -> audit metadata

Workers AI
  -> hosted model inference for agent experiments
  -> optional replacement for Thunder/Ollama when quality and cost are acceptable
```

## Persistence Split

Use R2 + Parquet for analytical market data. Use D1 for operational relational data.

R2/Parquet is better for:

- historical bars
- snapshots
- feature datasets
- raw ingestion payloads
- large logs
- replay and report artifacts

D1 is better for:

- users and auth metadata
- saved SQL queries
- chart definitions
- dataset manifests
- ingestion jobs
- agent run indexes
- audit logs

DuckDB should be treated as the query engine over Parquet and local cache, not the only durable store.

## Cost Rationale

R2 is object storage with low per-GB storage cost and no egress fees, which fits analytical history and Parquet files. D1 is row-metered SQL storage and is better suited to indexed operational metadata than high-volume market bars or tick history.

## Initial Backend Contract

The Python API should initially expose:

```http
POST /query
Content-Type: application/json

{
  "sql": "SELECT timestamp, close FROM market_bars WHERE symbol = 'US.NVDA' LIMIT 200"
}
```

Response:

```json
{
  "columns": [
    { "name": "timestamp", "type": "datetime" },
    { "name": "close", "type": "number" }
  ],
  "rows": [],
  "meta": {
    "row_count": 0,
    "execution_ms": 0
  }
}
```

The backend should not generate Vega-Lite. SQLPrism on the frontend owns visualization translation.

## Security Rules

- Accept read-only `SELECT` queries only.
- Enforce allowlisted tables and columns.
- Enforce default and maximum row limits.
- Block account, order, position, credential, and raw broker tables from public query paths.
- Log queries and errors.
- Require authentication before exposing private or operational datasets.

## Sources

- Cloudflare R2 pricing: https://workers.cloudflare.com/product/r2/
- Cloudflare D1 pricing: https://developers.cloudflare.com/d1/platform/pricing/
- Cloudflare Containers pricing: https://workers.cloudflare.com/pricing
- Cloudflare Workers AI pricing: https://developers.cloudflare.com/workers-ai/platform/pricing/
