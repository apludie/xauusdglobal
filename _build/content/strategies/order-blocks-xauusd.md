---
title: "Order Blocks on XAUUSD: Identification, Refinement and Risk"
short: "Order Blocks"
seo_title: "XAUUSD Order Blocks: How to Find and Trade Gold Order Blocks"
description: "How to identify XAUUSD order blocks, filter valid ones, refine them on lower timeframes, set invalidation and avoid common order block mistakes on gold."
lede: "Order blocks are one of the most used — and most over-used — tools in SMC-style gold trading. This guide gives you a strict definition, a filtering process and a realistic view of how often they fail."
category: "Liquidity frameworks"
level: "SMC"
card: "A strict definition, a filtering checklist and realistic expectations for trading gold order blocks."
published: "2026-10-13"
reviewed: null
featured: false
order: 6
related:
  - /strategies/smart-money-concepts-xauusd/
  - /strategies/fair-value-gap-xauusd/
  - /strategies/market-structure-xauusd/
  - /strategies/support-and-resistance-xauusd/
charts:
  ob-bull:
    title: "Hypothetical bullish order block with a structure break"
    caption: "The last down candle before an impulsive rally that breaks the prior swing high is marked as the order block. Price later returns to it. Hypothetical data."
    spec:
      seed: 41
      vol: 1.2
      path: [[0, 3824], [6, 3812], [9, 3816], [12, 3810], [13, 3809], [17, 3826], [20, 3830], [24, 3820], [26, 3815], [31, 3832]]
      override: {"13": {o: 3812, c: 3808.6, h: 3812.6, l: 3807.4}, "14": {o: 3808.6, c: 3814.4, l: 3808.2, h: 3814.8}, "15": {o: 3814.4, c: 3820.1, l: 3814, h: 3820.6}}
      lines:
        - {y: 3817.2, label: "Prior swing high → broken", color: muted, x1: 7, x2: 18}
      zones:
        - {y1: 3807.4, y2: 3812.6, x1: 13, x2: 31, label: "BULLISH ORDER BLOCK", color: cyan, label_pos: bottom}
      marks:
        - {i: 16, y: 3823, label: "Displacement", pos: above, color: cyan}
        - {i: 26, label: "Mitigation", pos: below, color: gold}
faqs:
  - q: "What is an order block in trading?"
    a: "In SMC terminology, a bullish order block is usually the last down-close candle before a strong rally that breaks structure; a bearish order block is the last up-close candle before a strong decline that breaks structure. Traders watch these areas for a reaction when price returns."
  - q: "How is an order block different from a supply or demand zone?"
    a: "They're closely related. Both mark the origin of a strong move. Order block definitions are usually narrower — a single candle — and require a structure break, whereas supply and demand zones are often drawn around a small base of candles."
  - q: "Should I use the full candle or just the body?"
    a: "Traders differ. Some use the full range including wicks; some use the body; others use the 50% level of the candle ('mean threshold'). Pick one rule, test it and apply it consistently."
  - q: "How often do order blocks hold?"
    a: "There's no reliable universal figure, and claims you see online are rarely verifiable. Many order blocks fail. The only meaningful statistic is the one from your own rule-based testing and journal."
---

## What an order block is

An **order block** is a price area that SMC traders believe marks where significant orders were placed before a strong move. The common working definition:

- **Bullish order block:** the last down-close candle (or small cluster) before an impulsive rally that **breaks structure** to the upside.
- **Bearish order block:** the last up-close candle before an impulsive decline that **breaks structure** to the downside.

The idea is that if large orders were only partly filled there, price may react when it returns — a return that SMC traders call "mitigation". As with all [Smart Money Concepts](/strategies/smart-money-concepts-xauusd/), this is a model, not something you can confirm from the chart. In practice, order blocks behave a lot like classic [supply and demand zones](/xauusd-trading-strategies/#supply-demand).

[[chart:ob-bull]]

## A filtering checklist

On any active gold chart there are dozens of "last opposing candles". Most mean nothing. Many traders apply filters such as:

1. **Did the move break structure?** Without a [Break of Structure or Change of Character](/strategies/market-structure-xauusd/), it's just a candle.
2. **Was the move impulsive?** Strong, large-bodied candles leaving a [fair value gap](/strategies/fair-value-gap-xauusd/) suggest urgency.
3. **Did it take liquidity first?** Order blocks that form right after a [liquidity sweep](/strategies/liquidity-sweep-xauusd/) are generally considered higher quality in SMC practice.
4. **Is it fresh?** Untested order blocks are preferred; each return weakens the case.
5. **Does it align with higher-timeframe direction?** A bullish order block inside an H4 downtrend is fighting the bigger flow.
6. **Is it in discount (for longs) or premium (for shorts)** of the relevant swing range?

## Refining an order block on XAUUSD

A single H4 gold candle can easily span ten dollars or more. Using the whole candle as a zone would require a very wide stop. Traders often **refine**: they drop to a lower timeframe (say M15) inside the H4 order block and look for the specific lower-timeframe candle or zone where the move originated.

Refinement reduces stop distance, but it also increases the chance that price reacts at the broader zone and never reaches the refined area — or trades straight through it. It's a trade-off, not a free improvement.

## Step-by-step methodology

1. Determine higher-timeframe bias and structure.
2. Identify a structure break with displacement on your setup timeframe.
3. Mark the last opposing candle before that move. Record which part you use (full range, body or 50%).
4. Apply the filtering checklist. Discard order blocks that fail it.
5. Decide whether to refine on a lower timeframe.
6. Plan entry (limit order at the zone or confirmation on a lower timeframe), invalidation and objective.

## Entry conditions and invalidation (educational example)

:::hypo
On a hypothetical H1 chart, gold sweeps below a prior low and prints a down candle from 3,812.6 to 3,808.6 (low 3,807.4). The next candles rally strongly, closing above the prior swing high at 3,817.2 and leaving an imbalance. The down candle (3,807.4–3,812.6) is marked as a bullish order block. A trader might consider a long position when price returns to the zone — either with a limit order near the top of the block or after a lower-timeframe bullish shift inside it — with invalidation below 3,807.4 plus a buffer. A close through the bottom of the block means the order block has failed.
:::

## Stop placement and risk

- Place invalidation **beyond the far edge of the order block**, not in its middle.
- If the logical stop is wide, reduce position size. Don't move the stop closer to make the trade "fit".
- Limit orders at order blocks can be filled during fast moves that slice straight through. Decide whether you prefer confirmation entries (lower risk of being run over, but more missed trades).
- See [XAUUSD risk management](/strategies/xauusd-risk-management/) for sizing calculations.

## Common mistakes and limitations

- **Marking every opposing candle** as an order block.
- **Ignoring whether structure actually broke.**
- **Trading old, repeatedly tested order blocks** as if they were fresh.
- **Counter-trend order blocks** without strong reasons.
- **Inconsistent definitions** — using the body on one trade and the wick on the next.

The deeper limitation: order blocks are subjective and widely watched, and there's no verified evidence that they reflect real institutional orders. Their usefulness lies in giving you a specific location and a specific invalidation — which only becomes an edge, if at all, through disciplined testing and review.
