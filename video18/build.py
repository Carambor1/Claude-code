#!/usr/bin/env python3
""""How your phone knows where you are" — motion-design reel look (charcoal / orange / off-white, smear type, grids, 3D sets).
3D (src/film.js -> assets/film.js): dotted globe + GPS constellation to scale, cube wave. Run: python3 build.py"""
import json, re, subprocess, math

VO = json.load(open("vo.json"))
ORDER = [f"r{i}" for i in range(1, 8)]
GAP = {"r1": 0.5, "r2": 0.45, "r3": 0.45, "r4": 0.45, "r5": 0.5, "r6": 0.55}
T, at = 0.3, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.3)
DUR = round(T + 2.4, 2)
W, H = 1080, 1920
OR, WH, BG = "#ff5a1f", "#f3efe8", "#121110"
def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)
B = [0] + [round(at[f"r{i}"] - 0.25, 2) for i in range(2, 8)] + [DUR]      # scene boundaries
K = dict(shout=round(w("r2", "shout") - B[1], 2), miss=w("r6", "off") - 0.1, at=dict(gA=B[1], gB=B[2], vA=B[5], vB=B[6]))

# trilateration geometry (px in the 1080x1920 frame)
P = (560, 1090)
SAT = [(300, 830), (820, 880), (500, 1400), (230, 1290)]
RAD = [math.dist(s, P) for s in SAT]
def isect(c0, r0, c1, r1):
    d = math.dist(c0, c1); a = (r0 * r0 - r1 * r1 + d * d) / (2 * d); h = math.sqrt(max(0, r0 * r0 - a * a)); xm = c0[0] + a * (c1[0] - c0[0]) / d; ym = c0[1] + a * (c1[1] - c0[1]) / d
    return [(xm + h * (c1[1] - c0[1]) / d, ym - h * (c1[0] - c0[0]) / d), (xm - h * (c1[1] - c0[1]) / d, ym + h * (c1[0] - c0[0]) / d)]
P2 = max(isect(SAT[0], RAD[0], SAT[1], RAD[1]), key=lambda q: math.dist(q, P))
GRID = "".join(f'<i id="gd{r}_{c}" style="left:{90 + c * 100 - 6}px;top:{640 + r * 100 - 6}px"></i>' for r in range(10) for c in range(10))
def circ(i): return f'<circle id="ci{i}" cx="{SAT[i][0]}" cy="{SAT[i][1]}" r="{RAD[i]:.1f}" fill="none" stroke="{OR if i < 3 else WH}" stroke-width="5" stroke-dasharray="{2 * math.pi * RAD[i]:.0f}" stroke-dashoffset="{2 * math.pi * RAD[i]:.0f}" transform="rotate(-90 {SAT[i][0]} {SAT[i][1]})"/>'
def satm(i): return f'<div class="abs sat" id="sm{i}" style="left:{SAT[i][0] - 22}px;top:{SAT[i][1] - 22}px"><b>{i + 1}</b></div>'
SX = [170, 420, 670, 910]; DEL = ["67.3", "71.8", "74.2", "69.5"]

def sc(i, inner): return f'<div class="abs scene" id="sc{i}">{inner}</div>'
S1 = ('<div class="abs ctr t1" id="a1">YOUR PHONE</div><div class="abs ctr t1 or" id="a2">ALWAYS KNOWS</div>'
      '<div class="abs ctr t1" id="a3">BUT IT NEVER</div><div class="abs ctr t1 blk" id="a4"><span>TALKS BACK.</span></div>'
      '<div class="abs phone" id="ph"><div class="abs ring" id="pr1"></div><div class="abs ring" id="pr2"></div><div class="abs dot" id="pd"></div></div>'
      f'<div class="abs mono" id="up" style="left:0;width:{W}px;text-align:center;top:1390px;font-size:30px">UPLINK <span class="or">0 BYTES</span> / DOWNLINK LISTENING</div>')
S2 = ('<div class="abs ctr t2" id="b1">20,000 KM</div><div class="abs ctr lab" id="b1l">ABOVE YOU / DRAWN TO SCALE</div>'
      '<div class="abs ctr t2 or" id="b2" style="top:1250px;font-size:150px">~30</div><div class="abs ctr lab" id="b2l" style="top:1410px">SATELLITES / SHOUTING THE TIME</div>')
S3 = ("".join(f'<div class="abs sat big" style="left:{x - 34}px;top:330px"><b>{i + 1}</b></div><div class="abs mono dl" id="dl{i}" style="left:{x - 110}px;top:420px">+<span id="dv{i}">0.0</span> ms</div>' + "".join(f'<div class="abs wave" id="wv{i}_{j}" style="left:{x - 500}px;top:{364 - 500}px"></div>' for j in range(3)) for i, x in enumerate(SX))
      + '<div class="abs ctr t1" id="c1" style="top:760px">IT JUST</div><div class="abs ctr t1 or" id="c2" style="top:900px">LISTENS.</div><div class="abs phone sm" id="ph3"><div class="abs dot"></div></div>')
S4 = ('<div class="abs ctr eq" id="eq"><span id="e1">LATE</span><span id="e2" class="or">=</span><span id="e3">FAR</span></div>'
      f'<div class="abs grid" id="g4">{GRID}</div>'
      f'<svg class="abs" style="left:0;top:0;width:{W}px;height:{H}px" viewBox="0 0 {W} {H}">{"".join(circ(i) for i in range(4))}</svg>'
      + "".join(satm(i) for i in range(4))
      + f'<div class="abs cand" id="x2" style="left:{P2[0] - 16:.0f}px;top:{P2[1] - 16:.0f}px"></div>'
      f'<div class="abs you" id="you" style="left:{P[0] - 26}px;top:{P[1] - 26}px"><i></i></div>'
      '<div class="abs ctr cnt" id="cnt"><b id="cn">1</b><span id="cl">SATELLITE = A CIRCLE</span></div>'
      f'<div class="abs clk" id="clk"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="{WH}" stroke-width="6"/><path id="clh" d="M50 50 V20" stroke="{OR}" stroke-width="7" stroke-linecap="round"/></svg><span>CLOCK FIXED</span></div>')
S6 = ('<div class="abs ctr t3 mono2" id="f1">0.000001 s</div><div class="abs ctr lab" id="f1l" style="top:420px">ONE MILLIONTH OF A SECOND LATE</div>'
      '<div class="abs ctr t2 or" id="f2" style="top:1210px">300 M OFF</div>')
S7 = (f'<div class="abs grid" id="g7">{GRID.replace("gd", "ge")}</div><div class="abs halo" id="hl"></div><div class="abs ring" id="er1" style="left:440px;top:990px"></div><div class="abs ring" id="er2" style="left:440px;top:990px"></div><div class="abs dot" id="ed" style="left:512px;top:1062px"></div>'
      '<div class="abs ctr t1" id="h1" style="top:300px;font-size:112px">THAT\'S THE DOT.</div><div class="abs ctr t1 blk" id="h2" style="top:450px;font-size:104px"><span>IT ONLY LISTENS.</span></div>')
body = (f'<canvas id="gl" width="720" height="1280" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px"></canvas>'
        + sc(1, S1) + sc(2, S2) + sc(3, S3) + sc(4, S4) + sc(6, S6) + sc(7, S7)
        + '<div class="abs hud"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i>'
          '<div class="abs mono" style="left:64px;top:104px">GPS / HOW IT WORKS</div><div class="abs mono" id="tc" style="right:64px;top:104px">00:00:00</div>'
          '<div class="abs mono" id="ix" style="left:64px;bottom:96px">01 / 07</div><div class="abs mono" style="right:64px;bottom:96px">N 52.52 / E 13.40</div></div>'
          '<div class="abs wipe" id="wipe"></div>')
CSS = f"""
    #root {{ position: absolute; inset: 0; background: radial-gradient(ellipse 90% 60% at 50% 45%, #24201d 0%, {BG} 70%); font-family: "Inter", sans-serif; color: {WH}; overflow: hidden; }}
    #root .abs {{ position: absolute; }}
    #root .ctr {{ left: 0; width: {W}px; text-align: center; }}
    #root .or {{ color: {OR}; }}
    #root .scene {{ inset: 0; opacity: 0; }}
    #root .mono {{ font-family: "JetBrains Mono", monospace; font-weight: 500; font-size: 26px; letter-spacing: 0.08em; color: rgba(243,239,232,0.6); white-space: nowrap; }}
    #root .t1 {{ font-weight: 900; font-size: 128px; letter-spacing: -0.045em; line-height: 1; white-space: nowrap; }}
    #root .t2 {{ font-weight: 900; font-size: 190px; letter-spacing: -0.05em; line-height: 1; top: 230px; white-space: nowrap; }}
    #root .t3 {{ font-size: 138px; top: 250px; line-height: 1; white-space: nowrap; }}
    #root .mono2 {{ font-family: "JetBrains Mono", monospace; font-weight: 800; letter-spacing: -0.04em; }}
    #root .lab {{ top: 440px; font-family: "JetBrains Mono", monospace; font-weight: 500; font-size: 32px; letter-spacing: 0.14em; color: rgba(243,239,232,0.75); }}
    #root .blk span {{ display: inline-block; background: {OR}; color: {BG}; padding: 6px 30px 12px; }}
    #root #a1 {{ top: 250px; }} #root #a2 {{ top: 390px; }} #root #a3 {{ top: 250px; }} #root #a4 {{ top: 390px; }}
    #root .phone {{ left: 365px; top: 640px; width: 350px; height: 690px; border: 6px solid {WH}; border-radius: 60px; }}
    #root .phone.sm {{ left: 470px; top: 1160px; width: 140px; height: 270px; border-width: 5px; border-radius: 28px; }}
    #root .dot {{ left: 147px; top: 317px; width: 56px; height: 56px; border-radius: 50%; background: {OR}; box-shadow: 0 0 40px rgba(255,90,31,0.8); }}
    #root .phone.sm .dot {{ left: 49px; top: 114px; width: 34px; height: 34px; }}
    #root .ring {{ left: 75px; top: 245px; width: 200px; height: 200px; border-radius: 50%; border: 4px solid {OR}; opacity: 0; }}
    #root .sat {{ width: 44px; height: 44px; background: {OR}; color: {BG}; font-family: "JetBrains Mono", monospace; font-weight: 800; font-size: 26px; display: flex; align-items: center; justify-content: center; opacity: 0; }}
    #root .sat.big {{ width: 68px; height: 68px; font-size: 36px; opacity: 1; }}
    #root .sat.big::before, #root .sat.big::after {{ content: ""; position: absolute; top: 24px; width: 46px; height: 20px; background: {WH}; }}
    #root .sat.big::before {{ left: -54px; }} #root .sat.big::after {{ right: -54px; }}
    #root .dl {{ width: 220px; text-align: center; font-size: 30px; color: {WH}; opacity: 0; }}
    #root .wave {{ width: 1000px; height: 1000px; border-radius: 50%; border: 4px solid {OR}; opacity: 0; clip-path: inset(50% 0 0 0); }}
    #root .eq {{ top: 250px; font-weight: 900; font-size: 200px; letter-spacing: -0.05em; line-height: 1; display: flex; justify-content: center; gap: 34px; transform-origin: 50% 0; }}
    #root .eq span {{ display: inline-block; opacity: 0; }}
    #root .grid i {{ position: absolute; width: 12px; height: 12px; background: rgba(243,239,232,0.35); }}
    #root .grid {{ inset: 0; opacity: 0; }}
    #root .cand {{ width: 32px; height: 32px; border: 5px solid {WH}; border-radius: 50%; opacity: 0; }}
    #root .you {{ width: 52px; height: 52px; opacity: 0; }}
    #root .you i {{ position: absolute; inset: 0; border-radius: 50%; background: {WH}; box-shadow: 0 0 0 10px rgba(243,239,232,0.25), 0 0 50px rgba(255,255,255,0.7); }}
    #root .cnt {{ top: 230px; display: flex; align-items: center; justify-content: center; gap: 30px; opacity: 0; }}
    #root .cnt b {{ font-weight: 900; font-size: 250px; letter-spacing: -0.05em; line-height: 1; color: {OR}; }}
    #root .cnt span {{ font-family: "JetBrains Mono", monospace; font-weight: 800; font-size: 44px; letter-spacing: 0.02em; text-align: left; width: 420px; line-height: 1.15; }}
    #root .clk {{ left: 780px; top: 520px; width: 250px; display: flex; flex-direction: column; align-items: center; gap: 10px; opacity: 0; }}
    #root .clk svg {{ width: 130px; height: 130px; }}
    #root .clk span {{ font-family: "JetBrains Mono", monospace; font-weight: 800; font-size: 28px; }}
    #root .halo {{ left: 340px; top: 890px; width: 400px; height: 400px; border-radius: 50%; background: rgba(255,90,31,0.14); border: 3px solid rgba(255,90,31,0.5); opacity: 0; }}
    #root #ed {{ opacity: 0; }}
    #root .hud {{ inset: 0; }}
    #root .hud i {{ position: absolute; width: 34px; height: 34px; border: 3px solid rgba(243,239,232,0.5); }}
    #root .hud .c1 {{ left: 40px; top: 60px; border-right: 0; border-bottom: 0; }} #root .hud .c2 {{ right: 40px; top: 60px; border-left: 0; border-bottom: 0; }}
    #root .hud .c3 {{ left: 40px; bottom: 60px; border-right: 0; border-top: 0; }} #root .hud .c4 {{ right: 40px; bottom: 60px; border-left: 0; border-top: 0; }}
    #root .wipe {{ inset: 0; background: {OR}; transform: scaleY(0); }}
"""
J = []; a = J.append
SFX = []; sx = lambda t, f, v=0.35: SFX.append((round(max(0, t), 2), f, v))
def smear(sel, t, dx=-520, d=0.5):
    a(f'tl.fromTo("{sel}", {{ opacity: 0, x: {dx}, scaleX: 2.6, filter: "blur(26px)" }}, {{ opacity: 1, x: 0, scaleX: 1, filter: "blur(0px)", duration: {d}, ease: "expo.out" }}, {t:.2f});'); sx(t, "swipe1" if dx < 0 else "swipe2", 0.3)
def out(sel, t, dx=420, d=0.28):
    a(f'tl.to("{sel}", {{ opacity: 0, x: {dx}, scaleX: 2.2, filter: "blur(22px)", duration: {d}, ease: "expo.in" }}, {t:.2f});')
def pop(sel, t, d=0.45):
    a(f'tl.fromTo("{sel}", {{ opacity: 0, scale: 0.2 }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "back.out(2.4)" }}, {t:.2f});')
def pulse(sel, t0, t1, period=1.1, s1=3.2):
    n = max(1, int((t1 - t0) / period))
    a(f'tl.fromTo("{sel}", {{ scale: 0.3, opacity: 0.9 }}, {{ scale: {s1}, opacity: 0, duration: {period}, ease: "power2.out", repeat: {n - 1} }}, {t0:.2f});')

# scene switching + orange wipes
SCN = [1, 2, 3, 4, 4, 6, 7]
a('tl.set("#sc1", { opacity: 1 }, 0);')
for n in range(1, 7):
    tb = B[n]
    if SCN[n] != SCN[n - 1]:
        a(f'tl.set("#wipe", {{ transformOrigin: "50% 100%" }}, {tb - 0.26:.2f}); tl.fromTo("#wipe", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.24, ease: "expo.in", immediateRender: false }}, {tb - 0.24:.2f});')
        a(f'tl.set("#wipe", {{ transformOrigin: "50% 0%" }}, {tb:.2f}); tl.to("#wipe", {{ scaleY: 0, duration: 0.34, ease: "expo.out" }}, {tb + 0.02:.2f});')
        a(f'tl.set("#sc{SCN[n - 1]}", {{ opacity: 0 }}, {tb:.2f}); tl.set("#sc{SCN[n]}", {{ opacity: 1 }}, {tb:.2f});'); sx(tb - 0.26, "zoom_whoosh", 0.34)
    a(f'tl.call(() => {{ $("#ix").textContent = "0{n + 1} / 07"; }}, null, {tb:.2f});')
a('tl.call(() => { $("#ix").textContent = "01 / 07"; }, null, 0);')
a(f'(() => {{ const c = {{ t: 0 }}; tl.fromTo(c, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: () => {{ const s = Math.floor(c.t), f = Math.floor((c.t % 1) * 30); $("#tc").textContent = "00:" + String(s).padStart(2, "0") + ":" + String(f).padStart(2, "0"); if (film) film.render(c.t); }} }}, 0); }})();')

# ---- 1 hook
smear("#a1", 0.05); smear("#a2", w("r1", "always") - 0.15, 520)
a('tl.fromTo("#ph", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.7, ease: "expo.out" }, 0.1);')
pulse("#pr1", 0.3, B[1]); pulse("#pr2", 0.85, B[1]); sx(0, "boom_open", 0.32); sx(w("r1", "knows"), "ping", 0.4)
a('tl.fromTo("#up", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.6);')
a('gsap.set(["#a3", "#a4"], { opacity: 0 });')
tb = w("r1", "but") - 0.1
out("#a1", tb - 0.25); out("#a2", tb - 0.2, -420)
smear("#a3", tb); smear("#a4", w("r1", "tells") - 0.1, 520); sx(w("r1", "tells") - 0.1, "impact", 0.42)
a(f'tl.fromTo("#up", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.14, yoyo: true, repeat: 5, ease: "steps(1)", immediateRender: false }}, {w("r1", "satellites"):.2f});')
# ---- 2 globe (3D)
a('gsap.set(["#b1", "#b2", "#b1l", "#b2l", "#c1", "#c2", "#f1", "#f2", "#f1l", "#h1", "#h2"], { opacity: 0 });')
smear("#b1", w("r2", "twenty") + 0.05); a(f'tl.fromTo("#b1l", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {w("r2", "kilometers"):.2f});')
smear("#b2", w("r2", "about") - 0.05, 520); a(f'tl.fromTo("#b2l", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {w("r2", "satellites"):.2f});'); sx(w("r2", "thirty"), "impact", 0.4)
for i in range(4): sx(w("r2", "shout") + i * 0.28, "ping", 0.3)
# ---- 3 listening
for i in range(4):
    for j in range(3):
        t0 = B[2] + 0.25 + i * 0.17 + j * 0.42
        n = max(1, int((B[3] - t0) / 1.26))
        a(f'tl.fromTo("#wv{i}_{j}", {{ scale: 0.04, opacity: 0.95 }}, {{ scale: 2.0, opacity: 0, duration: 1.26, ease: "power1.out", repeat: {n - 1} }}, {t0:.2f});')
    td = w("r3", "late") - 0.2 + i * 0.12
    a(f'tl.fromTo("#dl{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {td:.2f});')
    a(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {DEL[i]}, duration: 0.8, ease: "power3.out", immediateRender: false, onUpdate: () => {{ $("#dv{i}").textContent = o.v.toFixed(1); }} }}, {td:.2f}); }})();'); sx(td, "ui_tick2", 0.4)
smear("#c1", w("r3", "just") - 0.2); smear("#c2", w("r3", "listens") - 0.1, 520); sx(w("r3", "listens") - 0.1, "impact", 0.4)
a(f'tl.fromTo("#ph3", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {B[2] + 0.1:.2f});')
# ---- 4 late = far -> one circle
for sel, wd, dx in (("#e1", "late", -400), ("#e2", "means", 0), ("#e3", "far", 400)):
    a(f'tl.fromTo("{sel}", {{ opacity: 0, x: {dx}, scaleX: {2.4 if dx else 1}, scale: {1 if dx else 0.2}, filter: "blur({22 if dx else 0}px)" }}, {{ opacity: 1, x: 0, scaleX: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }}, {w("r4", wd) - 0.08:.2f});'); sx(w("r4", wd) - 0.08, "impact" if wd == "far" else "swipe1", 0.38)
t1 = w("r4", "one") - 0.25
a(f'tl.to("#eq", {{ opacity: 0, y: -60, duration: 0.3, ease: "power2.in" }}, {t1:.2f});')
a(f'tl.fromTo("#g4", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {t1 + 0.1:.2f});')
a(f'tl.fromTo("#cnt", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {t1 + 0.2:.2f});')
def draw(i, t, d=0.8):
    pop(f"#sm{i}", t - 0.25, 0.35); a(f'tl.to("#ci{i}", {{ strokeDashoffset: 0, duration: {d}, ease: "power3.inOut" }}, {t:.2f});'); sx(t - 0.25, "pop", 0.34); sx(t, "swipe2", 0.3)
def cnt(n, lab, t):
    a(f'tl.call(() => {{ $("#cn").textContent = "{n}"; $("#cl").textContent = "{lab}"; }}, null, {t:.2f});')
    a(f'tl.fromTo("#cn", {{ scale: 1.5 }}, {{ scale: 1, duration: 0.4, ease: "back.out(2)", immediateRender: false }}, {t:.2f});')
a('tl.call(() => { $("#cn").textContent = "1"; $("#cl").textContent = "SATELLITE = A CIRCLE"; }, null, 0);')
draw(0, w("r4", "distance") - 0.2, 1.1)
# ---- 5 two / three / four
e = {k: w("r5", k) for k in ("two", "twice", "three", "single", "fourth", "clock")}
cnt(2, "CIRCLES = 2 POINTS", e["two"] - 0.1); draw(1, e["two"] - 0.05)
pop("#x2", e["twice"] - 0.1); pop("#you", e["twice"] + 0.08); sx(e["twice"] - 0.1, "ping", 0.38); sx(e["twice"] + 0.08, "ping", 0.38)
cnt(3, "CIRCLES = 1 POINT", e["three"] - 0.1); draw(2, e["three"] - 0.05)
a(f'tl.to("#x2", {{ opacity: 0, scale: 0.2, duration: 0.3 }}, {e["single"] - 0.15:.2f});')
a(f'tl.to("#you i", {{ backgroundColor: "{OR}", boxShadow: "0 0 0 14px rgba(255,90,31,0.3), 0 0 70px rgba(255,90,31,0.9)", duration: 0.3 }}, {e["single"] - 0.1:.2f});')
a(f'tl.fromTo("#you", {{ scale: 1 }}, {{ scale: 1.7, duration: 0.2, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }}, {e["single"] - 0.1:.2f});'); sx(e["single"] - 0.1, "impact", 0.45)
for r in range(10):
    for c in range(10):
        dd = math.dist((90 + c * 100, 640 + r * 100), P)
        if dd < 330: a(f'tl.to("#gd{r}_{c}", {{ scale: {3.2 - dd / 130:.2f}, backgroundColor: "{OR}", rotation: 45, duration: 0.35, ease: "back.out(2)" }}, {e["single"] - 0.05 + dd / 900:.2f});')
cnt(4, "SATELLITES = CLOCK FIXED", e["fourth"] - 0.1); draw(3, e["fourth"] - 0.05)
pop("#clk", e["clock"] - 0.3); a(f'tl.fromTo("#clh", {{ rotation: -90, svgOrigin: "50 50" }}, {{ rotation: 0, duration: 0.5, ease: "back.out(2.5)" }}, {e["clock"] - 0.2:.2f});'); sx(e["clock"] - 0.2, "clock_tick", 0.7)
# ---- 6 one millionth -> 300 m (3D cube wave)
smear("#f1", w("r6", "one") - 0.15); a(f'tl.fromTo("#f1l", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {w("r6", "millionth") + 0.2:.2f});')
smear("#f2", w("r6", "three") - 0.12, 520); sx(w("r6", "three") - 0.12, "impact", 0.45); sx(K["miss"], "riser", 0.3)
# ---- 7 the dot
a(f'tl.fromTo("#g7", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {B[6] + 0.1:.2f});')
pop("#ed", w("r7", "dot") - 0.15); pop("#hl", w("r7", "dot")); sx(w("r7", "dot") - 0.15, "ping", 0.42)
pulse("#er1", w("r7", "dot"), DUR, 1.2, 3.6); pulse("#er2", w("r7", "dot") + 0.6, DUR, 1.2, 3.6)
smear("#h1", B[6] + 0.25); smear("#h2", w("r7", "only") - 0.2, 520); sx(w("r7", "listens"), "impact", 0.45); sx(w("r7", "listens") + 0.1, "shimmer", 0.35)
a(f'tl.fromTo("#h2", {{ x: 0 }}, {{ x: 14, duration: 0.05, yoyo: true, repeat: 5, ease: "steps(1)", immediateRender: false }}, {w("r7", "listens") + 0.25:.2f});')

subprocess.run(["node_modules/.bin/esbuild", "src/film.js", "--bundle", "--format=iife", "--global-name=Film", "--minify", "--outfile=assets/film.js", "--log-level=warning"], check=True)
open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    {body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const R = document.querySelector('[data-composition-id="w"]') || document;
    const $ = (s) => R.querySelector(s);
    let film = null;
    window.__hf = window.__hf || {{}}; window.__hf.buildReady = window.__hf.buildReady || {{}};
    window.__hf.buildReady["film"] = Film.init($("#gl"), {json.dumps(K)}).then((f) => {{ film = f; f.render(tl.time()); }});
{chr(10).join("    " + x for x in J)}
    window.__timelines["w"] = tl;
  </script>
</template>
""")

grp = []
for k in ORDER[:7]:
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
    #root .cap {{ left: 90px; width: 900px; top: 1570px; text-align: center; font-weight: 800; font-size: 52px; line-height: 1.15; color: #fff; }}
    #root .cap span {{ display: inline-block; padding: 6px 22px 10px; text-shadow: 0 2px 14px rgba(0,0,0,0.9), 0 0 3px rgba(0,0,0,0.8); }}
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
<script src="assets/film.js"></script>
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
