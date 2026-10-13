---
title: "Gold Breakout and Retest Strategy for XAUUSD"
short: "Breakout & Retest"
seo_title: "Gold Breakout and Retest Strategy: XAUUSD Guide"
description: "A practical gold breakout and retest strategy for XAUUSD: defining ranges, confirming breakouts, trading the retest and avoiding false breakouts."
lede: "Gold spends much of its time in ranges — and then moves hard when it leaves them. The breakout-and-retest approach aims to join those moves with defined risk while filtering out the false breaks gold is famous for."
category: "Foundations"
level: "Foundations"
card: "Join gold's range expansions with defined risk — and filter out the false breakouts XAUUSD loves."
published: "2026-10-13"
reviewed: null
featured: false
order: 8
related:
  - /strategies/support-and-resistance-xauusd/
  - /strategies/liquidity-sweep-xauusd/
  - /strategies/london-session-gold-trading/
  - /strategies/xauusd-risk-management/
charts:
  br-asia:
    title: "Hypothetical Asian range breakout and retest during London"
    caption: "Price consolidates overnight, breaks above the range high with a strong close, pulls back to retest the old range high from above, then continues. Hypothetical data."
    spec:
      seed: 63
      vol: 0.9
      path: [[0, 3812], [3, 3817], [6, 3811], [9, 3816.5], [12, 3812], [15, 3816], [18, 3824], [21, 3828], [24, 3818.8], [28, 3834]]
      override: {"24": {l: 3817.4}}
      zones:
        - {y1: 3810.5, y2: 3818, x1: 0, x2: 16, label: "ASIAN RANGE", color: muted, label_pos: bottom}
      lines:
        - {y: 3818, label: "Range high", color: gold, x1: 16, x2: 28}
        - {y: 3814.5, label: "Example invalidation", color: red, x1: 21, x2: 28, label_side: below}
      marks:
        - {i: 18, label: "Breakout close", pos: above, color: cyan}
        - {i: 24, label: "Retest", pos: below, color: gold}
faqs:
  - q: "Should I enter on the breakout or wait for the retest?"
    a: "It's a trade-off. Entering on the breakout catches every move but suffers more false breakouts and usually needs a wider stop. Waiting for the retest filters some false breaks and allows tighter invalidation, but you'll miss breakouts that never come back."
  - q: "What counts as a confirmed breakout on gold?"
    a: "Many traders require a candle close beyond the level on their setup timeframe, ideally with a strong body. Some add a minimum distance beyond the level. Write your definition down and keep it consistent."
  - q: "Why do so many gold breakouts fail?"
    a: "Obvious range edges attract stop orders and breakout orders. Once those orders are filled, there may be no further buying or selling to push price on — especially outside active sessions or ahead of news. Those failed breakouts are often called liquidity sweeps."
  - q: "What's a good target for a breakout trade?"
    a: "Common approaches include the next significant support or resistance zone, a measured move equal to the range height, or trailing the stop behind new structure. Each has trade-offs; none is guaranteed."
---

## What the strategy is

A **breakout** happens when price closes decisively beyond a well-defined level or range. A **retest** is the return to that level afterwards. If the old resistance now acts as support (or vice versa), traders see it as confirmation that the breakout has been accepted.

The breakout-and-retest approach waits for that sequence before entering. It deliberately gives up the first part of the move in exchange for a clearer invalidation point and some protection against false breakouts.

## Why it suits XAUUSD — and why it's tricky

Gold alternates between quiet consolidation and sharp expansion. Classic examples:

- The **Asian-session range** broken during the London open.
- A **pre-news consolidation** broken after a US data release.
- A **multi-day range** on H4 broken as a macro theme develops.

But gold is also notorious for **false breakouts** — moves through range edges that quickly reverse. These are what liquidity-based traders call [liquidity sweeps](/strategies/liquidity-sweep-xauusd/). Any breakout method on XAUUSD must have a plan for them.

[[chart:br-asia]]

## Step-by-step methodology

1. **Define the range objectively.** Use clear swing highs and lows or a time-based range (such as the Asian session). Avoid redrawing it once price moves.
2. **Check context.** Is the higher-timeframe trend in the direction of the potential breakout? Is high-impact news scheduled?
3. **Confirm the breakout.** Require a candle close beyond the level on your setup timeframe. A strong body and expanding range add conviction.
4. **Wait for the retest.** Let price return toward the broken level.
5. **Look for a reaction.** A rejection from the level — for example a lower-timeframe higher low forming above it — confirms the role reversal.
6. **Execute with a plan.** Entry, invalidation and target set before entering.

## Entry conditions and invalidation (educational example)

:::hypo
Hypothetically, gold ranges between 3,810.5 and 3,818 during the Asian session. Shortly after the London open, an M15 candle closes at 3,824, well above the range high. Price extends to 3,828, then pulls back to 3,817.4 — slightly below the old range high — before closing back above 3,818. A trader following this method might consider a long position on that reaction, with invalidation back inside the range (for example below 3,814.5, where the breakout would clearly have failed), targeting a measured move equal to the range height (about 7.5 dollars above the range high) or the next resistance zone. If price closes back inside the range and holds, the breakout has failed.
:::

Notice that the retest went slightly *below* the range high. On gold, retests often overshoot. Rules that require a perfect touch will either miss trades or get stopped out by normal noise.

## Stop-loss and risk management

- **Invalidation belongs back inside the range**, beyond the retest low (for longs) — not exactly at the broken level.
- **Use the range height to sanity-check risk.** If the stop would be larger than the range itself, the reward-to-risk is unlikely to make sense.
- **Avoid breakouts into news.** A breakout five minutes before a major US release is mostly a bet on the release.
- **Size consistently.** See [XAUUSD risk management](/strategies/xauusd-risk-management/).

## Common mistakes and limitations

- **Chasing the breakout candle** far from any logical stop.
- **Redrawing the range** after the fact to make a breakout fit.
- **Treating any touch as a retest** without a reaction.
- **Ignoring time of day.** Breakouts during thin hours (late New York, holidays) often lack follow-through.
- **Not accepting missed trades.** Strong breakouts frequently never retest.

The method's main limitation is that it can't avoid failed breakouts entirely — it only reduces them. Combining it with [support and resistance](/strategies/support-and-resistance-xauusd/) context, session awareness ([London-session trading](/strategies/london-session-gold-trading/)) and strict risk control is what makes it workable.
