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

/* 3D tilt: chat preview and hero chart follow the pointer (desktop only, respects reduced motion) */
(function () {
  if (!window.matchMedia || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
  var els = document.querySelectorAll("[data-tilt], .hero__visual");
  Array.prototype.forEach.call(els, function (el) {
    var base = el.classList.contains("hero__visual") ? [4, -8] : el.classList.contains("mock-wrap--compact") ? [6, -10] : [4, -5];
    el.addEventListener("pointermove", function (e) {
      var r = el.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      el.classList.add("is-tilting");
      el.style.setProperty("--ry", (x * 14).toFixed(2) + "deg");
      el.style.setProperty("--rx", (-y * 10).toFixed(2) + "deg");
    });
    el.addEventListener("pointerleave", function () {
      el.classList.remove("is-tilting");
      el.style.setProperty("--ry", base[1] + "deg");
      el.style.setProperty("--rx", base[0] + "deg");
    });
  });
})();
