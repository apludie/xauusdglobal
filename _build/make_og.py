#!/usr/bin/env python3
"""Generate one social-share image (1200x630 JPG) per public page.

Run after build.py (which writes _build/og_manifest.json), then run build.py
again so pages point at their new images:
    python3 _build/build.py && python3 _build/make_og.py && python3 _build/build.py
Needs: pip install playwright (with a Chromium browser available).
"""
import asyncio
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import lib as L  # noqa: E402

OUT = os.path.join(ROOT, "assets", "images", "og")


def eyebrow(path):
    if path.startswith("/strategies/"):
        return "Strategy guide"
    if path.startswith("/blog/") and path != "/blog/":
        return "Blog"
    if path.startswith("/tools/"):
        return "Free tool"
    return "XAUUSD Global"


def template(title, eb):
    logo = L.LOGO_SVG.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    size = 64 if len(title) < 42 else 56 if len(title) < 62 else 48
    candles = "".join(
        f'<div class="k" style="left:{i*38}px;height:{h}px;bottom:{b}px;background:{c}"></div>'
        for i, (h, b, c) in enumerate([(60, 40, "#3a3f47"), (80, 70, "#f2c14e"), (50, 120, "#3a3f47"), (90, 100, "#f2c14e"),
                                       (70, 160, "#f2c14e"), (40, 200, "#3a3f47"), (100, 170, "#f2c14e"), (60, 250, "#f2c14e")]))
    return f"""<html><head><style>
body{{margin:0;width:1200px;height:630px;background:#08090b;font-family:'Space Grotesk','Inter',system-ui,sans-serif;color:#f3f1ea;overflow:hidden;position:relative}}
.g{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:60px 60px}}
.glow{{position:absolute;width:900px;height:900px;right:-340px;top:-420px;background:radial-gradient(circle,rgba(242,193,78,.24),transparent 62%)}}
.l{{position:absolute;left:72px;top:64px;display:flex;align-items:center;gap:16px;font-weight:700;font-size:30px}}
.l svg{{width:56px;height:56px}} .l span{{color:#f2c14e}}
.eb{{position:absolute;left:72px;top:190px;font-family:ui-monospace,Menlo,monospace;font-size:22px;letter-spacing:4px;text-transform:uppercase;color:#f2c14e}}
h1{{position:absolute;left:72px;top:236px;margin:0;width:820px;font-size:{size}px;line-height:1.08;letter-spacing:-1.5px;font-weight:700}}
p{{position:absolute;left:72px;bottom:60px;margin:0;font-size:24px;color:#b4b2ab}} p b{{color:#f2c14e;font-weight:600}}
.ks{{position:absolute;right:80px;bottom:120px;width:300px;height:360px;opacity:.55}}
.k{{position:absolute;width:20px;border-radius:3px}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:6px;background:linear-gradient(90deg,#c9922f,#f2c14e,#ffe08a)}}
</style></head><body><div class="g"></div><div class="glow"></div><div class="ks">{candles}</div>
<div class="l">{logo}XAUUSD<span>Global</span></div>
<div class="eb">{html.escape(eb)}</div>
<h1>{html.escape(title)}</h1>
<p>Stop chasing signals. <b>Start understanding gold.</b></p><div class="bar"></div></body></html>"""


async def main():
    from playwright.async_api import async_playwright
    items = json.load(open(os.path.join(HERE, "og_manifest.json")))
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        for it in items:
            await pg.set_content(template(it["title"], eyebrow(it["path"])))
            await pg.screenshot(path=os.path.join(OUT, it["key"] + ".jpg"), type="jpeg", quality=82)
        await b.close()
    print(f"Wrote {len(items)} images to assets/images/og/")


if __name__ == "__main__":
    asyncio.run(main())
