/* XAUUSD Global — live gold market hours in the visitor's time zone.
   Pure Intl/Date maths (DST-correct), updates every second, no data feed. */
(function () {
  "use strict";
  var root = document.querySelector("[data-hours]");
  if (!root || !window.Intl) return;
  var SES = [
    { id: "sydney", tz: "Australia/Sydney", o: 7, c: 16 },
    { id: "tokyo", tz: "Asia/Tokyo", o: 9, c: 18 },
    { id: "london", tz: "Europe/London", o: 8, c: 17 },
    { id: "newyork", tz: "America/New_York", o: 8, c: 17 }
  ];
  var sel = root.querySelector("[data-tz]");
  var autoTz = (Intl.DateTimeFormat().resolvedOptions().timeZone) || "UTC";
  try { var saved = localStorage.getItem("xg-tz"); if (saved && sel.querySelector('option[value="' + saved + '"]')) sel.value = saved; } catch (e) {}
  sel.querySelector('option[value="auto"]').textContent = "Your time zone (" + autoTz.replace(/_/g, " ").split("/").pop() + ")";
  sel.addEventListener("change", function () { try { localStorage.setItem("xg-tz", sel.value); } catch (e) {} draw(true); });
  function tz() { return sel.value === "auto" ? autoTz : sel.value; }

  var fmtCache = {};
  function parts(ms, zone) {
    var f = fmtCache[zone] || (fmtCache[zone] = new Intl.DateTimeFormat("en-US", { timeZone: zone, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", weekday: "short" }));
    var o = {}; f.formatToParts(new Date(ms)).forEach(function (p) { o[p.type] = p.value; });
    return { y: +o.year, m: +o.month, d: +o.day, h: +o.hour % 24, mi: +o.minute, s: +o.second, wd: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(o.weekday) };
  }
  function offset(ms, zone) { var p = parts(ms, zone); return Date.UTC(p.y, p.m - 1, p.d, p.h, p.mi, p.s) - Math.floor(ms / 1000) * 1000; }
  function wall(y, m, d, h, zone) { // wall-clock time in zone -> UTC ms
    var g = Date.UTC(y, m - 1, d, h); var t = g - offset(g, zone); return g - offset(t, zone);
  }
  function addDays(p, n) { var t = new Date(Date.UTC(p.y, p.m - 1, p.d + n)); return { y: t.getUTCFullYear(), m: t.getUTCMonth() + 1, d: t.getUTCDate(), wd: t.getUTCDay() }; }
  function timeStr(ms, zone, sec) {
    return new Intl.DateTimeFormat(undefined, { timeZone: zone, hour: "numeric", minute: "2-digit", second: sec ? "2-digit" : undefined }).format(new Date(ms));
  }
  function dur(ms) {
    var m = Math.max(0, Math.round(ms / 60000)), h = Math.floor(m / 60), d = Math.floor(h / 24);
    if (d >= 1) return d + "d " + (h % 24) + "h";
    return h ? h + "h " + (m % 60) + "m" : m + "m";
  }
  // session occurrences (weekdays in the session's own zone) around now
  function occurrences(s, now) {
    var p = parts(now, s.tz), out = [];
    for (var k = -2; k <= 7; k++) {
      var q = addDays(p, k); if (q.wd === 0 || q.wd === 6) continue;
      out.push([wall(q.y, q.m, q.d, s.o, s.tz), wall(q.y, q.m, q.d, s.c, s.tz)]);
    }
    return out;
  }
  function goldOpen(now) { // Sun 18:00 NY -> Fri 17:00 NY, daily pause 17:00-18:00 NY
    var p = parts(now, "America/New_York");
    if (p.wd === 6) return false;
    if (p.wd === 5 && p.h >= 17) return false;
    if (p.wd === 0 && p.h < 18) return false;
    if (p.h === 17) return false;
    return true;
  }
  function nextGoldChange(now) { // scan minute steps on the hour
    var open = goldOpen(now), t = now - (now % 3600000); // NY changes state only on whole hours
    for (var i = 0; i < 24 * 4; i += 1) { t += 3600000; if (goldOpen(t) !== open) return t; }
    return now;
  }

  var $ = function (s) { return root.querySelector(s); };
  var clock = $("[data-clock]"), state = $("[data-state]"), sub = $("[data-sub]"), dot = $("[data-dot]"), nowEl = $("[data-now]"), best = $("[data-best]");
  var lastDay = "";
  function draw(force) {
    var now = Date.now(), zone = tz();
    clock.textContent = timeStr(now, zone, true);
    var open = goldOpen(now), nxt = nextGoldChange(now);
    root.classList.toggle("is-open", open); root.classList.toggle("is-closed", !open);
    var pNY = parts(now, "America/New_York");
    if (open) {
      state.textContent = "Gold market is open";
      var closingWeek = pNY.wd === 5;
      sub.textContent = (closingWeek ? "Closes for the weekend in " : "Daily pause in ") + dur(nxt - now) + " · at " + timeStr(nxt, zone);
    } else {
      state.textContent = (pNY.wd === 6 || (pNY.wd === 5 && pNY.h >= 17) || (pNY.wd === 0 && pNY.h < 18)) ? "Closed for the weekend" : "Daily pause";
      sub.textContent = "Opens in " + dur(nxt - now) + " · at " + timeStr(nxt, zone);
    }
    // timeline for the local day in the chosen zone
    var pl = parts(now, zone), d0 = wall(pl.y, pl.m, pl.d, 0, zone), d1 = d0 + 864e5;
    var dayKey = zone + pl.y + pl.m + pl.d;
    nowEl.style.left = "calc(var(--tl-label) + (100% - var(--tl-label)) * " + ((now - d0) / 864e5).toFixed(5) + ")";
    if (force || dayKey !== lastDay) {
      lastDay = dayKey;
      var lon = null, ny = null;
      SES.forEach(function (s) {
        var track = root.querySelector('[data-row="' + s.id + '"] .tl-track'); track.innerHTML = "";
        occurrences(s, now).forEach(function (o) {
          var a = Math.max(o[0], d0), b = Math.min(o[1], d1); if (b <= a) return;
          var bar = document.createElement("i"); bar.className = "tl-bar tl-bar--" + s.id;
          bar.style.left = ((a - d0) / 864e5 * 100).toFixed(3) + "%"; bar.style.width = ((b - a) / 864e5 * 100).toFixed(3) + "%";
          track.appendChild(bar);
        });
      });
      var ovT = $("[data-ov]"); ovT.innerHTML = "";
      var L1 = occurrences(SES[2], now), N1 = occurrences(SES[3], now), bestTxt = "";
      L1.forEach(function (l) { N1.forEach(function (n) {
        var a = Math.max(l[0], n[0]), b = Math.min(l[1], n[1]); if (b <= a) return;
        var ca = Math.max(a, d0), cb = Math.min(b, d1);
        if (cb > ca) { var bar = document.createElement("i"); bar.className = "tl-bar tl-bar--ov"; bar.style.left = ((ca - d0) / 864e5 * 100).toFixed(3) + "%"; bar.style.width = ((cb - ca) / 864e5 * 100).toFixed(3) + "%"; ovT.appendChild(bar); }
        if (!bestTxt && b > now) bestTxt = timeStr(a, zone) + " – " + timeStr(b, zone) + (a > now + 864e5 * 0.9 ? " (next trading day)" : "");
      }); });
      best.textContent = bestTxt || "—";
    }
    // session cards
    SES.forEach(function (s) {
      var card = root.querySelector('[data-s="' + s.id + '"]'), occ = occurrences(s, now), cur = null, next = null;
      occ.forEach(function (o) { if (now >= o[0] && now < o[1]) cur = o; else if (o[0] > now && !next) next = o; });
      var show = cur || next;
      card.classList.toggle("is-live", !!cur);
      card.querySelector(".sess-badge").textContent = cur ? "Open" : "Closed";
      card.querySelector("[data-time]").textContent = timeStr(show[0], zone) + " – " + timeStr(show[1], zone);
      card.querySelector("[data-cd]").textContent = cur ? "Closes in " + dur(cur[1] - now) : "Opens in " + dur(next[0] - now);
    });
  }
  draw(true);
  setInterval(function () { if (!document.hidden) draw(false); }, 1000);
})();
