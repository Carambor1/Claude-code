#!/usr/bin/env python3
"""Generates the scene HTML for "Deine 3 Stunden – Teil 2" (1080x1920, YouTube Shorts).
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

STARTS = {"m01": 0.4, "m02": 8.3, "m03": 15.3, "m04": 22.3, "m05": 30.5, "m06": 37.6, "m07": 47.8, "m08": 55.3,
          "m08b": 61.0, "m09": 66.0, "m10": 76.8, "m11": 84.0}
SCENES = [("s01", 0, 8), ("s02", 8, 7), ("s03", 15, 7), ("s04", 22, 15), ("s05", 37, 10), ("s06", 47, 11.5),
          ("s07", 58.5, 17.5), ("s08", 76, 14)]

PHONE_HAND = "left: 572px; top: 918px; width: 42px; height: 70px; border-radius: 9px; background: #fff; box-shadow: 0 0 40px 8px rgba(255,255,255,0.55);"
PHONE_FLOOR = "left: 752px; top: 1000px; width: 70px; height: 42px; border-radius: 9px;"
BEAM = "left: 470px; top: 820px; width: 160px; height: 120px; background: radial-gradient(ellipse at 70% 90%, rgba(255,255,255,0.35), rgba(255,255,255,0) 70%);"

# ---------- s01 hook 0–8: picks up exactly where part 1 ended ----------
d = 8
scenes["s01"] = scene("s01", d, f"""
    #s01-k {{ top: 205px; }}
    #s01-day {{ top: 245px; font-size: 150px; }}
    #s01-pill {{ top: 430px; }}
    #s01-phone {{ {PHONE_FLOOR} background: #fff; box-shadow: 0 0 50px 14px rgba(255,255,255,0.75); }}
    #s01-halo {{ left: 587px; top: 821px; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.08) 40%, rgba(255,255,255,0) 70%); }}
    #s01-card {{ left: 630px; top: 650px; width: 430px; height: 160px; border: 3px solid #fff; border-radius: 22px; background: #0b0b0b; box-shadow: 0 0 40px rgba(255,255,255,0.35); padding: 22px 26px; }}
    #s01-card .row {{ display: flex; align-items: center; gap: 18px; }}
    #s01-card .av {{ width: 54px; height: 54px; border-radius: 50%; background: #bbb; filter: blur(5px); flex: none; }}
    #s01-card .who {{ font-weight: 800; font-size: 28px; letter-spacing: 0.08em; text-transform: uppercase; }}
    #s01-card .bl {{ margin-top: 18px; height: 16px; border-radius: 8px; background: #cfcfcf; filter: blur(6px); }}
    #s01-cnt {{ left: 1000px; top: 630px; width: 56px; height: 56px; border-radius: 50%; background: #fff; color: #000; font-weight: 900; font-size: 32px; display: flex; align-items: center; justify-content: center; }}
""", "\n    ".join([
    clip("s01-ground", d, "ground", ""),
    clip("s01-halo", d, "", ""),
    clip("s01-phone", d, "", ""),
    FIG.format(id="s01-fig", cls="glow", d=d, x=480, y=845, c="#fff"),
    clip("s01-k", d, "small ctr", "", "Tag"),
    clip("s01-day", d, "big ctr glow", "", "50"),
    clip("s01-pill", d, "ctr", "", '<span class="pill">50 Tage ohne Handy</span>'),
    clip("s01-card", d, "", "", '<div class="row"><div class="av"></div><div class="who">3 neue Nachrichten</div></div><div class="bl" style="width:330px"></div>'),
    clip("s01-cnt", d, "", "", "3"),
]), """
    tl.fromTo("#s01-fig", { x: 50, rotation: 7, transformOrigin: "50% 100%" }, { x: 50, rotation: 7, duration: 0.01 }, 0);
    tl.fromTo("#s01-phone", { x: 0 }, { x: 6, duration: 0.05, yoyo: true, repeat: 7, ease: "none" }, 1.9);
    tl.fromTo("#s01-cnt", { scale: 1.4 }, { scale: 1, duration: 0.3, ease: "back.out(3)" }, 1.9);
    tl.fromTo("#s01-pill", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 4.9);
    tl.to("#s01-fig", { x: 140, rotation: 14, duration: 1.6, ease: "power1.inOut" }, 5.6);
    tl.to("#s01-halo", { scale: 1.3, duration: 2, ease: "sine.inOut" }, 5.6);
    tl.to(""" + ids("#s01-k", "#s01-day", "#s01-pill", "#s01-card", "#s01-cnt") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 7.6);
""")

# ---------- s02 grabs it 8–15 ----------
d = 7
scenes["s02"] = scene("s02", d, f"""
    #s02-k {{ top: 250px; }}
    #s02-clock {{ top: 295px; font-size: 180px; }}
    #s02-think {{ top: 560px; }}
    #s02-think .pill {{ font-style: italic; }}
    #s02-phone {{ {PHONE_HAND} }}
    #s02-beam {{ {BEAM} }}
""", "\n    ".join([
    clip("s02-ground", d, "ground", ""),
    clip("s02-beam", d, "", ""),
    FIG.format(id="s02-fig", cls="glow", d=d, x=480, y=845, c="#fff"),
    clip("s02-phone", d, "", ""),
    clip("s02-k", d, "small ctr", "", "Bildschirmzeit heute"),
    clip("s02-clock", d, "big ctr glow", "", "0:00"),
    clip("s02-think", d, "ctr", "", '<span class="pill">„Nur kurz …“</span>'),
]), """
    // The phone comes up from the floor into his hand
    tl.fromTo("#s02-phone", { x: 180, y: 95, rotation: 90, opacity: 1 }, { x: 0, y: 0, rotation: 0, duration: 0.45, ease: "power3.out" }, 0.25);
    tl.fromTo("#s02-beam", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.5);
    tl.fromTo(["#s02-k", "#s02-clock"], { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.35, stagger: 0.08 }, 1.0);
    tl.fromTo("#s02-think", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 1.75);
    tl.to("#s02-think", { opacity: 0, duration: 0.3 }, 3.6);
    const c = { m: 0 };
    tl.fromTo(c, { m: 0 }, { m: 5, duration: 0.5, ease: "none", onUpdate: () => { $("#s02-clock").textContent = "0:" + String(Math.round(c.m)).padStart(2, "0"); } }, 3.6);
    const c2 = { m: 5 };
    tl.fromTo(c2, { m: 5 }, { m: 72, duration: 1.4, ease: "power2.in", onUpdate: () => { const m = Math.round(c2.m); $("#s02-clock").textContent = Math.floor(m / 60) + ":" + String(m % 60).padStart(2, "0"); } }, 4.4);
    tl.fromTo("#s02-clock", { scale: 1 }, { scale: 1.08, duration: 0.25, yoyo: true, repeat: 1 }, 5.8);
    tl.to(""" + ids("#s02-k", "#s02-clock", "#s02-fig", "#s02-phone", "#s02-beam", "#s02-ground") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 6.65);
""")

# ---------- s03 relapse bars 15–22 ----------
d = 7
days = list(range(46, 58))
hours = {51: 1, 52: 2}
bars, labs = [], []
for i, dd in enumerate(days):
    h = 0 if dd <= 50 else hours.get(dd, 3)
    x = 165 + i * 63
    bh = max(6, h * 140)
    bars.append(f'<rect class="bar" data-t="{i}" x="{x}" y="{1000 - bh}" width="50" height="{bh}" rx="6"/>')
    labs.append(f'<text class="dl" x="{x + 25}" y="1045" text-anchor="middle">{dd}</text>')
scenes["s03"] = scene("s03", d, """
    #s03-k { top: 250px; }
    #s03-pill { top: 330px; }
    #s03-chart { left: 0; top: 0; width: 1080px; height: 1920px; }
    #s03-chart .bar { fill: #fff; }
    #s03-chart .dl { fill: #8a8a8a; font: 700 28px Inter, sans-serif; }
    #s03-chart .ref { stroke: rgba(255,255,255,0.5); stroke-width: 2; stroke-dasharray: 10 8; }
    #s03-chart .reft { fill: #9a9a9a; font: 700 28px Inter, sans-serif; letter-spacing: 0.15em; }
""", "\n    ".join([
    clip("s03-k", d, "small ctr", "", "Bildschirmzeit pro Tag"),
    clip("s03-pill", d, "ctr", "", '<span class="pill">Wie vorher</span>'),
    f'<svg id="s03-chart" class="abs clip" data-start="0" data-duration="{d}" viewBox="0 0 1080 1920"><line class="ref" x1="150" y1="580" x2="930" y2="580"/><text class="reft" x="930" y="560" text-anchor="end">3 H</text><line x1="150" y1="1002" x2="930" y2="1002" stroke="#666" stroke-width="2"/>' + "".join(bars) + "".join(labs) + "</svg>",
]), """
    tl.fromTo("#s03-k", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.1);
    tl.fromTo("#s03-chart", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.1);
    // days 46–50 sit at zero; 51 → 1 h, 52 → 2 h ("zwei Stunden"), 53 → 3 h ("drei"), then every day 3 h
    const T = [0.3, 0.38, 0.46, 0.54, 0.62, 0.9, 1.35, 2.75, 3.9, 4.15, 4.4, 4.65];
    document.querySelectorAll("#s03-chart .bar").forEach((b, i) => {
      tl.fromTo(b, { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.3, ease: "power2.out" }, T[i]);
    });
    tl.fromTo("#s03-pill", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 4.15);
    tl.to(""" + ids("#s03-k", "#s03-pill", "#s03-chart") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 6.65);
""")

# ---------- s04 the hidden price 22–37 ----------
d = 15
scenes["s04"] = scene("s04", d, """
    #s04-phone { left: 440px; top: 330px; width: 200px; height: 340px; border: 5px solid #fff; border-radius: 36px; box-shadow: 0 0 40px rgba(255,255,255,0.3); }
    #s04-string { left: 0; top: 0; width: 1080px; height: 1920px; }
    #s04-tag { left: 640px; top: 600px; width: 230px; height: 110px; }
    #s04-tagq { left: 690px; top: 618px; width: 170px; text-align: center; font-weight: 900; font-size: 64px; }
    #s04-hid { top: 790px; }
    #root .cost { left: 160px; width: 760px; height: 170px; border: 3px solid #fff; border-radius: 22px; background: #070707; display: flex; align-items: center; justify-content: space-between; padding: 0 44px; }
    #root .cost .v { font-weight: 900; font-size: 84px; }
    #root .cost .l { font-weight: 700; font-size: 28px; letter-spacing: 0.18em; text-transform: uppercase; color: #9a9a9a; text-align: right; line-height: 1.35; }
    #s04-c1 { top: 420px; } #s04-c2 { top: 620px; }
    #s04-k { top: 300px; }
    #s04-never { top: 850px; }
""", "\n    ".join([
    clip("s04-phone", d, "", ""),
    f'<svg id="s04-string" class="abs clip" data-start="0" data-duration="{d}" viewBox="0 0 1080 1920"><path id="s04-str" d="M640 380 C 700 420, 690 560, 660 600" fill="none" stroke="#fff" stroke-width="3"/></svg>',
    f'<svg id="s04-tag" class="abs clip" data-start="0" data-duration="{d}" viewBox="0 0 230 110"><path d="M40 4 H222 a4 4 0 0 1 4 4 V102 a4 4 0 0 1 -4 4 H40 L4 55 Z" fill="#0a0a0a" stroke="#fff" stroke-width="4"/><circle cx="38" cy="55" r="8" fill="none" stroke="#fff" stroke-width="4"/></svg>',
    clip("s04-tagq", d, "", "", "?"),
    clip("s04-hid", d, "ctr", "", '<span class="pill">Unsichtbar</span>'),
    clip("s04-k", d, "small ctr", "", "Der Preis pro Woche"),
    clip("s04-c1", d, "cost", "", '<span class="v">−21 h</span><span class="l">Stunden<br>pro Woche</span>'),
    clip("s04-c2", d, "cost", "", '<span class="v">−210</span><span class="l">Wörter<br>pro Woche</span>'),
    clip("s04-never", d, "ctr", "", '<span class="pill">Nie gelernt</span>'),
]), """
    tl.fromTo("#s04-phone", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, 0.2);
    tl.fromTo(["#s04-string", "#s04-tag", "#s04-tagq"], { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
    tl.fromTo(["#s04-k", "#s04-c1", "#s04-c2", "#s04-never", "#s04-hid"], { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
    // "hat einen Preis" — a price tag swings onto the phone
    tl.to(["#s04-string", "#s04-tag", "#s04-tagq"], { opacity: 1, duration: 0.3 }, 4.5);
    tl.fromTo(["#s04-tag", "#s04-tagq"], { rotation: -14, transformOrigin: "10% 50%" }, { rotation: 0, duration: 0.9, ease: "elastic.out(1, 0.4)" }, 4.5);
    // "man sieht ihn nur nicht" — the tag fades to a ghost
    tl.to(["#s04-tag", "#s04-tagq", "#s04-string"], { opacity: 0.18, duration: 0.6 }, 5.5);
    tl.to("#s04-hid", { opacity: 1, duration: 0.35 }, 5.6);
    tl.to(["#s04-phone", "#s04-tag", "#s04-tagq", "#s04-string", "#s04-hid"], { opacity: 0, duration: 0.35 }, 7.6);
    // The weekly cost, made visible
    tl.to("#s04-k", { opacity: 1, duration: 0.3 }, 8.2);
    tl.fromTo("#s04-c1", { x: -60 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, 8.25);
    tl.fromTo("#s04-c2", { x: -60 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, 10.9);
    tl.fromTo("#s04-never", { y: 10 }, { opacity: 1, y: 0, duration: 0.35 }, 12.6);
    tl.to(""" + ids("#s04-k", "#s04-c1", "#s04-c2", "#s04-never") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 14.65);
""")


# ---------- the words chart (used by s05 and s07) ----------
def X(dd): return 160 + 7.6 * dd
def Y(w): return 1020 - 0.2 * w


def chart_svg(pid):
    grid = "".join(f'<line x1="160" y1="{Y(w)}" x2="920" y2="{Y(w)}" stroke="#222" stroke-width="2"/><text class="yt" x="145" y="{Y(w) + 10}" text-anchor="end">{w // 1000}k</text>' for w in (1000, 2000, 3000))
    xt = "".join(f'<text class="xt" x="{X(dd)}" y="1065" text-anchor="middle">{dd}</text>' for dd in (0, 50, 70, 100))
    return (f'<svg id="{pid}-chart" class="abs clip" data-start="0" data-duration="DUR" viewBox="0 0 1080 1920">'
            f'<defs><clipPath id="{pid}-clip"><rect id="{pid}-cr" x="150" y="0" width="0" height="1920"/></clipPath></defs>'
            f'{grid}<line x1="160" y1="1020" x2="930" y2="1020" stroke="#777" stroke-width="2"/><line x1="160" y1="400" x2="160" y2="1020" stroke="#777" stroke-width="2"/>{xt}'
            f'<path id="{pid}-plan" d="M{X(0)} {Y(0)} L{X(100)} {Y(3000)}" stroke="rgba(255,255,255,0.35)" stroke-width="3" stroke-dasharray="10 9" fill="none"/>'
            f'<g clip-path="url(#{pid}-clip)"><path d="M{X(0)} {Y(0)} L{X(50)} {Y(1500)} L{X(70)} {Y(1500)} L{X(100)} {Y(2400)}" stroke="#fff" stroke-width="12" opacity="0.3" fill="none" style="filter: blur(6px)"/>'
            f'<path d="M{X(0)} {Y(0)} L{X(50)} {Y(1500)} L{X(70)} {Y(1500)} L{X(100)} {Y(2400)}" stroke="#fff" stroke-width="5" fill="none" stroke-linejoin="round"/></g>'
            f'<circle id="{pid}-dot" cx="{X(0)}" cy="{Y(0)}" r="11" fill="#fff" style="filter: drop-shadow(0 0 10px #fff)"/></svg>')


CHART_CSS = """
    #root .chart { left: 0; top: 0; width: 1080px; height: 1920px; }
    #root .yt, #root .xt { fill: #8a8a8a; font: 700 28px Inter, sans-serif; }
    #root .hk { top: 205px; }
    #root .hday { top: 245px; font-size: 120px; }
"""
CHART_JS = """
    const X = (d) => 160 + 7.6 * d, Y = (w) => 1020 - 0.2 * w;
    const words = (d) => d <= 50 ? d * 30 : d <= 70 ? 1500 : 1500 + (d - 70) * 30;
    const at = (pts, t) => { if (t <= pts[0][0]) return pts[0][1]; for (let i = 1; i < pts.length; i++) { const [t1, v1] = pts[i], [t0, v0] = pts[i - 1]; if (t <= t1) { const u = (t - t0) / (t1 - t0); return v0 + (v1 - v0) * (u * u * (3 - 2 * u)); } } return pts[pts.length - 1][1]; };
    // The drawn day is a pure function of scene time: pts = [[time, day], ...]
    const drawPts = (pid, pts, dur) => {
      const o = { t: 0 };
      tl.fromTo(o, { t: 0 }, { t: dur, duration: dur, ease: "none", onUpdate: () => {
        const d = at(pts, o.t);
        $("#" + pid + "-cr").setAttribute("width", (X(d) - 150 + 3).toFixed(1));
        $("#" + pid + "-dot").setAttribute("cx", X(d).toFixed(1));
        $("#" + pid + "-dot").setAttribute("cy", Y(words(d)).toFixed(1));
        $("#" + pid + "-day").textContent = Math.round(d);
      } }, 0);
    };
"""

# ---------- s05 the flat line 37–47 ----------
d = 10
scenes["s05"] = scene("s05", d, CHART_CSS + f"""
    #s05-gap {{ left: 0; top: 0; width: 1080px; height: 1920px; }}
    #s05-l1 {{ left: 200px; top: 440px; }}
    #s05-v1 {{ left: 200px; top: 478px; font-size: 84px; }}
    #s05-flat {{ left: 560px; top: 760px; }}
""", "\n    ".join([
    clip("s05-k", d, "small ctr hk", "", "Tag"),
    clip("s05-day", d, "big ctr glow hday", "", "0"),
    chart_svg("s05").replace("DUR", str(d)).replace('class="abs clip"', 'class="abs chart clip"'),
    f'<svg id="s05-gap" class="abs clip" data-start="0" data-duration="{d}" viewBox="0 0 1080 1920"><line x1="{X(70)}" y1="{Y(2100)}" x2="{X(70)}" y2="{Y(1500)}" stroke="#fff" stroke-width="4" stroke-dasharray="6 6"/><circle cx="{X(70)}" cy="{Y(2100)}" r="8" fill="none" stroke="#fff" stroke-width="3"/></svg>',
    clip("s05-l1", d, "small", "", "Fehlen"),
    clip("s05-v1", d, "big glow", "", "−600"),
    clip("s05-flat", d, "", "", '<span class="pill">Flach</span>'),
]), CHART_JS + """
    tl.fromTo(["#s05-chart", "#s05-k", "#s05-day"], { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0);
    tl.fromTo(["#s05-gap", "#s05-l1", "#s05-v1", "#s05-flat"], { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
    drawPts("s05", [[0.2, 0], [0.9, 50], [0.95, 50], [2.55, 70]], 10);   // 50 → 70 under "nach zwanzig Tagen …"
    tl.to("#s05-gap", { opacity: 1, duration: 0.3 }, 3.9); // "sechshundert Wörter"
    tl.fromTo(["#s05-l1", "#s05-v1"], { x: -20 }, { opacity: 1, x: 0, duration: 0.35, stagger: 0.06, ease: "back.out(1.8)" }, 3.95);
    tl.fromTo("#s05-flat", { y: 10 }, { opacity: 1, y: 0, duration: 0.35 }, 8.4);
    tl.to(""" + ids("#s05-chart", "#s05-k", "#s05-day", "#s05-gap", "#s05-l1", "#s05-v1", "#s05-flat") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 9.65);
""")

# ---------- s06 day 70: puts it down 47–58.5 ----------
d = 11.5
week = "".join(f'<div class="dd" id="s06-d{i}"><span>{71 + i}</span></div>' for i in range(5))
scenes["s06"] = scene("s06", d, f"""
    #s06-k {{ top: 205px; }}
    #s06-day {{ top: 245px; font-size: 150px; }}
    #s06-num {{ top: 470px; font-size: 110px; }}
    #s06-nl {{ top: 600px; }}
    #s06-phone {{ {PHONE_HAND} }}
    #s06-beam {{ {BEAM} }}
    #s06-today {{ top: 700px; }}
    #s06-week {{ left: 160px; top: 470px; width: 760px; display: flex; justify-content: space-between; }}
    #s06-week .dd {{ width: 130px; height: 130px; border: 3px solid #555; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 44px; color: #777; }}
""", "\n    ".join([
    clip("s06-ground", d, "ground", ""),
    clip("s06-beam", d, "", ""),
    FIG.format(id="s06-fig", cls="glow", d=d, x=480, y=845, c="#fff"),
    clip("s06-phone", d, "", ""),
    clip("s06-k", d, "small ctr", "", "Tag"),
    clip("s06-day", d, "big ctr glow", "", "70"),
    clip("s06-num", d, "big ctr", "", "−600"),
    clip("s06-nl", d, "small ctr", "", "Wörter verloren"),
    clip("s06-today", d, "ctr", "", '<span class="pill">Nur für heute</span>'),
    clip("s06-week", d, "", "", week),
]), """
    tl.fromTo(["#s06-ground", "#s06-fig", "#s06-phone", "#s06-beam", "#s06-k", "#s06-day"], { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0);
    tl.fromTo(["#s06-num", "#s06-nl", "#s06-today", "#s06-week"], { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
    // "Er sieht die Zahl"
    tl.fromTo("#s06-num", { scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 2.35);
    tl.to("#s06-nl", { opacity: 1, duration: 0.3 }, 2.5);
    // "… und legt das Handy weg"
    tl.to("#s06-phone", { x: 200, y: 98, rotation: 90, duration: 0.55, ease: "power2.in" }, 3.8);
    tl.to("#s06-phone", { boxShadow: "0 0 0px 0px rgba(255,255,255,0)", backgroundColor: "#2a2a2a", duration: 0.4 }, 4.35);
    tl.to("#s06-beam", { opacity: 0, duration: 0.4 }, 3.9);
    tl.to(["#s06-num", "#s06-nl"], { opacity: 0, duration: 0.3 }, 4.9);
    tl.fromTo("#s06-today", { y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 6.25);
    // "Und morgen wieder" — one day at a time
    tl.to("#s06-week", { opacity: 1, duration: 0.3 }, 8.2);
    [8.35, 8.95, 9.75, 10.15, 10.55].forEach((t, i) => {
      tl.fromTo("#s06-d" + i, { borderColor: "#555", color: "#777", backgroundColor: "#000" }, { borderColor: "#fff", color: "#000", backgroundColor: "#fff", duration: 0.2 }, t);
    });
    tl.to(""" + ids("#s06-k", "#s06-day", "#s06-today", "#s06-week") + """, { opacity: 0, duration: 0.3, ease: "power2.in" }, 11.15);
""")

# ---------- s07 comeback to day 100 58.5–76 ----------
d = 17.5
scenes["s07"] = scene("s07", d, CHART_CSS + f"""
    #s07-area {{ left: 0; top: 0; width: 1080px; height: 1920px; }}
    #s07-a1 {{ left: 200px; top: 480px; }}
    #s07-v1 {{ left: 200px; top: 518px; font-size: 84px; }}
    #s07-pl {{ left: 200px; top: 425px; color: #8a8a8a; }}
    #s07-plus {{ top: 1090px; }}
""", "\n    ".join([
    f'<svg id="s07-area" class="abs clip" data-start="0" data-duration="{d}" viewBox="0 0 1080 1920"><path d="M{X(0)} {Y(0)} L{X(50)} {Y(1500)} L{X(70)} {Y(1500)} L{X(100)} {Y(2400)} L{X(100)} {Y(0)} Z" fill="rgba(255,255,255,0.12)"/></svg>',
    clip("s07-k", d, "small ctr hk", "", "Tag"),
    clip("s07-day", d, "big ctr glow hday", "", "70"),
    chart_svg("s07").replace("DUR", str(d)).replace('class="abs clip"', 'class="abs chart clip"'),
    clip("s07-pl", d, "small", "", "Geplant: 3.000"),
    clip("s07-a1", d, "small", "", "Geschafft"),
    clip("s07-v1", d, "big glow", "", "2.400"),
    clip("s07-plus", d, "ctr", "", '<span class="pill">+2.400 mehr als vorher</span>'),
]), CHART_JS + """
    tl.fromTo(["#s07-chart", "#s07-k", "#s07-day"], { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0);
    tl.fromTo(["#s07-area", "#s07-pl", "#s07-a1", "#s07-v1", "#s07-plus"], { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
    drawPts("s07", [[0, 0], [0.7, 70], [1.0, 70], [3.0, 80], [4.4, 90], [6.6, 100]], 17.5);   // "Tag 80 … Tag 90 … die Kurve steigt wieder"
    tl.fromTo(["#s07-a1", "#s07-v1"], { x: -20 }, { opacity: 1, x: 0, duration: 0.4, stagger: 0.06, ease: "back.out(1.8)" }, 9.1);  // "2.400 Wörter"
    tl.to("#s07-pl", { opacity: 1, duration: 0.35 }, 11.55);   // "nicht 3.000, wie geplant"
    tl.to("#s07-area", { opacity: 1, duration: 0.6 }, 13.9);  // "aber 2.400 mehr als vorher"
    tl.fromTo("#s07-plus", { y: 10 }, { opacity: 1, y: 0, duration: 0.35 }, 14.1);
    tl.to(""" + ids("#s07-chart", "#s07-k", "#s07-day", "#s07-area", "#s07-pl", "#s07-a1", "#s07-v1", "#s07-plus") + """, { opacity: 0, duration: 0.35, ease: "power2.in" }, 17.1);
""")

# ---------- s08 the lesson 76–90 ----------
d = 14
scenes["s08"] = scene("s08", d, f"""
    #s08-l1 {{ top: 330px; }}
    #s08-t1 {{ top: 380px; font-size: 104px; }}
    #s08-l2 {{ top: 560px; }}
    #s08-t2 {{ top: 610px; font-size: 104px; }}
    #s08-q {{ top: 360px; font-size: 92px; line-height: 1.1; }}
    #s08-done {{ top: 640px; }}
    #s08-phone {{ {PHONE_FLOOR} background: #2a2a2a; }}
""", "\n    ".join([
    clip("s08-ground", d, "ground", ""),
    FIG.format(id="s08-fig", cls="glow", d=d, x=480, y=845, c="#fff"),
    clip("s08-phone", d, "", ""),
    clip("s08-l1", d, "small ctr", "", "Der Rückfall"),
    clip("s08-t1", d, "big ctr", "", "20 Tage"),
    clip("s08-l2", d, "small ctr", "", "Aufgeben"),
    clip("s08-t2", d, "big ctr glow", "", "Alles"),
    clip("s08-q", d, "big ctr glow", "", "Und deine<br>3 Stunden?"),
    clip("s08-done", d, "ctr", "", '<span class="pill">Tag 100 / 100 ✓</span>'),
]), """
    tl.fromTo(["#s08-ground", "#s08-fig", "#s08-phone"], { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0);
    tl.fromTo(["#s08-l1", "#s08-t1", "#s08-l2", "#s08-t2", "#s08-q", "#s08-done"], { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
    tl.to("#s08-l1", { opacity: 1, duration: 0.3 }, 0.9);
    tl.fromTo("#s08-t1", { scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 1.1);
    tl.to("#s08-l2", { opacity: 1, duration: 0.3 }, 3.9);
    tl.fromTo("#s08-t2", { scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, 5.1);
    tl.to(["#s08-l1", "#s08-t1", "#s08-l2", "#s08-t2"], { opacity: 0, duration: 0.35 }, 7.4);
    tl.fromTo("#s08-q", { y: 16 }, { opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }, 8.0);
    tl.fromTo("#s08-done", { y: 10 }, { opacity: 1, y: 0, duration: 0.35 }, 9.4);
    tl.to(""" + ids("#s08-q", "#s08-done", "#s08-ground", "#s08-fig", "#s08-phone") + """, { opacity: 0, duration: 1.0, ease: "power1.in" }, 12.8);
""")

# ---------- captions ----------
FIX = {"fünfzig.": "50.", "fünfzig": "50", "zwanzig": "20", "sechzig": "60", "sechshundert": "600", "2400": "2.400", "3000": "3.000"}
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
    groups[-1].append(("", st + dur[k]))
flat = []
for g in groups:
    end_marker = g[-1][0] == ""
    ws = [x for x in g if x[0]]
    flat.append([ws, g[-1][1] if end_marker else None])
cap_html = []
for i, (ws, endt) in enumerate(flat):
    s = round(ws[0][1] - 0.05, 2)
    e = endt if endt is not None else flat[i + 1][0][0][1] - 0.05
    e = round(min(e, 89.9), 2)
    txt = " ".join(w for w, _ in ws)
    cap_html.append(f'<div id="cap-{i}" class="abs cap clip" data-start="{s}" data-duration="{round(e - s, 2)}"><span>{txt}</span></div>')
scenes["cap"] = scene("cap", 90, """
    #root { background: transparent; }
    #root .cap { left: 90px; width: 900px; top: 1175px; text-align: center; font-weight: 800; font-size: 56px; line-height: 1.15; color: #fff; text-shadow: 0 0 18px rgba(0,0,0,0.9), 0 2px 4px #000; }
""", "\n    ".join(cap_html), "")

# ---------- index.html ----------
host = '      <div id="{0}" data-composition-id="{0}" data-composition-src="compositions/{0}.html" data-start="{1}" data-duration="{2}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>'
H = [host.format(*s) for s in SCENES]
H.append('      <div id="cap" data-composition-id="cap" data-composition-src="compositions/cap.html" data-start="0" data-duration="90" data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:10"></div>')
A = ['      <!-- Voiceover: ElevenLabs "Brian", eleven_v4, German -->']
for k, s in STARTS.items():
    A.append(f'      <audio id="vo-{k}" class="clip" src="assets/vo/{k}.mp3" data-start="{s}" data-duration="{round(dur[k] - 0.01, 2)}" data-track-index="2" data-volume="1"></audio>')
A.append('      <!-- Ambient bed: suspense -> stagnant -> hopeful -> resolve -->')
A.append('      <audio id="bed" class="clip" src="assets/music/bed.mp3" data-start="0" data-duration="90" data-track-index="3" data-volume="0.55"></audio>')
SFX = [("vibrate", [2.3], 0.18), ("whoosh-short", [8.6, 22.0, 46.85], 0.45), ("whoosh", [14.85, 36.85, 58.35, 75.85], 0.45),
       ("pop", [21.0, 26.95, 30.75, 33.4, 41.55, 49.95, 55.65, 56.25, 57.05, 57.45, 57.85, 67.6, 72.6, 77.1, 81.1, 85.4], 0.45),
       ("riser", [62.7], 0.3), ("impact-bass-1", [81.1], 0.5)]
n = 0
for name, ts, vol in SFX:
    for t in ts:
        n += 1
        extra = ' data-duration="2.4" data-fade-out="0.3"' if name == "riser" else ""
        A.append(f'      <audio id="sfx-{n:02d}" class="clip" src="assets/sfx/{name}.mp3" data-start="{t}"{extra} data-track-index="{10 + n}" data-volume="{vol}"></audio>')
index = f'''<!doctype html>
<html lang="de">
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
{chr(10).join(H)}

{chr(10).join(A)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
open("index.html", "w", encoding="utf-8").write(index)
scenes["s01"] = scenes["s01"].replace('id="s01-cnt" class="abs  clip"', 'id="s01-cnt" data-layout-allow-overlap class="abs  clip"')
os.makedirs("compositions", exist_ok=True)
for sid, html in scenes.items():
    open(f"compositions/{sid}.html", "w", encoding="utf-8").write(html)
print("wrote", ", ".join(scenes), "and", len(cap_html), "caption groups")
