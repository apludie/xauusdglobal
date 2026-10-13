# XAUUSD Global — website

Static, SEO-ready website for **https://www.xauusdglobal.com/** — *One Market. One Global Community.*

Plain HTML, CSS and a small vanilla JS file. No backend, database or API keys. Built for GitHub Pages.

---

## 1. What's in this repository

```
/                                  ← published site (GitHub Pages serves the repo root)
├── index.html                     Homepage
├── xauusd-price/                  Gold price page (TradingView chart embed)
├── xauusd-news/                   News hub (feed-ready, transparent empty state)
├── xauusd-trading-strategies/     Strategy hub — 18 topics
├── strategies/<11 guides>/        In-depth strategy articles
├── blog/ + blog/<10 articles>/    Blog with filter, search and "load more"
├── community/  membership/  about/  contact/  faq/
├── risk-disclaimer/  privacy-policy/  terms/   (draft legal pages)
├── 404.html  robots.txt  sitemap.xml  CNAME  _config.yml
├── assets/css/style.css           Design system
├── assets/js/main.js              Nav, session clock, lazy chart widgets, blog filter, news feed
├── assets/images/                 Logo, favicons, social share image
├── assets/data/news.json          Empty news feed (fill only with real, licensed items)
└── _build/                        Generator source — NOT published
    ├── config.py                  Domain, contact email, widget switch, planned price
    ├── build.py                   Generates every page, sitemap, robots, CNAME
    ├── check.py                   Pre-deploy QA (links, anchors, metadata, sitemap, secrets)
    ├── lib.py / pages.py          Layout, SEO head, diagrams, page templates
    └── content/                   Markdown articles, hub topics, legal pages
```

The HTML in the root is already built — you can upload it as-is. Edit content in `_build/content/` and rebuild when you want changes.

## 2. Editing and rebuilding

```bash
pip install markdown pyyaml          # one-time
python3 _build/build.py              # regenerate all pages
python3 _build/check.py              # verify before pushing
```

- **New blog post:** copy any file in `_build/content/blog/`, change the front matter (title, `seo_title` ≤ 60 chars, `description` ≤ 160 chars, `published` date) and body, rebuild. It's added to the blog index, sitemap and related-link system automatically.
- **Diagrams:** articles draw original candlestick schematics from a `charts:` block in front matter and a `[[chart:key]]` line in the body. All are labelled as hypothetical.
- **Callouts:** `:::hypo` (hypothetical example), `:::warn` (risk note), `:::note` (key idea), closed with `:::`.
- **"Last reviewed" date:** set `reviewed: "YYYY-MM-DD"` in an article **only** after a genuine review. Add real `author:` / `reviewer:` names only with verifiable identities.
- **Contact email:** set `CONTACT_EMAIL` in `_build/config.py` once a monitored inbox exists.

## 3. Deploy to GitHub Pages

1. Create a GitHub repository (for example `xauusdglobal`). Public repos get Pages on the free plan.
2. Upload everything in this folder to the repository root (drag-and-drop in the GitHub web UI, or):
   ```bash
   git init && git add . && git commit -m "Launch XAUUSD Global"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/xauusdglobal.git
   git push -u origin main
   ```
3. Repository → **Settings → Pages** → *Build and deployment* → Source: **Deploy from a branch** → Branch: **main**, folder **/ (root)** → Save.
4. Under **Custom domain**, enter `www.xauusdglobal.com` and save (the `CNAME` file already contains it).
5. After DNS is working (section 4), tick **Enforce HTTPS**. GitHub issues the certificate automatically; this can take a while.

> **Preview before DNS?** Links are root-relative (`/blog/`), which is correct for the custom domain. If you want to preview at `https://USERNAME.github.io/xauusdglobal/` first, set `BASE_PATH = "/xauusdglobal"` in `_build/config.py`, rebuild, push — and set it back to `""` and rebuild before connecting the domain.

## 4. Custom-domain DNS

At your domain registrar's DNS settings:

| Type | Host / Name | Value |
|---|---|---|
| CNAME | `www` | `YOUR-USERNAME.github.io` |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA (optional) | `@` | `2606:50c0:8000::153` |
| AAAA (optional) | `@` | `2606:50c0:8001::153` |
| AAAA (optional) | `@` | `2606:50c0:8002::153` |
| AAAA (optional) | `@` | `2606:50c0:8003::153` |

- With `www` as the custom domain and the apex records above, GitHub redirects `xauusdglobal.com` → `www.xauusdglobal.com`.
- Remove any conflicting old A/CNAME records (e.g. registrar "parking" records).
- Recommended: verify the domain under **GitHub → Settings (your account) → Pages → Verified domains** to prevent takeover.
- Check these IPs against GitHub's current documentation ("Managing a custom domain for your GitHub Pages site") before saving — they rarely change, but the docs are the source of truth.
- DNS can take up to 24–48 hours. **The domain is not live until** `https://www.xauusdglobal.com/` loads with a valid certificate and `http://xauusdglobal.com` redirects to it.

## 5. Google Search Console

1. Add a **Domain property** for `xauusdglobal.com` (verify with a DNS TXT record), or a URL-prefix property for `https://www.xauusdglobal.com/`.
2. Submit `https://www.xauusdglobal.com/sitemap.xml`.
3. Use URL Inspection on the homepage and a few articles to request indexing.
Indexing and rankings are never guaranteed; expect weeks, not days.

## 6. Data honesty — how the site handles prices and news

- **Prices:** the price page and homepage preview embed **TradingView** widgets (symbol `OANDA:XAUUSD`, set in `config.py`). They load in the visitor's browser with no keys, are lazy-loaded, and are credited with a note that quotes may be delayed. Set `PRICE_WIDGETS = False` to replace them with a clearly labelled "no data source configured" state. Review TradingView's widget terms before launch.
- **News:** `assets/data/news.json` is intentionally empty, so the news hub shows "Market news feed integration coming soon". When you connect a licensed feed, write items in this format (the page renders them with source, date and link):
  ```json
  {"source": "Provider name", "updated": "2026-10-13T09:00:00Z",
   "items": [{"title": "...", "url": "https://...", "source": "Publisher",
              "published": "2026-10-13T08:30:00Z", "category": "Federal Reserve",
              "summary": "One or two sentences in your own words."}]}
  ```
  A scheduled GitHub Action could regenerate this file from an RSS/API source using a repository secret — never put API keys in `assets/`.

## 7. Optional integrations for later

| Integration | Options to evaluate | Notes |
|---|---|---|
| Live gold price | TradingView widgets (in place), a licensed market-data API via a serverless proxy | Keys must stay server-side (Cloudflare Worker, Netlify/Vercel function) |
| News feed | Licensed news API or publisher RSS feeds → `news.json` via scheduled job | Headlines + link + your own summary only |
| Analytics | **Umami Cloud — already installed** on every page (`UMAMI_WEBSITE_ID` in `_build/config.py`) | Privacy policy updated; set the ID to `""` to remove it |
| Registration & auth | Circle, Discourse, Discord with role gating, Supabase/Auth0, Memberstack | Choose platform first, then finalise terms and privacy |
| Payments / recurring billing | Stripe Billing, Paddle, Lemon Squeezy | Requires final terms, refund policy, tax handling |
| Email updates | Buttondown, ConvertKit, Mailchimp | Only after the privacy policy covers it; double opt-in |
| Hosting upgrade | Cloudflare Pages, Netlify, Vercel | Same static files; adds headers, redirects and functions |

The design already has slots for this: the header CTA, `#registration` section on `/membership/`, status badges, and the tier cards.

## 8. Pre-launch checklist

- [ ] `python3 _build/check.py` passes (links, anchors, titles, descriptions, canonicals, sitemap, secrets)
- [ ] Repository pushed; Pages source = `main` / root
- [ ] DNS records added; custom domain shows a green check in Settings → Pages
- [ ] **Enforce HTTPS** enabled; `http://`, apex and `www` all end at `https://www.xauusdglobal.com/`
- [ ] Price page: TradingView chart loads in a normal browser (and you accept the widget terms)
- [ ] `CONTACT_EMAIL` set to a monitored inbox, or left empty intentionally
- [ ] Legal pages reviewed by a qualified professional (they are marked as drafts)
- [ ] Article authors/reviewers added only with real, verifiable identities; `reviewed` dates only after real reviews
- [ ] Social preview checked (paste the URL into LinkedIn/X post composer)
- [ ] Search Console property verified and sitemap submitted
- [ ] Lighthouse run on mobile for `/`, `/xauusd-price/` and one article
- [ ] Registration, payments and member access still described as "not open yet" everywhere
