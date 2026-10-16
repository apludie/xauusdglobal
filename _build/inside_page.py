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


def room_stage():
    return """<section class="stage" id="app" aria-label="Interactive preview of the community rooms">
  <div class="stage__inner">
    <div class="float float--a" aria-hidden="true"><span class="fd-live__badge"><i></i>LIVE</span> Daily briefing ready before London</div>
    <div class="float float--b" aria-hidden="true"><b class="fd-r fd-r--win">4.5/5</b> Trade scored by your peers</div>
    <div class="float float--c" aria-hidden="true"><span class="float__ai">XG</span> Your pod posted the Monday plan</div>
    <div class="float float--d" aria-hidden="true"><span class="float__poll"><i style="--w:72%"></i></span> Daily chart challenge: answered</div>
    <div class="app3d">
      <div class="app" data-app>
        <div class="app__bar"><span class="app__dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="app__url">community.xauusdglobal.com</span><span class="app__tag">Interactive preview · sample conversations</span></div>
        <div class="app__body">
          <nav class="app__side" aria-label="Rooms" data-rooms></nav>
          <div class="app__main">
            <header class="app__head"><div><h2 data-room-name># daily-game-plan</h2><p data-room-desc></p></div><span class="app__watch"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 4.6L18 9.5l-4.2 1.9L12 16l-1.8-4.6L6 9.5l4.2-1.9z"/></svg>Mentors in this room</span></header>
            <div class="app__pin" data-pin hidden></div>
            <div class="app__thread" data-thread role="log" aria-live="off"></div>
            <div class="app__typing" data-typing hidden><span class="dots"><i></i><i></i><i></i></span><span data-typing-name></span></div>
            <form class="app__compose" data-compose><label class="sr-only" for="app-msg">Write a message</label><input id="app-msg" type="text" autocomplete="off" placeholder="Ask the mentors anything about gold…"><button class="btn btn--gold btn--sm" type="submit">Send</button></form>
          </div>
          <aside class="app__rail" aria-label="Room details">
            <div class="rail-card rail-card--live"><div class="rail-k"><i></i>LIVE NOW</div><b>NY open + PPI prep</b><span>Live walkthrough with a mentor</span></div>
            <div class="rail-card"><div class="rail-k">ONLINE NOW</div><div class="rail-online" data-online></div></div>
            <div class="rail-card"><div class="rail-k">THIS WEEK'S CHALLENGE</div><b>Only A+ setups, max 3 trades</b><div class="rail-prog"><i style="width:62%"></i></div><span>Your pod's weekly goal</span></div>
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


TOUR = [
    ("briefing", "Today", "Wake up to a plan, not a blank chart.",
     "Every morning the desk writes your gold briefing from live data: what changed overnight, the levels that matter, high-impact news and the scenarios on both sides. Then a six-step routine keeps you consistent: plan, challenge, pod, journal, check-in, learn.",
     ["Automatic daily briefing from live XAU/USD data", "Pre-session checklist and end-of-session recap", "Price alerts and session-open reminders"]),
    ("rooms", "The rooms", "Gold traders from every time zone, in one place.",
     "Mumbai, Dubai, London, Lagos, New York, Singapore: members sit in the same rooms, each with their country flag. Share charts, reply in threads, react, and ask the mentors when you're stuck.",
     ["Rooms for game plans, live sessions, chart reviews, wins and lessons", "Share chart screenshots in a tap", "Clean by design: no paid signals, no DM spam"]),
    ("pod", "Trading pods", "Your own small crew of 5 to 8 traders.",
     "You're matched with traders on your level in your session: Sydney, Tokyo, London or New York. Post your plan on Monday, check in on Wednesday, review the week on Friday. A volunteer host rotates every week.",
     ["Matched by skill floor and session", "Weekly process goals everyone can see", "Accountability that keeps you showing up"]),
    ("review", "Peer reviews", "Get your trades scored on what you control.",
     "Post a trade with your entry, stop, target and reasoning. Members rate it 1 to 5 on plan, execution and risk, and leave written feedback. A well-planned loss can score higher than a lucky win.",
     ["Scores for plan, execution and risk", "Feedback from traders and mentors", "Your average shows exactly what to fix"]),
    ("planner", "Trade planner", "Validate the trade before you click buy or sell.",
     "Enter entry, stop and target. The planner checks reward-to-risk, whether your stop is inside normal volatility, upcoming news, timeframe alignment and nearby liquidity, then gives the plan a quality score.",
     ["Position size rounded down so you never over-risk", "News, volatility and liquidity checks", "Save plans, mark them taken or skipped, log the result"]),
    ("intel", "Market intelligence", "See structure, liquidity and confluence at a glance.",
     "Market structure on 4H, 1H and 15M with every break of structure, liquidity pools and sweeps, a multi-timeframe confluence score, how gold reacts to each US release, and gold against the dollar and yields.",
     ["BOS / CHoCH and swing levels across timeframes", "Liquidity map: untouched, swept and broken levels", "News-impact stats and live correlations"]),
    ("challenge", "Academy", "Learn by doing, every single day.",
     "Short lessons with quizzes, unlimited structure drills and a daily chart challenge: a real moment from gold's history, the same chart for every member, scored by the server. Members also write lessons for the community library.",
     ["Lessons from foundations to structure and liquidity", "Daily chart challenge on real XAU/USD history", "Community library, voted by members"]),
    ("risk", "Risk lab", "Know your drawdowns before the market shows you.",
     "Run 5,000 simulations of your own win rate and R. See typical drawdowns, the odds of losing streaks, risk of ruin, and how much you'd need to recover. Fill it straight from your journal.",
     ["Monte Carlo on your real numbers", "Losing-streak and drawdown odds", "Recovery table for every drawdown"]),
    ("journal", "Journal & mindset", "Track the trader, not just the trades.",
     "Log trades in R in seconds and watch your stats build: win rate, expectancy, profit factor and streaks. A 30-second daily check-in links your mood, sleep and discipline to your results.",
     ["Private journal with R-curve and stats", "Daily mindset and discipline check-in", "See how your state shows up in your P&L"]),
]
ALL = [
    ("Live XAU/USD chart", "Full TradingView chart with drawing tools"), ("Session clock", "Sydney, Tokyo, London and New York, in your time zone"),
    ("Key levels", "Previous day, Asian range and session highs and lows"), ("Economic calendar", "High-impact news with countdown alerts"),
    ("Volatility meter", "ATR across timeframes so you size correctly"), ("Position-size calculator", "Exact lots for your account and stop"),
    ("Daily gold briefing", "Written automatically before London"), ("Market structure", "Breaks of structure on 4H, 1H and 15M"),
    ("Liquidity & sweeps", "Where stops sit and when they get taken"), ("Confluence score", "How many timeframes agree, −100 to +100"),
    ("News impact", "How gold reacted to every US release"), ("Correlations", "Gold against the US dollar and 10-year yields"),
    ("Trade planner", "Score every plan before you trade"), ("Risk lab", "5,000 simulations of your edge"),
    ("Trade journal", "Stats, R-curve and streaks"), ("Mindset tracker", "Mood, sleep and discipline, linked to results"),
    ("Trading pods", "Your crew of 5 to 8 in your session"), ("Peer reviews", "Trades scored on plan, execution and risk"),
    ("Academy", "Lessons, quizzes and structure drills"), ("Daily chart challenge", "One real chart a day, scored for you"),
    ("Community library", "Lessons written by members"), ("Skill floors", "Starter, Advanced, Pro and Mentor's Lab"),
    ("Reputation & badges", "Earned by helping and staying consistent"), ("Install as an app", "On your phone and desktop, alerts included"),
]
FLOORS = [
    ("Starter", "#8fd3ff", "Foundations, gold basics and beginner chart reviews. Everyone starts here."),
    ("Advanced", "#45d6c4", "Pass the exam and keep a 10-day journal streak to unlock analysis and trade breakdowns."),
    ("Pro", "#f2c14e", "Show three detailed trade breakdowns to step into the Pro rooms."),
    ("Mentor's Lab", "#c9a7ff", "The top floor: traders who lead pods, review in depth and help others grow."),
]
COMPARE = [
    ("The trade", "\"BUY GOLD NOW\"", "The reasoning, the levels and what would invalidate the idea"),
    ("Results", "Only the wins get posted", "Every trade logged in R: wins, losses and breakevens"),
    ("Feedback", "Emojis and hype", "Peer scores on plan, execution and risk, with written notes"),
    ("Risk", "Calls without a stop", "Planner, position sizing and a risk lab built in"),
    ("Structure", "One noisy feed", "Rooms by topic, skill floors and a small pod in your session"),
    ("The goal", "Copy someone else", "Build your own edge with a journal, routine and daily practice"),
]


def inside_page():
    path = "/community/inside/"
    crumbs = [("/", "Home"), ("/community/", "Community"), (path, "Look Inside")]
    tour = ""
    for i, (img, k, h, p, pts) in enumerate(TOUR):
        lis = "".join(f"<li>{esc(x)}</li>" for x in pts)
        tour += f"""<div class="tour__row{' tour__row--flip' if i % 2 else ''} reveal">
      <div class="tour__txt"><span class="eyebrow">{esc(k)}</span><h3>{esc(h)}</h3><p>{esc(p)}</p><ul class="checklist">{lis}</ul></div>
      <figure class="tour__shot"><img src="/assets/images/inside/{img}.webp" alt="{esc(k)} screen in the XAUUSD Global community app" loading="lazy" decoding="async"></figure>
    </div>"""
    allg = "".join(f'<div class="incl__i"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in ALL)
    floors = "".join(f'<div class="floor reveal" style="--c:{c}"><span class="floor__n">Floor {i + 1}</span><b>{esc(n)}</b><p>{esc(t)}</p></div>' for i, (n, c, t) in enumerate(FLOORS))
    rows = "".join(f'<tr><th scope="row">{esc(a)}</th><td class="cmp-them">{esc(b)}</td><td class="cmp-us">{esc(c)}</td></tr>' for a, b, c in COMPARE)
    cities = ["Mumbai", "Dubai", "London", "New York", "Singapore", "Karachi", "Lagos", "Johannesburg", "Hong Kong", "Sydney", "Zürich", "Toronto", "Riyadh", "Nairobi", "São Paulo", "Istanbul", "Kuala Lumpur", "Manila"]
    city_html = "".join(f"<span>{esc(c)}</span>" for c in cities)
    faqs = [
        {"q": "What will I get inside the community?", "a": "Everything on this page: the rooms, your trading pod, peer reviews, the trade planner, market intelligence, the academy and daily chart challenge, the risk lab, your journal and mindset tracker, plus the live chart, session clock, key levels and news calendar."},
        {"q": "Do you give buy or sell signals?", "a": "No. We share reasoning, levels and risk, and help you build your own skill. Every idea comes with an invalidation and a stop."},
        {"q": "I'm a beginner. Is it for me?", "a": "Yes. You start on the Starter floor with lessons, a daily routine and a pod of traders at your level. You unlock the next floors as your skill and discipline grow."},
        {"q": "Does it work on my phone?", "a": "Yes. Open it in your browser and install it as an app on your phone or desktop, alerts and reminders included."},
        {"q": "How do I join?", "a": f"[Claim your free month](/membership/#registration). Your first month is free, then it's {C.PLANNED_PRICE}/month. We'll email your personal invitation to the rooms."},
    ]
    body = f"""<section class="inside-hero">
  <div class="wrap center">
    <span class="status-pill status-pill--offer intro" style="--d:0"><span class="dot dot--gold"></span>Look inside · First month free</span>
    <h1 class="inside-title"><span class="ht-l"><span class="ht-in" style="--d:1">Gold traders from</span></span> <span class="ht-l"><span class="ht-in" style="--d:2">every time zone. <em class="serif gold-text">One desk.</em></span></span></h1>
    <p class="hero__lede intro" style="--d:4">XAUUSD Global connects gold traders from all over the world. Plan the session together, trade with a pod that has your back, get your trades scored by peers, and grow with tools built only for gold.</p>
    <div class="btn-row intro" style="--d:5; justify-content:center"><a class="btn btn--gold magnetic" href="/membership/#registration">Claim my free month {ARROW}</a><a class="btn btn--ghost" href="#tour">Take the tour</a></div>
  </div>
</section>

{room_stage()}

<div class="marquee marquee--cities" aria-hidden="true"><div class="marquee__inner">{city_html}{city_html}</div></div>

<section class="section" id="tour">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">The tour</span><h2>Everything a serious gold trader <em class="serif gold-text">needs.</em></h2>
      <p>Real screens from the members' app. Built for learning on the live market, not for copying calls.</p></div>
    <div class="tour">{tour}</div>
    <p class="tour__note">Screens from the community app. Market data is live; member names shown are examples.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split split--mock">
      <div class="reveal"><span class="eyebrow">In your pocket</span><h2>Your trading desk, <em class="serif gold-text">on your phone.</em></h2>
        <p class="lead">Install the community as an app. Your briefing, pod, alerts and journal are one tap away, from the Sydney open to the New York close.</p>
        <ul class="checklist"><li>Session-open reminders and price alerts</li><li>Bottom tab bar made for one hand</li><li>Works on iPhone, Android and desktop</li></ul>
        <a class="btn btn--gold magnetic" href="/membership/#registration">Claim my free month {ARROW}</a></div>
      <div class="phone reveal"><img src="/assets/images/inside/phone.webp" alt="The community app on a phone" loading="lazy" decoding="async"></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">All included</span><h2>24 tools. <em class="serif gold-text">One membership.</em></h2><p>Every member gets every tool, from day one.</p></div>
    <div class="incl reveal">{allg}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">Skill floors</span><h2>The deeper you go, the <em class="serif gold-text">sharper</em> it gets.</h2>
      <p>You don't buy your way up. You climb with skill, discipline and by helping others.</p></div>
    <div class="floors">{floors}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head section-head--center reveal"><span class="eyebrow">Why it's different</span><h2>A Telegram group vs <em class="serif gold-text">our rooms.</em></h2></div>
    <div class="cmp-wrap reveal"><table class="cmp"><thead><tr><th scope="col"><span class="sr-only">Topic</span></th><th scope="col">Typical Telegram group</th><th scope="col">XAUUSD Global</th></tr></thead><tbody>{rows}</tbody></table></div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="offer-stage reveal">
      <div class="coin-wrap" aria-hidden="true"><canvas class="coin3d"></canvas><div class="coin-shadow"></div><div class="coin-fallback">1</div></div>
      {L.offer_box()}
    </div>
    <div class="wrap--text" style="margin:56px auto 0">{L.faq_html(faqs)}</div>
  </div>
</section>
{room_scripts()}
<i hidden data-lazy-js data-src="/assets/js/coin.js" data-when=".coin3d"></i>"""
    return L.page(path=path, title="Look Inside the XAUUSD Global Community",
                  description="Look inside XAUUSD Global: gold traders from every time zone, daily briefings, trading pods, peer-scored trades, a trade planner, an academy and a risk lab.",
                  body=body, crumbs=crumbs, schema_extra=[L.faq_schema(faqs)])
