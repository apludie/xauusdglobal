"""'Look inside the community' showcase page: 3D unfolding app window with a live-simulated room."""
import json, os
import lib as L
import config as C
from lib import esc, icon

HERE = os.path.dirname(os.path.abspath(__file__))
ARROW = icon("arrow")


def _data():
    with open(os.path.join(HERE, "content", "inside.json"), encoding="utf-8") as f:
        return json.load(f)


FEATURES = [
    ("plan", "Daily game plan", "Bias, key levels, session times and the day's news, pinned before London opens."),
    ("recap", "Trade recaps in R", "Entry, stop, exit and result in R-multiples. Wins, losses and breakevens, all logged."),
    ("review", "AI chart reviews", "Post your chart and Goldie checks your reasoning point by point in seconds."),
    ("live", "Live market rooms", "Watch London and New York unfold with mentors, with questions answered as price moves."),
    ("poll", "Bias polls", "See how the room leans into big events, then compare it with what really happened."),
    ("levels", "Levels that unlock", "Starter, Advanced, Pro and Degen rooms open up as your skill and contribution grow."),
]

COMPARE = [
    ("The trade", "\"BUY GOLD NOW\"", "The reasoning, the levels and what would invalidate the idea"),
    ("Results", "Only the wins get posted", "Every recap logged in R: wins, losses and breakevens"),
    ("Questions", "One-way broadcast", "Ask Goldie any time, plus mentors and members in threads"),
    ("Risk", "Calls without a stop", "Every idea comes with a stop and a risk-to-reward"),
    ("Structure", "One noisy feed", "Separate rooms for the plan, live market, reviews and each level"),
    ("The goal", "Copy someone else", "Build your own skill with a journal, checklists and challenges"),
]


def _feature_demo(kind):
    if kind == "plan":
        return ('<div class="fd fd-plan"><div class="fd-row"><span>Structure</span><b>Bearish below 4,150</b></div>'
                '<div class="fd-row"><span>Support</span><b>4,050 · 4,000</b></div><div class="fd-row"><span>Key event</span><b>PPI · 6:00 PM IST</b></div></div>')
    if kind == "recap":
        return ('<div class="fd fd-recap"><div class="fd-recap__top"><span class="fd-dir fd-dir--long">LONG</span><b class="fd-r fd-r--win">+3.3R</b></div>'
                '<div class="fd-recap__grid"><span>Entry<b>4,061</b></span><span>Stop<b>4,048</b></span><span>Exit<b>4,104</b></span></div></div>')
    if kind == "review":
        return ('<ul class="fd fd-checks"><li class="ok">Context: sweep + displacement</li><li class="ok">Invalidation below the sweep</li>'
                '<li class="no">Risk: stop inside the noise</li></ul>')
    if kind == "live":
        return ('<div class="fd fd-live"><span class="fd-live__badge"><i></i>LIVE</span><b>NY open + PPI prep</b><span class="fd-live__eye">87 watching</span></div>')
    if kind == "poll":
        return ('<div class="fd fd-poll"><div class="fd-bar" style="--w:44%"><span>Bearish</span><b>44%</b></div>'
                '<div class="fd-bar" style="--w:33%"><span>Flat</span><b>33%</b></div><div class="fd-bar" style="--w:23%"><span>Bullish</span><b>23%</b></div></div>')
    return ('<div class="fd fd-levels"><span class="lv lv--s">Starter</span><span class="lv lv--a">Advanced</span>'
            '<span class="lv lv--p">Pro <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg></span>'
            '<span class="lv lv--d">Degen <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg></span></div>')


def room_stage():
    return """<section class="stage" id="app" aria-label="Interactive preview of the community rooms">
  <div class="stage__inner">
    <div class="float float--a" aria-hidden="true"><span class="fd-live__badge"><i></i>LIVE</span> NY open session today</div>
    <div class="float float--b" aria-hidden="true"><b class="fd-r fd-r--loss">−1.0R</b> Loss logged, lesson saved</div>
    <div class="float float--c" aria-hidden="true"><span class="float__ai">AI</span> Goldie reviewed your chart</div>
    <div class="float float--d" aria-hidden="true"><span class="float__poll"><i style="--w:44%"></i></span> 212 voted on today's bias</div>
    <div class="app3d">
      <div class="app" data-app>
        <div class="app__bar"><span class="app__dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="app__url">community.xauusdglobal.com</span><span class="app__tag">Interactive preview · sample conversations</span></div>
        <div class="app__body">
          <nav class="app__side" aria-label="Rooms" data-rooms></nav>
          <div class="app__main">
            <header class="app__head"><div><h2 data-room-name># daily-game-plan</h2><p data-room-desc></p></div><span class="app__watch"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 4.6L18 9.5l-4.2 1.9L12 16l-1.8-4.6L6 9.5l4.2-1.9z"/></svg>Goldie is in this room</span></header>
            <div class="app__pin" data-pin hidden></div>
            <div class="app__thread" data-thread role="log" aria-live="off"></div>
            <div class="app__typing" data-typing hidden><span class="dots"><i></i><i></i><i></i></span><span data-typing-name></span></div>
            <form class="app__compose" data-compose><label class="sr-only" for="app-msg">Write a message</label><input id="app-msg" type="text" autocomplete="off" placeholder="Ask Goldie anything about gold trading…"><button class="btn btn--gold btn--sm" type="submit">Send</button></form>
          </div>
          <aside class="app__rail" aria-label="Room details">
            <div class="rail-card rail-card--live"><div class="rail-k"><i></i>LIVE NOW</div><b>NY open + PPI prep</b><span>with Lindiwe · <span data-viewers>87</span> watching</span></div>
            <div class="rail-card"><div class="rail-k">ONLINE NOW</div><div class="rail-online" data-online></div></div>
            <div class="rail-card"><div class="rail-k">THIS WEEK'S CHALLENGE</div><b>Only A+ setups, max 3 trades</b><div class="rail-prog"><i style="width:62%"></i></div><span>62% of members on track</span></div>
            <div class="rail-card"><div class="rail-k">JOURNAL STREAK LEADERS</div><ol class="rail-lead" data-lead></ol></div>
          </aside>
        </div>
      </div>
    </div>
  </div>
</section>"""


def room_scripts():
    payload = json.dumps(_data(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="inside-data">{payload}</script>\n<script src="/assets/js/inside.js" defer></script>'


def inside_page():
    path = "/community/inside/"
    crumbs = [("/", "Home"), ("/community/", "Community"), (path, "Look Inside")]
    d = _data()
    feats = "".join(f'<article class="feat reveal">{_feature_demo(k)}<h3>{esc(t)}</h3><p>{esc(x)}</p></article>' for k, t, x in FEATURES)
    rows = "".join(f'<tr><th scope="row">{esc(a)}</th><td class="cmp-them">{esc(b)}</td><td class="cmp-us">{esc(c)}</td></tr>' for a, b, c in COMPARE)
    cities = ["Mumbai", "Dubai", "London", "New York", "Singapore", "Karachi", "Lagos", "Johannesburg", "Hong Kong", "Sydney", "Zürich", "Toronto", "Riyadh", "Nairobi", "São Paulo", "Istanbul", "Kuala Lumpur", "Manila", "Frankfurt"]
    city_html = "".join(f"<span>{esc(c)}</span>" for c in cities)
    faqs = [
        {"q": "What will I see inside the community?", "a": "Rooms for the daily game plan, live market sessions, chart reviews, trade ideas, wins and lessons, plus level rooms that unlock as you grow. Goldie, the AI mentor, answers questions and reviews your charts any time."},
        {"q": "Who is Goldie?", "a": "Goldie is the community's AI mentor. It explains concepts, reviews the reasoning on your chart, posts the daily game plan and keeps the rooms clean. It never tells you to buy or sell; it helps you build your own judgement."},
        {"q": "How do I join?", "a": f"[Claim your spot](/membership/#registration). The first 50 founding members get the full community free for 3 months, then it's {C.PLANNED_PRICE}/month."},
    ]
    body = f"""<section class="inside-hero">
  <div class="wrap center">
    <span class="status-pill status-pill--offer intro" style="--d:0"><span class="dot dot--gold"></span>Look inside · Founding 50</span>
    <h1 class="inside-title"><span class="ht-l"><span class="ht-in" style="--d:1">Step inside</span></span> <span class="ht-l"><span class="ht-in" style="--d:2">the <em class="serif gold-text">rooms.</em></span></span></h1>
    <p class="hero__lede intro" style="--d:4">This is where gold traders from every time zone plan the day, watch the market live, review each other's charts and learn from every trade, with Goldie, our AI mentor, always on.</p>
    <div class="btn-row intro" style="--d:5; justify-content:center"><a class="btn btn--gold magnetic" href="/membership/#registration">Claim my free spot {ARROW}</a><a class="btn btn--ghost" href="#app">Explore the rooms</a></div>
  </div>
</section>

{room_stage()}

<div class="marquee marquee--cities" aria-hidden="true"><div class="marquee__inner">{city_html}{city_html}</div></div>

<section class="section">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">What you get inside</span><h2>Everything a serious gold trader <em class="serif gold-text">needs.</em></h2>
      <p>Built for learning on the live market, not for copying calls.</p></div>
    <div class="feats">{feats}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">Why it's different</span><h2>A Telegram group vs <em class="serif gold-text">our rooms.</em></h2></div>
    <div class="cmp-wrap reveal"><table class="cmp"><thead><tr><th scope="col"><span class="sr-only">Topic</span></th><th scope="col">Typical Telegram group</th><th scope="col">XAUUSD Global rooms</th></tr></thead><tbody>{rows}</tbody></table></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Meet Goldie</span>
        <h2>Your AI mentor that <em class="serif gold-text">never sleeps.</em></h2>
        <p class="lead">Ask about a fair value gap at 3 AM, post a chart before London, or get the day's plan before your first coffee. Goldie answers in seconds, checks your reasoning and keeps every room clean.</p>
        <ul class="checklist">
          <li>Explains any concept, from basics to ICT and SMC</li>
          <li>Reviews your chart: context, invalidation, risk and timing</li>
          <li>Posts the daily gold game plan before London opens</li>
          <li>Removes spam, scams and "DM me for signals" instantly</li>
        </ul>
      </div>
      <div class="goldie-card reveal" aria-hidden="true">
        <div class="gc-msg gc-msg--me">Is a CHoCH on M15 enough to flip my bias?</div>
        <div class="gc-msg gc-msg--ai"><span class="float__ai">AI</span><div>On its own, rarely. An M15 CHoCH against an H4 downtrend is usually a pullback. Look for displacement, a fair value gap and the higher-timeframe level it formed at. If all three line up, it's worth a plan.</div></div>
        <div class="gc-msg gc-msg--me">So what would make it valid?</div>
        <div class="gc-typing"><span class="dots"><i></i><i></i><i></i></span> Goldie is typing…</div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">Level rooms</span><h2>The deeper you go, the <em class="serif gold-text">sharper</em> it gets.</h2>
      <p>Degen lab and the Mentor circle unlock as you contribute. Here's a glimpse of the conversations waiting for you.</p></div>
    <div class="locked reveal">
      <div class="locked__blur" aria-hidden="true">
        <p><b>rohan_mumbai</b> With 10-year yields at 5.2%, a hike on the 28th is partly priced. The asymmetric trade is a dovish surprise: watch the front-end, not the headline.</p>
        <p><b>weiling_sg</b> Agreed. DXY failed to make a new high while gold swept 4,056. That SMT divergence is the confirmation I want before any long.</p>
        <p><b>aisha_dxb</b> Mitigation block at 4,104 vs the breaker at 4,138: which one do you respect if PPI comes in hot?</p>
      </div>
      <div class="locked__over"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg><b>Mentor circle</b><span>Unlocks as you level up</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="offer-stage reveal">
      <div class="coin-wrap" aria-hidden="true"><canvas class="coin3d"></canvas><div class="coin-shadow"></div><div class="coin-fallback">50</div></div>
      {L.offer_box()}
    </div>
    <div class="wrap--text" style="margin:56px auto 0">{L.faq_html(faqs)}</div>
  </div>
</section>
{room_scripts()}
<i hidden data-lazy-js data-src="/assets/js/coin.js" data-when=".coin3d"></i>"""
    return L.page(path=path, title="Look Inside the XAUUSD Global Community Rooms",
                  description="Step inside the XAUUSD Global rooms: daily gold game plans, live market sessions, AI chart reviews, trade recaps and level rooms. First 50 members get 3 months free.",
                  body=body, crumbs=crumbs, schema_extra=[L.faq_schema(faqs)])
