---
title: "XAUUSD Risk Management and Position Sizing"
short: "Risk Management"
seo_title: "Gold Trading Risk Management: XAUUSD Position Sizing Guide"
description: "XAUUSD risk management: position sizing from stop distance, contract size, leverage, stop placement, loss limits, and news and gap risk, with examples."
lede: "Most traders don't fail because their analysis is bad — they fail because one bad week takes too much of their account. This guide shows how to size XAUUSD positions, where stops belong, and how to build limits that keep you trading."
category: "Risk & process"
level: "Essential"
card: "Size gold positions from stop distance, understand contract size and leverage, and set limits that protect you."
published: "2026-10-13"
reviewed: null
featured: true
order: 9
related:
  - /blog/risk-management-volatile-gold-markets/
  - /blog/how-to-build-a-xauusd-trading-plan/
  - /blog/how-to-keep-a-trading-journal/
  - /strategies/new-york-session-gold-trading/
charts:
  rm-stop:
    title: "Hypothetical stop placement: inside noise versus beyond structure"
    caption: "A stop just below the support line sits inside normal gold noise and is hit before the move develops. A stop beyond the swing low plus a buffer survives — with a smaller position size to keep the same dollar risk. Hypothetical data."
    spec:
      seed: 77
      vol: 1.2
      path: [[0, 3826], [6, 3814], [10, 3820], [14, 3813.5], [16, 3816], [19, 3812], [23, 3824], [28, 3832]]
      override: {"19": {l: 3809.6}}
      zones:
        - {y1: 3812.4, y2: 3815, x1: 4, x2: 28, label: "SUPPORT ZONE", color: green}
      lines:
        - {y: 3811.6, label: "Tight stop — inside noise", color: red, x1: 15, x2: 28, label_side: below}
        - {y: 3806.8, label: "Structural stop + buffer", color: gold, x1: 15, x2: 28, label_side: below}
      marks:
        - {i: 19, label: "Wick takes tight stop", pos: below, color: red}
faqs:
  - q: "How much should I risk per gold trade?"
    a: "Many educators suggest risking a small, fixed percentage of the account per trade — often cited in the range of 0.5% to 2%. What's appropriate depends on your experience, strategy and circumstances. This is general education, not a personal recommendation."
  - q: "How much is one lot of XAUUSD?"
    a: "On many platforms, one standard lot of XAUUSD is 100 troy ounces, so a $1 move in price equals about $100 per lot. Some brokers use different contract sizes, so always check your broker's contract specifications."
  - q: "Is a stop-loss guaranteed to limit my loss?"
    a: "No. A standard stop-loss becomes a market order when triggered. During fast markets, news releases and weekend gaps, it can be filled at a worse price (slippage). Some brokers offer guaranteed stops for a fee; terms vary."
  - q: "Does high leverage increase risk?"
    a: "Leverage itself only determines how much margin a position requires. The real risk is position size relative to your account. High leverage makes it easy to open positions that are far too large, which is why it contributes to large losses."
---

## Why risk management comes first

Gold is one of the most volatile major markets that retail traders commonly access. It can move many dollars within minutes around US data, and it can gap over a weekend. With leverage, those moves translate directly into large swings in account value.

Risk management is what keeps a run of normal losses from becoming a disaster. Every strategy — [support and resistance](/strategies/support-and-resistance-xauusd/), [SMC](/strategies/smart-money-concepts-xauusd/), [breakouts](/strategies/gold-breakout-retest-strategy/) — will have losing streaks. Your sizing rules decide whether you survive them.

:::note
**Pro tip:** check your broker's contract size and margin rules once, write them down, and size every trade from them. Pros never guess their lot size.
:::

## Understanding XAUUSD contract size

Before you can size a position, you need to know what a price move is worth. On many platforms:

| Position size | Ounces | Value of a $1 move |
|---|---|---|
| 1.00 lot | 100 oz | about $100 |
| 0.10 lot | 10 oz | about $10 |
| 0.01 lot | 1 oz | about $1 |

So a $10 move against a 1-lot position is roughly a $1,000 loss. Because brokers can define lots differently, confirm this in your own platform before relying on it.

## Position sizing from the stop distance

The standard approach is:

> **Position size = (Account balance × risk %) ÷ (stop distance in $ × value per $1 move per lot)**

### Worked example

:::hypo
A trader has a $10,000 account and risks 1% per trade: $100. The trade idea's logical invalidation is $8 away from the entry. With a contract where $1 per ounce equals $100 per lot, one lot would lose $800 at the stop. Position size = $100 ÷ $800 = 0.125 lots, which the trader rounds **down** to 0.12 lots. If the stop were $16 away instead, the position would be roughly 0.06 lots — half the size for the same dollar risk.
:::

The key principle: **the stop is decided by the chart; the position size is decided by the stop.** Never pick a lot size first and then squeeze the stop to fit it.

## Where stops belong

A stop should sit where your trade idea is clearly wrong, plus a buffer for normal noise.

[[chart:rm-stop]]

- **Beyond structure, not at it.** Below the swing low that defines your idea, not just below the support line.
- **Add a volatility buffer.** Many traders use a fraction of ATR on their execution timeframe.
- **Account for the spread.** Sell stops trigger on the bid and buy stops on the ask; spreads widen at news and during thin hours.
- **If the logical stop is too wide**, the answer is a smaller position — or skipping the trade.

## Limits that protect the account

Individual trade risk isn't enough on its own. Common additional limits include:

- **Daily loss limit** — for example stopping for the day after losing a set multiple of normal risk.
- **Weekly drawdown limit** — stepping back to review after a defined weekly loss.
- **Maximum open risk** — capping total risk across all open positions, including correlated ones (for example gold and silver, or gold and a dollar pair).
- **Losing-streak rule** — reducing size after a run of losses, rather than increasing it to "win it back".

Write these into your [trading plan](/blog/how-to-build-a-xauusd-trading-plan/) before you need them.

## News, gaps and slippage

- **Scheduled news:** consider being flat, reducing size, or not entering in the minutes before and after major US releases. See [New York-session gold trading](/strategies/new-york-session-gold-trading/).
- **Weekend gaps:** gold can open Monday far from Friday's close. Positions held over the weekend carry gap risk that stops cannot fully control.
- **Slippage:** in fast markets, stops can fill worse than the stop price. Your real worst-case loss can exceed your planned risk.

## Reward-to-risk and expectancy

Reward-to-risk compares the potential gain to the planned loss. A 2:1 ratio means aiming to make twice what you risk. On its own it says nothing about profitability: what matters is **expectancy** — win rate and average win versus average loss across many trades. A high-ratio setup that rarely works can lose money; a lower-ratio setup with a higher win rate may not. Only a journal of real or carefully simulated trades can tell you which you have — see [how to keep a trading journal](/blog/how-to-keep-a-trading-journal/).

## Common mistakes

- Sizing by "feel" or by a fixed lot regardless of stop distance.
- Moving the stop further away once the trade goes against you.
- Increasing size after losses.
- Ignoring correlation between positions.
- Holding full size through major news or over weekends without a plan.
- Treating a stop-loss as a guaranteed maximum loss.

Good risk management is unglamorous. It doesn't make any single trade better. It makes sure that you're still here — with capital and confidence intact — when your analysis is right.
