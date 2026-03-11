"""交易所端点配置 + symbol 映射"""

# Top 30 主流交易对
TOP_SYMBOLS = [
    "BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "ADA", "AVAX", "DOT", "LINK",
    "MATIC", "UNI", "LTC", "BCH", "NEAR", "APT", "OP", "ARB", "FIL", "ATOM",
    "ETC", "IMX", "INJ", "SEI", "SUI", "TIA", "JUP", "WLD", "PEPE", "WIF",
]

# 交易所配置
EXCHANGES = {
    "binance": {
        "name": "Binance",
        "base_url": "https://api.binance.com",
        "futures_url": "https://fapi.binance.com",
        "endpoints": {
            "funding_rate": "/fapi/v1/premiumIndex",
            "spot_ticker": "/api/v3/ticker/bookTicker",
            "futures_ticker": "/fapi/v1/ticker/price",
            "spot_price": "/api/v3/ticker/price",
        },
        "symbol_format": lambda base: f"{base}USDT",
        "swap_format": lambda base: f"{base}USDT",
        "funding_interval_hours": 8,
    },
    "bybit": {
        "name": "Bybit",
        "base_url": "https://api.bybit.com",
        "futures_url": "https://api.bybit.com",
        "endpoints": {
            "funding_rate": "/v5/market/tickers",
            "spot_ticker": "/v5/market/tickers",
            "futures_ticker": "/v5/market/tickers",
        },
        "symbol_format": lambda base: f"{base}USDT",
        "swap_format": lambda base: f"{base}USDT",
        "funding_interval_hours": 8,
    },
    "okx": {
        "name": "OKX",
        "base_url": "https://www.okx.com",
        "futures_url": "https://www.okx.com",
        "endpoints": {
            "funding_rate": "/api/v5/public/funding-rate",
            "spot_ticker": "/api/v5/market/ticker",
            "futures_ticker": "/api/v5/market/ticker",
        },
        "symbol_format": lambda base: f"{base}-USDT",
        "swap_format": lambda base: f"{base}-USDT-SWAP",
        "funding_interval_hours": 8,
    },
    "bitget": {
        "name": "Bitget",
        "base_url": "https://api.bitget.com",
        "futures_url": "https://api.bitget.com",
        "endpoints": {
            "funding_rate": "/api/v2/mix/market/current-fund-rate",
            "spot_ticker": "/api/v2/spot/market/tickers",
            "futures_ticker": "/api/v2/mix/market/tickers",
        },
        "symbol_format": lambda base: f"{base}USDT",
        "swap_format": lambda base: f"{base}USDT",
        "funding_interval_hours": 8,
    },
}

# 请求配置
REQUEST_TIMEOUT = 10  # 秒
RATE_LIMIT_DELAY = 0.2  # 秒，请求间隔
