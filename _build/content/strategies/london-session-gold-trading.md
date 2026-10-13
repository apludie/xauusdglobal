---
title: "London Session Gold Trading: How XAUUSD Behaves at the London Open"
short: "London Session"
seo_title: "London Session Gold Trading: XAUUSD at the London Open"
description: "How gold trades in the London session: the Asian range, London open behaviour, LBMA Gold Price auctions, common setups, timing and risk for XAUUSD."
lede: "London is the centre of the global over-the-counter gold market, and its open often sets the tone for the day. Here's how XAUUSD typically behaves during London hours and how session traders plan around it."
category: "Sessions & timing"
level: "Sessions"
card: "Why London matters for gold, how the Asian range gets tested, and how to plan around the open."
published: "2026-10-13"
reviewed: null
featured: true
order: 10
related:
  - /strategies/new-york-session-gold-trading/
  - /blog/london-vs-new-york-sessions/
  - /strategies/gold-breakout-retest-strategy/
  - /strategies/liquidity-sweep-xauusd/
charts:
  ldn-judas:
    title: "Hypothetical London open: false move against the trend, then expansion"
    caption: "After a narrow Asian range, the London open first pushes below the range low, sweeps it, then reverses and expands above the range high in the direction of the higher-timeframe trend. Hypothetical data."
    spec:
      seed: 88
      vol: 0.8
      path: [[0, 3814], [4, 3817.5], [8, 3813], [12, 3817], [15, 3815], [17, 3809], [19, 3814], [23, 3824], [27, 3830], [32, 3836]]
      override: {"17": {l: 3807.8, c: 3810.2}}
      zones:
        - {y1: 3812.4, y2: 3818.2, x1: 0, x2: 15, label: "ASIAN RANGE", color: muted}
      marks:
        - {i: 17, label: "Sweep of Asian low", pos: below, color: gold}
        - {i: 23, label: "Expansion", pos: above, color: cyan}
faqs:
  - q: "What time does the London session open for gold?"
    a: "Conventionally, 08:00 London time — 07:00 UTC during British Summer Time and 08:00 UTC in winter. Many brokers' gold markets are already open, so the 'open' refers to the jump in participation, not the start of trading."
  - q: "What is the LBMA Gold Price?"
    a: "It's a benchmark gold price set twice each London business day, at 10:30 and 15:00 London time, through an electronic auction. It's used as a reference for many contracts. Activity can increase around those times."
  - q: "Is the London session the best time to trade gold?"
    a: "There's no universally 'best' time. London typically offers higher liquidity and clearer directional moves than the Asian session, but also more false moves at the open. The best time is the one where your tested setups perform and you can trade attentively."
  - q: "Does the London open always sweep the Asian range?"
    a: "No. Sometimes it breaks out cleanly, sometimes it stays inside, and sometimes it sweeps one side and reverses. Treat it as a scenario to prepare for, not a rule."
---

## Why London matters for gold

London is the hub of the global over-the-counter (OTC) gold market: major bullion banks, the clearing system for loco London gold and the **LBMA Gold Price** benchmark are all centred there. When London traders arrive, participation and liquidity in XAUUSD typically increase sharply compared with the Asian session.

For intraday traders, that means the London open is often where the day's first meaningful move begins — and, frequently, where an early high or low of the day is set.

## Typical session timeline

| Time (London) | What tends to happen |
|---|---|
| Before 08:00 | Asian session; gold often trades in a narrower range |
| 07:00–08:00 | European pre-open; early positioning, occasional false moves |
| 08:00–10:00 | London open; volatility and volume rise, Asian range tested |
| 10:30 | LBMA Gold Price morning auction |
| 12:00–13:00 | Midday lull is common before US participants arrive |
| 13:00–17:00 | Overlap with New York; US data releases and the largest moves |
| 15:00 | LBMA Gold Price afternoon auction |

These are tendencies, not rules. Data releases from Europe or the UK, central-bank announcements, holidays and geopolitical news can change the picture on any day. Note that British and US clocks change on different dates in spring and autumn, which temporarily shifts the overlap.

## Common London-session scenarios

### 1. Asian range breakout

Price breaks out of the overnight range with momentum and continues. Traders may use the [breakout and retest strategy](/strategies/gold-breakout-retest-strategy/) to join the move after confirmation.

### 2. Sweep and reverse

Price first pushes through one side of the Asian range — taking the stops resting there — then reverses and expands in the opposite direction. ICT-style traders sometimes call this a "Judas swing". See [liquidity sweeps on XAUUSD](/strategies/liquidity-sweep-xauusd/).

[[chart:ldn-judas]]

### 3. Range continuation

On quiet days, especially ahead of major US data later in the day, gold may stay inside or near the Asian range all morning. Forcing breakout trades on these days often produces small, repeated losses.

## A pre-session routine

1. **Check the calendar** for European, UK and US releases and any central-bank speakers.
2. **Mark the Asian range high and low**, the previous day's high and low, and the higher-timeframe levels nearby.
3. **Define your bias** from H4/daily [market structure](/strategies/market-structure-xauusd/).
4. **Write two scenarios**: what you'll do on a breakout, and what you'll do on a sweep and reversal. Include invalidation for each.
5. **Set a time limit** — for example, no new entries after a certain hour if your setups haven't appeared.

## Entry conditions and invalidation (educational example)

:::hypo
Hypothetically, the H4 trend in gold is up. The Asian range runs from 3,812.4 to 3,818.2. Shortly after 08:00 London time, price drops to 3,807.8 — below the Asian low — and the candle closes back at 3,810.2. Over the next few candles price reclaims the range and breaks the short-term lower high. A trader following a sweep-and-reverse plan might look for a long entry on a pullback, with invalidation below 3,807.8 plus a buffer, and the Asian high and then the previous day's high as objectives. If price instead accepts below the Asian low, the scenario is invalid and the breakout-down scenario takes over.
:::

## Risk management in London

- **Volatility rises fast.** Use stops that account for the larger London ranges, and size down accordingly.
- **Expect false moves** in the first 30–60 minutes; many traders wait for structure to form.
- **Plan for US data later in the day.** Decide whether you'll close, reduce or protect London positions ahead of New York releases.
- Read the full [XAUUSD risk management](/strategies/xauusd-risk-management/) guide for sizing.

## Common mistakes and limitations

- Entering on the first spike at 08:00 without a plan.
- Assuming yesterday's London pattern will repeat.
- Ignoring daylight-saving shifts that move session times.
- Over-trading the midday lull after the morning move is done.
- Treating the Asian range as a magic level rather than one piece of context.

Session tendencies are useful precisely because they're tendencies. The value of studying London behaviour is preparing clear scenarios in advance — not predicting what happens at 08:01.
