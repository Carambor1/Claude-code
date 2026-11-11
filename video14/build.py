#!/usr/bin/env python3
""""$1 Million vs $1 Billion vs $1 Trillion — to scale". One continuous zoom-out: a stack of $100 bills next to real things.
Everything on screen is a pure function of time (seek-safe): scale s(t) in px per metre, stack height H(t) in metres.
Facts: a US bill is 0.109 mm thick -> $1M = 10,000 bills = 1.09 m; $1B = 1.09 km; $1T = 1,090 km. Run: python3 build.py"""
import json, re, subprocess, math, random

VO = json.load(open("vo.json"))
ORDER = ["r1", "r2", "r3", "r4"]
GAP = {"r1": 0.5, "r2": 0.6, "r3": 0.7}
T, at = 0.3, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.3)
DUR = round(T + 2.2, 2)
W, H = 1080, 1920
G = "#4ade80"
def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)

GY, TOP = 1330, 700           # ground line (px), max stack height on screen (px)
S1, S2, S3 = math.log10(340), math.log10(TOP / 1090), math.log10(TOP / 1.09e6)
z2a, z2b = at["r2"] + 0.2, w("r2", "kilometer") + 0.5
z3a, z3b = at["r3"] + 0.4, w("r3", "thousand") + 0.6
g1a, g1b = 0.35, w("r1", "waist") + 0.05
KEYS = dict(S1=S1, S2=S2, S3=S3, z2a=z2a, z2b=z2b, z3a=z3a, z3b=z3b, g1a=g1a, g1b=g1b, GY=GY, TOP=TOP, DUR=DUR)

S = 'fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"'
SV = lambda vb, inner: f'<svg viewBox="{vb}" preserveAspectRatio="none">{inner}</svg>'
# ground objects: (id, label, height m, aspect w/h, x offset from centre, svg)
OBJ = [
    ("person", "You · 1.75 m", 1.75, 0.6, -230, SV("0 0 60 100", '<circle cx="30" cy="12" r="11" fill="#fff"/><path d="M8 100 V46 a22 22 0 0 1 44 0 V100 Z" fill="#fff"/>')),
    ("house", "House · 10 m", 10, 1.1, 250, SV("0 0 110 100", f'<path d="M6 46 L55 6 L104 46 V96 H6 Z M42 96 V64 H68 V96" {S}/>')),
    ("liberty", "Statue of Liberty · 93 m", 93, 0.34, -240, SV("0 0 34 100", f'<path d="M4 100 V62 H30 V100 Z M9 62 V34 C9 26 25 26 25 34 V62 M17 26 a6 6 0 1 0 0.1 0 M25 36 L31 6 M28 4 h6" {S}/>')),
    ("eiffel", "Eiffel Tower · 330 m", 330, 0.42, 250, SV("0 0 42 100", f'<path d="M21 2 V18 M17 18 H25 L33 62 H9 L17 18 M9 62 L2 100 M33 62 L40 100 M6 80 H36 M14 100 C14 84 28 84 28 100" {S}/>')),
    ("burj", "Burj Khalifa · 828 m", 828, 0.16, -210, SV("0 0 16 100", f'<path d="M8 0 V20 M6 20 H10 V40 H12 V62 H14 V100 H2 V70 H4 V44 H6 Z" {S}/>')),
    ("everest", "Mount Everest · 8.8 km", 8849, 1.9, 330, SV("0 0 190 100", f'<path d="M0 100 L70 30 L92 52 L120 2 L190 100 M104 30 L120 44 L132 26" {S}/>')),
]
# things in the air: (id, label, altitude m, html)
AIR = [
    ("plane", "Airliner · 11 km", 11000, -250, SV("0 0 120 50", f'<path d="M6 30 H92 C104 30 112 26 114 22 C104 20 96 20 88 20 L64 20 L44 2 H34 L46 20 H24 L14 10 H6 L12 24 Z M58 30 L44 46 H54 L74 30" {S}/>'), 120, 50),
    ("cloud", "Clouds · up to 12 km", 12000, 250, SV("0 0 120 60", f'<path d="M24 52 a18 18 0 0 1 4 -35 a24 24 0 0 1 46 -4 a20 20 0 0 1 22 39 Z" {S}/>'), 130, 65),
    ("karman", "Space begins · 100 km", 100000, 0, "", 0, 0),
    ("iss", "Space Station · 408 km", 408000, -250, SV("0 0 140 60", f'<path d="M50 24 H90 V36 H50 Z M70 10 V24 M70 36 V50 M4 14 H40 V46 H4 Z M100 14 H136 V46 H100 Z M40 30 H50 M90 30 H100 M16 14 V46 M28 14 V46 M112 14 V46 M124 14 V46" {S}/>'), 140, 60),
]
random.seed(7)
STARS = "".join(f'<i style="left:{random.randint(10, 1070)}px;top:{random.randint(120, 1250)}px;width:{sz}px;height:{sz}px;opacity:{random.uniform(0.3, 0.9):.2f}"></i>' for sz in [random.choice((2, 2, 3, 4)) for _ in range(90)])

objs = "".join(f'<div class="abs ob" id="o_{i}">{svg}</div><div class="abs lb" id="l_{i}">{lab}</div>' for i, lab, h, asp, dx, svg in OBJ)
airs = "".join((f'<div class="abs ar" id="a_{i}" style="width:{aw}px;height:{ah}px">{svg}</div>' if svg else f'<div class="abs kl" id="a_{i}"></div>') + f'<div class="abs lb" id="l_{i}">{lab}</div>' for i, lab, alt, dx, svg, aw, ah in AIR)
body = f"""
    <div class="abs stars" id="stars">{STARS}</div>
    <div class="abs earth" id="earth"></div>
    <div class="abs ground"></div>
    {objs}{airs}
    <div class="abs stack" id="stack"></div><div class="abs cap1" id="cap1"></div>
    <div class="abs tick" id="tick"><b id="rd">0 m</b></div>
    <div class="abs ctr amt" id="amt">$1 MILLION</div>
    <div class="abs ctr sub" id="sub">in $100 bills · to scale</div>
    <div class="abs px" id="px">↓ <b>$1B</b> stack: under 1 pixel</div>
    <div class="abs rec" id="rec"><div class="rr" id="rr0"><b>$1M</b><span>1.09 m</span></div><div class="rr" id="rr1"><b>$1B</b><span>1.09 km</span></div><div class="rr" id="rr2"><b>$1T</b><span>1,090 km</span></div></div>
"""
CSS = f"""
    #root {{ position: absolute; inset: 0; background-color: #000; background-image: radial-gradient(ellipse at 50% 60%, rgba(255,255,255,0.07), rgba(0,0,0,0) 62%), radial-gradient(rgba(255,255,255,0.14) 1.6px, transparent 1.8px); background-size: 100% 100%, 34px 34px; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
    #root .abs {{ position: absolute; }}
    #root .ctr {{ left: 0; width: {W}px; text-align: center; }}
    #root svg {{ width: 100%; height: 100%; display: block; overflow: visible; }}
    #root #lay {{ position: absolute; inset: 0; filter: drop-shadow(0 0 6px rgba(255,255,255,0.5)) drop-shadow(0 0 18px rgba(255,255,255,0.22)); }}
    #root .ground {{ left: 0; top: {GY}px; width: {W}px; height: 0; border-top: 3px solid rgba(255,255,255,0.75); }}
    #root .earth {{ left: 0; top: 0; border-radius: 50%; border: 3px solid #fff; background: #0b1730; opacity: 0; }}
    #root .px {{ left: 590px; top: {GY - 96}px; font-weight: 800; font-size: 34px; color: #fff; background: rgba(0,0,0,0.7); padding: 4px 14px; border-radius: 10px; opacity: 0; }}
    #root .px b {{ color: {G}; }}
    #root .stars i {{ position: absolute; background: #fff; border-radius: 50%; }}
    #root .stars {{ inset: 0; opacity: 0; }}
    #root .ob, #root .ar, #root .lb, #root .kl {{ opacity: 0; left: 0; top: 0; will-change: transform; }}
    #root .lb {{ font-weight: 700; font-size: 30px; letter-spacing: 0.04em; white-space: nowrap; color: #e6e6e6; background: rgba(0,0,0,0.6); padding: 2px 10px; border-radius: 8px; }}
    #root .kl {{ width: {W}px; height: 0; border-top: 3px dashed rgba(140,190,255,0.9); }}
    #root .stack {{ left: 0; top: 0; background: repeating-linear-gradient(0deg, {G} 0 5px, #2fa862 5px 7px); border-radius: 4px 4px 0 0; box-shadow: 0 0 24px rgba(74,222,128,0.65); transform-origin: 0 0; }}
    #root .cap1 {{ left: 0; top: 0; height: 0; border-top: 4px solid {G}; }}
    #root .tick {{ left: 0; top: 0; white-space: nowrap; }}
    #root .tick b {{ display: inline-block; font-weight: 900; font-size: 64px; letter-spacing: -0.02em; color: {G}; font-variant-numeric: tabular-nums; background: rgba(0,0,0,0.65); padding: 0 14px; border-radius: 12px; }}
    #root .amt {{ top: 230px; font-weight: 900; font-size: 118px; letter-spacing: -0.03em; }}
    #root .sub {{ top: 372px; font-weight: 700; font-size: 34px; letter-spacing: 0.2em; text-transform: uppercase; color: #bdbdbd; }}
    #root .rec {{ left: 70px; top: 560px; width: 400px; display: flex; flex-direction: column; gap: 18px; }}
    #root .rr {{ display: flex; align-items: baseline; justify-content: space-between; border: 3px solid #fff; border-radius: 18px; padding: 12px 22px; background: #000; opacity: 0; }}
    #root .rr b {{ font-weight: 900; font-size: 52px; }}
    #root .rr span {{ font-weight: 800; font-size: 44px; color: {G}; }}
"""
JS = r"""
    const K = __KEYS__, OBJ = __OBJ__, AIR = __AIR__;
    const R = document.querySelector('[data-composition-id="w"]') || document;
    const $ = (s) => R.querySelector(s);
    const sm = (a, b, t) => { const x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * x * (x * (x * 6 - 15) + 10); };
    const lerp = (a, b, x) => a + (b - a) * x;
    const fmt = (m) => m < 1000 ? (m < 10 ? m.toFixed(2) : Math.round(m)) + " m" : m < 1e5 ? (m / 1000).toFixed(m < 1e4 ? 2 : 1) + " km" : Math.round(m / 1000).toLocaleString("en-US") + " km";
    const band = (v, a, b, c, d) => v <= a || v >= d ? 0 : v < b ? (v - a) / (b - a) : v > c ? (d - v) / (d - c) : 1;
    const set = (el, x, y, o, w, h) => { el.style.opacity = o; el.style.transform = "translate(" + x.toFixed(1) + "px," + y.toFixed(1) + "px)"; if (w !== undefined) { el.style.width = w.toFixed(1) + "px"; el.style.height = h.toFixed(1) + "px"; } };
    const el = {}; ["stack", "cap1", "tick", "rd", "stars", "earth"].forEach((k) => el[k] = $("#" + k));
    OBJ.concat(AIR).forEach((o) => { o.e = $("#" + (o.air ? "a_" : "o_") + o.id); o.l = $("#l_" + o.id); });
    function frame(t) {
      const ls = t < K.z3a ? lerp(K.S1, K.S2, sm(K.z2a, K.z2b, t)) : lerp(K.S2, K.S3, sm(K.z3a, K.z3b, t));
      const s = Math.pow(10, ls);
      const cap = t < K.z2a ? 1.09 * sm(K.g1a, K.g1b, t) : t < K.z3a ? Math.pow(10, lerp(Math.log10(1.09), Math.log10(1090), sm(K.z2a, K.z2a + 0.5, t))) : Math.pow(10, lerp(Math.log10(1090), Math.log10(1.09e6), sm(K.z3a, K.z3a + 0.5, t)));
      const Hm = Math.min(cap, K.TOP / s), hp = Hm * s, sw = Math.max(26, 0.156 * s);
      set(el.stack, 540 - sw / 2, K.GY - hp, hp > 0.5 ? 1 : 0, sw, hp);
      set(el.cap1, 540 - sw / 2 - 14, K.GY - hp, hp > 0.5 ? 1 : 0); el.cap1.style.width = (sw + 28) + "px";
      set(el.tick, 540 + sw / 2 + 30, K.GY - hp - 40, hp > 0.5 ? 1 : 0); el.rd.textContent = fmt(Hm);
      OBJ.forEach((o) => { const h = o.h * s, wd = h * o.asp, x = 540 + o.dx - wd / 2, op = band(h, 5, 26, 760, 1000);
        set(o.e, x, K.GY - h, op, wd, h);
        const lo = band(h, 110, 170, 640, 900) * (o.id === "person" ? (t < K.z2a + 0.2 ? 1 : 0) : 1);
        set(o.l, o.dx < 0 ? Math.max(16, x + wd / 2 - 150) : Math.min(700, x + wd / 2 - 150), K.GY + 18, lo); });
      AIR.forEach((o) => { const y = K.GY - o.h * s, v = K.GY - y, op = band(v, 70, 130, 640, 780);
        if (o.id === "karman") { set(o.e, 0, y, op); set(o.l, 600, y - 50, op); }
        else { const x = 540 + o.dx - o.w / 2; set(o.e, x, y - o.hh / 2, op); set(o.l, o.dx < 0 ? 40 : 600, y + o.hh / 2 + 8, op); } });
      const sp = sm(K.z3a + 0.3, K.z3b - 0.6, t);
      el.stars.style.opacity = sp;
      const edT = 2 * 6.371e6 * s, ed = Math.min(40000, edT); el.earth.style.width = el.earth.style.height = ed.toFixed(0) + "px";
      el.earth.style.transform = "translate(" + (540 - ed / 2).toFixed(1) + "px," + K.GY + "px)"; el.earth.style.opacity = 1 - sm(24000, 40000, edT);
    }
    const tl = gsap.timeline({ paused: true });
    const clock = { t: 0 };
    tl.fromTo(clock, { t: 0 }, { t: K.DUR, duration: K.DUR, ease: "none", onUpdate: () => frame(clock.t) }, 0);
    frame(0);
"""
J = []; a = J.append
SFX = []; sx = lambda t, f, v=0.35: SFX.append((round(max(0, t), 2), f, v))
# amount label swaps
a('tl.fromTo("#amt", { scale: 0.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, 0.05);')
a('tl.fromTo("#sub", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.3);')
for k, txt in (("r2", "$1 BILLION"), ("r3", "$1 TRILLION")):
    t0 = at[k] + 0.1
    a(f'tl.to("#amt", {{ scale: 0.7, opacity: 0, duration: 0.18, ease: "power2.in" }}, {t0 - 0.2:.2f});')
    a(f'tl.call(() => {{ $("#amt").textContent = "{txt}"; }}, null, {t0:.2f});')
    a(f'tl.fromTo("#amt", {{ scale: 1.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)", immediateRender: false }}, {t0:.2f});')
    sx(t0, "impact", 0.42)
a(f'tl.to("#sub", {{ opacity: 0, duration: 0.3 }}, {at["r3"]:.2f});')
# recap
for i, t0 in enumerate((w("r4", "gap") - 0.1, w("r4", "million"), w("r4", "trillion"))):
    a(f'tl.fromTo("#rr{i}", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, {t0:.2f});'); sx(t0, "pop", 0.32)
a(f'tl.fromTo("#px", {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }}, {w("r4", "trillion") + 0.5:.2f});'); sx(w("r4", "trillion") + 0.5, "ui_tick2", 0.4)
a(f'tl.fromTo("#rec", {{ scale: 1 }}, {{ scale: 1.04, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut", transformOrigin: "0 50%" }}, {w("r4", "which"):.2f});'); sx(w("r4", "which"), "ping", 0.38)
sx(0, "boom_open", 0.3); sx(g1a, "count_fast", 0.3); sx(g1b, "kaching", 0.4)
sx(z2a, "riser", 0.3); sx(z2a + 0.2, "zoom_whoosh", 0.3); sx(z2b - 0.2, "impact", 0.45); sx(w("r2", "tallest"), "ui_tick2", 0.4)
sx(z3a, "riser", 0.32); sx(z3a + 0.2, "zoom_whoosh", 0.32); sx(w("r3", "clouds"), "swipe1", 0.3); sx(w("r3", "space"), "swipe2", 0.3); sx(z3b - 0.2, "impact", 0.5); sx(z3b, "shimmer", 0.35)

objs_js = json.dumps([dict(id=i, h=h, asp=asp, dx=dx) for i, lab, h, asp, dx, svg in OBJ])
airs_js = json.dumps([dict(id=i, h=alt, dx=dx, w=aw, hh=ah, air=1) for i, lab, alt, dx, svg, aw, ah in AIR])
JS = JS.replace("__KEYS__", json.dumps(KEYS)).replace("__OBJ__", objs_js).replace("__AIR__", airs_js)
open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    <div id="lay">{body}</div>
  </div>
  <script>
{JS}
{chr(10).join("    " + x for x in J)}
    window.__timelines["w"] = tl;
  </script>
</template>
""")

grp = []
for k in ORDER:
    cur = []
    for wd, t in VO[k]["words"]:
        cur.append((wd, at[k] + t))
        if len(cur) >= 3 or wd[-1] in ".,?:!":
            grp.append([cur, None]); cur = []
    if cur:
        grp.append([cur, None])
    grp[-1][1] = at[k] + VO[k]["dur"]
caps = []
for i, (ws, end) in enumerate(grp):
    s = round(ws[0][1] - 0.05, 2)
    e2 = end if end is not None else grp[i + 1][0][0][1] - 0.05
    caps.append(f'<div id="cap{i}" class="abs cap clip" data-start="{s}" data-duration="{round(min(e2, DUR - 0.05) - s, 2)}"><span>{" ".join(x for x, _ in ws)}</span></div>')
open("compositions/cap.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; }}
    #root .abs {{ position: absolute; }}
    #root .cap {{ left: 90px; width: 900px; top: 1480px; text-align: center; font-weight: 800; font-size: 58px; line-height: 1.15; color: #fff; }}
    #root .cap span {{ display: inline-block; background: rgba(0,0,0,0.86); padding: 6px 22px 10px; border-radius: 16px; }}
  </style>
  <div id="root" data-composition-id="cap" data-width="{W}" data-height="{H}">
{chr(10).join("    " + c for c in caps)}
  </div>
  <script>window.__timelines["cap"] = gsap.timeline({{ paused: true }});</script>
</template>
""")

dur = {f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/sfx/{f}.mp3"], capture_output=True, text=True).stdout) for f in {x[1] for x in SFX}}
aud = [f'  <audio id="vo-{k}" class="clip" src="assets/vo/{k}.mp3" data-start="{round(at[k], 2)}" data-duration="{round(VO[k]["dur"] - 0.01, 2)}" data-track-index="2" data-volume="1.8"></audio>' for k in ORDER]
aud += [f'  <audio id="sx{n}" class="clip" src="assets/sfx/{f}.mp3" data-start="{max(0, t)}" data-duration="{round(min(dur[f], DUR - t) - 0.01, 2)}" data-track-index="{10 + n}" data-volume="{v}"></audio>' for n, (t, f, v) in enumerate(SFX) if t < DUR - 0.2]
open("index.html", "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" />
<script src="assets/vendor/gsap.min.js"></script>
<style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }} #root {{ position: relative; width: 100%; height: 100%; background: #000; }}</style>
</head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
  <div id="w" data-composition-id="w" data-composition-src="compositions/w.html" data-start="0" data-duration="{DUR}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>
  <div id="cap" data-composition-id="cap" data-composition-src="compositions/cap.html" data-start="0" data-duration="{DUR}" data-track-index="5" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:10"></div>
{chr(10).join(aud)}
</div>
<script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>
""")
print("duration", DUR, "sfx", len(SFX))
print({k: round(v, 2) for k, v in at.items()})
