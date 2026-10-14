/* XAUUSD Global — rotating dotted globe with gold trading hubs and animated arcs.
   Canvas 2D, no libraries. Drag to rotate; respects reduced motion; pauses off-screen. */
(function () {
  "use strict";
  var cv = document.getElementById("globe");
  if (!cv || !cv.getContext) return;
  var ctx = cv.getContext("2d");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var D2R = Math.PI / 180;

  var HUBS = [
    ["London", 51.5, -0.1], ["New York", 40.7, -74.0], ["Zürich", 47.4, 8.5], ["Dubai", 25.2, 55.3],
    ["Mumbai", 19.1, 72.9], ["Singapore", 1.35, 103.8], ["Hong Kong", 22.3, 114.2], ["Tokyo", 35.7, 139.7],
    ["Sydney", -33.9, 151.2], ["Shanghai", 31.2, 121.5], ["Chicago", 41.9, -87.6], ["Johannesburg", -26.2, 28.0]
  ];
  var LINKS = [[0, 1], [0, 2], [0, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [2, 3], [1, 10], [6, 9], [0, 11], [1, 7], [5, 8]];

  // Fibonacci sphere of dots
  var N = window.innerWidth < 760 ? 900 : 1500, DOTS = [];
  for (var i = 0; i < N; i++) {
    var y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), th = Math.PI * (3 - Math.sqrt(5)) * i;
    DOTS.push([Math.cos(th) * r, y, Math.sin(th) * r]);
  }
  function ll2v(lat, lon) {
    var la = lat * D2R, lo = lon * D2R;
    return [Math.cos(la) * Math.sin(lo), Math.sin(la), Math.cos(la) * Math.cos(lo)];
  }
  var HV = HUBS.map(function (h) { return ll2v(h[1], h[2]); });
  function slerp(a, b, t) {
    var d = Math.max(-1, Math.min(1, a[0] * b[0] + a[1] * b[1] + a[2] * b[2])), w = Math.acos(d);
    if (w < 1e-4) return a.slice();
    var s = Math.sin(w), k1 = Math.sin((1 - t) * w) / s, k2 = Math.sin(t * w) / s;
    return [a[0] * k1 + b[0] * k2, a[1] * k1 + b[1] * k2, a[2] * k1 + b[2] * k2];
  }
  var ARCS = LINKS.map(function (l, k) {
    var a = HV[l[0]], b = HV[l[1]], pts = [];
    var d = Math.acos(Math.max(-1, Math.min(1, a[0] * b[0] + a[1] * b[1] + a[2] * b[2])));
    for (var j = 0; j <= 48; j++) {
      var t = j / 48, p = slerp(a, b, t), lift = 1 + Math.sin(Math.PI * t) * (0.12 + d * 0.12);
      pts.push([p[0] * lift, p[1] * lift, p[2] * lift]);
    }
    return { pts: pts, off: k * 0.37 };
  });

  var rotY = -0.35, rotX = 0.38, vel = 0.0022, drag = null, W = 0, H = 0, R = 0, dpr = 1;
  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    R = Math.min(W, H) * 0.34;
  }
  if ("ResizeObserver" in window) new ResizeObserver(resize).observe(cv); else window.addEventListener("resize", resize);
  resize();

  function proj(v) {
    var cy = Math.cos(rotY), sy = Math.sin(rotY), cx = Math.cos(rotX), sx = Math.sin(rotX);
    var x = v[0] * cy + v[2] * sy, z = -v[0] * sy + v[2] * cy, y = v[1];
    var y2 = y * cx - z * sx, z2 = y * sx + z * cx;
    return [W / 2 + x * R, H / 2 - y2 * R, z2];
  }

  cv.addEventListener("pointerdown", function (e) { drag = [e.clientX, e.clientY, rotY, rotX]; cv.setPointerCapture(e.pointerId); });
  cv.addEventListener("pointermove", function (e) {
    if (!drag) return;
    rotY = drag[2] + (e.clientX - drag[0]) * 0.006;
    rotX = Math.max(-1.1, Math.min(1.1, drag[3] + (e.clientY - drag[1]) * 0.004));
  });
  function endDrag() { drag = null; }
  cv.addEventListener("pointerup", endDrag); cv.addEventListener("pointercancel", endDrag);

  var visible = true, raf = 0, t0 = performance.now();
  function frame(now) {
    var t = Math.max(0, (now - t0) / 1000);
    if (!drag && !reduce) rotY += vel;
    ctx.clearRect(0, 0, W, H);

    // atmosphere glow
    var g = ctx.createRadialGradient(W / 2, H / 2, R * 0.85, W / 2, H / 2, R * 1.35);
    g.addColorStop(0, "rgba(242,193,78,0.16)"); g.addColorStop(1, "rgba(242,193,78,0)");
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(W / 2, H / 2, R * 1.35, 0, Math.PI * 2); ctx.fill();
    // sphere body
    var b = ctx.createRadialGradient(W / 2 - R * 0.35, H / 2 - R * 0.4, R * 0.1, W / 2, H / 2, R);
    b.addColorStop(0, "#1b1d22"); b.addColorStop(1, "#0b0c0f");
    ctx.fillStyle = b; ctx.beginPath(); ctx.arc(W / 2, H / 2, R, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "rgba(242,193,78,0.25)"; ctx.lineWidth = 1; ctx.stroke();

    // dots
    for (var i = 0; i < DOTS.length; i++) {
      var p = proj(DOTS[i]);
      if (p[2] < -0.05) continue;
      var a = 0.12 + 0.55 * Math.max(0, p[2]);
      ctx.fillStyle = "rgba(220,214,200," + a.toFixed(3) + ")";
      ctx.fillRect(p[0] - 0.9, p[1] - 0.9, 1.8, 1.8);
    }

    // arcs
    ARCS.forEach(function (arc) {
      var ps = arc.pts.map(proj);
      ctx.lineWidth = 1.3;
      for (var j = 1; j < ps.length; j++) {
        if (ps[j][2] < -0.15 || ps[j - 1][2] < -0.15) continue;
        ctx.strokeStyle = "rgba(242,193,78," + (0.18 + 0.25 * Math.max(0, ps[j][2])).toFixed(3) + ")";
        ctx.beginPath(); ctx.moveTo(ps[j - 1][0], ps[j - 1][1]); ctx.lineTo(ps[j][0], ps[j][1]); ctx.stroke();
      }
      // travelling pulse
      var u = reduce ? 0.5 : (((t * 0.35 + arc.off) % 1) + 1) % 1;
      var k = Math.floor(u * (ps.length - 1)), q = ps[k];
      if (q[2] > -0.1) {
        var gl = ctx.createRadialGradient(q[0], q[1], 0, q[0], q[1], 9);
        gl.addColorStop(0, "rgba(255,224,138,0.95)"); gl.addColorStop(1, "rgba(255,224,138,0)");
        ctx.fillStyle = gl; ctx.beginPath(); ctx.arc(q[0], q[1], 9, 0, Math.PI * 2); ctx.fill();
      }
    });

    // hubs
    ctx.font = "600 12px Inter, system-ui, sans-serif";
    HUBS.forEach(function (h, idx) {
      var p = proj(HV[idx]);
      if (p[2] < 0.02) return;
      var pulse = reduce ? 0 : (Math.sin(t * 2 + idx) + 1) / 2;
      ctx.fillStyle = "rgba(242,193,78," + (0.18 + 0.2 * pulse).toFixed(3) + ")";
      ctx.beginPath(); ctx.arc(p[0], p[1], 7 + pulse * 5, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#f2c14e"; ctx.beginPath(); ctx.arc(p[0], p[1], 3.4, 0, Math.PI * 2); ctx.fill();
      if (p[2] > 0.35) {
        ctx.fillStyle = "rgba(243,241,234," + Math.min(1, (p[2] - 0.35) * 2.2).toFixed(3) + ")";
        ctx.fillText(h[0], p[0] + 9, p[1] - 7);
      }
    });

    if (!reduce && visible && !document.hidden) raf = requestAnimationFrame(frame); else raf = 0;
  }
  function kick() { if (!raf && visible && !document.hidden) raf = requestAnimationFrame(frame); }
  if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; kick(); }).observe(cv);
  document.addEventListener("visibilitychange", kick);
  raf = requestAnimationFrame(frame);
})();
