# ArbiScan — 跨交易所套利扫描器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**扫描 Binance、OKX、Bybit、Bitget 之间的套利机会。只看不做，无需 API key。**

ArbiScan 是一个 [OpenClaw Skill](https://clawhub.ai)，扫描主流加密货币交易所之间的套利机会。它识别价格和费率差异，计算预估收益，以清晰的表格呈现。是否行动由你决定 — ArbiScan 只负责发现。

## 扫描类型

| 类型 | 功能 | 数据源 |
|------|------|--------|
| **资金费率套利** | 比较各交易所永续合约资金费率差异 | 公开资金费率端点 |
| **期现基差套利** | 发现同交易所现货与合约价差 | 现货 + 合约价格 |
| **跨所现货价差** | 寻找不同交易所之间的 bid/ask 价差 | 订单簿最优报价 |
| **稳定币脱锚监控** | 监测 USDT/USDC/DAI 偏离 $1 的情况 | 稳定币价格 |

## 快速开始

### 作为 OpenClaw Skill

从 ClawHub 安装，让 AI Agent 帮你扫描：

```
"扫描资金费率套利机会，APY 大于 10%"
"检查有没有稳定币在脱锚"
"看看 BTC 和 ETH 的跨所价差"
```

### 独立运行（Python）

```bash
cd scripts/
pip install -r requirements.txt

# 运行所有扫描
python scanner.py --all

# 只看资金费率套利，最低 10% 年化
python scanner.py --type funding --min-apy 10

# 输出 Markdown 格式
python scanner.py --type funding --format markdown

# 输出 JSON（适合管道处理）
python scanner.py --type spread --format json
```

## 设计理念："看和用分开"

ArbiScan **只扫描、不交易**：
- 零风险：不接触你的资金，不需要 API key
- 纯信息：发现机会后，执行交给你或交易所 Skill
- 可组合：和 Binance/Bybit/Bitget 的交易 Skill 配合使用

## 支持的交易所

| 交易所 | 现货 | 合约 | 资金费率 |
|--------|------|------|----------|
| Binance | ✅  | ✅   | ✅       |
| Bybit   | ✅  | ✅   | ✅       |
| OKX     | ✅  | ✅   | ✅       |
| Bitget  | ✅  | ✅   | ✅       |

## 免责声明

ArbiScan 仅供信息参考，不构成投资建议。显示的套利机会是理论值，实际执行需考虑 Gas 费、提币时间、滑点、流动性和交易所风险。请自行研究后再做决策。

## 开源协议

MIT
