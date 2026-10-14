/* XAUUSD Global — 3D "gold market landscape" for the homepage hero.
   Hand-written WebGL2 (no libraries): rows of 3D candlesticks scroll like live
   charts receding into the dark, lit in gold, with pointer parallax.
   Pauses when off-screen or the tab is hidden; renders one still frame for
   prefers-reduced-motion; does nothing if WebGL2 is unavailable. */
(function () {
  "use strict";
  var canvas = document.getElementById("hero3d");
  if (!canvas) return;
  var gl = canvas.getContext("webgl2", { antialias: true, alpha: true, premultipliedAlpha: false, powerPreference: "low-power" });
  if (!gl) { canvas.remove(); return; }

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var small = window.innerWidth < 760;
  var COLS = small ? 40 : 64, ROWS = small ? 10 : 15;

  var VS = [
    "#version 300 es",
    "precision highp float;",
    "layout(location=0) in vec3 aPos;",
    "layout(location=1) in vec3 aNor;",
    "layout(location=2) in vec2 aInst;",
    "uniform mat4 uPV; uniform float uT; uniform float uWick; uniform vec2 uGrid;",
    "out vec3 vN; out vec3 vW; out float vUp; out float vEdge; out float vTop;",
    "float series(float x, float r){ float s=r*1.73;",
    "  return 1.6 + 0.9*sin(x*0.19+s) + 0.55*sin(x*0.47+s*2.3) + 0.28*sin(x*1.31+s*0.7) + 0.18*sin(x*2.9+s*3.1) + 0.45*sin(x*0.061+s*1.2); }",
    "void main(){",
    "  float i=aInst.x, r=aInst.y;",
    "  float shift=uT*1.6;",
    "  float idx=i+floor(shift);",
    "  float o=series(idx-1.0,r), c=series(idx,r);",
    "  float lo=min(o,c), hi=max(o,c);",
    "  float wk=0.18+0.22*fract(sin(idx*12.9898+r*78.233)*43758.5453);",
    "  float y0=mix(lo, lo-wk, uWick), y1=mix(max(hi,lo+0.05), hi+wk, uWick);",
    "  float w=mix(0.30,0.05,uWick);",
    "  float x=(i-fract(shift)-uGrid.x*0.5)*0.55;",
    "  float z=-r*1.55;",
    "  vec3 p=vec3(x + aPos.x*w, y0 + aPos.y*(y1-y0), z + aPos.z*w);",
    "  vW=p; vN=aNor; vUp=step(o,c); vTop=aPos.y*step(0.5,aNor.y);",
    "  float ex=(i-fract(shift))/uGrid.x;",
    "  vEdge=smoothstep(0.0,0.08,ex)*smoothstep(1.0,0.9,ex);",
    "  gl_Position=uPV*vec4(p,1.0);",
    "}"
  ].join("\n");

  var FS = [
    "#version 300 es",
    "precision highp float;",
    "in vec3 vN; in vec3 vW; in float vUp; in float vEdge; in float vTop;",
    "uniform vec3 uEye; uniform float uWick;",
    "out vec4 frag;",
    "void main(){",
    "  vec3 gold=vec3(0.949,0.757,0.306); vec3 deep=vec3(0.79,0.57,0.18); vec3 slate=vec3(0.23,0.25,0.29);",
    "  vec3 base=mix(slate, mix(deep,gold,0.6), vUp);",
    "  vec3 N=normalize(vN); vec3 L=normalize(vec3(-0.4,0.9,0.5)); vec3 V=normalize(uEye-vW);",
    "  float dif=max(dot(N,L),0.0)*0.75+0.25;",
    "  float spec=pow(max(dot(N,normalize(L+V)),0.0),24.0)*0.6*vUp;",
    "  float rim=pow(1.0-max(dot(N,V),0.0),3.0)*0.55;",
    "  vec3 col=base*dif + gold*(spec+rim*mix(0.25,0.8,vUp)) + gold*vTop*0.25*vUp;",
    "  col*=mix(1.0,0.7,uWick);",
    "  float d=length(uEye-vW);",
    "  float fog=smoothstep(9.0,34.0,d);",
    "  float a=(1.0-fog)*vEdge;",
    "  frag=vec4(col, a);",
    "}"
  ].join("\n");

  function sh(type, src) {
    var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { throw new Error(gl.getShaderInfoLog(s)); }
    return s;
  }
  var prog;
  try {
    prog = gl.createProgram();
    gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS));
    gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
  } catch (e) { canvas.remove(); return; }

  // Unit box: x,z in [-0.5,0.5], y in [0,1], with flat normals.
  var faces = [
    [[0, 1, 0], [[-.5, 1, -.5], [-.5, 1, .5], [.5, 1, .5], [.5, 1, -.5]]],
    [[0, -1, 0], [[-.5, 0, -.5], [.5, 0, -.5], [.5, 0, .5], [-.5, 0, .5]]],
    [[1, 0, 0], [[.5, 0, -.5], [.5, 1, -.5], [.5, 1, .5], [.5, 0, .5]]],
    [[-1, 0, 0], [[-.5, 0, -.5], [-.5, 0, .5], [-.5, 1, .5], [-.5, 1, -.5]]],
    [[0, 0, 1], [[-.5, 0, .5], [.5, 0, .5], [.5, 1, .5], [-.5, 1, .5]]],
    [[0, 0, -1], [[-.5, 0, -.5], [-.5, 1, -.5], [.5, 1, -.5], [.5, 0, -.5]]]
  ];
  var verts = [];
  faces.forEach(function (f) {
    var n = f[0], q = f[1];
    [0, 1, 2, 0, 2, 3].forEach(function (k) { verts.push(q[k][0], q[k][1], q[k][2], n[0], n[1], n[2]); });
  });
  var inst = [];
  for (var r = 0; r < ROWS; r++) for (var c = 0; c < COLS; c++) inst.push(c, r);

  var vao = gl.createVertexArray(); gl.bindVertexArray(vao);
  var vb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vb); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(verts), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 24, 0);
  gl.enableVertexAttribArray(1); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 24, 12);
  var ib = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, ib); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(inst), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(2); gl.vertexAttribPointer(2, 2, gl.FLOAT, false, 8, 0); gl.vertexAttribDivisor(2, 1);

  var U = {};
  ["uPV", "uT", "uWick", "uGrid", "uEye"].forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });

  function persp(fovy, asp, n, f) {
    var t = 1 / Math.tan(fovy / 2), nf = 1 / (n - f);
    return [t / asp, 0, 0, 0, 0, t, 0, 0, 0, 0, (f + n) * nf, -1, 0, 0, 2 * f * n * nf, 0];
  }
  function lookAt(e, c, up) {
    var zx = e[0] - c[0], zy = e[1] - c[1], zz = e[2] - c[2], l = Math.hypot(zx, zy, zz); zx /= l; zy /= l; zz /= l;
    var xx = up[1] * zz - up[2] * zy, xy = up[2] * zx - up[0] * zz, xz = up[0] * zy - up[1] * zx; l = Math.hypot(xx, xy, xz); xx /= l; xy /= l; xz /= l;
    var yx = zy * xz - zz * xy, yy = zz * xx - zx * xz, yz = zx * xy - zy * xx;
    return [xx, yx, zx, 0, xy, yy, zy, 0, xz, yz, zz, 0,
      -(xx * e[0] + xy * e[1] + xz * e[2]), -(yx * e[0] + yy * e[1] + yz * e[2]), -(zx * e[0] + zy * e[1] + zz * e[2]), 1];
  }
  function mul(a, b) {
    var o = new Array(16);
    for (var i = 0; i < 4; i++) for (var j = 0; j < 4; j++) {
      o[j * 4 + i] = a[i] * b[j * 4] + a[4 + i] * b[j * 4 + 1] + a[8 + i] * b[j * 4 + 2] + a[12 + i] * b[j * 4 + 3];
    }
    return o;
  }

  var mx = 0, my = 0, tx = 0, ty = 0;
  window.addEventListener("pointermove", function (e) {
    tx = (e.clientX / window.innerWidth - 0.5) * 2; ty = (e.clientY / window.innerHeight - 0.5) * 2;
  }, { passive: true });

  function resize() {
    var dpr = Math.min(window.devicePixelRatio || 1, small ? 1 : 1.5);
    var w = canvas.clientWidth, h = canvas.clientHeight;
    canvas.width = Math.max(1, Math.round(w * dpr)); canvas.height = Math.max(1, Math.round(h * dpr));
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  if ("ResizeObserver" in window) new ResizeObserver(resize).observe(canvas); else window.addEventListener("resize", resize);
  resize();

  gl.enable(gl.DEPTH_TEST); gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
  gl.clearColor(0, 0, 0, 0);

  var visible = true, start = performance.now(), raf = 0;
  function frame(now) {
    var t = reduce ? 4.0 : (now - start) / 1000;
    mx += (tx - mx) * 0.04; my += (ty - my) * 0.04;
    var asp = canvas.width / canvas.height;
    var eye = [Math.sin(t * 0.07) * 1.2 + mx * 2.2, 7.2 - my * 1.1, 9.5];
    var pv = mul(persp(0.75, asp, 0.1, 60), lookAt(eye, [mx * 0.8, 0.2, -11], [0, 1, 0]));
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.useProgram(prog); gl.bindVertexArray(vao);
    gl.uniformMatrix4fv(U.uPV, false, pv); gl.uniform1f(U.uT, t); gl.uniform2f(U.uGrid, COLS, ROWS); gl.uniform3fv(U.uEye, eye);
    gl.uniform1f(U.uWick, 1); gl.drawArraysInstanced(gl.TRIANGLES, 0, 36, COLS * ROWS);
    gl.uniform1f(U.uWick, 0); gl.drawArraysInstanced(gl.TRIANGLES, 0, 36, COLS * ROWS);
    if (!reduce && visible && !document.hidden) raf = requestAnimationFrame(frame); else raf = 0;
  }
  function kick() { if (!raf && visible && !document.hidden) raf = requestAnimationFrame(frame); }
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (en) { visible = en[0].isIntersecting; kick(); }).observe(canvas);
  }
  document.addEventListener("visibilitychange", kick);
  canvas.classList.add("on");
  raf = requestAnimationFrame(frame);
})();
