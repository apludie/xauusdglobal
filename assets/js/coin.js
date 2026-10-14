/* XAUUSD Global — 3D "Founding 50" gold coin.
   Hand-written WebGL (no libraries). Embossed relief is drawn as a height map on a 2D canvas
   and turned into per-pixel normals in the shader; the metal is lit by a procedural studio
   environment so it reads as polished gold. Pointer tilts it, scrolling spins it.
   Pauses off-screen / hidden tab; one still frame for reduced motion; CSS fallback without WebGL. */
(function () {
  "use strict";
  var canvases = document.querySelectorAll("canvas.coin3d");
  if (!canvases.length) return;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function heightMap(front) {
    var S = 1024, P = 768, c = document.createElement("canvas"); c.width = c.height = P;
    var x = c.getContext("2d"), m = S / 2; x.setTransform(P / S, 0, 0, P / S, 0, 0);
    function g(v) { var k = Math.round(v * 255); return "rgb(" + k + "," + k + "," + k + ")"; }
    x.fillStyle = g(0.32); x.fillRect(0, 0, S, S);
    // machined concentric field
    for (var r = 30; r < m * 0.78; r += 7) { x.beginPath(); x.arc(m, m, r, 0, 6.2832); x.strokeStyle = g(r % 14 ? 0.35 : 0.29); x.lineWidth = 3; x.stroke(); }
    // rims
    x.beginPath(); x.arc(m, m, m * 0.94, 0, 6.2832); x.strokeStyle = g(1); x.lineWidth = m * 0.1; x.stroke();
    x.beginPath(); x.arc(m, m, m * 0.84, 0, 6.2832); x.strokeStyle = g(0.15); x.lineWidth = 8; x.stroke();
    x.beginPath(); x.arc(m, m, m * 0.81, 0, 6.2832); x.strokeStyle = g(0.8); x.lineWidth = 6; x.stroke();
    // dotted bead ring
    for (var i = 0; i < 120; i++) { var a = i / 120 * 6.2832; x.beginPath(); x.arc(m + Math.cos(a) * m * 0.875, m + Math.sin(a) * m * 0.875, 5, 0, 6.2832); x.fillStyle = g(0.85); x.fill(); }
    function arcText(txt, rad, top, size) {
      x.font = "700 " + size + "px 'Inter Tight', Inter, Arial, sans-serif"; x.fillStyle = g(0.95); x.textAlign = "center"; x.textBaseline = "middle";
      var tot = 0, w = []; for (var k = 0; k < txt.length; k++) { w.push(x.measureText(txt[k]).width + size * 0.18); tot += w[k]; }
      var ang = tot / rad, a0 = top ? -Math.PI / 2 - ang / 2 : Math.PI / 2 + ang / 2;
      for (k = 0; k < txt.length; k++) {
        var mid = top ? a0 + (w[k] / 2) / rad : a0 - (w[k] / 2) / rad;
        x.save(); x.translate(m + Math.cos(mid) * rad, m + Math.sin(mid) * rad); x.rotate(top ? mid + Math.PI / 2 : mid - Math.PI / 2);
        x.fillText(txt[k], 0, 0); x.restore();
        a0 = top ? a0 + w[k] / rad : a0 - w[k] / rad;
      }
    }
    function star(cx, cy, s) { x.beginPath(); for (var j = 0; j < 8; j++) { var aa = j / 8 * 6.2832 - Math.PI / 2, rr = j % 2 ? s * 0.38 : s; x.lineTo(cx + Math.cos(aa) * rr, cy + Math.sin(aa) * rr); } x.closePath(); x.fillStyle = g(0.95); x.fill(); }
    if (front) {
      arcText("FOUNDING MEMBER", m * 0.66, true, 58);
      arcText("XAUUSD GLOBAL", m * 0.66, false, 58);
      star(m - m * 0.66, m, 22); star(m + m * 0.66, m, 22);
      x.font = "italic 400 430px 'Instrument Serif', Georgia, serif"; x.textAlign = "center"; x.textBaseline = "middle";
      x.fillStyle = g(1); x.fillText("50", m, m + 18);
    } else {
      arcText("TRADE SMARTER", m * 0.66, true, 56);
      arcText("TOGETHER", m * 0.66, false, 56);
      // X monogram
      x.save(); x.translate(m, m); x.lineCap = "round";
      x.strokeStyle = g(1); x.lineWidth = 64;
      x.beginPath(); x.moveTo(-150, -170); x.lineTo(150, 170); x.stroke();
      x.beginPath(); x.moveTo(150, -170); x.lineTo(-150, 170); x.stroke();
      x.strokeStyle = g(0.55); x.lineWidth = 14;
      x.beginPath(); x.arc(0, 0, 250, 0, 6.2832); x.stroke();
      x.restore();
      star(m - m * 0.66, m, 22); star(m + m * 0.66, m, 22);
    }
    // soften so the relief has bevelled edges
    var o = document.createElement("canvas"); o.width = o.height = P; var ox = o.getContext("2d");
    ox.filter = "blur(1.7px)"; ox.drawImage(c, 0, 0); ox.filter = "none";
    return ox.filter === "none" ? o : c;
  }

  var VS = [
    "attribute vec3 aPos; attribute vec3 aNor; attribute vec2 aUV; attribute float aK;",
    "uniform mat4 uM; uniform mat4 uPV;",
    "varying vec3 vW; varying vec3 vN; varying vec2 vUV; varying float vK; varying vec3 vP;",
    "void main(){ vec4 w=uM*vec4(aPos,1.); vW=w.xyz; vN=mat3(uM)*aNor; vUV=aUV; vK=aK; vP=aPos; gl_Position=uPV*w; }"
  ].join("\n");
  var FS = [
    "precision highp float;",
    "uniform sampler2D uF; uniform sampler2D uB; uniform mat4 uM; uniform vec3 uEye; uniform float uT;",
    "varying vec3 vW; varying vec3 vN; varying vec2 vUV; varying float vK; varying vec3 vP;",
    "vec3 env(vec3 r){",
    "  float k=0.20+0.12*r.y;",
    "  k+=1.6*smoothstep(0.55,0.95,r.y)*smoothstep(-0.9,0.2,r.z);",          // overhead softbox
    "  k+=1.15*exp(-pow((r.x-0.62)*3.2,2.))*smoothstep(-0.3,0.6,r.y+0.4);",   // right strip
    "  k+=0.55*exp(-pow((r.x+0.75)*4.,2.))*smoothstep(-0.5,0.5,r.y+0.2);",   // left kicker
    "  k+=0.35*smoothstep(0.2,1.,r.z);",                                      // front fill
    "  return mix(vec3(0.10,0.065,0.025), vec3(1.0,0.95,0.82), clamp(k,0.,1.6)); }",
    "void main(){",
    "  vec3 n=normalize(vN); float h=0.6; float cav=1.;",
    "  if(vK<1.5){",
    "    float e=1.4/768.; vec2 uv=vUV; float hc, gx, gy;",
    "    if(vK<0.5){ hc=texture2D(uF,uv).r; gx=texture2D(uF,uv+vec2(e,0.)).r-texture2D(uF,uv-vec2(e,0.)).r; gy=texture2D(uF,uv+vec2(0.,e)).r-texture2D(uF,uv-vec2(0.,e)).r; }",
    "    else { hc=texture2D(uB,uv).r; gx=texture2D(uB,uv+vec2(e,0.)).r-texture2D(uB,uv-vec2(e,0.)).r; gy=texture2D(uB,uv+vec2(0.,e)).r-texture2D(uB,uv-vec2(0.,e)).r; }",
    "    float s=5.5; vec3 on = vK<0.5 ? vec3(-gx*s, gy*s, 1.) : vec3(gx*s, gy*s, -1.);",
    "    n=normalize(mat3(uM)*normalize(on)); h=hc; cav=mix(0.80,1.1,smoothstep(0.2,0.9,hc));",
    "  } else {",
    "    float th=atan(vP.y,vP.x); float mid=1.-smoothstep(0.4,0.95,abs(vP.z)/0.075);",
    "    vec3 tg=normalize(mat3(uM)*vec3(-sin(th),cos(th),0.));",
    "    n=normalize(n+tg*sin(th*180.)*0.35*mid);",
    "  }",
    "  vec3 V=normalize(uEye-vW); vec3 R=reflect(-V,n);",
    "  float ndv=clamp(dot(n,V),0.,1.);",
    "  vec3 gold=vec3(1.0,0.74,0.30);",
    "  vec3 F=mix(gold, vec3(1.0,0.93,0.78), pow(1.-ndv,4.)*0.75);",
    "  vec3 L=normalize(vec3(0.5,0.8,0.6));",
    "  vec3 c=env(R)*F*1.15;",
    "  c+=gold*0.22*max(dot(n,L),0.);",
    "  float sp=pow(max(dot(R,L),0.),90.); c+=vec3(1.,0.95,0.85)*sp*0.9;",
    "  float satin=1.-smoothstep(0.25,0.75,h); c=mix(c, c*0.85+gold*0.16, satin*0.4);",
    "  c*=cav;",
    "  c=c/(1.+c*0.22); c=pow(c,vec3(0.92));",
    "  gl_FragColor=vec4(c,1.);",
    "}"
  ].join("\n");

  function build() {
    // coin with its axis along Z: faces at z=±T, rounded edge of radius T at r=1-T
    var T = 0.075, RC = 1 - T, SEG = 160, RINGS = 6, P = [], N = [], U = [], K = [];
    function push(p, n, uv, k) { P.push(p[0], p[1], p[2]); N.push(n[0], n[1], n[2]); U.push(uv[0], uv[1]); K.push(k); }
    for (var side = 0; side < 2; side++) {
      var z = side ? -T : T, nz = side ? -1 : 1;
      for (var ri = 0; ri < RINGS; ri++) for (var s = 0; s < SEG; s++) {
        var r0 = RC * ri / RINGS, r1 = RC * (ri + 1) / RINGS, a0 = s / SEG * 6.2832, a1 = (s + 1) / SEG * 6.2832;
        var q = [[r0, a0], [r1, a0], [r1, a1], [r0, a0], [r1, a1], [r0, a1]];
        if (side) q = [q[0], q[2], q[1], q[3], q[5], q[4]];
        for (var j = 0; j < 6; j++) {
          var px = Math.cos(q[j][1]) * q[j][0], py = Math.sin(q[j][1]) * q[j][0];
          var u = side ? 0.5 - px * 0.5 / RC * 0.985 : 0.5 + px * 0.5 / RC * 0.985, v = 0.5 - py * 0.5 / RC * 0.985;
          push([px, py, z], [0, 0, nz], [u, v], side);
        }
      }
    }
    var ES = 14;
    for (var e = 0; e < ES; e++) for (var s2 = 0; s2 < SEG; s2++) {
      var p0 = Math.PI / 2 - Math.PI * e / ES, p1 = Math.PI / 2 - Math.PI * (e + 1) / ES;
      var b0 = s2 / SEG * 6.2832, b1 = (s2 + 1) / SEG * 6.2832;
      var vv = [[p0, b0], [p0, b1], [p1, b1], [p0, b0], [p1, b1], [p1, b0]];
      for (var t = 0; t < 6; t++) {
        var ph = vv[t][0], be = vv[t][1], rr = RC + T * Math.cos(ph);
        push([Math.cos(be) * rr, Math.sin(be) * rr, T * Math.sin(ph)], [Math.cos(be) * Math.cos(ph), Math.sin(be) * Math.cos(ph), Math.sin(ph)], [0, 0], 2);
      }
    }
    return { P: new Float32Array(P), N: new Float32Array(N), U: new Float32Array(U), K: new Float32Array(K), n: P.length / 3 };
  }

  function persp(f, a, n, fa) { var t = 1 / Math.tan(f / 2); return [t / a, 0, 0, 0, 0, t, 0, 0, 0, 0, (fa + n) / (n - fa), -1, 0, 0, 2 * fa * n / (n - fa), 0]; }
  function mul(a, b) { var o = new Array(16); for (var i = 0; i < 4; i++) for (var j = 0; j < 4; j++) o[j * 4 + i] = a[i] * b[j * 4] + a[4 + i] * b[j * 4 + 1] + a[8 + i] * b[j * 4 + 2] + a[12 + i] * b[j * 4 + 3]; return o; }
  function rotY(a) { var c = Math.cos(a), s = Math.sin(a); return [c, 0, -s, 0, 0, 1, 0, 0, s, 0, c, 0, 0, 0, 0, 1]; }
  function rotX(a) { var c = Math.cos(a), s = Math.sin(a); return [1, 0, 0, 0, 0, c, s, 0, 0, -s, c, 0, 0, 0, 0, 1]; }
  function rotZ(a) { var c = Math.cos(a), s = Math.sin(a); return [c, s, 0, 0, -s, c, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]; }
  var view = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, -4.4, 1], EYE = [0, 0, 4.4];

  var geo = null, scrollV = 0, lastY = window.scrollY;
  window.addEventListener("scroll", function () { var y = window.scrollY; scrollV += (y - lastY) * 0.0016; lastY = y; }, { passive: true });

  Array.prototype.forEach.call(canvases, function (cv) {
    var gl = cv.getContext("webgl", { antialias: true, alpha: true, premultipliedAlpha: true });
    if (!gl) { cv.parentNode.classList.add("no-gl"); return; }
    function sh(t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw gl.getShaderInfoLog(o); return o; }
    var pr = gl.createProgram();
    try { gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); } catch (err) { cv.parentNode.classList.add("no-gl"); return; }
    gl.linkProgram(pr); gl.useProgram(pr);
    geo = geo || build();
    function attr(name, arr, size) { var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, arr, gl.STATIC_DRAW); var l = gl.getAttribLocation(pr, name); gl.enableVertexAttribArray(l); gl.vertexAttribPointer(l, size, gl.FLOAT, false, 0, 0); }
    attr("aPos", geo.P, 3); attr("aNor", geo.N, 3); attr("aUV", geo.U, 2); attr("aK", geo.K, 1);
    function tex(unit, src) {
      var t = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    }
    var idle = window.requestIdleCallback || function (f) { return setTimeout(f, 16); };
    function textures(done) { tex(0, heightMap(true)); idle(function () { tex(1, heightMap(false)); if (done) done(); }); }
    var fontsReady = !document.fonts || document.fonts.status === "loaded";
    textures();
    if (!fontsReady && document.fonts.ready) document.fonts.ready.then(function () { idle(function () { textures(kick); }); });
    var Uf = {}; ["uM", "uPV", "uF", "uB", "uEye", "uT"].forEach(function (n) { Uf[n] = gl.getUniformLocation(pr, n); });
    gl.uniform1i(Uf.uF, 0); gl.uniform1i(Uf.uB, 1); gl.uniform3fv(Uf.uEye, EYE);
    gl.enable(gl.DEPTH_TEST); gl.clearColor(0, 0, 0, 0);

    function resize() {
      var d = Math.min(window.devicePixelRatio || 1, 2), w = cv.clientWidth, h = cv.clientHeight;
      cv.width = Math.max(1, Math.round(w * d)); cv.height = Math.max(1, Math.round(h * d)); gl.viewport(0, 0, cv.width, cv.height);
      gl.uniformMatrix4fv(Uf.uPV, false, mul(persp(0.62, cv.width / cv.height, 0.1, 20), view));
      kick();
    }
    var tx = 0, ty = 0, mx = 0, my = 0, ang = 0.5, spin = 0;
    cv.parentNode.addEventListener("pointermove", function (e) {
      var r = cv.getBoundingClientRect(); tx = ((e.clientX - r.left) / r.width - 0.5) * 2; ty = ((e.clientY - r.top) / r.height - 0.5) * 2; kick();
    }, { passive: true });
    cv.parentNode.addEventListener("pointerleave", function () { tx = ty = 0; });
    var drag = false, px = 0;
    cv.addEventListener("pointerdown", function (e) { drag = true; px = e.clientX; try { cv.setPointerCapture(e.pointerId); } catch (_) {} });
    cv.addEventListener("pointermove", function (e) { if (drag) { spin += (e.clientX - px) * 0.012; px = e.clientX; } });
    cv.addEventListener("pointerup", function () { drag = false; });
    cv.addEventListener("pointercancel", function () { drag = false; });

    var visible = true, raf = 0, last = 0;
    function frame(now) {
      var dt = last ? Math.min(0.05, (now - last) / 1000) : 0.016; last = now;
      mx += (tx - mx) * 0.06; my += (ty - my) * 0.06;
      spin += scrollV; scrollV *= 0.0; spin *= Math.pow(0.04, dt);
      ang += (reduce ? 0 : 0.45 * dt) + spin * dt * 6;
      var m = mul(rotX(0.10 + my * 0.32), mul(rotY(ang + mx * 0.5), rotZ(Math.sin(now * 0.0006) * 0.05)));
      gl.uniformMatrix4fv(Uf.uM, false, m); gl.uniform1f(Uf.uT, now / 1000);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT); gl.drawArrays(gl.TRIANGLES, 0, geo.n);
      raf = !reduce && visible && !document.hidden ? requestAnimationFrame(frame) : 0;
      if (!raf) last = 0;
    }
    function kick() { if (!raf && visible && !document.hidden) raf = requestAnimationFrame(frame); }
    if ("ResizeObserver" in window) new ResizeObserver(resize).observe(cv); else window.addEventListener("resize", resize);
    resize();
    if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; kick(); }, { rootMargin: "120px" }).observe(cv);
    document.addEventListener("visibilitychange", kick);
    cv.parentNode.classList.add("on");
    kick();
  });
})();
