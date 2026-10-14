"""Gold Market Hours tool page + Tools hub. Times are computed with zoneinfo so DST is exact."""
from datetime import datetime
from zoneinfo import ZoneInfo as Z
import lib as L
import config as C
from lib import esc, icon

SESSIONS = [("sydney", "Sydney", "Australia/Sydney", 7, 16), ("tokyo", "Tokyo", "Asia/Tokyo", 9, 18),
            ("london", "London", "Europe/London", 8, 17), ("newyork", "New York", "America/New_York", 8, 17)]
REGIONS = [
    ("india", "India", "IST", "Asia/Kolkata"), ("uae", "UAE & Dubai", "GST", "Asia/Dubai"),
    ("pakistan", "Pakistan", "PKT", "Asia/Karachi"), ("singapore", "Singapore & Malaysia", "SGT", "Asia/Singapore"),
    ("uk", "United Kingdom", "UK time", "Europe/London"), ("usa", "United States (Eastern)", "ET", "America/New_York"),
    ("nigeria", "Nigeria", "WAT", "Africa/Lagos"), ("south-africa", "South Africa", "SAST", "Africa/Johannesburg"),
]
SUMMER, WINTER = datetime(2026, 7, 15), datetime(2026, 1, 14)


def _t(dt):
    s = dt.strftime("%I:%M %p").lstrip("0").lower()
    return s.replace(":00 ", " ")


def _conv(d, stz, h, tz, wd_shift=0):
    return datetime(d.year, d.month, d.day, h, tzinfo=Z(stz)).astimezone(Z(tz))


def _day(dt):
    return dt.strftime("%a")


def region_rows(tz):
    rows = []
    for _, name, stz, o, c in SESSIONS:
        cells = []
        for d in (SUMMER, WINTER):
            cells.append(f"{_t(_conv(d, stz, o, tz))} – {_t(_conv(d, stz, c, tz))}")
        rows.append((f"{name} session", cells))
    ov = []
    for d in (SUMMER, WINTER):
        ov.append(f"{_t(_conv(d, 'Europe/London', 13, tz))} – {_t(_conv(d, 'Europe/London', 17, tz))}")
    rows.append(("London–New York overlap ✦", ov))
    # weekly open: Sunday 18:00 New York; close: Friday 17:00 New York (Jul 12 2026 = Sun, Jul 17 = Fri; Jan 11 = Sun, Jan 16 = Fri)
    op, cl = [], []
    for sun, fri in ((datetime(2026, 7, 12), datetime(2026, 7, 17)), (datetime(2026, 1, 11), datetime(2026, 1, 16))):
        a = _conv(sun, "America/New_York", 18, tz); b = _conv(fri, "America/New_York", 17, tz)
        op.append(f"{_day(a)} {_t(a)}"); cl.append(f"{_day(b)} {_t(b)}")
    rows.append(("Weekly open", op)); rows.append(("Weekly close", cl))
    return rows


def region_table(tz):
    body = "".join(f'<tr{" class=hl" if "✦" in n else ""}><th scope="row">{esc(n)}</th><td>{a}</td><td>{b}</td></tr>' for n, (a, b) in region_rows(tz))
    return ('<div class="tbl-wrap"><table class="hours-tbl"><thead><tr><th scope="col">Session</th>'
            '<th scope="col">Apr – Oct <small>(US/UK summer time)</small></th><th scope="col">Nov – Mar <small>(US/UK winter time)</small></th></tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


def hours_page():
    path = "/tools/gold-market-hours/"
    crumbs = [("/", "Home"), ("/tools/", "Tools"), (path, "Gold Market Hours")]
    ind = dict((k, region_rows(tz)) for k, _, _, tz in REGIONS)
    lon_ist = ind["india"][2][1]; ny_ist = ind["india"][3][1]; ov_ist = ind["india"][4][1]
    faqs = [
        {"q": "What are gold (XAUUSD) trading hours?", "a": "Spot gold trades almost 24 hours a day, five days a week. The week opens on Sunday at 6 pm New York time and closes on Friday at 5 pm New York time, with a short daily pause around 5–6 pm New York time (the exact break depends on your broker)."},
        {"q": "What is the best time to trade gold?", "a": "Most traders focus on the London–New York overlap, when both major centres are open. It usually brings the most liquidity, the tightest spreads and the biggest moves of the day, especially around US data releases."},
        {"q": "What time does the gold market open in India (IST)?", "a": f"The London session opens at {lon_ist[0].split(' – ')[0]} IST from April to October and {lon_ist[1].split(' – ')[0]} IST from November to March. The New York session opens at {ny_ist[0].split(' – ')[0]} IST in summer and {ny_ist[1].split(' – ')[0]} IST in winter. The London–New York overlap runs {ov_ist[0]} IST in summer and {ov_ist[1]} IST in winter."},
        {"q": "Why do the times change during the year?", "a": "The UK and the US move their clocks forward in spring and back in autumn, on slightly different dates. India, the UAE, Pakistan, Singapore and Nigeria don't use daylight saving, so session times in those countries shift by one hour twice a year. The live clock above always uses today's exact times."},
        {"q": "Is the gold market open on weekends?", "a": "No. Spot gold closes on Friday at 5 pm New York time and reopens on Sunday at 6 pm New York time. Prices can gap at the Sunday open if major news breaks over the weekend."},
    ]
    tz_opts = "".join(f'<option value="{tz}">{esc(n)} ({esc(a)})</option>' for _, n, a, tz in REGIONS)
    extra_tz = [("Asia/Hong_Kong", "Hong Kong"), ("Asia/Tokyo", "Japan"), ("Australia/Sydney", "Sydney"), ("Europe/Berlin", "Central Europe"),
                ("Europe/Zurich", "Switzerland"), ("Asia/Riyadh", "Saudi Arabia"), ("Asia/Dhaka", "Bangladesh"), ("Asia/Kathmandu", "Nepal"),
                ("Asia/Jakarta", "Indonesia"), ("Asia/Manila", "Philippines"), ("Africa/Nairobi", "Kenya"), ("Africa/Cairo", "Egypt"),
                ("America/Chicago", "US Central"), ("America/Los_Angeles", "US Pacific"), ("America/Toronto", "Canada (Toronto)"), ("America/Sao_Paulo", "Brazil")]
    tz_opts += "".join(f'<option value="{tz}">{esc(n)}</option>' for tz, n in extra_tz)
    regions_html = "".join(
        f'<details class="region reveal" id="{k}"{" open" if i == 0 else ""}><summary><span>Gold trading hours in <strong>{esc(n)}</strong></span><small>{esc(a)}</small></summary>{region_table(tz)}</details>'
        for i, (k, n, a, tz) in enumerate(REGIONS))
    sess_cards = "".join(
        f'<article class="sess-card" data-s="{k}"><div class="sess-card__top"><h3>{n}</h3><span class="sess-badge">—</span></div>'
        f'<p class="sess-card__time" data-time>—</p><p class="sess-card__cd" data-cd>—</p></article>' for k, n, _, _, _ in SESSIONS)
    ticks = "".join(f'<span style="left:{h/24*100:.4f}%">{h:02d}</span>' for h in range(0, 24, 3))
    rows = "".join(f'<div class="tl-row" data-row="{k}"><span class="tl-name">{n}</span><div class="tl-track"></div></div>' for k, n, _, _, _ in SESSIONS)
    body = f"""{L.page_head(crumbs, 'Gold Market Hours <span class="gold-text">in Your Time Zone</span>', 'Live XAUUSD trading sessions converted to your local time: see whether gold is open right now, when London and New York open, and the best time to trade gold today.', eyebrow='Free tool · live')}
<section class="section section--tight">
  <div class="wrap">
    <div class="hours" data-hours>
      <div class="hours__top">
        <div class="hours__status">
          <span class="hours__dot" data-dot></span>
          <div><p class="hours__state" data-state>Checking the market…</p><p class="hours__sub" data-sub>&nbsp;</p></div>
        </div>
        <div class="hours__clock">
          <p class="hours__time" data-clock>--:--:--</p>
          <label class="hours__tz"><span class="sr-only">Time zone</span><select class="input" data-tz><option value="auto">Your time zone (auto)</option>{tz_opts}</select></label>
        </div>
      </div>
      <div class="tl" aria-hidden="true">
        <div class="tl-head"><span class="tl-name"></span><div class="tl-ticks">{ticks}</div></div>
        {rows}
        <div class="tl-row tl-row--ov"><span class="tl-name">Overlap ✦</span><div class="tl-track" data-ov></div></div>
        <div class="tl-now" data-now><span>Now</span></div>
      </div>
      <div class="sess-grid">{sess_cards}</div>
      <div class="best">
        <span class="eyebrow">Best time to trade gold today</span>
        <p class="best__time" data-best>—</p>
        <p class="best__note">The London–New York overlap: both major centres open, with the deepest liquidity and the biggest moves. Major US data (CPI, NFP, Fed) usually lands in this window.</p>
      </div>
    </div>
    <p class="hours__fine">Times use conventional session hours and your device clock. Spot gold trades from Sunday 6 pm to Friday 5 pm New York time, with a short daily pause around 5–6 pm New York time; exact hours vary slightly by broker and on public holidays.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Country guide</span><h2>Gold trading hours by <em class="serif gold-text">country.</em></h2>
      <p>Session times for the busiest gold-trading regions, including the shift when the UK and US change their clocks.</p></div>
    <div class="regions">{regions_html}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wrap--text prose">
    <h2>How the gold trading day works</h2>
    <p>Gold is traded around the world, so its day follows the sun. <strong>Asia</strong> opens the week: Sydney, then Tokyo, Hong Kong and Singapore. Moves here are usually calmer, and many traders mark the Asian high and low as the day's first range.</p>
    <p><strong>London</strong> is the centre of the physical gold market, and its open brings a wave of volume. It is common to see the Asian range swept in the first hours of London.</p>
    <p><strong>New York</strong> adds US economic data and the biggest futures market. When London and New York are open together, gold usually sees its deepest liquidity and its sharpest moves of the day.</p>
    <h2>Plan your session</h2>
    <ul>
      <li>Check the <a href="/xauusd-news/">economic calendar</a> before the overlap: CPI, NFP and Fed decisions can move gold by tens of dollars in minutes.</li>
      <li>Size every trade with the <a href="/tools/position-size-calculator/">position size calculator</a>.</li>
      <li>Read the <a href="/strategies/london-session-gold-trading/">London session guide</a> and the <a href="/strategies/new-york-session-gold-trading/">New York session guide</a>.</li>
    </ul>
    <h2 id="faq">Frequently asked questions</h2>
    {L.faq_html(faqs)}
    {L.community_cta()}
  </div>
</section>
<script src="/assets/js/hours.js" defer></script>"""
    app = {"@type": "WebApplication", "name": "Gold Market Hours — XAUUSD session clock", "url": L.canonical(path),
           "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    return L.page(path=path, title="Gold Market Hours Live — XAUUSD Sessions in Your Time Zone",
                  description="Is the gold market open now? Live XAUUSD trading hours in your time zone: London, New York and Asia sessions, the best time to trade gold, plus IST and GST tables.",
                  body=body, crumbs=crumbs, schema_extra=[app, L.faq_schema(faqs)] if hasattr(L, "faq_schema") else [app])


def tools_index():
    path = "/tools/"
    crumbs = [("/", "Home"), (path, "Tools")]
    tools = [
        ("/tools/gold-market-hours/", "clock", "Gold Market Hours", "Is gold open right now? Live sessions in your time zone, with countdowns and the best time to trade today."),
        ("/tools/position-size-calculator/", "scale", "Position Size Calculator", "Turn your balance, risk % and stop-loss into the right XAUUSD lot size, with risk-to-reward."),
        ("/xauusd-price/", "chart", "Live XAUUSD Chart", "A full interactive gold chart with the current session and the factors that move gold."),
        ("/xauusd-news/", "news", "Gold News & Calendar", "Hourly gold headlines plus the economic calendar for CPI, NFP and Fed days."),
    ]
    cards = "".join(f'<a class="card card--link tool-card reveal" href="{p}"><div class="card__icon">{icon(i)}</div><h3>{t}</h3><p>{d}</p><span class="link-arrow">Open {icon("arrow")}</span></a>' for p, i, t, d in tools)
    body = f"""{L.page_head(crumbs, 'Free Gold Trading <span class="gold-text">Tools</span>', 'Everything you need before you place a gold trade: live market hours, lot size, the chart and the calendar. Free, forever.', eyebrow='Tools')}
<section class="section"><div class="wrap"><div class="cards cards--2">{cards}</div><div class="mt-3">{L.community_cta()}</div></div></section>"""
    return L.page(path=path, title="Free Gold Trading Tools — XAUUSD Calculators & Live Market Hours",
                  description="Free XAUUSD trading tools: live gold market hours in your time zone, a gold position size calculator, the live gold chart and the economic calendar.",
                  body=body, crumbs=crumbs)
