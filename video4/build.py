#!/usr/bin/env python3
""""4,000 Weeks" — 90 s vertical (1080x1920) for YouTube Shorts.

One continuous world: a single glowing week zooms out into a 52 x 77 grid (one row = one year),
categories wipe weeks away, the used blocks fall out of frame, the camera flies into the one
week that goes dark. Everything that moves the camera is a pure function of time (seek-safe).

Run: python3 build.py   (writes index.html and compositions/*.html)
"""
import json, os

W, H = 1080, 1920
COLS, ROWS, CELL, PITCH = 52, 77, 10, 12
GX, GY = 228, 230                      # grid position in world space (camera identity)
GW, GH = COLS * PITCH - 2, ROWS * PITCH - 2

# weeks for a 25-year-old who lives to ~77 (4,004 weeks): lived, then what the rest goes to
CATS = [  # id, first, last (inclusive), fill, name, value
    ("lived", 0, 1299, "#1c1c1c", "Lived", "−1,300"),
    ("sleep", 1300, 2200, "#353535", "Sleep", "≈ 900"),
    ("work", 2201, 2695, "#525252", "Work", "≈ 500"),
    ("chores", 2696, 3033, "#6f6f6f", "Life admin", "≈ 340"),
    ("phone", 3034, 3371, "#939393", "Phone", "≈ 340"),
    ("free", 3372, 4003, None, "Yours", "≈ 600"),
]
DARK_CELL, THIS_CELL = 3372, 3373


def rc(i):
    return divmod(i, COLS)  # row, col


def cell_xy(i):
    r, c = rc(i)
    return c * PITCH, r * PITCH


def cells_path(a, b):
    out = []
    for i in range(a, b + 1):
        x, y = cell_xy(i)
        out.append(f"M{x} {y}h{CELL}v{CELL}h-{CELL}z")
    return "".join(out)


def mid_row(a, b):
    return (a / COLS + (b + 1) / COLS) / 2


VO = json.load(open("vo-durations.json"))
VO = {k: float(v) for k, v in VO.items()}
STARTS = {"e01": 0.5, "e02": 3.4, "e03": 9.6, "e03b": 14.8, "e04": 19.2, "e05": 25.9, "e06": 29.1, "e07": 31.9,
          "e08": 36.6, "e09": 43.6, "e10": 48.3, "e10b": 50.8, "e11": 58.2, "e11b": 61.6, "e12": 65.2,
          "e13": 71.6, "e14": 75.0, "e15": 81.0}

ICONS = {
    "lived": '<path d="M10 4h20M10 36h20M12 4c0 10 16 10 16 16s-16 6-16 16M28 4c0 10-16 10-16 16s16 6 16 16" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>',
    "sleep": '<path d="M25 5a15 15 0 1 0 10 25a12 12 0 1 1 -10 -25z" fill="#fff"/>',
    "work": '<rect x="5" y="13" width="30" height="21" rx="3" fill="none" stroke="#fff" stroke-width="3"/><path d="M15 13v-5h10v5M5 22h30" fill="none" stroke="#fff" stroke-width="3"/>',
    "chores": '<path d="M5 20 L20 7 L35 20 V35 H5 Z" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/><rect x="16" y="24" width="8" height="11" fill="#fff"/>',
    "phone": '<rect x="11" y="3" width="18" height="34" rx="4" fill="none" stroke="#fff" stroke-width="3"/><circle cx="20" cy="31" r="2" fill="#fff"/>',
    "free": '<circle cx="20" cy="20" r="7" fill="#fff"/><path d="M20 3v5M20 32v5M3 20h5M32 20h5M8 8l3.5 3.5M28.5 28.5L32 32M8 32l3.5-3.5M28.5 11.5L32 8" stroke="#fff" stroke-width="3" stroke-linecap="round"/>',
}

# ------------------------------------------------------------------ grid svg
defs = [
    f'<clipPath id="w-rv"><circle id="w-rvc" cx="{26 * PITCH + 5}" cy="{38 * PITCH + 5}" r="6.98"/></clipPath>',
    '<linearGradient id="w-shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="624" y2="924" spreadMethod="pad">'
    '<stop offset="0" stop-color="#dcdcdc"/><stop offset="0.44" stop-color="#dcdcdc"/><stop offset="0.5" stop-color="#ffffff"/>'
    '<stop offset="0.56" stop-color="#dcdcdc"/><stop offset="1" stop-color="#dcdcdc"/></linearGradient>',
]
groups = []
for cid, a, b, fill, _, _ in CATS:
    r0 = a // COLS
    r1 = b // COLS
    defs.append(f'<clipPath id="w-cw-{cid}"><rect id="w-cr-{cid}" x="-2" y="{r0 * PITCH - 1}" width="{GW + 4}" height="0"/></clipPath>')
    inner = f'<path class="base" d="{cells_path(a, b)}" fill="url(#w-shine)"/>'
    if fill:
        inner += f'<path id="w-ov-{cid}" d="{cells_path(a, b)}" fill="{fill}" clip-path="url(#w-cw-{cid})"/>'
    else:
        dx, dy = cell_xy(DARK_CELL)
        tx, ty = cell_xy(THIS_CELL)
        inner += (f'<path id="w-free-hi" d="{cells_path(a, b)}" fill="#ffffff" opacity="0"/>'
                  f'<rect id="w-dark" x="{dx}" y="{dy}" width="{CELL}" height="{CELL}" fill="#141414" opacity="0"/>'
                  f'<circle id="w-ring" cx="{tx + 5}" cy="{ty + 5}" r="9" fill="none" stroke="#fff" stroke-width="1.6" opacity="0"/>')
    groups.append(f'<g id="w-g-{cid}">{inner}</g>')
row_hi = f'<rect id="w-rowhi" x="-3" y="{38 * PITCH - 3}" width="0" height="{CELL + 6}" rx="3" fill="none" stroke="#fff" stroke-width="2"/>'
edge = f'<rect id="w-edge" x="-6" y="0" width="{GW + 12}" height="3" rx="1.5" fill="#fff" opacity="0" style="filter: drop-shadow(0 0 6px #fff)"/>'
grid_svg = (f'<svg id="w-grid" viewBox="-20 -20 {GW + 40} {GH + 40}" style="position:absolute;left:{GX - 20}px;top:{GY - 20}px;width:{GW + 40}px;height:{GH + 40}px;overflow:visible">'
            f'<defs>{"".join(defs)}</defs><g id="w-all" clip-path="url(#w-rv)">{"".join(groups)}</g>{row_hi}{edge}</svg>')

# ------------------------------------------------------------------ legend (screen space, grid shifted to x=60)
SCREEN_GX = 60
legend = []
for cid, a, b, _, name, val in CATS:
    y = GY + mid_row(a, b) * PITCH
    legend.append(
        f'<div id="w-lg-{cid}" class="abs lg clip" data-start="0" data-duration="90" style="top:{y - 40:.0f}px">'
        f'<div class="ld" style="top:39px"></div><svg class="li" viewBox="0 0 40 40">{ICONS[cid]}</svg>'
        f'<div class="lt"><div class="ln">{name}</div><div class="lv" id="w-lv-{cid}">{val}</div></div></div>')

FIG = '<svg id="w-fig" class="abs glow clip" data-start="0" data-duration="90" style="left:480px;top:905px;width:120px;height:195px" viewBox="0 0 80 130"><circle id="w-fig-head" cx="40" cy="24" r="20" fill="#fff"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="#fff"/></svg>'


def T(id, cls, style, inner=""):
    return f'<div id="{id}" class="abs {cls} clip" data-start="0" data-duration="90" style="{style}">{inner}</div>'


body = "\n    ".join([
    T("w-halo", "", "left:290px;top:510px;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle, rgba(255,255,255,0.35) 0%, rgba(255,255,255,0.06) 42%, rgba(255,255,255,0) 70%)"),
    f'<div id="w-cam" class="abs clip" data-start="0" data-duration="90" data-layout-allow-overflow style="left:0;top:0;width:1080px;height:1920px">{grid_svg}</div>',
    T("w-big", "big ctr glow", "top:330px;font-size:220px", "4,000"),
    T("w-weeks", "small ctr", "top:575px;font-size:34px", "weeks"),
    T("w-80", "ctr", "top:880px", '<span class="pill">If you make it to 80</span>'),
    T("w-rowlab", "ctr", "top:625px", '<span class="pill dark">1 row = 1 year</span>'),
    T("w-plenty", "ctr", "top:640px", '<span class="pill dark big2">4,000 weeks</span>'),
    T("w-ph", "", f"left:{SCREEN_GX - 8}px;top:{GY - 2}px;width:960px;height:4px",
      f'<div class="phl" style="width:{GW + 16}px"></div><span class="pill php">You · 25</span>'),
] + legend + [
    T("w-12y", "ctr", f"left:{SCREEN_GX}px;width:{GW}px;top:1050px", '<span class="pill dark">≈ 12 years</span>'),
    T("w-4k", "big ctr", "top:240px;font-size:150px;color:#8a8a8a", "4,000"),
    T("w-strike", "", "left:330px;top:318px;width:420px;height:12px;background:#fff;border-radius:6px"),
    T("w-600", "big ctr glow", "top:420px;font-size:190px", "600"),
    T("w-wl", "small ctr", "top:245px", "Weeks left"),
    T("w-cnt", "big ctr glow", "top:290px;font-size:150px", '<span id="w-c600">600</span><span id="w-c599" style="position:absolute;left:0;width:1080px;top:0;opacity:0">599</span>'),
    T("w-sun", "ctr", "top:880px", '<span class="pill dark">Sunday · 23:59</span>'),
    T("w-ground", "ground", "top:1100px"),
    FIG,
    T("w-t1", "ctr", "top:300px;font-size:76px;font-weight:800", "You don’t have time."),
    T("w-t2", "big ctr glow", "top:400px;font-size:104px", "You have weeks."),
    T("w-t3", "big ctr glow", "top:270px;font-size:100px;line-height:1.08", "Spend them<br>on purpose."),
    T("w-black", "", "left:0;top:0;width:1080px;height:1920px;background:#000;z-index:50"),
])

CSS = """
    #root { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, #141414 0%, #000 72%); font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }
    #root .abs { position: absolute; }
    #root .glow { filter: drop-shadow(0 0 16px rgba(255,255,255,0.55)); }
    #root .pill { font-weight: 700; font-size: 30px; letter-spacing: 0.18em; text-transform: uppercase; color: #d8d8d8; background: #141414; border: 2px solid #4a4a4a; border-radius: 999px; padding: 12px 26px; white-space: nowrap; display: inline-block; }
    #root .pill.dark { background: rgba(0,0,0,0.88); border-color: #fff; color: #fff; box-shadow: 0 0 24px rgba(0,0,0,0.9); }
    #root .pill.big2 { font-size: 40px; padding: 16px 34px; }
    #root .small { font-weight: 700; font-size: 30px; letter-spacing: 0.22em; text-transform: uppercase; color: #9a9a9a; }
    #root .big { font-weight: 900; letter-spacing: -0.03em; line-height: 1; }
    #root .ctr { left: 0; width: 1080px; text-align: center; }
    #root .ground { left: 0; width: 1080px; height: 0; border-top: 2px dashed rgba(255,255,255,0.32); }
    #root #w-cam { transform-origin: 0 0; }
    #root .lg { left: 704px; width: 360px; height: 80px; display: flex; align-items: center; gap: 16px; }
    #root .lg .ld { position: absolute; left: -20px; width: 18px; height: 2px; background: rgba(255,255,255,0.6); }
    #root .lg .li { width: 40px; height: 40px; flex: none; }
    #root .lg .ln { font-weight: 700; font-size: 28px; letter-spacing: 0.16em; text-transform: uppercase; color: #a0a0a0; line-height: 1.1; }
    #root .lg .lv { font-weight: 900; font-size: 44px; line-height: 1.05; }
    #root #w-lg-free .lv { font-size: 54px; }
    #root .phl { position: absolute; left: 0; top: 0; height: 3px; background: #fff; box-shadow: 0 0 10px #fff; border-radius: 2px; }
    #root .php { position: absolute; left: 650px; top: -30px; padding: 8px 18px; background: #fff; color: #000; border-color: #fff; }
"""

JS = """
    const tl = gsap.timeline({ paused: true });
    const $ = (s) => document.querySelector(s);
    const ss = (u) => u * u * (3 - 2 * u);
    const lerp = (a, b, u) => a + (b - a) * u;
    // keyframes -> value at t (smoothstep between keys)
    const at = (K, t, ease) => {
      if (t <= K[0][0]) return K[0].slice(1);
      for (let i = 1; i < K.length; i++) {
        if (t <= K[i][0]) {
          const u = (ease || ss)((t - K[i - 1][0]) / (K[i][0] - K[i - 1][0]));
          return K[i].slice(1).map((v, j) => lerp(K[i - 1][j + 1], v, u));
        }
      }
      return K[K.length - 1].slice(1);
    };
    // ---- camera: [t, log(scale), focusX, focusY, screenX, screenY] (world -> screen)
    const L = Math.log;
    const CAM = [
      [0, L(16), 545, 691, 540, 760], [7.35, L(16), 545, 691, 540, 760],
      [9.6, L(1), 545, 691, 545, 691],
      [18.25, L(1), 545, 691, 545, 691], [19.25, L(1), 545, 691, 377, 691],
      [56.4, L(1), 545, 691, 377, 691], [58.0, L(1.45), 540, 1081, 540, 780],
      [63.2, L(1.45), 540, 1081, 540, 780], [65.0, L(5.5), 761, 1003, 540, 760],
      [68.5, L(5.5), 761, 1003, 540, 760], [70.6, L(1.45), 540, 1081, 540, 720],
      [75.0, L(1.45), 540, 1081, 540, 720], [87.0, L(1.62), 540, 1081, 540, 712],
    ];
    const zoomEase = (u) => 1 - Math.pow(1 - u, 3);
    // ---- circular reveal radius around the first week
    const RV = [[0, 6.98], [7.4, 6.98], [9.5, 1100]];
    // ---- shine band position along the grid diagonal (-1 = before, +1 = after)
    const SH = [[0, -1], [10.85, -1], [12.1, 1], [12.11, -1], [15.05, -1], [16.4, 1], [16.41, -1], [75.15, -1], [76.7, 1]];
    const clock = { t: 0 };
    tl.fromTo(clock, { t: 0 }, { t: 90, duration: 90, ease: "none", onUpdate: () => {
      const t = clock.t;
      let seg = 0; for (let i = 1; i < CAM.length; i++) if (t > CAM[i - 1][0]) seg = i;
      const [ls, fx, fy, cx, cy] = at(CAM, t, (seg === 2 || seg === 8 || seg === 10) ? zoomEase : seg === 12 ? ((u) => u) : ss);
      const s = Math.exp(ls);
      gsap.set("#w-cam", { x: cx - s * fx, y: cy - s * fy, scale: s });
      $("#w-rvc").setAttribute("r", at(RV, t, (u) => u * u)[0].toFixed(1));
      const p = at(SH, t, (u) => u)[0];
      $("#w-shine").setAttribute("gradientTransform", `translate(${(p * 640).toFixed(1)} ${(p * 950).toFixed(1)})`);
    } }, 0);

    // ================= HOOK =================
    tl.fromTo("#w-big", { scale: 1 }, { scale: 1.06, duration: 0.18, yoyo: true, repeat: 1, ease: "power1.out" }, 1.5);
    tl.fromTo("#w-weeks", { opacity: 0.6 }, { opacity: 1, duration: 0.3 }, 2.2);
    tl.fromTo("#w-80", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, 4.55);
    // the title collapses into the week, then we pull back
    tl.to("#w-big", { scale: 0.08, y: 330, opacity: 0, duration: 0.55, ease: "power3.in" }, 6.9);
    tl.to("#w-weeks", { scale: 0.2, y: 170, opacity: 0, duration: 0.45, ease: "power3.in" }, 6.95);
    tl.to("#w-80", { opacity: 0, y: -20, duration: 0.3 }, 6.9);
    tl.fromTo("#w-halo", { opacity: 1, scale: 1 }, { opacity: 0, scale: 0.3, duration: 1.2, ease: "power2.in" }, 7.3);

    // ================= GRID =================
    tl.fromTo("#w-rowhi", { attr: { width: 0 }, opacity: 1 }, { attr: { width: 630 }, duration: 0.55, ease: "power2.inOut" }, 12.65);
    tl.to("#w-rowhi", { opacity: 0, duration: 0.4 }, 14.3);
    tl.fromTo("#w-rowlab", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, 12.95);
    tl.to("#w-rowlab", { opacity: 0, duration: 0.3 }, 14.4);
    tl.fromTo("#w-plenty", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 15.1);
    tl.to("#w-plenty", { opacity: 0, scale: 1.1, duration: 0.35 }, 17.95);

    // ================= TAKING WEEKS AWAY =================
    tl.fromTo("#w-ph", { opacity: 0, y: 0 }, { opacity: 1, duration: 0.3 }, 21.3);
    tl.to("#w-ph", { y: 25 * 12, duration: 1.15, ease: "power2.inOut" }, 21.6);
    const wipe = (cid, t, dur, ease) => {
      const r = $("#w-cr-" + cid);
      const rows = Math.ceil((CATS[cid][1] + 1) / 52) - Math.floor(CATS[cid][0] / 52);
      const y0 = Math.floor(CATS[cid][0] / 52) * 12 - 1;
      tl.fromTo(r, { attr: { height: 0 } }, { attr: { height: rows * 12 + 2 }, duration: dur, ease: ease || "power1.inOut" }, t);
      tl.fromTo("#w-edge", { attr: { y: y0 }, opacity: 1 }, { attr: { y: y0 + rows * 12 }, duration: dur, ease: ease || "power1.inOut", immediateRender: false }, t);
      tl.to("#w-edge", { opacity: 0, duration: 0.2 }, t + dur);
    };
    const CATS = { lived: [0, 1299], sleep: [1300, 2200], work: [2201, 2695], chores: [2696, 3033], phone: [3034, 3371] };
    const legendIn = (cid, t) => {
      tl.fromTo("#w-lg-" + cid, { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.8)" }, t);
      tl.fromTo("#w-lg-" + cid + " .ld", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.3 }, t);
    };
    wipe("lived", 23.25, 1.4);
    legendIn("lived", 24.85);
    wipe("sleep", 26.15, 1.6);
    legendIn("sleep", 27.9);
    wipe("work", 29.25, 1.15);
    legendIn("work", 30.55);
    wipe("chores", 31.95, 1.9, "steps(3)");
    legendIn("chores", 35.25);
    wipe("phone", 37.05, 0.85);
    legendIn("phone", 40.8);
    // the phone block flickers like a screen
    [37.95, 38.4, 38.55, 39.3, 39.42, 40.2, 41.0, 41.12, 41.9, 42.5].forEach((t, i) => {
      tl.to("#w-ov-phone", { opacity: i % 2 ? 1 : 0.55, duration: 0.06 }, t);
    });
    tl.to("#w-ov-phone", { opacity: 1, duration: 0.1 }, 42.9);

    // ================= WHAT'S LEFT =================
    tl.to(["#w-g-lived", "#w-g-sleep", "#w-g-work", "#w-g-chores", "#w-g-phone"], { opacity: 0.38, duration: 0.8, ease: "power2.inOut" }, 44.3);
    tl.to(["#w-lg-lived", "#w-lg-sleep", "#w-lg-work", "#w-lg-chores", "#w-lg-phone", "#w-ph"], { opacity: 0.3, duration: 0.8 }, 44.3);
    tl.fromTo("#w-free-hi", { opacity: 0 }, { opacity: 0.55, duration: 0.5, yoyo: true, repeat: 2, ease: "sine.inOut" }, 44.9);
    tl.to("#w-free-hi", { opacity: 1, duration: 0.5, ease: "power2.out" }, 46.4);
    tl.fromTo("#w-g-free", { filter: "drop-shadow(0 0 0px rgba(255,255,255,0))" }, { filter: "drop-shadow(0 0 7px rgba(255,255,255,0.9))", duration: 0.6 }, 46.4);
    legendIn("free", 49.05);
    tl.fromTo("#w-lv-free", { scale: 1.35, transformOrigin: "0% 50%" }, { scale: 1, duration: 0.5, ease: "back.out(2.5)" }, 49.05);
    tl.fromTo("#w-12y", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, 51.3);

    // ================= THE FALL =================
    tl.to(["#w-lg-lived", "#w-lg-sleep", "#w-lg-work", "#w-lg-chores", "#w-lg-phone", "#w-lg-free", "#w-ph", "#w-12y"], { opacity: 0, duration: 0.35 }, 54.1);
    ["lived", "sleep", "work", "chores", "phone"].forEach((cid, i) => {
      tl.to("#w-g-" + cid, { y: 1500, rotation: (i % 2 ? 6 : -5), svgOrigin: "312 400", opacity: 0, duration: 1.35, ease: "power2.in" }, 54.55 + i * 0.28);
    });

    // ================= NOT 4,000. 600. =================
    tl.fromTo("#w-4k", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 58.55);
    tl.fromTo("#w-strike", { scaleX: 0, opacity: 1, transformOrigin: "0% 50%" }, { scaleX: 1, opacity: 1, duration: 0.3, ease: "power2.out" }, 59.0);
    tl.to("#w-4k", { opacity: 0.35, duration: 0.3 }, 59.1);
    tl.fromTo("#w-600", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, 59.95);
    tl.to(["#w-4k", "#w-strike", "#w-600"], { opacity: 0, duration: 0.4 }, 62.9);

    // ================= ONE MORE GOES DARK =================
    tl.fromTo(["#w-wl", "#w-cnt"], { opacity: 0 }, { opacity: 1, duration: 0.4 }, 65.0);
    tl.fromTo("#w-sun", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, 65.85);
    [[67.0, 0.75], [67.12, 0], [67.3, 0.85], [67.4, 0.1], [67.55, 0.6]].forEach(([t, o]) => tl.to("#w-dark", { opacity: o, duration: 0.05 }, t));
    tl.to("#w-dark", { opacity: 1, duration: 0.08 }, 67.8);
    tl.fromTo("#w-c600", { opacity: 1 }, { opacity: 0, duration: 0.05 }, 67.85);
    tl.fromTo("#w-c599", { opacity: 0 }, { opacity: 1, duration: 0.05 }, 67.85);
    tl.fromTo("#w-cnt", { scale: 1.25 }, { scale: 1, duration: 0.4, ease: "back.out(2.5)" }, 67.85);
    tl.to("#w-sun", { opacity: 0, duration: 0.3 }, 68.4);
    tl.to(["#w-wl", "#w-cnt"], { opacity: 0, duration: 0.4 }, 70.9);

    // ================= THE FIGURE =================
    tl.fromTo("#w-ground", { opacity: 0, scaleX: 0.3 }, { opacity: 1, scaleX: 1, duration: 0.8, ease: "power2.out" }, 69.3);
    tl.fromTo("#w-fig", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 69.4);
    tl.fromTo("#w-fig", { x: -640 }, { x: 0, duration: 2.1, ease: "power1.out", immediateRender: false }, 69.4);
    [69.4, 69.92, 70.44, 70.96].forEach((t) => tl.fromTo("#w-fig", { y: 0 }, { y: -10, duration: 0.13, yoyo: true, repeat: 1, ease: "sine.out" }, t));
    tl.fromTo("#w-fig-head", { attr: { cy: 24 } }, { attr: { cy: 21 }, duration: 0.6, ease: "power2.out" }, 81.3);

    // ================= THE LINES =================
    tl.fromTo("#w-t1", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }, 71.7);
    tl.fromTo("#w-t2", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }, 73.2);
    tl.to(["#w-t1", "#w-t2"], { opacity: 0, y: -14, duration: 0.35 }, 74.7);
    tl.fromTo("#w-t3", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 75.12);
    // "starting with this one"
    tl.fromTo("#w-ring", { opacity: 0, attr: { r: 30 } }, { opacity: 1, attr: { r: 9 }, duration: 0.5, ease: "power3.out", immediateRender: false }, 81.75);
    [82.4, 83.6, 84.8, 86.0].forEach((t) => tl.fromTo("#w-ring", { attr: { r: 9 }, opacity: 1 }, { attr: { r: 15 }, opacity: 0.25, duration: 1.0, ease: "sine.out", immediateRender: false }, t));
    tl.fromTo("#w-black", { opacity: 0 }, { opacity: 1, duration: 2.3, ease: "power1.in" }, 87.6);
"""

# hide everything that enters later (initial states, authored once at t=0)
HIDE = ["#w-80", "#w-rowlab", "#w-plenty", "#w-ph", "#w-12y", "#w-4k", "#w-strike", "#w-600", "#w-wl", "#w-cnt", "#w-sun",
        "#w-ground", "#w-fig", "#w-t1", "#w-t2", "#w-t3", "#w-black"] + [f"#w-lg-{c[0]}" for c in CATS]
CSS += "    " + ", ".join(f"#root {h}" for h in HIDE) + " { opacity: 0; }\n"
JS = JS.replace("const CATS = { lived: [0, 1299], sleep: [1300, 2200], work: [2201, 2695], chores: [2696, 3033], phone: [3034, 3371] };", "")
JS = JS.replace("    const wipe = (cid, t, dur, ease) => {", "    const CATS = { lived: [0, 1299], sleep: [1300, 2200], work: [2201, 2695], chores: [2696, 3033], phone: [3034, 3371] };\n    const wipe = (cid, t, dur, ease) => {")

world = f"""<template>
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

# ------------------------------------------------------------------ captions
FIX = {"twenty-five,": "25,", "thirteen": "1,300", "hundred": None}
words = {}
for line in open("words.txt", encoding="utf-8"):
    k, *ws = line.split()
    words[k] = [(w.rsplit("@", 1)[0], float(w.rsplit("@", 1)[1])) for w in ws]
groups_c = []
for k, st in STARTS.items():
    cur, ws = [], words[k]
    i = 0
    while i < len(ws):
        w, t = ws[i]
        if k == "e04" and w == "thirteen":           # "thirteen hundred" -> "1,300"
            w = "1,300"; i += 1
        elif k == "e08" and w == "three" and i + 3 < len(ws) and ws[i + 1][0] == "hundred":
            w = "340"; i += 3                          # "three hundred and forty" -> "340"
        elif k == "e11" and w == "four":
            w = "4,000,"; i += 1
        elif k == "e11" and w == "six":
            w = "600."; i += 1
        elif w == "twenty-five,":
            w = "25,"
        cur.append((w, st + t))
        i += 1
        if len(cur) >= 3 or w[-1] in ".,?:!":
            groups_c.append(cur); cur = []
    if cur:
        groups_c.append(cur)
    groups_c[-1].append(("", st + VO[k]))
flat = []
for g in groups_c:
    end = g[-1][1] if g[-1][0] == "" else None
    flat.append(([x for x in g if x[0]], end))
caps = []
for i, (ws, end) in enumerate(flat):
    s = round(ws[0][1] - 0.05, 2)
    e = end if end is not None else flat[i + 1][0][0][1] - 0.05
    e = round(min(e, 89.0), 2)
    caps.append(f'<div id="cap-{i}" class="abs cap clip" data-start="{s}" data-duration="{round(e - s, 2)}"><span>{" ".join(w for w, _ in ws)}</span></div>')
cap = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; background: transparent; font-family: "Inter", sans-serif; }}
    #root .abs {{ position: absolute; }}
    #root .cap {{ left: 90px; width: 900px; top: 1180px; text-align: center; font-weight: 800; font-size: 56px; line-height: 1.15; color: #fff; text-shadow: 0 2px 4px #000; }}
    #root .cap span {{ display: inline-block; background: rgba(0,0,0,0.72); padding: 6px 22px 10px; border-radius: 16px; box-decoration-break: clone; -webkit-box-decoration-break: clone; }}
  </style>
  <div id="root" data-composition-id="cap" data-width="{W}" data-height="{H}">
    {chr(10).join("    " + c for c in caps)}
  </div>
  <script>
    window.__timelines["cap"] = gsap.timeline({{ paused: true }});
  </script>
</template>
"""

# ------------------------------------------------------------------ sound design (time, file, volume)
SFX = [
    (1.5, "ui_tick2", 0.5), (4.55, "pop", 0.55), (6.85, "swipe1", 0.6),
    (7.45, "zoom_whoosh", 0.9), (7.6, "shimmer", 0.75),
    (10.55, "shimmer", 0.4), (12.3, "row_scan", 0.6), (12.95, "pop", 0.4),
    (14.75, "shimmer", 0.35), (15.1, "pop", 0.5), (18.2, "swipe2", 0.6),
    (21.3, "ui_tick2", 0.5), (21.55, "ratchet", 0.7), (22.75, "ui_tick2", 0.6),
    (23.15, "swipe1", 0.6), (24.4, "power_down", 0.7), (24.85, "pop", 0.5),
    (26.05, "swipe2", 0.6), (27.9, "pop", 0.5),
    (29.15, "swipe1", 0.6), (30.55, "pop", 0.5),
    (31.95, "ui_tick2", 0.5), (32.6, "ui_tick2", 0.5), (33.25, "ui_tick2", 0.5), (35.25, "pop", 0.5),
    (36.95, "glitch", 0.55), (38.35, "glitch", 0.25), (40.8, "pop", 0.5),
    (43.0, "riser", 0.65), (44.25, "power_down", 0.45), (45.4, "swell", 0.7),
    (49.0, "impact", 0.85), (51.3, "pop", 0.45),
    (54.1, "fall", 0.9), (55.1, "fall", 0.55), (56.35, "swipe2", 0.55),
    (58.5, "strike", 0.8), (59.95, "pop", 0.6), (59.95, "impact", 0.45),
    (62.5, "clock_tick", 0.6), (63.15, "zoom_whoosh", 0.55), (63.5, "clock_tick", 0.6), (64.5, "clock_tick", 0.6),
    (65.5, "clock_tick", 0.6), (65.85, "pop", 0.4), (66.5, "clock_tick", 0.6),
    (67.0, "glitch", 0.2), (67.79, "clunk", 1.0), (67.8, "impact", 0.55), (67.85, "pop", 0.35),
    (68.3, "zoom_whoosh", 0.55), (69.3, "footsteps", 0.9),
    (71.7, "ui_tick2", 0.45), (73.2, "pop", 0.5), (74.6, "swell", 0.75),
    (81.5, "shimmer", 0.45), (81.75, "pop", 0.5),
]
DUR = {}
for f in set(s[1] for s in SFX):
    import subprocess
    DUR[f] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/sfx/{f}.mp3"], capture_output=True, text=True).stdout)
audio = ['      <!-- Voiceover: ElevenLabs "Brian", eleven_v4, English -->']
for k, s in STARTS.items():
    audio.append(f'      <audio id="vo-{k}" class="clip" src="assets/vo/{k}.mp3" data-start="{s}" data-duration="{round(VO[k] - 0.01, 2)}" data-track-index="2" data-volume="1.8"></audio>')
audio.append('      <!-- Score: four ElevenLabs sound-generation phases (wonder, pensive, tension, warm resolve) -->')
audio.append('      <audio id="bed" class="clip" src="assets/music/bed.mp3" data-start="0" data-duration="90" data-track-index="3" data-volume="0.55"></audio>')
audio.append('      <!-- Sound design: custom ElevenLabs effects, each on a visible action -->')
for n, (t, f, v) in enumerate(SFX, 1):
    d = round(min(DUR[f], 90 - t) - 0.01, 2)
    audio.append(f'      <audio id="sfx-{n:02d}" class="clip" src="assets/sfx/{f}.mp3" data-start="{t}" data-duration="{d}" data-track-index="{10 + n}" data-volume="{v}"></audio>')

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
    <div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">
      <div id="w" data-composition-id="w" data-composition-src="compositions/w.html" data-start="0" data-duration="90" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="cap" data-composition-id="cap" data-composition-src="compositions/cap.html" data-start="0" data-duration="90" data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:10"></div>

{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
os.makedirs("compositions", exist_ok=True)
open("compositions/w.html", "w", encoding="utf-8").write(world)
open("compositions/cap.html", "w", encoding="utf-8").write(cap)
open("index.html", "w", encoding="utf-8").write(index)
print(f"world {len(world)//1024} KB, {len(caps)} caption groups, {len(SFX)} sound effects")
