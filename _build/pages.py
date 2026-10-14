"""Hand-designed pages: home, price, news, strategy hub, community, membership,
about, FAQ, legal pages and 404."""
import json
import os

import yaml

import config as C
import lib as L
from mock import chat_mockup
from lib import esc, icon

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")

TITLES = {
    "/": "XAUUSD Global home",
    "/xauusd-price/": "XAUUSD price and live gold chart",
    "/xauusd-news/": "XAUUSD news hub: what moves gold",
    "/xauusd-trading-strategies/": "XAUUSD trading strategies hub",
    "/blog/": "The XAUUSD Global blog",
    "/community/": "The XAUUSD Global community vision",
    "/membership/": "Membership levels and planned pricing",
    "/about/": "About XAUUSD Global",
    "/contact/": "Contact XAUUSD Global",
    "/faq/": "Frequently asked questions",
    "/risk-disclaimer/": "Risk disclaimer",
    "/privacy-policy/": "Privacy policy",
    "/terms/": "Terms of use",
    "/tools/position-size-calculator/": "XAUUSD position size calculator",
}


def tv_box(widget, cfg, cls, label):
    """Lazy third-party widget container with an honest placeholder."""
    if not C.PRICE_WIDGETS:
        return (f'<div class="tv-box {cls}"><div class="tv-placeholder"><div><strong>Demo state — no price data source configured</strong>'
                f'No live or delayed XAUUSD prices are shown on this site yet.</div></div></div>')
    return (f'<div class="tv-box {cls}" data-tv-widget="{widget}" aria-label="{esc(label)}">'
            f'<script type="application/json">{json.dumps(cfg)}</script>'
            f'<div class="tv-placeholder"><div><strong>Loading {esc(label)}…</strong>'
            f'Provided by TradingView. If nothing appears, the widget may be blocked by your browser or network.</div></div>'
            f'<noscript><div class="tv-placeholder"><div><strong>JavaScript is required for the live chart.</strong></div></div></noscript></div>')


DATA_CREDIT = ("Price data and charts on this page are supplied by an embedded <a href=\"https://www.tradingview.com/symbols/XAUUSD/\" "
               "rel=\"noopener nofollow\" target=\"_blank\">TradingView</a> widget (symbol " + C.TV_SYMBOL + "). Quotes are indicative, may be delayed, "
               "and can differ from your broker's prices. XAUUSD Global does not produce, verify or store this data, and any timestamp shown comes from the provider.")


def sessions_html():
    rows = [
        ("sydney", "Sydney", "07:00–16:00 Sydney time"),
        ("tokyo", "Tokyo / Asia", "09:00–18:00 Tokyo time"),
        ("london", "London", "08:00–17:00 London time"),
        ("newyork", "New York", "08:00–17:00 New York time"),
    ]
    items = "".join(
        f'<div class="session" data-session="{i}"><span class="session__name">{n}</span>'
        f'<span class="session__state">—</span><span class="session__hours">{h} · <span data-localtime></span></span></div>'
        for i, n, h in rows)
    return (f'<div class="sessions" data-sessions>{items}</div>'
            '<p class="session-note">Session status is calculated from your device clock using approximate, conventional session hours. '
            'It is not a market-data feed and ignores public holidays. Spot gold and gold CFDs usually trade almost 24 hours on weekdays, with a short daily break that varies by broker.</p>')


def tool_band():
    return f"""<a class="tool-band reveal" href="/tools/position-size-calculator/">
      <div class="tool-band__icon">{icon("scale")}</div>
      <div class="tool-band__text"><span class="eyebrow">Free tool</span><h3>XAUUSD Position Size Calculator</h3>
        <p>Enter your balance, risk % and stop-loss — get your gold lot size and risk-to-reward before you trade.</p></div>
      <span class="btn btn--gold btn--sm">Open calculator {ARROW_BTN}</span></a>"""


def card(path, title, text, tag=None, meta=None, ico=None, num=None):
    t = f'<span class="tag">{esc(tag)}</span>' if tag else ""
    i = f'<div class="card__icon">{icon(ico)}</div>' if ico else ""
    n = f'<div class="card__num">{esc(num)}</div>' if num else ""
    m = f'<div class="card__meta">{meta}</div>' if meta else ""
    return f'<article class="card card--link reveal">{i}{n}{t}<h3><a href="{path}">{esc(title)}</a></h3><p>{esc(text)}</p>{m}</article>'


HERO_CHART = {
    "id": "hero", "seed": 11, "vol": 2.2, "axis": False,
    "path": [[0, 40], [6, 52], [10, 46], [16, 60], [19, 55], [22, 50], [27, 66], [32, 74], [35, 70], [39, 80]],
    "override": {"22": {"l": 43.5}},
    "zones": [{"y1": 44, "y2": 48, "x1": 8, "x2": 39, "label": "DEMAND ZONE", "color": "cyan", "label_pos": "bottom"}],
    "lines": [{"y": 60.8, "label": "PRIOR HIGH", "color": "gold", "x1": 15, "x2": 39}],
    "marks": [{"i": 22, "y": 43.5, "label": "Sweep", "pos": "below", "color": "gold"},
              {"i": 27, "y": 66.5, "label": "BOS", "pos": "above", "color": "cyan"}],
}

ARROW_BTN = icon("arrow")


def home(strategies, posts):
    featured = [s for s in strategies if s.get("featured")][:6]
    latest = sorted(posts, key=lambda p: (p["published"], -p.get("order", 0)), reverse=True)[:3]
    strat_cards = "".join(card(s["path"], s["title"], s["card"], tag=s.get("level", "Strategy"), meta=f"<span>{s.get('minutes', '')} min read</span>") for s in featured)
    blog_cards = "".join(card(p["path"], p["title"], p["card"], tag=p["category"], meta=f"<time datetime='{p['published']}'>{L.fmt_date(p['published'])}</time><span>{p.get('minutes', '')} min read</span>") for p in latest)
    marquee_items = ["Bring your charts. Bring your questions. Bring your reasoning.", "Stop chasing signals. Start understanding gold.",
                     "A good trade can lose. A bad trade can win. Learn the difference.", "Understand the idea, not just the entry.",
                     "One market. Different perspectives. Better decisions."]
    mq = "".join(f"<span>{esc(t)}</span>" for t in marquee_items * 2)
    mini_cfg = {"symbol": C.TV_SYMBOL, "width": "100%", "height": "100%", "locale": "en", "dateRange": "1D",
                "colorTheme": "dark", "isTransparent": True, "autosize": True, "largeChartUrl": ""}
    faqs = [
        {"q": "Is this a signal group?", "a": "No. Trade ideas will be discussed, but always with their reasoning: context, thesis, invalidation and risk. The goal is for you to understand an idea well enough to judge it yourself, not to copy entries."},
        {"q": "Who is XAUUSD Global for?", "a": "Mainly intermediate gold traders — people who know some concepts but want to apply them more consistently. Motivated learners and experienced traders who enjoy explaining their thinking are welcome too."},
        {"q": "Is membership open?", "a": f"Not yet. The guides on this site are free and available now. The community is being prepared and membership is planned at **{C.PLANNED_PRICE}/month**. [Get launch updates](/membership/#registration) to hear first when it opens — no payment and no obligation."},
        {"q": "Will joining make me profitable?", "a": "No community, course or strategy can promise that. Trading leveraged gold products carries a high risk of loss. What we aim to help with is better reasoning, risk habits and review — the parts of trading you can control."},
        {"q": "Why only gold?", "a": "Gold has its own drivers, sessions and behaviour. Focusing on one market lets discussions go deep and lets traders compare like-for-like analysis on the same chart."},
    ]
    body = f"""
<section class="hero grid-bg">
  <div class="wrap hero__grid">
    <div>
      <span class="status-pill"><span class="dot"></span>Free guides available now · Community launching soon</span>
      <h1>Trade Gold. Think Deeper. <span class="gold-text">Grow Together.</span></h1>
      <p class="hero__lede">Learn to read the market, question trading ideas, review your decisions, and develop your own process alongside traders who take improvement seriously.</p>
      <div class="btn-row">
        <a class="btn btn--gold" href="/xauusd-trading-strategies/">Explore the Free Guides {ARROW_BTN}</a>
        <a class="btn btn--ghost" href="/membership/#registration">Get Launch Updates</a>
      </div>
      <div class="hero__status">
        <span class="status-pill"><span class="dot"></span>Education: free and open</span>
        <span class="status-pill"><span class="dot dot--gold"></span>Community: waitlist open</span>
      </div>
    </div>
    <div class="hero__visual">
      <div class="chart-card">
        <div class="particles" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
        <div class="chart-card__top"><span class="chart-card__sym">XAU/USD · ANALYSIS VIEW</span><span class="tf" aria-hidden="true"><span>M15</span><span class="on">H1</span><span>H4</span></span></div>
        {L.chart_svg(HERO_CHART, "Illustrative gold chart showing a liquidity sweep into a demand zone followed by a break of structure")}
        <p class="chart-card__note">Illustration with hypothetical data — not live prices. <a href="/xauusd-price/">See the XAUUSD chart</a>.</p>
      </div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee__inner">{mq}</div></div>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Sound familiar?</span><h2>Surrounded by information. Still alone with the chart.</h2>
      <p>You've watched the videos and learned the concepts — structure, liquidity, order blocks, fair value gaps. Then you open your own chart and the same questions come back.</p></div>
    <div class="cards cards--3 qgrid">
      <article class="card q-card reveal"><h3>Is this a genuine breakout, or a liquidity sweep?</h3></article>
      <article class="card q-card reveal"><h3>Why did this setup work yesterday but fail today?</h3></article>
      <article class="card q-card reveal"><h3>Where exactly would my idea be wrong?</h3></article>
      <article class="card q-card reveal"><h3>Is this a high-quality setup, or a trade I just want to take?</h3></article>
      <article class="card q-card reveal"><h3>Who can review my analysis and tell me what I missed?</h3></article>
      <article class="card q-card reveal"><h3>How do I stop relying on other people's calls?</h3></article>
    </div>
    <p class="lead center mt-3 reveal" style="max-width:760px;margin-left:auto;margin-right:auto"><strong>Information is everywhere. Structured learning, honest feedback and accountability are much harder to find.</strong> That's the gap XAUUSD Global exists to close.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Our approach</span>
        <h2>Understand the idea, not just the entry.</h2>
        <p class="lead">Videos are a great way to discover concepts, and a trade idea can be useful. But understanding an idea is what lasts. When the trade fails or the market changes, reasoning is what lets you decide for yourself.</p>
        <p>So every idea discussed at XAUUSD Global is expected to answer the same questions — before the outcome is known. Members learn to judge the quality of the reasoning, not just whether the trade won.</p>
        <p><strong>A well-reasoned trade can lose. A poorly reasoned trade can win.</strong> Learning to tell the difference is the skill we care about most.</p>
        <a class="btn btn--gold" href="/community/">See how the community will work {ARROW_BTN}</a>
      </div>
      <div class="compare reveal">
        <div class="compare__col compare__col--bad"><h3>A trade call tells you</h3><ul>
          <li>Where to enter</li><li>Where to put the stop</li><li>Where to take profit</li></ul></div>
        <div class="compare__col compare__col--good"><h3>A reasoned idea also tells you</h3><ul>
          <li>The market context</li><li>The thesis and its evidence</li><li>What would prove it wrong</li><li>The risk being taken</li><li>Other ways to read the chart</li><li>What to learn afterwards</li></ul></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split split--mock">
      <div class="reveal">
        <span class="eyebrow">A look inside the community</span>
        <h2>Not a signal feed. A room full of reasoning.</h2>
        <p class="lead">Post your chart and your thinking. Get it tested by traders who read gold differently — then review what really happened.</p>
        <ul class="checklist">
          <li>Every idea shares its context, thesis, invalidation and risk.</li>
          <li>Feedback challenges the analysis, never the person.</li>
          <li>Wins and losses are reviewed with the same honesty.</li>
        </ul>
        <div class="btn-row"><a class="btn btn--gold" href="/community/">See how the community will work {ARROW_BTN}</a></div>
      </div>
      <div>{chat_mockup(compact=True)}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">The learning journey</span><h2>From collecting concepts to building your own judgement.</h2>
      <p>Six stages, one direction: becoming a trader who can think through the market independently. Not everyone moves at the same pace, and nobody is promised a result.</p></div>
    <div class="steps steps--6">
      <div class="step reveal"><span class="tag tag--cyan">Available now</span><h3>Understand</h3><p>Study free guides on XAUUSD, price action, market structure, liquidity, sessions and risk.</p></div>
      <div class="step reveal"><span class="tag tag--cyan">Available now</span><h3>Apply</h3><p>Analyse your own charts, write scenarios and document your reasoning with our planning and journal guides.</p></div>
      <div class="step reveal"><span class="tag">With membership</span><h3>Discuss</h3><p>Share your analysis, ask specific questions and compare interpretations with other traders.</p></div>
      <div class="step reveal"><span class="tag">With membership</span><h3>Review</h3><p>Revisit decisions, find mistakes and learn from wins and losses alike.</p></div>
      <div class="step reveal"><span class="tag">With membership</span><h3>Improve</h3><p>Turn lessons into a more disciplined, evidence-aware and repeatable process.</p></div>
      <div class="step reveal"><span class="tag">With membership</span><h3>Contribute</h3><p>Help others with thoughtful analysis and explanations as your experience grows.</p></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Start here — free</span><h2>Gold trading guides that explain the why.</h2>
      <p>Each guide covers what a framework claims, how traders apply it to XAUUSD, where it breaks down, and how to manage risk around it.</p></div>
    <div class="cards cards--3">{strat_cards}</div>
    <div class="mt-3"><a class="btn btn--ghost" href="/xauusd-trading-strategies/">Browse all 18 strategy topics {ARROW_BTN}</a></div>
    <div class="mt-3">{tool_band()}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Gold trading education</span><h2>Learn by category.</h2></div>
    <div class="cards cards--3">
      {card("/strategies/market-structure-xauusd/", "Market structure", "Trends, swings, Break of Structure and Change of Character — the backbone of most discretionary gold analysis.", ico="chart")}
      {card("/strategies/smart-money-concepts-xauusd/", "Liquidity frameworks (SMC & ICT)", "Liquidity pools, sweeps, order blocks and fair value gaps — treated as interpretive models, not certainties.", ico="layers")}
      {card("/strategies/london-session-gold-trading/", "Sessions & timing", "How London, New York and Asian hours change gold's volatility and behaviour.", ico="clock")}
      {card("/strategies/xauusd-risk-management/", "Risk management", "Position sizing for gold's contract size, stop placement and surviving volatility.", ico="shield")}
      {card("/blog/how-to-keep-a-trading-journal/", "Journaling & review", "Turn every trade into data you can learn from, and review setups systematically.", ico="journal")}
      {card("/blog/what-moves-gold-prices/", "Macro drivers", "The US dollar, real yields, inflation and the Fed — why they matter to XAUUSD.", ico="globe")}
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">XAUUSD price preview</span>
        <h2>Watch gold with context, not just a number.</h2>
        <p class="lead">A price on its own tells you very little. On the <a href="/xauusd-price/">XAUUSD price page</a> you'll find a full interactive chart, the current trading session, and the macro factors that tend to move gold.</p>
        {sessions_html()}
      </div>
      <div class="reveal">
        {tv_box("mini-symbol-overview", mini_cfg, "tv-box--mini", "XAUUSD price preview")}
        <p class="data-credit">{DATA_CREDIT}</p>
        <a class="btn btn--ghost mt-2" href="/xauusd-price/">Open the full XAUUSD chart {ARROW_BTN}</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Latest gold-market news</span><h2>News that moves gold — with the context to read it.</h2>
      <p>Hourly headlines on gold, the Fed, inflation and the dollar, plus an economic calendar on our news hub.</p></div>
    <div data-news-feed="{C.BASE_PATH}/assets/data/news.json" data-news-limit="3">
      <div class="news-empty">
        {L.notice("<strong>Live headlines refresh every hour.</strong> Until the first update arrives, here's what typically moves gold and why.", "info", "news")}
        <div class="cards cards--3 mt-2">
          {card("/xauusd-news/#fed", "Federal Reserve decisions", "Rate decisions and guidance shift real yields and the dollar — two of gold's key drivers.", tag="Explainer")}
          {card("/xauusd-news/#inflation", "Inflation data", "CPI and PCE releases change rate expectations, often producing sharp intraday gold moves.", tag="Explainer")}
          {card("/xauusd-news/#central-banks", "Central-bank gold demand", "Official-sector buying and selling is a slower-moving but important structural factor.", tag="Explainer")}
        </div>
      </div>
      <div class="cards cards--3 news-feed" hidden></div>
    </div>
    <div class="mt-3"><a class="btn btn--ghost" href="/xauusd-news/">All headlines &amp; the economic calendar {ARROW_BTN}</a></div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">From the blog</span><h2>Latest articles</h2></div>
    <div class="cards cards--3">{blog_cards}</div>
    <div class="mt-3"><a class="btn btn--ghost" href="/blog/">Read the gold trading blog {ARROW_BTN}</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Who it's for</span><h2>Built for traders who want to keep improving.</h2>
      <p>Most members will be intermediate traders. Everyone is welcome to ask questions without feeling foolish — trading is hard, and struggling is part of learning it. Levels are planned discussion categories, earned through contribution, never bought.</p></div>
    <div class="cards cards--4">
      <article class="card reveal"><div class="card__icon">{icon("compass")}</div><h3>Intermediate</h3><p>You know candlesticks and several strategies, but struggle with context and consistency. You want answers to your own questions, not more videos.</p></article>
      <article class="card reveal"><div class="card__icon">{icon("layers")}</div><h3>Advanced</h3><p>You have a method. You want to stress-test it, compare trade plans, and refine your read of structure and liquidity.</p></article>
      <article class="card reveal"><div class="card__icon">{icon("target")}</div><h3>Pro</h3><p>You can explain your process clearly and enjoy breaking down theses, reviewing trades and helping others improve.</p></article>
      <article class="card reveal"><div class="card__icon">{icon("bolt")}</div><h3>Degen</h3><p>Experimental and high-conviction — but accountable. Alternative theses, transparent reasoning and strict risk controls.</p></article>
    </div>
    <p class="mt-2"><a href="/membership/">See how the planned trader levels work</a></p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Free and paid</span>
        <h2>The guides stay free. The community is the membership.</h2>
        <p>Everything educational on this website is free and will stay that way. Membership is planned for the part that can't be put in an article: discussing your own charts, getting feedback on your reasoning, and reviewing trades with other traders.</p>
        <p class="muted">We'll only advertise community features once they exist or are firmly planned, and we'll label which is which.</p>
        <a href="/membership/">What membership is planned to include</a>
      </div>
      <div class="reveal">
        <div class="tier tier--pro" style="padding:34px">
          <span class="tier__lvl">Membership preview</span>
          <div class="price-big" style="margin:14px 0 6px">{C.PLANNED_PRICE}<small> /month · planned</small></div>
          <p class="muted">One planned price. Levels inside the community are earned through analysis quality and contribution — not by paying more.</p>
          <ul class="status-list" style="margin-top:18px">
            <li><span class="badge badge--live">Live</span>Free guides, news and calendar</li>
            <li><span class="badge badge--live">Open</span>Launch-updates waitlist</li>
            <li><span class="badge badge--soon">Soon</span>Community registration</li>
            <li><span class="badge badge--no">Not yet</span>Payments &amp; member access</li>
          </ul>
          <div class="btn-row mt-2"><a class="btn btn--gold" href="/membership/#registration">Get Launch Updates {ARROW_BTN}</a></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--text">
    <div class="section-head reveal"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>
    {L.faq_html(faqs)}
    <p class="mt-2"><a href="/faq/">Read all frequently asked questions</a></p>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    {L.community_cta()}
    <div class="mt-2">{L.notice("<strong>Risk warning.</strong> Leveraged trading and CFDs can result in substantial losses. Content on XAUUSD Global is educational and not personalised financial advice. No strategy or community participation guarantees results.", "risk", "alert")}</div>
  </div>
</section>"""
    return L.page(path="/", title="XAUUSD Global — Learn to Understand Gold, Not Chase Signals",
                  description="A gold trading learning community built on market reasoning, honest discussion and trade reviews. Free XAUUSD guides now; membership launching soon.",
                  body=body)


# --------------------------------------------------------------------------

def price_page():
    crumbs = [("/", "Home"), ("/xauusd-price/", "XAUUSD Price")]
    info_cfg = {"symbol": C.TV_SYMBOL, "width": "100%", "locale": "en", "colorTheme": "dark", "isTransparent": True}
    chart_cfg = {"autosize": True, "symbol": C.TV_SYMBOL, "interval": "60", "timezone": "Etc/UTC", "theme": "dark",
                 "style": "1", "locale": "en", "backgroundColor": "rgba(18, 21, 26, 1)", "gridColor": "rgba(255, 255, 255, 0.04)",
                 "hide_side_toolbar": True, "allow_symbol_change": False, "save_image": False, "calendar": False,
                 "support_host": "https://www.tradingview.com"}
    faqs = [
        {"q": "Is the gold price on this page live?", "a": "The price and chart come from an embedded TradingView widget. Depending on the provider, quotes may be real-time or delayed and are indicative only. XAUUSD Global does not generate these prices. Always confirm prices with your own broker before making any decision."},
        {"q": "Why does my broker show a different XAUUSD price?", "a": "Spot gold trades over the counter, so there is no single official price. Each broker and liquidity provider quotes its own bid and ask, and spreads widen around news and during quieter hours."},
        {"q": "What is the difference between XAUUSD and gold futures?", "a": "XAUUSD is the spot (or spot-referenced CFD) price of one troy ounce of gold in US dollars. Gold futures, such as those listed on COMEX, are exchange-traded contracts for future delivery and include a premium or discount related to interest rates and storage."},
        {"q": "When is gold most volatile?", "a": "Activity typically increases at the London open and during the London–New York overlap, and especially around scheduled US data such as inflation and employment reports and Federal Reserve decisions. Read our guides to [London-session](/strategies/london-session-gold-trading/) and [New York-session](/strategies/new-york-session-gold-trading/) gold trading."},
    ]
    factors = [
        ("scale", "US dollar", "Gold is priced in dollars. A stronger dollar often (not always) weighs on XAUUSD, and a weaker dollar can support it."),
        ("chart", "Real yields", "Gold pays no interest. When inflation-adjusted Treasury yields rise, the opportunity cost of holding gold rises too."),
        ("bolt", "Federal Reserve policy", "Rate decisions, projections and speeches reshape expectations for yields and the dollar."),
        ("layers", "Inflation & data", "CPI, PCE, payrolls and growth data change rate expectations and can trigger sharp intraday moves."),
        ("globe", "Geopolitics & risk sentiment", "Conflicts, crises and market stress can increase demand for gold as a perceived safe haven."),
        ("shield", "Central banks & physical demand", "Official-sector buying, ETF flows and jewellery and bar demand shape the longer-term backdrop."),
    ]
    fcards = "".join(f'<article class="card reveal"><div class="card__icon">{icon(i)}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in factors)
    body = f"""{L.page_head(crumbs, 'XAUUSD Price Today: <span class="gold-text">Live Gold Chart</span> &amp; Market Overview', 'Follow the gold price against the US dollar on an interactive chart, check which trading session is active, and understand the forces that move XAUUSD.', eyebrow='Gold price · XAU/USD')}
<section class="section--tight section">
  <div class="wrap">
    <div class="price-panel">
      <div>
        {tv_box("advanced-chart", chart_cfg, "tv-box--chart", "interactive XAUUSD chart")}
      </div>
      <div>
        {tv_box("symbol-info", info_cfg, "tv-box--info", "XAUUSD price and daily change")}
        <h2 class="mt-2" style="font-size:1.25rem">Market sessions</h2>
        {sessions_html()}
      </div>
    </div>
    <p class="data-credit">{DATA_CREDIT} Use the chart's own controls to change timeframe. Bid/ask quotes are not shown because the free widget does not supply them.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wrap--text prose">
    <h2 class="mt-0">What XAUUSD means</h2>
    <p><strong>XAUUSD</strong> is the market symbol for the price of one troy ounce of gold quoted in US dollars. “XAU” is the ISO 4217 code for gold — X marks a non-national “currency”, AU comes from <em>aurum</em>, Latin for gold — and “USD” is the US dollar. If XAUUSD is quoted at 3,500.00, one ounce costs 3,500 dollars.</p>
    <p>Retail traders usually access XAUUSD through spot gold or gold CFDs offered by brokers. These are typically leveraged, which magnifies both gains and losses. On many platforms one standard lot is 100 troy ounces, so a $1 move in price changes the value of one lot by about $100 — but contract specifications vary, so always check yours. Our <a href="/strategies/xauusd-risk-management/">XAUUSD risk management guide</a> walks through position sizing in detail.</p>
    <h3>How to read a gold quote</h3>
    <ul>
      <li><strong>Bid</strong> — the price at which you can sell. <strong>Ask</strong> — the price at which you can buy. The gap between them is the <strong>spread</strong>, a cost you pay on every trade.</li>
      <li><strong>Daily change</strong> — usually measured from the previous session's close, which differs by provider.</li>
      <li><strong>Points and pips</strong> — terminology varies by broker. Talk in dollars per ounce to avoid confusion.</li>
    </ul>
    <h3>Trading sessions and gold</h3>
    <p>Spot gold trades around the clock on weekdays, but liquidity is uneven. The Asian session is often quieter and range-bound; the London open tends to bring expansion; and the London–New York overlap, together with US data releases, usually brings the largest moves. Read more on <a href="/blog/london-vs-new-york-sessions/">London vs. New York sessions for gold traders</a>.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Market drivers</span><h2>Factors that influence gold prices</h2>
      <p>No single factor explains gold at all times. Relationships shift, and several drivers can pull in opposite directions at once. For a deeper explanation, read <a href="/blog/what-moves-gold-prices/">what moves gold prices</a>.</p></div>
    <div class="cards cards--3">{fcards}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Go from price to process</span><h2>Turn the chart into analysis</h2></div>
    <div class="cards cards--3">
      {card("/strategies/support-and-resistance-xauusd/", "Support and resistance on XAUUSD", "How to mark meaningful gold levels and avoid drawing a line at every wick.", tag="Strategy")}
      {card("/strategies/market-structure-xauusd/", "Gold market structure", "Read trends with swing highs, swing lows, BOS and CHoCH.", tag="Strategy")}
      {card("/xauusd-news/", "XAUUSD news hub", "Understand the events that typically move gold and how traders prepare for them.", tag="News")}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--text">
    <h2>XAUUSD price FAQ</h2>
    {L.faq_html(faqs)}
  </div>
</section>
<section class="section--tight section"><div class="wrap">{tool_band()}<div class="mt-3">{L.community_cta()}</div></div></section>"""
    return L.page(path="/xauusd-price/", title="XAUUSD Price Today — Live Gold Price Chart | XAUUSD Global",
                  description="Check the XAUUSD price on a live gold chart with timeframe controls, active trading sessions, and a clear guide to what moves the gold price today.",
                  body=body, crumbs=crumbs)


# --------------------------------------------------------------------------

NEWS_CATS = [
    ("fed", "Federal Reserve", "bolt", "Interest-rate decisions, the statement, the dot plot and press-conference tone change expectations for the path of US rates. Because gold pays no yield, a more hawkish outlook (higher rates for longer) often pressures gold through higher real yields and a firmer dollar, while a dovish shift can support it. The surprise relative to expectations matters more than the decision itself.", "/blog/what-moves-gold-prices/", "What moves gold prices"),
    ("inflation", "Inflation", "chart", "CPI, PCE and producer-price data influence how restrictive the Fed is expected to be. Gold is often described as an inflation hedge, but in the short term a hot inflation print can push gold lower if it raises rate expectations. Traders watch the reaction in yields and the dollar alongside gold.", "/strategies/new-york-session-gold-trading/", "New York-session gold trading"),
    ("dollar", "US dollar", "scale", "Because XAUUSD is priced in dollars, broad dollar strength tends to make gold more expensive for non-dollar buyers and is often associated with weaker gold prices — though the relationship is not constant, and both can rise together during stress.", "/blog/what-is-xauusd/", "What is XAUUSD?"),
    ("yields", "Treasury yields", "layers", "Real (inflation-adjusted) yields represent the return foregone by holding gold. Rising real yields have historically been a headwind for gold and falling real yields a tailwind, although that link has weakened or broken during some periods, including when central-bank buying was strong.", "/blog/what-moves-gold-prices/", "Gold, yields and the Fed"),
    ("geopolitics", "Geopolitics", "globe", "Wars, sanctions, elections and financial crises can increase demand for gold as a perceived safe haven. These moves are hard to predict, can reverse quickly when tensions ease, and are a reason to respect weekend gap risk.", "/strategies/xauusd-risk-management/", "Risk management for gold"),
    ("central-banks", "Central banks", "shield", "Central banks are significant holders of gold. Reported purchases and sales — published with a lag by official sources and industry bodies — shape the long-term demand picture rather than intraday price action.", "/blog/what-moves-gold-prices/", "Structural gold demand"),
    ("analysis", "Gold-market analysis", "compass", "Positioning reports, ETF flows and technical analysis pieces help traders understand sentiment and key levels. Treat any outlook as one perspective, check the date, and compare it with your own analysis.", "/xauusd-trading-strategies/", "The strategy hub"),
]


def news_page():
    crumbs = [("/", "Home"), ("/xauusd-news/", "XAUUSD News")]
    cats = "".join(
        f'<article class="card reveal" id="{i}"><div class="card__icon">{icon(ic)}</div><h3>{n}</h3><p>{d}</p>'
        f'<div class="card__meta"><a href="{p}">Related: {esc(t)}</a></div></article>'
        for i, n, ic, d, p, t in NEWS_CATS)
    feed_url = C.BASE_PATH + "/assets/data/news.json"
    cal_cfg = {"colorTheme": "dark", "isTransparent": True, "width": "100%", "height": "100%", "locale": "en",
               "importanceFilter": "0,1", "countryFilter": "us,eu,gb,jp,cn,ch,ca,au"}
    body = f"""{L.page_head(crumbs, 'XAUUSD News &amp; <span class="gold-text">Economic Calendar</span>', 'An economic calendar, hourly gold-market headlines, and clear explanations of the events that drive XAUUSD — so you know what is scheduled, what is happening, and why it matters.', eyebrow='Gold market news')}
<section class="section section--tight" id="calendar">
  <div class="wrap">
    <div class="section-head" style="margin-bottom:24px"><span class="eyebrow">Economic calendar</span><h2>This week's market-moving events</h2>
      <p>Scheduled releases and central-bank events with forecast, previous and actual figures. High-impact US data — inflation, jobs and Federal Reserve decisions — tends to matter most for gold. Times are shown in your local time zone.</p></div>
    {tv_box("events", cal_cfg, "tv-box--calendar", "economic calendar")}
    <p class="data-credit">Economic calendar provided by an embedded <a href="https://www.tradingview.com/economic-calendar/" rel="noopener nofollow" target="_blank">TradingView</a> widget. Event times, forecasts and results come from the provider and may change; XAUUSD Global does not produce or verify them.</p>
  </div>
</section>
<section class="section section--alt" id="headlines">
  <div class="wrap" data-news-feed="{feed_url}" data-news-limit="24">
    <div class="section-head" style="margin-bottom:24px"><span class="eyebrow">Latest headlines</span><h2>Gold-market news</h2>
      <p>Headlines collected automatically every hour from public RSS feeds and filtered for gold, the Federal Reserve, inflation, the US dollar and yields. Each card links to the original publisher — read the full story at the source.</p>
      <p class="data-credit" data-news-updated hidden></p></div>
    <div class="news-empty">{L.notice("<strong>Headlines are on their way.</strong> The news feed refreshes automatically every hour. If nothing appears here yet, the first update hasn't run or the sources are temporarily unavailable. XAUUSD Global never invents headlines, dates or quotes.", "info", "news")}</div>
    <div class="cards cards--3 news-feed" hidden></div>
    <p class="muted mt-2" style="font-size:.85rem">Headlines, excerpts and trademarks belong to their respective publishers. Inclusion of a headline is not an endorsement of its content and is not financial advice.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Evergreen explainers</span><h2>News categories and why they affect gold</h2>
      <p>Knowing <em>why</em> a type of event matters helps you decide whether to trade, wait, or reduce size around it.</p></div>
    <div class="news-cats">{cats}</div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap wrap--text prose">
    <h2 class="mt-0">How to read gold news as a trader</h2>
    <ol>
      <li><strong>Separate the event from the reaction.</strong> Markets move on surprises relative to expectations. A “strong” number that was fully expected may barely move gold.</li>
      <li><strong>Watch the transmission channels.</strong> After a release, check the dollar and Treasury yields. If gold moves without them, the driver may be positioning or liquidity rather than the data.</li>
      <li><strong>Expect noise first.</strong> The first minutes after major US data often include whipsaws and wide spreads. Many traders wait for a structure to form instead of reacting to the first candle.</li>
      <li><strong>Check the date and source.</strong> Old news resurfacing on social media is a common trap. Prefer primary sources such as central-bank statements and official statistics.</li>
      <li><strong>Plan risk before the event.</strong> Decide in advance whether you will be flat, reduce size, or widen stops — never improvise at release time.</li>
    </ol>
    <p>Our guide to <a href="/strategies/new-york-session-gold-trading/">trading gold during the New York session</a> covers high-impact US releases in depth, and <a href="/blog/risk-management-volatile-gold-markets/">risk management for volatile gold markets</a> explains how to size positions when volatility jumps.</p>
    <div class="related"><h2>Related education</h2><ul>
      <li><a href="/blog/what-moves-gold-prices/">What moves gold prices? The dollar, yields, inflation and the Fed</a></li>
      <li><a href="/xauusd-price/">XAUUSD price chart and market sessions</a></li>
      <li><a href="/blog/how-to-build-a-xauusd-trading-plan/">How to build a trading plan for XAUUSD</a></li>
    </ul></div>
  </div>
</section>
<section class="section--tight section"><div class="wrap">{tool_band()}<div class="mt-3">{L.community_cta()}</div></div></section>"""
    return L.page(path="/xauusd-news/", title="XAUUSD News & Economic Calendar — Gold Market Headlines",
                  description="Gold market news for XAUUSD traders: economic calendar, hourly gold headlines, and how the Fed, inflation, the dollar and yields move the gold price.",
                  body=body, crumbs=crumbs)


# --------------------------------------------------------------------------

def strategy_hub(strategies):
    crumbs = [("/", "Home"), ("/xauusd-trading-strategies/", "Trading Strategies")]
    hub = yaml.safe_load(open(os.path.join(CONTENT, "hub.yaml"), encoding="utf-8"))
    index_html, sections = [], []
    n = 0
    for group in hub["groups"]:
        index_html.append(f'<h3 class="mt-2">{esc(group["name"])}</h3><div class="cards cards--3">')
        sec = [f'<h2 id="{group["id"]}">{esc(group["name"])}</h2><p>{esc(group["intro"])}</p>']
        for t in group["topics"]:
            n += 1
            num = f"{n:02d}"
            index_html.append(
                f'<article class="card card--link"><div class="card__num">{num}</div><h3><a href="#{t["id"]}">{esc(t["name"])}</a></h3><p>{esc(t["summary"])}</p></article>')
            guide = "".join(f'<li><a href="{p}">{esc(lbl)}</a></li>' for p, lbl in t["links"])
            sec.append(f"""<section aria-labelledby="{t['id']}">
<h3 id="{t['id']}"><span class="mono" style="color:var(--gold);font-size:.8em">{num}</span> {esc(t['name'])}</h3>
<p><strong>What it is.</strong> {esc(t['what'])}</p>
<p><strong>How traders interpret it.</strong> {esc(t['interpret'])}</p>
<p><strong>Applying it to XAUUSD.</strong> {esc(t['xau'])}</p>
<p><strong>Limitations.</strong> {esc(t['limits'])}</p>
<p><strong>Common mistakes.</strong> {esc(t['mistakes'])}</p>
<div class="callout"><p><strong>Read next:</strong></p><ul>{guide}</ul></div>
</section>""")
        index_html.append("</div>")
        sections.append("".join(sec))
    guides = "".join(card(s["path"], s["title"], s["card"], tag=s.get("level", "Guide"),
                          meta=f"<span>{s.get('minutes', '')} min read</span>") for s in strategies)
    body = f"""{L.page_head(crumbs, 'XAUUSD Trading Strategies: <span class="gold-text">How Traders Analyse Gold</span>', 'Eighteen ways traders read the gold market — from support and resistance to Smart Money Concepts, ICT, session timing and risk management. Each topic explains the idea, how it is applied to XAUUSD, where it fails, and the mistakes to avoid.', eyebrow='Strategy hub')}
<section class="section section--tight">
  <div class="wrap">
    {L.notice("<strong>How to use this hub.</strong> These are analytical frameworks, not trading systems with guaranteed outcomes. SMC and ICT in particular are interpretations of price behaviour; they do not reveal what banks or institutions are actually doing. Combine any method with strict risk management and test it before risking money.", "info", "info")}
    <h2 class="mt-3">In-depth XAUUSD strategy guides</h2>
    <div class="cards cards--3">{guides}</div>
    <h2 class="mt-3">All 18 strategy topics</h2>
    {"".join(index_html)}
  </div>
</section>
<section class="section section--alt">
  <div class="wrap wrap--text prose">{"".join(sections)}</div>
</section>
<section class="section"><div class="wrap">{tool_band()}<div class="mt-3">{L.community_cta()}</div></div></section>"""
    item_list = {"@type": "ItemList", "name": "XAUUSD strategy guides", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": L.canonical(s["path"]), "name": s["title"]} for i, s in enumerate(strategies)]}
    return L.page(path="/xauusd-trading-strategies/", title="XAUUSD Trading Strategies — 18 Gold Trading Methods Explained",
                  description="Gold trading strategies for XAUUSD explained: support and resistance, price action, SMC, ICT, liquidity sweeps, order blocks, FVGs, sessions and risk management.",
                  body=body, crumbs=crumbs, schema_extra=[item_list])


# --------------------------------------------------------------------------

def blog_index(posts):
    crumbs = [("/", "Home"), ("/blog/", "Blog")]
    cats = []
    for p in posts:
        if p["category"] not in cats:
            cats.append(p["category"])
    feat = next((p for p in posts if p.get("featured")), posts[0])
    others = sorted([p for p in posts if p is not feat], key=lambda p: p.get("order", 99))
    slug = lambda c: c.lower().replace(" ", "-").replace("&", "and")
    chips = '<button type="button" class="chip" data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" class="chip" data-filter="{slug(c)}" aria-pressed="false">{esc(c)}</button>' for c in cats)
    cards = "".join(
        f'<article class="card card--link post-card" data-cat="{slug(p["category"])}"><span class="tag">{esc(p["category"])}</span>'
        f'<h3><a href="{p["path"]}">{esc(p["title"])}</a></h3><p>{esc(p["card"])}</p>'
        f'<div class="card__meta"><time datetime="{p["published"]}">{L.fmt_date(p["published"])}</time><span>{p["minutes"]} min read</span></div></article>'
        for p in others)
    body = f"""{L.page_head(crumbs, 'The Gold Trading Blog for <span class="gold-text">XAUUSD Traders</span>', 'Original, practical articles on trading gold: market drivers, technical analysis, trading plans, risk management, journaling and the mistakes that hold intermediate traders back.', eyebrow='Blog')}
<section class="section section--tight">
  <div class="wrap" data-blog data-page-size="6">
    <div class="feature-post">
      <div><span class="tag">Featured · {esc(feat["category"])}</span>
        <h2><a href="{feat["path"]}">{esc(feat["title"])}</a></h2>
        <p>{esc(feat["card"])}</p>
        <div class="card__meta"><time datetime="{feat["published"]}">{L.fmt_date(feat["published"])}</time><span>{feat["minutes"]} min read</span></div>
      </div>
      <div><a class="btn btn--gold" href="{feat["path"]}">Read the featured guide {ARROW_BTN}</a></div>
    </div>
    <div class="filters" role="search">
      <label class="sr-only" for="blog-q">Search articles</label>
      <input id="blog-q" type="search" placeholder="Search articles…" autocomplete="off">
      <div class="btn-row" role="group" aria-label="Filter by category">{chips}</div>
    </div>
    <div class="cards cards--3">{cards}</div>
    <p class="empty-state" hidden>No articles match that search yet.</p>
    <div class="load-more-wrap" hidden><button type="button" class="btn btn--ghost" data-load-more>Load more articles</button></div>
  </div>
</section>
<section class="section section--alt"><div class="wrap">
  <div class="section-head"><h2>Looking for structured strategy guides?</h2><p>The <a href="/xauusd-trading-strategies/">XAUUSD strategy hub</a> covers 18 analytical methods in depth, with diagrams, examples and common mistakes.</p></div>
  {L.community_cta()}
</div></section>"""
    blog_schema = {"@type": "Blog", "name": "XAUUSD Global Blog", "url": L.canonical("/blog/"), "publisher": {"@id": L.ORG_ID},
                   "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": L.canonical(p["path"]), "datePublished": p["published"]} for p in posts]}
    return L.page(path="/blog/", title="Gold Trading Blog — XAUUSD Analysis & Education | XAUUSD Global",
                  description="Original gold trading blog for XAUUSD traders: what moves gold, support and resistance, SMC and ICT concepts, trading plans, risk management and journaling.",
                  body=body, crumbs=crumbs, schema_extra=[blog_schema])


# --------------------------------------------------------------------------

def community_page():
    crumbs = [("/", "Home"), ("/community/", "Community")]
    benefits = [
        ("users", "Learn alongside other traders", "Intermediate, advanced and experienced traders, all focused on the same market."),
        ("compass", "Compare perspectives", "See how traders using different frameworks read the same price action — and where they disagree."),
        ("journal", "See how plans are built", "Learn how other traders develop, document and review their trade plans."),
        ("message", "Share breakdowns & reviews", "Post chart breakdowns and post-trade reviews for structured feedback."),
        ("shield", "Improve risk habits", "Make position sizing, invalidation and drawdown rules part of every discussion."),
        ("repeat", "Learn from mistakes", "Losses and errors are reviewed openly, not hidden behind highlight reels."),
        ("layers", "Build a structured process", "Turn scattered ideas into a repeatable process you can measure and refine."),
        ("news", "Reasons to keep returning", "Ongoing market discussions, review threads, learning milestones and community challenges are among the ideas we're planning — learning shouldn't end after one course."),
        ("globe", "Global relationships", "Build lasting trading relationships with people across time zones and sessions."),
    ]
    bcards = "".join(f'<article class="card reveal"><div class="card__icon">{icon(i)}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in benefits)
    faqs = [
        {"q": "When will the community open?", "a": "We haven't announced a date. It will open once the platform, community standards and membership terms are ready. [Get launch updates](/membership/#registration) to hear first."},
        {"q": "I'm not an experienced trader. Is it for me?", "a": "Yes, if you're serious about learning. Most members are expected to be intermediate traders. Thoughtful questions are welcome at every level, and nobody should feel foolish for asking."},
        {"q": "Can I disagree with more experienced traders?", "a": "Yes — respectfully, and with your reasoning. Comparing interpretations is one of the main ways people learn here. Challenge the analysis, never the person."},
        {"q": "Will experienced traders give me trades to copy?", "a": "No. The community is for sharing reasoning and reviews, not for copying entries. Members remain responsible for their own decisions."},
        {"q": "Where will discussions take place?", "a": "The platform is still being chosen. We'll publish details — including how data is handled — before registration opens."},
        {"q": "Does membership guarantee better results?", "a": "No. Membership does not guarantee profitable trading. Leveraged gold trading can result in substantial losses."},
    ]
    framework = [
        ("Context", "What is the higher-timeframe picture, the session and the calendar?"),
        ("Thesis", "What do you expect, and why?"),
        ("Evidence", "What on the chart or in the data supports it?"),
        ("Invalidation", "What would prove the idea wrong?"),
        ("Risk", "How much is at stake, and how is the position sized?"),
        ("Alternatives", "How else could this chart be read?"),
        ("Lessons", "Afterwards: what happened, and what would you change?"),
    ]
    fcards = "".join(f'<article class="card reveal"><div class="card__num">{n:02d}</div><h3>{t}</h3><p>{d}</p></article>' for n, (t, d) in enumerate(framework, 1))
    body = f"""{L.page_head(crumbs, 'Bring your charts. Bring your questions. <span class="gold-text">Bring your reasoning.</span>', 'XAUUSD Global is a learning community for gold traders, built around market reasoning, honest discussion, transparent trade reviews and continuous improvement. Leave room to learn.', eyebrow='The community', extra='<div class="hero__status"><span class="status-pill"><span class="dot dot--gold"></span>In development · Launch-updates waitlist open</span></div>')}
<section class="section section--tight">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">A look inside</span><h2>What a conversation will look like</h2>
      <p>One member shares a chart with their reasoning. Others test it from different angles — structure, liquidity, risk. Afterwards, the trade is reviewed honestly, win or lose.</p></div>
    {chat_mockup()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Why it exists</span>
        <h2>Stop learning alone. Start learning together.</h2>
        <p class="lead">Many traders improve slowly because they learn in isolation: the same mistakes repeat, blind spots stay hidden, and advice arrives in scattered fragments.</p>
        <p>XAUUSD Global is being built so a trader can put their analysis next to someone else's, ask why, and get a thoughtful answer — then review what actually happened.</p>
        <p>We want members to feel welcome to ask a question, disagree respectfully, admit a mistake and learn from someone with more experience.</p>
      </div>
      <div class="reveal">
        <div class="compare">
          <div class="compare__col compare__col--bad"><h3>Copying an entry</h3><ul><li>Works until it doesn't</li><li>You can't tell a good loss from a bad one</li><li>Little you can reuse next time</li></ul></div>
          <div class="compare__col compare__col--good"><h3>Understanding the reasoning</h3><ul><li>You learn the context and the invalidation</li><li>You can judge decision quality</li><li>Skills build over time</li></ul></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Planned discussion format</span><h2>Every idea answers seven questions</h2>
      <p>When a trade idea is shared, it's expected to cover these points — ideally before the outcome is known. It turns a chart screenshot into something others can learn from and challenge.</p></div>
    <div class="cards cards--4">{fcards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">One chart, several perspectives</span><h2>No single trader has every answer</h2>
      <p>Here's how one gold chart might be read by different traders. This is an illustration of the idea, not a real member discussion.</p></div>
    <div class="cards cards--4">
      <article class="card reveal"><span class="tag">Structure</span><h3 style="margin-top:12px">"Higher highs on H4."</h3><p>Sees a bullish trend and wants to buy a pullback into the last higher low.</p></article>
      <article class="card reveal"><span class="tag">Liquidity</span><h3 style="margin-top:12px">"Equal highs above."</h3><p>Points out resting buy stops just above price — a sweep could come before any continuation.</p></article>
      <article class="card reveal"><span class="tag">Risk</span><h3 style="margin-top:12px">"CPI is in two hours."</h3><p>Asks whether the stop survives a news spike, and whether the position should be smaller.</p></article>
      <article class="card reveal"><span class="tag">Challenger</span><h3 style="margin-top:12px">"What proves you wrong?"</h3><p>Asks for the exact level where the bullish idea is invalid — and whether that's acceptable risk.</p></article>
    </div>
    <p class="muted text-center mt-2">Together, the idea is clearer than any one view. You compare, ask questions — and form your own conclusion.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">How discussions will work</span><h2>Better conversations, not a noisier feed</h2></div>
    <div class="steps">
      <div class="step reveal"><h3>Chart breakdowns</h3><p>Members post an XAUUSD chart with their read of structure, key levels and context.</p></div>
      <div class="step reveal"><h3>Feedback</h3><p>Other traders test the reasoning, point out missed context and offer alternative reads.</p></div>
      <div class="step reveal"><h3>Trade reviews</h3><p>After the trade, the decision, execution and emotions are reviewed — win or loss.</p></div>
      <div class="step reveal"><h3>Level-based rooms</h3><p>Discussion categories for Starter, Advanced, Pro and Degen keep conversations useful at every level.</p></div>
    </div>
    <div class="mt-3">{L.notice("<strong>A winning screenshot doesn't tell the whole story.</strong> Status in the community is planned to reflect thoughtful analysis, transparency and responsible participation — not confidence, popularity, payment or one profitable trade.", "info", "info")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Planned membership benefits</span><h2>What the community aims to provide</h2>
      <p>These are the benefits we are designing for; none is live yet. Exact features will be confirmed and labelled before launch.</p></div>
    <div class="cards cards--3">{bcards}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Planned community standards</span>
        <h2>Principles we intend to hold members to</h2>
        <ul class="checklist">
          <li><strong>Explain the reasoning.</strong> Ideas without a thesis and invalidation don't belong in analysis threads.</li>
          <li><strong>Disclose risk.</strong> Talk about position size and risk in percentages, not just targets.</li>
          <li><strong>No paid signals or promotions.</strong> No selling signals, accounts or schemes to other members.</li>
          <li><strong>Review losses honestly.</strong> Mistakes are learning material, not something to hide.</li>
          <li><strong>Respect other perspectives.</strong> Challenge the analysis, never the person.</li>
          <li><strong>No guarantees.</strong> Nobody claims certainty about where gold goes next.</li>
        </ul>
      </div>
      <div class="reveal">
        {L.notice("<strong>Membership does not guarantee profitable trading.</strong> The community is designed to improve analysis, discipline and review habits. It does not provide personalised financial advice, signals to follow, or any assurance of returns. Leveraged trading can result in substantial losses.", "risk", "alert")}
        <div class="mt-2">{L.notice("<strong>Membership isn't open yet.</strong> Get launch updates and we'll email you when it opens. No payment, no obligation, unsubscribe anytime.", "", "lock")}</div>
        <div class="btn-row mt-2"><a class="btn btn--gold" href="/membership/#registration">Get Launch Updates {ARROW_BTN}</a><a class="btn btn--ghost" href="/membership/">See membership details</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Start now, for free</span><h2>Build the foundations before the community opens</h2></div>
    <div class="cards cards--3">
      {card("/strategies/market-structure-xauusd/", "Market structure for XAUUSD", "The shared language most community discussions will use.", tag="Guide")}
      {card("/blog/how-to-keep-a-trading-journal/", "How to keep a trading journal", "Start building the review habit that structured feedback depends on.", tag="Blog")}
      {card("/blog/common-mistakes-intermediate-gold-traders/", "Common mistakes intermediate gold traders make", "The patterns that hold traders back — and how to break them.", tag="Blog")}
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wrap--text"><h2>Community FAQ</h2>{L.faq_html(faqs)}</div>
</section>"""
    return L.page(path="/community/", title="XAUUSD Trading Community — Learn Gold Trading Together",
                  description="A gold trading community built on reasoning, not signals: share chart analysis, get feedback, review wins and losses, and build your own judgement.",
                  body=body, crumbs=crumbs)


# --------------------------------------------------------------------------

def membership_page():
    crumbs = [("/", "Home"), ("/membership/", "Membership")]
    tiers = [
        ("starter", "Level 1", "Starter", "For traders building a solid base in XAUUSD and the community's way of working.",
         ["Learn the community framework.", "Strengthen core XAUUSD knowledge.", "Participate in foundational discussions.", "Learn risk-management basics."]),
        ("advanced", "Level 2", "Advanced", "For traders with a method who want deeper analysis and structured comparison.",
         ["Participate in deeper chart-analysis discussions.", "Compare structured trade plans.", "Explore market structure, liquidity, and confluence.", "Review trading journals and execution decisions."]),
        ("pro", "Level 3", "Pro", "For traders who can explain a full process and help others improve.",
         ["Participate in advanced analytical discussions.", "Share detailed trade theses and post-trade reviews.", "Contribute thoughtful feedback and educational insights.", "Help other members improve their analysis."]),
        ("degen", "Level 4", "Degen", "A high-level category for experienced, experimental and unconventional perspectives.",
         ["Explore complex market scenarios and alternative theses.", "Contribute rigorous trade breakdowns and critical analysis.", "Emphasise accountability and transparent reasoning.", "Disciplined risk controls are mandatory, not optional."]),
    ]
    tier_html = "".join(
        f'<article class="tier tier--{k} reveal"><span class="tier__lvl">{lvl}</span><h3>{n}</h3><p class="tier__who">{w}</p>'
        f'<ul>{"".join(f"<li>{esc(x)}</li>" for x in items)}</ul></article>' for k, lvl, n, w, items in tiers)
    faqs = [
        {"q": "Can I pay now or pre-register?", "a": "You can't pay yet — payment and member access are not available. You can [get launch updates](#registration) for free and be notified first when membership opens. Please don't send money to anyone claiming to sell XAUUSD Global memberships."},
        {"q": "What stays free if I never become a member?", "a": "All educational guides, the strategy hub, the blog, the live price page and the news and economic calendar stay free and open. Membership adds the community — discussion, feedback and trade reviews — not access to the guides."},
        {"q": "Does a higher level cost more?", "a": f"No. The plan is one membership at {C.PLANNED_PRICE} per month. Levels are discussion categories and participation privileges earned through contribution quality — they cannot be bought."},
        {"q": "How will I move between levels?", "a": "Advancement is planned to depend on demonstrated analytical quality, risk awareness, transparent reviews and meaningful contributions — not on payment or a single profitable trade. Exact criteria will be published before launch."},
        {"q": "Is the price final?", "a": f"{C.PLANNED_PRICE}/month is the currently planned price. It may change before launch, and the final price and terms will be shown clearly before anyone is asked to pay."},
        {"q": "Will members receive trading signals?", "a": "No. Membership is about discussion, analysis and review. It does not include signals to copy, managed accounts or personalised financial advice."},
    ]
    body = f"""{L.page_head(crumbs, 'Membership &amp; <span class="gold-text">Trader Levels</span>', 'The guides stay free. Membership is the community: a place to share your reasoning, get feedback and review your trades with other gold traders. One planned price, four discussion levels earned through contribution — never bought.', eyebrow='Planned membership')}
<section class="section">
  <div class="wrap">
    <div class="price-hero reveal">
      <span class="eyebrow">Membership planned</span>
      <div class="price-big">{C.PLANNED_PRICE}<small> /month</small></div>
      <p class="lead" style="max-width:640px;margin:16px auto 28px">Membership planned: {C.PLANNED_PRICE}/month. Registration opening soon. Payment and member access are not available yet — <a href="#registration">get launch updates</a> (free) to hear first when it opens.</p>
      <ul class="status-list" style="max-width:520px;margin:0 auto;text-align:left">
        <li><span class="badge badge--live">Live</span>Public educational website and guides</li>
        <li><span class="badge badge--live">Open</span>Launch-updates waitlist (free)</li>
        <li><span class="badge badge--soon">Soon</span>Community registration</li>
        <li><span class="badge badge--no">Not yet</span>Payment and member access</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Free and paid</span><h2>What's free, what membership adds</h2>
      <p>You don't need to pay to learn here. Membership is for traders who want to discuss, test and review their thinking with others.</p></div>
    <div class="cards cards--2">
      <article class="card reveal"><span class="tag tag--cyan">Free · available now</span><h3 style="margin-top:12px">Learn on your own</h3><ul class="checklist">
        <li>11 in-depth XAUUSD strategy guides and the strategy hub</li>
        <li>Blog articles on gold drivers, sessions, risk and psychology</li>
        <li>Live XAUUSD price chart and economic calendar</li>
        <li>Gold news headlines from public sources</li>
        <li>Launch updates by email</li></ul></article>
      <article class="card reveal"><span class="tag">Membership · planned</span><h3 style="margin-top:12px">Learn with other traders</h3><ul class="checklist">
        <li>Post chart breakdowns and trade plans for feedback</li>
        <li>Structured trade reviews — losses included</li>
        <li>Compare different readings of the same gold chart</li>
        <li>Level-based discussion rooms (Starter to Degen)</li>
        <li>A culture built on reasoning, risk discipline and respect</li></ul>
        <p class="muted" style="font-size:.9rem">None of these are live yet. Exact features will be confirmed before launch.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Trader levels</span><h2>Four planned discussion levels</h2>
      <p>These levels represent intended discussion categories and participation privileges. Access criteria and exact benefits will be finalised before launch.</p></div>
    <div class="tiers">{tier_html}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">How advancement is planned to work</span>
        <h2>Earned through quality, not payment</h2>
        <p>Moving between levels should reflect how well you think, not how much you pay or one lucky trade. We intend to look at:</p>
        <ul class="checklist">
          <li><strong>Analytical quality</strong> — clear theses with context, confluence and invalidation.</li>
          <li><strong>Risk awareness</strong> — consistent position sizing and respect for stops.</li>
          <li><strong>Transparent reviews</strong> — honest post-trade reviews, losses included.</li>
          <li><strong>Meaningful contributions</strong> — feedback that helps other members improve.</li>
        </ul>
      </div>
      <div class="reveal">
        <h2>What membership aims to provide</h2>
        <ul class="checklist">
          <li>Organised, level-aware XAUUSD discussion categories.</li>
          <li>A place to post chart breakdowns, trade plans and post-trade reviews for feedback.</li>
          <li>Exposure to multiple analytical frameworks applied to the same market.</li>
          <li>A culture built on reasoning, risk discipline and honest review.</li>
        </ul>
        <h3 class="mt-2">What membership will not include</h3>
        <ul class="checklist">
          <li>No trading signals or calls to copy.</li>
          <li>No promise of profits, returns or a win rate.</li>
          <li>No personalised financial advice or account management.</li>
          <li>No guaranteed access to "profitable traders".</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section" id="registration">
  <div class="wrap">
    <div class="waitlist reveal">
      <div class="waitlist__intro">
        <span class="eyebrow">Launch updates · Free</span>
        <h2>Get Launch Updates</h2>
        <p class="lead">Be first to know when the XAUUSD Global community opens. People on the launch list get the first invitation to join.</p>
        <ul class="checklist">
          <li><strong>No payment now.</strong> Joining the waitlist is free and creates no obligation.</li>
          <li><strong>No spam.</strong> We'll only email you about the community launch.</li>
          <li><strong>Unsubscribe anytime</strong> with one click from any email.</li>
        </ul>
        <p class="muted" style="font-size:.9rem">Registration, payments and member access are not open yet. Membership is planned at {C.PLANNED_PRICE}/month; the final price and terms will be shown before anyone is asked to pay.</p>
      </div>
      <div class="waitlist__card">
        <div class="sib-form">
          <div id="sib-form-container" class="sib-form-container">
            <div id="error-message" class="sib-form-message-panel waitlist__msg waitlist__msg--error" role="alert">
              <div class="sib-form-message-panel__text"><span class="sib-form-message-panel__inner-text">Sorry, we couldn't save your details. Please check your email address and try again.</span></div>
            </div>
            <div id="success-message" class="sib-form-message-panel waitlist__msg waitlist__msg--ok" role="status">
              <div class="sib-form-message-panel__text"><span class="sib-form-message-panel__inner-text"><strong>Almost done!</strong> Please check your inbox and click the confirmation link to confirm your launch updates. (If you don't see it, check your spam or promotions folder.)</span></div>
            </div>
            <div id="sib-container" class="sib-container--large sib-container--vertical">
              <form id="sib-form" method="POST" action="{C.BREVO_FORM_ACTION}" data-type="subscription">
                <h3 class="waitlist__title">Reserve your early invitation</h3>
                <div class="sib-input sib-form-block">
                  <div class="form__entry entry_block">
                    <div class="form__label-row">
                      <label class="entry__label" for="FIRSTNAME">First name <span class="muted">(optional)</span></label>
                      <div class="entry__field"><input class="input" maxlength="200" type="text" id="FIRSTNAME" name="FIRSTNAME" autocomplete="given-name" placeholder="Your first name"></div>
                    </div>
                    <label class="entry__error entry__error--primary"></label>
                  </div>
                </div>
                <div class="sib-input sib-form-block">
                  <div class="form__entry entry_block">
                    <div class="form__label-row">
                      <label class="entry__label" for="EMAIL" data-required="*">Email address</label>
                      <div class="entry__field"><input class="input" type="email" id="EMAIL" name="EMAIL" autocomplete="email" value="" placeholder="you@example.com" data-required="true" required></div>
                    </div>
                    <label class="entry__error entry__error--primary"></label>
                  </div>
                </div>
                <div class="sib-form-block">
                  <button class="btn btn--gold waitlist__btn sib-form-block__button sib-form-block__button-with-loader" form="sib-form" type="submit" data-umami-event="waitlist-submit">
                    <svg class="icon clickable__icon progress-indicator__icon sib-hide-loader-icon" viewBox="0 0 512 512" aria-hidden="true"><path d="M460.116 373.846l-20.823-12.022c-5.541-3.199-7.54-10.159-4.663-15.874 30.137-59.886 28.343-131.652-5.386-189.946-33.641-58.394-94.896-95.833-161.827-99.676C261.028 55.961 256 50.751 256 44.352V20.309c0-6.904 5.808-12.337 12.703-11.982 83.556 4.306 160.163 50.864 202.11 123.677 42.063 72.696 44.079 162.316 6.031 236.832-3.14 6.148-10.75 8.461-16.728 5.01z"/></svg>
                    Get Launch Updates
                  </button>
                </div>
                <p class="waitlist__legal">By joining, you agree to receive emails from XAUUSD Global about the membership launch. We'll send a confirmation email first. You can unsubscribe at any time. See our <a href="/privacy-policy/">Privacy Policy</a>.</p>
                <input type="text" name="email_address_check" value="" class="input--hidden" tabindex="-1" autocomplete="off" aria-hidden="true">
                <input type="hidden" name="locale" value="en">
              </form>
            </div>
          </div>
        </div>
        <noscript><p class="waitlist__legal">Please enable JavaScript to join the waitlist, or email us at {C.CONTACT_EMAIL}.</p></noscript>
      </div>
    </div>
    <div class="btn-row mt-3" style="justify-content:center"><a class="btn btn--ghost" href="/xauusd-trading-strategies/">Explore Trading Strategies {ARROW_BTN}</a><a class="btn btn--ghost" href="/community/">Explore the Community Vision</a></div>
  </div>
  <script>
    window.REQUIRED_CODE_ERROR_MESSAGE = 'Please choose a country code';
    window.LOCALE = 'en';
    window.EMAIL_INVALID_MESSAGE = window.SMS_INVALID_MESSAGE = "Please enter a valid email address.";
    window.REQUIRED_ERROR_MESSAGE = "This field cannot be left blank.";
    window.GENERIC_INVALID_MESSAGE = "The information provided is invalid. Please check and try again.";
    window.INVALID_NUMBER = "The information provided is invalid. Please check and try again.";
    window.INVALID_DATE = "Please enter a valid date";
    window.REQUIRED_MULTISELECT_MESSAGE = 'Please select at least 1 option';
    window.translation = {{ common: {{ selectedList: '{{quantity}} list selected', selectedLists: '{{quantity}} lists selected', selectedOption: '{{quantity}} selected', selectedOptions: '{{quantity}} selected' }} }};
    var AUTOHIDE = Boolean(0);
  </script>
  <script defer src="https://sibforms.com/forms/end-form/build/main.js"></script>
</section>

<section class="section section--alt">
  <div class="wrap wrap--text"><h2>Membership FAQ</h2>{L.faq_html(faqs)}
    <div class="mt-2">{L.notice("Leveraged trading and CFDs can result in substantial losses. Membership is educational and does not guarantee results. See our <a href='/risk-disclaimer/'>risk disclaimer</a>.", "risk", "alert")}</div>
  </div>
</section>"""
    return L.page(path="/membership/", title=f"Membership & Trader Levels — Planned {C.PLANNED_PRICE}/month | XAUUSD Global",
                  description=f"XAUUSD Global membership is planned at {C.PLANNED_PRICE}/month with four discussion levels. Free guides stay free. Get launch updates today.",
                  body=body, crumbs=crumbs)


# --------------------------------------------------------------------------

def about_page():
    crumbs = [("/", "Home"), ("/about/", "About")]
    values = [
        ("message", "Reasoning over results", "A well-reasoned trade can lose; a poor one can win. We judge the thinking, the risk and the lesson — not just the outcome."),
        ("compass", "Independence, not dependence", "We want you to be able to think through the market yourself, not to need us forever."),
        ("users", "Many perspectives", "Structure, liquidity, session and macro traders read gold differently. Comparing them is how blind spots show up."),
        ("shield", "Risk first", "Protecting capital comes before any target. Risk is part of every conversation."),
        ("info", "Honesty about uncertainty", "We talk openly about losses, mistakes and what we don't know. Trading is uncertain, and we won't pretend otherwise."),
        ("target", "Skill over promises", "We never promise profits, income or financial freedom. We help people build knowledge, discipline and judgement."),
    ]
    vcards = "".join(f'<article class="card reveal"><div class="card__icon">{icon(i)}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in values)
    gaps = [
        ("A video isn't a skill", "A tutorial can introduce order blocks or liquidity in ten minutes. Applying them to a live gold chart — and knowing when they don't apply — takes practice, follow-up questions and feedback.",
         "We pair free guides with discussion, so concepts get tested on real charts."),
        ("A signal can create dependency", "A buy or sell call gives you an entry, but not the structure behind it or what would make it wrong. When the provider disappears or conditions change, you're left without a framework.",
         "We focus on the reasoning behind an idea, so you can judge the next one yourself."),
        ("The right mentor is hard to find", "Specific questions often go unanswered. Some groups are mostly promotion; others turn into contests over who made the most.",
         "We're building a space where careful questions and respectful disagreement are the norm."),
        ("Too many conflicting systems", "One person teaches one method, another says it's useless, a third claims to have the only strategy that works. Many traders spend years switching.",
         "We help you evaluate ideas by evidence, context and risk — and build a process that fits you."),
        ("Screenshots hide the full story", "A winning screenshot doesn't show the risk taken, the losing trades around it, or whether the approach is repeatable.",
         "We encourage reviews of reasoning, invalidation, risk and mistakes — not just outcomes."),
    ]
    gcards = "".join(f'<article class="card reveal"><div class="card__num">{n:02d}</div><h3>{t}</h3><p>{d}</p><p class="gap__fix"><strong>Our approach:</strong> {f}</p></article>' for n, (t, d, f) in enumerate(gaps, 1))
    body = f"""{L.page_head(crumbs, 'Why <span class="gold-text">XAUUSD Global</span> exists', 'Traders can find endless information online. What they struggle to find is the right guidance, honest feedback, meaningful discussion and a reliable path to developing their own skills.', eyebrow='About us')}
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">The problem</span>
        <h2>Information is everywhere. Guidance is not.</h2>
        <p class="lead">Many gold traders spend months or years learning: tutorials, influencers, ICT and Smart Money Concepts, Telegram groups, saved charts and indicators.</p>
        <p>Yet on their own chart, the hard questions remain. Is this a real breakout or a sweep? Where is my idea wrong? Am I too early, too late, or in the wrong conditions? Who can look at my analysis and tell me what I missed?</p>
        <p>Watching a video introduces a concept. Receiving a signal gives an entry. Neither, on its own, builds the judgement to decide for yourself when conditions change.</p>
      </div>
      <div class="reveal">
        <span class="eyebrow">Our belief</span>
        <h2>We don't want you to depend on us forever.</h2>
        <p class="lead">We want to help you become capable of thinking for yourself.</p>
        <ul class="checklist">
          <li>Read price action and market structure in context.</li>
          <li>Build a clear thesis — and define what would invalidate it.</li>
          <li>Size positions and set stops before the trade, not during it.</li>
          <li>Recognise revenge trading, overtrading and confirmation bias.</li>
          <li>Review wins and losses with the same honesty.</li>
          <li>Accept that even excellent setups can fail.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Five gaps we want to close</span><h2>Where the usual path leaves traders stuck</h2>
      <p>Many educators do genuinely valuable work. These aren't accusations — they're gaps many traders describe running into again and again.</p></div>
    <div class="cards cards--3">{gcards}</div>
  </div>
</section>
<section class="section">
  <div class="wrap wrap--text prose">
    <h2 class="mt-0">Where we fit</h2>
    <p>YouTube is excellent for discovering concepts. Courses can provide structured instruction. Signal services appeal to people who want trade ideas. Many educators do genuinely valuable work.</p>
    <p>Our role is different: <strong>we connect education, practical discussion, analytical reasoning and peer learning in one continuing community</strong>, focused on a single market. We want traders to ask not only “where might gold go next?” but also:</p>
    <ul>
      <li>Why might it move there, and what evidence supports that?</li>
      <li>What could prove the idea wrong?</li>
      <li>What risk am I taking?</li>
      <li>What should I learn if the trade fails — and how do I apply it next time?</li>
    </ul>
    <blockquote class="pull">We are not here to tell you that every trade can win. We are here to help you understand why a trade might work, what could go wrong, and what you can learn either way.</blockquote>
    <p><strong>The community is the setting. Education and discussion are the methods. Better-informed, more disciplined decision-making is the goal.</strong></p>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Values</span><h2>What we stand for</h2></div>
    <div class="cards cards--3">{vcards}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">The honest part</span>
        <h2>What learning to trade really takes</h2>
        <p class="lead">Many people come to trading hoping for more independence and control over their future. That ambition is real, and we respect it.</p>
        <p>But we won't tell you that you'll replace your salary, get rich or quit your job. Learning to trade responsibly takes time, deliberate practice, risk management and emotional discipline — and losses are part of it, even for skilled traders.</p>
        <p>What we can help you build is <strong>knowledge, independent thinking, discipline and confidence in your own process</strong>. What you do with that is yours.</p>
      </div>
      <div class="reveal">
        <span class="eyebrow">Join us if…</span>
        <h2>This is for you if you want to</h2>
        <ul class="checklist">
          <li>Understand why gold moves, not just where someone says it will go.</li>
          <li>Stop jumping between strategies and build one process you trust.</li>
          <li>Ask detailed questions without feeling foolish.</li>
          <li>Have your analysis challenged — and challenge others respectfully.</li>
          <li>Review your losses honestly and learn from them.</li>
        </ul>
        <p class="muted">Not "join us because you can't succeed without us" — join us if you want to take your learning seriously and grow alongside people who care about understanding the market.</p>
      </div>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Where we are today</span>
        <h2>Built in the open, one stage at a time</h2>
        <ul class="status-list">
          <li><span class="badge badge--live">Now</span>Free guides on XAUUSD strategy, risk, sessions and market drivers.</li>
          <li><span class="badge badge--live">Now</span>Gold news hub with an economic calendar.</li>
          <li><span class="badge badge--soon">Next</span>The learning community: analysis discussion, feedback and trade reviews.</li>
          <li><span class="badge badge--no">Later</span>Member tools such as shared journals and review templates.</li>
        </ul>
        <p class="mt-2 muted">Plans may change as we learn from traders. We'll update this page as each stage becomes real.</p>
      </div>
      <div class="reveal">
        <span class="eyebrow">What we will never do</span>
        <h2>Our commitments</h2>
        <ul class="checklist">
          <li>Promise profits, income or financial freedom.</li>
          <li>Publish fake testimonials, member stories or trading results.</li>
          <li>Present hypothetical examples as real trades.</li>
          <li>Manage money or take trades on anyone's behalf.</li>
          <li>Advertise a community feature before it exists.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap wrap--text prose">
    <h2 class="mt-0" id="founder">Who is behind XAUUSD Global</h2>
    <p>XAUUSD Global is an independent project focused entirely on gold. A founder profile — who runs the site and their trading background, described plainly and verifiably — will be published here. We won't publish invented credentials, trading records, testimonials or member numbers.</p>
    <h2 id="editorial-standards">Our editorial standards</h2>
    <ul>
      <li>Articles are original and written to explain how traders think about gold, not to sell outcomes.</li>
      <li>Hypothetical examples are labelled as hypothetical. Real market examples will always carry a date.</li>
      <li>News is never invented. Headlines are credited to and linked to the original publisher.</li>
      <li>Each article shows its publication date. A “last reviewed” date appears only after a genuine review.</li>
      <li>Corrections are welcome — email <a href="mailto:{C.CONTACT_EMAIL}">{C.CONTACT_EMAIL}</a> with the page and the issue.</li>
      <li>We aren't a regulated financial adviser and nothing on this site is personalised advice. See our <a href="/risk-disclaimer/">risk disclaimer</a>.</li>
    </ul>
    {L.community_cta()}
  </div>
</section>"""
    return L.page(path="/about/", title="About XAUUSD Global — Our Mission and Philosophy",
                  description="Why XAUUSD Global exists: helping gold traders move beyond signals and scattered information to build their own judgement through reasoning, discussion and review.",
                  body=body, crumbs=crumbs)


# --------------------------------------------------------------------------

def prose_page(meta, body_md, path):
    crumbs = [("/", "Home"), (path, meta["short"])]
    html_body, _ = L.render_md(body_md)
    extra = ""
    faqs = meta.get("faqs") or []
    faq_block = ""
    schema = []
    if faqs:
        groups = {}
        for f in faqs:
            groups.setdefault(f.get("group", "General"), []).append(f)
        faq_block = "".join(f'<h2 id="{g.lower().replace(" ", "-")}">{esc(g)}</h2>{L.faq_html(fs)}' for g, fs in groups.items())
        schema.append(L.faq_schema(faqs))
    updated = f'<p class="muted">Last updated: {L.fmt_date(meta["updated"])}</p>' if meta.get("updated") else ""
    body = f"""{L.page_head(crumbs, esc(meta['title']), esc(meta['lede']), eyebrow=meta.get('eyebrow'), extra=extra)}
<section class="section section--tight"><div class="wrap wrap--text prose">{updated}{html_body}{faq_block}</div></section>"""
    return L.page(path=path, title=meta["seo_title"], description=meta["description"], body=body, crumbs=crumbs,
                  schema_extra=schema)


def contact_body():
    if C.CONTACT_EMAIL:
        return f"Email us at <a href=\"mailto:{C.CONTACT_EMAIL}\">{C.CONTACT_EMAIL}</a>."
    return ("<strong>Our public contact channel is being set up.</strong> A monitored email address will be published here before community "
            "registration opens. We are not collecting messages through forms on this site.")


def waitlist_confirmed():
    """Shown after a visitor clicks the double opt-in link in Brevo's email."""
    body = f"""<section class="hero grid-bg">
  <div class="wrap wrap--text center">
    <div class="confirm-badge" aria-hidden="true">{icon("shield")}</div>
    <span class="eyebrow">Launch updates · Confirmed</span>
    <h1>You're on the list. <span class="gold-text">Welcome.</span></h1>
    <p class="hero__lede" style="margin-left:auto;margin-right:auto">Thank you for confirming your email. You're now on the XAUUSD Global launch list, and you'll be among the first to hear when the community opens. Until then, the free guides are the best place to start building your process.</p>
    <div class="btn-row" style="justify-content:center"><a class="btn btn--gold" href="/xauusd-trading-strategies/">Explore Trading Strategies {ARROW_BTN}</a><a class="btn btn--ghost" href="/community/">Read the Community Vision</a></div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="section-head section-head--center"><span class="eyebrow">What happens next</span><h2>Three things to know</h2></div>
    <div class="steps" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">
      <div class="step"><h3>We'll email you at launch</h3><p>You'll receive an invitation from <strong>updates@xauusdglobal.com</strong> as soon as registration opens. Add it to your contacts so it doesn't land in spam.</p></div>
      <div class="step"><h3>No payment, no obligation</h3><p>Joining the waitlist is free. The final price and membership terms will be shown clearly before anyone is asked to pay.</p></div>
      <div class="step"><h3>Unsubscribe anytime</h3><p>Every email includes a one-click unsubscribe link. Read how we handle your details in our <a href="/privacy-policy/">Privacy Policy</a>.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Start learning while you wait</span><h2>Popular guides</h2></div>
    <div class="cards cards--3">
      {card("/strategies/market-structure-xauusd/", "XAUUSD market structure", "The shared language most community discussions will use: swings, BOS and CHoCH.", tag="Guide")}
      {card("/strategies/xauusd-risk-management/", "Risk management & position sizing", "Size gold positions from your stop distance and protect your account.", tag="Guide")}
      {card("/blog/how-to-keep-a-trading-journal/", "How to keep a trading journal", "Build the review habit that structured community feedback depends on.", tag="Blog")}
    </div>
  </div>
</section>"""
    return L.page(path="/waitlist-confirmed/", title="You're on the Waitlist | XAUUSD Global",
                  description="Your place on the XAUUSD Global launch-updates list is confirmed.", body=body, noindex=True)


def not_found():
    body = f"""<section class="hero grid-bg"><div class="wrap wrap--text center">
  <span class="eyebrow">Error 404</span>
  <h1>This level didn't hold.</h1>
  <p class="hero__lede" style="margin-left:auto;margin-right:auto">The page you were looking for doesn't exist or has moved. Here are some useful places to continue:</p>
  <div class="btn-row" style="justify-content:center"><a class="btn btn--gold" href="/">Back to the homepage</a><a class="btn btn--ghost" href="/xauusd-trading-strategies/">Trading strategies</a></div>
  <div class="related" style="text-align:left"><ul>
    <li><a href="/xauusd-price/">XAUUSD price and chart</a></li>
    <li><a href="/blog/">Gold trading blog</a></li>
    <li><a href="/community/">Community vision</a></li>
    <li><a href="/faq/">Frequently asked questions</a></li>
  </ul></div>
</div></section>"""
    return L.page(path="/404.html", title="Page Not Found | XAUUSD Global",
                  description="The requested page could not be found on XAUUSD Global.", body=body, noindex=True)


# --------------------------------------------------------------------------

def calculator_page():
    path = "/tools/position-size-calculator/"
    crumbs = [("/", "Home"), ("/xauusd-trading-strategies/", "Trading Strategies"), (path, "Position Size Calculator")]
    faqs = [
        {"q": "How is the XAUUSD lot size calculated?", "a": "Lot size = amount you're willing to risk ÷ (stop distance in dollars × ounces per lot). With a standard contract of 100 oz, a $1.00 move in gold changes the value of 1 lot by $100. So risking $100 with a $5.00 stop gives 100 ÷ (5 × 100) = 0.20 lots."},
        {"q": "Is one lot of gold always 100 ounces?", "a": "No. Many brokers use 100 oz per standard lot, but some use different contract sizes. Check your broker's contract specification and change the \"ounces per lot\" field if needed."},
        {"q": "What percentage should I risk per trade?", "a": "There is no correct number for everyone. Many educational sources discuss risking a small fixed percentage, often 0.5–2% of the account, so that a run of losses doesn't do serious damage. Choose what you can accept losing several times in a row."},
        {"q": "Does this calculator account for spreads, commission or slippage?", "a": "No. It shows risk at your stop price only. Spreads, commission, swaps and slippage — especially around news or weekend gaps — can make a real loss larger than the calculated amount."},
        {"q": "My account isn't in US dollars. Can I still use it?", "a": "XAUUSD profit and loss is in US dollars. If your account is in another currency, convert your risk amount to USD first, enter it as the balance and risk, then convert the result back."},
    ]
    body = f"""{L.page_head(crumbs, 'XAUUSD <span class="gold-text">Position Size Calculator</span>', 'Work out your gold lot size from your account balance, the percentage you are willing to risk and your stop-loss — before you enter the trade.', eyebrow='Free tool')}
<section class="section--tight section">
  <div class="wrap">
    <div class="calc reveal">
      <form class="calc__form" id="calc" novalidate>
        <div class="calc__grid">
          <label class="calc__field"><span>Account balance (USD)</span><input class="input" type="number" inputmode="decimal" id="c-bal" value="5000" min="0" step="any"></label>
          <label class="calc__field"><span>Risk per trade (%)</span><input class="input" type="number" inputmode="decimal" id="c-risk" value="1" min="0" step="any"></label>
          <label class="calc__field"><span>Entry price</span><input class="input" type="number" inputmode="decimal" id="c-entry" value="4000" min="0" step="any"></label>
          <label class="calc__field"><span>Stop-loss price</span><input class="input" type="number" inputmode="decimal" id="c-stop" value="3995" min="0" step="any"></label>
          <label class="calc__field"><span>Take-profit price <small>(optional)</small></span><input class="input" type="number" inputmode="decimal" id="c-tp" value="4010" min="0" step="any"></label>
          <label class="calc__field"><span>Ounces per lot <small>(check your broker)</small></span><input class="input" type="number" inputmode="decimal" id="c-oz" value="100" min="0" step="any"></label>
        </div>
        <p class="calc__note">Example values are hypothetical. Enter your own numbers — results update as you type.</p>
      </form>
      <div class="calc__out" aria-live="polite">
        <div class="calc__main"><span>Position size</span><strong id="o-lots">—</strong><small id="o-oz"></small></div>
        <dl class="calc__list">
          <div><dt>Amount at risk</dt><dd id="o-risk">—</dd></div>
          <div><dt>Stop distance</dt><dd id="o-dist">—</dd></div>
          <div><dt>Value of a $1 move</dt><dd id="o-pv">—</dd></div>
          <div><dt>Risk at rounded size</dt><dd id="o-real">—</dd></div>
          <div><dt>Potential reward</dt><dd id="o-rew">—</dd></div>
          <div><dt>Risk : reward</dt><dd id="o-rr">—</dd></div>
        </dl>
        <p class="calc__warn" id="o-warn" hidden></p>
      </div>
    </div>
    <p class="muted mt-2" style="font-size:.9rem">Lots are rounded <strong>down</strong> to 0.01 so you never risk more than you chose. Results ignore spreads, commission, swaps and slippage, which can increase real losses — especially around news and weekend gaps. Educational tool only, not financial advice.</p>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--text prose">
    <h2 class="mt-0">How the calculation works</h2>
    <p>Position sizing turns a decision you've already made — <em>where is my idea wrong?</em> — into a trade size. The stop comes first; the size follows from it. Never the other way round.</p>
    <ol>
      <li><strong>Amount at risk</strong> = balance × risk %. For example, $5,000 × 1% = $50.</li>
      <li><strong>Stop distance</strong> = the gap between entry and stop in dollars. For example, $4,000 − $3,995 = $5.00.</li>
      <li><strong>Value per $1 move</strong> = ounces per lot × lots. At 100 oz, 1 lot moves $100 per $1 in gold.</li>
      <li><strong>Lot size</strong> = amount at risk ÷ (stop distance × ounces per lot). Here: $50 ÷ ($5 × 100) = <strong>0.10 lots</strong>.</li>
    </ol>
    <p>Notice what happens if you widen the stop to $10 with the same $50 risk: the size halves to 0.05 lots. A wider stop doesn't mean more risk — it means a smaller position.</p>
    <h2>Common sizing mistakes on gold</h2>
    <ul>
      <li><strong>Choosing the lot size first</strong>, then squeezing the stop to fit. The stop should sit where the idea is invalid.</li>
      <li><strong>Forgetting gold's speed.</strong> A $5 stop on a quiet Asian session and on a CPI release are very different risks.</li>
      <li><strong>Assuming the contract size.</strong> Some brokers don't use 100 oz per lot — check yours.</li>
      <li><strong>Raising size after losses</strong> to win it back. That's how a bad week becomes a damaged account.</li>
    </ul>
    <p>For the full method, read <a href="/strategies/xauusd-risk-management/">XAUUSD risk management and position sizing</a> and <a href="/blog/risk-management-volatile-gold-markets/">risk management for volatile gold markets</a>.</p>
    <aside class="think" aria-labelledby="think-h"><span class="eyebrow">Before you click buy or sell</span>
      <h2 id="think-h">Think it through</h2>
      <ol>
        <li>Is your stop where the trade idea is wrong — or where the loss feels comfortable?</li>
        <li>Could news or a weekend gap move price past your stop?</li>
        <li>If this trade and the next four all lose, is that acceptable?</li>
        <li>Is today's size the same rule you used yesterday?</li>
      </ol>
    </aside>
    <h2>Frequently asked questions</h2>{L.faq_html(faqs)}
    {L.community_cta()}
  </div>
</section>
<script>
(function(){{
  var $=function(i){{return document.getElementById(i)}};
  var f=function(n){{return n.toLocaleString('en-US',{{minimumFractionDigits:2,maximumFractionDigits:2}})}};
  var ids=['c-bal','c-risk','c-entry','c-stop','c-tp','c-oz'];
  function v(i){{var x=parseFloat($(i).value);return isFinite(x)?x:NaN}}
  function calc(){{
    var bal=v('c-bal'),rp=v('c-risk'),en=v('c-entry'),st=v('c-stop'),tp=v('c-tp'),oz=v('c-oz'),w=$('o-warn');
    var out=['o-lots','o-oz','o-risk','o-dist','o-pv','o-real','o-rew','o-rr'];
    w.hidden=true;
    if(!(bal>0&&rp>0&&en>0&&st>0&&oz>0)||en===st){{out.forEach(function(o){{$(o).textContent=o==='o-oz'?'':'—'}});
      if(en===st&&en>0){{w.textContent='Entry and stop-loss can’t be the same price.';w.hidden=false}}return}}
    var risk=bal*rp/100,dist=Math.abs(en-st),raw=risk/(dist*oz),lots=Math.floor(raw*100+1e-9)/100,real=lots*oz*dist;
    $('o-lots').textContent=lots.toFixed(2)+' lots';
    $('o-oz').textContent='= '+f(lots*oz)+' oz (exact: '+raw.toFixed(3)+')';
    $('o-risk').textContent='$'+f(risk);
    $('o-dist').textContent='$'+f(dist);
    $('o-pv').textContent='$'+f(lots*oz)+' per $1';
    $('o-real').textContent='$'+f(real)+' ('+(real/bal*100).toFixed(2)+'%)';
    var long=en>st;
    if(tp>0&&((long&&tp>en)||(!long&&tp<en))){{var rew=Math.abs(tp-en)*lots*oz;$('o-rew').textContent='$'+f(rew);$('o-rr').textContent='1 : '+(Math.abs(tp-en)/dist).toFixed(2)}}
    else{{$('o-rew').textContent='—';$('o-rr').textContent='—';if(tp>0){{w.textContent='Take-profit is on the wrong side of entry for a '+(long?'buy':'sell')+'.';w.hidden=false}}}}
    if(lots<0.01){{w.textContent='Your risk is too small for a 0.01-lot position with this stop. Widen your risk or tighten the stop only if the idea allows it.';w.hidden=false}}
    else if(rp>2){{w.textContent='You are risking more than 2% of your account on one trade. A few losses in a row would hurt. Make sure that’s a deliberate choice.';w.hidden=false}}
  }}
  ids.forEach(function(i){{$(i).addEventListener('input',calc)}});
  $('calc').addEventListener('submit',function(e){{e.preventDefault()}});
  calc();
}})();
</script>"""
    schema = [L.faq_schema(faqs), {"@type": "WebApplication", "name": "XAUUSD Position Size Calculator", "url": L.canonical(path),
               "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "isAccessibleForFree": True,
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": L.ORG_ID}}]
    return L.page(path=path, title="XAUUSD Position Size Calculator — Gold Lot Size Calculator",
                  description="Free XAUUSD position size calculator: work out your gold lot size from account balance, risk percentage and stop-loss, with risk-to-reward.",
                  body=body, crumbs=crumbs, schema_extra=schema)


def build_all(strategies, posts, titles):
    out = [
        ("/", home(strategies, posts), "1.0"),
        ("/xauusd-price/", price_page(), "0.9"),
        ("/xauusd-news/", news_page(), "0.8"),
        ("/xauusd-trading-strategies/", strategy_hub(strategies), "0.9"),
        ("/blog/", blog_index(posts), "0.8"),
        ("/community/", community_page(), "0.9"),
        ("/membership/", membership_page(), "0.8"),
        ("/about/", about_page(), "0.6"),
        ("/tools/position-size-calculator/", calculator_page(), "0.8"),
    ]
    for name, prio in [("contact", "0.4"), ("faq", "0.6"), ("risk-disclaimer", "0.4"), ("privacy-policy", "0.3"), ("terms", "0.3")]:
        meta, body = L.load_md(os.path.join(CONTENT, "pages", f"{name}.md"))
        body = body.replace("{{CONTACT}}", contact_body())
        out.append((f"/{name}/", prose_page(meta, body, f"/{name}/"), prio))
    return out


def make_images(root):
    img = os.path.join(root, "assets", "images")
    os.makedirs(img, exist_ok=True)
    svg = L.LOGO_SVG.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    open(os.path.join(img, "favicon.svg"), "w").write(svg)
    open(os.path.join(img, "logo.svg"), "w").write(svg)
