"""A small, liquid, large-cap default universe for the screener.

Discovery needs a pool to rank. This curated list keeps a first run fast and
reliable across sectors. Swap it for a broader list (for example an index
membership file) once the funnel is proven.
"""

DEFAULT_UNIVERSE = [
    # Mega-cap tech
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "AVGO", "AMD", "ORCL", "ADBE",
    "CRM", "NFLX",
    # Financials
    "JPM", "BAC", "V", "MA",
    # Health care
    "UNH", "JNJ", "LLY", "ABBV",
    # Consumer
    "COST", "WMT", "HD", "PG", "KO", "PEP",
    # Energy / industrials
    "XOM", "CVX", "CAT", "GE",
]
