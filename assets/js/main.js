/* XAUUSD Global — minimal progressive enhancement. The site works without JS. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");

  /* ---- Mobile navigation ---- */
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  /* ---- Reveal on scroll (respects reduced motion via CSS) ---- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); ro.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    var vh = window.innerHeight || 800;
    reveals.forEach(function (el) {
      // Only animate elements that start below the fold; visible content is never hidden.
      if (el.getBoundingClientRect().top > vh) el.classList.add("pre");
      ro.observe(el);
    });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Table of contents: highlight current section ---- */
  var tocLinks = document.querySelectorAll(".toc a[href^='#']");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var to = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("active"); });
          var link = map[en.target.id];
          if (link) link.classList.add("active");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) {
      var h = document.getElementById(id);
      if (h) to.observe(h);
    });
    // On wide screens keep the TOC expanded
    if (window.matchMedia("(min-width: 1060px)").matches) {
      document.querySelectorAll(".toc details").forEach(function (d) { d.open = true; });
    }
  }

  /* ---- Market session clock (computed from the visitor's clock, not market data) ---- */
  var sessionsEl = document.querySelector("[data-sessions]");
  if (sessionsEl && window.Intl) {
    var sessions = [
      { id: "sydney", tz: "Australia/Sydney", open: 7, close: 16 },
      { id: "tokyo", tz: "Asia/Tokyo", open: 9, close: 18 },
      { id: "london", tz: "Europe/London", open: 8, close: 17 },
      { id: "newyork", tz: "America/New_York", open: 8, close: 17 }
    ];
    var parts = function (tz) {
      var f = new Intl.DateTimeFormat("en-GB", { timeZone: tz, weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false });
      var o = {};
      f.formatToParts(new Date()).forEach(function (p) { o[p.type] = p.value; });
      return o;
    };
    var update = function () {
      sessions.forEach(function (s) {
        var row = sessionsEl.querySelector("[data-session='" + s.id + "']");
        if (!row) return;
        var p = parts(s.tz);
        var h = parseInt(p.hour, 10) % 24 + parseInt(p.minute, 10) / 60;
        var weekend = p.weekday === "Sat" || p.weekday === "Sun";
        var open = !weekend && h >= s.open && h < s.close;
        row.classList.toggle("is-open", open);
        var st = row.querySelector(".session__state");
        if (st) st.textContent = open ? "Active" : "Closed";
        var lt = row.querySelector("[data-localtime]");
        if (lt) lt.textContent = p.weekday + " " + p.hour + ":" + p.minute + " local";
      });
    };
    update();
    setInterval(update, 30000);
  }

  /* ---- Third-party chart widgets (TradingView), lazy-loaded when visible ---- */
  var widgetsOn = document.body.getAttribute("data-price-widgets") === "on";
  var tvBoxes = document.querySelectorAll("[data-tv-widget]");
  var loadTv = function (box) {
    if (box.getAttribute("data-loaded")) return;
    box.setAttribute("data-loaded", "1");
    var cfgEl = box.querySelector("script[type='application/json']");
    var cfg = {};
    try { cfg = JSON.parse(cfgEl ? cfgEl.textContent : "{}"); } catch (e) { cfg = {}; }
    var container = document.createElement("div");
    container.className = "tradingview-widget-container";
    var inner = document.createElement("div");
    inner.className = "tradingview-widget-container__widget";
    inner.style.height = "100%";
    container.appendChild(inner);
    var s = document.createElement("script");
    s.src = "https://s3.tradingview.com/external-embedding/embed-widget-" + box.getAttribute("data-tv-widget") + ".js";
    s.async = true;
    s.textContent = JSON.stringify(cfg);
    s.onload = function () { box.classList.add("tv-loaded"); };
    container.appendChild(s);
    box.appendChild(container);
  };
  if (widgetsOn && tvBoxes.length) {
    if ("IntersectionObserver" in window) {
      var tvo = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { loadTv(en.target); tvo.unobserve(en.target); }
        });
      }, { rootMargin: "200px 0px" });
      tvBoxes.forEach(function (b) { tvo.observe(b); });
    } else {
      tvBoxes.forEach(loadTv);
    }
  }

  /* ---- News feed: renders only real items from /assets/data/news.json ---- */
  var feeds = document.querySelectorAll("[data-news-feed]");
  if (feeds.length && window.fetch) {
    var esc = function (t) { var d = document.createElement("div"); d.textContent = t == null ? "" : String(t); return d.innerHTML; };
    var ago = function (date) {
      var mins = Math.round((Date.now() - date.getTime()) / 60000);
      if (mins < 1) return "just now";
      if (mins < 60) return mins + " min ago";
      if (mins < 1440) return Math.round(mins / 60) + " h ago";
      return date.toLocaleDateString(undefined, { day: "numeric", month: "short" });
    };
    fetch(feeds[0].getAttribute("data-news-feed"), { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data || !Array.isArray(data.items)) return;
        var items = data.items.filter(function (it) {
          return it && it.title && it.source && it.published && /^https?:\/\//.test(it.url || "");
        });
        if (!items.length) return;
        feeds.forEach(function (feed) {
          var limit = parseInt(feed.getAttribute("data-news-limit") || "24", 10);
          var list = feed.querySelector(".news-feed");
          var empty = feed.querySelector(".news-empty");
          var stamp = feed.querySelector("[data-news-updated]");
          if (!list) return;
          list.innerHTML = items.slice(0, limit).map(function (it) {
            var date = new Date(it.published);
            var full = isNaN(date) ? "" : date.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
            return '<article class="card card--link news-card">' +
              (it.category ? '<span class="tag">' + esc(it.category) + "</span>" : "") +
              '<h3><a href="' + esc(it.url) + '" rel="noopener nofollow" target="_blank">' + esc(it.title) + "</a></h3>" +
              (it.summary ? "<p>" + esc(it.summary) + "</p>" : "") +
              '<div class="card__meta"><span class="src">' + esc(it.source) + "</span>" +
              (full ? '<time datetime="' + esc(it.published) + '" title="' + esc(full) + '">' + esc(ago(date)) + "</time>" : "") +
              "</div></article>";
          }).join("");
          list.hidden = false;
          if (empty) empty.hidden = true;
          if (stamp && data.updated) {
            var u = new Date(data.updated);
            if (!isNaN(u)) {
              stamp.textContent = "Headlines updated " + u.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" }) +
                " (your local time) · " + (data.source || "Public RSS feeds");
              stamp.hidden = false;
            }
          }
        });
      })
      .catch(function () { /* keep the transparent empty state */ });
  }

  /* ---- Blog: category filter, search, load more ---- */
  var blog = document.querySelector("[data-blog]");
  if (blog) {
    var cards = Array.prototype.slice.call(blog.querySelectorAll(".post-card"));
    var chips = blog.querySelectorAll(".chip");
    var search = blog.querySelector("input[type='search']");
    var more = blog.querySelector("[data-load-more]");
    var emptyMsg = blog.querySelector(".empty-state");
    var pageSize = parseInt(blog.getAttribute("data-page-size") || "6", 10);
    var shown = pageSize;
    var cat = "all";
    var apply = function () {
      var q = (search && search.value || "").trim().toLowerCase();
      var matches = cards.filter(function (c) {
        var okCat = cat === "all" || c.getAttribute("data-cat") === cat;
        var okQ = !q || c.textContent.toLowerCase().indexOf(q) > -1;
        c.classList.toggle("is-hidden", !(okCat && okQ));
        return okCat && okQ;
      });
      matches.forEach(function (c, i) { c.classList.toggle("is-paged", i >= shown); });
      if (more) more.parentNode.hidden = matches.length <= shown;
      if (emptyMsg) emptyMsg.hidden = matches.length > 0;
    };
    chips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        chips.forEach(function (o) { o.setAttribute("aria-pressed", "false"); });
        ch.setAttribute("aria-pressed", "true");
        cat = ch.getAttribute("data-filter");
        shown = pageSize;
        apply();
      });
    });
    if (search) search.addEventListener("input", function () { shown = pageSize; apply(); });
    if (more) more.addEventListener("click", function () {
      var before = shown;
      shown += pageSize;
      apply();
      var next = cards.filter(function (c) { return !c.classList.contains("is-hidden"); })[before];
      if (next) { var a = next.querySelector("a"); if (a) a.focus(); }
    });
    apply();
  }
})();

/* Lazy-load heavy 3D scripts so the intro animation has the main thread to itself */
(function () {
  "use strict";
  var els = document.querySelectorAll("[data-lazy-js]");
  if (!els.length) return;
  var h = document.documentElement;
  function load(src) { var s = document.createElement("script"); s.src = src; s.async = true; document.body.appendChild(s); }
  function afterIntro(cb) {
    var t0 = Date.now();
    (function chk() { if (!h.classList.contains("intro-wait") || Date.now() - t0 > 1500) cb(); else setTimeout(chk, 40); })();
  }
  var idle = window.requestIdleCallback || function (f) { return setTimeout(f, 1); };
  Array.prototype.forEach.call(els, function (el) {
    var src = el.getAttribute("data-src"), when = el.getAttribute("data-when");
    if (when === "idle") { afterIntro(function () { setTimeout(function () { idle(function () { load(src); }, { timeout: 400 }); }, 250); }); return; }
    var target = document.querySelector(when);
    if (!target || !("IntersectionObserver" in window)) { afterIntro(function () { load(src); }); return; }
    var io = new IntersectionObserver(function (en) {
      for (var i = 0; i < en.length; i++) if (en[i].isIntersecting) { io.disconnect(); idle(function () { load(src); }, { timeout: 300 }); return; }
    }, { rootMargin: "700px 0px" });
    io.observe(target);
  });
})();

/* =====================================================================
   Premium motion layer — all effects respect prefers-reduced-motion
   ===================================================================== */
(function () {
  "use strict";
  var mm = window.matchMedia ? function (q) { return window.matchMedia(q).matches; } : function () { return false; };
  var reduce = mm("(prefers-reduced-motion: reduce)");
  var fine = mm("(hover: hover) and (pointer: fine)");
  var header = document.querySelector(".site-header");

  /* stagger index for reveals that share a parent */
  var groups = new Map();
  Array.prototype.forEach.call(document.querySelectorAll(".reveal"), function (el) {
    var p = el.parentNode, n = groups.get(p) || 0; groups.set(p, n + 1); el.style.setProperty("--i", Math.min(n, 6));
  });

  /* word-by-word scroll statement */
  var stmts = [];
  Array.prototype.forEach.call(document.querySelectorAll("[data-words]"), function (el) {
    function wrap(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (ch) {
        if (ch.nodeType === 3) {
          var frag = document.createDocumentFragment();
          ch.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var sp = document.createElement("span"); sp.className = "w"; sp.textContent = part; frag.appendChild(sp);
          });
          node.replaceChild(frag, ch);
        } else if (ch.nodeType === 1) wrap(ch);
      });
    }
    wrap(el);
    stmts.push({ sec: el.closest(".statement") || el, words: el.querySelectorAll(".w"), lit: -1 });
  });

  /* reading progress bar on articles */
  var bar = null, art = document.querySelector(".article-layout .prose");
  if (art) { bar = document.createElement("div"); bar.className = "read-progress"; bar.setAttribute("aria-hidden", "true"); document.body.appendChild(bar); }

  var ticking = false;
  function onScroll() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset, vh = window.innerHeight;
    if (header) header.classList.toggle("is-scrolled", y > 8);
    stmts.forEach(function (st) {
      var r = st.sec.getBoundingClientRect();
      var p = reduce ? 1 : Math.max(0, Math.min(1, (-r.top + vh * 0.25) / Math.max(1, r.height - vh * 0.9)));
      var n = Math.round(p * st.words.length);
      if (n !== st.lit) { for (var i = 0; i < st.words.length; i++) st.words[i].classList.toggle("on", i < n); st.lit = n; }
    });
    if (bar) {
      var ar = art.getBoundingClientRect();
      var prog = Math.max(0, Math.min(1, (vh * 0.3 - ar.top) / Math.max(1, ar.height - vh * 0.5)));
      bar.style.transform = "scaleX(" + prog.toFixed(4) + ")";
    }
  }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }
  window.addEventListener("scroll", req, { passive: true });
  window.addEventListener("resize", req);
  onScroll();

  if (reduce) return;

  /* buttery wheel scrolling (desktop mice/trackpads; touch keeps native momentum) */
  if (fine && !mm("(any-pointer: coarse)")) {
    var target = 0, cur = 0, running = false;
    var maxY = function () { return document.documentElement.scrollHeight - window.innerHeight; };
    var canScroll = function (el, dy) {
      while (el && el !== document.body && el !== document.documentElement) {
        if (el.scrollHeight > el.clientHeight + 1) {
          var oy = getComputedStyle(el).overflowY;
          if ((oy === "auto" || oy === "scroll") && ((dy < 0 && el.scrollTop > 0) || (dy > 0 && el.scrollTop + el.clientHeight < el.scrollHeight - 1))) return true;
        }
        el = el.parentElement;
      }
      return false;
    };
    var step = function () {
      cur += (target - cur) * 0.12;
      if (Math.abs(target - cur) < 0.4) { cur = target; running = false; }
      window.scrollTo({ top: cur, left: 0, behavior: "instant" });
      if (running) requestAnimationFrame(step);
    };
    window.addEventListener("wheel", function (e) {
      if (e.ctrlKey || e.defaultPrevented || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      if (document.body.classList.contains("nav-open") || canScroll(e.target, e.deltaY)) return;
      if (e.target.closest && e.target.closest("iframe, .tradingview-widget-container, [data-native-scroll]")) return;
      e.preventDefault();
      var d = e.deltaY * (e.deltaMode === 1 ? 36 : e.deltaMode === 2 ? window.innerHeight : 1);
      if (!running) { cur = target = window.scrollY; }
      target = Math.max(0, Math.min(maxY(), target + d));
      if (!running) { running = true; requestAnimationFrame(step); }
    }, { passive: false });
    ["keydown", "mousedown", "touchstart"].forEach(function (ev) { window.addEventListener(ev, function () { running = false; }, { passive: true }); });
  }

  if (!fine) return;

  /* cursor spotlight on cards */
  var spot = null, sx = 0, sy = 0, sraf = 0;
  document.addEventListener("pointermove", function (e) {
    var c = e.target.closest && e.target.closest(".card, .tier, .offer-box");
    if (!c) return; spot = c; sx = e.clientX; sy = e.clientY;
    if (!sraf) sraf = requestAnimationFrame(function () {
      sraf = 0; var r = spot.getBoundingClientRect();
      spot.style.setProperty("--mx", (sx - r.left) + "px"); spot.style.setProperty("--my", (sy - r.top) + "px");
    });
  }, { passive: true });

  /* magnetic primary buttons */
  Array.prototype.forEach.call(document.querySelectorAll(".magnetic"), function (b) {
    var r = null;
    b.addEventListener("pointerenter", function () { r = b.getBoundingClientRect(); b.style.transition = "transform .25s var(--ease-out)"; });
    b.addEventListener("pointermove", function (e) {
      if (!r) return;
      var x = (e.clientX - r.left - r.width / 2) / r.width, y = (e.clientY - r.top - r.height / 2) / r.height;
      b.style.transform = "translate(" + (x * 10).toFixed(1) + "px," + (y * 8).toFixed(1) + "px)";
    });
    b.addEventListener("pointerleave", function () { r = null; b.style.transition = "transform .7s var(--ease-spring)"; b.style.transform = ""; });
  });

  /* 3D tilt on the chat preview: eased in rAF, rect read once per hover */
  Array.prototype.forEach.call(document.querySelectorAll("[data-tilt]"), function (el) {
    var base = el.classList.contains("mock-wrap--compact") ? [6, -10] : [4, -5];
    var cx = base[0], cy = base[1], tx = cx, ty = cy, rect = null, raf = 0;
    function loop() {
      cx += (tx - cx) * 0.1; cy += (ty - cy) * 0.1;
      el.style.setProperty("--rx", cx.toFixed(3) + "deg"); el.style.setProperty("--ry", cy.toFixed(3) + "deg");
      raf = (Math.abs(tx - cx) + Math.abs(ty - cy) > 0.01) ? requestAnimationFrame(loop) : 0;
    }
    function go() { if (!raf) raf = requestAnimationFrame(loop); }
    el.addEventListener("pointerenter", function () { rect = el.getBoundingClientRect(); });
    el.addEventListener("pointermove", function (e) {
      if (!rect) rect = el.getBoundingClientRect();
      var x = (e.clientX - rect.left) / rect.width - 0.5, y = (e.clientY - rect.top) / rect.height - 0.5;
      ty = x * 14; tx = -y * 10; go();
    });
    el.addEventListener("pointerleave", function () { rect = null; tx = base[0]; ty = base[1]; go(); });
  });
})();

/* free GPU layers once intro animations finish */
(function () {
  document.addEventListener("animationend", function (e) {
    var t = e.target; if (t.classList && (t.classList.contains("ht-in") || t.classList.contains("intro"))) { t.style.willChange = "auto"; t.style.filter = "none"; }
  });
  var gb = document.querySelector(".globe-box");
  if (gb) gb.addEventListener("transitionend", function (e) { if (e.propertyName === "filter" && gb.classList.contains("on")) gb.classList.add("settled"); });
})();

/* look preview switch */
(function () {
  if (!document.documentElement.classList.contains("look-elegant")) return;
  var d = document.createElement("div"); d.className = "look-switch";
  d.innerHTML = 'Elegant look preview <a href="?look=original">Back to original</a>';
  document.body.appendChild(d);
})();
