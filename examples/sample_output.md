# ArbiScan Sample Output

> Scanned at 2026-03-11 15:29 UTC

## Funding Rate Arbitrage

| Symbol    | Long (低费率)        | Short (高费率)      | Rate Diff   | Est. APY%   | Risk   | Window |
|-----------|---------------------|---------------------|-------------|-------------|--------|--------|
| FILUSDT   | Binance -0.1206%    | OKX -0.0478%        | 0.0728%     | 79.8%       | HIGH   | ~8h    |
| WLDUSDT   | Binance -0.0300%    | Bybit 0.0100%       | 0.0399%     | 43.7%       | HIGH   | ~8h    |
| ETCUSDT   | OKX -0.0211%        | Bitget 0.0100%      | 0.0311%     | 34.1%       | HIGH   | ~8h    |
| WIFUSDT   | Bybit -0.0911%      | Bitget -0.0628%     | 0.0283%     | 31.0%       | HIGH   | ~8h    |
| DOGEUSDT  | Bybit -0.0155%      | Binance 0.0092%     | 0.0247%     | 27.0%       | HIGH   | ~8h    |
| SEIUSDT   | Binance -0.0367%    | OKX -0.0122%        | 0.0245%     | 26.8%       | HIGH   | ~8h    |
| DOTUSDT   | Binance -0.0368%    | Bitget -0.0131%     | 0.0237%     | 25.9%       | HIGH   | ~8h    |
| INJUSDT   | Binance -0.0216%    | OKX 0.0019%         | 0.0236%     | 25.8%       | HIGH   | ~8h    |
| BTCUSDT   | Binance -0.0111%    | OKX -0.0004%        | 0.0106%     | 11.6%       | LOW    | ~8h    |
| ETHUSDT   | Bybit -0.0017%      | OKX 0.0075%         | 0.0092%     | 10.1%       | LOW    | ~8h    |
| SOLUSDT   | Bybit -0.0062%      | Binance 0.0007%     | 0.0068%     | 7.5%        | LOW    | ~8h    |

> 27 total opportunities found in 152.2s

## How to Read This

- **Long (低费率)**: The exchange with the lower funding rate — go long here
- **Short (高费率)**: The exchange with the higher funding rate — go short here
- **Rate Diff**: The difference between the two rates (per funding interval)
- **Est. APY%**: Annualized yield estimate = `rate_diff × (365 × 24 / 8) × 100`
- **Risk**: LOW (APY<15% + major coin), MEDIUM (15-30%), HIGH (>30% or small cap)
- **Window**: Time until next funding settlement (~8h for most exchanges)

## Disclaimer

These are **theoretical opportunities**. Actual returns depend on execution costs, slippage, transfer times, and exchange risks. This is not financial advice.
