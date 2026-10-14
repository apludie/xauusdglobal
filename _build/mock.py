"""Design preview of the planned community chat room.

Always rendered with a visible label: it is an example conversation with
example roles, not real members or real messages.
"""
import random


def _mini_chart():
    rnd = random.Random(7)
    price, xs = 40.0, []
    path = [0.4, 0.6, 0.3, -0.5, -0.7, -0.4, -0.9, 0.2, 0.8, 1.1, 0.6, 0.9, 1.3, 0.4, 1.0, 1.2]
    for i, d in enumerate(path):
        o = price
        c = price + d * 6
        hi = max(o, c) + rnd.uniform(1, 4)
        lo = min(o, c) - rnd.uniform(1, 4)
        if i == 6:
            lo -= 9
        xs.append((o, c, hi, lo))
        price = c
    lo_all = min(x[3] for x in xs)
    hi_all = max(x[2] for x in xs)
    H, W = 120, 300

    def y(v):
        return H - 10 - (v - lo_all) / (hi_all - lo_all) * (H - 20)

    out = []
    for i, (o, c, hi, lo) in enumerate(xs):
        cx = 12 + i * 18
        col = "#3ecf8e" if c >= o else "#ef6461"
        out.append(f'<line x1="{cx}" x2="{cx}" y1="{y(hi):.1f}" y2="{y(lo):.1f}" stroke="{col}" stroke-width="1.2"/>'
                   f'<rect x="{cx - 4}" y="{min(y(o), y(c)):.1f}" width="8" height="{max(abs(y(o) - y(c)), 1.5):.1f}" fill="{col}" rx="1"/>')
    zy = y(xs[6][3]) - 4
    eh = y(hi_all) + 4
    return (f'<svg class="mock-chart" viewBox="0 0 {W} {H}" role="img" aria-label="Illustrative mini gold chart: a sweep into a demand zone">'
            f'<rect x="0" y="{zy - 10:.1f}" width="{W}" height="16" fill="rgba(62,207,142,.12)" stroke="rgba(62,207,142,.45)" stroke-dasharray="3 3"/>'
            f'<text x="{W - 6}" y="{zy + 1:.1f}" text-anchor="end" fill="#3ecf8e" font-size="8" font-family="monospace">DEMAND ZONE</text>'
            f'<line x1="0" x2="{W}" y1="{eh:.1f}" y2="{eh:.1f}" stroke="#f2c14e" stroke-dasharray="4 3" stroke-width=".8"/>'
            f'<text x="6" y="{eh - 3:.1f}" fill="#f2c14e" font-size="8" font-family="monospace">EQUAL HIGHS</text>'
            + "".join(out) + "</svg>")


def _av(initials, cls):
    return f'<span class="mock-av mock-av--{cls}" aria-hidden="true">{initials}</span>'


def _lvl(name):
    return f'<span class="mock-lvl mock-lvl--{name.lower()}">{name}</span>'


REPLIES = [
    ("SR", "a", "structure_reader", "Advanced",
     "Structure supports the idea — the H1 higher low held. But your entry is in the middle of the zone. Would you wait for a reaction first?", "3"),
    ("LL", "b", "liquidity_lens", "Pro",
     "Equal highs above are still untouched. Price could run there first. Does that change your target — or your entry?", "5"),
    ("RF", "c", "risk_first", "Pro",
     "US CPI is due later today. Your stop is tight for a news spike. Smaller size, or wait until after the release?", "7"),
]


def chat_mockup(compact=False):
    rooms = "".join(f'<li class="{c}"><span>#</span>{n}</li>' for n, c in [
        ("start-here", ""), ("chart-breakdowns", "on"), ("trade-reviews", ""), ("ask-anything", ""),
        ("starter-room", ""), ("advanced-room", ""), ("pro-room", ""), ("degen-room", "")])
    replies = REPLIES[1:] if compact else REPLIES
    reply_html = "".join(
        f'<div class="mock-msg mock-msg--reply" style="--z:{44 + i * 18}px">{_av(ini, c)}<div>'
        f'<div class="mock-meta"><b>@{u}</b>{_lvl(lv)}<time>just now</time></div>'
        f'<p>{t}</p><div class="mock-react"><span>💡 {r}</span><span>↩ Reply</span></div></div></div>'
        for i, (ini, c, u, lv, t, r) in enumerate(replies))
    review = "" if compact else (
        '<div class="mock-review" style="--z:80px"><div class="mock-review__head"><span class="mock-pin">Trade review</span>'
        f'<b>@new_to_gold</b>{_lvl("Starter")}</div><ul>'
        '<li><span>Result</span>Stopped out — loss of 0.5%</li>'
        '<li><span>Decision quality</span>Plan followed, risk as planned ✓</li>'
        '<li><span>Lesson</span>Check the calendar before entry</li></ul></div>')
    post = (f'<div class="mock-msg mock-msg--post" style="--z:24px">{_av("NG", "d")}<div>'
            f'<div class="mock-meta"><b>@new_to_gold</b>{_lvl("Starter")}<time>London session</time></div>'
            '<p>XAUUSD H1 — considering a long from this demand zone after the sweep. Real reversal or just a pullback? What am I missing?</p>'
            f'<div class="mock-card">{_mini_chart()}<dl class="mock-plan">'
            '<div><dt>Context</dt><dd>H4 uptrend, London open</dd></div>'
            '<div><dt>Thesis</dt><dd>Sweep into demand, then continuation</dd></div>'
            '<div><dt>Invalidation</dt><dd>H1 close below the zone</dd></div>'
            '<div><dt>Risk</dt><dd>0.5% of account</dd></div></dl></div></div></div>')
    cls = "mock-wrap mock-wrap--compact" if compact else "mock-wrap"
    return f'''<figure class="{cls}" data-tilt>
  <figcaption class="mock-label"><span class="dot dot--gold"></span>Design preview · example conversation, not real members</figcaption>
  <div class="mock">
    <aside class="mock-side" aria-hidden="true"><div class="mock-brand">XAUUSD <span>Global</span></div><ul class="mock-rooms">{rooms}</ul></aside>
    <div class="mock-main">
      <div class="mock-top"><b># chart-breakdowns</b><span>Share the chart. Share the reasoning.</span></div>
      <div class="mock-thread">{post}{reply_html}{review}</div>
      <div class="mock-compose" aria-hidden="true"><span>Share your chart, thesis and invalidation…</span><i>Context</i><i>Thesis</i><i>Invalidation</i><i>Risk</i></div>
    </div>
  </div>
</figure>'''
