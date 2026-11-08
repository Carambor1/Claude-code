#!/usr/bin/env python3
""""This €5 habit is worth €364,000" — ~53 s vertical Short, English, Sarah (dramatic), no music.
Style of the 1%-rule video: black, glowing white figure, dashed ground, pills, counters, one growing curve.
Timeline is derived from the voice (vo.json). Run: python3 build.py"""
import json, re, subprocess

VO = json.load(open("vo.json"))
ORDER = [f"s{i}" for i in range(1, 14)]
GAP = {"s1": 0.15, "s2": 0.35, "s5": 0.25, "s9": 0.45, "s11": 0.25, "s12": 0.45}
T, at = 0.1, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.12)
DUR = round(T + 1.6, 2)

def w(k, word, nth=0):                      # absolute time of a word in a line
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9-]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)

E = {  # events
    "worth": w("s1", "worth"), "euros1": w("s1", "euros"), "nobody": w("s2", "nobody"),
    "coffee": w("s3", "coffee"), "away": w("s3", "away"), "year": w("s4", "year"), "invest": w("s5", "invest"),
    "seven": w("s5", "seven"), "y10": w("s6", "ten"), "y20": w("s7", "twenty"), "y30": w("s8", "thirty"),
    "y40": w("s9", "forty"), "big": w("s9", "three"), "paid": w("s10", "seventy-three"), "other": w("s11", "other"),
    "made": w("s11", "made"), "wait": w("s12", "wait"), "lose": w("s12", "lose"), "coffee2": w("s13", "coffee"),
}

# ---------------------------------------------------------------- the money
def V(y): return 1825 * ((1.07 ** y - 1) / 0.07)          # €5/day, 7 %/year, paid in yearly
def D(y): return 1825 * y
def Lt(y): return 0 if y <= 10 else V(y - 10)
X0, XW, Y0, YH, VMAX = 160, 760, 1050, 600, 400000
def px(y): return X0 + XW * y / 40
def py(v): return Y0 - YH * v / VMAX
def path(f, a=0, b=40, step=0.5):
    pts, y = [], a
    while y <= b + 1e-9:
        pts.append(f"{px(y):.1f} {py(f(y)):.1f}"); y += step
    return "M" + " L".join(pts)
area_paid = path(D) + f" L{px(40)} {Y0} L{px(0)} {Y0} Z"
area_int = path(V) + " L" + " L".join(f"{px(y):.1f} {py(D(y)):.1f}" for y in [40 - i * 0.5 for i in range(81)]) + " Z"

FIG = '<svg viewBox="0 0 80 130"><circle cx="40" cy="24" r="20" fill="#fff"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="#fff"/></svg>'
CUP = '<svg viewBox="0 0 100 100"><path d="M18 32h52v38a14 14 0 0 1 -14 14h-24a14 14 0 0 1 -14 -14z M70 42h8a11 11 0 0 1 0 22h-8" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/><path d="M34 8c-5 7 5 10 0 18M50 8c-5 7 5 10 0 18" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>'
COIN = '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#fff"/><circle cx="50" cy="50" r="34" fill="none" stroke="#000" stroke-width="3"/><text x="50" y="62" text-anchor="middle" font-family="Inter" font-weight="900" font-size="34" fill="#000">€5</text></svg>'

def C(id, cls, style, inner=""):
    return f'<div id="{id}" class="abs {cls} clip" data-start="0" data-duration="{DUR}" style="{style}">{inner}</div>'

chart = (f'<svg id="ch" class="abs clip" data-start="0" data-duration="{DUR}" style="left:0;top:0;width:1080px;height:1920px" viewBox="0 0 1080 1920">'
         f'<defs><clipPath id="chc"><rect id="chr" x="150" y="0" width="0" height="1920"/></clipPath></defs>'
         f'<g id="axes"><line x1="{X0}" y1="{Y0}" x2="{X0 + XW + 10}" y2="{Y0}" stroke="#777" stroke-width="2"/>'
         + "".join(f'<line x1="{px(y)}" y1="{Y0}" x2="{px(y)}" y2="{Y0 + 12}" stroke="#777" stroke-width="2"/><text class="xt" x="{px(y)}" y="{Y0 + 50}" text-anchor="middle">{y}y</text>' for y in (10, 20, 30, 40))
         + f'</g><path id="apaid" d="{area_paid}" fill="#3a3a3a"/><path id="aint" d="{area_int}" fill="#ffffff" opacity="0.9"/>'
         f'<path id="late" d="{path(Lt, 10, 40)}" fill="none" stroke="#9a9a9a" stroke-width="5" stroke-dasharray="14 10"/>'
         f'<g clip-path="url(#chc)"><path d="{path(V)}" fill="none" stroke="#fff" stroke-width="14" opacity="0.3" style="filter:blur(6px)"/><path d="{path(V)}" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/></g>'
         f'<circle id="dot" cx="{px(0)}" cy="{py(0)}" r="13" fill="#fff" style="filter:drop-shadow(0 0 12px #fff)"/>'
         + "".join(f'<g class="ms" id="ms{y}"><circle cx="{px(y)}" cy="{py(V(y))}" r="9" fill="#fff"/><text class="mt" x="{px(y) - 16}" y="{py(V(y)) - 24}" text-anchor="end">€{round(V(y) / 1000)}k</text></g>' for y in (10, 20, 30))
         + f'<line id="gap" x1="{px(40) + 34}" y1="{py(V(40))}" x2="{px(40) + 34}" y2="{py(Lt(40))}" stroke="#fff" stroke-width="5"/>'
         f'</svg>')

body = "\n    ".join([
    C("hk-n", "ctr big glow", "top:360px;font-size:190px", "€5"),
    C("hk-l", "small ctr", "top:580px", "a day"),
    C("hk-p", "ctr", "top:640px", '<span class="pill">Almost nobody does it</span>'),
    C("ground", "", "left:0;top:1100px;width:1080px;height:0;border-top:2px dashed rgba(255,255,255,0.32)"),
    C("fig", "glow", "left:300px;top:905px;width:120px;height:195px", FIG),
    C("cup", "glow", "left:410px;top:950px;width:80px;height:80px", CUP),
    C("coin", "", "left:410px;top:945px;width:92px;height:92px", COIN),
    C("jar", "", "left:640px;top:820px;width:240px;height:280px", '<div class="jarb"></div><div id="jarf" class="jarf"></div>'),
    C("yr", "ctr", "top:330px", '<div class="big glow" style="font-size:150px">€1,825</div><div class="small" style="margin-top:12px">every year</div>'),
    chart,
    C("cnt-l", "small ctr", "top:200px", 'After <span id="yrs">0</span> years'),
    C("cnt", "ctr big glow", "top:240px;font-size:140px", "€0"),
    C("p7", "", "left:180px;top:470px", '<span class="pill">7 % a year</span>'),
    C("lpaid", "", "left:690px;top:968px", '<div class="small" style="color:#cfcfcf;font-size:26px">You paid</div><div class="big" style="font-size:48px">€73,000</div>'),
    C("lint", "", "left:190px;top:470px", '<div class="small" style="color:#000;background:#fff;padding:6px 14px;border-radius:10px;display:inline-block">Your money made</div><div class="big glow" style="font-size:96px;margin-top:8px">€291,000</div>'),
    C("lgap", "", "left:180px;top:480px;width:500px", '<div class="small">Start 10 years later</div><div class="big glow" style="font-size:80px">−€192k</div>'),
    C("end-cup", "glow", "left:440px;top:600px;width:200px;height:200px", CUP),
    C("end-q", "ctr big", "top:840px;font-size:84px", "€5?"),
    C("fl", "", "left:0;top:0;width:1080px;height:1920px;background:#fff"),
    C("dim", "", "left:0;top:0;width:1080px;height:1920px;background:#000"),
])
HIDDEN = ["#hk-p", "#ground", "#fig", "#cup", "#coin", "#jar", "#yr", "#ch", "#cnt-l", "#cnt", "#p7", "#lpaid", "#lint", "#lgap", "#end-cup", "#end-q", "#fl", "#dim"]
CSS = """
    #root { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 55%, #161616 0%, #000 70%); font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }
    #root .abs { position: absolute; }
    #root .ctr { left: 0; width: 1080px; text-align: center; }
    #root .big { font-weight: 900; letter-spacing: -0.03em; line-height: 1; }
    #root .glow { filter: drop-shadow(0 0 16px rgba(255,255,255,0.55)); }
    #root .small { font-weight: 700; font-size: 30px; letter-spacing: 0.2em; text-transform: uppercase; color: #9a9a9a; }
    #root .pill { font-weight: 700; font-size: 32px; letter-spacing: 0.16em; text-transform: uppercase; color: #ddd; background: #141414; border: 2px solid #4a4a4a; border-radius: 999px; padding: 12px 28px; white-space: nowrap; display: inline-block; }
    #root svg { width: 100%; height: 100%; display: block; }
    #root .jarb { position: absolute; inset: 0; border: 6px solid #fff; border-top: none; border-radius: 0 0 46px 46px; box-shadow: 0 0 30px rgba(255,255,255,0.25); }
    #root .jarf { position: absolute; left: 14px; right: 14px; bottom: 14px; height: 230px; background: #fff; border-radius: 0 0 34px 34px; transform-origin: 50% 100%; }
    #root .xt { fill: #8a8a8a; font: 700 30px Inter, sans-serif; }
    #root .mt { fill: #fff; font: 900 40px Inter, sans-serif; }
    #root #ch .ms, #root #apaid, #root #aint, #root #late, #root #gap { opacity: 0; }
""" + "    " + ", ".join(f"#root {h}" for h in HIDDEN) + " { opacity: 0; }\n"

J = []
a = J.append
# hook: €5 races to €364,000
a(f'const o1 = {{ v: 5 }}; tl.fromTo(o1, {{ v: 5 }}, {{ v: 364000, duration: {E["euros1"] - E["worth"] + 0.2:.2f}, ease: "expo.in", onUpdate: () => {{ $("#hk-n").textContent = "€" + Math.round(o1.v).toLocaleString("en-US"); }} }}, {E["worth"]});')
a(f'tl.to("#hk-l", {{ opacity: 0, duration: 0.2 }}, {E["worth"]});')
a(f'tl.fromTo("#hk-n", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.15, yoyo: true, repeat: 1, ease: "power2.out" }}, {E["euros1"] + 0.2});')
a(f'tl.fromTo("#fl", {{ opacity: 0 }}, {{ opacity: 0.25, duration: 0.05 }}, {E["euros1"] + 0.2}); tl.to("#fl", {{ opacity: 0, duration: 0.4 }}, {E["euros1"] + 0.26});')
a(f'tl.to("#hk-n", {{ opacity: 0.35, scale: 0.92, duration: 0.6 }}, {at["s2"]});')
a(f'tl.fromTo("#hk-p", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {E["nobody"]});')
a(f'tl.to(["#hk-n", "#hk-p"], {{ opacity: 0, y: -30, duration: 0.3 }}, {at["s3"] - 0.1});')
# coffee becomes a coin, coin drops into the jar
a(f'tl.fromTo(["#ground", "#fig"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {at["s3"]});')
a(f'tl.fromTo("#cup", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {E["coffee"] - 0.1});')
a(f'tl.fromTo("#jar", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {E["away"] - 0.6});')
a(f'tl.fromTo("#jarf", {{ scaleY: 0 }}, {{ scaleY: 0.02, duration: 0.01 }}, 0);')
a(f'tl.to("#cup", {{ opacity: 0, scale: 0.4, duration: 0.2 }}, {E["away"] - 0.75});')
a(f'tl.fromTo("#coin", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)" }}, {E["away"] - 0.7});')
a(f'tl.to("#coin", {{ keyframes: [{{ x: 120, y: -200, duration: 0.3, ease: "power2.out" }}, {{ x: 300, y: -20, duration: 0.35, ease: "power2.in" }}] }}, {E["away"] + 0.05});')
a(f'tl.to("#coin", {{ opacity: 0, duration: 0.08 }}, {E["away"] + 0.7});')
a(f'tl.to("#jarf", {{ scaleY: 0.06, duration: 0.15 }}, {E["away"] + 0.7});')
# a year of coins
a(f'tl.fromTo("#yr", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }}, {E["year"] - 0.9});')
a(f'tl.to("#jarf", {{ scaleY: 0.85, duration: 1.6, ease: "power1.inOut" }}, {at["s4"]});')
a(f'tl.to("#fig", {{ y: -18, duration: 0.18, yoyo: true, repeat: 1 }}, {E["year"]});')
# the jar becomes the chart
a(f'tl.to(["#yr", "#fig", "#ground", "#jar"], {{ opacity: 0, duration: 0.35 }}, {E["invest"]});')
a(f'tl.to("#jar", {{ scale: 0.2, x: -440, y: 140, duration: 0.45, ease: "power3.in" }}, {E["invest"]});')
a(f'tl.fromTo(["#ch", "#cnt-l", "#cnt"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {E["invest"] + 0.3});')
a(f'tl.fromTo("#p7", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {E["seven"]});')
a(f'tl.to("#p7", {{ opacity: 0, duration: 0.3 }}, {E["y20"] - 0.4});')
# the curve: years as a pure function of time
K = [(0, 0), (E["y10"] - 0.3, 0), (E["y10"] + 0.5, 10), (E["y20"] - 0.2, 10), (E["y20"] + 0.5, 20), (E["y30"] - 0.2, 20), (E["y30"] + 0.5, 30), (E["y40"] - 0.2, 30), (E["big"] + 0.1, 40), (DUR, 40)]
a(f'const K = {json.dumps([[round(t, 2), y] for t, y in K])};')
a('const yAt = (t) => { if (t <= K[0][0]) return 0; for (let i = 1; i < K.length; i++) if (t <= K[i][0]) { const u = (t - K[i-1][0]) / (K[i][0] - K[i-1][0]); return K[i-1][1] + (K[i][1] - K[i-1][1]) * (u * u * (3 - 2 * u)); } return 40; };')
a('const V = (y) => 1825 * ((Math.pow(1.07, y) - 1) / 0.07);')
a(f'const clock = {{ t: 0 }}; tl.fromTo(clock, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: () => {{ const y = yAt(clock.t), x = {X0} + {XW} * y / 40; $("#chr").setAttribute("width", (x - 150 + 4).toFixed(1)); $("#dot").setAttribute("cx", x.toFixed(1)); $("#dot").setAttribute("cy", ({Y0} - {YH} * V(y) / {VMAX}).toFixed(1)); $("#yrs").textContent = Math.round(y); $("#cnt").textContent = "€" + Math.round(V(y)).toLocaleString("en-US"); }} }}, 0);')
for y in (10, 20, 30):
    a(f'tl.fromTo("#ms{y}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {E["y" + str(y)] + 0.5});')
a(f'tl.fromTo("#cnt", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }}, {E["big"] + 0.1});')
a(f'tl.fromTo("#fl", {{ opacity: 0 }}, {{ opacity: 0.3, duration: 0.05, immediateRender: false }}, {E["big"] + 0.1}); tl.to("#fl", {{ opacity: 0, duration: 0.5 }}, {E["big"] + 0.16});')
a(f'tl.fromTo("#ch", {{ scale: 1, transformOrigin: "50% 60%" }}, {{ scale: 1.04, duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {E["big"]});')
# paid vs made
a(f'tl.to("#apaid", {{ opacity: 1, duration: 0.4 }}, {E["paid"] - 0.1});')
a(f'tl.fromTo("#lpaid", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {E["paid"]});')
a(f'tl.to(["#ms10", "#ms20", "#ms30"], {{ opacity: 0, duration: 0.3 }}, {E["paid"]});')
a(f'tl.to("#aint", {{ opacity: 0.9, duration: 0.5 }}, {E["other"]});')
a(f'tl.fromTo("#lint", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, {E["other"] + 0.2});')
# waiting costs
a(f'tl.to(["#aint", "#apaid", "#lint", "#lpaid"], {{ opacity: 0, duration: 0.35 }}, {at["s12"]});')
a(f'tl.to("#late", {{ opacity: 1, duration: 0.6 }}, {E["wait"]});')
a(f'tl.fromTo("#gap", {{ opacity: 0, scaleY: 0, transformOrigin: "50% 0%" }}, {{ opacity: 1, scaleY: 1, duration: 0.4 }}, {E["lose"]});')
a(f'tl.fromTo("#lgap", {{ opacity: 0, x: 20 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "back.out(2)" }}, {E["lose"] + 0.1});')
# end: back to the coffee
a(f'tl.to(["#ch", "#cnt-l", "#cnt", "#lgap"], {{ opacity: 0, duration: 0.4 }}, {at["s13"]});')
a(f'tl.fromTo("#end-cup", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "power2.out" }}, {at["s13"] + 0.3});')
a(f'tl.fromTo("#end-q", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {E["coffee2"]});')
a(f'tl.fromTo("#dim", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.0 }}, {DUR - 1.05});')

open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="1080" data-height="1920">
    {body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const $ = (s) => document.querySelector(s);
{chr(10).join("    " + x for x in J)}
    window.__timelines["w"] = tl;
  </script>
</template>
""")

# captions
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
    e = end if end is not None else grp[i + 1][0][0][1] - 0.05
    caps.append(f'<div id="cap{i}" class="abs cap clip" data-start="{s}" data-duration="{round(e - s, 2)}"><span>{" ".join(x for x, _ in ws)}</span></div>')
open("compositions/cap.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; }}
    #root .abs {{ position: absolute; }}
    #root .cap {{ left: 90px; width: 900px; top: 1180px; text-align: center; font-weight: 800; font-size: 56px; line-height: 1.15; color: #fff; }}
    #root .cap span {{ display: inline-block; background: rgba(0,0,0,0.86); padding: 6px 22px 10px; border-radius: 16px; }}
  </style>
  <div id="root" data-composition-id="cap" data-width="1080" data-height="1920">
{chr(10).join("    " + c for c in caps)}
  </div>
  <script>window.__timelines["cap"] = gsap.timeline({{ paused: true }});</script>
</template>
""")

SFX = [(0.0, "boom_open", 0.45), (E["worth"], "count_fast", 0.6), (E["euros1"] + 0.18, "kaching", 0.9), (E["nobody"], "heartbeat", 0.6),
       (at["s3"], "swipe1", 0.5), (E["coffee"] - 0.1, "pop", 0.45), (E["away"] - 0.25, "pop", 0.4), (E["away"] + 0.62, "coin_jar", 0.9),
       (at["s4"], "coins_pour", 0.7), (E["invest"], "zoom_whoosh", 0.5), (E["seven"], "pop", 0.45),
       (E["y10"] - 0.2, "up1", 0.6), (E["y10"] + 0.5, "pop", 0.4), (E["y20"] - 0.2, "up2", 0.6), (E["y20"] + 0.5, "pop", 0.4),
       (E["y30"] - 0.2, "up1", 0.6), (E["y30"] + 0.5, "pop", 0.4), (E["y40"] - 1.6, "riser", 0.6), (E["big"] + 0.1, "impact", 0.9), (E["big"] + 0.12, "kaching", 0.8),
       (E["paid"] - 0.1, "swipe2", 0.5), (E["other"] + 0.2, "impact", 0.5), (E["other"] + 0.2, "pop", 0.5),
       (at["s12"] - 0.1, "scratch", 0.6), (E["lose"] + 0.1, "impact", 0.6), (at["s13"] + 0.3, "heartbeat", 0.6)]
dur = {f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/sfx/{f}.mp3"], capture_output=True, text=True).stdout) for f in {x[1] for x in SFX}}
aud = [f'  <audio id="vo-{k}" class="clip" src="assets/vo/{k}.mp3" data-start="{round(at[k], 2)}" data-duration="{round(VO[k]["dur"] - 0.01, 2)}" data-track-index="2" data-volume="1.8"></audio>' for k in ORDER]
aud += [f'  <audio id="sx{n}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(max(t, 0), 2)}" data-duration="{round(min(dur[f], DUR - t) - 0.01, 2)}" data-track-index="{10 + n}" data-volume="{v}"></audio>' for n, (t, f, v) in enumerate(SFX)]
open("index.html", "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/vendor/gsap.min.js"></script>
<style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }} #root {{ position: relative; width: 100%; height: 100%; background: #000; }}</style>
</head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <div id="w" data-composition-id="w" data-composition-src="compositions/w.html" data-start="0" data-duration="{DUR}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
  <div id="cap" data-composition-id="cap" data-composition-src="compositions/cap.html" data-start="0" data-duration="{DUR}" data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:10"></div>
{chr(10).join(aud)}
</div>
<script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>
""")
print("duration", DUR, {k: E[k] for k in ("worth", "away", "y10", "big", "paid", "other", "lose")})
