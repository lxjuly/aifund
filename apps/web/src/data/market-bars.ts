export interface MarketBar {
  symbol: string;
  market: string;
  timestamp: string;
  timeframe: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  source: string;
  ingested_at: string;
}

export const marketBars: MarketBar[] = [
  {
    symbol: "US.NVDA",
    market: "US",
    timestamp: "2026-04-20",
    timeframe: "K_DAY",
    open: 232.2,
    high: 238.6,
    low: 229.8,
    close: 235.1,
    volume: 31400000,
    source: "fixture",
    ingested_at: "2026-05-02T00:00:00Z",
  },
  {
    symbol: "US.NVDA",
    market: "US",
    timestamp: "2026-04-21",
    timeframe: "K_DAY",
    open: 235.3,
    high: 241.1,
    low: 233.9,
    close: 239.6,
    volume: 33700000,
    source: "fixture",
    ingested_at: "2026-05-02T00:00:00Z",
  },
  {
    symbol: "US.NVDA",
    market: "US",
    timestamp: "2026-04-22",
    timeframe: "K_DAY",
    open: 238.8,
    high: 240.4,
    low: 231.6,
    close: 233.7,
    volume: 36200000,
    source: "fixture",
    ingested_at: "2026-05-02T00:00:00Z",
  },
  {
    symbol: "US.NVDA",
    market: "US",
    timestamp: "2026-04-23",
    timeframe: "K_DAY",
    open: 234.4,
    high: 237.9,
    low: 230.4,
    close: 236.8,
    volume: 29800000,
    source: "fixture",
    ingested_at: "2026-05-02T00:00:00Z",
  },
  {
    symbol: "US.NVDA",
    market: "US",
    timestamp: "2026-04-24",
    timeframe: "K_DAY",
    open: 237.1,
    high: 240.2,
    low: 234.7,
    close: 238.9,
    volume: 32100000,
    source: "fixture",
    ingested_at: "2026-05-02T00:00:00Z",
  },
];
