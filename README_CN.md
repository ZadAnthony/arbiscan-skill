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
| **稳定币脱锚监控** | 监测 USDC/DAI/FDUSD/TUSD 偏离 $1 的情况 | 稳定币价格 |

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

## 示例输出

```
  Funding Rate Arbitrage
================================================================================
Symbol     Long (低费率)         Short (高费率)        Rate Diff   Est. APY%   Risk    Window
---------  -------------------  --------------------  ----------  ----------  ------  --------
WIFUSDT    Bybit 0.0012%        Binance 0.0450%       0.0438%     48.0%       HIGH    ~8h
ETHUSDT    OKX 0.0030%          Bitget 0.0310%        0.0280%     30.7%       MEDIUM  ~8h
BTCUSDT    Bybit 0.0100%        OKX 0.0180%           0.0080%     8.8%        LOW     ~8h
```

## 可组合使用

ArbiScan 设计为与交易所交易 Skill 配合使用：

1. **ArbiScan** 扫描发现机会（本 Skill）
2. **Binance/Bybit/Bitget Skill** 执行交易（如果你决定行动）
3. **TradeOS** 可管理完整的套利工作流

```
"用 ArbiScan 找机会，然后用 Binance skill 执行最优的那个"
```

## 设计理念："看和用分开"

ArbiScan **只扫描、不交易**：
- 零风险：不接触你的资金，不需要 API key
- 纯信息：发现机会后，执行交给你或交易所 Skill
- 可组合：和 Binance/Bybit/Bitget 的交易 Skill 配合使用

## 工作原理

- 仅使用**公开 API 端点** — 无需 API key，无需认证
- 内置限频（请求间隔 200ms），遵守交易所速率限制
- 覆盖市值 **Top 100 交易对**
- 基于年化收益和币种类别的风险评分

## 支持的交易所

| 交易所 | 现货 | 合约 | 资金费率 |
|--------|------|------|----------|
| Binance | ✅  | ✅   | ✅       |
| Bybit   | ✅  | ✅   | ✅       |
| OKX     | ✅  | ✅   | ✅       |
| Bitget  | ✅  | ✅   | ✅       |

## 免责声明

ArbiScan 仅供信息参考，不构成投资建议。显示的套利机会是理论值，实际执行需考虑：

- Gas/提币手续费
- 交易所之间的转账时间
- 滑点和流动性
- 交易所对手风险
- 合规要求

请自行研究后再做决策。

## 开源协议

MIT
