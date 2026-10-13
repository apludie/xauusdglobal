#!/usr/bin/env python3
"""Pre-deploy checks: links, anchors, metadata uniqueness, H1s, canonicals,
indexability, sitemap. Run after build:  python3 _build/check.py"""
import glob
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_build"))
import config as C  # noqa: E402


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.h1, self.title, self.meta, self.imgs = [], set(), 0, "", {}, []
        self._in_title = False
        self.canon = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag in ("link", "script", "img") and (a.get("href") or a.get("src")):
            if tag == "link" and a.get("rel") == "canonical":
                self.canon = a["href"]
            elif not (tag == "link" and a.get("rel") in ("preconnect",)):
                self.links.append(a.get("href") or a.get("src"))
        if tag == "img":
            self.imgs.append(a.get("alt"))
        if tag == "h1":
            self.h1 += 1
        if tag == "title" and not self.title:
            self._in_title = True
        if tag == "meta" and ("name" in a or "property" in a):
            self.meta[a.get("name") or a.get("property")] = a.get("content", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, d):
        if self._in_title:
            self.title += d


def url_to_file(path):
    path = path.split("#")[0].split("?")[0]
    if C.BASE_PATH and path.startswith(C.BASE_PATH):
        path = path[len(C.BASE_PATH):]
    fp = os.path.join(ROOT, path.lstrip("/"))
    if path.endswith("/"):
        fp = os.path.join(fp, "index.html")
    return fp


def main():
    errors, pages = [], {}
    files = [f for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True) if "/_build/" not in f]
    for f in files:
        p = P()
        p.feed(open(f, encoding="utf-8").read())
        pages[f] = p
    titles, descs = {}, {}
    for f, p in pages.items():
        rel = "/" + os.path.relpath(f, ROOT).replace("index.html", "")
        is404 = rel == "/404.html" or "noindex" in p.meta.get("robots", "")
        if p.h1 != 1:
            errors.append(f"{rel}: {p.h1} <h1> elements")
        if not is404:
            if "noindex" in p.meta.get("robots", ""):
                errors.append(f"{rel}: noindex on public page")
            if p.canon != C.SITE_URL + rel:
                errors.append(f"{rel}: canonical {p.canon}")
            titles.setdefault(p.title, []).append(rel)
            descs.setdefault(p.meta.get("description"), []).append(rel)
            d = p.meta.get("description", "")
            if not (50 <= len(d) <= 165):
                errors.append(f"{rel}: description length {len(d)}")
            if len(p.title) > 70:
                errors.append(f"{rel}: title length {len(p.title)}")
        for alt in p.imgs:
            if alt is None:
                errors.append(f"{rel}: <img> without alt")
        for href in p.links:
            if href.startswith(("http://", "https://", "mailto:", "//")):
                continue
            if href.startswith("#"):
                if href[1:] and href[1:] not in p.ids:
                    errors.append(f"{rel}: missing anchor {href}")
                continue
            target = url_to_file(href)
            if not os.path.exists(target):
                errors.append(f"{rel}: broken link {href}")
            elif "#" in href:
                frag = href.split("#", 1)[1]
                tp = pages.get(target)
                if frag and tp and frag not in tp.ids:
                    errors.append(f"{rel}: missing anchor {href}")
    for t, rels in titles.items():
        if len(rels) > 1:
            errors.append(f"duplicate title '{t}': {rels}")
    for d, rels in descs.items():
        if len(rels) > 1:
            errors.append(f"duplicate description: {rels}")
    sm = open(os.path.join(ROOT, "sitemap.xml")).read()
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    for loc in locs:
        if not os.path.exists(url_to_file(loc.replace(C.SITE_URL, ""))):
            errors.append(f"sitemap entry missing: {loc}")
    public = sum(1 for q in pages.values() if "noindex" not in q.meta.get("robots", ""))
    if len(locs) != public:
        errors.append(f"sitemap has {len(locs)} URLs but {public} public pages exist")
    secrets = re.compile(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9]{12,}", re.I)
    for f in glob.glob(os.path.join(ROOT, "assets", "**", "*.*"), recursive=True) + files:
        if f.endswith((".js", ".html", ".json")) and secrets.search(open(f, encoding="utf-8", errors="ignore").read()):
            errors.append(f"possible secret in {f}")
    print(f"Checked {len(pages)} HTML files, {len(locs)} sitemap URLs.")
    if errors:
        print("\n".join("  ✗ " + e for e in errors))
        sys.exit(1)
    print("  ✓ All checks passed")


if __name__ == "__main__":
    main()
