# 📊 ROAS Calculator for Cross-border E-commerce

A free, open-source command-line tool to calculate **Return on Ad Spend (ROAS)**, break-even CPA, profit margins, and multi-channel ad budget allocation — built specifically for **cross-border e-commerce sellers**.

> 🌐 **Prefer a visual calculator?** Use the free online version at [kuajingbase.com/en/tools/roas-calculator](https://kuajingbase.com/en/tools/roas-calculator)

---

## Why This Tool?

Most ROAS calculators online are oversimplified — they only divide revenue by ad spend. But cross-border sellers deal with **hidden costs** that eat into margins:

- 💳 **Payment processing fees** (Stripe 2.9% + $0.30, PayPal 3.49%, etc.)
- 📦 **International shipping costs** ($5–$15 per order)
- 🏷️ **Platform commissions** (Amazon 15%, Shopify 0%)
- 🔄 **Refund/chargeback losses** (typically 2–5%)
- 💱 **Currency conversion fees** (0.5–2%)

This calculator factors in **all of these** to give you a realistic break-even ROAS — not the fantasy number most tools show.

> 📖 Learn more about cross-border payment fees: [Payment Methods Compared](https://kuajingbase.com/en/payment)

---

## Quick Start

**Requirements:** Python 3.8+

```bash
# Clone the repo
git clone https://github.com/reituman602/roas-calculator.git
cd roas-calculator

# Basic calculation
python roas_calculator.py --price 49.99 --cogs 12.00 --shipping 5.50

# With target ROAS and budget simulation
python roas_calculator.py \
  --price 49.99 \
  --cogs 12.00 \
  --shipping 5.50 \
  --target-roas 3.0 \
  --daily-budget 50 \
  --cpc 1.20 \
  --cvr 0.02

# Multi-channel comparison
python roas_calculator.py \
  --price 49.99 \
  --cogs 12.00 \
  --shipping 5.50 \
  --compare

# JSON output (for piping to other tools)
python roas_calculator.py --price 49.99 --cogs 12.00 --json
```

---

## Example Output

```
============================================================
  ROAS CALCULATOR — Cross-border E-commerce Analysis
  https://kuajingbase.com/en/tools/roas-calculator
============================================================

📦 PRODUCT ECONOMICS
  Selling Price:        $49.99
  Total Cost/Unit:      $20.45
  Gross Profit/Unit:    $29.54
  Gross Margin:         59.1%

📊 BREAK-EVEN ANALYSIS
  Break-even ROAS:      1.69x
  Break-even CPA:       $29.54
  (You must spend < $29.54 per sale to profit)

🎯 TARGET ROAS ANALYSIS
  Target ROAS:          3.0x
  Target CPA:           $16.66
  Net Profit/Unit:      $12.88
  Net Margin:           25.8%
  ✅  Profitable! (break-even is 1.69x)

💰 BUDGET SIMULATION (30-day projection)
  Daily Ad Budget:      $50.00
  Expected Daily Sales: 0.8
  Expected Daily Rev:   $41.66
  Expected Daily Profit:$-26.37
  Monthly Profit:       $-791.10
  ⚠️  Projected LOSS — optimize CPC or conversion rate!
```

---

## Multi-Channel Comparison

Compare ROAS across Google, Facebook, TikTok, and Pinterest ads in one view:

```
======================================================================
  MULTI-CHANNEL ROAS COMPARISON
======================================================================

Channel          CPC    CVR      CPA   ROAS   Daily P/L
----------------------------------------------------------------------
Google Ads      $1.50   2.5%   $60.00   0.8x    $-25.18 ❌
Facebook Ads    $0.80   1.5%   $53.33   0.9x    $-22.37 ❌
TikTok Ads      $0.40   1.0%   $40.00   1.2x    $-13.07 ❌
Pinterest Ads   $0.60   2.0%   $30.00   1.7x     $-0.46 ❌
```

> 📖 **Deep dive into ad strategies:** [TikTok Ads Guide for Cross-border Stores](https://kuajingbase.com/en/articles) | [Facebook Ads vs TikTok Ads](https://kuajingbase.com/en/articles)

---

## All Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--price` | *required* | Selling price per unit (USD) |
| `--cogs` | *required* | Cost of goods sold per unit |
| `--shipping` | 0 | Shipping cost per unit |
| `--payment-fee` | 0.029 | Payment processing rate (Stripe: 0.029) |
| `--payment-fixed` | 0.30 | Payment fixed fee per transaction |
| `--platform-fee` | 0.0 | Platform commission (Amazon: 0.15, Shopify: 0) |
| `--refund-rate` | 0.02 | Refund/chargeback rate |
| `--tax-rate` | 0.0 | Tax rate |
| `--target-roas` | — | Target ROAS multiplier (e.g., 3.0) |
| `--daily-budget` | — | Daily ad spend (USD) |
| `--cpc` | — | Average cost per click (USD) |
| `--cvr` | — | Conversion rate (e.g., 0.02 = 2%) |
| `--compare` | — | Run multi-channel comparison |
| `--json` | — | Output as JSON |

---

## Use as a Python Module

```python
from roas_calculator import ProductMetrics, calculate_roas, format_report

product = ProductMetrics(
    selling_price=49.99,
    cost_of_goods=12.00,
    shipping_cost=5.50,
    payment_fee_rate=0.029,     # Stripe
    platform_fee_rate=0.0,      # Shopify (no commission)
)

result = calculate_roas(
    product,
    target_roas=3.0,
    daily_budget=100,
    avg_cpc=0.80,
    conversion_rate=0.02,
)

print(f"Break-even ROAS: {result.breakeven_roas}x")
print(f"Break-even CPA: ${result.breakeven_cpa}")
print(f"Monthly profit at target: ${result.expected_monthly_profit}")
```

---

## Common Scenarios for Cross-border Sellers

### Shopify Store (Self-hosted)
```bash
python roas_calculator.py --price 39.99 --cogs 8.00 --shipping 4.50 \
  --payment-fee 0.029 --platform-fee 0.0 --target-roas 3.0
```

### Amazon FBA
```bash
python roas_calculator.py --price 29.99 --cogs 6.00 --shipping 0 \
  --payment-fee 0.0 --platform-fee 0.15 --refund-rate 0.05 --target-roas 4.0
```

### WooCommerce + Stripe
```bash
python roas_calculator.py --price 59.99 --cogs 15.00 --shipping 6.00 \
  --payment-fee 0.029 --payment-fixed 0.30 --target-roas 2.5
```

> 📖 **Need help choosing a platform?** Read [Shopify vs WooCommerce — Which Is Right for You?](https://kuajingbase.com/en/compare/shopify-vs-woocommerce)

---

## Related Resources

- 🌐 [Online ROAS Calculator](https://kuajingbase.com/en/tools/roas-calculator) — Interactive web version with charts
- 💳 [Cross-border Payment Guide](https://kuajingbase.com/en/payment) — Compare Stripe, Airwallex, Wise, Payoneer fees
- 🏪 [Build Your First Store](https://kuajingbase.com/en/build-store) — Step-by-step from zero to first sale
- 🌐 [Best Hosting for E-commerce](https://kuajingbase.com/en/hosting) — Cloudways, VPS, and shared hosting compared
- 🛠️ [70+ Cross-border Tools Directory](https://kuajingbase.com/en/listings) — Every tool tested with real data

---

## Contributing

Issues and PRs are welcome! If you have ideas for new features (e.g., currency conversion, LTV projection, cohort analysis), please open an issue.

## License

MIT License — free to use, modify, and distribute.

---

**Built with ❤️ by [Bob Tong](https://kuajingbase.com/en/author) · [KuajingBase 跨境基地](https://kuajingbase.com)**

*A practical resource hub for cross-border e-commerce sellers — store setup, payment solutions, hosting reviews, and growth strategies.*
