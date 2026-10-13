---
title: "Fair Value Gaps (FVG) on XAUUSD: A Practical Guide"
short: "Fair Value Gaps"
seo_title: "Fair Value Gap Gold Strategy: Trading XAUUSD FVGs"
description: "What a fair value gap is, how to spot bullish and bearish FVGs on XAUUSD, filter meaningful gaps, set entries and invalidation, and avoid FVG mistakes."
lede: "Fair value gaps appear on almost every fast gold move. That's exactly the problem. Learn how to identify FVGs precisely, filter the few that matter, and manage risk when you trade them."
category: "Liquidity frameworks"
level: "ICT / SMC"
card: "Identify bullish and bearish FVGs precisely and filter the few that are worth attention on gold."
published: "2026-10-13"
reviewed: null
featured: false
order: 7
related:
  - /strategies/ict-trading-xauusd/
  - /strategies/order-blocks-xauusd/
  - /strategies/smart-money-concepts-xauusd/
  - /blog/ict-concepts-for-gold-trading/
charts:
  fvg-bull:
    title: "Hypothetical bullish fair value gap and partial fill"
    caption: "The high of candle 1 and the low of candle 3 do not overlap, leaving a gap inside candle 2. Price later retraces into the gap and reacts. Hypothetical data."
    spec:
      seed: 52
      vol: 1.0
      path: [[0, 3810], [6, 3806], [9, 3809], [10, 3808], [14, 3826], [18, 3830], [22, 3820], [27, 3834]]
      override: {"10": {o: 3809.2, c: 3810.6, h: 3811.2, l: 3808.4}, "11": {o: 3810.6, c: 3818.3, h: 3818.8, l: 3810.2}, "12": {o: 3818.3, c: 3821.5, h: 3822.4, l: 3814.6}}
      zones:
        - {y1: 3811.2, y2: 3814.6, x1: 11, x2: 27, label: "BULLISH FVG", color: cyan, label_pos: bottom}
      marks:
        - {i: 10, y: 3811.2, label: "C1 high", pos: above, color: muted}
        - {i: 12, y: 3814.6, label: "C3 low", pos: below, color: muted}
        - {i: 22, label: "Retrace into gap", pos: below, color: gold}
faqs:
  - q: "What is a fair value gap?"
    a: "A fair value gap (FVG) is a three-candle pattern in which the first candle's high and the third candle's low (bullish) — or the first candle's low and the third candle's high (bearish) — do not overlap. The space between them, inside the middle candle, is the gap."
  - q: "Do fair value gaps always get filled?"
    a: "No. Many FVGs are only partly revisited and many are never revisited at all, especially in strong trends. The idea that gaps must be filled is a common and costly misconception."
  - q: "Is an FVG the same as a price gap?"
    a: "No. A classic price gap is a jump between one candle's close and the next candle's open, often over a weekend. An FVG is formed within continuous trading by three overlapping candles."
  - q: "What timeframe is best for FVGs on gold?"
    a: "Gaps on higher timeframes (H1 and above) are generally considered more significant than those on M1 or M5, where gaps are extremely common. Many traders use higher-timeframe gaps as areas of interest and lower timeframes to time entries."
---

## What a fair value gap is

A **fair value gap (FVG)** — also called an imbalance or inefficiency — is a three-candle pattern that marks an area where price moved so quickly that trading only happened in one direction.

- **Bullish FVG:** the **high of candle 1** is below the **low of candle 3**. The gap between them, inside the large middle candle, is the FVG.
- **Bearish FVG:** the **low of candle 1** is above the **high of candle 3**.

[[chart:fvg-bull]]

The concept is central to [ICT concepts](/strategies/ict-trading-xauusd/) and [Smart Money Concepts](/strategies/smart-money-concepts-xauusd/). The theory is that price may return to "rebalance" the area before continuing. In practice, an FVG is simply a measurable footprint of a fast move — useful for marking where momentum originated, but not a promise of anything.

## Why FVGs are everywhere on XAUUSD

Gold regularly moves several dollars in a single candle around session opens and economic releases. That means FVGs appear constantly, on every timeframe. If you treat them all as trade signals, you'll have dozens of "setups" per day. The real skill is **filtering**.

## Filtering meaningful gaps

Traders commonly prioritise FVGs that:

1. **Formed during displacement that broke structure** — for example the move that created a [Change of Character](/strategies/market-structure-xauusd/).
2. **Followed a liquidity sweep** — see [liquidity sweeps](/strategies/liquidity-sweep-xauusd/).
3. **Align with the higher-timeframe direction.**
4. **Sit in discount (for longs) or premium (for shorts)** of the relevant swing.
5. **Formed on a meaningful timeframe** — H1 or higher for context, lower timeframes only for entry refinement.
6. **Are still unfilled** — a gap that has already been fully traded through has lost its relevance in most frameworks.

## Ways traders use FVGs

- **As an entry area.** Placing an order inside the gap (at its edge or midpoint) in the direction of the original move.
- **As confluence.** Combining an FVG with an [order block](/strategies/order-blocks-xauusd/) or a support zone.
- **As a target.** Some traders treat unfilled gaps on the opposite side as potential objectives.
- **As a strength gauge.** A gap that price respects quickly suggests strong momentum; a gap that price slices through suggests the move is weakening.

## Entry conditions and invalidation (educational example)

:::hypo
On a hypothetical M15 chart during the London session, gold sweeps a prior low and then rallies hard. Candle 1 has a high of 3,811.2; candle 3 has a low of 3,814.6. The bullish FVG sits between 3,811.2 and 3,814.6, and the rally breaks the most recent lower high. A trader might place a limit order near the top of the gap (around 3,814.5) or wait for price to enter the gap and show a lower-timeframe bullish reaction. Invalidation could sit below the swing low that started the move rather than just below the gap, because price often trades through the full gap before reversing. A close well below the gap would mark the setup as failed.
:::

## Risk management

- **Don't place stops just below the gap by default.** Price often fills the entire gap and a little more. Use the swing low/high that created the move as a more robust invalidation, and size down.
- **Expect missed trades.** In strong momentum, price may never return.
- **Be careful around news.** FVGs created by a data release can be revisited violently, with wide spreads.
- **Fixed risk per trade.** Read [XAUUSD risk management](/strategies/xauusd-risk-management/).

## Common mistakes and limitations

- **"Gaps must fill."** They don't. Treating fills as inevitable leads to counter-trend trades against strong moves.
- **Trading every gap.** Without filters, FVGs become noise.
- **Ignoring timeframe.** An M1 gap has little to do with H4 structure.
- **Using inconsistent levels** — the edge on one trade, the midpoint on the next.
- **Hindsight.** The gaps that "worked" stand out; the ones that failed are forgotten. Journal every FVG you would have traded, not only the ones you did.

Fair value gaps are best thought of as a precise way to describe *where* a fast move began. Combined with structure, liquidity and strict risk rules, they can help define locations. On their own, they're not a strategy.
