#!/usr/bin/env python3
""""Fold This Paper 42 Times" — 86 s vertical (1080x1920) for YouTube Shorts. No music (added later by hand).

The world is a logarithmic tower: every fold adds the same height on screen, so the camera rides the top
of the paper past real landmarks. Fold count, camera, column, landmark highlights and speed streaks are
all pure functions of time (seek-safe). Run: python3 build.py
"""
import json, math, os, subprocess

W, H, DUR = 1080, 1920, 86
K = 420                       # px per decade (log10 metres)
L0 = -4                       # 0.1 mm = 1e-4 m sits at world Y = 0
WH = 32 * K + 2200            # world height
COLX, COLW = 272, 56          # paper column on screen

def Y(m):                     # world height (px above the paper's base) for a height in metres
    return (math.log10(m) - L0) * K

VO = {k: float(v) for k, v in json.load(open("vo-durations.json")).items()}
STARTS = {"h1": 0.25, "h2": 2.7, "h3": 5.05, "h4": 7.3, "f1": 11.8, "f2": 15.2, "f3": 20.5, "f4": 24.4, "f5": 27.6,
          "f6": 30.2, "f7": 33.9, "f8": 38.0, "f9": 42.9, "f10": 47.4, "f11": 50.6, "f12": 54.4, "f13": 57.6,
          "f14": 60.3, "t1": 62.6, "t2": 66.3, "t3": 69.3, "t4": 72.6, "t5": 77.0}

# ---------------------------------------------------------------- icons (stroke style, white)
S = 'fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'
IC = {
    "book": f'<svg viewBox="0 0 100 100"><rect x="18" y="58" width="64" height="24" rx="3" {S}/><path d="M18 66h64M18 74h64" {S}/></svg>',
    "cup": f'<svg viewBox="0 0 100 100"><path d="M24 30h44v40a12 12 0 0 1 -12 12h-20a12 12 0 0 1 -12 -12z" {S}/><path d="M68 40h8a10 10 0 0 1 0 20h-8" {S}/><path d="M36 12c-4 6 4 8 0 14M50 12c-4 6 4 8 0 14" {S}/></svg>',
    "you": '<svg viewBox="0 0 80 130"><circle cx="40" cy="24" r="20" fill="#fff"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="#fff"/></svg>',
    "building": f'<svg viewBox="0 0 100 130"><rect x="25" y="10" width="50" height="118" {S}/>' + "".join(f'<path d="M35 {y}h8M57 {y}h8" {S}/>' for y in range(24, 120, 14)) + '</svg>',
    "spire": f'<svg viewBox="0 0 100 160"><path d="M50 2 L50 20 M42 158 L44 60 L50 20 L56 60 L58 158 Z M32 158 L36 100 L44 90 M68 158 L64 100 L56 90" {S}/></svg>',
    "mountain": f'<svg viewBox="0 0 160 110"><path d="M4 106 L60 20 L82 50 L98 30 L156 106 Z" {S}/><path d="M48 38 L60 20 L72 38 L64 34 L56 40 Z" fill="#fff"/></svg>',
    "sat": f'<svg viewBox="0 0 120 80"><rect x="48" y="28" width="24" height="24" {S}/><rect x="4" y="30" width="36" height="20" {S}/><rect x="80" y="30" width="36" height="20" {S}/><path d="M40 40h8M72 40h8M60 28v-12" {S}/></svg>',
    "earth": '<svg viewBox="0 0 220 220"><circle cx="110" cy="110" r="104" fill="#0c0c0c" stroke="#fff" stroke-width="4"/><path d="M40 70c30 10 40-20 70-10s20 40 50 30M30 140c40-10 50 20 90 10s30-30 60-20M70 190c20-15 40-5 60-15" fill="none" stroke="#9a9a9a" stroke-width="4" stroke-linecap="round"/></svg>',
    "sun": '<svg viewBox="0 0 300 300"><circle cx="150" cy="150" r="120" fill="#fff"/></svg>',
    "star": '<svg viewBox="0 0 80 80"><path d="M40 4 L46 34 L76 40 L46 46 L40 76 L34 46 L4 40 L34 34 Z" fill="#fff"/></svg>',
    "galaxy": '<svg viewBox="0 0 260 260"><ellipse cx="130" cy="130" rx="118" ry="48" fill="none" stroke="#fff" stroke-width="3" opacity="0.5"/><ellipse cx="130" cy="130" rx="80" ry="30" fill="none" stroke="#fff" stroke-width="3" opacity="0.75"/><ellipse cx="130" cy="130" rx="34" ry="14" fill="#fff"/></svg>',
    "universe": '<svg viewBox="0 0 300 300"><circle cx="150" cy="150" r="140" fill="none" stroke="#fff" stroke-width="5"/><circle cx="150" cy="150" r="110" fill="none" stroke="#fff" stroke-width="2" opacity="0.5"/><circle cx="150" cy="150" r="80" fill="none" stroke="#fff" stroke-width="2" opacity="0.3"/></svg>',
}
# name, value, metres, icon, box w, box h, mode ("stand" = sits on the line, "float" = centred on it)
LMS = [
    ("A notebook", "1.3 cm", 0.0128, "book", 100, 100, "stand"),
    ("A coffee cup", "10 cm", 0.10, "cup", 100, 100, "stand"),
    ("You", "1.8 m", 1.8, "you", 62, 100, "stand"),
    ("30-story building", "100 m", 100, "building", 92, 120, "stand"),
    ("Tallest building on Earth", "828 m", 828, "spire", 90, 144, "stand"),
    ("Mount Everest", "8,849 m", 8849, "mountain", 160, 110, "stand"),
    ("Edge of space", "100 km", 1e5, None, 0, 0, "line"),
    ("Space station", "≈ 410 km", 4.1e5, "sat", 120, 80, "float"),
    ("Earth's width", "12,742 km", 1.2742e7, "earth", 220, 220, "float"),
    ("The Sun", "150 million km", 1.496e11, "sun", 300, 300, "float"),
    ("Nearest star", "4.2 light-years", 4.0e16, "star", 80, 80, "float"),
    ("The Milky Way", "100,000 light-years", 9.5e20, "galaxy", 260, 260, "float"),
    ("Observable universe", "93 billion light-years", 8.8e26, "universe", 300, 300, "float"),
]
lm_html = []
for i, (name, val, m, ic, bw, bh, mode) in enumerate(LMS):
    y = WH - Y(m)
    parts = [f'<div class="lml" style="top:{y:.0f}px"></div>']
    if ic:
        if mode == "stand":
            parts.append(f'<div class="lmi" style="left:410px;top:{y - bh:.0f}px;width:{bw}px;height:{bh}px">{IC[ic]}</div>')
            parts.append(f'<div class="lmt" style="left:{410 + bw + 22}px;top:{y - 84:.0f}px"><div class="n">{name}</div><div class="v">{val}</div></div>')
        else:
            parts.append(f'<div class="lmi" style="left:{410 if bw < 200 else 380}px;top:{y - bh / 2:.0f}px;width:{bw}px;height:{bh}px">{IC[ic]}</div>')
            if bw < 200:
                parts.append(f'<div class="lmt" style="left:{410 + bw + 22}px;top:{y - 42:.0f}px"><div class="n">{name}</div><div class="v">{val}</div></div>')
            else:
                parts.append(f'<div class="lmt" style="left:{380 + bw + 24}px;top:{y - 42:.0f}px;width:{1040 - 404 - bw}px"><div class="n">{name}</div><div class="v sm">{val}</div></div>')
    else:
        parts.append(f'<div class="lmt" style="left:410px;top:{y - 84:.0f}px"><div class="n">{name}</div><div class="v">{val}</div></div>')
    lm_html.append(f'<div class="lm" id="w-lm{i}" data-y="{Y(m):.1f}">{"".join(parts)}</div>')

# the Moon: centred on the column, its lowest point exactly 384,400 km up
moon_r = 190
moon_y = WH - Y(3.844e8)
moon = (f'<div id="w-moon" class="lm" data-y="{Y(3.844e8):.1f}"><svg class="moon" style="left:{COLX + COLW / 2 - moon_r}px;top:{moon_y - 2 * moon_r:.0f}px;width:{2 * moon_r}px;height:{2 * moon_r}px" viewBox="0 0 380 380">'
        '<circle cx="190" cy="190" r="186" fill="#e9e9e9"/><circle cx="120" cy="140" r="34" fill="#cfcfcf"/><circle cx="240" cy="110" r="22" fill="#d4d4d4"/>'
        '<circle cx="250" cy="250" r="44" fill="#cdcdcd"/><circle cx="140" cy="270" r="18" fill="#d6d6d6"/><circle cx="300" cy="190" r="14" fill="#d2d2d2"/></svg>'
        f'<div class="lmt" style="left:{COLX + COLW / 2 + moon_r + 24}px;top:{moon_y - moon_r - 42:.0f}px"><div class="n">The Moon</div><div class="v">384,400 km</div></div></div>')

# stars above the edge of space (deterministic LCG)
seed = 12345
def rnd():
    global seed
    seed = (seed * 1103515245 + 12345) % 2 ** 31
    return seed / 2 ** 31
stars = []
for _ in range(520):
    x, yy = rnd() * 1080, WH - (Y(1.5e5) + rnd() * (WH - Y(1.5e5) - 400))
    r = 1 + rnd() * 2.2
    stars.append(f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="{r:.1f}" fill="#fff" opacity="{0.25 + rnd() * 0.6:.2f}"/>')
stars_svg = f'<svg id="w-stars" style="position:absolute;left:0;top:0;width:1080px;height:{WH}px" viewBox="0 0 1080 {WH}">{"".join(stars)}</svg>'

world = (f'<div id="w-world" class="abs clip" data-start="0" data-duration="{DUR}" data-layout-allow-overflow '
         f'style="left:0;top:0;width:1080px;height:{WH}px;background:linear-gradient(to top, #1d1d1d 0px, #141414 {Y(10) + 200:.0f}px, #0a0a0a {Y(1e4):.0f}px, #000 {Y(1.2e5):.0f}px, #000 100%)">'
         f'{stars_svg}'
         f'<div id="w-ground" style="position:absolute;left:0;width:1080px;top:{WH + 30}px;height:0;border-top:2px dashed rgba(255,255,255,0.35)"></div>'
         f'<div id="w-col" style="position:absolute;left:{COLX}px;width:{COLW}px;top:0;height:{WH + 30}px;background:linear-gradient(90deg,#cfcfcf,#ffffff 45%,#d9d9d9);box-shadow:0 0 30px rgba(255,255,255,0.45)"></div>'
         f'{"".join(lm_html)}{moon}</div>')

streaks = "".join(f'<div class="stk" id="w-s{i}" style="left:{x}px;height:{h}px"></div>' for i, (x, h) in enumerate(
    [(60, 260), (150, 180), (410, 300), (520, 160), (640, 240), (760, 320), (860, 200), (960, 280), (1030, 170), (230, 220)]))

def T(id, cls, style, inner=""):
    return f'<div id="{id}" class="abs {cls} clip" data-start="0" data-duration="{DUR}" style="{style}">{inner}</div>'

paper = (T("w-pp", "", "left:360px;top:450px;width:360px;height:500px",
           '<div id="w-pT" class="ph" style="left:0;top:0;width:360px;height:250px"></div>'
           '<div id="w-pB" class="ph" style="left:0;top:250px;width:360px;height:250px"></div>'
           '<div id="w-pL" class="ph two" style="left:0;top:250px;width:180px;height:250px;opacity:0"></div>'
           '<div id="w-pR" class="ph two" style="left:180px;top:250px;width:180px;height:250px;opacity:0"></div>'))

body = "\n    ".join([
    world,
    T("w-stks", "", "left:0;top:0;width:1080px;height:1920px", streaks),
    T("w-tip", "", f"left:{COLX - 30}px;top:0;width:{COLW + 60}px;height:24px;border-radius:12px;background:radial-gradient(ellipse, rgba(255,255,255,0.95), rgba(255,255,255,0) 70%)"),
    T("w-plane", "", "left:0;top:520px;width:180px;height:70px",
      f'<svg viewBox="0 0 180 70"><path d="M8 38 L150 30 Q176 32 176 38 Q176 44 150 46 L8 40 Z M70 36 L40 6 L58 6 L104 34 M70 42 L40 66 L58 66 L104 44 M12 38 L4 22 L16 22 L30 36" {S}/></svg>'),
    T("w-sheetpill", "", f"left:{COLX + COLW + 18}px;top:980px", '<span class="pill dark">← 1 sheet of paper</span>'),
    T("w-hk", "small", "left:60px;top:180px", "Folds"),
    T("w-hn", "big glow", "left:56px;top:212px;font-size:128px", "42"),
    T("w-hv", "", "left:60px;top:345px;font-weight:800;font-size:46px", "439,805 km"),
    paper,
    T("w-plab", "ctr", "top:990px", '<span class="pill" id="w-plab-t">0.1 mm thick</span>'),
    T("w-l2", "ctr", "top:990px", '<span class="pill">2 layers</span>'),
    T("w-l4", "ctr", "top:990px", '<span class="pill">4 layers</span>'),
    T("w-flash", "", "left:0;top:0;width:1080px;height:1920px;background:#fff"),
    T("w-scrim", "", "left:0;top:0;width:1080px;height:1920px;background:rgba(0,0,0,0.9)"),
    T("w-rec", "ctr", "top:520px",
      '<div class="small">Real-world record</div><div class="big glow" id="w-rec12" style="font-size:190px;margin-top:14px">12 folds</div><div class="small" style="margin-top:26px;color:#cfcfcf">≈ 41 cm thick</div>'),
    T("w-black", "", "left:0;top:0;width:1080px;height:1920px;background:#000"),
    T("w-end", "", "left:470px;top:620px;width:140px;height:200px;background:#f0f0f0;box-shadow:0 0 50px rgba(255,255,255,0.5);border-radius:3px"),
    T("w-endt", "small ctr", "top:880px;color:#cfcfcf", "1 sheet · 103 folds"),
])

CSS = f"""
    #root {{ position: absolute; inset: 0; background: #000; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
    #root .abs {{ position: absolute; }}
    #root .glow {{ filter: drop-shadow(0 0 16px rgba(255,255,255,0.55)); }}
    #root .pill {{ font-weight: 700; font-size: 30px; letter-spacing: 0.16em; text-transform: uppercase; color: #d8d8d8; background: #141414; border: 2px solid #4a4a4a; border-radius: 999px; padding: 12px 26px; white-space: nowrap; display: inline-block; }}
    #root .pill.dark {{ background: rgba(0,0,0,0.85); border-color: #fff; color: #fff; }}
    #root .small {{ font-weight: 700; font-size: 30px; letter-spacing: 0.22em; text-transform: uppercase; color: #9a9a9a; }}
    #root .big {{ font-weight: 900; letter-spacing: -0.03em; line-height: 1; }}
    #root .ctr {{ left: 0; width: 1080px; text-align: center; }}
    #root #w-world {{ transform-origin: 0 0; }}
    #root .lm {{ position: absolute; left: 0; top: 0; width: 1080px; opacity: 0.45; }}
    #root .lm.hit {{ opacity: 1; }}
    #root .lm.under .lmt {{ opacity: 0; }}
    #root .lml {{ position: absolute; left: {COLX + COLW}px; width: {1040 - COLX - COLW}px; height: 0; border-top: 2px dashed rgba(255,255,255,0.45); }}
    #root .lmi {{ position: absolute; }}
    #root .lmi svg {{ width: 100%; height: 100%; display: block; }}
    #root .lmt {{ position: absolute; }}
    #root .lmt .n {{ font-weight: 700; font-size: 28px; letter-spacing: 0.16em; text-transform: uppercase; color: #a8a8a8; line-height: 1.15; }}
    #root .lmt .v {{ font-weight: 900; font-size: 46px; line-height: 1.05; }}
    #root .lmt .v.sm {{ font-size: 36px; }}
    #root .moon {{ position: absolute; filter: drop-shadow(0 0 40px rgba(255,255,255,0.45)); }}
    #root .stk {{ position: absolute; top: 0; width: 3px; border-radius: 2px; background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0.75), rgba(255,255,255,0)); opacity: 0; }}
    #root .ph {{ position: absolute; background: #efefef; box-shadow: inset 0 0 0 2px #bcbcbc; }}
    #root .ph.two {{ background: #e2e2e2; box-shadow: inset 0 0 0 3px #a8a8a8; }}
    #root #w-hv, #root #w-hn, #root #w-hk {{ text-shadow: 0 2px 10px #000; }}
    #root #w-pp, #root #w-plab, #root #w-l2, #root #w-l4, #root #w-flash, #root #w-scrim, #root #w-rec, #root #w-black, #root #w-end, #root #w-endt, #root #w-plane, #root #w-hk, #root #w-hn, #root #w-hv {{ opacity: 0; }}
"""

JS = f"""
    const tl = gsap.timeline({{ paused: true }});
    const $ = (s) => document.querySelector(s);
    const WH = {WH}, K = {K}, L0 = {L0}, TOP = {Y(1)};
    const Yh = (m) => (Math.log10(m) - L0) * K;
    // ---- fold count over time: [t, n, ease]  (ease applies to the segment ending at this key)
    const io3 = (u) => u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
    const ss = (u) => u * u * (3 - 2 * u);
    const inQ = (u) => Math.pow(u, 2.4);
    const io2 = (u) => u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
    const N = [
      [0, 42], [8.9, 42], [11.4, 0, io3], [15.4, 0], [15.9, 1], [17.9, 1], [18.4, 2], [20.2, 2], [20.95, 7, io2],
      [24.3, 7], [24.75, 10], [27.5, 10], [28.05, 15], [30.15, 15], [30.75, 20], [33.9, 20], [34.4, 23],
      [37.9, 23], [38.55, 27], [42.85, 27], [43.45, 30], [47.45, 30], [47.95, 32], [50.55, 32], [51.35, 37],
      [54.35, 37], [55.1, 41], [58.0, 41], [60.45, 42, inQ], [68.6, 42], [71.3, 51, io2], [72.8, 51], [75.95, 103, io2], [{DUR}, 103],
    ];
    const nAt = (t) => {{
      if (t <= N[0][0]) return N[0][1];
      for (let i = 1; i < N.length; i++) if (t <= N[i][0]) {{
        const u = (t - N[i - 1][0]) / (N[i][0] - N[i - 1][0]);
        return N[i - 1][1] + (N[i][1] - N[i - 1][1]) * (N[i][2] || ss)(u);
      }}
      return N[N.length - 1][1];
    }};
    // screen y of the paper's top
    const SY = [[0, 820], [8.9, 820], [11.4, 760], [{DUR}, 760]];
    const syAt = (t) => {{ if (t <= SY[1][0]) return 820; if (t >= SY[2][0]) return 760; return 820 - 60 * ss((t - 8.9) / 2.5); }};
    const fmt = (h) => {{
      if (h < 0.01) return (h * 1000).toFixed(1) + " mm";
      if (h < 1) return (h * 100).toFixed(h < 0.1 ? 1 : 0) + " cm";
      if (h < 1000) return (h < 10 ? h.toFixed(1) : Math.round(h).toLocaleString("en-US")) + " m";
      if (h < 1e9) return Math.round(h / 1000).toLocaleString("en-US") + " km";
      if (h < 1e12) return Math.round(h / 1e9).toLocaleString("en-US") + " million km";
      if (h < 9.461e15) return Math.round(h / 1e12).toLocaleString("en-US") + " billion km";
      const ly = h / 9.461e15;
      if (ly < 1e6) return Math.round(ly).toLocaleString("en-US") + " light-years";
      if (ly < 1e9) return Math.round(ly / 1e6).toLocaleString("en-US") + " million light-years";
      return Math.round(ly / 1e9).toLocaleString("en-US") + " billion light-years";
    }};
    const lms = Array.from(document.querySelectorAll("#w-world .lm")).map((el) => [el, parseFloat(el.dataset.y)]);
    const stk = Array.from(document.querySelectorAll("#w-stks .stk"));
    const clock = {{ t: 0 }};
    tl.fromTo(clock, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: () => {{
      const t = clock.t, n = nAt(t);
      const h = 1e-4 * Math.pow(2, n);
      const top = Yh(h), sy = syAt(t);
      const ty = sy - (WH - top);
      gsap.set("#w-world", {{ y: ty }});
      $("#w-col").style.clipPath = `inset(${{(WH - top).toFixed(1)}}px 0 0 0)`;
      gsap.set("#w-tip", {{ y: sy - 12 }});
      $("#w-hn").textContent = Math.floor(n + 1e-6);
      $("#w-hv").textContent = fmt(h);
      for (const [el, y] of lms) {{
        el.classList.toggle("hit", top >= y - 2);
        const yy = sy + (top - y);                                  // landmark line on screen
        el.classList.toggle("under", yy > 1150 && yy < 1400);        // keep the caption band clear
      }}
      // speed streaks: brightness follows climb speed, direction follows its sign
      const v = (nAt(t + 0.02) - nAt(t - 0.02)) / 0.04;          // folds per second
      const a = Math.min(1, Math.max(0, (Math.abs(v) - 4) / 14));
      stk.forEach((s, i) => {{
        const span = 2300, off = (i * 397) % span;
        const p = ((t * (900 + i * 90) * Math.sign(v || 1) + off) % span + span) % span - 200;
        s.style.opacity = (a * (0.45 + (i % 3) * 0.2)).toFixed(3);
        s.style.transform = `translateY(${{p.toFixed(1)}}px)`;
      }});
    }} }}, 0);

    // ================= HOOK =================
    tl.fromTo("#w-sheetpill", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.2, yoyo: true, repeat: 1, ease: "power1.out", transformOrigin: "0% 50%" }}, 3.45);
    tl.to("#w-sheetpill", {{ opacity: 0, duration: 0.3 }}, 8.7);
    tl.fromTo(["#w-hk", "#w-hn", "#w-hv"], {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.35, stagger: 0.06, ease: "power2.out" }}, 5.85);
    tl.fromTo("#w-hn", {{ scale: 1.25, transformOrigin: "0% 50%" }}, {{ scale: 1, duration: 0.5, ease: "back.out(2.5)" }}, 5.9);
    tl.fromTo("#w-world", {{ filter: "blur(0px)" }}, {{ filter: "blur(2.5px)", duration: 0.8, yoyo: true, repeat: 1, ease: "power2.in" }}, 9.35);

    // ================= THE SHEET =================
    tl.to(["#w-world", "#w-tip"], {{ opacity: 0.12, duration: 0.5 }}, 11.2);
    tl.fromTo("#w-pp", {{ opacity: 0, scale: 0.7, rotation: -8 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.55, ease: "back.out(1.6)" }}, 11.45);
    tl.fromTo("#w-plab", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }}, 13.35);
    tl.to("#w-plab", {{ opacity: 0, duration: 0.25 }}, 15.3);
    // fold 1: the top half swings down onto the bottom half
    tl.fromTo("#w-pT", {{ rotationX: 0, transformPerspective: 1400, transformOrigin: "50% 100%" }}, {{ rotationX: -90, duration: 0.22, ease: "power2.in" }}, 15.4);
    tl.fromTo("#w-pT", {{ backgroundColor: "#efefef" }}, {{ backgroundColor: "#d6d6d6", duration: 0.01 }}, 15.62);
    tl.to("#w-pT", {{ rotationX: -180, duration: 0.22, ease: "power2.out" }}, 15.63);
    tl.fromTo("#w-l2", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, 16.65);
    tl.to("#w-l2", {{ opacity: 0, duration: 0.2 }}, 17.7);
    // fold 2: swap to the two-layer halves, the left half swings over the right
    tl.to(["#w-pT", "#w-pB"], {{ opacity: 0, duration: 0.01 }}, 17.85);
    tl.to(["#w-pL", "#w-pR"], {{ opacity: 1, duration: 0.01 }}, 17.85);
    tl.fromTo("#w-pL", {{ rotationY: 0, transformPerspective: 1400, transformOrigin: "100% 50%" }}, {{ rotationY: 90, duration: 0.22, ease: "power2.in" }}, 17.9);
    tl.fromTo("#w-pL", {{ backgroundColor: "#e2e2e2" }}, {{ backgroundColor: "#c9c9c9", duration: 0.01 }}, 18.12);
    tl.to("#w-pL", {{ rotationY: 180, duration: 0.22, ease: "power2.out" }}, 18.13);
    tl.fromTo("#w-l4", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, 18.72);
    tl.to("#w-l4", {{ opacity: 0, duration: 0.25 }}, 19.45);
    // the folded sheet flies into the top of the tower
    tl.to("#w-pp", {{ x: {COLX + COLW / 2} - 630, y: 760 - 825 + 60, scaleX: 0.31, scaleY: 0.22, duration: 0.75, ease: "power3.in" }}, 19.45);
    tl.to("#w-pp", {{ opacity: 0, duration: 0.15 }}, 20.15);
    tl.to(["#w-world", "#w-tip"], {{ opacity: 1, duration: 0.5 }}, 19.85);

    // ================= THE CLIMB =================
    tl.fromTo("#w-plane", {{ opacity: 1, x: 1160 }}, {{ opacity: 1, x: -260, duration: 1.4, ease: "none" }}, 41.25);
    tl.to("#w-plane", {{ opacity: 0, duration: 0.05 }}, 42.66);
    // the Moon
    tl.fromTo("#w-flash", {{ opacity: 0 }}, {{ opacity: 0.85, duration: 0.06 }}, 60.45);
    tl.to("#w-flash", {{ opacity: 0, duration: 0.9, ease: "power2.out" }}, 60.52);
    tl.fromTo("#w-world", {{ x: 0 }}, {{ x: 10, duration: 0.05, yoyo: true, repeat: 7, ease: "none" }}, 60.46);

    // ================= THE RECORD =================
    tl.fromTo("#w-scrim", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, 62.4);
    tl.fromTo("#w-moon .lmt", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.25 }}, 62.4);
    tl.to("#w-moon .lmt", {{ opacity: 1, duration: 0.4 }}, 66.8);
    tl.fromTo("#w-rec", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.8)" }}, 63.9);
    tl.fromTo("#w-rec12", {{ scale: 0.6 }}, {{ scale: 1, duration: 0.45, ease: "back.out(2.4)" }}, 64.95);
    tl.to("#w-rec", {{ opacity: 0, y: -20, duration: 0.35 }}, 66.55);
    tl.to("#w-scrim", {{ opacity: 0, duration: 0.5 }}, 66.8);
    // the Sun and the universe
    tl.fromTo("#w-flash", {{ opacity: 0 }}, {{ opacity: 0.7, duration: 0.05, immediateRender: false }}, 71.2);
    tl.to("#w-flash", {{ opacity: 0, duration: 0.6 }}, 71.26);
    tl.fromTo("#w-flash", {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.05, immediateRender: false }}, 75.9);
    tl.to("#w-flash", {{ opacity: 0, duration: 0.8 }}, 75.96);

    // ================= ONE SHEET =================
    tl.fromTo("#w-black", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12 }}, 76.85);
    tl.fromTo("#w-end", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, 77.2);
    tl.fromTo("#w-endt", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.5 }}, 78.4);
    tl.fromTo("#w-end", {{ rotation: 0 }}, {{ rotation: -4, scale: 1.1, duration: 6.4, ease: "sine.inOut", immediateRender: false }}, 78.0);
    tl.fromTo("#w-end", {{ boxShadow: "0 0 50px rgba(255,255,255,0.5)" }}, {{ boxShadow: "0 0 110px rgba(255,255,255,0.8)", duration: 3, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, 78.2);
    tl.to(["#w-end", "#w-endt"], {{ opacity: 0, duration: 1.4, ease: "power1.in" }}, 84.4);
"""

wcomp = f"""<template>
  <style>{CSS}
  </style>
  <div id="root" data-composition-id="w" data-width="{W}" data-height="{H}">
    {body}
  </div>
  <script>{JS}
    window.__timelines["w"] = tl;
  </script>
</template>
"""

# ---------------------------------------------------------------- captions
FIX = {"plains": "planes", "Hundred": "A hundred"}
words = {}
for line in open("words.txt", encoding="utf-8"):
    k, *ws = line.split()
    words[k] = [(w.rsplit("@", 1)[0], float(w.rsplit("@", 1)[1])) for w in ws]
grp = []
for k, st in STARTS.items():
    cur = []
    for w, t in words[k]:
        w = FIX.get(w, w)
        cur.append((w, st + t))
        if len(cur) >= 3 or w[-1] in ".,?:!":
            grp.append(cur); cur = []
    if cur:
        grp.append(cur)
    grp[-1].append(("", st + VO[k]))
flat = [([x for x in g if x[0]], g[-1][1] if g[-1][0] == "" else None) for g in grp]
caps = []
for i, (ws, end) in enumerate(flat):
    s = round(ws[0][1] - 0.05, 2)
    e = end if end is not None else flat[i + 1][0][0][1] - 0.05
    caps.append(f'<div id="cap-{i}" class="abs cap clip" data-start="{s}" data-duration="{round(min(e, DUR - 0.1) - s, 2)}"><span>{" ".join(w for w, _ in ws)}</span></div>')
cap = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; background: transparent; font-family: "Inter", sans-serif; }}
    #root .abs {{ position: absolute; }}
    #root .cap {{ left: 90px; width: 900px; top: 1180px; text-align: center; font-weight: 800; font-size: 56px; line-height: 1.15; color: #fff; }}
    #root .cap span {{ display: inline-block; background: rgba(0,0,0,0.86); padding: 6px 22px 10px; border-radius: 16px; }}
  </style>
  <div id="root" data-composition-id="cap" data-width="{W}" data-height="{H}">
{chr(10).join("    " + c for c in caps)}
  </div>
  <script>
    window.__timelines["cap"] = gsap.timeline({{ paused: true }});
  </script>
</template>
"""

# ---------------------------------------------------------------- sound design (start, file, volume)
SFX = [
    (0.0, "boom_open", 0.55), (3.45, "pop", 0.4), (5.85, "up2", 0.55), (5.9, "pop", 0.45),
    (8.85, "rewind_fall", 0.95), (11.33, "land", 0.8), (11.45, "paper_slide", 0.6), (13.35, "pop", 0.35),
    (15.1, "paper_fold1", 1.0), (16.65, "pop", 0.35), (17.57, "paper_fold2", 1.0), (18.72, "pop", 0.35),
    (19.45, "up1", 0.6), (20.2, "counter", 0.55), (20.85, "up2", 0.5),
    (24.25, "up1", 0.6), (27.45, "up2", 0.6), (28.86, "pop", 0.3), (30.1, "up1", 0.6), (33.85, "up2", 0.6), (36.05, "pop", 0.3),
    (37.6, "wind", 0.75), (38.0, "up1", 0.5), (40.95, "jet", 0.85),
    (42.85, "up2", 0.6), (45.4, "space", 0.8), (47.4, "up1", 0.6), (49.25, "radio", 0.8),
    (50.5, "counter", 0.5), (51.0, "up2", 0.5), (52.6, "big_pass", 0.8), (54.35, "counter", 0.5), (55.0, "up1", 0.5),
    (57.35, "riser", 0.75), (57.6, "heartbeat", 0.9), (59.1, "heartbeat", 0.9), (60.38, "moon_impact", 1.0),
    (62.25, "scratch", 0.9), (63.9, "pop", 0.5), (64.95, "pop", 0.5),
    (68.4, "warp", 0.85), (71.12, "flare", 0.8), (72.6, "warp", 0.85), (75.75, "cosmic", 1.0), (77.15, "rustle", 0.8),
]
dur_of = {f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/sfx/{f}.mp3"], capture_output=True, text=True).stdout) for f in {s[1] for s in SFX}}
audio = ['      <!-- Voiceover: ElevenLabs "Brian", eleven_v4, English -->']
for k, s in STARTS.items():
    audio.append(f'      <audio id="vo-{k}" class="clip" src="assets/vo/{k}.mp3" data-start="{s}" data-duration="{round(VO[k] - 0.01, 2)}" data-track-index="2" data-volume="1.8"></audio>')
audio.append('      <!-- Sound design (no music by request): custom ElevenLabs effects on their actions -->')
for i, (t, f, v) in enumerate(SFX, 1):
    audio.append(f'      <audio id="sfx-{i:02d}" class="clip" src="assets/sfx/{f}.mp3" data-start="{t}" data-duration="{round(min(dur_of[f], DUR - t) - 0.01, 2)}" data-track-index="{10 + i}" data-volume="{v}"></audio>')

index = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #000; font-family: "Inter", sans-serif; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      <div id="w" data-composition-id="w" data-composition-src="compositions/w.html" data-start="0" data-duration="{DUR}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="cap" data-composition-id="cap" data-composition-src="compositions/cap.html" data-start="0" data-duration="{DUR}" data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:10"></div>

{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
os.makedirs("compositions", exist_ok=True)
open("compositions/w.html", "w", encoding="utf-8").write(wcomp)
open("compositions/cap.html", "w", encoding="utf-8").write(cap)
open("index.html", "w", encoding="utf-8").write(index)
print(f"world {len(wcomp)//1024} KB, world height {WH}px, {len(caps)} captions, {len(SFX)} sound effects")
