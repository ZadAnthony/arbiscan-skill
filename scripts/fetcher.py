"""统一数据获取层 — 公开 API，无需 key"""

import time
import requests
from typing import Optional
from config import EXCHANGES, REQUEST_TIMEOUT, RATE_LIMIT_DELAY

_last_request_time = 0


def _rate_limit():
    """限频：请求间隔至少 RATE_LIMIT_DELAY 秒"""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - elapsed)
    _last_request_time = time.time()


def _get(url: str, params: Optional[dict] = None) -> Optional[dict]:
    """发起 GET 请求，返回 JSON 或 None"""
    _rate_limit()
    try:
        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  [WARN] 请求失败 {url}: {e}")
        return None


# ====== 资金费率 ======

def fetch_funding_rate_binance(symbol: str) -> Optional[float]:
    cfg = EXCHANGES["binance"]
    url = cfg["futures_url"] + cfg["endpoints"]["funding_rate"]
    data = _get(url, {"symbol": cfg["swap_format"](symbol)})
    if data:
        return float(data.get("lastFundingRate", 0))
    return None


def fetch_funding_rate_bybit(symbol: str) -> Optional[float]:
    cfg = EXCHANGES["bybit"]
    url = cfg["base_url"] + cfg["endpoints"]["funding_rate"]
    data = _get(url, {"category": "linear", "symbol": cfg["swap_format"](symbol)})
    if data and data.get("result", {}).get("list"):
        return float(data["result"]["list"][0].get("fundingRate", 0))
    return None


def fetch_funding_rate_okx(symbol: str) -> Optional[float]:
    cfg = EXCHANGES["okx"]
    url = cfg["base_url"] + cfg["endpoints"]["funding_rate"]
    data = _get(url, {"instId": cfg["swap_format"](symbol)})
    if data and data.get("data"):
        return float(data["data"][0].get("fundingRate", 0))
    return None


def fetch_funding_rate_bitget(symbol: str) -> Optional[float]:
    cfg = EXCHANGES["bitget"]
    url = cfg["base_url"] + cfg["endpoints"]["funding_rate"]
    data = _get(url, {"symbol": cfg["swap_format"](symbol), "productType": "USDT-FUTURES"})
    if data and data.get("data"):
        return float(data["data"][0].get("fundingRate", 0))
    return None


def fetch_all_funding_rates(symbol: str) -> dict:
    """获取某个 symbol 在所有交易所的资金费率"""
    fetchers = {
        "binance": fetch_funding_rate_binance,
        "bybit": fetch_funding_rate_bybit,
        "okx": fetch_funding_rate_okx,
        "bitget": fetch_funding_rate_bitget,
    }
    results = {}
    for exchange, fetcher in fetchers.items():
        rate = fetcher(symbol)
        if rate is not None:
            results[exchange] = rate
    return results


# ====== 现货行情 ======

def fetch_spot_ticker_binance(symbol: str) -> Optional[dict]:
    cfg = EXCHANGES["binance"]
    url = cfg["base_url"] + cfg["endpoints"]["spot_ticker"]
    data = _get(url, {"symbol": cfg["symbol_format"](symbol)})
    if data:
        return {"bid": float(data["bidPrice"]), "ask": float(data["askPrice"])}
    return None


def fetch_spot_ticker_bybit(symbol: str) -> Optional[dict]:
    cfg = EXCHANGES["bybit"]
    url = cfg["base_url"] + cfg["endpoints"]["spot_ticker"]
    data = _get(url, {"category": "spot", "symbol": cfg["symbol_format"](symbol)})
    if data and data.get("result", {}).get("list"):
        item = data["result"]["list"][0]
        return {"bid": float(item["bid1Price"]), "ask": float(item["ask1Price"])}
    return None


def fetch_spot_ticker_okx(symbol: str) -> Optional[dict]:
    cfg = EXCHANGES["okx"]
    url = cfg["base_url"] + cfg["endpoints"]["spot_ticker"]
    data = _get(url, {"instId": cfg["symbol_format"](symbol)})
    if data and data.get("data"):
        item = data["data"][0]
        return {"bid": float(item["bidPx"]), "ask": float(item["askPx"])}
    return None


def fetch_spot_ticker_bitget(symbol: str) -> Optional[dict]:
    cfg = EXCHANGES["bitget"]
    url = cfg["base_url"] + cfg["endpoints"]["spot_ticker"]
    data = _get(url, {"symbol": cfg["symbol_format"](symbol)})
    if data and data.get("data"):
        item = data["data"][0] if isinstance(data["data"], list) else data["data"]
        return {"bid": float(item.get("bidPr", 0)), "ask": float(item.get("askPr", 0))}
    return None


def fetch_all_spot_tickers(symbol: str) -> dict:
    """获取某个 symbol 在所有交易所的现货 bid/ask"""
    fetchers = {
        "binance": fetch_spot_ticker_binance,
        "bybit": fetch_spot_ticker_bybit,
        "okx": fetch_spot_ticker_okx,
        "bitget": fetch_spot_ticker_bitget,
    }
    results = {}
    for exchange, fetcher in fetchers.items():
        ticker = fetcher(symbol)
        if ticker and ticker["bid"] > 0 and ticker["ask"] > 0:
            results[exchange] = ticker
    return results


# ====== 合约行情 ======

def fetch_futures_price_binance(symbol: str) -> Optional[float]:
    cfg = EXCHANGES["binance"]
    url = cfg["futures_url"] + cfg["endpoints"]["futures_ticker"]
    data = _get(url, {"symbol": cfg["swap_format"](symbol)})
    if data:
        return float(data["price"])
    return None


def fetch_futures_price_bybit(symbol: str) -> Optional[float]:
    cfg = EXCHANGES["bybit"]
    url = cfg["base_url"] + cfg["endpoints"]["futures_ticker"]
    data = _get(url, {"category": "linear", "symbol": cfg["swap_format"](symbol)})
    if data and data.get("result", {}).get("list"):
        return float(data["result"]["list"][0].get("lastPrice", 0))
    return None


def fetch_futures_price_okx(symbol: str) -> Optional[float]:
    cfg = EXCHANGES["okx"]
    url = cfg["base_url"] + cfg["endpoints"]["futures_ticker"]
    data = _get(url, {"instId": cfg["swap_format"](symbol)})
    if data and data.get("data"):
        return float(data["data"][0].get("last", 0))
    return None


def fetch_futures_price_bitget(symbol: str) -> Optional[float]:
    cfg = EXCHANGES["bitget"]
    url = cfg["base_url"] + cfg["endpoints"]["futures_ticker"]
    data = _get(url, {"productType": "USDT-FUTURES", "symbol": cfg["swap_format"](symbol)})
    if data and data.get("data"):
        item = data["data"][0] if isinstance(data["data"], list) else data["data"]
        return float(item.get("lastPr", 0))
    return None


def fetch_all_futures_prices(symbol: str) -> dict:
    """获取某个 symbol 在所有交易所的合约价格"""
    fetchers = {
        "binance": fetch_futures_price_binance,
        "bybit": fetch_futures_price_bybit,
        "okx": fetch_futures_price_okx,
        "bitget": fetch_futures_price_bitget,
    }
    results = {}
    for exchange, fetcher in fetchers.items():
        price = fetcher(symbol)
        if price and price > 0:
            results[exchange] = price
    return results


# ====== 现货价格（简单版，用于期现基差） ======

def fetch_spot_price_binance(symbol: str) -> Optional[float]:
    cfg = EXCHANGES["binance"]
    url = cfg["base_url"] + cfg["endpoints"]["spot_price"]
    data = _get(url, {"symbol": cfg["symbol_format"](symbol)})
    if data:
        return float(data["price"])
    return None


def fetch_spot_price_bybit(symbol: str) -> Optional[float]:
    ticker = fetch_spot_ticker_bybit(symbol)
    if ticker:
        return (ticker["bid"] + ticker["ask"]) / 2
    return None


def fetch_spot_price_okx(symbol: str) -> Optional[float]:
    ticker = fetch_spot_ticker_okx(symbol)
    if ticker:
        return (ticker["bid"] + ticker["ask"]) / 2
    return None


def fetch_spot_price_bitget(symbol: str) -> Optional[float]:
    ticker = fetch_spot_ticker_bitget(symbol)
    if ticker:
        return (ticker["bid"] + ticker["ask"]) / 2
    return None


def fetch_all_spot_prices(symbol: str) -> dict:
    """获取某个 symbol 在所有交易所的现货中间价"""
    fetchers = {
        "binance": fetch_spot_price_binance,
        "bybit": fetch_spot_price_bybit,
        "okx": fetch_spot_price_okx,
        "bitget": fetch_spot_price_bitget,
    }
    results = {}
    for exchange, fetcher in fetchers.items():
        price = fetcher(symbol)
        if price and price > 0:
            results[exchange] = price
    return results
