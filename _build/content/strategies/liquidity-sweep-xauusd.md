---
title: "Liquidity Sweeps on XAUUSD: How Gold Stop Runs Work"
short: "Liquidity Sweeps"
seo_title: "XAUUSD Liquidity Sweep Strategy: Trading Gold Stop Runs"
description: "Identify XAUUSD liquidity sweeps: where gold liquidity sits, sweep vs breakout, confirmation, invalidation and risk management for stop-run reversals."
lede: "Gold has a habit of spiking through obvious highs and lows and then snapping back. Here's how traders identify liquidity sweeps on XAUUSD, separate them from genuine breakouts, and manage the risk of trading them."
category: "Liquidity frameworks"
level: "Liquidity"
card: "Where gold liquidity sits, how to tell a sweep from a real breakout, and where invalidation belongs."
published: "2026-10-13"
reviewed: null
featured: true
order: 5
related:
  - /strategies/smart-money-concepts-xauusd/
  - /strategies/gold-breakout-retest-strategy/
  - /strategies/market-structure-xauusd/
  - /strategies/london-session-gold-trading/
charts:
  sweep-high:
    title: "Hypothetical sweep of equal highs followed by rejection"
    caption: "Two roughly equal highs create an obvious cluster of buy stops above. Price spikes through, fails to hold, and closes back inside the range before breaking lower. Hypothetical data."
    spec:
      seed: 8
      vol: 1.2
      path: [[0, 3810], [5, 3824], [9, 3816], [13, 3824], [17, 3816], [21, 3823], [23, 3820], [27, 3812], [31, 3804]]
      override: {"21": {h: 3830.2, c: 3822.4}}
      lines:
        - {y: 3825.4, label: "Equal highs — buy-side liquidity", color: muted, x1: 3, x2: 24}
        - {y: 3814.6, label: "Range low", color: muted, x1: 7, x2: 30, label_side: below}
      marks:
        - {i: 21, label: "Sweep + close back inside", pos: above, color: gold}
        - {i: 28, y: 3811.5, label: "Range low breaks", pos: below, color: red}
  sweep-vs-break:
    title: "Hypothetical genuine breakout: no rejection, acceptance above the level"
    caption: "Price moves through the same kind of level but keeps closing above it and builds a base. Without a rejection back inside, there is no sweep — just a breakout. Hypothetical data."
    spec:
      seed: 19
      vol: 1.2
      path: [[0, 3810], [5, 3824], [9, 3816], [13, 3824], [17, 3817], [21, 3829], [25, 3827], [30, 3840]]
      lines:
        - {y: 3825.4, label: "Equal highs", color: muted, x1: 3, x2: 30}
      marks:
        - {i: 22, label: "Closes hold above", pos: above, color: cyan}
faqs:
  - q: "What is a liquidity sweep in gold trading?"
    a: "It's a move through an obvious high or low — where many stop and breakout orders are likely clustered — that quickly reverses back inside the prior range. Traders also call it a stop hunt, stop run or false breakout."
  - q: "How do I know whether it's a sweep or a real breakout?"
    a: "You can't know in advance. The difference is confirmed by what happens next: a sweep closes back inside the range and fails to hold beyond the level; a breakout holds, builds acceptance and often retests the level from the other side."
  - q: "Where should the stop go on a sweep trade?"
    a: "Most traders place invalidation beyond the extreme of the sweep, plus a buffer. If price returns beyond that extreme, the sweep interpretation is wrong."
  - q: "Are sweeps more common at certain times?"
    a: "On XAUUSD, sweeps of the Asian range and previous-day extremes are frequently discussed around the London open and the New York open, and around major data releases. They can happen at any time."
---

## What a liquidity sweep is

In trading, **liquidity** refers to the orders available to trade against. Many orders cluster at predictable places: just above obvious highs (stop-losses of short sellers and buy-stop breakout entries) and just below obvious lows (stop-losses of buyers and sell-stop breakout entries).

A **liquidity sweep** is a move through one of those obvious levels that quickly reverses back inside the previous range. The orders beyond the level get triggered, but the move lacks follow-through. Traders also call this a stop hunt, a stop run or a false breakout.

Whether the sweep is "engineered" by large players, as [Smart Money Concepts](/strategies/smart-money-concepts-xauusd/) suggests, or simply the natural result of many orders clustering in one place, the behaviour is real and visible on the chart — and gold produces plenty of it.

## Where liquidity tends to sit on XAUUSD

- **Previous day's high and low** — widely watched by intraday gold traders.
- **The Asian-session range** — frequently tested at the London open.
- **Equal highs and equal lows** — two or more swing points at roughly the same price look like "strong" levels and attract stops.
- **Round numbers** — gold often trades through whole numbers before reacting.
- **Obvious trendlines** — many traders place stops just beyond them.

[[chart:sweep-high]]

## Sweep or breakout? The key distinction

Every sweep starts out looking like a breakout. The difference only appears afterwards:

| Behaviour | Likely sweep | Likely breakout |
|---|---|---|
| Close after the move | Back inside the prior range | Beyond the level |
| Follow-through | Little or none | Continues or consolidates beyond the level |
| Retest | Level becomes resistance/support against the move | Level holds from the other side |
| Structure | Short-term structure shifts back | Structure continues in breakout direction |

[[chart:sweep-vs-break]]

This is why the most important rule in sweep trading is **wait for the rejection**. Trying to fade a move while it's still pushing through a level is simply betting against a breakout.

## Step-by-step: analysing a potential sweep

1. **Mark obvious liquidity in advance.** Before the session, mark the previous-day high/low, the Asian range and any equal highs or lows.
2. **Define context.** What is the higher-timeframe trend? Sweeps against the higher-timeframe trend into a major level are generally more interesting than sweeps in the middle of a range.
3. **Watch for the run.** Price trades through the level.
4. **Require rejection.** A close back inside the range on your execution timeframe — and, for a stricter rule, a break of the short-term swing in the opposite direction ([market structure shift](/strategies/market-structure-xauusd/)).
5. **Define the plan.** Entry area (often a pullback after the rejection), invalidation beyond the sweep extreme, and an objective such as the opposite side of the range.

## Entry conditions and invalidation (educational example)

:::hypo
On a hypothetical H1 chart, gold has formed equal highs near 3,825.4 with a range low near 3,814.6. Early in the New York session price spikes to 3,830.2, then the candle closes back at 3,822.4, inside the range. A trader using a sweep model might wait for a pullback toward the swept level, considering a short with invalidation above 3,830.2 plus a buffer (for example 3,833), and the range low around 3,814.6 as an initial objective. A sustained close back above the equal highs would show the move was a breakout, not a sweep.
:::

## Risk management

- **Invalidation beyond the extreme.** The sweep wick defines where the idea fails. A stop inside the wick will often be taken by a second probe.
- **Second sweeps happen.** Gold sometimes sweeps a level twice. Decide in advance whether you'll re-enter, and with what risk.
- **News distortion.** Sweeps around US data are often fast and wide, with slippage. Many traders avoid entries in the minutes around releases.
- **Size from the stop.** Sweep wicks on gold can be large, so the logical stop can be wide. Reduce size accordingly — see [XAUUSD risk management](/strategies/xauusd-risk-management/).

## Common mistakes and limitations

- **Calling every break a sweep.** Many breakouts are genuine. If you fade them all, you'll be on the wrong side of every trend day.
- **Entering before the rejection.** "It's going to sweep and reverse" is a prediction, not a setup.
- **Labelling after the fact.** Sweeps are easy to spot in hindsight. Mark the liquidity before the session to test yourself honestly.
- **Ignoring the trend.** A sweep of a low in a strong downtrend often leads only to a brief bounce.

The limitation of any liquidity-based model is that the concept describes a common pattern but can't tell you which instance will follow through. Clear rules, consistent invalidation and honest journaling are what turn the idea into a testable approach.
