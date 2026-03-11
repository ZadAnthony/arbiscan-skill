# ArbiScan — Cross-Exchange Arbitrage Scanner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Scan arbitrage opportunities across Binance, OKX, Bybit, and Bitget. Read-only — no trading, no API keys needed.**

ArbiScan is an [OpenClaw Skill](https://clawhub.ai) that scans for arbitrage opportunities across major crypto exchanges. It identifies price and rate discrepancies, calculates estimated yields, and presents them in a clean format. You decide whether to act — ArbiScan only watches.

## Scan Types

| Type | What it does | Data Source |
|------|-------------|-------------|
| **Funding Rate Arb** | Compares perpetual funding rates across exchanges | Public funding rate endpoints |
| **Basis Arb** | Spots premium/discount between spot and futures | Spot + futures price tickers |
| **Spot Spread** | Finds bid/ask gaps across exchanges | Order book top-of-book |
| **Stablecoin Depeg** | Monitors USDC/DAI/FDUSD/TUSD deviation from $1 | Stablecoin price tickers |

## Quick Start

### As an OpenClaw Skill

Install from ClawHub and let your AI agent scan for opportunities:

```
"Scan for funding rate arbitrage opportunities with APY > 10%"
"Check if any stablecoins are depegging"
"Show me cross-exchange spread opportunities for BTC and ETH"
```

### Standalone (Python)

```bash
cd scripts/
pip install -r requirements.txt

# Run all scans
python scanner.py --all

# Funding rate arbitrage only, min 10% APY
python scanner.py --type funding --min-apy 10

# Output as markdown
python scanner.py --type funding --format markdown

# Output as JSON (for piping)
python scanner.py --type spread --format json
```

## Sample Output

```
  Funding Rate Arbitrage
================================================================================
Symbol     Long (低费率)         Short (高费率)        Rate Diff   Est. APY%   Risk    Window
---------  -------------------  --------------------  ----------  ----------  ------  --------
WIFUSDT    Bybit 0.0012%        Binance 0.0450%       0.0438%     48.0%       HIGH    ~8h
ETHUSDT    OKX 0.0030%           Bitget 0.0310%        0.0280%     30.7%       MEDIUM  ~8h
BTCUSDT    Bybit 0.0100%         OKX 0.0180%           0.0080%     8.8%        LOW     ~8h
```

## Composable with Exchange Skills

ArbiScan is designed to work alongside exchange trading skills:

1. **ArbiScan** scans and identifies opportunities (this skill)
2. **Binance/Bybit/Bitget Skills** can execute trades if you decide to act
3. **TradeOS** can manage the full arbitrage workflow

```
"Use ArbiScan to find opportunities, then use Binance skill to execute the best one"
```

## How It Works

- Fetches data from **public API endpoints only** — no API keys, no authentication
- Built-in rate limiting (200ms between requests) to respect exchange limits
- Covers **Top 30 trading pairs** by market cap
- Risk scoring based on APY magnitude and coin category

## Covered Exchanges

| Exchange | Spot | Futures | Funding Rate |
|----------|------|---------|--------------|
| Binance  | ✅   | ✅      | ✅           |
| Bybit    | ✅   | ✅      | ✅           |
| OKX      | ✅   | ✅      | ✅           |
| Bitget   | ✅   | ✅      | ✅           |

## Disclaimer

ArbiScan is for **informational purposes only**. It does not constitute financial advice. Arbitrage opportunities shown are theoretical — actual execution requires considering:

- Gas/withdrawal fees
- Transfer times between exchanges
- Slippage and liquidity
- Exchange counterparty risk
- Regulatory compliance

Always do your own research before trading.

## License

MIT
