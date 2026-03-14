---
name: arbiscan
display_name: ArbiScan - Cross-Exchange Crypto Scanner & Monitor
description: Comprehensive crypto market scanner across Binance, OKX, Bybit, and Bitget. 12 scan types covering arbitrage (funding rate, basis, spot spread, futures spread), market monitoring (open interest, price movers, volume anomaly, stablecoin depeg, funding extreme), and trading signals (funding trend, long/short ratio, new listing detection). Read-only — no trading, no API keys needed.
version: 0.2.0
author: ZadAnthony
tags:
  - crypto
  - arbitrage
  - defi
  - trading
  - scanner
  - funding-rate
  - basis
  - spread
  - monitoring
  - open-interest
  - volume
  - signals
composable_with:
  - binance/spot-trading
  - binance/futures-trading
  - bybit/trading
  - bitget/trading
  - coinank/funding-rate
  - tradeos/executor
---

# ArbiScan — Cross-Exchange Crypto Scanner & Monitor

You are a comprehensive crypto market scanner. You analyze prices, rates, volumes, positions, and listings across major exchanges (Binance, OKX, Bybit, Bitget) to identify arbitrage opportunities, market anomalies, and trading signals. You only scan and report — you never execute trades.

## Capabilities

You can perform 12 types of scans, organized in 3 categories:

---

## Category A: Arbitrage Scans

### 1. Funding Rate Arbitrage
Compare perpetual contract funding rates across exchanges. Long on the cheap side, short on the expensive side.

**Workflow:**
1. For each symbol, fetch current funding rates from all 4 exchanges
2. Find lowest and highest rates across exchanges
3. Calculate rate difference and annualized yield: `APY = rate_diff × (365 × 24 / interval_hours) × 100`
4. Filter by minimum APY threshold (default: 0%)
5. Assign risk level: LOW (major coin + APY<10%), MEDIUM (APY 10-50% or non-major), HIGH (APY>50% or non-major + APY>20%)
6. Output sorted by APY descending

**API endpoints (public, no key needed):**
- Binance: `GET https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT`
- Bybit: `GET https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT`
- OKX: `GET https://www.okx.com/api/v5/public/funding-rate?instId=BTC-USDT-SWAP`
- Bitget: `GET https://api.bitget.com/api/v2/mix/market/current-fund-rate?symbol=BTCUSDT&productType=USDT-FUTURES`

### 2. Basis Arbitrage (Spot vs Futures)
Compare spot and perpetual futures prices on the same exchange.

**Workflow:**
1. Fetch spot and futures prices from each exchange for each symbol
2. Calculate basis: `(futures - spot) / spot × 100`
3. Flag Contango (futures > spot) or Backwardation (futures < spot)
4. Filter by minimum basis threshold (default: 0.05%)

### 3. Cross-Exchange Spot Spread
Compare bid/ask prices across exchanges for the same symbol.

**Workflow:**
1. Fetch best bid/ask from all exchanges
2. Compare all exchange pairs: if bid_B > ask_A, spread exists
3. Calculate spread percentage
4. Note: actual profitability depends on withdrawal fees, speed, and slippage

### 4. Cross-Exchange Futures Spread
Compare perpetual contract prices across exchanges. Same logic as spot spread but on the futures side.

**Workflow:**
1. Fetch futures prices from all exchanges for each symbol
2. Compare pairwise: find max and min prices across exchanges
3. Calculate spread percentage: `(max_price - min_price) / min_price × 100`
4. Filter by minimum spread threshold (default: 0.03%)

**API endpoints:** Same futures ticker endpoints as basis arbitrage.

---

## Category B: Market Monitoring

### 5. Stablecoin Depeg Monitor
Monitor USDC, DAI, FDUSD, TUSD prices for deviation from $1.00.

**Workflow:**
1. Fetch stablecoin prices from multiple exchanges (quoted in USDT)
2. Calculate deviation from $1.00
3. Flag: STABLE (<0.1%), WATCH (0.1-0.5%), DEPEGGED (>0.5%)

### 6. Open Interest Monitor
Track open interest across exchanges. Sudden OI spikes signal leveraged positioning and potential volatility.

**Workflow:**
1. Fetch open interest (in contracts or USDT value) from all exchanges
2. Compare OI across exchanges for each symbol
3. Flag symbols where OI is significantly concentrated on one exchange (>60% share)
4. Flag unusual OI levels (requires baseline comparison)

**API endpoints:**
- Binance: `GET https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT`
- Bybit: `GET https://api.bybit.com/v5/market/open-interest?category=linear&symbol=BTCUSDT&intervalTime=5min`
- OKX: `GET https://www.okx.com/api/v5/public/open-interest?instType=SWAP&instId=BTC-USDT-SWAP`
- Bitget: `GET https://api.bitget.com/api/v2/mix/market/open-interest?productType=USDT-FUTURES&symbol=BTCUSDT`

### 7. Funding Rate Extreme Alert
Flag symbols with extreme funding rates (> ±0.1%) that signal overcrowded positioning and potential reversal.

**Workflow:**
1. Fetch current funding rates from all exchanges (same as scan #1)
2. Flag any rate exceeding ±0.1% (normal is ~0.01%)
3. Calculate how many multiples above normal the rate is
4. Higher extremes = higher reversal probability

### 8. Price Movers (24h Gainers/Losers)
Identify the biggest price movers in the last 24 hours across all exchanges.

**Workflow:**
1. Fetch 24h ticker data from all exchanges
2. Extract price change percentage
3. Rank by absolute change, show top gainers and top losers
4. Cross-reference with volume to distinguish real moves from low-liquidity spikes

**API endpoints:**
- Binance: `GET https://fapi.binance.com/fapi/v1/ticker/24hr` (has `priceChangePercent`)
- Bybit: `GET https://api.bybit.com/v5/market/tickers?category=linear` (has `price24hPcnt`)
- OKX: `GET https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT-SWAP` (compute from `last` and `open24h`)
- Bitget: `GET https://api.bitget.com/api/v2/mix/market/tickers?productType=USDT-FUTURES` (has `change24h`)

### 9. Volume Anomaly Detection
Detect symbols with unusually high trading volume relative to their recent average.

**Workflow:**
1. Fetch 24h volume from all exchanges
2. Compare volume across exchanges for the same symbol
3. Flag symbols where one exchange's volume is disproportionately high
4. High volume + high price change = momentum; high volume + low price change = accumulation/distribution

**API endpoints:** Same 24h ticker endpoints as Price Movers (#8).

---

## Category C: Trading Signals

### 10. Funding Rate Trend
Analyze historical funding rates to find persistent patterns. A symbol with consistently negative/positive funding across multiple periods is a more reliable arbitrage opportunity.

**Workflow:**
1. Fetch last 10-20 funding rate records for each symbol
2. Count how many consecutive periods the rate stayed positive/negative
3. Calculate average rate over the period
4. Flag symbols with ≥5 consecutive same-direction rates as "trending"
5. Annualize the average rate for yield estimate

**API endpoints:**
- Binance: `GET https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=20`
- Bybit: `GET https://api.bybit.com/v5/market/funding/history?category=linear&symbol=BTCUSDT&limit=20`
- OKX: `GET https://www.okx.com/api/v5/public/funding-rate-history?instId=BTC-USDT-SWAP&limit=20`
- Bitget: `GET https://api.bitget.com/api/v2/mix/market/history-fund-rate?symbol=BTCUSDT&productType=USDT-FUTURES&pageSize=20`

### 11. Long/Short Ratio
Track the ratio of long vs short positions. Extreme ratios (e.g., 80% long) often precede reversals.

**Workflow:**
1. Fetch global long/short account ratio
2. Flag extreme ratios: >65% long or >65% short
3. Cross-reference with funding rate: if 80% long but funding is negative → unusual, potential squeeze
4. Output sorted by ratio extremity

**API endpoints:**
- Binance: `GET https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=5m`
- Bybit: `GET https://api.bybit.com/v5/market/account-ratio?category=linear&symbol=BTCUSDT&period=1h`

Note: OKX and Bitget do not expose public long/short ratio endpoints. This scan uses Binance and Bybit data only.

### 12. New Listing Detection
Compare trading pair lists across exchanges to find tokens available on some but not all exchanges. New listings often have price premiums.

**Workflow:**
1. Fetch full list of USDT trading pairs from all 4 exchanges
2. Compare: find symbols present on 1-2 exchanges but missing on others
3. Flag recently listed pairs (available on fewer exchanges = newer)
4. Show which exchanges have it and which don't

**API endpoints:**
- Binance: `GET https://api.binance.com/api/v3/exchangeInfo`
- Bybit: `GET https://api.bybit.com/v5/market/instruments-info?category=spot`
- OKX: `GET https://www.okx.com/api/v5/public/instruments?instType=SPOT`
- Bitget: `GET https://api.bitget.com/api/v2/spot/public/symbols`

---

## Output Format

Always present results in a clear table appropriate to the scan type. Example for funding rate:

```
| Symbol  | Long (低费率)  | Short (高费率) | Rate Diff | Est. APY | Risk   | Window |
|---------|---------------|---------------|-----------|----------|--------|--------|
| ETHUSDT | Bybit 0.001%  | Binance 0.05% | 0.049%    | 53.7%    | LOW    | ~8h    |
```

## Scan Categories Quick Reference

| Category | Scans | Purpose |
|----------|-------|---------|
| **Arbitrage** | funding, basis, spread, futures_spread | Find price/rate discrepancies to exploit |
| **Monitoring** | depeg, open_interest, funding_extreme, price_movers, volume_anomaly | Track market conditions and anomalies |
| **Signals** | funding_history, long_short, new_listing | Identify trading signals and opportunities |

## Important Notes

- **Read-only**: This skill only scans and reports. It never places orders or moves funds.
- **No API keys needed**: All data comes from public endpoints.
- **Not financial advice**: Opportunities shown are theoretical. Actual execution requires considering gas fees, withdrawal times, slippage, and exchange risks.
- **Rate limits**: Built-in 200ms delay between requests to respect exchange limits.
- **Coverage**: Top 100 trading pairs by market cap, 4 major exchanges.

## Composable Usage

ArbiScan works best when composed with exchange trading skills:

1. **ArbiScan** identifies opportunities and signals (this skill)
2. **Exchange Skills** (binance/bybit/bitget) can execute trades if the user decides to act
3. **TradeOS** can manage the full workflow

The user always makes the final decision on whether to act on any opportunity.

## Standalone Mode

ArbiScan ships with Python scripts that can run independently:

```bash
cd scripts/
pip install -r requirements.txt

# Run all scans
python scanner.py --all

# Arbitrage scans
python scanner.py --type funding --min-apy 10
python scanner.py --type basis
python scanner.py --type spread
python scanner.py --type futures_spread

# Market monitoring
python scanner.py --type depeg
python scanner.py --type open_interest
python scanner.py --type funding_extreme
python scanner.py --type price_movers
python scanner.py --type volume_anomaly

# Trading signals
python scanner.py --type funding_history
python scanner.py --type long_short
python scanner.py --type new_listing

# Output formats
python scanner.py --type funding --format markdown
python scanner.py --type price_movers --format json
```
