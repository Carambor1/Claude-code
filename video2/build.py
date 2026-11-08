#!/usr/bin/env python3
"""Generates the scene HTML for "Deine 3 Stunden" (1080x1920, YouTube Shorts).
Run from this folder: python3 build.py  — then edit the generated files freely or re-run."""
import json, os

W, H = 1080, 1920
BASE = """
    #root { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 55%, #161616 0%, #000 70%); font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }
    #root .abs { position: absolute; }
    #root .glow { filter: drop-shadow(0 0 16px rgba(255,255,255,0.55)); }
    #root .pill { font-weight: 700; font-size: 30px; letter-spacing: 0.18em; text-transform: uppercase; color: #d0d0d0; background: #141414; border: 2px solid #4a4a4a; border-radius: 999px; padding: 12px 26px; white-space: nowrap; display: inline-block; }
    #root .small { font-weight: 700; font-size: 30px; letter-spacing: 0.22em; text-transform: uppercase; color: #9a9a9a; }
    #root .big { font-weight: 900; letter-spacing: -0.03em; line-height: 1; }
    #root .ctr { left: 0; width: 1080px; text-align: center; }
    #root .ground { left: 0; width: 1080px; top: 1040px; height: 0; border-top: 2px dashed rgba(255,255,255,0.32); }
"""
FIG = '<svg id="{id}" class="abs {cls} clip" data-start="0" data-duration="{d}" style="left:{x}px;top:{y}px;width:120px;height:195px" viewBox="0 0 80 130"><circle cx="40" cy="24" r="20" fill="{c}"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="{c}"/></svg>'


def clip(id, d, cls, style, inner=""):
    return f'<div id="{id}" class="abs {cls} clip" data-start="0" data-duration="{d}" style="{style}">{inner}</div>'


def scene(sid, d, css, body, js, bg=None):
    return f"""<template>
  <style>{BASE}{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
    {body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const $ = (s) => document.querySelector(s);
    const de = (n) => Math.round(n).toLocaleString("de-DE");
{js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""


def ids(*a):
    return json.dumps(list(a))


scenes = {}

# ---------- s01 hook 0–8 ----------
d = 8
scenes["s01"] = scene("s01", d, """
    #s01-q { top: 300px; font-size: 120px; }
    #s01-strike { left: 170px; top: 362px; width: 740px; height: 10px; background: #fff; border-radius: 5px; }
    #s01-three { top: 500px; font-size: 170px; }
    #s01-each { top: 700px; }
    #s01-phone { left: 572px; top: 918px; width: 42px; height: 70px; border-radius: 9px; background: #fff; box-shadow: 0 0 40px 8px rgba(255,255,255,0.55); }
    #s01-beam { left: 470px; top: 820px; width: 160px; height: 120px; background: radial-gradient(ellipse at 70% 90%, rgba(255,255,255,0.35), rgba(255,255,255,0) 70%); }
    #s01-you { top: 1065px; }
""", "\n    ".join([
    clip("s01-ground", d, "ground", ""),
    clip("s01-beam", d, "", ""),
    FIG.format(id="s01-fig", cls="glow", d=d, x=480, y=845, c="#fff"),
    clip("s01-phone", d, "", ""),
    clip("s01-you", d, "small ctr", "", "Du"),
    clip("s01-q", d, "big ctr glow", "", "Keine Zeit?"),
    clip("s01-strike", d, "", ""),
    clip("s01-three", d, "big ctr glow", "", "3 Stunden"),
    clip("s01-each", d, "ctr", "", '<span class="pill">Jeden Tag</span>'),
]), """
    tl.fromTo("#s01-strike", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, 2.4);
    tl.to("#s01-q", { opacity: 0.35, duration: 0.3 }, 2.5);
    tl.fromTo("#s01-three", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }, 3.55);
    tl.fromTo("#s01-each", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 4.75);
    tl.fromTo("#s01-phone", { opacity: 0.75 }, { opacity: 1, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }, 5.9);
    tl.fromTo("#s01-beam", { opacity: 0.6 }, { opacity: 1, duration: 0.6 }, 5.9);
    tl.to(""" + ids("#s01-q", "#s01-strike", "#s01-three", "#s01-each", "#s01-you", "#s01-fig", "#s01-phone", "#s01-beam", "#s01-ground") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 7.65);
""")

# ---------- s02 year math 8–16 ----------
d = 8
scenes["s02"] = scene("s02", d, """
    #s02-k { top: 300px; }
    #s02-h { top: 345px; font-size: 170px; }
    #s02-x { top: 560px; }
    #s02-n { top: 690px; font-size: 200px; }
    #s02-u { top: 905px; }
""", "\n    ".join([
    clip("s02-k", d, "small ctr", "", "Bildschirmzeit · Ø pro Tag"),
    clip("s02-h", d, "big ctr glow", "", "≈ 3 h"),
    clip("s02-x", d, "ctr", "", '<span class="pill">× 365 Tage</span>'),
    clip("s02-n", d, "big ctr glow", "", "0"),
    clip("s02-u", d, "small ctr", "", "Stunden pro Jahr"),
]), """
    tl.fromTo(["#s02-k", "#s02-h"], { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.4, stagger: 0.1, ease: "power2.out" }, 0.3);
    tl.fromTo("#s02-x", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 2.85);
    tl.fromTo("#s02-n", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 3.6);
    const c = { v: 0 };
    tl.fromTo(c, { v: 0 }, { v: 1095, duration: 1.0, ease: "power2.out", onUpdate: () => { $("#s02-n").textContent = de(c.v); } }, 3.6);
    tl.fromTo("#s02-u", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 4.5);
    tl.fromTo("#s02-n", { scale: 1 }, { scale: 1.06, duration: 0.25, yoyo: true, repeat: 1, ease: "power1.inOut" }, 4.6);
    tl.to(""" + ids("#s02-k", "#s02-h", "#s02-x", "#s02-n", "#s02-u") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 7.65);
""")

# ---------- s03 45 days grid 16–22 ----------
d = 6
cells = []
COLS, SZ, GAP, TOP, LEFT = 21, 30, 6, 440, 162
for i in range(365):
    r, cc = divmod(i, COLS)
    cls = "cell on" if i < 45 else "cell"
    cells.append(f'<rect class="{cls}" x="{LEFT + cc * (SZ + GAP)}" y="{TOP + r * (SZ + GAP)}" width="{SZ}" height="{SZ}" rx="4"/>')
scenes["s03"] = scene("s03", d, """
    #s03-big { top: 210px; font-size: 130px; }
    #s03-pill { top: 362px; }
    #s03-grid { left: 0; top: 0; width: 1080px; height: 1920px; }
    #s03-grid .cell { fill: #0c0c0c; stroke: #3a3a3a; stroke-width: 2; }
""", "\n    ".join([
    clip("s03-big", d, "big ctr glow", "", "45 Tage"),
    clip("s03-pill", d, "ctr", "", '<span class="pill">Wach · Blick nach unten</span>'),
    f'<svg id="s03-grid" class="abs clip" data-start="0" data-duration="{d}" viewBox="0 0 1080 1920">' + "".join(cells) + "</svg>",
]), """
    tl.fromTo("#s03-grid", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0);
    tl.fromTo("#s03-grid .on", { fill: "#0c0c0c", stroke: "#3a3a3a" }, { fill: "#ffffff", stroke: "#ffffff", duration: 0.12, stagger: 0.022 }, 0.3);
    tl.fromTo("#s03-big", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 0.3);
    tl.fromTo("#s03-pill", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 2.5);
    tl.to(""" + ids("#s03-big", "#s03-pill", "#s03-grid") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 5.65);
""")

# ---------- s04 ten years 22–27.5 ----------
d = 5.5
bars = []
for i in range(10):
    y = 470 + i * 58
    bars.append(f'<rect class="bar" x="160" y="{y}" width="760" height="40" rx="8"/>')
    bars.append(f'<text class="yl" x="140" y="{y + 30}" text-anchor="end">{i + 1}</text>')
# 1.25 years highlighted = whole bar 1 + quarter of bar 2
bars.append('<rect id="s04-hi1" x="160" y="470" width="760" height="40" rx="8" fill="#fff"/>')
bars.append('<rect id="s04-hi2" x="160" y="528" width="190" height="40" rx="8" fill="#fff"/>')
scenes["s04"] = scene("s04", d, """
    #s04-k { top: 215px; }
    #s04-big { top: 262px; font-size: 130px; }
    #s04-chart { left: 0; top: 0; width: 1080px; height: 1920px; }
    #s04-chart .bar { fill: #0c0c0c; stroke: #555; stroke-width: 2; }
    #s04-chart .yl { fill: #8a8a8a; font: 700 28px Inter, sans-serif; }
    #s04-lab { top: 1075px; }
""", "\n    ".join([
    clip("s04-k", d, "small ctr", "", "In 10 Jahren"),
    clip("s04-big", d, "big ctr glow", "", "> 1 Jahr"),
    f'<svg id="s04-chart" class="abs clip" data-start="0" data-duration="{d}" viewBox="0 0 1080 1920">' + "".join(bars) + "</svg>",
    clip("s04-lab", d, "small ctr", "", "≈ 1,25 Jahre nur am Handy"),
]), """
    tl.fromTo("#s04-k", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35 }, 0.3);
    tl.fromTo("#s04-chart .bar", { opacity: 0, scaleX: 0, transformOrigin: "0% 50%" }, { opacity: 1, scaleX: 1, duration: 0.3, stagger: 0.07, ease: "power2.out" }, 0.4);
    tl.fromTo("#s04-chart .yl", { opacity: 0 }, { opacity: 1, duration: 0.3, stagger: 0.07 }, 0.4);
    tl.fromTo(["#s04-hi1", "#s04-hi2"], { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.45, stagger: 0.4, ease: "power2.inOut" }, 2.4);
    tl.fromTo("#s04-big", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 3.0);
    tl.fromTo("#s04-lab", { opacity: 0 }, { opacity: 1, duration: 0.35 }, 3.4);
    tl.to(""" + ids("#s04-k", "#s04-big", "#s04-chart", "#s04-lab") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 5.15);
""")

# ---------- s05 1000 hours 27.5–37.5 ----------
d = 10
ICON = {
    "talk": '<path d="M10 14 h60 a8 8 0 0 1 8 8 v30 a8 8 0 0 1 -8 8 h-34 l-14 12 v-12 h-12 a8 8 0 0 1 -8 -8 v-30 a8 8 0 0 1 8 -8 z" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/>',
    "note": '<path d="M34 62 V16 l34 -6 v44" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/><circle cx="26" cy="62" r="9" fill="#fff"/><circle cx="60" cy="56" r="9" fill="#fff"/>',
    "gym": '<rect x="4" y="28" width="10" height="28" rx="3" fill="#fff"/><rect x="16" y="20" width="10" height="44" rx="3" fill="#fff"/><rect x="26" y="38" width="32" height="8" fill="#fff"/><rect x="58" y="20" width="10" height="44" rx="3" fill="#fff"/><rect x="70" y="28" width="10" height="28" rx="3" fill="#fff"/>',
}
cards = []
for i, (key, label) in enumerate([("talk", "Eine Sprache"), ("note", "Ein Instrument"), ("gym", "Ein neuer Körper")]):
    top = 480 + i * 205
    cards.append(clip(f"s05-c{i}", d, "card", f"top:{top}px",
                      f'<svg viewBox="0 0 84 84" class="ic">{ICON[key]}</svg><span>{label}</span>'))
scenes["s05"] = scene("s05", d, """
    #s05-big { top: 230px; font-size: 150px; }
    #s05-u { top: 395px; }
    #root .card { left: 160px; width: 760px; height: 175px; border: 3px solid #fff; border-radius: 22px; display: flex; align-items: center; gap: 40px; padding: 0 50px; font-weight: 800; font-size: 54px; background: #070707; box-shadow: 0 0 30px rgba(255,255,255,0.18); }
    #root .card .ic { width: 84px; height: 84px; flex: none; }
""", "\n    ".join([
    clip("s05-big", d, "big ctr glow", "", "1.000 h"),
    clip("s05-u", d, "small ctr", "", "Was wäre möglich?"),
] + cards), """
    tl.fromTo("#s05-big", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 1.3);
    tl.fromTo("#s05-u", { opacity: 0 }, { opacity: 1, duration: 0.35 }, 1.7);
    [3.75, 5.05, 6.55].forEach((t, i) => {
      tl.fromTo("#s05-c" + i, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, t);
      if (i > 0) tl.to("#s05-c" + (i - 1), { opacity: 0.45, duration: 0.3 }, t);
    });
    tl.to(["#s05-c0", "#s05-c1"], { opacity: 1, duration: 0.3 }, 8.4);
    tl.to(""" + ids("#s05-big", "#s05-u", "#s05-c0", "#s05-c1", "#s05-c2") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 9.65);
""")

# ---------- s06 experiment start 37.5–45.5 ----------
d = 8
scenes["s06"] = scene("s06", d, """
    #s06-k { top: 290px; }
    #s06-big { top: 370px; font-size: 160px; }
    #s06-phone { left: 572px; top: 918px; width: 42px; height: 70px; border-radius: 9px; background: #fff; box-shadow: 0 0 40px 8px rgba(255,255,255,0.55); }
    #s06-lang { top: 570px; }
    #s06-bub { left: 300px; top: 670px; width: 330px; height: 120px; border: 3px solid #fff; border-radius: 26px; background: #070707; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 56px; box-shadow: 0 0 30px rgba(255,255,255,0.25); }
    #s06-bub::after { content: ""; position: absolute; left: 190px; bottom: -22px; width: 36px; height: 36px; background: #070707; border-right: 3px solid #fff; border-bottom: 3px solid #fff; transform: rotate(45deg); }
""", "\n    ".join([
    clip("s06-ground", d, "ground", ""),
    FIG.format(id="s06-fig", cls="glow", d=d, x=480, y=845, c="#fff"),
    clip("s06-phone", d, "", ""),
    clip("s06-k", d, "ctr", "", '<span class="pill">Das Experiment</span>'),
    clip("s06-big", d, "big ctr glow", "", "100 Tage"),
    clip("s06-lang", d, "small ctr", "", "3 h am Tag · Spanisch"),
    clip("s06-bub", d, "", "", "¡Hola!"),
]), """
    tl.fromTo(["#s06-ground", "#s06-fig", "#s06-phone"], { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0);
    tl.fromTo("#s06-k", { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 0.3);
    tl.fromTo("#s06-big", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 1.8);
    // The phone leaves his hand and lands on the ground to the right (it returns at the end)
    tl.to("#s06-phone", { x: 200, y: 98, rotation: 90, duration: 0.6, ease: "power2.in" }, 4.3);
    tl.to("#s06-phone", { boxShadow: "0 0 0px 0px rgba(255,255,255,0)", backgroundColor: "#2a2a2a", duration: 0.4 }, 4.9);
    tl.fromTo("#s06-lang", { opacity: 0 }, { opacity: 1, duration: 0.35 }, 5.6);
    tl.fromTo("#s06-bub", { opacity: 0, scale: 0.5, transformOrigin: "60% 100%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.2)" }, 6.75);
    tl.to(""" + ids("#s06-k", "#s06-big", "#s06-lang", "#s06-bub") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 7.65);
""")

# ---------- s07 the experiment + cliffhanger 45.5–85.5 ----------
d = 40
scenes["s07"] = scene("s07", d, """
    #s07-k { top: 205px; }
    #s07-day { top: 245px; font-size: 150px; }
    #s07-track { left: 160px; top: 428px; width: 760px; height: 14px; border: 2px solid #666; border-radius: 8px; }
    #s07-fill { left: 160px; top: 428px; width: 760px; height: 14px; background: #fff; border-radius: 8px; box-shadow: 0 0 14px rgba(255,255,255,0.6); }
    #s07-of { top: 456px; font-size: 28px; }
    #root .box { top: 520px; width: 360px; height: 150px; border: 2px solid #777; border-radius: 16px; text-align: center; padding-top: 20px; }
    #root .box .lab { font-weight: 700; font-size: 28px; letter-spacing: 0.2em; text-transform: uppercase; color: #9a9a9a; }
    #root .box .val { font-weight: 900; font-size: 72px; margin-top: 6px; }
    #s07-bh { left: 160px; } #s07-bw { left: 560px; }
    #s07-p1, #s07-p2, #s07-p3, #s07-p4 { top: 712px; }
    #s07-ghost { left: 604px; top: 900px; width: 48px; height: 78px; border: 3px dashed rgba(255,255,255,0.8); border-radius: 10px; }
    #s07-book { left: 495px; top: 945px; width: 90px; height: 56px; border: 3px solid #fff; background: #111; border-radius: 4px; z-index: 2; }
    #s07-phone { left: 752px; top: 1000px; width: 70px; height: 42px; border-radius: 9px; background: #2a2a2a; }
    #s07-halo { left: 587px; top: 821px; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.08) 40%, rgba(255,255,255,0) 70%); }
    #s07-dim { left: 0; top: 0; width: 1080px; height: 1920px; background: #000; z-index: 5; }
    #s07-fig, #s07-phone, #s07-card, #s07-cnt { z-index: 6; }
    #s07-halo { z-index: 5; }
    #s07-card { left: 630px; top: 650px; width: 430px; height: 160px; border: 3px solid #fff; border-radius: 22px; background: #0b0b0b; box-shadow: 0 0 40px rgba(255,255,255,0.35); padding: 22px 26px; }
    #s07-card .row { display: flex; align-items: center; gap: 18px; }
    #s07-card .av { width: 54px; height: 54px; border-radius: 50%; background: #bbb; filter: blur(5px); flex: none; }
    #s07-card .who { font-weight: 800; font-size: 28px; letter-spacing: 0.08em; text-transform: uppercase; }
    #s07-card .bl { margin-top: 18px; height: 16px; border-radius: 8px; background: #cfcfcf; filter: blur(6px); }
    #s07-cnt .n { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: #fff; border-radius: 50%; }
    #s07-cnt { left: 1000px; top: 630px; width: 56px; height: 56px; border-radius: 50%; background: #fff; color: #000; font-weight: 900; font-size: 32px; display: flex; align-items: center; justify-content: center; }
    #s07-q { left: 80px; top: 700px; width: 410px; height: 110px; border: 3px solid #fff; border-radius: 26px; background: #070707; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 48px; }
    #s07-a { left: 590px; top: 700px; width: 420px; height: 110px; border: 3px solid #fff; border-radius: 26px; background: #070707; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 48px; box-shadow: 0 0 30px rgba(255,255,255,0.3); }
""", "\n    ".join([
    clip("s07-ground", d, "ground", ""),
    clip("s07-halo", d, "", ""),
    clip("s07-phone", d, "", ""),
    FIG.format(id="s07-figB", cls="", d=d, x=170, y=845, c="#9a9a9a"),
    FIG.format(id="s07-fig", cls="glow", d=d, x=480, y=845, c="#fff"),
    clip("s07-book", d, "", ""),
    clip("s07-ghost", d, "", ""),
    clip("s07-k", d, "small ctr", "", "Tag"),
    clip("s07-day", d, "big ctr glow", "", "1"),
    clip("s07-track", d, "", ""),
    clip("s07-fill", d, "", ""),
    clip("s07-of", d, "small ctr", "", "von 100"),
    clip("s07-bh", d, "box", "", '<div class="lab">Stunden</div><div class="val" id="s07-vh">3</div>'),
    clip("s07-bw", d, "box", "", '<div class="lab">Wörter</div><div class="val" id="s07-vw">30</div>'),
    clip("s07-p1", d, "ctr", "", '<span class="pill">Griffe zum Handy: <b id="s07-g">0</b></span>'),
    clip("s07-p2", d, "ctr", "", '<span class="pill">Es wird ruhiger</span>'),
    clip("s07-q", d, "", "", "¿Qué tal?"),
    clip("s07-a", d, "", "", "¡Muy bien!"),
    clip("s07-p3", d, "ctr", "", '<span class="pill">Halbzeit</span>'),
    clip("s07-dim", d, "", ""),
    clip("s07-card", d, "", "", '<div class="row"><div class="av"></div><div class="who">Neue Nachricht</div></div><div class="bl" style="width:330px"></div>'),
    clip("s07-cnt", d, "", "", '<span class="n">1</span><span class="n" id="s07-n2">2</span><span class="n" id="s07-n3">3</span>'),
]), """
    const set = (sel, v) => { $(sel).textContent = de(v); };
    // All counters are a pure function of scene time, so any seek shows the right numbers.
    const K = {
      "#s07-day": [[0, 1], [7.25, 1], [7.7, 10], [14.25, 10], [14.75, 30], [21.25, 30], [21.7, 50]],
      "#s07-vh": [[0, 3], [8.5, 3], [9.0, 30], [15.7, 30], [16.2, 90], [22.7, 90], [23.2, 150]],
      "#s07-vw": [[0, 30], [9.95, 30], [10.55, 300], [15.9, 300], [16.5, 900], [22.9, 900], [23.5, 1500]],
      "#s07-g": [[0, 0], [2.95, 0], [5.35, 20]],
    };
    const at = (pts, t) => { if (t <= pts[0][0]) return pts[0][1]; for (let i = 1; i < pts.length; i++) { const [t1, v1] = pts[i], [t0, v0] = pts[i - 1]; if (t <= t1) return v0 + (v1 - v0) * (t - t0) / (t1 - t0); } return pts[pts.length - 1][1]; };
    const clock = { t: 0 };
    tl.fromTo(clock, { t: 0 }, { t: 40, duration: 40, ease: "none", onUpdate: () => { for (const k in K) set(k, at(K[k], clock.t)); } }, 0);
    const fillTo = (p, t, dur) => tl.to("#s07-fill", { scaleX: p, duration: dur, ease: "power1.inOut" }, t);
    // initial states
    tl.fromTo("#s07-fill", { scaleX: 0.01, transformOrigin: "0% 50%" }, { scaleX: 0.01, duration: 0.01 }, 0);
    tl.fromTo(["#s07-halo", "#s07-dim", "#s07-card", "#s07-cnt", "#s07-ghost", "#s07-figB", "#s07-q", "#s07-a", "#s07-p1", "#s07-p2", "#s07-p3"], { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
    tl.fromTo(["#s07-k", "#s07-day", "#s07-track", "#s07-fill", "#s07-of", "#s07-bh", "#s07-bw", "#s07-book"], { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.35, stagger: 0.04, ease: "power2.out" }, 0.1);

    // Day 1 — tough; reaches for a phone that is not there
    tl.fromTo("#s07-p1", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.3 }, 2.9);
    [3.0, 3.6, 4.1, 4.55, 5.0].forEach((t) => {
      tl.to("#s07-ghost", { opacity: 1, duration: 0.08 }, t);
      tl.to("#s07-ghost", { opacity: 0, duration: 0.25 }, t + 0.2);
    });
    tl.to("#s07-p1", { opacity: 0, duration: 0.3 }, 6.6);

    // Day 10
    fillTo(0.1, 7.25, 0.45);
    tl.fromTo("#s07-p2", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35 }, 12.1);
    tl.to("#s07-p2", { opacity: 0, duration: 0.3 }, 13.7);

    // Day 30 — first whole conversation
    fillTo(0.3, 14.25, 0.5);
    tl.to("#s07-book", { opacity: 0, duration: 0.3 }, 16.9);
    tl.to("#s07-figB", { opacity: 1, duration: 0.4 }, 16.9);
    tl.fromTo("#s07-q", { scale: 0.5, transformOrigin: "20% 100%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 17.3);
    tl.fromTo("#s07-a", { scale: 0.5, transformOrigin: "60% 100%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 19.5);
    tl.to(["#s07-q", "#s07-a", "#s07-figB"], { opacity: 0, duration: 0.35 }, 20.7);

    // Day 50 — halfway
    fillTo(0.5, 21.25, 0.45);
    tl.fromTo("#s07-p3", { y: 10 }, { opacity: 1, y: 0, duration: 0.35 }, 24.5);

    // "...und genau da passiert etwas" — the world goes quiet
    tl.to("#s07-dim", { opacity: 0.72, duration: 1.6, ease: "power1.inOut" }, 25.7);
    tl.to("#s07-p3", { opacity: 0, duration: 0.6 }, 25.7);

    // Cliffhanger: the phone on the floor lights up
    tl.to("#s07-phone", { backgroundColor: "#ffffff", boxShadow: "0 0 50px 14px rgba(255,255,255,0.75)", duration: 0.15 }, 30.0);
    tl.to("#s07-halo", { opacity: 1, duration: 0.3 }, 30.0);
    [30.0, 32.5, 34.0].forEach((t) => {
      tl.fromTo("#s07-phone", { x: 0 }, { x: 6, duration: 0.05, yoyo: true, repeat: 7, ease: "none" }, t);
    });
    tl.fromTo("#s07-card", { y: 30, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 31.0);
    tl.fromTo("#s07-cnt", { scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }, 31.1);
    tl.fromTo("#s07-n2", { opacity: 0 }, { opacity: 1, duration: 0.05 }, 32.5);
    tl.fromTo("#s07-n3", { opacity: 0 }, { opacity: 1, duration: 0.05 }, 34.0);
    tl.fromTo("#s07-cnt", { scale: 1.4 }, { scale: 1, duration: 0.3, ease: "back.out(3)" }, 32.5);
    tl.fromTo("#s07-cnt", { scale: 1.4 }, { scale: 1, duration: 0.3, ease: "back.out(3)" }, 34.0);
    // He turns toward it... and leans in
    tl.to("#s07-fig", { x: 50, rotation: 7, transformOrigin: "50% 100%", duration: 2.2, ease: "power1.inOut" }, 35.2);
    tl.to("#s07-halo", { scale: 1.25, duration: 4, ease: "sine.inOut" }, 35.0);
""")

# ---------- s08 black end 85.5–90 ----------
d = 4.5
scenes["s08"] = scene("s08", d, """
    #root { background: #000; }
    #s08-t { top: 900px; }
""", clip("s08-t", d, "small ctr", "", "Tag 50 / 100"), """
    tl.fromTo("#s08-t", { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "power1.out" }, 1.4);
""")

# ---------- captions ----------
STARTS = {"l01": 0.3, "l02": 8.2, "l03": 16.2, "l04": 22.2, "l05": 27.7, "l06": 37.7, "l07": 45.7, "l08": 52.7, "l09": 59.7, "l10": 66.7}
FIX = {"30": "30", "eins:": "eins.", "fünfzig,": "50,", "hundertfünfzig": "150", "Fünfundvierzig": "45"}
words = {}
for line in open("words.txt", encoding="utf-8"):
    k, *ws = line.split()
    words[k] = [(w.rsplit("@", 1)[0], float(w.rsplit("@", 1)[1])) for w in ws]
dur = {k: float(v) for k, v in json.load(open("vo-durations.json")).items()}
groups = []
for k, st in STARTS.items():
    cur = []
    for w, t in words[k]:
        w = FIX.get(w, w)
        cur.append((w, st + t))
        if len(cur) >= 3 or w[-1] in ".,?:!":
            groups.append(cur); cur = []
    if cur:
        groups.append(cur)
    groups[-1].append(("", st + dur[k]))  # end marker for the line
cap_html, cap_js = [], []
flat = []
for g in groups:
    end_marker = g[-1][0] == ""
    ws = [x for x in g if x[0]]
    flat.append([ws, g[-1][1] if end_marker else None])
for i, (ws, endt) in enumerate(flat):
    s = round(ws[0][1] - 0.05, 2)
    e = endt if endt is not None else flat[i + 1][0][0][1] - 0.05
    e = round(min(e, 85.4), 2)
    txt = " ".join(w for w, _ in ws).replace("%", " %")
    cap_html.append(f'<div id="cap-{i}" class="abs cap clip" data-start="{s}" data-duration="{round(e - s, 2)}"><span>{txt}</span></div>')
scenes["cap"] = scene("cap", 90, """
    #root { background: transparent; }
    #root .cap { left: 90px; width: 900px; top: 1175px; text-align: center; font-weight: 800; font-size: 56px; line-height: 1.15; color: #fff; text-shadow: 0 0 18px rgba(0,0,0,0.9), 0 2px 4px #000; }
""", "\n    ".join(cap_html), """
""")

scenes["s07"] = scenes["s07"].replace('id="s07-cnt" class="abs  clip"', 'id="s07-cnt" data-layout-allow-overlap class="abs  clip"')
os.makedirs("compositions", exist_ok=True)
for sid, html in scenes.items():
    open(f"compositions/{sid}.html", "w", encoding="utf-8").write(html)
print("wrote", ", ".join(scenes), "and", len(cap_html), "caption groups")
