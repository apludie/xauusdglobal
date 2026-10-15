"""Hand-designed pages: home, price, news, strategy hub, community, membership,
about, FAQ, legal pages and 404."""
import json
import os

import yaml

import config as C
import lib as L
from mock import chat_mockup
import hours_page as HP
import inside_page as IP
from lib import esc, icon

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")

TITLES = {
    "/": "XAUUSD Global home",
    "/xauusd-price/": "XAUUSD price and live gold chart",
    "/xauusd-news/": "XAUUSD news hub: what moves gold",
    "/xauusd-trading-strategies/": "XAUUSD trading strategies hub",
    "/blog/": "The XAUUSD Global blog",
    "/community/": "Inside the XAUUSD Global community",
    "/membership/": "Membership: first 50 get 3 months free",
    "/about/": "About XAUUSD Global",
    "/tools/gold-market-hours/": "Live gold market hours in your time zone",
    "/tools/": "Free gold trading tools",
    "/community/inside/": "Look inside the community rooms",
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
    return f"""<div class="tool-bands"><a class="tool-band reveal" href="/tools/gold-market-hours/">
      <div class="tool-band__icon">{icon("clock")}</div>
      <div class="tool-band__text"><span class="eyebrow">Free tool · live</span><h3>Gold Market Hours</h3>
        <p>Is gold open right now? Live sessions in your time zone and the best time to trade today.</p></div>
      <span class="btn btn--gold btn--sm">Open market hours {ARROW_BTN}</span></a>
    <a class="tool-band reveal" href="/tools/position-size-calculator/">
      <div class="tool-band__icon">{icon("scale")}</div>
      <div class="tool-band__text"><span class="eyebrow">Free tool</span><h3>XAUUSD Position Size Calculator</h3>
        <p>Enter your balance, risk % and stop-loss — get your gold lot size and risk-to-reward before you trade.</p></div>
      <span class="btn btn--gold btn--sm">Open calculator {ARROW_BTN}</span></a></div>"""


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
    marquee_items = ["London", "New York", "Dubai", "Mumbai", "Singapore", "Hong Kong", "Tokyo", "Sydney", "Zürich", "Johannesburg", "Toronto", "Frankfurt"]
    mq = "".join(f"<span>{esc(t)}</span>" for t in marquee_items * 2)
    mini_cfg = {"symbol": C.TV_SYMBOL, "width": "100%", "height": "100%", "locale": "en", "dateRange": "1D",
                "colorTheme": "dark", "isTransparent": True, "autosize": True, "largeChartUrl": ""}
    faqs = [
        {"q": "Is this a signal group?", "a": "It's much more than that. Trade ideas are shared with their full reasoning — context, thesis, invalidation and risk — so you understand every setup well enough to take action with confidence yourself."},
        {"q": "Who is XAUUSD Global for?", "a": "Mainly intermediate gold traders — people who know some concepts but want to apply them more consistently. Motivated learners and experienced traders who enjoy explaining their thinking are welcome too."},
        {"q": "How do I get 3 months free?", "a": f"The first **50 founding members** get full community access **free for 3 months**. After that it's {C.PLANNED_PRICE}/month. [Claim your spot](/membership/#registration) with your email — it takes 20 seconds."},
        {"q": "Do you sell courses?", "a": "No. We don't sell courses — we teach you on the live market. You learn by watching real gold price action with experienced traders, asking questions in real time and getting feedback on your own charts."},
        {"q": "Who will I learn from?", "a": "Experienced gold traders, mentors and educators from around the world — plus a global network of members who trade the same market as you. Many members find their mentor inside the community."},
        {"q": "Why only gold?", "a": "Gold has its own drivers, sessions and behaviour. Focusing on one market lets discussions go deep and lets traders compare like-for-like analysis on the same chart."},
    ]
    body = f"""
<section class="hero grid-bg hero--home">
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <span class="status-pill status-pill--offer intro" style="--d:0"><span class="dot dot--gold"></span>Founding 50 · 3 months free</span>
      <h1 class="hero__title"><span class="ht-l"><span class="ht-in" style="--d:1">Connect traders</span></span> <span class="ht-l"><span class="ht-in" style="--d:2">around the world.</span></span> <span class="ht-l"><span class="ht-in gold-text" style="--d:3">Trade smarter</span></span> <span class="ht-l ht-l--serif"><span class="ht-in" style="--d:4"><em class="serif gold-text">together.</em></span></span></h1>
      <p class="hero__lede intro" style="--d:5">A global community of gold traders. Learn live on the market with mentors and experienced traders, and connect with XAUUSD traders in every time zone.</p>
      <div class="btn-row intro" style="--d:6">
        <a class="btn btn--gold magnetic" href="/membership/#registration">Claim my free spot {ARROW_BTN}</a>
        <a class="btn btn--ghost btn--inside" href="/community/inside/"><span class="live-dot" aria-hidden="true"></span>Look inside the rooms</a>
      </div>
      <p class="hero__fine intro" style="--d:7">Only 50 founding spots · then {C.PLANNED_PRICE}/month</p>
    </div>
    <div class="hero__visual hero__visual--globe">
      <div class="globe-card">
        <div class="globe-box"><canvas id="globe" class="globe" aria-label="Rotating globe connecting gold trading hubs: London, New York, Zürich, Dubai, Mumbai, Singapore, Hong Kong, Tokyo and Sydney" role="img"></canvas></div>
      </div>
    </div>
  </div>
</section>

<div class="marquee marquee--cities" aria-hidden="true"><div class="marquee__inner">{mq}</div></div>

<section class="showcase" id="rooms" aria-labelledby="rooms-h">
  <div class="wrap center showcase__head">
    <span class="eyebrow reveal">Live preview · click any room</span>
    <h2 id="rooms-h" class="showcase__title reveal">Step inside <em class="serif gold-text">the rooms.</em></h2>
    <p class="lead reveal">This is what you get. Plan the day, get your charts reviewed and ask Goldie anything, with gold traders in every time zone. Click around: it's live.</p>
  </div>
  {IP.room_stage()}
  <div class="wrap center showcase__cta">
    <div class="btn-row" style="justify-content:center"><a class="btn btn--gold magnetic" href="/membership/#registration">Claim my free spot {ARROW_BTN}</a><a class="btn btn--ghost" href="/community/inside/">Take the full tour</a></div>
  </div>
</section>

<section class="section offer-sec">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">Founding 50 · limited spots</span><h2>Your seat in a worldwide room of <em class="serif gold-text">gold traders.</em></h2>
      <p>The first 50 people to join get the full community free for 3 months. Here's what's waiting for you inside.</p></div>
    <div class="offer-stage reveal">
      <div class="coin-wrap" aria-hidden="true"><canvas class="coin3d"></canvas><div class="coin-shadow"></div><div class="coin-fallback">50</div></div>
      {L.offer_box()}
    </div>
    {L.benefits_grid(4)}
    <p class="center mt-3 reveal"><a class="link-arrow" href="/membership/">See everything membership includes {ARROW_BTN}</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Sound familiar?</span><h2>Surrounded by information. Still alone <em class="serif">with the chart?</em></h2>
      <p>You've watched the videos and learned the concepts — structure, liquidity, order blocks, fair value gaps. Then you open your own chart and the same questions come back.</p></div>
    <div class="cards cards--3 qgrid">
      <article class="card q-card reveal"><h3>Is this a genuine breakout, or a liquidity sweep?</h3></article>
      <article class="card q-card reveal"><h3>Why did this setup work yesterday but fail today?</h3></article>
      <article class="card q-card reveal"><h3>Where exactly would my idea be wrong?</h3></article>
      <article class="card q-card reveal"><h3>Is this a high-quality setup, or a trade I just want to take?</h3></article>
      <article class="card q-card reveal"><h3>Who can review my analysis and tell me what I missed?</h3></article>
      <article class="card q-card reveal"><h3>How do I stop relying on other people's calls?</h3></article>
    </div>
    <p class="lead center mt-3 reveal" style="max-width:760px;margin-left:auto;margin-right:auto"><strong>Information is everywhere. A room of traders who'll look at your chart with you is rare.</strong> That's exactly what XAUUSD Global gives you.</p>
  </div>
</section>

<section class="statement" aria-label="Our community">
  <div class="statement__sticky">
    <div class="wrap">
      <span class="eyebrow">One market. One room.</span>
      <p class="statement__text" data-words>Gold never sleeps, and neither does our community. Traders in London, New York, Dubai and Singapore, reading the same chart, sharing what they see, and getting sharper <em class="serif gold-text">together.</em></p>
    </div>
  </div>
</section>


<section class="section">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">The learning journey</span><h2>From collecting concepts to building your own judgement.</h2>
      <p>Six stages, one direction: becoming a confident trader who reads gold on your own — with a whole community cheering you on.</p></div>
    <div class="steps steps--6">
      <div class="step reveal"><span class="tag tag--cyan">Free today</span><h3>Understand</h3><p>Study free guides on XAUUSD, price action, market structure, liquidity, sessions and risk.</p></div>
      <div class="step reveal"><span class="tag tag--cyan">Free today</span><h3>Apply</h3><p>Analyse your own charts, write scenarios and document your reasoning with our planning and journal guides.</p></div>
      <div class="step reveal"><span class="tag">Inside the community</span><h3>Discuss</h3><p>Share your analysis, ask specific questions and compare interpretations with other traders.</p></div>
      <div class="step reveal"><span class="tag">Inside the community</span><h3>Review</h3><p>Break down every trade with mentors and turn each one into a lesson that sharpens your edge.</p></div>
      <div class="step reveal"><span class="tag">Inside the community</span><h3>Improve</h3><p>Turn lessons into a more disciplined, evidence-aware and repeatable process.</p></div>
      <div class="step reveal"><span class="tag">Inside the community</span><h3>Contribute</h3><p>Help others with thoughtful analysis and explanations as your experience grows.</p></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Start here — free</span><h2>Gold trading guides that explain the why.</h2>
      <p>Each guide shows what a framework is, how traders apply it to XAUUSD, and how to use it with confidence.</p></div>
    <div class="cards cards--3">{strat_cards}</div>
    <div class="mt-3"><a class="btn btn--ghost" href="/xauusd-trading-strategies/">Browse all 18 strategy topics {ARROW_BTN}</a></div>
    <div class="mt-3">{tool_band()}</div>
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
  <div class="wrap wrap--text">
    <div class="section-head reveal"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>
    {L.faq_html(faqs)}
    <p class="mt-2"><a href="/faq/">Read all frequently asked questions</a></p>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="cta-3d">
      <canvas id="hero3d" class="hero3d" aria-hidden="true"></canvas>
      {L.community_cta()}
    </div>
  </div>
</section>
{IP.room_scripts()}
<i hidden data-lazy-js data-src="/assets/js/globe.js" data-when="idle"></i>
<i hidden data-lazy-js data-src="/assets/js/coin.js" data-when=".coin3d"></i>
<i hidden data-lazy-js data-src="/assets/js/hero3d.js" data-when="#hero3d"></i>"""
    return L.page(path="/", title="XAUUSD Global — Connect With Gold Traders Around the World",
                  description=f"Join a global community of XAUUSD traders. Learn live on the market with experienced traders and mentors. First 50 members get 3 months free, then {C.PLANNED_PRICE}/month.",
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
    ("yields", "Treasury yields", "layers", "Real (inflation-adjusted) yields represent the return forgone by holding gold. Rising real yields have historically been a headwind for gold and falling real yields a tailwind, although that link has weakened or broken during some periods, including when central-bank buying was strong.", "/blog/what-moves-gold-prices/", "Gold, yields and the Fed"),
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
    body = f"""{L.page_head(crumbs, 'XAUUSD Trading Strategies: <span class="gold-text">How Traders Analyse Gold</span>', 'Eighteen ways traders read the gold market — from support and resistance to Smart Money Concepts, ICT, session timing and risk management. Each topic explains the idea, how it is applied to XAUUSD, and the pro tips that make it work.', eyebrow='Strategy hub')}
<section class="section section--tight">
  <div class="wrap">
    {L.notice("<strong>How to use this hub.</strong> Pick one framework, study it here, then watch it play out on the live gold chart. Inside the community, mentors and experienced traders break these exact setups down in real time.", "info", "info")}
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
        ("users", "Learn from mentors &amp; experienced traders", "Seasoned gold traders and educators share how they read the market — live, as it moves. Find your guru here."),
        ("bolt", "Learn on the live market", "We don't sell courses. Every lesson happens on real, live XAUUSD price action."),
        ("compass", "Compare perspectives", "See how traders using different frameworks read the same price action — and where they disagree."),
        ("journal", "See how plans are built", "Learn how other traders develop, document and review their trade plans."),
        ("message", "Share breakdowns & reviews", "Post chart breakdowns and post-trade reviews for structured feedback."),
        ("shield", "Improve risk habits", "Make position sizing, invalidation and drawdown rules part of every discussion."),
        ("repeat", "Turn every trade into progress", "Break down each trade with the room and walk away sharper every single time."),
        ("layers", "Build a structured process", "Turn scattered ideas into a repeatable process you can measure and refine."),
        ("news", "Reasons to keep coming back", "Daily market discussions, review threads, learning milestones and community challenges keep you growing every week."),
        ("globe", "Global relationships", "Connect in real time with gold traders from every continent — London, New York, Dubai, Mumbai, Singapore and more."),
    ]
    bcards = "".join(f'<article class="card reveal"><div class="card__icon">{icon(i)}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in benefits)
    faqs = [
        {"q": "How do I join?", "a": f"[Claim your spot](/membership/#registration) with your email. The first 50 founding members get the community **free for 3 months**, then it's {C.PLANNED_PRICE}/month. We'll send your invitation to the rooms by email."},
        {"q": "I'm not an experienced trader. Is it for me?", "a": "Absolutely. There's a room for every level, and experienced traders love helping newer traders grow. Every question is welcome."},
        {"q": "Can I disagree with more experienced traders?", "a": "Yes — respectfully, and with your reasoning. Comparing interpretations is one of the main ways people learn here. Challenge the analysis, never the person."},
        {"q": "Will I see real trade ideas?", "a": "Yes — live ideas shared with the full reasoning behind them, so you learn to spot the setups yourself and take action with confidence."},
        {"q": "Who will I meet inside?", "a": "Gold traders from around the world — intermediate traders levelling up, advanced traders refining their edge, and experienced mentors sharing what they know. You'll find your people, and maybe your guru."},
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
    body = f"""{L.page_head(crumbs, 'Bring your charts. Bring your questions. <em class="serif gold-text">Bring your reasoning.</em>', 'A worldwide community of gold traders. Learn live on the market with mentors and experienced traders, connect with XAUUSD traders in every time zone, and grow your skills every day.', eyebrow='The community', extra='<div class="hero__status"><span class="status-pill"><span class="dot dot--gold"></span>Founding 50 · first 50 members get 3 months free</span></div><div class="btn-row mt-2"><a class="btn btn--gold" href="/membership/#registration">Claim my free spot</a><a class="btn btn--ghost" href="/community/inside/">Look inside the rooms</a></div>')}
<section class="section section--tight">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">A look inside</span><h2>A peek inside the rooms</h2>
      <p>One member shares a chart with their reasoning. Others test it from different angles — structure, liquidity, risk. Then the whole room learns from how it plays out.</p></div>
    {chat_mockup()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Why it exists</span>
        <h2>Stop learning alone. Start learning together.</h2>
        <p class="lead">Traders grow fastest when they're surrounded by other traders. One conversation with the right mentor can teach you more than a year of watching videos alone.</p>
        <p>At XAUUSD Global you put your chart next to traders from around the world, ask why, and get real answers — live, while the market is moving.</p>
        <p>Find your mentor. Find your trading partners. Find the room that makes you better.</p>
      </div>
      <div class="reveal">
        <div class="compare">
          <div class="compare__col compare__col--good"><h3>What you get inside</h3><ul><li>Live-market teaching sessions</li><li>Mentors &amp; experienced gold traders</li><li>Chart reviews on your own analysis</li><li>Real-time trade ideas with full reasoning</li><li>Traders from every time zone</li><li>Skills that compound every week</li></ul></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">How ideas are shared</span><h2>Every idea answers seven questions</h2>
      <p>Every trade idea in the rooms covers these seven points — so you don't just see the setup, you understand it and can find the next one yourself.</p></div>
    <div class="cards cards--4">{fcards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">One chart, several perspectives</span><h2>No single trader has every answer</h2>
      <p>Here's how one gold chart gets read by different traders in the room — and why that makes everyone sharper.</p></div>
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
    <div class="section-head reveal"><span class="eyebrow">How the rooms work</span><h2>Real conversations with real gold traders</h2></div>
    <div class="steps">
      <div class="step reveal"><h3>Chart breakdowns</h3><p>Members post an XAUUSD chart with their read of structure, key levels and context.</p></div>
      <div class="step reveal"><h3>Feedback</h3><p>Other traders test the reasoning, point out missed context and offer alternative reads.</p></div>
      <div class="step reveal"><h3>Trade reviews</h3><p>After the trade, the decision, execution and emotions are reviewed — win or loss.</p></div>
      <div class="step reveal"><h3>Level-based rooms</h3><p>Discussion categories for Starter, Advanced, Pro and Degen keep conversations useful at every level.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Membership benefits</span><h2>Everything waiting for you inside</h2>
      <p>One membership. Every room, every session, every mentor.</p></div>
    <div class="cards cards--3">{bcards}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Our culture</span>
        <h2>A community where traders lift each other up</h2>
        <ul class="checklist">
          <li><strong>Share the reasoning.</strong> Every idea comes with its why, so everyone learns.</li>
          <li><strong>Trade like a pro.</strong> Smart sizing and clear risk on every idea.</li>
          <li><strong>Clean, focused rooms.</strong> Pure gold trading — zero spam.</li>
          <li><strong>Grow from every trade.</strong> Each trade becomes a lesson for the whole room.</li>
          <li><strong>Respect every trader.</strong> Different views make everyone sharper.</li>
          <li><strong>Help the next trader.</strong> Today's student is tomorrow's mentor.</li>
        </ul>
      </div>
      <div class="reveal">
        {L.offer_box()}
        <div class="btn-row mt-2"><a class="btn btn--ghost" href="/membership/">See membership details</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Start now for free</span><h2>Warm up before you enter the rooms</h2></div>
    <div class="cards cards--3">
      {card("/strategies/market-structure-xauusd/", "Market structure for XAUUSD", "The shared language most community discussions use.", tag="Guide")}
      {card("/blog/how-to-keep-a-trading-journal/", "How to keep a trading journal", "Start building the review habit that structured feedback depends on.", tag="Blog")}
      {card("/blog/common-mistakes-intermediate-gold-traders/", "Common mistakes intermediate gold traders make", "Level up faster by fixing the habits pros fixed early.", tag="Blog")}
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wrap--text"><h2>Community FAQ</h2>{L.faq_html(faqs)}</div>
</section>"""
    return L.page(path="/community/", title="XAUUSD Trading Community — Learn Gold Trading Together",
                  description="Join a worldwide community of gold traders. Learn live on the market with mentors and connect with XAUUSD traders everywhere. First 50 get 3 months free.",
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
        {"q": "How do I claim a free founding spot?", "a": f"Enter your email in the [form below](#registration) and confirm it. The first 50 founding members get **3 months free**, then {C.PLANNED_PRICE}/month. No card needed to claim your spot."},
        {"q": "Do you sell courses?", "a": "No. We don't sell courses — we teach you on the live market, with mentors and experienced traders, in real time."},
        {"q": "What stays free if I never become a member?", "a": "All guides, the strategy hub, the blog, the live price page and the economic calendar stay free forever. Membership unlocks the community: live sessions, mentors, chart reviews and traders worldwide."},
        {"q": "Does a higher level cost more?", "a": f"No. One membership at {C.PLANNED_PRICE}/month unlocks everything. Levels are earned through your contribution and skill — so you grow into them."},
        {"q": "How will I move between levels?", "a": "You level up by sharing quality analysis, trading with discipline and helping other members. The more you contribute, the higher you climb."},
        {"q": "What happens after my 3 free months?", "a": f"Membership continues at {C.PLANNED_PRICE}/month — one simple price for every room, session and level. You'll always see the price clearly before anything is charged."},
        {"q": "Will I see live trade ideas?", "a": "Yes. Trade ideas are shared in real time with their full reasoning, so you understand the setup and can take action with confidence."},
    ]
    body = f"""{L.page_head(crumbs, 'Membership &amp; <span class="gold-text">Trader Levels</span>', 'Join gold traders from around the world. Learn live on the market with mentors and experienced traders, get your charts reviewed, and find your guru. The first 50 members get 3 months free.', eyebrow='Founding 50 membership')}
<section class="section">
  <div class="wrap">
    <div class="price-hero reveal">
      <div class="coin-wrap coin-wrap--sm" aria-hidden="true"><canvas class="coin3d"></canvas><div class="coin-shadow"></div><div class="coin-fallback">50</div></div>
      <span class="eyebrow">Founding 50 · limited spots</span>
      <div class="price-big"><em class="serif gold-text">Free</em> <small>for 3 months</small></div>
      <p class="lead" style="max-width:660px;margin:16px auto 28px">The first 50 members get the full community free for 3 months. After that, just {C.PLANNED_PRICE}/month. <strong>We don't sell courses — we teach you on the live market.</strong></p>
      <ul class="status-list" style="max-width:560px;margin:0 auto;text-align:left">
        <li><span class="badge badge--live">✓</span>Live-market teaching sessions</li>
        <li><span class="badge badge--live">✓</span>Mentors, educators &amp; experienced gold traders</li>
        <li><span class="badge badge--live">✓</span>Real-time trade ideas and chart reviews</li>
        <li><span class="badge badge--live">✓</span>Connect with gold traders worldwide</li>
        <li><span class="badge badge--live">✓</span>Level rooms: Starter → Advanced → Pro → Degen</li>
      </ul>
      <div class="btn-row mt-3" style="justify-content:center"><a class="btn btn--gold" href="#registration">Claim my free spot {ARROW_BTN}</a></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Free and membership</span><h2>Start free. Level up inside.</h2>
      <p>Learn the foundations on your own for free — then step inside and trade alongside the world.</p></div>
    <div class="cards cards--2">
      <article class="card reveal"><span class="tag tag--cyan">Free · forever</span><h3 style="margin-top:12px">Learn on your own</h3><ul class="checklist">
        <li>11 in-depth XAUUSD strategy guides and the strategy hub</li>
        <li>Blog articles on gold drivers, sessions, risk and psychology</li>
        <li>Live XAUUSD price chart and economic calendar</li>
        <li>Gold news headlines from public sources</li>
        <li>Free trading tools and calculator</li></ul></article>
      <article class="card reveal"><span class="tag">Membership · 3 months free for first 50</span><h3 style="margin-top:12px">Learn live with traders worldwide</h3><ul class="checklist">
        <li>Live-market sessions with mentors and experienced traders</li>
        <li>Real-time trade ideas with the full reasoning</li>
        <li>Your charts and trade plans reviewed</li>
        <li>Connect with gold traders in every time zone</li>
        <li>Level rooms from Starter to Degen</li>
        <li>Find your mentor, your trading guru</li></ul></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Trader levels</span><h2>Four levels. Keep climbing.</h2>
      <p>Every level opens new rooms, deeper discussions and new people to learn from.</p></div>
    <div class="tiers">{tier_html}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">How you level up</span>
        <h2>Earned through skill and contribution</h2>
        <p>Your level grows as you grow. Here's what moves you up:</p>
        <ul class="checklist">
          <li><strong>Analytical quality</strong> — clear theses with context, confluence and invalidation.</li>
          <li><strong>Risk awareness</strong> — consistent position sizing and respect for stops.</li>
          <li><strong>Trade reviews</strong> — sharing what each trade taught you.</li>
          <li><strong>Meaningful contributions</strong> — feedback that helps other members improve.</li>
        </ul>
      </div>
      <div class="reveal">
        <h2>What you get as a member</h2>
        <ul class="checklist">
          <li><strong>Live-market teaching</strong> — we don't sell courses, we teach you on real gold price action.</li>
          <li><strong>Mentors &amp; gurus</strong> — experienced traders and educators who share their knowledge and skills.</li>
          <li><strong>A global network</strong> — connect in real time with gold traders from everywhere in the world.</li>
          <li><strong>Real-time trade ideas</strong> — setups with full reasoning, so you can take action with confidence.</li>
          <li><strong>Chart reviews</strong> — feedback on your own analysis from traders at the next level.</li>
          <li><strong>Daily gold game plan</strong> — key levels, sessions and news before the market moves.</li>
        </ul>
        <p class="cta-sign">See you in the community rooms soon. ✦</p>
      </div>
    </div>
  </div>
</section>

<section class="section" id="registration">
  <div class="wrap">
    <div class="waitlist reveal">
      <div class="waitlist__intro">
        <span class="eyebrow">Founding 50 · spots are limited</span>
        <h2>Claim your free spot</h2>
        <p class="lead">The first 50 members get the full XAUUSD Global community <strong>free for 3 months</strong> — then just {C.PLANNED_PRICE}/month.</p>
        <ul class="checklist">
          <li><strong>Learn on the live market</strong> with mentors and experienced gold traders.</li>
          <li><strong>Connect with traders worldwide</strong> — the rooms are open in every time zone.</li>
          <li><strong>Find your guru</strong> and grow your skills every week.</li>
        </ul>
        <p class="cta-sign">See you in the community rooms soon. ✦</p>
      </div>
      <div class="waitlist__card">
        <div class="sib-form">
          <div id="sib-form-container" class="sib-form-container">
            <div id="error-message" class="sib-form-message-panel waitlist__msg waitlist__msg--error" role="alert">
              <div class="sib-form-message-panel__text"><span class="sib-form-message-panel__inner-text">Sorry, we couldn't save your details. Please check your email address and try again.</span></div>
            </div>
            <div id="success-message" class="sib-form-message-panel waitlist__msg waitlist__msg--ok" role="status">
              <div class="sib-form-message-panel__text"><span class="sib-form-message-panel__inner-text"><strong>You're on the list! 🎉</strong> Your founding spot is reserved. Taking you to your welcome page…</span></div>
            </div>
            <div id="sib-container" class="sib-container--large sib-container--vertical">
              <form id="sib-form" method="POST" action="{C.BREVO_FORM_ACTION}" data-type="subscription">
                <h3 class="waitlist__title">Claim your founding spot</h3>
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
                    Claim my free spot
                  </button>
                </div>
                <p class="waitlist__legal">By joining, you agree to receive emails from XAUUSD Global about the community. We'll send a quick confirmation email first. Unsubscribe anytime. See our <a href="/privacy-policy/">Privacy Policy</a>.</p>
                <input type="text" name="email_address_check" value="" class="input--hidden" tabindex="-1" autocomplete="off" aria-hidden="true">
                <input type="hidden" name="locale" value="en">
              </form>
            </div>
          </div>
        </div>
        <noscript><p class="waitlist__legal">Please enable JavaScript to claim your free spot, or email us at {C.CONTACT_EMAIL}.</p></noscript>
      </div>
    </div>
    <div class="btn-row mt-3" style="justify-content:center"><a class="btn btn--ghost" href="/xauusd-trading-strategies/">Explore trading strategies {ARROW_BTN}</a><a class="btn btn--ghost" href="/community/">See inside the community</a></div>
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
  <script>
  /* Backup: every sign-up is also emailed instantly to the owner, so no lead is lost if the provider is slow. */
  (function () {{
    var f = document.getElementById("sib-form"); if (!f) return;
    f.addEventListener("submit", function () {{
      try {{
        var em = ((f.querySelector("#EMAIL") || {{}}).value || "").trim(), fn = ((f.querySelector("#FIRSTNAME") || {{}}).value || "").trim();
        if (!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(em)) return;
        fetch("https://formsubmit.co/ajax/{C.CONTACT_EMAIL}", {{
          method: "POST", headers: {{ "Content-Type": "application/json", "Accept": "application/json" }},
          body: JSON.stringify({{ _subject: "New Founding 50 sign-up: " + em, email: em, first_name: fn, page: location.href, _template: "table", _captcha: "false" }})
        }}).catch(function () {{}});
      }} catch (e) {{}}
    }}, true);
    var ok = document.getElementById("success-message");
    if (ok && "MutationObserver" in window) {{
      new MutationObserver(function () {{
        if (ok.offsetParent !== null || getComputedStyle(ok).display !== "none") setTimeout(function () {{ location.href = "/waitlist-confirmed/"; }}, 1400);
      }}).observe(ok, {{ attributes: true, attributeFilter: ["style", "class"] }});
    }}
  }})();
  </script>
</section>

<section class="section section--alt">
  <div class="wrap wrap--text"><h2>Membership FAQ</h2>{L.faq_html(faqs)}
  </div>
</section>
<i hidden data-lazy-js data-src="/assets/js/coin.js" data-when=".coin3d"></i>"""
    return L.page(path="/membership/", title="Membership — First 50 Get 3 Months Free | XAUUSD Global",
                  description=f"Join the XAUUSD Global gold trading community. First 50 members get 3 months free, then {C.PLANNED_PRICE}/month. Learn live on the market with mentors and traders worldwide.",
                  body=body, crumbs=crumbs)


# --------------------------------------------------------------------------

def about_page():
    crumbs = [("/", "Home"), ("/about/", "About")]
    values = [
        ("message", "Live, real, practical", "We don't sell courses. We teach on the live market, where real skill is built."),
        ("compass", "Become your own trader", "We teach you to read gold yourself, so you trade with confidence and conviction."),
        ("users", "Many perspectives", "Structure, liquidity, session and macro traders read gold differently. Comparing them is how blind spots show up."),
        ("shield", "Trade like a pro", "Smart risk on every trade — the habit every great trader shares."),
        ("globe", "One global room", "Gold trades around the clock, and so does our community. Traders from every continent, learning together."),
        ("target", "Skill that compounds", "Every session, every review and every conversation adds to your edge. Small gains in skill, week after week."),
    ]
    vcards = "".join(f'<article class="card reveal"><div class="card__icon">{icon(i)}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in values)
    gaps = [
        ("Turn videos into skill", "A tutorial can introduce order blocks or liquidity in ten minutes. Applying them to a live gold chart — and knowing when they don't apply — takes practice, follow-up questions and feedback.",
         "We pair free guides with discussion, so concepts get tested on real charts."),
        ("Understand the reasoning, not just the signal", "A buy or sell call gives you an entry, but not the structure behind it or what would make it wrong. When the provider disappears or conditions change, you're left without a framework.",
         "We focus on the reasoning behind an idea, so you can judge the next one yourself."),
        ("Find the right mentor", "Specific questions deserve thoughtful, specific answers — from traders who have been there.",
         "Our rooms are a space where careful questions and respectful debate are the norm."),
        ("Too many conflicting systems", "One person teaches one method, another says it's useless, a third claims to have the only strategy that works. Many traders spend years switching.",
         "We help you evaluate ideas by evidence, context and risk — and build a process that fits you."),
        ("Screenshots hide the full story", "A winning screenshot doesn't show the risk taken, the losing trades around it, or whether the approach is repeatable.",
         "We encourage reviews of reasoning, invalidation, risk and mistakes — not just outcomes."),
    ]
    gcards = "".join(f'<article class="card reveal"><div class="card__num">{n:02d}</div><h3>{t}</h3><p>{d}</p><p class="gap__fix"><strong>Our approach:</strong> {f}</p></article>' for n, (t, d, f) in enumerate(gaps, 1))
    body = f"""{L.page_head(crumbs, 'Why <span class="gold-text">XAUUSD Global</span> exists', 'We connect gold traders around the world so they can learn live on the market, find their mentors and trade smarter together.', eyebrow='About us')}
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
        <h2>We help you become your own trader.</h2>
        <p class="lead">Learn live with mentors and traders worldwide until you read gold with real confidence.</p>
        <ul class="checklist">
          <li>Read price action and market structure in context.</li>
          <li>Build a clear thesis — and define what would invalidate it.</li>
          <li>Size positions and set stops before the trade, not during it.</li>
          <li>Recognise revenge trading, overtrading and confirmation bias.</li>
          <li>Turn every trade into a lesson that sharpens your edge.</li>
          <li>Trade with calm, confident discipline.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">What we do differently</span><h2>Five ways we help traders break through</h2>
      <p>Here's what traders tell us they were missing — and how the XAUUSD Global community gives it to them.</p></div>
    <div class="cards cards--3">{gcards}</div>
  </div>
</section>
<section class="section">
  <div class="wrap wrap--text prose">
    <h2 class="mt-0">Where we fit</h2>
    <p>We don't sell courses — <strong>we teach you on the live market</strong>. XAUUSD Global connects gold traders, mentors and experienced educators from around the world in one continuing community, focused on a single market. Inside, you learn to answer the questions that separate pros from everyone else:</p>
    <ul>
      <li>Why might it move there, and what evidence supports that?</li>
      <li>Where exactly is the smart entry — and the smart exit?</li>
      <li>How do I size this trade like a pro?</li>
      <li>How do I turn this trade into a lesson for the next one?</li>
    </ul>
    <blockquote class="pull">Find your mentor. Find your people. Grow into the trader you want to be — together.</blockquote>
    <p><strong>The community is the room. The live market is the classroom. Traders around the world are your classmates.</strong></p>
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
        <span class="eyebrow">Your journey</span>
        <h2>Great traders are made together</h2>
        <p class="lead">Many people come to trading for more independence and control over their future. That ambition is powerful — and we're here to fuel it.</p>
        <p>The fastest path is practice with the right people around you: mentors who've been there, traders who challenge you, and a community that celebrates your progress.</p>
        <p>That's what we build with you: <strong>knowledge, sharp skills, discipline and real confidence in your own process</strong>.</p>
      </div>
      <div class="reveal">
        <span class="eyebrow">Join us if…</span>
        <h2>This is for you if you want to</h2>
        <ul class="checklist">
          <li>Understand why gold moves, not just where someone says it will go.</li>
          <li>Stop jumping between strategies and build one process you trust.</li>
          <li>Ask detailed questions without feeling foolish.</li>
          <li>Have your analysis challenged — and challenge others respectfully.</li>
          <li>Connect with gold traders from all over the world.</li>
        </ul>
        <p><a class="btn btn--gold" href="/membership/#registration">Claim my free spot {ARROW_BTN}</a></p>
      </div>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">What's inside</span>
        <h2>Everything a gold trader needs, in one place</h2>
        <ul class="status-list">
          <li><span class="badge badge--live">Free</span>Guides on XAUUSD strategy, risk, sessions and market drivers.</li>
          <li><span class="badge badge--live">Free</span>Gold news hub, economic calendar and trading calculator.</li>
          <li><span class="badge badge--soon">Members</span>Live-market sessions, mentors, chart reviews and global trader rooms.</li>
          <li><span class="badge badge--soon">Founding 50</span>First 50 members get 3 months free, then {C.PLANNED_PRICE}/month.</li>
        </ul>
      </div>
      <div class="reveal">
        <span class="eyebrow">Our promise to you</span>
        <h2>Our commitments</h2>
        <ul class="checklist">
          <li>Teach you on the live market, in real time.</li>
          <li>Connect you with experienced traders and mentors worldwide.</li>
          <li>Share every idea with its full reasoning.</li>
          <li>Keep every guide on this site free forever.</li>
          <li>Keep the rooms welcoming, focused and pure gold.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap wrap--text prose">
    <h2 class="mt-0" id="founder">Who is behind XAUUSD Global</h2>
    <p>XAUUSD Global is an independent project focused entirely on gold. Built by gold traders, for gold traders — with one mission: connect traders around the world and help every one of them trade smarter. A full founder profile is coming soon.</p>
    <h2 id="editorial-standards">Our editorial standards</h2>
    <ul>
      <li>Articles are original and written to explain how traders think about gold, not to sell outcomes.</li>
      <li>Hypothetical examples are labelled as hypothetical. Real market examples will always carry a date.</li>
      <li>News is never invented. Headlines are credited to and linked to the original publisher.</li>
      <li>Each article shows its publication date. A “last reviewed” date appears only after a genuine review.</li>
      <li>Corrections are welcome — email <a href="mailto:{C.CONTACT_EMAIL}">{C.CONTACT_EMAIL}</a> with the page and the issue.</li>
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
    """Thank-you page shown right after a successful sign-up."""
    body = f"""<section class="hero grid-bg">
  <div class="wrap wrap--text center">
    <div class="confirm-badge" aria-hidden="true">{icon("shield")}</div>
    <span class="eyebrow">Founding spot · Reserved</span>
    <h1>Thank you. <span class="gold-text">You're on the list.</span></h1>
    <p class="hero__lede" style="margin-left:auto;margin-right:auto">Your Founding 50 spot is reserved: 3 months free when the rooms open. Your invitation will arrive by email from info@xauusdglobal.com. Warm up with the free guides in the meantime. See you in the community rooms soon!</p>
    <div class="btn-row" style="justify-content:center"><a class="btn btn--gold" href="/xauusd-trading-strategies/">Explore trading strategies {ARROW_BTN}</a><a class="btn btn--ghost" href="/community/">See inside the community</a></div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="section-head section-head--center"><span class="eyebrow">What happens next</span><h2>Three things to know</h2></div>
    <div class="steps" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">
      <div class="step"><h3>Watch your inbox</h3><p>Your invitation comes from <strong>info@xauusdglobal.com</strong>. Add it to your contacts so you never miss a message.</p></div>
      <div class="step"><h3>Founding 50 offer</h3><p>The first 50 members get 3 months free, then {C.PLANNED_PRICE}/month. You\'ll see everything clearly before anything is charged.</p></div>
      <div class="step"><h3>Unsubscribe anytime</h3><p>Every email includes a one-click unsubscribe link. Read how we handle your details in our <a href="/privacy-policy/">Privacy Policy</a>.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Start learning while you wait</span><h2>Popular guides</h2></div>
    <div class="cards cards--3">
      {card("/strategies/market-structure-xauusd/", "XAUUSD market structure", "The shared language most community discussions use: swings, BOS and CHoCH.", tag="Guide")}
      {card("/strategies/xauusd-risk-management/", "Risk management & position sizing", "Size gold positions from your stop distance and protect your account.", tag="Guide")}
      {card("/blog/how-to-keep-a-trading-journal/", "How to keep a trading journal", "Build the review habit that structured community feedback depends on.", tag="Blog")}
    </div>
  </div>
</section>"""
    return L.page(path="/waitlist-confirmed/", title="Your Founding Spot Is Confirmed | XAUUSD Global",
                  description="Your XAUUSD Global founding spot request is confirmed.", body=body, noindex=True)


def not_found():
    body = f"""<section class="hero grid-bg"><div class="wrap wrap--text center">
  <span class="eyebrow">Error 404</span>
  <h1>This level didn't hold.</h1>
  <p class="hero__lede" style="margin-left:auto;margin-right:auto">The page you were looking for doesn't exist or has moved. Here are some useful places to continue:</p>
  <div class="btn-row" style="justify-content:center"><a class="btn btn--gold" href="/">Back to the homepage</a><a class="btn btn--ghost" href="/xauusd-trading-strategies/">Trading strategies</a></div>
  <div class="related" style="text-align:left"><ul>
    <li><a href="/xauusd-price/">XAUUSD price and chart</a></li>
    <li><a href="/blog/">Gold trading blog</a></li>
    <li><a href="/community/">Community</a></li>
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
    <p class="muted mt-2" style="font-size:.9rem">Lots are rounded <strong>down</strong> to 0.01 so you never risk more than you chose. Tip: leave a little extra room for spread and commission, especially around big news releases.</p>
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
        ("/tools/gold-market-hours/", HP.hours_page(), "0.9"),
        ("/tools/", HP.tools_index(), "0.7"),
        ("/community/inside/", IP.inside_page(), "0.9"),
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
