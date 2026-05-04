type RefractResult = {
  vega?: {
    $schema: string;
    mark: "line";
    encoding: Record<string, unknown>;
  };
};

const TIMESTAMP_CLOSE_QUERY =
  /select\s+timestamp\s*,\s*close\s+from\s+market_bars/i;

export function refractSqlToVega(sql: string): RefractResult {
  if (!TIMESTAMP_CLOSE_QUERY.test(sql)) {
    return {};
  }

  return {
    vega: {
      $schema: "https://vega.github.io/schema/vega-lite/v6.json",
      mark: "line",
      encoding: {
        x: {
          field: "timestamp",
          type: "temporal",
          title: "Date",
          axis: {
            format: "%b %d",
          },
        },
        y: {
          field: "close",
          type: "quantitative",
          title: "Close",
          axis: {
            format: "$,.2f",
          },
        },
        tooltip: [
          {
            field: "timestamp",
            type: "temporal",
            title: "Date",
          },
          {
            field: "close",
            type: "quantitative",
            title: "Close",
            format: "$,.2f",
          },
        ],
      },
    },
  };
}
