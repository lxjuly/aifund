# SQLPrism Semantic Visualization

## Recommendation

Use SQLPrism as the semantic query and visualization layer for AI Fund charts.

The target path is:

```text
Moomoo OpenD
  -> ingestion scripts
  -> R2 Parquet warehouse
  -> Cloudflare Container Python API
  -> tabular query responses

Cloudflare Pages frontend
  -> SQLPrism query/refraction
  -> Vega-Lite specs
  -> render returned rows
```

## Why This Fits

SQLPrism already converts SQL into:

- a reusable SQL AST
- OSI payloads for governed semantic requests
- DuckDB SQL for local cache/query execution
- Vega-Lite specs for declarative charts

That aligns well with the AI Fund need to avoid one-off chart code and expose market, run, and paper-trading data through a stable semantic interface.

## Direct Moomoo Loading vs Ingestion

Do not have the public site load directly from Moomoo OpenD.

Reasons:

- OpenD is a local or server-side gateway, not a browser-safe public API.
- OpenD may carry account/session state.
- Moomoo market data permissions and redistribution rules may constrain what can be shown publicly.
- Cloudflare Pages is best treated as a public renderer, not the place where broker connectivity lives.

Instead, ingest Moomoo data into AI Fund-owned datasets, then expose sanitized semantic data through a Python query API.

## Frontend / Backend Separation

The frontend owns visualization intent:

- accept or select SQL
- use SQLPrism to parse SQL and generate Vega-Lite
- send SQL to the backend query API
- attach returned rows to the Vega-Lite spec
- render the chart

The backend owns data access and safety:

- validate SQL
- enforce read-only queries
- resolve semantic table names
- query DuckDB over R2-backed Parquet or local cache
- return tabular rows only
- never return broker credentials or private OpenD state

## Initial Semantic Datasets

Start with public-safe, non-account datasets:

### `market_bars`

Candlestick/kline data.

Fields:

- `symbol`
- `market`
- `timestamp`
- `timeframe`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `source`
- `ingested_at`

### `market_snapshots`

Point-in-time quote snapshots.

Fields:

- `symbol`
- `market`
- `timestamp`
- `last_price`
- `open_price`
- `high_price`
- `low_price`
- `prev_close`
- `volume`
- `turnover`
- `source`
- `ingested_at`

### `agent_runs`

TradingAgents run metadata.

Fields:

- `run_id`
- `symbol`
- `trade_date`
- `rating`
- `action`
- `model_deep`
- `model_quick`
- `backend`
- `started_at`
- `completed_at`
- `status`

### `agent_decisions`

Structured final decisions and policy outcomes.

Fields:

- `run_id`
- `symbol`
- `trade_date`
- `rating`
- `action`
- `approved`
- `policy_reason`
- `confidence`
- `thesis_excerpt`

## Example SQLPrism Queries

Price trend:

```sql
SELECT timestamp, close
FROM market_bars
WHERE symbol = 'US.NVDA' AND timeframe = 'K_DAY'
ORDER BY timestamp
```

Volume by day:

```sql
SELECT timestamp, SUM(volume) AS volume
FROM market_bars
WHERE symbol = 'US.NVDA' AND timeframe = 'K_DAY'
GROUP BY timestamp
ORDER BY timestamp
```

Decision distribution:

```sql
SELECT rating, COUNT(run_id) AS runs
FROM agent_runs
GROUP BY rating
ORDER BY runs DESC
```

## Implementation Shape

Phase 1 should be frontend-first and fixture-based:

1. Add sample normalized JSON rows under `apps/web/src/data`.
2. Add SQLPrism to `apps/web`.
3. Turn curated SQL examples into Vega-Lite specs on the frontend.
4. Render charts on the Astro research page using fixture rows.
5. Keep all data fixture-based until the visual grammar feels right.

Local development can consume SQLPrism from the sibling workspace repo before npm publication:

```json
"sqlprism": "file:../../../sqlprism"
```

Cloudflare production builds should switch to `github:lxjuly/sqlprism` or the npm package once SQLPrism is published or otherwise buildable from GitHub.

Phase 2 adds the Python query backend:

1. Add a FastAPI app under `services/api`.
2. Add a read-only `/query` endpoint.
3. Validate SQL against allowlisted semantic tables and columns.
4. Use DuckDB to query local Parquet fixtures first.
5. Return `{ columns, rows, meta }` only.

Phase 3 adds Cloudflare storage:

1. Use R2 as durable storage for raw artifacts and normalized Parquet.
2. Use D1 for operational metadata, manifests, saved queries, chart definitions, and run indexes.
3. Keep container disk as cache/scratch only.
4. Keep DuckDB as the analytical query engine, not the durable database.

Phase 4 adds Moomoo ingestion:

1. Use the installed `moomooapi` skill scripts as references for `get_kline` and `get_snapshot`.
2. Add project-owned ingestion scripts under `services/api` or `tradingagents/dataflows/`.
3. Write normalized Parquet artifacts locally first.
4. Sync raw and normalized artifacts to R2.

Phase 5 adds Cloudflare-native runtime:

1. Run the Python API in Cloudflare Containers.
2. Use Workers AI for hosted inference where model quality is sufficient.
3. Keep Cloudflare Pages as the frontend host.
4. Use D1/R2 bindings or Cloudflare APIs for metadata and object storage.

## Safety Boundaries

- Do not expose OpenD directly to the public internet.
- Do not expose account, order, or position data on the public site.
- Do not publish live trade recommendations.
- Treat market data redistribution as a permission-sensitive area.
- Keep public visualizations focused on research, paper trading, and delayed/sanitized data.
- Treat R2 as durable warehouse storage and container disk as ephemeral cache.

## Sources

- SQLPrism README: https://github.com/lxjuly/sqlprism
- SQLPrism `refract` API: https://github.com/lxjuly/sqlprism/blob/main/src/index.ts
- SQLPrism OSI generator: https://github.com/lxjuly/sqlprism/blob/main/src/generators/osi.ts
- SQLPrism OSI runtime demo: https://github.com/lxjuly/sqlprism/blob/main/src/runtime/execute-osi.ts
- Moomoo OpenAPI AI integration: https://openapi.moomoo.com/moomoo-api-doc/en/intro/ai.html
- Moomoo OpenAPI introduction: https://openapi.moomoo.com/moomoo-api-doc/en/intro/intro.html
