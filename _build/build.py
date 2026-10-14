#!/usr/bin/env python3
"""Static site generator for XAUUSD Global.

Usage (from the repository root):
    pip install markdown pyyaml pillow
    python3 _build/build.py

Content lives in _build/content/. Output is written to the repository root,
which is exactly what GitHub Pages serves.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import config as C  # noqa: E402
import lib as L  # noqa: E402
import pages as P  # noqa: E402

CONTENT = os.path.join(HERE, "content")
OUT = []  # (path, html, sitemap_priority)

import yaml  # noqa: E402
THINK = yaml.safe_load(open(os.path.join(CONTENT, "think.yaml"), encoding="utf-8"))

# Official / primary sources (each URL checked before adding). Shown as "Sources and further reading".
SOURCES = {
    "wgc": ("World Gold Council — Goldhub", "https://www.gold.org/goldhub", "Gold demand, supply and market research"),
    "fomc": ("Federal Reserve — FOMC meeting calendar", "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm", "Rate-decision dates and statements"),
    "cpi": ("U.S. Bureau of Labor Statistics — Consumer Price Index", "https://www.bls.gov/cpi/", "Official US inflation data"),
    "nfp": ("U.S. Bureau of Labor Statistics — Employment Situation", "https://www.bls.gov/news.release/empsit.toc.htm", "The monthly US jobs report (non-farm payrolls)"),
    "cot": ("CFTC — Commitments of Traders", "https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm", "Weekly futures positioning, including gold"),
    "real": ("FRED — 10-Year Treasury Inflation-Indexed Yield (DFII10)", "https://fred.stlouisfed.org/series/DFII10", "A common measure of US real yields"),
    "usd": ("FRED — Nominal Broad U.S. Dollar Index", "https://fred.stlouisfed.org/series/DTWEXBGS", "A broad measure of US dollar strength"),
    "lbma": ("LBMA — Precious Metal Prices", "https://www.lbma.org.uk/prices-and-data/precious-metal-prices", "The LBMA Gold Price benchmark set in London"),
    "cme": ("CME Group — Gold futures overview", "https://www.cmegroup.com/markets/metals/precious/gold.html", "Contract specifications and trading hours for COMEX gold"),
    "stop": ("Investor.gov — Stop order", "https://www.investor.gov/introduction-investing/investing-basics/glossary/stop-order", "How stop orders work, and their limits in fast markets"),
    "fraud": ("CFTC — Foreign Currency (Forex) Fraud advisory", "https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/fraudadv_forex.html", "Warning signs of trading scams and unrealistic promises"),
}
TECH = ["cme", "cot", "stop"]
ARTICLE_SOURCES = {
    "what-moves-gold-prices": ["usd", "real", "fomc", "cpi", "wgc", "cot"],
    "what-is-xauusd": ["lbma", "cme", "wgc", "fraud"],
    "new-york-session-gold-trading": ["nfp", "cpi", "fomc", "cme"],
    "london-session-gold-trading": ["lbma", "cme"],
    "london-vs-new-york-sessions": ["lbma", "nfp", "cme"],
    "xauusd-risk-management": ["stop", "cme", "fraud"],
    "risk-management-volatile-gold-markets": ["stop", "cme", "fraud"],
    "how-to-build-a-xauusd-trading-plan": ["stop", "fomc", "fraud"],
    "how-to-keep-a-trading-journal": ["stop", "fraud"],
    "common-mistakes-intermediate-gold-traders": ["stop", "fraud"],
}

# Overlapping topic pairs: each page points to its companion so they serve different intents.
COMPANIONS = {
    "/strategies/ict-trading-xauusd/": ("/blog/ict-concepts-for-gold-trading/", "Want a shorter introduction first? Read"),
    "/blog/ict-concepts-for-gold-trading/": ("/strategies/ict-trading-xauusd/", "This is the quick introduction. For the full, step-by-step guide, read"),
    "/strategies/smart-money-concepts-xauusd/": ("/blog/smart-money-concepts-explained-xauusd/", "Want a shorter introduction first? Read"),
    "/blog/smart-money-concepts-explained-xauusd/": ("/strategies/smart-money-concepts-xauusd/", "This is the quick introduction. For the full, step-by-step guide, read"),
    "/strategies/support-and-resistance-xauusd/": ("/blog/how-to-identify-support-and-resistance-gold/", "New to drawing levels? Start with"),
    "/blog/how-to-identify-support-and-resistance-gold/": ("/strategies/support-and-resistance-xauusd/", "This article covers drawing levels. To trade them, read"),
    "/strategies/xauusd-risk-management/": ("/blog/risk-management-volatile-gold-markets/", "For handling fast, news-driven conditions specifically, read"),
    "/blog/risk-management-volatile-gold-markets/": ("/strategies/xauusd-risk-management/", "This article focuses on volatile conditions. For the complete position-sizing guide, read"),
    "/strategies/london-session-gold-trading/": ("/blog/london-vs-new-york-sessions/", "Comparing sessions? Read"),
    "/strategies/new-york-session-gold-trading/": ("/blog/london-vs-new-york-sessions/", "Comparing sessions? Read"),
    "/blog/london-vs-new-york-sessions/": ("/strategies/london-session-gold-trading/", "This is the side-by-side comparison. For a deep dive into one session, read"),
}


def write(path, html):
    rel = path.strip("/")
    target = os.path.join(ROOT, rel, "index.html") if not rel.endswith(".html") else os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    if C.BASE_PATH:
        html = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{C.BASE_PATH}/', html)
    with open(target, "w", encoding="utf-8") as f:
        f.write(html)


def load_collection(kind):
    items = []
    for fp in sorted(glob.glob(os.path.join(CONTENT, kind, "*.md"))):
        meta, body = L.load_md(fp)
        slug = os.path.splitext(os.path.basename(fp))[0]
        meta["slug"] = slug
        meta["path"] = f"/{kind}/{slug}/"
        meta["body"] = body
        meta["kind"] = kind
        items.append(meta)
    items.sort(key=lambda m: m.get("order", 99))
    return items


def render_article(a, titles):
    hub = ("/xauusd-trading-strategies/", "Trading Strategies") if a["kind"] == "strategies" else ("/blog/", "Blog")
    crumbs = [("/", "Home"), hub, (a["path"], a.get("short", a["title"]))]
    html_body, toc = L.render_md(a["body"], a.get("charts"))
    faqs = a.get("faqs") or []
    if faqs:
        toc.append(("faq", "Frequently asked questions"))
    minutes = L.reading_minutes(a["body"])
    a["minutes"] = minutes
    reviewed = a.get("reviewed")
    reviewed_txt = L.fmt_date(reviewed) if reviewed else "Pending editorial review"
    author = a.get("author") or "XAUUSD Global Editorial"
    reviewer_html = f'<span>Reviewed by <b>{a["reviewer"]}</b></span>' if a.get("reviewer") else ""
    reviewed_html = f'<span>Last reviewed <b>{reviewed_txt}</b></span>' if reviewed else ""
    byline = f"""<div class="byline">
      <span>Published <b><time datetime="{a['published']}">{L.fmt_date(a['published'])}</time></b></span>
      <span><b>{minutes} min</b> read</span>
      <span>By <b>{author}</b> · <a href="/about/#editorial-standards">Editorial standards</a></span>
      {reviewer_html}{reviewed_html}
    </div>"""
    related = "".join(f'<li><a href="{p}">{L.esc(titles[p])}</a></li>' for p in a.get("related", []))
    faq_block = f'<h2 id="faq">Frequently asked questions</h2>{L.faq_html(faqs)}' if faqs else ""
    qs = THINK.get(a["slug"], [])
    think_block = ""
    if qs:
        think_block = ('<aside class="think" aria-labelledby="think-h"><span class="eyebrow">Apply it to your chart</span>'
                       '<h2 id="think-h">Think it through</h2><p>Before your next gold trade using this idea, answer these in your journal — ideally before you know the result.</p><ol>'
                       + "".join(f"<li>{L.esc(q)}</li>" for q in qs)
                       + '</ol><p class="think__foot">A well-reasoned trade can still lose. The goal is a decision you can explain and learn from. '
                         '<a href="/blog/how-to-keep-a-trading-journal/">How to keep a trading journal</a></p></aside>')
        toc.insert(len(toc) - (1 if faqs else 0), ("think-h", "Think it through"))
    src_keys = ARTICLE_SOURCES.get(a["slug"], TECH)
    src_block = ('<section class="sources" aria-labelledby="src-h"><h2 id="src-h">Sources and further reading</h2><ul>'
                 + "".join(f'<li><a href="{SOURCES[k][1]}" target="_blank" rel="noopener">{L.esc(SOURCES[k][0])}</a> — {L.esc(SOURCES[k][2])}</li>' for k in src_keys)
                 + '</ul><p class="muted">External sites are independent of XAUUSD Global. Check dates and data yourself.</p></section>')
    tool_block = ""
    if a["slug"] in ("xauusd-risk-management", "risk-management-volatile-gold-markets", "how-to-build-a-xauusd-trading-plan", "what-is-xauusd"):
        tool_block = '<p class="companion"><strong>Free tool:</strong> work out your lot size from your risk and stop with the <a href="/tools/position-size-calculator/">XAUUSD position size calculator</a>.</p>'
    comp = COMPANIONS.get(a["path"])
    comp_block = ""
    if comp and comp[0] in titles:
        comp_block = f'<p class="companion">{comp[1]} <a href="{comp[0]}">{L.esc(titles[comp[0]])}</a>.</p>' 
    toc_html = "".join(f'<li><a href="#{i}">{L.esc(n)}</a></li>' for i, n in toc)
    body = f"""{L.page_head(crumbs, L.esc(a['title']), L.esc(a['lede']), eyebrow=a.get('category'), extra=byline)}
<div class="wrap">
  <div class="article-layout">
    <aside class="toc" aria-label="Table of contents"><details><summary>On this page</summary><ol>{toc_html}</ol></details></aside>
    <article class="prose">
      {comp_block}{tool_block}
      <div style="height:1.4em"></div>
      {html_body}
      {think_block}
      {faq_block}
      {src_block}
      <section class="related" aria-labelledby="rel-h"><h2 id="rel-h">Continue learning</h2><ul>{related}</ul></section>
      {L.community_cta()}
    </article>
  </div>
</div>"""
    schema = [{
        "@type": "Article",
        "headline": a["title"][:110],
        "description": a["description"],
        "datePublished": a["published"],
        "dateModified": a.get("reviewed") or a["published"],
        "author": {"@id": L.ORG_ID},
        "publisher": {"@id": L.ORG_ID},
        "image": C.SITE_URL + (f"/assets/images/og/{L.og_key(a['path'])}.jpg" if os.path.exists(os.path.join(ROOT, "assets", "images", "og", L.og_key(a["path"]) + ".jpg")) else "/assets/images/og-default.png"),
        "mainEntityOfPage": L.canonical(a["path"]),
        "articleSection": a.get("category", ""),
        "inLanguage": "en",
    }]
    return L.page(path=a["path"], title=a["seo_title"], description=a["description"], body=body,
                  crumbs=crumbs, og_type="article", schema_extra=schema,
                  article_meta={"published": a["published"], "section": a.get("category", "")})


def main():
    strategies = load_collection("strategies")
    posts = load_collection("blog")
    titles = {a["path"]: a["title"] for a in strategies + posts}
    titles.update(P.TITLES)

    pages = []  # (path, html, priority)
    for a in strategies + posts:
        a["_html"] = render_article(a, titles)
    for a in strategies:
        pages.append((a["path"], a["_html"], "0.8"))
    for a in posts:
        pages.append((a["path"], a["_html"], "0.7"))

    for path, html, prio in P.build_all(strategies, posts, titles):
        pages.append((path, html, prio))

    seen = set()
    for path, html, _ in pages:
        assert path not in seen, f"duplicate page {path}"
        seen.add(path)
        write(path, html)

    # 404 (not in sitemap, noindex)
    write("/404.html", P.not_found())
    # private confirmation page (noindex, not in sitemap)
    write("/waitlist-confirmed/", P.waitlist_confirmed())

    json.dump(L.OG_MANIFEST, open(os.path.join(HERE, "og_manifest.json"), "w"), indent=1)

    # sitemap
    # lastmod: the date each page's HTML last actually changed (tracked by content hash)
    import hashlib, datetime
    lm_file = os.path.join(HERE, "lastmod.json")
    lm = json.load(open(lm_file)) if os.path.exists(lm_file) else {}
    today = datetime.date.today().isoformat()
    urls = []
    for path, html, prio in sorted(pages, key=lambda p: (p[0] != "/", p[0])):
        h = hashlib.sha1(html.encode("utf-8")).hexdigest()
        if lm.get(path, {}).get("hash") != h:
            lm[path] = {"hash": h, "date": today if path in lm or os.path.exists(lm_file) else C.FIRST_PUBLISHED}
        urls.append(f"  <url><loc>{L.canonical(path)}</loc><lastmod>{lm[path]['date']}</lastmod><priority>{prio}</priority></url>")
    json.dump(lm, open(lm_file, "w"), indent=1, sort_keys=True)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {C.SITE_URL}/sitemap.xml\n")
    host = C.SITE_URL.split("://", 1)[1]
    open(os.path.join(ROOT, "CNAME"), "w").write(host + "\n")

    # news data file (filled hourly by _build/fetch_news.py in the deploy workflow)
    news_fp = os.path.join(ROOT, "assets", "data", "news.json")
    if not os.path.exists(news_fp):
        json.dump({"source": None, "updated": None, "items": []}, open(news_fp, "w"), indent=2)

    P.make_images(ROOT)
    print(f"Built {len(pages)} pages + 404 into {ROOT}")


if __name__ == "__main__":
    main()
