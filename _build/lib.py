"""Shared building blocks: layout, SEO head, icons, diagrams, markdown."""
import datetime as _dt
import html
import json
import math
import random
import re

import markdown
import os
import yaml

import config as C

# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def esc(s):
    return html.escape(str(s), quote=True)


def canonical(path):
    return C.SITE_URL + path


def fmt_date(iso):
    d = _dt.date.fromisoformat(iso)
    return d.strftime("%-d %B %Y")


def reading_minutes(text):
    words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", text)))
    return max(1, round(words / 220))


# --------------------------------------------------------------------------
# Icons (original, stroke-based)
# --------------------------------------------------------------------------

_ICON_PATHS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chart": '<path d="M4 19V5M4 19h16"/><path d="M8 15l3-4 3 2 5-7"/>',
    "candles": '<path d="M7 4v16M17 4v16"/><rect x="5" y="8" width="4" height="7" rx="1"/><rect x="15" y="6" width="4" height="9" rx="1"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 19c.8-3 3-4.6 5.5-4.6s4.7 1.6 5.5 4.6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.6c2.2.1 3.9 1.5 4.5 4.4"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.3-3 7.6-7 9-4-1.4-7-4.7-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 016.5 3H20v15H6.5A2.5 2.5 0 004 20.5v-15z"/><path d="M4 20.5A2.5 2.5 0 016.5 18H20v3H6.5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "news": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 8h10M7 12h10M7 16h6"/>',
    "journal": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 7h6M9 11h6M9 15h4"/>',
    "alert": '<path d="M12 3l9.5 17H2.5L12 3z"/><path d="M12 10v4M12 17.5v.01"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.5v.01"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
    "scale": '<path d="M12 3v18M5 21h14"/><path d="M5 7h14"/><path d="M5 7l-3 7a3.5 3.5 0 006 0L5 7zM19 7l-3 7a3.5 3.5 0 006 0l-3-7z"/>',
    "message": '<path d="M4 5h16v11H9l-5 4V5z"/><path d="M8 9h8M8 12h5"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
    "lock": '<rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 018 0v3"/>',
    "repeat": '<path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 013-3h15M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 01-3 3H3"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            f'{_ICON_PATHS[name]}</svg>')


LOGO_SVG = (
    '<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false">'
    '<defs><linearGradient id="lg-g" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#ffe08a"/><stop offset=".5" stop-color="#f2c14e"/><stop offset="1" stop-color="#b8862b"/>'
    '</linearGradient></defs>'
    '<rect x="2" y="2" width="60" height="60" rx="16" fill="#111318" stroke="url(#lg-g)" stroke-width="2"/>'
    '<path d="M18 18l28 28M46 18L18 46" stroke="url(#lg-g)" stroke-width="5" stroke-linecap="round"/>'
    '<circle cx="32" cy="32" r="21" fill="none" stroke="#f2c14e" stroke-opacity=".28" stroke-width="1.5"/>'
    '<rect x="28.5" y="24" width="7" height="16" rx="1.6" fill="#111318" stroke="#45d6c4" stroke-width="1.8"/>'
    '<path d="M32 19v5M32 40v5" stroke="#45d6c4" stroke-width="1.8" stroke-linecap="round"/>'
    '</svg>'
)


# --------------------------------------------------------------------------
# Diagram engine: original candlestick schematics (hypothetical data)
# --------------------------------------------------------------------------

_COL = {
    "gold": "#f2c14e", "cyan": "#45d6c4", "red": "#ef6a5b", "green": "#3ccf91",
    "muted": "#8a8983", "white": "#f3f1ea", "orange": "#e8794f",
}


def _synth_candles(spec):
    """Build OHLC candles from waypoints with deterministic noise."""
    rng = random.Random(spec.get("seed", 7))
    pts = spec["path"]
    n = pts[-1][0] + 1
    vol = spec.get("vol", 1.0)
    targets = []
    for k in range(len(pts) - 1):
        (i0, p0), (i1, p1) = pts[k], pts[k + 1]
        for i in range(i0, i1):
            t = (i - i0) / (i1 - i0)
            targets.append(p0 + (p1 - p0) * t)
    targets.append(pts[-1][1])
    candles = []
    prev = targets[0] - (targets[1] - targets[0]) * 0.6 if n > 1 else targets[0]
    for i in range(n):
        o = prev
        c = targets[i] + rng.uniform(-0.35, 0.35) * vol
        body_top, body_bot = max(o, c), min(o, c)
        h = body_top + rng.uniform(0.15, 0.9) * vol
        l = body_bot - rng.uniform(0.15, 0.9) * vol
        candles.append([o, h, l, c])
        prev = c
    for idx, ov in (spec.get("override") or {}).items():
        idx = int(idx)
        for k, key in enumerate("ohlc"):
            if key in ov:
                candles[idx][k] = ov[key]
        o, h, l, c = candles[idx]
        candles[idx][1] = max(h, o, c)
        candles[idx][2] = min(l, o, c)
        if idx + 1 < n and "c" in ov and "keep_next" not in ov:
            nxt = candles[idx + 1]
            nxt[0] = c
            nxt[1] = max(nxt[1], c, nxt[3])
            nxt[2] = min(nxt[2], c, nxt[3])
    return candles


def chart_svg(spec, title):
    W, H = 760, 400
    padL, padR, padT, padB = 14, 96, 22, 26
    candles = _synth_candles(spec)
    n = len(candles)
    lows = [c[2] for c in candles]
    highs = [c[1] for c in candles]
    extra = []
    for z in spec.get("zones", []):
        extra += [z["y1"], z["y2"]]
    for ln in spec.get("lines", []):
        extra.append(ln["y"])
    for m in spec.get("marks", []):
        if "y" not in m:  # snap to the candle's extreme
            c = candles[m["i"]]
            m["y"] = c[2] if m.get("pos", "above") == "below" else c[1]
        extra.append(m["y"])
    lo, hi = min(lows + extra), max(highs + extra)
    span = hi - lo or 1
    lo -= span * 0.08
    hi += span * 0.1
    plotW, plotH = W - padL - padR, H - padT - padB
    step = plotW / n

    def X(i):
        return padL + step * (i + 0.5)

    def Y(p):
        return padT + (hi - p) / (hi - lo) * plotH

    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="t-{spec["id"]}" '
           f'xmlns="http://www.w3.org/2000/svg" font-family="ui-monospace, Menlo, monospace">'
           f'<title id="t-{spec["id"]}">{esc(title)}</title>'
           f'<rect width="{W}" height="{H}" rx="10" fill="#0d0f12"/>']
    # grid
    gl = 6
    for k in range(gl + 1):
        y = padT + plotH * k / gl
        out.append(f'<line x1="{padL}" x2="{W - padR + 6}" y1="{y:.1f}" y2="{y:.1f}" stroke="#ffffff" stroke-opacity=".05"/>')
        price = hi - (hi - lo) * k / gl
        if spec.get("axis", True):
            out.append(f'<text x="{W - padR + 12}" y="{y + 4:.1f}" font-size="11" fill="#6f6e69">{price:,.1f}</text>')
    for k in range(1, 8):
        x = padL + plotW * k / 8
        out.append(f'<line y1="{padT}" y2="{H - padB}" x1="{x:.1f}" x2="{x:.1f}" stroke="#ffffff" stroke-opacity=".035"/>')
    # zones
    for z in spec.get("zones", []):
        col = _COL[z.get("color", "gold")]
        x1 = X(z.get("x1", 0)) - step / 2 if "x1" in z else padL
        x2 = X(z.get("x2", n - 1)) + step / 2 if "x2" in z else W - padR
        y1, y2 = Y(max(z["y1"], z["y2"])), Y(min(z["y1"], z["y2"]))
        out.append(f'<rect x="{x1:.1f}" y="{y1:.1f}" width="{x2 - x1:.1f}" height="{max(2, y2 - y1):.1f}" '
                   f'fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".55" stroke-dasharray="4 3"/>')
        if z.get("label"):
            ly = y1 - 6 if z.get("label_pos", "top") == "top" else y2 + 14
            out.append(f'<text x="{x1 + 6:.1f}" y="{ly:.1f}" font-size="11.5" fill="{col}" font-weight="600">{esc(z["label"])}</text>')
    # lines
    for ln in spec.get("lines", []):
        col = _COL[ln.get("color", "gold")]
        y = Y(ln["y"])
        x1 = X(ln["x1"]) if "x1" in ln else padL
        x2 = X(ln["x2"]) if "x2" in ln else W - padR
        dash = ' stroke-dasharray="6 5"' if ln.get("dash", True) else ""
        out.append(f'<line x1="{x1:.1f}" x2="{x2:.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="1.4"{dash}/>')
        if ln.get("label"):
            lx = x1 + 6 if ln.get("label_at") == "start" else x2 - 6
            anchor = "start" if ln.get("label_at") == "start" else "end"
            ly = y - 7 if ln.get("label_side", "above") == "above" else y + 16
            out.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="11.5" text-anchor="{anchor}" fill="{col}" font-weight="600">{esc(ln["label"])}</text>')
    # polyline (e.g. structure path)
    for pl in spec.get("polylines", []):
        col = _COL[pl.get("color", "cyan")]
        pts = " ".join(f"{X(i):.1f},{Y(p):.1f}" for i, p in pl["pts"])
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="1.6" stroke-opacity=".85" stroke-dasharray="2 4"/>')
    # candles
    bw = max(3.0, step * 0.58)
    for i, (o, h, l, c) in enumerate(candles):
        up = c >= o
        col = "#3ccf91" if up else "#ef6a5b"
        hl = (spec.get("highlight") or [])
        stroke_extra = ' stroke="#f2c14e" stroke-width="1.6"' if i in hl else ""
        x = X(i)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(h):.1f}" y2="{Y(l):.1f}" stroke="{col}" stroke-width="1.3"/>')
        top, bot = Y(max(o, c)), Y(min(o, c))
        out.append(f'<rect x="{x - bw / 2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{max(1.4, bot - top):.1f}" '
                   f'fill="{col}" fill-opacity="{0.9 if up else 0.85}" rx="1"{stroke_extra}/>')
    # marks
    for m in spec.get("marks", []):
        col = _COL[m.get("color", "gold")]
        x, y = X(m["i"]), Y(m["y"])
        pos = m.get("pos", "above")
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}" stroke="#0d0f12" stroke-width="1.5"/>')
        dy = -14 if pos == "above" else 22
        anchor = m.get("anchor", "middle")
        out.append(f'<text x="{x:.1f}" y="{y + dy:.1f}" font-size="11.5" text-anchor="{anchor}" fill="{col}" font-weight="700">{esc(m["label"])}</text>')
    # arrows
    for a in spec.get("arrows", []):
        col = _COL[a.get("color", "white")]
        (i1, p1), (i2, p2) = a["from"], a["to"]
        x1, y1, x2, y2 = X(i1), Y(p1), X(i2), Y(p2)
        ang = math.atan2(y2 - y1, x2 - x1)
        hx1 = x2 - 9 * math.cos(ang - 0.45)
        hy1 = y2 - 9 * math.sin(ang - 0.45)
        hx2 = x2 - 9 * math.cos(ang + 0.45)
        hy2 = y2 - 9 * math.sin(ang + 0.45)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="1.6" stroke-opacity=".9"/>'
                   f'<path d="M{hx1:.1f},{hy1:.1f} L{x2:.1f},{y2:.1f} L{hx2:.1f},{hy2:.1f}" fill="none" stroke="{col}" stroke-width="1.6"/>')
    out.append(f'<text x="{padL + 6}" y="{H - 8}" font-size="10.5" fill="#6f6e69">HYPOTHETICAL DATA · ILLUSTRATION ONLY · NOT A REAL XAUUSD CHART</text>')
    out.append("</svg>")
    return "".join(out)


def figure(spec, title, caption):
    return (f'<figure class="figure">{chart_svg(spec, title)}'
            f'<figcaption><b>{esc(title)}.</b> {esc(caption)}</figcaption></figure>')


# --------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------

def load_md(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta = yaml.safe_load(m.group(1)) if m else {}
    return meta, (m.group(2) if m else raw)


_CALLOUT_RE = re.compile(r"^:::(hypo|warn|note|plain)\s*\n(.*?)\n:::\s*$", re.S | re.M)


def render_md(body, charts=None):
    charts = charts or {}

    def callout(m):
        kind, inner = m.group(1), m.group(2)
        cls = "callout" if kind == "plain" else f"callout callout--{kind}"
        return f'<div class="{cls}" markdown="1">\n\n{inner}\n\n</div>'

    body = _CALLOUT_RE.sub(callout, body)

    def chart(m):
        key = m.group(1)
        c = charts[key]
        spec = dict(c["spec"])
        spec["id"] = key
        return "\n" + figure(spec, c["title"], c["caption"]) + "\n"

    body = re.sub(r"^\[\[chart:([\w-]+)\]\]\s*$", chart, body, flags=re.M)
    md = markdown.Markdown(extensions=["toc", "tables", "attr_list", "md_in_html", "smarty", "sane_lists", "fenced_code"],
                           extension_configs={"toc": {"toc_depth": "2-2"}})
    out = md.convert(body)
    toc = [(t["id"], t["name"]) for t in md.toc_tokens]
    return out, toc


def md_inline(text):
    return markdown.markdown(text, extensions=["smarty"])


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

NAV = [
    ("/xauusd-price/", "Gold Price"),
    ("/xauusd-news/", "News"),
    ("/xauusd-trading-strategies/", "Strategies"),
    ("/blog/", "Blog"),
    ("/tools/position-size-calculator/", "Calculator"),
    ("/community/", "Community"),
    ("/membership/", "Membership"),
    ("/about/", "About"),
]

ORG_ID = C.SITE_URL + "/#organization"


def org_schema():
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": C.SITE_NAME,
        "url": C.SITE_URL + "/",
        "logo": {"@type": "ImageObject", "url": C.SITE_URL + "/assets/images/logo-512.png", "width": 512, "height": 512},
        "slogan": C.TAGLINE,
        "description": "An educational website and planned global community for XAUUSD (gold) traders.",
    }


def breadcrumb_schema(crumbs):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": canonical(path)}
            for i, (path, name) in enumerate(crumbs)
        ],
    }


def breadcrumbs_html(crumbs):
    items = []
    for i, (path, name) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li><span aria-current="page">{esc(name)}</span></li>')
        else:
            items.append(f'<li><a href="{path}">{esc(name)}</a></li>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def header(current):
    links = []
    for path, label in NAV:
        cur = ' aria-current="page"' if current and current.startswith(path) else ""
        links.append(f'<li><a href="{path}"{cur}>{label}</a></li>')
    links.append('<li class="nav-cta"><a class="btn btn--gold btn--sm" href="/membership/#registration">Get Launch Updates</a></li>')
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="{C.SITE_NAME} home">{LOGO_SVG}<span class="brand__name">XAUUSD<span> Global</span></span></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">{icon("menu", "icon-open")}{icon("close", "icon-close")}</button>
    <nav class="site-nav" id="site-nav" aria-label="Main"><ul>{"".join(links)}</ul></nav>
  </div>
</header>"""


def footer():
    year = C.FIRST_PUBLISHED[:4]
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/" aria-label="{C.SITE_NAME} home">{LOGO_SVG}<span class="brand__name">XAUUSD<span> Global</span></span></a>
        <p>{C.TAGLINE} Free gold-trading education and a learning community built on market reasoning, honest discussion and transparent trade reviews.</p>
      </div>
      <div><h2>Markets</h2><ul>
        <li><a href="/xauusd-price/">XAUUSD price &amp; chart</a></li>
        <li><a href="/xauusd-news/">Gold market news</a></li>
        <li><a href="/blog/what-moves-gold-prices/">What moves gold</a></li>
      </ul></div>
      <div><h2>Learn</h2><ul>
        <li><a href="/xauusd-trading-strategies/">Strategy hub</a></li>
        <li><a href="/strategies/smart-money-concepts-xauusd/">Smart Money Concepts</a></li>
        <li><a href="/strategies/xauusd-risk-management/">Risk management</a></li>
        <li><a href="/tools/position-size-calculator/">Position size calculator</a></li>
        <li><a href="/blog/">Blog</a></li>
      </ul></div>
      <div><h2>Community</h2><ul>
        <li><a href="/community/">Community vision</a></li>
        <li><a href="/membership/">Membership &amp; levels</a></li>
        <li><a href="/about/">About us</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul></div>
      <div><h2>Legal</h2><ul>
        <li><a href="/risk-disclaimer/">Risk disclaimer</a></li>
        <li><a href="/privacy-policy/">Privacy policy</a></li>
        <li><a href="/terms/">Terms of use</a></li>
      </ul></div>
    </div>
    <div class="footer-risk"><strong>Risk warning:</strong> Trading leveraged products such as CFDs and spot gold (XAUUSD) carries a high level of risk and can result in losses that exceed your expectations, including substantial losses of capital. Everything on this website is general educational information, not personalised financial, investment or trading advice. No strategy, framework or community participation guarantees results. Read the full <a href="/risk-disclaimer/">risk disclaimer</a>.</div>
    <div class="footer-bottom"><span>&copy; {year} {C.SITE_NAME}. All rights reserved.</span><span>Membership launching soon · Launch-updates waitlist open.</span></div>
  </div>
</footer>"""


FONT_URL = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap"


OG_MANIFEST = []


def og_key(path):
    return path.strip("/").replace("/", "-") or "home"


def page(*, path, title, description, body, crumbs=None, og_type="website", schema_extra=None,
         article_meta=None, noindex=False, body_attrs=""):
    url = canonical(path)
    og_img = C.SITE_URL + "/assets/images/og-default.png"
    og_alt = "XAUUSD Global — Connect Traders Around the World. Trade Smarter Together."
    if not noindex and path != "/":
        key = og_key(path)
        OG_MANIFEST.append({"key": key, "path": path, "title": title.split(" | ")[0]})
        if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "images", "og", key + ".jpg")):
            og_img = f"{C.SITE_URL}/assets/images/og/{key}.jpg"
            og_alt = title.split(" | ")[0]
    graph = [org_schema()]
    if path == "/":
        graph.append({"@type": "WebSite", "@id": C.SITE_URL + "/#website", "url": C.SITE_URL + "/",
                      "name": C.SITE_NAME, "description": description, "publisher": {"@id": ORG_ID},
                      "inLanguage": "en"})
    if crumbs and len(crumbs) > 1:
        graph.append(breadcrumb_schema(crumbs))
    if schema_extra:
        graph.extend(schema_extra)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    art = ""
    if article_meta:
        art = (f'<meta property="article:published_time" content="{article_meta["published"]}">'
               f'<meta property="article:section" content="{esc(article_meta["section"])}">')
    tw = f'<meta name="twitter:site" content="@{C.TWITTER_HANDLE}">' if C.TWITTER_HANDLE else ""
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    canon = "" if noindex else f'<link rel="canonical" href="{url}">'
    widgets = "on" if C.PRICE_WIDGETS else "off"
    analytics = (f'<script defer src="{C.UMAMI_SCRIPT}" data-website-id="{C.UMAMI_WEBSITE_ID}"></script>'
                 if getattr(C, "UMAMI_WEBSITE_ID", "") else "")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
{canon}
<meta name="theme-color" content="#08090b">{('<meta name="p:domain_verify" content="' + C.PINTEREST_VERIFY + '"/>') if getattr(C, "PINTEREST_VERIFY", "") else ""}
<meta property="og:site_name" content="{C.SITE_NAME}">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
{art}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{og_img}">
{tw}
<link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/images/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{FONT_URL}">
<link rel="stylesheet" href="{FONT_URL}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{FONT_URL}"></noscript>
<link rel="stylesheet" href="/assets/css/style.css">
<script type="application/ld+json">{ld}</script>
<script src="/assets/js/main.js" defer></script>
{analytics}
</head>
<body data-price-widgets="{widgets}"{body_attrs}>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""


def page_head(crumbs, h1, lede, eyebrow=None, extra=""):
    eb = f'<span class="eyebrow">{esc(eyebrow)}</span>' if eyebrow else ""
    return f"""<section class="page-head grid-bg">
  <div class="wrap">
    {breadcrumbs_html(crumbs)}
    <div style="margin-top:22px">{eb}</div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    {extra}
  </div>
</section>"""


def notice(text, kind="", ico="info"):
    k = f" notice--{kind}" if kind else ""
    return f'<div class="notice{k}">{icon(ico)}<div>{text}</div></div>'


def faq_html(faqs):
    items = "".join(
        f'<details><summary>{esc(f["q"])}</summary><div>{md_inline(f["a"])}</div></details>' for f in faqs)
    return f'<div class="faq-list">{items}</div>'


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["q"],
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", md_inline(f["a"])).strip()}}
        for f in faqs]}


def community_cta(compact=False):
    return f"""<aside class="cta-band" aria-labelledby="cta-h">
  <span class="eyebrow">Bring your charts. Bring your questions.</span>
  <h2 id="cta-h">A trade idea can be useful. Understanding it lasts longer.</h2>
  <p>XAUUSD Global is building a learning community around market reasoning, honest discussion and transparent trade reviews. Membership isn't open yet — get launch updates and be first to hear when it is.</p>
  <div class="btn-row"><a class="btn btn--gold" href="/membership/#registration">Get Launch Updates {icon("arrow")}</a><a class="btn btn--ghost" href="/community/">How the community will work</a></div>
</aside>"""
