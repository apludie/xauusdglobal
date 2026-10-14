"""Builds assets/css/style-elegant.css: a calmer champagne-gold variant of style.css (preview with ?look=elegant)."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = [
    ("linear-gradient(135deg, #ffe08a 0%, #f2c14e 42%, #c9922f 100%)", "linear-gradient(180deg, #d2b67c 0%, #c2a265 100%)"),
    ("linear-gradient(135deg,#ffe08a,#f2c14e 45%,#c9922f)", "linear-gradient(180deg,#d2b67c,#c2a265)"),
    ("linear-gradient(135deg,#ffe08a,#c9922f)", "linear-gradient(180deg,#d2b67c,#b39457)"),
    ("linear-gradient(90deg,#c9922f,#f2c14e,#ffe08a)", "linear-gradient(90deg,#b39457,#c8a96b)"),
    ("#ffe08a", "#d9c393"), ("#f2c14e", "#c8a96b"), ("#ffd978", "#d8c294"), ("#b8862b", "#9a7b45"),
    ("#c9922f", "#a98a52"), ("#e0a73a", "#b8975c"), ("#e0b04f", "#bfa064"), ("#f2a14e", "#c99a6a"),
    ("242, 193, 78", "200, 169, 107"), ("242,193,78", "200,169,107"), ("255, 217, 120", "216, 194, 148"),
    ("#3ccf91", "#7fb99a"), ("#3ecf8e", "#7fb99a"), ("60, 207, 145", "127, 185, 154"), ("60,207,145", "127,185,154"),
    ("#ef6a5b", "#cf8274"), ("#ef6461", "#cf8274"), ("239,106,91", "207,130,116"), ("239, 106, 91", "207, 130, 116"),
    ("#ff8f70", "#d9a088"), ("#6ee7d0", "#93c6b7"), ("#8fd3ff", "#a5c2d6"), ("#45d6c4", "#8fc4b8"),
]
EXTRA = """
/* ===== Elegant look: matte champagne gold, no glare, calmer motion ===== */
.gold-text, .serif.gold-text, .offer-box__free .serif, .best__time { background: none !important; color: #cdb07a !important; -webkit-text-fill-color: #cdb07a !important; }
.btn--gold { box-shadow: none !important; } .btn--gold::after { display: none !important; }
.btn--gold:hover { transform: none; background: #d4bb86; box-shadow: none !important; }
.hero::after { opacity: .35; } .showcase::before, .inside-hero::before, .offer-sec::before { opacity: .45; }
.stage__inner::before, .coin-wrap::before { opacity: .35; } .coin-shadow { opacity: .55; }
.offer-box, .best { box-shadow: none !important; background: #121418 !important; }
.app { box-shadow: 0 30px 70px -40px rgba(0,0,0,.9) !important; }
.tl-bar--ov { box-shadow: none !important; }
.status-pill--offer { background: transparent; }
.marquee--cities .marquee__inner { color: rgba(243,241,234,.28); }
.marquee--cities .marquee__inner span::before { opacity: .5; }
.live-dot, .fd-live__badge i, .rail-k i, .hours__dot { animation: none !important; box-shadow: none !important; }
.float { animation: none !important; }
.card::after { background: radial-gradient(380px circle at var(--mx, 50%) var(--my, 50%), rgba(200,169,107,.05), transparent 45%) !important; }
.statement__sticky::before { opacity: .5; }
.js .globe-box.on { opacity: .88; }
.site-nav .nav-cta a.btn--gold, .site-nav .nav-cta a.btn--gold:hover { background: #c8a96b; }
@media (prefers-reduced-motion: no-preference) {
  .js .hero--home .ht-in, .js .inside-title .ht-in { animation-name: blurUpSoft; animation-duration: 1.2s; }
  .js .intro { animation-name: blurUpSoftSm; animation-duration: 1.1s; }
}
@keyframes blurUpSoft { 0% { opacity: 0; transform: translate3d(0, 22px, 0); filter: blur(6px); } 100% { opacity: 1; transform: none; filter: blur(0); } }
@keyframes blurUpSoftSm { 0% { opacity: 0; transform: translate3d(0, 12px, 0); filter: blur(4px); } 100% { opacity: 1; transform: none; filter: blur(0); } }
.look-switch { position: fixed; left: 16px; bottom: 16px; z-index: 80; display: flex; align-items: center; gap: 10px; padding: 8px 10px 8px 14px; border-radius: 999px; background: rgba(18,20,24,.96); border: 1px solid rgba(255,255,255,.14); font-size: .82rem; color: #b4b2ab; }
.look-switch a { color: #d8c294; text-decoration: none; padding: 4px 10px; border-radius: 999px; border: 1px solid rgba(200,169,107,.4); }
"""
def build():
    src = open(os.path.join(ROOT, "assets", "css", "style.css"), encoding="utf-8").read()
    for a, b in MAP:
        src = src.replace(a, b)
    open(os.path.join(ROOT, "assets", "css", "style-elegant.css"), "w", encoding="utf-8").write(src + EXTRA)
