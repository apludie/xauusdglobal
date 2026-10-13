#!/usr/bin/env python3
"""Collect gold-relevant headlines from public RSS/Atom feeds into assets/data/news.json.

Standard library only, so it runs on GitHub Actions without installing anything:
    python3 _build/fetch_news.py

Each item keeps only: headline, link to the original, source name, publication
time, a category and a short excerpt. Full articles are never copied.
If every feed fails, the existing news.json is left untouched.
"""
import datetime as dt
import email.utils
import html
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "data", "news.json")
CFG = json.load(open(os.path.join(HERE, "news_feeds.json"), encoding="utf-8"))
UA = "Mozilla/5.0 (compatible; XAUUSDGlobalNewsBot/1.0; +https://www.xauusdglobal.com/xauusd-news/)"

CATEGORIES = [
    ("Gold market", r"\b(gold|xau|bullion|precious)\b"),
    ("Federal Reserve", r"\b(fed|fomc|powell|federal reserve|federal open market)\b"),
    ("Inflation", r"\b(cpi|pce|inflation|ppi|prices index)\b"),
    ("Treasury yields", r"\b(treasury|treasuries|yields?|bond)\b"),
    ("Central banks", r"\b(ecb|boj|boe|pboc|central banks?|lagarde|monetary policy)\b"),
    ("US dollar", r"\b(us dollar|usd|dxy|greenback)\b"),
    ("Geopolitics", r"\b(war|sanctions?|tariffs?|geopolitic\w*|conflict|election)\b"),
]
ATOM = "{http://www.w3.org/2005/Atom}"


def clean(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def excerpt(text, limit):
    text = clean(text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",.;:-–—")
    return cut + "…"


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = email.utils.parsedate_to_datetime(re.sub(r"\s+", " ", s))
    except (TypeError, ValueError):
        try:
            d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d.astimezone(dt.timezone.utc)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml"})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = r.read()
    return data.lstrip(b"\xef\xbb\xbf").lstrip()


def items_from(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = []
    for it in root.iter("item"):  # RSS 2.0
        out.append({
            "title": it.findtext("title"),
            "url": (it.findtext("link") or "").strip(),
            "date": it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date"),
            "summary": it.findtext("description"),
        })
    for en in root.iter(ATOM + "entry"):  # Atom
        link = en.find(ATOM + "link[@rel='alternate']")
        if link is None:
            link = en.find(ATOM + "link")
        out.append({
            "title": en.findtext(ATOM + "title"),
            "url": link.get("href") if link is not None else "",
            "date": en.findtext(ATOM + "published") or en.findtext(ATOM + "updated"),
            "summary": en.findtext(ATOM + "summary") or en.findtext(ATOM + "content"),
        })
    return out


def categorize(text, default):
    if default:
        return default
    for name, pattern in CATEGORIES:
        if re.search(pattern, text, re.I):
            return name
    return "Markets"


def main():
    now = dt.datetime.now(dt.timezone.utc)
    oldest = now - dt.timedelta(days=CFG.get("max_age_days", 7))
    collected, ok_sources = [], []
    for feed in CFG["feeds"]:
        try:
            raw = items_from(fetch(feed["url"]))
        except Exception as e:  # network errors, bad XML: skip this feed
            print(f"  ! {feed['name']}: {e}", file=sys.stderr)
            continue
        ok_sources.append(feed["name"])
        pat = re.compile(feed.get("include", "."), re.I)
        kept = 0
        for it in raw:
            title = clean(it["title"])
            url = it["url"]
            when = parse_date(it["date"])
            if not title or not url.startswith(("https://", "http://")) or not when or when < oldest or when > now + dt.timedelta(hours=1):
                continue
            hay = f"{title} {clean(it['summary'])} {url}"
            if not pat.search(hay):
                continue
            collected.append({
                "title": title,
                "url": url,
                "source": feed["name"],
                "published": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "category": categorize(title, feed.get("category")) if categorize(title, None) != "Markets" else categorize(hay, feed.get("category")),
                "summary": excerpt(it["summary"], CFG.get("excerpt_chars", 180)),
            })
            kept += 1
            if kept >= feed.get("max_items", 20):
                break
        print(f"  ✓ {feed['name']}: {kept} items")

    if not ok_sources:
        print("No feeds could be fetched; keeping the existing news.json.")
        return

    seen, unique = set(), []
    for it in sorted(collected, key=lambda x: x["published"], reverse=True):
        key = (it["url"].split("?")[0], it["title"].lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(it)
    data = {
        "source": "Public RSS feeds: " + ", ".join(ok_sources),
        "updated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "items": unique[: CFG.get("max_total", 40)],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"Wrote {len(data['items'])} headlines to {OUT}")


if __name__ == "__main__":
    main()
