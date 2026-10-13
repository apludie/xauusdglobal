---
title: "How to Identify Support and Resistance on a Gold Chart"
short: "Identifying S/R on Gold"
seo_title: "How to Identify Support and Resistance on a Gold Chart"
description: "A repeatable routine to identify support and resistance on a gold chart: which levels to mark, zone width, ranking levels and keeping XAUUSD charts clean."
lede: "Most traders can define support and resistance. Far fewer can mark them consistently. This is a practical, repeatable routine for mapping the levels that matter on an XAUUSD chart in about ten minutes."
category: "Technical analysis"
card: "A repeatable ten-minute routine for mapping, ranking and cleaning up the gold levels that matter."
published: "2026-10-13"
reviewed: null
order: 3
related:
  - /strategies/support-and-resistance-xauusd/
  - /strategies/gold-breakout-retest-strategy/
  - /strategies/market-structure-xauusd/
  - /blog/how-to-build-a-xauusd-trading-plan/
charts:
  blog-sr-rank:
    title: "Hypothetical gold chart with ranked levels"
    caption: "A higher-timeframe level (A) with several reactions, an intraday level (B) from a recent swing, and a minor level (C) that a trader might delete to reduce clutter. Hypothetical data."
    spec:
      seed: 101
      vol: 1.3
      path: [[0, 3804], [5, 3820], [9, 3810], [13, 3826], [17, 3812], [21, 3822], [25, 3809], [30, 3824]]
      zones:
        - {y1: 3807.5, y2: 3811, label: "A — tier 1 (multiple reactions)", color: green, label_pos: bottom}
        - {y1: 3824.5, y2: 3827.5, label: "B — tier 2 (recent swing high)", color: gold}
      lines:
        - {y: 3818, label: "C — minor, consider deleting", color: muted, x1: 2}
---

## Why consistency matters more than precision

Two traders can look at the same gold chart and draw completely different levels. That isn't a problem in itself — but if *you* draw levels differently every day, you can't test anything, compare anything or learn from your results. The goal of this routine is not to find "perfect" levels. It's to mark them the **same way every time**.

This article is the practical companion to our full [support and resistance guide for XAUUSD](/strategies/support-and-resistance-xauusd/), which covers how traders build trades around levels.

## Before you start: set up a clean chart

- Remove indicators you won't use for the decision.
- Use the same colour code every day (for example: daily levels in one colour, H4 in another).
- Decide your zone width rule in advance — for example, the area covering the candle bodies and wicks of the reactions, or a fixed fraction of the daily ATR.

## The ten-minute level-mapping routine

### Step 1 — Weekly and daily anchors (3 minutes)

On the daily chart, mark:

- The **previous week's high and low**.
- The **previous day's high and low**.
- Two or three **major swing points** from the last few months that are visible at a glance.

These are the levels most gold traders will be watching.

### Step 2 — H4 reaction zones (3 minutes)

Switch to H4 and add zones where price has:

- Turned at least twice, or
- Launched a strong move (a sharp rally or drop with little overlap), or
- Broken through and then retested from the other side.

Merge anything within a couple of dollars into a single zone.

### Step 3 — Session context (2 minutes)

On H1 or M15, mark the **Asian-session range** and any **round numbers** near current price. Note where the current session's high and low are.

### Step 4 — Rank and delete (2 minutes)

Give each level a tier:

| Tier | Typical characteristics |
|---|---|
| Tier 1 | Daily or weekly level, multiple clear reactions, recent |
| Tier 2 | H4 swing or zone, one or two reactions |
| Tier 3 | Minor intraday level, unclear history |

Now **delete most tier-3 levels**. If you still have more than four or five zones near price, you're probably keeping levels "just in case" — which makes every move look like it respected something.

[[chart:blog-sr-rank]]

## Questions to ask about every level

- **Would I have marked this before price reached it?** If not, it's hindsight.
- **What happened the last time price was here?** A sharp rejection is more meaningful than a slow drift.
- **Is it in the trend direction?** Support in an uptrend is more interesting than support in a downtrend.
- **Where are the stops?** Obvious levels attract stop orders, so expect probes through them. See [liquidity sweeps on XAUUSD](/strategies/liquidity-sweep-xauusd/).

## How wide should a gold zone be?

There's no universal answer, but some rules of thumb:

- Zones from **higher timeframes** are naturally wider than intraday ones.
- If price regularly overshoots your zone by a few dollars before reacting, your zone is too narrow.
- If your zone is so wide that a stop beyond it makes every trade unattractive, you may be merging levels that should be separate — or the level just isn't tradable on your timeframe.

## Keeping a level log

Add a simple line to your [trading journal](/blog/how-to-keep-a-trading-journal/) each day: the levels you marked, their tier, and what price did at each. After a few weeks you'll see which kinds of levels actually produce reactions for the way *you* trade — information no generic rule can give you.

## Practice exercise

Take a gold chart from a few weeks ago. Hide everything after a chosen date, run the routine, and save a screenshot. Then reveal the following days and record which levels mattered. Repeat for ten different dates. It's one of the fastest ways to build an honest feel for level quality — and an excellent thing to compare with other traders, who will often have marked something you missed.
