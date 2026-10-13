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
    toc_html = "".join(f'<li><a href="#{i}">{L.esc(n)}</a></li>' for i, n in toc)
    minutes = L.reading_minutes(a["body"])
    a["minutes"] = minutes
    reviewed = a.get("reviewed")
    reviewed_txt = L.fmt_date(reviewed) if reviewed else "Pending editorial review"
    author = a.get("author") or "XAUUSD Global Editorial <span class=\"muted\">(named author profile to be added)</span>"
    reviewer = a.get("reviewer") or "To be assigned <span class=\"muted\">(qualified reviewer, credentials to be verified)</span>"
    byline = f"""<div class="byline">
      <span>Published <b><time datetime="{a['published']}">{L.fmt_date(a['published'])}</time></b></span>
      <span><b>{minutes} min</b> read</span>
      <span>Author: <b>{author}</b></span>
      <span>Reviewer: <b>{reviewer}</b></span>
      <span>Last reviewed: <b>{reviewed_txt}</b></span>
    </div>"""
    related = "".join(f'<li><a href="{p}">{L.esc(titles[p])}</a></li>' for p in a.get("related", []))
    faq_block = f'<h2 id="faq">Frequently asked questions</h2>{L.faq_html(faqs)}' if faqs else ""
    body = f"""{L.page_head(crumbs, L.esc(a['title']), L.esc(a['lede']), eyebrow=a.get('category'), extra=byline)}
<div class="wrap">
  <div class="article-layout">
    <aside class="toc" aria-label="Table of contents"><details><summary>On this page</summary><ol>{toc_html}</ol></details></aside>
    <article class="prose">
      {L.notice("<strong>Educational content, not financial advice.</strong> Examples are hypothetical and simplified. Trading leveraged gold products can result in substantial losses. <a href='/risk-disclaimer/'>Read the risk disclaimer</a>.", "risk", "alert")}
      <div style="height:1.4em"></div>
      {html_body}
      {faq_block}
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
        "image": C.SITE_URL + "/assets/images/og-default.png",
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

    # sitemap
    urls = []
    for path, _, prio in sorted(pages, key=lambda p: (p[0] != "/", p[0])):
        urls.append(f"  <url><loc>{L.canonical(path)}</loc><lastmod>{C.FIRST_PUBLISHED}</lastmod><priority>{prio}</priority></url>")
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {C.SITE_URL}/sitemap.xml\n")
    host = C.SITE_URL.split("://", 1)[1]
    open(os.path.join(ROOT, "CNAME"), "w").write(host + "\n")

    # news data file (filled hourly by _build/fetch_news.py in the GitHub Actions workflow)
    news_fp = os.path.join(ROOT, "assets", "data", "news.json")
    if not os.path.exists(news_fp):
        json.dump({"source": None, "updated": None, "items": []}, open(news_fp, "w"), indent=2)

    P.make_images(ROOT)
    print(f"Built {len(pages)} pages + 404 into {ROOT}")


if __name__ == "__main__":
    main()
