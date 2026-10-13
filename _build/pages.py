"""Hand-designed pages: home, price, news, strategy hub, community, membership,
about, FAQ, legal pages and 404."""
import json
import os

import yaml

import config as C
import lib as L
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
    "/privacy-policy/": "Privacy policy (draft)",
    "/terms/": "Terms of use (draft)",
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
    marquee_items = ["One market. Different perspectives. Better traders.", "Stop learning alone. Start learning together.",
                     "Connect with traders who challenge your thinking.", "Learn the reasoning behind a trade, not just the entry.",
                     "Better analysis. Stronger discipline. A more structured process."]
    mq = "".join(f"<span>{esc(t)}</span>" for t in marquee_items * 2)
    mini_cfg = {"symbol": C.TV_SYMBOL, "width": "100%", "height": "100%", "locale": "en", "dateRange": "1D",
                "colorTheme": "dark", "isTransparent": True, "autosize": True, "largeChartUrl": ""}
    faqs = [
        {"q": "Is XAUUSD Global open for registration?", "a": "Not yet. The educational website is public and free to read today. Community registration, payments and member access are being developed and are **not available yet**. We do not collect sign-ups or payment details at this stage."},
        {"q": "Do you sell trading signals?", "a": "No. XAUUSD Global is built around discussion, analysis and review — learning *why* a trade idea exists and how it is risk-managed — not around copying unexplained entries."},
        {"q": "How much will membership cost?", "a": f"Membership is currently planned at **{C.PLANNED_PRICE} per month**. This is a planned price, not an active offer, and may change before launch. See [membership and trader levels](/membership/)."},
        {"q": "Will joining the community make me profitable?", "a": "No community, course or strategy can guarantee results. Trading leveraged gold products carries a high risk of loss. Our aim is to help traders build better analysis habits, discipline and review processes."},
        {"q": "Why focus only on gold?", "a": "Gold has its own drivers, sessions and behaviour. Concentrating on one market lets discussions go deeper and lets traders compare like-for-like analysis instead of scattering attention across dozens of instruments."},
    ]
    body = f"""
<section class="hero grid-bg">
  <div class="wrap hero__grid">
    <div>
      <span class="status-pill"><span class="dot"></span>Educational hub live · Community registration opening soon</span>
      <h1>Trade Gold. <span class="gold-text">Think Deeper.</span> Grow Together.</h1>
      <p class="hero__lede">XAUUSD Global is building a worldwide community where intermediate traders connect with advanced, Pro, and Degen traders to exchange market perspectives, study strategies, review trade ideas, and sharpen their trading skills.</p>
      <div class="btn-row">
        <a class="btn btn--gold" href="/xauusd-trading-strategies/">Explore Trading Strategies {ARROW_BTN}</a>
        <a class="btn btn--ghost" href="/membership/#registration">Community Registration Opening Soon</a>
      </div>
      <div class="hero__status">
        <span class="status-pill"><span class="dot"></span>Free guides &amp; articles: available now</span>
        <span class="status-pill"><span class="dot dot--gold"></span>Paid community: not open yet</span>
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

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Our difference</span>
        <h2>We connect traders to traders — not followers to signals.</h2>
        <p class="lead">Most trading content is a one-way broadcast: an entry, a target, a screenshot of a win. You learn very little from that. XAUUSD Global is being built around conversation — intermediate traders comparing their reasoning with traders who have more experience, and everyone reviewing their losses as openly as their wins.</p>
        <ul class="checklist">
          <li><strong>Different perspectives on one market.</strong> See how a structure trader, a liquidity trader and a session trader read the same gold chart.</li>
          <li><strong>Reasoning before entries.</strong> Every idea is expected to state its thesis, invalidation and risk.</li>
          <li><strong>Honest reviews.</strong> Post-trade reviews and journals, including the trades that didn't work.</li>
        </ul>
        <a class="btn btn--gold" href="/community/">Explore the Community Vision {ARROW_BTN}</a>
      </div>
      <div class="compare reveal">
        <div class="compare__col compare__col--bad"><h3>Typical signal channel</h3><ul>
          <li>Unexplained entries to copy</li><li>Wins highlighted, losses hidden</li><li>Dependency on one caller</li><li>No review of decision quality</li><li>Scattered across many markets</li></ul></div>
        <div class="compare__col compare__col--good"><h3>XAUUSD Global (planned)</h3><ul>
          <li>Trade theses with clear invalidation</li><li>Post-trade reviews, wins and losses</li><li>Many perspectives, peer feedback</li><li>Focus on process and risk</li><li>Deep focus on gold only</li></ul></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Who it's for</span><h2>One market. Four ways of seeing it.</h2>
      <p>The community is designed around trader levels so that discussions stay useful for everyone. Levels are planned discussion categories — not badges you buy.</p></div>
    <div class="cards cards--4">
      <article class="card reveal"><div class="card__icon">{icon("compass")}</div><h3>Intermediate</h3><p>You know the basics and you've placed real trades. Now you want structure, feedback, and to understand why setups fail.</p></article>
      <article class="card reveal"><div class="card__icon">{icon("layers")}</div><h3>Advanced</h3><p>You have a method. You want to stress-test it, compare trade plans, and refine your read of structure and liquidity.</p></article>
      <article class="card reveal"><div class="card__icon">{icon("target")}</div><h3>Pro</h3><p>You can explain your process clearly and enjoy breaking down theses, post-trade reviews, and helping others improve.</p></article>
      <article class="card reveal"><div class="card__icon">{icon("bolt")}</div><h3>Degen</h3><p>Experimental and high-conviction — but accountable. Complex scenarios, alternative theses and rigorous, transparent risk controls.</p></article>
    </div>
    <p class="mt-2"><a href="/membership/">See how the planned trader levels work</a></p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Featured strategies</span><h2>XAUUSD trading strategies, explained properly.</h2>
      <p>In-depth guides on how traders analyse gold — what each framework claims, how it's applied to XAUUSD, where it breaks down, and how to manage risk around it.</p></div>
    <div class="cards cards--3">{strat_cards}</div>
    <div class="mt-3"><a class="btn btn--ghost" href="/xauusd-trading-strategies/">Browse all 18 strategy topics {ARROW_BTN}</a></div>
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
    <div class="section-head reveal"><span class="eyebrow">Latest gold-market news</span><h2>News that moves gold — with the context to read it.</h2></div>
    {L.notice("<strong>Market news feed integration coming soon.</strong> We don't publish invented or copied headlines. Until a licensed news feed is connected, our news hub explains the event types that move gold and how traders interpret them.", "info", "news")}
    <div class="cards cards--3 mt-2">
      {card("/xauusd-news/#fed", "Federal Reserve decisions", "Rate decisions and guidance shift real yields and the dollar — two of gold's key drivers.", tag="Explainer")}
      {card("/xauusd-news/#inflation", "Inflation data", "CPI and PCE releases change rate expectations, often producing sharp intraday gold moves.", tag="Explainer")}
      {card("/xauusd-news/#central-banks", "Central-bank gold demand", "Official-sector buying and selling is a slower-moving but important structural factor.", tag="Explainer")}
    </div>
    <div class="mt-3"><a class="btn btn--ghost" href="/xauusd-news/">Visit the XAUUSD news hub {ARROW_BTN}</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">From the blog</span><h2>Latest articles</h2></div>
    <div class="cards cards--3">{blog_cards}</div>
    <div class="mt-3"><a class="btn btn--ghost" href="/blog/">Read the gold trading blog {ARROW_BTN}</a></div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">Why learn together</span><h2>Better decisions come from better feedback.</h2>
      <p>Trading alone, it's easy to repeat the same mistake for months without noticing. Structured discussion shortens that loop.</p></div>
    <div class="steps">
      <div class="step reveal"><h3>Share the thesis</h3><p>Explain what you see on the chart, why, and what would prove you wrong — before the outcome is known.</p></div>
      <div class="step reveal"><h3>Get challenged</h3><p>Traders at other levels test your reasoning, point out missed context and offer alternative reads.</p></div>
      <div class="step reveal"><h3>Review honestly</h3><p>Afterwards, review the decision — not just the result. Good trades can lose; bad trades can win.</p></div>
      <div class="step reveal"><h3>Refine the process</h3><p>Over time, patterns in your reviews show what to keep, what to drop and where your risk habits slip.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Why one market</span>
        <h2>Gold deserves undivided attention.</h2>
        <p>XAUUSD reacts to its own mix of forces — the US dollar, real interest rates, inflation expectations, central-bank demand, geopolitics and session-driven liquidity. It can move many dollars within minutes around major data.</p>
        <p>By building the whole community around a single market, discussions can go deep: everyone looks at the same chart, the same sessions and the same news, so comparisons are genuinely like-for-like.</p>
        <a href="/blog/what-is-xauusd/">New to the market? Start with our practical guide to XAUUSD</a>
      </div>
      <div class="reveal">
        <div class="tier tier--pro" style="padding:34px">
          <span class="tier__lvl">Membership preview</span>
          <div class="price-big" style="margin:14px 0 6px">{C.PLANNED_PRICE}<small> /month · planned</small></div>
          <p class="muted">One planned price. Access to discussion categories based on demonstrated analysis quality and contribution — not on paying more.</p>
          <ul class="status-list" style="margin-top:18px">
            <li><span class="badge badge--live">Live</span>Public educational website</li>
            <li><span class="badge badge--soon">Soon</span>Community registration</li>
            <li><span class="badge badge--no">Not yet</span>Payments &amp; member access</li>
          </ul>
          <div class="btn-row mt-2"><a class="btn btn--gold" href="/membership/">See membership &amp; levels {ARROW_BTN}</a></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wrap--text">
    <div class="section-head reveal"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>
    {L.faq_html(faqs)}
    <p class="mt-2"><a href="/faq/">Read all frequently asked questions</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {L.community_cta()}
    <div class="mt-2">{L.notice("<strong>Risk warning.</strong> Leveraged trading and CFDs can result in substantial losses. Content on XAUUSD Global is educational and not personalised financial advice. No strategy or community participation guarantees results.", "risk", "alert")}</div>
  </div>
</section>"""
    return L.page(path="/", title="XAUUSD Global — Gold Trading Community, Strategies & Education",
                  description="XAUUSD Global connects gold traders to learn together: XAUUSD trading strategies, a live gold chart, market education and a planned trading community.",
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
<section class="section--tight section"><div class="wrap">{L.community_cta()}</div></section>"""
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
    body = f"""{L.page_head(crumbs, 'XAUUSD News: <span class="gold-text">What Moves Gold</span> and Why', 'A gold-market news hub built to explain, not just report: the event categories that drive XAUUSD, how traders interpret them, and how to prepare your risk around them.', eyebrow='Gold market news')}
<section class="section section--tight">
  <div class="wrap" data-news-feed="{feed_url}">
    <h2>Latest gold-market headlines</h2>
    <div class="news-empty">{L.notice("<strong>Market news feed integration coming soon.</strong> XAUUSD Global does not invent headlines, dates or quotes, and we don't republish other publishers' articles. When a licensed feed is connected, headlines will appear here with the source, publication date, an original summary and a link to the original reporting. Until then, the explainers below are evergreen educational content — not time-sensitive news.", "info", "news")}</div>
    <div class="cards cards--3 news-feed" hidden></div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Evergreen explainers</span><h2>News categories and why they affect gold</h2>
      <p>Knowing <em>why</em> a type of event matters helps you decide whether to trade, wait, or reduce size around it.</p></div>
    <div class="news-cats">{cats}</div>
  </div>
</section>
<section class="section">
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
<section class="section--tight section"><div class="wrap">{L.community_cta()}</div></section>"""
    return L.page(path="/xauusd-news/", title="XAUUSD News — Gold Market Drivers Explained | XAUUSD Global",
                  description="Gold market news hub for XAUUSD traders: how the Fed, inflation, the US dollar, Treasury yields, geopolitics and central banks affect the gold price.",
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
<section class="section"><div class="wrap">{L.community_cta()}</div></section>"""
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
        ("users", "Connect across experience levels", "Meet intermediate, advanced, Pro and Degen traders who all focus on the same market."),
        ("chart", "Discuss XAUUSD structure", "Talk through market structure, liquidity and trading concepts on live gold charts."),
        ("compass", "Compare perspectives", "See how traders using different frameworks read the same price action — and where they disagree."),
        ("journal", "See how plans are built", "Learn how other traders develop, document and review their trade plans."),
        ("message", "Share breakdowns & reviews", "Post chart breakdowns and post-trade reviews for structured feedback."),
        ("shield", "Improve risk habits", "Make position sizing, invalidation and drawdown rules part of every discussion."),
        ("repeat", "Learn from mistakes", "Losses and errors are reviewed openly, not hidden behind highlight reels."),
        ("layers", "Build a structured process", "Turn scattered ideas into a repeatable process you can measure and refine."),
        ("news", "Organised discussion", "Topic-based, level-aware discussions instead of scattered social-media posts."),
        ("globe", "Global relationships", "Build lasting trading relationships with people across time zones and sessions."),
    ]
    bcards = "".join(f'<article class="card reveal"><div class="card__icon">{icon(i)}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in benefits)
    faqs = [
        {"q": "When will the community open?", "a": "We haven't announced a date. Registration will open once the platform, community standards, privacy policy and terms are finalised. This website will be updated when that happens."},
        {"q": "Where will discussions take place?", "a": "The platform is still being chosen and built. We'll publish details — including how data is handled — before registration opens."},
        {"q": "Will experienced traders give me trades to copy?", "a": "No. The community is designed for sharing reasoning and reviews, not for copying entries. Members remain responsible for their own decisions."},
        {"q": "Does membership guarantee better results?", "a": "No. Community membership does not guarantee profitable trading. Leveraged gold trading can result in substantial losses."},
    ]
    body = f"""{L.page_head(crumbs, 'A Global Community for <span class="gold-text">XAUUSD Traders</span>', 'We connect intermediate traders with advanced, Pro, and Degen traders to encourage better analysis, stronger execution habits, and continuous improvement.', eyebrow='Community vision', extra='<div class="hero__status"><span class="status-pill"><span class="dot dot--gold"></span>In development · Registration not open yet</span></div>')}
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">The mission</span>
        <h2>Stop learning alone. Start learning together.</h2>
        <p class="lead">Most traders improve slowly because they learn in isolation. They repeat the same errors, can't see their own blind spots, and rely on fragments of advice from social media.</p>
        <p>XAUUSD Global is being built to change that for gold traders. Instead of selling information one way, we want to connect traders to traders — so an intermediate trader can put their analysis next to that of someone more experienced, ask why, and get an honest answer.</p>
        <p>One market. Different perspectives. Better traders.</p>
      </div>
      <div class="reveal">
        <div class="compare">
          <div class="compare__col compare__col--bad"><h3>Copying an entry</h3><ul><li>Works until it doesn't</li><li>You can't tell a good loss from a bad one</li><li>No transferable skill</li></ul></div>
          <div class="compare__col compare__col--good"><h3>Understanding the reasoning</h3><ul><li>You learn the context and the invalidation</li><li>You can judge decision quality</li><li>Skills compound over time</li></ul></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Planned membership benefits</span><h2>What the community aims to provide</h2>
      <p>These are the benefits we are designing for. Exact features will be confirmed before launch.</p></div>
    <div class="cards cards--3">{bcards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">How discussions will work</span><h2>Structured conversation, not a noisy feed</h2></div>
    <div class="steps">
      <div class="step reveal"><h3>Chart breakdowns</h3><p>Members post an XAUUSD chart with their read of structure, key levels and context.</p></div>
      <div class="step reveal"><h3>Trade-plan reviews</h3><p>Ideas are expected to include a thesis, an invalidation level and the planned risk — before the outcome.</p></div>
      <div class="step reveal"><h3>Post-trade reviews</h3><p>After the trade, members review the decision, execution and emotions — win or loss.</p></div>
      <div class="step reveal"><h3>Level-based rooms</h3><p>Discussion categories for Starter, Advanced, Pro and Degen keep conversations useful at every level.</p></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Community standards (draft)</span>
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
        <div class="mt-2">{L.notice("<strong>Registration is not open yet.</strong> We are not collecting names, emails or payment details at this stage. When registration opens, it will be announced on this site.", "", "lock")}</div>
        <div class="btn-row mt-2"><a class="btn btn--gold" href="/membership/">See membership &amp; trader levels {ARROW_BTN}</a></div>
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
      {card("/blog/common-mistakes-intermediate-gold-traders/", "Common mistakes intermediate gold traders make", "The patterns we see most often — and how to break them.", tag="Blog")}
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wrap--text"><h2>Community FAQ</h2>{L.faq_html(faqs)}</div>
</section>"""
    return L.page(path="/community/", title="XAUUSD Trading Community — Learn Gold Trading Together | XAUUSD Global",
                  description="The XAUUSD Global community connects intermediate gold traders with advanced, Pro and Degen traders to compare analysis, review trades and improve together.",
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
        {"q": "Can I pay now or pre-register?", "a": "No. Payment and member access are not available yet, and we're not running a waiting list. Please don't send money to anyone claiming to sell XAUUSD Global memberships."},
        {"q": "Does a higher level cost more?", "a": f"No. The plan is one membership at {C.PLANNED_PRICE} per month. Levels are discussion categories and participation privileges earned through contribution quality — they cannot be bought."},
        {"q": "How will I move between levels?", "a": "Advancement is planned to depend on demonstrated analytical quality, risk awareness, transparent reviews and meaningful contributions — not on payment or a single profitable trade. Exact criteria will be published before launch."},
        {"q": "Is the price final?", "a": f"{C.PLANNED_PRICE}/month is the currently planned price. It may change before launch, and the final price and terms will be shown clearly before anyone is asked to pay."},
        {"q": "Will members receive trading signals?", "a": "No. Membership is about discussion, analysis and review. It does not include signals to copy, managed accounts or personalised financial advice."},
    ]
    body = f"""{L.page_head(crumbs, 'Membership &amp; <span class="gold-text">Trader Levels</span>', 'One planned membership. Four discussion levels. Advancement earned through analysis quality and contribution — never bought.', eyebrow='Planned membership')}
<section class="section">
  <div class="wrap">
    <div class="price-hero reveal">
      <span class="eyebrow">Membership planned</span>
      <div class="price-big">{C.PLANNED_PRICE}<small> /month</small></div>
      <p class="lead" style="max-width:640px;margin:16px auto 28px">Membership planned: {C.PLANNED_PRICE}/month. Registration opening soon. Payment and member access are not available yet.</p>
      <ul class="status-list" style="max-width:520px;margin:0 auto;text-align:left">
        <li><span class="badge badge--live">Live</span>Public educational website and guides</li>
        <li><span class="badge badge--soon">Soon</span>Community registration</li>
        <li><span class="badge badge--no">Not yet</span>Payment and member access</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Trader levels</span><h2>Four planned discussion levels</h2>
      <p>These levels represent intended discussion categories and participation privileges. Access criteria and exact benefits will be finalised before launch.</p></div>
    <div class="tiers">{tier_html}</div>
  </div>
</section>

<section class="section">
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
        <h3 class="mt-2">What it does not include</h3>
        <p class="muted">No guaranteed access to profitable traders, no winning signals, no financial returns or specific performance, and no personalised financial advice.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt" id="registration">
  <div class="wrap wrap--text">
    <div class="cta-band reveal">
      <span class="eyebrow">Registration status</span>
      <h2>Registration is not open yet.</h2>
      <p>We're finishing the community platform, standards, privacy policy and terms before accepting any members. There is no sign-up form, waiting list or checkout on this site yet, and we are not collecting personal or payment details. When registration opens, this section will be updated.</p>
      <p>Join the next chapter of gold trading by building your foundations now:</p>
      <div class="btn-row"><a class="btn btn--gold" href="/xauusd-trading-strategies/">Explore Trading Strategies {ARROW_BTN}</a><a class="btn btn--ghost" href="/community/">Explore the Community Vision</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--text"><h2>Membership FAQ</h2>{L.faq_html(faqs)}
    <div class="mt-2">{L.notice("Leveraged trading and CFDs can result in substantial losses. Membership is educational and does not guarantee results. See our <a href='/risk-disclaimer/'>risk disclaimer</a>.", "risk", "alert")}</div>
  </div>
</section>"""
    return L.page(path="/membership/", title=f"Membership & Trader Levels — Planned {C.PLANNED_PRICE}/month | XAUUSD Global",
                  description=f"XAUUSD Global membership is planned at {C.PLANNED_PRICE}/month with Starter, Advanced, Pro and Degen discussion levels. Registration is opening soon; payments are not open yet.",
                  body=body, crumbs=crumbs)


# --------------------------------------------------------------------------

def about_page():
    crumbs = [("/", "Home"), ("/about/", "About")]
    values = [
        ("users", "Learn together", "Progress is faster when traders compare reasoning and give each other honest feedback."),
        ("compass", "Respect different perspectives", "Structure, liquidity, session and macro traders can all read gold differently — and all learn from each other."),
        ("message", "Explain the reasoning", "An idea without a thesis and an invalidation level isn't analysis; it's a guess."),
        ("shield", "Disciplined risk management", "Protecting capital comes before any target. Risk is part of every conversation."),
        ("info", "Transparency about uncertainty", "We are open about mistakes, losing trades and what we don't know."),
        ("target", "Skill over profit promises", "We build around skill development — never around unrealistic claims of returns."),
    ]
    vcards = "".join(f'<article class="card reveal"><div class="card__icon">{icon(i)}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in values)
    body = f"""{L.page_head(crumbs, 'About <span class="gold-text">XAUUSD Global</span>', 'We are building a global home for gold traders who want to think more clearly, trade more carefully and improve together.', eyebrow='About us')}
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Purpose</span>
        <h2>Why XAUUSD Global exists</h2>
        <p class="lead">Gold is one of the most actively traded markets in the world, and one of the most unforgiving for underprepared traders. Its moves can be fast, news-driven and emotionally demanding.</p>
        <p>Plenty of websites sell signals, and plenty of channels post screenshots of winning trades. Far fewer help traders understand <em>why</em> a setup made sense, how its risk was defined, and what to learn when it failed. XAUUSD Global exists to fill that gap with clear education today and a structured, global community tomorrow.</p>
      </div>
      <div class="reveal">
        <span class="eyebrow">Vision</span>
        <h2>Where we're going</h2>
        <ul class="status-list">
          <li><span class="badge badge--live">Now</span>Free, original education on XAUUSD strategy, risk and market drivers.</li>
          <li><span class="badge badge--soon">Next</span>Community registration, trader levels and structured discussion spaces.</li>
          <li><span class="badge badge--no">Later</span>Member tools such as shared journals, review templates and session-based discussion rooms.</li>
        </ul>
        <p class="mt-2 muted">Plans may change as we learn from traders. We'll update this page as each phase becomes real.</p>
      </div>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Values</span><h2>What we stand for</h2></div>
    <div class="cards cards--3">{vcards}</div>
  </div>
</section>
<section class="section">
  <div class="wrap wrap--text prose">
    <h2 class="mt-0">Who is behind XAUUSD Global</h2>
    <p>XAUUSD Global is an independent project in its early stage. We'll introduce the people behind the site — with real names and verifiable backgrounds — on this page as the community develops. We won't publish invented credentials, trading records, testimonials or member numbers.</p>
    <h2>Our editorial standards</h2>
    <ul>
      <li>Articles are original, educational and written to explain concepts, not to sell outcomes.</li>
      <li>Hypothetical examples are labelled as hypothetical. We do not present illustrations as real trades.</li>
      <li>News is never invented. Until a licensed feed is connected, our news hub contains clearly labelled explainers only.</li>
      <li>Each article shows its publication date and a “last reviewed” field that is only updated when a genuine review takes place.</li>
      <li>We aren't a regulated financial adviser and nothing on this site is personalised advice. See our <a href="/risk-disclaimer/">risk disclaimer</a>.</li>
    </ul>
    <p>Questions or corrections? Visit the <a href="/contact/">contact page</a>.</p>
    {L.community_cta()}
  </div>
</section>"""
    return L.page(path="/about/", title="About XAUUSD Global — Our Mission, Vision & Values",
                  description="About XAUUSD Global: an independent gold trading education site building a global XAUUSD community around shared reasoning, risk discipline and honest review.",
                  body=body, crumbs=crumbs)


# --------------------------------------------------------------------------

def prose_page(meta, body_md, path):
    crumbs = [("/", "Home"), (path, meta["short"])]
    html_body, _ = L.render_md(body_md)
    extra = ""
    if meta.get("draft_notice"):
        extra = f'<div class="mt-2">{L.notice("<strong>Draft — not final.</strong> " + meta["draft_notice"], "", "info")}</div>'
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
