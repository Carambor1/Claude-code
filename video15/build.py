#!/usr/bin/env python3
""""Only 2 countries are doubly landlocked" — animated map video, 9:16. World map (Natural Earth 110m) lights up the landlocked
countries, then zooms to Uzbekistan (50m detail) and Liechtenstein (10m detail). Map paths come from gen-maps.mjs -> maps.json.
Run: python3 build.py"""
import json, re, subprocess

VO = json.load(open("vo.json"))
M = json.load(open("maps.json"))
ORDER = ["r1", "r2", "r3", "r4", "r5"]
GAP = {"r1": 0.45, "r2": 0.5, "r3": 0.5, "r4": 0.45}
T, at = 0.3, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.3)
DUR = round(T + 2.4, 2)
W, H = 1080, 1920
G, GD = "#4ade80", "#1f6b3c"
def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)

def svg(key, pfx, extra=""):
    m = M[key]
    items = [x for x in m["items"] if -300 < x["c"][0] < m["w"] + 300 and -300 < x["c"][1] < m["h"] + 300]
    paths = "".join(f'<path id="{pfx}{i}" d="{x["d"]}"/>' for i, x in enumerate(items))
    return f'<svg viewBox="0 0 {m["w"]} {m["h"]}" width="{m["w"]}" height="{m["h"]}" class="map">{paths}{extra}</svg>', {x["n"]: f"#{pfx}{i}" for i, x in enumerate(items)}, items
WS, WID, WIT = svg("world", "w")
CS, CID, _ = svg("ca", "c")
AS_, AID, AIT = svg("alps", "a")
ap, cp, wp = M["alps"]["pts"], M["ca"]["pts"], M["world"]["pt"]
# lens: zoomed copy around Liechtenstein
lens_paths = "".join(f'<path class="{"lli" if x["n"] == "Liechtenstein" else ""}" d="{x["d"]}"/>' for x in AIT if x["n"] in ("Liechtenstein", "Switzerland", "Austria"))
LENS = f'<svg viewBox="{ap["li"][0] - 34} {ap["li"][1] - 34} 68 68" class="map">{lens_paths}</svg>'

SK = 'fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
NOI = {
    "beach": f'<svg viewBox="0 0 100 100"><path d="M10 52 a40 40 0 0 1 80 0 Z M50 52 V88 M34 88 H66 M50 12 V6" {SK}/><path d="M12 92 L88 8" {SK} stroke="#ff5a5a" stroke-width="7"/></svg>',
    "port": f'<svg viewBox="0 0 100 100"><circle cx="50" cy="18" r="9" {SK}/><path d="M50 27 V88 M30 44 H70 M14 62 C16 82 34 90 50 88 C66 90 84 82 86 62 M14 62 l-6 12 M14 62 l12 6 M86 62 l6 12 M86 62 l-12 6" {SK}/><path d="M12 92 L88 8" {SK} stroke="#ff5a5a" stroke-width="7"/></svg>',
    "sea": f'<svg viewBox="0 0 100 100"><path d="M6 34 q11 -14 22 0 t22 0 t22 0 t22 0 M6 56 q11 -14 22 0 t22 0 t22 0 t22 0 M6 78 q11 -14 22 0 t22 0 t22 0 t22 0" {SK}/><path d="M12 92 L88 8" {SK} stroke="#ff5a5a" stroke-width="7"/></svg>',
}
WAVE = f'<svg viewBox="0 0 100 60"><path d="M4 18 q11 -14 22 0 t22 0 t22 0 t22 0 M4 42 q11 -14 22 0 t22 0 t22 0 t22 0" {SK} stroke="#7cc4ff"/></svg>'

WX0, WY0, WS0 = 0, 470, 0.95                       # world: start of pan
WX1 = W - 2000 * WS0
BS = 1.9; BX, BY = 540 - (wp["uz"][0] + wp["li"][0]) / 2 * BS, 800 - (wp["uz"][1] + wp["li"][1]) / 2 * BS
ZS = 7.0; ZX, ZY = 540 - wp["uz"][0] * ZS, 880 - wp["uz"][1] * ZS
ES = 0.8; EX, EY = -140, 560
CAX, CAY = 40, 440
ALX, ALY = 20, 500
def scr(p): return (BX + p[0] * BS, BY + p[1] * BS)
uzS, liS = scr(wp["uz"]), scr(wp["li"])
NB = (("kz", "Kazakhstan"), ("kg", "Kyrgyzstan"), ("tj", "Tajikistan"), ("af", "Afghanistan"), ("tm", "Turkmenistan"))
route = f'M{ap["li"][0]} {ap["li"][1]} L{ap["border1"][0]} {ap["border1"][1]} L{ap["border2"][0]} {ap["border2"][1]} L{ap["genoa"][0]} {ap["genoa"][1]} L{ap["sea"][0]} {ap["sea"][1] + 20}'
body = f"""
    <div class="abs hud" id="hA"><div class="hl">COUNTRIES WITH NO COAST</div><div class="hb g" id="cnt">0</div></div>
    <div class="abs hud" id="hB"><div class="hl">DOUBLY LANDLOCKED</div><div class="hb">ONLY <span class="g">2</span></div></div>
    <div class="abs hud" id="hC"><div class="hl">1 OF 2</div><div class="hb g">UZBEKISTAN</div></div>
    <div class="abs hud" id="hD"><div class="hl">2 OF 2 · 160 KM²</div><div class="hb g sm">LIECHTENSTEIN</div></div>
    <div class="abs hud" id="hE"><div class="hl">IS YOUR COUNTRY</div><div class="hb g sm">LANDLOCKED?</div></div>
    <div class="abs" id="world" style="left:0;top:0;width:2000px;height:{M["world"]["h"]}px;transform-origin:0 0">{WS}</div>
    <div class="abs ring" id="rU" style="left:{uzS[0] - 70:.0f}px;top:{uzS[1] - 70:.0f}px"></div><div class="abs ring" id="rL" style="left:{liS[0] - 70:.0f}px;top:{liS[1] - 70:.0f}px"></div>
    <div class="abs dot" id="dL" style="left:{liS[0] - 9:.0f}px;top:{liS[1] - 9:.0f}px"></div>
    <div class="abs qq" id="qU" style="left:{uzS[0] - 30:.0f}px;top:{uzS[1] - 170:.0f}px">?</div><div class="abs qq" id="qL" style="left:{liS[0] - 30:.0f}px;top:{liS[1] - 170:.0f}px">?</div>
    <div class="abs noi" id="noi">{"".join(f'<div class="ni" id="ni{i}">{NOI[k]}</div>' for i, k in enumerate(("beach", "port", "sea")))}</div>
    <div class="abs endc" id="endc"><div><span class="g">44</span> landlocked</div><div><span class="g">2</span> doubly</div></div>
    <div class="abs" id="ca" style="left:{CAX}px;top:{CAY}px;width:1000px;height:900px">{CS}
      {"".join(f'<div class="abs bdg" id="nb{i}" style="left:{cp[k][0] - 32}px;top:{cp[k][1] - 32}px">{i + 1}</div><div class="abs nm" id="nn{i}" style="left:{cp[k][0] - 150}px;top:{cp[k][1] + 36}px">{nm}</div>' for i, (k, nm) in enumerate(NB))}
      <div class="abs nm lake" id="lake" style="left:{cp["caspian"][0] - 150}px;top:{cp["caspian"][1] - 20}px">Caspian Sea<br>(a lake)</div>
    </div>
    <div class="abs" id="alps" style="left:{ALX}px;top:{ALY}px;width:1040px;height:760px">{AS_.replace("</svg>", f'<path id="rt" d="{route}" class="rt"/></svg>')}
      <div class="abs ring sm" id="rA" style="left:{ap["li"][0] - 40}px;top:{ap["li"][1] - 40}px"></div>
      <div class="abs nm big" id="nCH" style="left:{ap["ch"][0] - 230}px;top:{ap["ch"][1] + 20}px">Switzerland</div><div class="abs nm big" id="nAT" style="left:{ap["at"][0] - 150}px;top:{ap["at"][1] - 20}px">Austria</div>
      <div class="abs nm" id="nIT" style="left:{ap["it"][0] - 150 + 120}px;top:{ap["it"][1]}px">Italy</div>
      <div class="abs bdg" id="b1" style="left:{ap["border1"][0] + 24}px;top:{ap["border1"][1] - 6}px">1</div><div class="abs bdg" id="b2" style="left:{ap["border2"][0] + 24}px;top:{ap["border2"][1] - 32}px">2</div>
      <div class="abs wv" id="wv" style="left:{ap["sea"][0] - 60}px;top:{ap["sea"][1] + 30}px">{WAVE}<div class="nm sea">SEA</div></div>
      <div class="abs lens" id="lens" style="left:640px;top:-70px">{LENS}</div>
      <svg class="abs" style="left:0;top:0;width:1040px;height:760px" viewBox="0 0 1040 760"><path id="ll" d="M{ap["li"][0] + 14} {ap["li"][1] - 14} L650 150" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="8 8"/></svg>
    </div>
"""
CSS = f"""
    #root {{ position: absolute; inset: 0; background-color: #000; background-image: radial-gradient(ellipse at 50% 45%, rgba(255,255,255,0.07), rgba(0,0,0,0) 62%), radial-gradient(rgba(255,255,255,0.14) 1.6px, transparent 1.8px); background-size: 100% 100%, 34px 34px; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
    #root .abs {{ position: absolute; }}
    #root .g {{ color: {G}; }}
    #root .map {{ display: block; overflow: visible; }}
    #root .map path {{ fill: #1c2025; stroke: rgba(255,255,255,0.7); stroke-width: 1.3; vector-effect: non-scaling-stroke; stroke-linejoin: round; }}
    #root #ca .map, #root #alps .map {{ width: 100%; height: 100%; }}
    #root #alps .map path, #root #ca .map path {{ stroke-width: 2; }}
    #root .map path.rt {{ fill: none; stroke: #fff; stroke-width: 6; stroke-dasharray: 14 12; stroke-linecap: round; }}
    #root .hud {{ left: 0; top: 190px; width: {W}px; text-align: center; opacity: 0; }}
    #root .hl {{ font-weight: 800; font-size: 36px; letter-spacing: 0.22em; color: #d6d6d6; }}
    #root .hb {{ font-weight: 900; font-size: 150px; letter-spacing: -0.03em; line-height: 1.05; text-shadow: 0 0 22px rgba(255,255,255,0.35); font-variant-numeric: tabular-nums; }}
    #root .hb.g {{ text-shadow: 0 0 26px rgba(74,222,128,0.55); }}
    #root .hb.sm {{ font-size: 112px; }}
    #root #hC .hb {{ font-size: 128px; }}
    #root .ring {{ width: 140px; height: 140px; border: 5px solid {G}; border-radius: 50%; box-shadow: 0 0 24px rgba(74,222,128,0.7); opacity: 0; }}
    #root .ring.sm {{ width: 80px; height: 80px; }}
    #root .dot {{ width: 18px; height: 18px; border-radius: 50%; background: {G}; box-shadow: 0 0 16px {G}; opacity: 0; }}
    #root .qq {{ width: 60px; text-align: center; font-weight: 900; font-size: 84px; opacity: 0; }}
    #root .noi {{ left: 0; top: 1320px; width: {W}px; display: flex; justify-content: center; gap: 70px; }}
    #root .ni {{ width: 150px; height: 150px; opacity: 0; }}
    #root .endc {{ left: 0; top: 1300px; width: 1080px; display: flex; justify-content: center; gap: 24px; opacity: 0; }}
    #root .endc div {{ border: 3px solid #fff; border-radius: 999px; padding: 10px 28px; font-weight: 800; font-size: 40px; background: #000; }}
    #root .ni svg {{ width: 100%; height: 100%; }}
    #root .bdg {{ width: 64px; height: 64px; border-radius: 50%; background: #fff; color: #000; font-weight: 900; font-size: 40px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 18px rgba(255,255,255,0.6); opacity: 0; }}
    #root .nm {{ width: 300px; text-align: center; font-weight: 800; font-size: 30px; letter-spacing: 0.04em; text-shadow: 0 0 8px #000, 0 0 8px #000, 0 2px 4px #000; opacity: 0; }}
    #root .nm.big {{ font-size: 40px; }}
    #root .nm.lake {{ color: #7cc4ff; font-size: 28px; line-height: 1.15; }}
    #root .nm.sea {{ color: #7cc4ff; opacity: 1; width: 120px; font-size: 34px; letter-spacing: 0.2em; }}
    #root .wv {{ width: 120px; opacity: 0; }}
    #root .wv svg {{ width: 120px; height: 72px; display: block; }}
    #root .lens {{ width: 330px; height: 330px; border-radius: 50%; border: 5px solid #fff; overflow: hidden; background: #000; box-shadow: 0 0 30px rgba(255,255,255,0.35); opacity: 0; }}
    #root .lens .map {{ width: 100%; height: 100%; }}
    #root .lens .map path {{ fill: {GD}; stroke-width: 3; }}
    #root .lens .map path.lli {{ fill: {G}; }}
    #root #ca, #root #alps {{ opacity: 0; }}
    #root #ca > .map, #root #alps > .map {{ -webkit-mask-image: radial-gradient(ellipse 72% 72% at 50% 50%, #000 62%, transparent 100%); mask-image: radial-gradient(ellipse 72% 72% at 50% 50%, #000 62%, transparent 100%); }}
"""
J = []; a = J.append
SFX = []; sx = lambda t, f, v=0.35: SFX.append((round(max(0, t), 2), f, v))
def hud(i, t0, t1):
    a(f'tl.fromTo("#h{i}", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {t0:.2f});')
    if t1: a(f'tl.to("#h{i}", {{ opacity: 0, y: -18, duration: 0.3, ease: "power2.in" }}, {t1 - 0.3:.2f});')
def pop(sel, t, d=0.4, s0=0.4):
    a(f'tl.fromTo("{sel}", {{ opacity: 0, scale: {s0} }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "back.out(2.2)" }}, {t:.2f});')

# ---- A: pan across the world, landlocked countries light up west -> east
t_all = w("r1", "all")
a(f'tl.fromTo("#world", {{ x: {WX0}, y: {WY0}, scale: {WS0} }}, {{ x: {WX1:.0f}, duration: {t_all + 0.6:.2f}, ease: "power1.inOut" }}, 0);')
hud("A", 0.0, at["r2"])
ll = sorted([x for x in WIT if x["ll"]], key=lambda x: x["c"][0])
N = len(ll)
for i, x in enumerate(ll):
    # light each country as the pan brings it toward the middle of the screen
    frac = min(1, max(0, (x["c"][0] * WS0 - 380) / (2000 * WS0 - W)))
    t0 = 0.25 + frac * (t_all + 0.1)
    a(f'tl.to("{WID[x["n"]]}", {{ fill: "{G}", duration: 0.3 }}, {t0:.2f});')
    cnt = round((i + 1) / N * 44)
    a(f'tl.call(() => {{ $("#cnt").textContent = "{cnt}"; }}, null, {t0:.2f});')
    if i % 3 == 0: sx(t0, "ui_tick2", 0.3)
a('tl.call(() => { $("#cnt").textContent = "0"; }, null, 0);')
a(f'tl.fromTo("#cnt", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.2, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {t_all + 0.35:.2f});'); sx(t_all + 0.35, "impact", 0.4)
for i, k in enumerate(("beach", "port", "sea")):
    pop(f"#ni{i}", w("r1", k) - 0.2); sx(w("r1", k) - 0.2, "scratch", 0.3)
a(f'tl.to("#noi", {{ opacity: 0, duration: 0.3 }}, {at["r2"] - 0.3:.2f});')
sx(0, "boom_open", 0.3)

# ---- B: only two
e = {k: w("r2", k) for k in ("two", "doubly", "every", "neighbor")}
a(f'tl.to("#world", {{ x: {BX:.0f}, y: {BY:.0f}, scale: {BS}, duration: 1.2, ease: "power3.inOut" }}, {at["r2"] - 0.3:.2f});'); sx(at["r2"] - 0.3, "zoom_whoosh", 0.3)
hud("B", at["r2"] + 0.2, at["r3"])
for x in ll:
    if x["n"] != "Uzbekistan": a(f'tl.to("{WID[x["n"]]}", {{ fill: "{GD}", duration: 0.6 }}, {at["r2"] + 0.2:.2f});')
a(f'tl.fromTo("#dL", {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }}, {e["two"] + 0.15:.2f});')
for sel, q, t0 in (("#rU", "#qU", e["two"] - 0.1), ("#rL", "#qL", e["two"] + 0.15)):
    pop(sel, t0, 0.45, 2.2); pop(q, t0 + 0.1); sx(t0, "ping", 0.38)
    a(f'tl.fromTo("{sel}", {{ scale: 1 }}, {{ scale: 1.25, duration: 0.45, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false }}, {t0 + 0.5:.2f});')
sx(e["doubly"], "heartbeat", 0.38)
for sel in ("#rU", "#rL", "#qU", "#qL", "#dL"): a(f'tl.to("{sel}", {{ opacity: 0, duration: 0.3 }}, {at["r3"] - 0.4:.2f});')

# ---- C: Uzbekistan
e = {k: w("r3", k) for k in ("uzbekistan", "five", "not", "ocean")}
a(f'tl.to("#world", {{ x: {ZX:.0f}, y: {ZY:.0f}, scale: {ZS}, duration: 1.1, ease: "power3.in" }}, {at["r3"] - 0.35:.2f});'); sx(at["r3"] - 0.35, "zoom_whoosh", 0.32)
a(f'tl.to("#world", {{ opacity: 0, duration: 0.4 }}, {at["r3"] + 0.4:.2f});')
a(f'tl.fromTo("#ca", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.7, ease: "power3.out" }}, {at["r3"] + 0.4:.2f});')
a(f'gsap.set("{CID["Uzbekistan"]}", {{ fill: "{G}" }});')
hud("C", e["uzbekistan"] - 0.2, at["r4"]); sx(e["uzbekistan"] - 0.2, "impact", 0.42)
for i, (k, nm) in enumerate(NB):
    t0 = e["five"] - 0.1 + i * 0.3
    a(f'tl.to("{CID[nm]}", {{ fill: "{GD}", duration: 0.3 }}, {t0:.2f});'); pop(f"#nb{i}", t0); a(f'tl.to("#nn{i}", {{ opacity: 1, duration: 0.3 }}, {t0 + 0.1:.2f});'); sx(t0, "pop", 0.32)
a(f'tl.to("#lake", {{ opacity: 1, duration: 0.4 }}, {e["not"]:.2f});'); sx(e["ocean"], "ui_tick2", 0.4)

# ---- D: Liechtenstein
e = {k: w("r4", k) for k in ("tiny", "liechtenstein", "squeezed", "switzerland", "austria")}
a(f'tl.to("#ca", {{ opacity: 0, x: -120, duration: 0.45, ease: "power2.in" }}, {at["r4"] - 0.4:.2f});'); sx(at["r4"] - 0.4, "swipe1", 0.3)
a(f'tl.fromTo("#alps", {{ opacity: 0, x: 120 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }}, {at["r4"] - 0.05:.2f});')
a(f'gsap.set("{AID["Liechtenstein"]}", {{ fill: "{G}" }}); gsap.set(["#ll", "#rt"], {{ opacity: 0 }});')
pop("#rA", e["tiny"] - 0.1, 0.45, 2.4); sx(e["tiny"] - 0.1, "ping", 0.38)
a(f'tl.fromTo("#rA", {{ scale: 1 }}, {{ scale: 1.3, duration: 0.45, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }}, {e["tiny"] + 0.4:.2f});')
hud("D", e["liechtenstein"] - 0.25, w("r5", "is")); sx(e["liechtenstein"] - 0.25, "impact", 0.42)
a(f'tl.to("#ll", {{ opacity: 1, duration: 0.3 }}, {e["liechtenstein"]:.2f});'); pop("#lens", e["liechtenstein"], 0.5, 0.3); sx(e["liechtenstein"], "shimmer", 0.3)
for nm, lab, k in (("Switzerland", "#nCH", "switzerland"), ("Austria", "#nAT", "austria")):
    a(f'tl.to("{AID[nm]}", {{ fill: "{GD}", duration: 0.35 }}, {e[k] - 0.1:.2f});'); a(f'tl.to("{lab}", {{ opacity: 1, duration: 0.3 }}, {e[k] - 0.1:.2f});'); sx(e[k] - 0.1, "pop", 0.32)

# ---- E: two borders to the sea, then back to the world
e = {k: w("r5", k) for k in ("cross", "two", "borders", "sea", "is", "landlocked")}
a(f'tl.to(["#lens", "#ll"], {{ opacity: 0, duration: 0.3 }}, {at["r5"] - 0.1:.2f});')
a(f'tl.to("#rt", {{ opacity: 1, duration: 0.1 }}, {e["cross"] - 0.2:.2f});')
a(f'tl.fromTo("#rt", {{ strokeDasharray: "14 12", strokeDashoffset: 0, clipPath: "inset(0 0 100% 0)" }}, {{ clipPath: "inset(0 0 0% 0)", duration: {e["sea"] - e["cross"] + 0.3:.2f}, ease: "power1.inOut" }}, {e["cross"] - 0.2:.2f});'); sx(e["cross"] - 0.2, "swipe2", 0.3)
pop("#b1", e["two"] - 0.05); pop("#b2", e["borders"]); sx(e["two"] - 0.05, "pop", 0.34); sx(e["borders"], "pop", 0.34)
a(f'tl.to("#nIT", {{ opacity: 1, duration: 0.3 }}, {e["borders"] + 0.2:.2f});')
pop("#wv", e["sea"] - 0.1); sx(e["sea"] - 0.1, "shimmer", 0.35)
a(f'tl.to("#alps", {{ opacity: 0, scale: 0.85, duration: 0.45, ease: "power2.in" }}, {e["is"] - 0.4:.2f});'); sx(e["is"] - 0.4, "zoom_whoosh", 0.3)
a(f'tl.fromTo("#world", {{ x: {EX}, y: {EY}, scale: {ES * 1.6:.3f}, opacity: 0 }}, {{ x: {EX}, y: {EY}, scale: {ES}, opacity: 1, duration: 0.8, ease: "power3.out", immediateRender: false }}, {e["is"] - 0.1:.2f});')
a(f'tl.to("#world", {{ x: {EX - 380}, duration: {DUR - e["is"] - 0.7:.2f}, ease: "none" }}, {e["is"] + 0.7:.2f});')
for x in ll: a(f'tl.to("{WID[x["n"]]}", {{ fill: "{G}", duration: 0.3 }}, {e["is"] - 0.15:.2f});')
a(f'tl.fromTo("#endc", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {e["is"] + 0.5:.2f});')
hud("E", e["is"], None); sx(e["landlocked"], "ping", 0.4)
a(f'tl.fromTo("#hE .hb", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.35, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {e["landlocked"] + 0.2:.2f});')

open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    <div id="lay" style="position:absolute;inset:0">{body}</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const R = document.querySelector('[data-composition-id="w"]') || document;
    const $ = (s) => R.querySelector(s);
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
    #root .cap {{ left: 90px; width: 900px; top: 1500px; text-align: center; font-weight: 800; font-size: 58px; line-height: 1.15; color: #fff; }}
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
