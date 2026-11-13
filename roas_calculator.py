#!/usr/bin/env python3
"""
ROAS Calculator for Cross-border E-commerce

A command-line tool to calculate Return on Ad Spend (ROAS), break-even CPA,
profit margins, and optimal ad budget allocation for cross-border sellers.

Author: Bob Tong (https://kuajingbase.com)
License: MIT
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ProductMetrics:
    """Core product economics."""
    selling_price: float          # 售价 (USD)
    cost_of_goods: float          # 货物成本 (USD)
    shipping_cost: float = 0.0    # 物流成本 (USD)
    payment_fee_rate: float = 0.029  # 支付手续费率 (默认 Stripe 2.9%)
    payment_fee_fixed: float = 0.30  # 支付固定费 (默认 Stripe $0.30)
    platform_fee_rate: float = 0.0   # 平台佣金率 (Shopify 0%, Amazon ~15%)
    refund_rate: float = 0.02        # 退款率 (默认 2%)
    tax_rate: float = 0.0            # 税率

    @property
    def payment_fee(self) -> float:
        return self.selling_price * self.payment_fee_rate + self.payment_fee_fixed

    @property
    def platform_fee(self) -> float:
        return self.selling_price * self.platform_fee_rate

    @property
    def refund_loss(self) -> float:
        return self.selling_price * self.refund_rate

    @property
    def tax(self) -> float:
        return self.selling_price * self.tax_rate

    @property
    def total_cost(self) -> float:
        """Total cost per unit (excluding ad spend)."""
        return (self.cost_of_goods + self.shipping_cost + self.payment_fee
                + self.platform_fee + self.refund_loss + self.tax)

    @property
    def gross_profit(self) -> float:
        """Gross profit per unit before ad spend."""
        return self.selling_price - self.total_cost

    @property
    def gross_margin(self) -> float:
        """Gross margin percentage before ad spend."""
        if self.selling_price == 0:
            return 0.0
        return (self.gross_profit / self.selling_price) * 100


@dataclass
class ROASResult:
    """Complete ROAS analysis result."""
    # Input metrics
    selling_price: float
    total_cost_per_unit: float
    gross_profit_per_unit: float
    gross_margin_pct: float

    # ROAS metrics
    breakeven_roas: float
    breakeven_cpa: float
    target_roas: Optional[float] = None
    target_cpa: Optional[float] = None
    net_profit_at_target: Optional[float] = None
    net_margin_at_target: Optional[float] = None

    # Budget simulation
    daily_budget: Optional[float] = None
    expected_daily_orders: Optional[float] = None
    expected_daily_revenue: Optional[float] = None
    expected_daily_profit: Optional[float] = None
    expected_monthly_profit: Optional[float] = None


def calculate_roas(product: ProductMetrics,
                   target_roas: Optional[float] = None,
                   daily_budget: Optional[float] = None,
                   avg_cpc: Optional[float] = None,
                   conversion_rate: Optional[float] = None) -> ROASResult:
    """
    Calculate ROAS metrics for a cross-border e-commerce product.

    Args:
        product: Product cost/pricing metrics
        target_roas: Desired ROAS multiplier (e.g., 3.0 = 300%)
        daily_budget: Daily ad budget in USD
        avg_cpc: Average cost per click in USD
        conversion_rate: Conversion rate as decimal (e.g., 0.02 = 2%)

    Returns:
        ROASResult with complete analysis
    """
    # Break-even ROAS: the minimum ROAS to not lose money
    # ROAS = Revenue / Ad Spend
    # At break-even: Ad Spend = Gross Profit per unit
    # So: Break-even ROAS = Selling Price / Gross Profit per unit
    if product.gross_profit <= 0:
        breakeven_roas = float('inf')
        breakeven_cpa = 0.0
    else:
        breakeven_roas = product.selling_price / product.gross_profit
        breakeven_cpa = product.gross_profit  # Max you can spend per acquisition

    result = ROASResult(
        selling_price=product.selling_price,
        total_cost_per_unit=round(product.total_cost, 2),
        gross_profit_per_unit=round(product.gross_profit, 2),
        gross_margin_pct=round(product.gross_margin, 1),
        breakeven_roas=round(breakeven_roas, 2),
        breakeven_cpa=round(breakeven_cpa, 2),
    )

    # Target ROAS analysis
    if target_roas and target_roas > 0:
        # At target ROAS: CPA = Selling Price / Target ROAS
        target_cpa = product.selling_price / target_roas
        net_profit = product.gross_profit - target_cpa
        net_margin = (net_profit / product.selling_price) * 100 if product.selling_price else 0

        result.target_roas = target_roas
        result.target_cpa = round(target_cpa, 2)
        result.net_profit_at_target = round(net_profit, 2)
        result.net_margin_at_target = round(net_margin, 1)

    # Budget simulation
    if daily_budget and avg_cpc and conversion_rate and conversion_rate > 0:
        daily_clicks = daily_budget / avg_cpc
        daily_orders = daily_clicks * conversion_rate
        daily_revenue = daily_orders * product.selling_price
        cpa = daily_budget / daily_orders if daily_orders > 0 else float('inf')
        daily_profit = daily_orders * product.gross_profit - daily_budget

        result.daily_budget = daily_budget
        result.expected_daily_orders = round(daily_orders, 1)
        result.expected_daily_revenue = round(daily_revenue, 2)
        result.expected_daily_profit = round(daily_profit, 2)
        result.expected_monthly_profit = round(daily_profit * 30, 2)

    return result


def format_report(result: ROASResult) -> str:
    """Format ROAS analysis as a readable report."""
    lines = []
    lines.append("=" * 60)
    lines.append("  ROAS CALCULATOR — Cross-border E-commerce Analysis")
    lines.append("  https://kuajingbase.com/en/toolkit/roas-calculator")
    lines.append("=" * 60)
    lines.append("")

    # Section 1: Product Economics
    lines.append("📦 PRODUCT ECONOMICS")
    lines.append(f"  Selling Price:        ${result.selling_price:.2f}")
    lines.append(f"  Total Cost/Unit:      ${result.total_cost_per_unit:.2f}")
    lines.append(f"  Gross Profit/Unit:    ${result.gross_profit_per_unit:.2f}")
    lines.append(f"  Gross Margin:         {result.gross_margin_pct}%")
    lines.append("")

    # Section 2: Break-even
    lines.append("📊 BREAK-EVEN ANALYSIS")
    if result.breakeven_roas == float('inf'):
        lines.append("  ⚠️  Negative margin — cannot break even with ads!")
    else:
        lines.append(f"  Break-even ROAS:      {result.breakeven_roas}x")
        lines.append(f"  Break-even CPA:       ${result.breakeven_cpa:.2f}")
        lines.append(f"  (You must spend < ${result.breakeven_cpa:.2f} per sale to profit)")
    lines.append("")

    # Section 3: Target ROAS
    if result.target_roas:
        lines.append("🎯 TARGET ROAS ANALYSIS")
        lines.append(f"  Target ROAS:          {result.target_roas}x")
        lines.append(f"  Target CPA:           ${result.target_cpa:.2f}")
        lines.append(f"  Net Profit/Unit:      ${result.net_profit_at_target:.2f}")
        lines.append(f"  Net Margin:           {result.net_margin_at_target}%")

        if result.net_profit_at_target < 0:
            lines.append(f"  ⚠️  This ROAS target is BELOW break-even ({result.breakeven_roas}x)!")
        else:
            lines.append(f"  ✅  Profitable! (break-even is {result.breakeven_roas}x)")
        lines.append("")

    # Section 4: Budget Simulation
    if result.daily_budget:
        lines.append("💰 BUDGET SIMULATION (30-day projection)")
        lines.append(f"  Daily Ad Budget:      ${result.daily_budget:.2f}")
        lines.append(f"  Expected Daily Sales: {result.expected_daily_orders}")
        lines.append(f"  Expected Daily Rev:   ${result.expected_daily_revenue:.2f}")
        lines.append(f"  Expected Daily Profit:${result.expected_daily_profit:.2f}")
        lines.append(f"  Monthly Profit:       ${result.expected_monthly_profit:.2f}")

        if result.expected_monthly_profit < 0:
            lines.append("  ⚠️  Projected LOSS — optimize CPC or conversion rate!")
        else:
            lines.append("  ✅  Projected profitable campaign")
        lines.append("")

    lines.append("-" * 60)
    lines.append("  Built by Bob Tong | https://kuajingbase.com")
    lines.append("  Full guide: https://kuajingbase.com/en/toolkit/roas-calculator")
    lines.append("-" * 60)

    return "\n".join(lines)


def multi_channel_compare(product: ProductMetrics, channels: dict) -> str:
    """
    Compare ROAS across multiple ad channels.

    Args:
        product: Product metrics
        channels: Dict of {channel_name: {cpc, conversion_rate, daily_budget}}
    """
    lines = []
    lines.append("=" * 70)
    lines.append("  MULTI-CHANNEL ROAS COMPARISON")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"{'Channel':<15} {'CPC':>6} {'CVR':>6} {'CPA':>8} {'ROAS':>6} {'Daily P/L':>10}")
    lines.append("-" * 70)

    for name, config in channels.items():
        cpc = config.get('cpc', 0)
        cvr = config.get('conversion_rate', 0)
        budget = config.get('daily_budget', 50)

        if cvr > 0 and cpc > 0:
            cpa = cpc / cvr
            roas = product.selling_price / cpa if cpa > 0 else 0
            daily_clicks = budget / cpc
            daily_orders = daily_clicks * cvr
            daily_profit = daily_orders * product.gross_profit - budget
            status = "✅" if daily_profit > 0 else "❌"

            lines.append(
                f"{name:<15} ${cpc:>5.2f} {cvr*100:>5.1f}% ${cpa:>7.2f} {roas:>5.1f}x ${daily_profit:>8.2f} {status}"
            )

    lines.append("-" * 70)
    lines.append("")
    lines.append("  Compare more channels: https://kuajingbase.com/en/toolkit/roas-calculator")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="ROAS Calculator for Cross-border E-commerce — by KuajingBase.com",
        epilog="Full interactive version: https://kuajingbase.com/en/toolkit/roas-calculator",
    )

    parser.add_argument("--price", type=float, required=True,
                        help="Selling price per unit (USD)")
    parser.add_argument("--cogs", type=float, required=True,
                        help="Cost of goods sold per unit (USD)")
    parser.add_argument("--shipping", type=float, default=0,
                        help="Shipping cost per unit (USD, default: 0)")
    parser.add_argument("--payment-fee", type=float, default=0.029,
                        help="Payment processing fee rate (default: 0.029 for Stripe)")
    parser.add_argument("--payment-fixed", type=float, default=0.30,
                        help="Payment fixed fee per txn (default: 0.30)")
    parser.add_argument("--platform-fee", type=float, default=0.0,
                        help="Platform commission rate (default: 0 for Shopify, 0.15 for Amazon)")
    parser.add_argument("--refund-rate", type=float, default=0.02,
                        help="Refund/chargeback rate (default: 0.02)")
    parser.add_argument("--tax-rate", type=float, default=0.0,
                        help="Tax rate (default: 0)")

    parser.add_argument("--target-roas", type=float, default=None,
                        help="Target ROAS multiplier (e.g., 3.0)")
    parser.add_argument("--daily-budget", type=float, default=None,
                        help="Daily ad budget (USD)")
    parser.add_argument("--cpc", type=float, default=None,
                        help="Average cost per click (USD)")
    parser.add_argument("--cvr", type=float, default=None,
                        help="Conversion rate as decimal (e.g., 0.02 = 2%%)")

    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")

    parser.add_argument("--compare", action="store_true",
                        help="Run multi-channel comparison with example data")

    args = parser.parse_args()

    product = ProductMetrics(
        selling_price=args.price,
        cost_of_goods=args.cogs,
        shipping_cost=args.shipping,
        payment_fee_rate=args.payment_fee,
        payment_fee_fixed=args.payment_fixed,
        platform_fee_rate=args.platform_fee,
        refund_rate=args.refund_rate,
        tax_rate=args.tax_rate,
    )

    result = calculate_roas(
        product,
        target_roas=args.target_roas,
        daily_budget=args.daily_budget,
        avg_cpc=args.cpc,
        conversion_rate=args.cvr,
    )

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print(format_report(result))

    # Multi-channel comparison
    if args.compare:
        channels = {
            "Google Ads": {"cpc": 1.50, "conversion_rate": 0.025, "daily_budget": 50},
            "Facebook Ads": {"cpc": 0.80, "conversion_rate": 0.015, "daily_budget": 50},
            "TikTok Ads": {"cpc": 0.40, "conversion_rate": 0.010, "daily_budget": 50},
            "Pinterest Ads": {"cpc": 0.60, "conversion_rate": 0.020, "daily_budget": 30},
        }
        print()
        print(multi_channel_compare(product, channels))


if __name__ == "__main__":
    main()
