"""ArbiScan CLI 统一入口"""

import argparse
import sys
import time
from datetime import datetime

from funding_arb import scan_funding_arbitrage
from basis_arb import scan_basis_arbitrage
from spot_spread import scan_spot_spread
from stablecoin_depeg import scan_stablecoin_depeg
from formatter import format_output


BANNER = """
    _          _     _ ____
   / \\   _ __ | |__ (_) ___|  ___ __ _ _ __
  / _ \\ | '__|| '_ \\| \\___ \\ / __/ _` | '_ \\
 / ___ \\| |   | |_) | |___) | (_| (_| | | | |
/_/   \\_\\_|   |_.__/|_|____/ \\___\\__,_|_| |_|

  Cross-Exchange Arbitrage Scanner v0.1.0
  Scan only. No trading. No API keys needed.
"""


def run_scan(scan_type: str, fmt: str, min_apy: float):
    """运行指定类型的扫描"""
    scanners = {
        "funding": ("Funding Rate Arbitrage", scan_funding_arbitrage),
        "basis": ("Basis Arbitrage (Spot vs Futures)", scan_basis_arbitrage),
        "spread": ("Cross-Exchange Spot Spread", scan_spot_spread),
        "depeg": ("Stablecoin Depeg Monitor", scan_stablecoin_depeg),
    }

    if scan_type == "all":
        types_to_run = list(scanners.keys())
    elif scan_type in scanners:
        types_to_run = [scan_type]
    else:
        print(f"Unknown scan type: {scan_type}")
        print(f"Available: {', '.join(scanners.keys())}, all")
        sys.exit(1)

    total_opps = 0
    for stype in types_to_run:
        title, scanner = scanners[stype]
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}")

        if stype == "funding":
            rows, headers = scanner(min_apy=min_apy)
        elif stype == "depeg":
            rows, headers = scanner()
        else:
            rows, headers = scanner()

        print(format_output(rows, headers, fmt))
        print(f"  -> {len(rows)} opportunities found\n")
        total_opps += len(rows)

    return total_opps


def main():
    parser = argparse.ArgumentParser(
        description="ArbiScan - Cross-Exchange Arbitrage Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scanner.py --all
  python scanner.py --type funding --min-apy 10
  python scanner.py --type funding --format markdown
  python scanner.py --type spread --format json
        """
    )
    parser.add_argument("--all", action="store_true", help="运行所有扫描类型")
    parser.add_argument("--type", choices=["funding", "basis", "spread", "depeg"], help="指定扫描类型")
    parser.add_argument("--format", choices=["table", "markdown", "json"], default="table", help="输出格式")
    parser.add_argument("--min-apy", type=float, default=0, help="最低年化过滤（仅 funding 类型）")

    args = parser.parse_args()

    if not args.all and not args.type:
        parser.print_help()
        sys.exit(0)

    print(BANNER)
    print(f"  Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    scan_type = "all" if args.all else args.type
    start = time.time()
    total = run_scan(scan_type, args.format, args.min_apy)
    elapsed = time.time() - start

    print(f"{'='*80}")
    print(f"  Scan complete. {total} total opportunities in {elapsed:.1f}s")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
