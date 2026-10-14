/* XAUUSD Global — "Look inside" interactive room preview.
   Renders sample rooms from embedded JSON, streams messages in like a live chat,
   unfolds the app window in 3D on scroll. Transform/opacity only; respects reduced motion. */
(function () {
  "use strict";
  var app = document.querySelector("[data-app]");
  var src = document.getElementById("inside-data");
  if (!app || !src) return;
  var D = JSON.parse(src.textContent);
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var M = {}; D.members.forEach(function (m) { M[m.id] = m; });
  M.goldie = { id: "goldie", name: "Goldie", handle: "Goldie", level: "AI mentor", color: "#f2c14e", cc: "AI", ai: true };
  var $ = function (s, r) { return (r || app).querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var LV = { Starter: "lv-s", Advanced: "lv-a", Pro: "lv-p", Degen: "lv-d", Mentor: "lv-m", "AI mentor": "lv-ai" };
  var ICON = {
    hash: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 4L7 20M17 4l-2 16M4 9h17M3 15h17"/></svg>',
    lock: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
    reply: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 9V5l-7 7 7 7v-4.1c5 0 8.5 1.6 11 5.1-1-5-4-10-11-11z"/></svg>'
  };

  /* ---------- sidebar ---------- */
  var groups = [], gi = {};
  D.rooms.forEach(function (r) { if (!(r.group in gi)) { gi[r.group] = groups.length; groups.push({ name: r.group, rooms: [] }); } groups[gi[r.group]].rooms.push(r); });
  var side = $("[data-rooms]"), html = "";
  groups.forEach(function (g) {
    html += '<div class="rg"><div class="rg__k">' + esc(g.name) + "</div>";
    g.rooms.forEach(function (r) {
      html += '<button type="button" class="rm" data-room="' + r.id + '">' + ICON.hash + "<span>" + esc(r.name) + "</span>" +
        (r.live ? '<em class="rm__live">LIVE</em>' : '<em class="rm__new" data-new></em>') + "</button>";
    });
    html += "</div>";
  });
  html += '<div class="rg"><div class="rg__k">Unlock as you grow</div><button type="button" class="rm rm--locked" disabled>' + ICON.lock + '<span>degen-lab</span></button><button type="button" class="rm rm--locked" disabled>' + ICON.lock + "<span>mentor-circle</span></button></div>";
  side.innerHTML = html;

  /* ---------- message renderers ---------- */
  function who(m) {
    var u = M[m.from] || M.goldie;
    var av = '<div class="msg__av' + (u.ai ? " msg__av--ai" : "") + '" style="--c:' + u.color + '" aria-hidden="true">' + (u.ai ? "AI" : esc(u.name.charAt(0))) + "</div>";
    var meta = '<div class="msg__meta"><b>' + esc(u.ai ? "Goldie" : u.handle) + '</b><span class="lv ' + (LV[u.level] || "") + '">' + esc(u.level) + "</span>" +
      (u.ai || u.id === "__you" ? "" : '<span class="cc">' + esc(u.cc) + "</span>") + "<time>" + esc(m.time || "") + "</time></div>";
    return { av: av, meta: meta, ai: !!u.ai };
  }
  function reacts(m) {
    var out = "";
    if (m.reactions && m.reactions.length) out += m.reactions.map(function (r) { return '<span class="re">' + esc(r[0]) + " " + r[1] + "</span>"; }).join("");
    if (m.replies) out += '<span class="re re--th">' + ICON.reply + m.replies + " replies</span>";
    return out ? '<div class="msg__re">' + out + "</div>" : "";
  }
  function num(v) { return parseFloat(String(v).replace(/,/g, "")); }
  function chartSVG(m) {
    var lv = {}; (m.levels || []).forEach(function (l) { lv[l[0]] = num(l[1]); });
    var E = lv.Entry, S = lv.Stop, T = lv.Target, long = m.bias === "long", dir = long ? 1 : -1;
    var R = Math.abs(E - S) || 5, span = Math.abs(T - E) || R * 2;
    var vals = [E, S, T].filter(function (v) { return !isNaN(v); });
    var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), pad = (hi - lo) * 0.18 + R * 0.3; lo -= pad; hi += pad;
    var seed = (m.time || "x").length * 7 + (m.from || "").length * 13 + Math.round(E);
    function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
    var n = 22, keys = [[0, E + dir * 0.35 * span], [9, S + dir * 0.12 * R], [n - 1, E]], cs = [], prev = keys[0][1];
    function path(i) { for (var k = 0; k < keys.length - 1; k++) if (i <= keys[k + 1][0]) { var t = (i - keys[k][0]) / (keys[k + 1][0] - keys[k][0]); return keys[k][1] + (keys[k + 1][1] - keys[k][1]) * t; } return E; }
    var noise = Math.max(R * 0.45, span * 0.05);
    for (var i = 0; i < n; i++) {
      var c = i === n - 1 ? E : path(i) + (rnd() - 0.5) * noise, o = prev;
      var hh = Math.max(o, c) + rnd() * noise * 0.5, ll = Math.min(o, c) - rnd() * noise * 0.5;
      if (i === 9) { if (long) ll = Math.max(S + R * 0.04, Math.min(ll, S + R * 0.08)); else hh = Math.min(S - R * 0.04, Math.max(hh, S - R * 0.08)); }
      cs.push([o, c, Math.min(hi, hh), Math.max(lo, ll)]); prev = c;
    }
    var W = 440, H = 170, top = 12, bot = 22, y = function (v) { return top + (hi - v) / (hi - lo) * (H - top - bot); }, cw = (W - 130) / n;
    var s = '<svg class="mchart" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="' + esc(m.tf + " " + (long ? "long" : "short") + " idea chart") + '">';
    cs.forEach(function (k, i) {
      var x = 10 + i * cw + cw / 2, up = k[1] >= k[0], col = up ? "#3ccf91" : "#ef6461";
      s += '<line x1="' + x.toFixed(1) + '" x2="' + x.toFixed(1) + '" y1="' + y(k[2]).toFixed(1) + '" y2="' + y(k[3]).toFixed(1) + '" stroke="' + col + '" stroke-width="1.4"/>';
      s += '<rect x="' + (x - cw * 0.32).toFixed(1) + '" y="' + Math.min(y(k[0]), y(k[1])).toFixed(1) + '" width="' + (cw * 0.64).toFixed(1) + '" height="' + Math.max(2, Math.abs(y(k[0]) - y(k[1]))).toFixed(1) + '" rx="1.5" fill="' + col + '"/>';
    });
    var colr = { Entry: "#f3f1ea", Stop: "#ef6461", Target: "#3ccf91" }, labs = [];
    (m.levels || []).forEach(function (L) { var v = lv[L[0]]; if (isNaN(v) || !colr[L[0]]) return; labs.push({ k: L[0], t: L[1], y: y(v) }); });
    labs.forEach(function (l) { s += '<line x1="10" x2="' + (W - 122) + '" y1="' + l.y.toFixed(1) + '" y2="' + l.y.toFixed(1) + '" stroke="' + colr[l.k] + '" stroke-dasharray="4 4" stroke-width="1.2" opacity=".9"/>'; });
    labs.sort(function (a, b) { return a.y - b.y; });
    for (var j = 1; j < labs.length; j++) if (labs[j].y - labs[j - 1].y < 14) labs[j].ly = (labs[j - 1].ly || labs[j - 1].y) + 14;
    labs.forEach(function (l) { var ly = l.ly || l.y; s += '<text class="lvl" x="' + (W - 116) + '" y="' + (ly + 4).toFixed(1) + '" fill="' + colr[l.k] + '" font-size="11" font-family="JetBrains Mono, monospace">' + esc(l.k.toUpperCase() + " " + l.t) + "</text>"; });
    s += '<text x="12" y="' + (H - 6) + '" fill="#8a8983" font-size="10" font-family="JetBrains Mono, monospace">XAUUSD · ' + esc(m.tf || "") + "</text></svg>";
    return s;
  }
  function body(m) {
    switch (m.type) {
      case "plan":
        return '<div class="card-plan"><div class="card-plan__t">' + esc(m.title) + "</div><p>" + esc(m.text) + '</p><dl>' +
          m.rows.map(function (r) { return "<div><dt>" + esc(r[0]) + "</dt><dd>" + esc(r[1]) + "</dd></div>"; }).join("") + "</dl></div>";
      case "lesson":
        return '<div class="card-lesson"><span>SAVED LESSON</span><b>' + esc(m.title.replace(/^Saved lesson:\s*/i, "")) + "</b><p>" + esc(m.text) + "</p></div>";
      case "poll":
        return '<div class="card-poll"><b>' + esc(m.question) + "</b>" + m.options.map(function (o) {
          return '<div class="pb"><i style="--w:' + o[1] + '%"></i><span>' + esc(o[0]) + "</span><em>" + o[1] + "%</em></div>"; }).join("") + "<small>" + m.votes + " votes</small></div>";
      case "chart":
        return "<p>" + esc(m.text) + '</p><div class="card-chart">' + chartSVG(m) + '<div class="card-chart__lv">' +
          m.levels.map(function (l) { return "<span>" + esc(l[0]) + "<b>" + esc(l[1]) + "</b></span>"; }).join("") + "</div></div>";
      case "review":
        return "<p>" + esc(m.text) + '</p><ul class="card-checks">' + m.checks.map(function (c) { return '<li class="' + (c[0] ? "ok" : "no") + '">' + esc(c[1]) + "</li>"; }).join("") + "</ul>";
      case "recap":
        var cls = m.result === "win" ? "win" : m.result === "loss" ? "loss" : "be";
        return '<div class="card-recap card-recap--' + cls + '"><div class="card-recap__top"><span class="fd-dir fd-dir--' + (m.dir === "Long" ? "long" : "short") + '">' + esc(m.dir.toUpperCase()) +
          '</span><span class="card-recap__lbl">Trade recap</span><b class="fd-r fd-r--' + cls + '">' + esc(m.r) + '</b></div><div class="fd-recap__grid"><span>Entry<b>' + esc(m.entry) + "</b></span><span>Stop<b>" + esc(m.sl) +
          "</b></span><span>Exit<b>" + esc(m.exit) + "</b></span></div><p>" + esc(m.note) + "</p></div>";
      case "live":
        return '<div class="card-live"><span class="fd-live__badge"><i></i>LIVE</span><b>' + esc(m.title) + "</b><span>" + m.viewers + " watching · join the thread</span></div>";
      default:
        return "<p>" + esc(m.text) + "</p>";
    }
  }
  function renderMsg(m) {
    var el = document.createElement("article");
    if (m.type === "mod") { el.className = "msg msg--mod"; el.innerHTML = '<div class="msg__av msg__av--ai" aria-hidden="true">AI</div><div class="msg__c"><div class="msg__meta"><b>Goldie</b><span class="lv lv-ai">Auto-mod</span><time>' + esc(m.time) + '</time></div><p class="mod">' + esc(m.text) + "</p></div>"; return el; }
    var w = who(m);
    el.className = "msg" + (w.ai ? " msg--ai" : "") + " msg--" + m.type;
    el.innerHTML = w.av + '<div class="msg__c">' + w.meta + '<div class="msg__b">' + body(m) + "</div>" + reacts(m) + "</div>";
    return el;
  }

  /* ---------- room playback ---------- */
  var thread = $("[data-thread]"), typing = $("[data-typing]"), typingName = $("[data-typing-name]"), pin = $("[data-pin]");
  var timer = 0, visible = false, cur = null, queue = [];
  function scrollEnd() { thread.scrollTo({ top: thread.scrollHeight, behavior: reduce ? "auto" : "smooth" }); }
  function add(m, animate) {
    var el = renderMsg(m); if (animate && !reduce) el.classList.add("msg--in");
    thread.appendChild(el); scrollEnd();
  }
  function step() {
    timer = 0;
    if (!queue.length || !visible) { typing.hidden = true; return; }
    var m = queue[0], u = M[m.from] || M.goldie;
    typingName.textContent = (m.type === "mod" || u.ai ? "Goldie" : u.handle) + " is typing…";
    typing.hidden = false;
    var len = (m.text || m.note || m.question || m.title || "").length;
    timer = setTimeout(function () {
      typing.hidden = true; add(queue.shift(), true);
      timer = setTimeout(step, 900 + Math.random() * 700);
    }, Math.min(2400, 700 + len * 9));
  }
  function open(id) {
    var r = D.rooms.filter(function (x) { return x.id === id; })[0]; if (!r) return;
    cur = id; clearTimeout(timer);
    Array.prototype.forEach.call(side.querySelectorAll(".rm"), function (b) { var on = b.getAttribute("data-room") === id; b.classList.toggle("on", on); b.setAttribute("aria-current", on ? "true" : "false"); if (on) { var n = b.querySelector("[data-new]"); if (n) n.remove(); } });
    $("[data-room-name]").textContent = "# " + r.name; $("[data-room-desc]").textContent = r.desc || "";
    if (r.pinned) { pin.hidden = false; pin.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 4l5 5-3 1-4 4 1 5-2 1-3-4-5 5-1-1 5-5-4-3 1-2 5 1 4-4z"/></svg><span>' + esc(r.pinned) + "</span>"; } else pin.hidden = true;
    thread.innerHTML = "";
    var first = reduce ? r.messages.length : Math.min(3, r.messages.length);
    r.messages.slice(0, first).forEach(function (m) { add(m, false); });
    queue = r.messages.slice(first);
    thread.scrollTop = thread.scrollHeight;
    if (visible) timer = setTimeout(step, 800);
    var rl = document.querySelector(".rail-card--live .rail-k"); if (rl) rl.lastChild.textContent = id === "live" ? "LIVE NOW" : "LIVE TODAY · 5:30 PM IST";
  }
  side.addEventListener("click", function (e) { var b = e.target.closest(".rm"); if (b && !b.disabled) open(b.getAttribute("data-room")); });
  open("plan");

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (en) {
      var v = en[0].isIntersecting; if (v === visible) return; visible = v;
      if (visible && !timer && queue.length) timer = setTimeout(step, 600);
      if (!visible) { clearTimeout(timer); timer = 0; typing.hidden = true; }
    }, { threshold: 0.25 }).observe(app);
  } else visible = true;

  /* compose: try it yourself, with real sample answers */
  M.__you = { id: "__you", name: "You", handle: "You", level: "Starter", color: "#e0a73a", cc: "··" };
  var CHIPS = [
    ["What's a liquidity sweep?", "A sweep is when price briefly trades beyond an obvious high or low, where lots of stop orders sit, then snaps back inside. The tell is a long wick and a fast close back in the range. What matters next is whether price displaces away from it, ideally leaving a fair value gap."],
    ["Is my stop too tight?", "Compare it with the market's normal noise. If your stop is smaller than about half of the current M15 ATR, a normal wiggle can take you out. Put the stop where your idea is truly wrong, then reduce the lot size so your risk in dollars stays the same."],
    ["How do I handle CPI days?", "Plan it, don't gamble it. Know the release time, decide beforehand whether you'll be flat, reduced or holding, and let the first spike settle before reading direction. Many traders wait for the retest of the first fair value gap after the release."],
    ["Should I buy gold now?", "I never tell anyone to buy or sell. What I can do is help you build your own plan: the context, the level where you'd be wrong, and a size that keeps the risk small. Post your chart in #chart-reviews and I'll check the reasoning with you."]
  ];
  var chipsEl = document.createElement("div"); chipsEl.className = "app__chips";
  chipsEl.innerHTML = '<span>Try asking Goldie:</span>' + CHIPS.map(function (c, i) { return '<button type="button" data-chip="' + i + '">' + esc(c[0]) + "</button>"; }).join("");
  var form = $("[data-compose]"); form.parentNode.insertBefore(chipsEl, form);
  var pending = false, asked = 0;
  function ask(q, a) {
    if (pending) return; pending = true;
    clearTimeout(timer); timer = 0; queue = [];
    add({ type: "text", from: "__you", time: "Just now", text: q }, true);
    typing.hidden = false; typingName.textContent = "Goldie is typing…";
    setTimeout(function () {
      typing.hidden = true; pending = false; asked++;
      add({ type: "text", from: "goldie", time: "Just now", text: a }, true);
      if (asked === 1) {
        var bar = document.createElement("div"); bar.className = "app__join";
        bar.innerHTML = '<span><b>Your seat is waiting.</b> First 50 members get 3 months free.</span><a class="btn btn--gold btn--sm" href="/membership/#registration">Claim my spot</a>';
        form.parentNode.insertBefore(bar, form); 
      }
    }, 1400);
  }
  chipsEl.addEventListener("click", function (e) { var b = e.target.closest("[data-chip]"); if (b) { var c = CHIPS[+b.getAttribute("data-chip")]; ask(c[0], c[1]); } });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var inp = $("#app-msg"), t = inp.value.trim(); if (!t || pending) return; inp.value = "";
    ask(t, "Good question. In the live community I'd answer this in seconds with an explanation you can use on your own chart (never a buy or sell call), and mentors and members can add their view in the thread.");
  });

  /* rail: online, leaders, live viewers */
  var online = D.members.slice(0, 14);
  $("[data-online]").innerHTML = online.map(function (u) { return '<span class="on-av" style="--c:' + u.color + '" title="' + esc(u.handle + " · " + u.country) + '">' + esc(u.name.charAt(0)) + "</span>"; }).join("") + '<span class="on-more">+' + (D.members.length - online.length) + "</span>";
  var leaders = D.members.filter(function (u) { return u.level !== "Mentor"; }).slice(0, 4);
  $("[data-lead]").innerHTML = leaders.map(function (u, i) { return '<li><span class="on-av" style="--c:' + u.color + '">' + esc(u.name.charAt(0)) + "</span>" + esc(u.handle) + "<b>" + (31 - i * 6) + " days</b></li>"; }).join("");
  var vEl = $("[data-viewers]"), vv = 87;
  if (!reduce) setInterval(function () { if (!visible) return; vv = Math.max(70, Math.min(110, vv + Math.round((Math.random() - 0.45) * 3))); vEl.textContent = vv; }, 2600);

  /* ---------- 3D unfold: one compositor-driven transition when the window enters view ---------- */
  var stage = document.querySelector(".stage");
  if (reduce || !stage) { if (stage) stage.classList.add("unfolded"); return; }
  if ("IntersectionObserver" in window) {
    var uo = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { stage.classList.add("unfolded"); uo.disconnect(); } }, { threshold: 0.12 });
    uo.observe(stage);
  } else stage.classList.add("unfolded");
})();
