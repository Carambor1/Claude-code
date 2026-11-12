#!/usr/bin/env python3
""""Nobody remembers your first try" — kinetic-type motivation piece in the motion-design reel look (charcoal / orange / off-white).
3D (src/film.js -> assets/film.js): a glossy metaball blob, lumpy at first, a clean sphere at the end. Run: python3 build.py"""
import json, re, subprocess, math

VO = json.load(open("vo.json"))
ORDER = ["r1"]
at = {"r1": 0.3}
DUR = round(0.3 + VO["r1"]["dur"] + 2.6, 2)
W, H = 1080, 1920
OR, WH, BG = "#ff5a1f", "#f3efe8", "#121110"
def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)
W1 = lambda word, nth=0: w("r1", word, nth)
B = [0, W1("not") - 0.2, W1("the", 3) - 0.2, W1("people") - 0.2, W1("and") - 0.15, W1("so") - 0.2, DUR]
K = dict(today=W1("today"), at=dict(a1=B[1], b0=B[5]))

SK = f'fill="none" stroke="{WH}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"'
IC = [
    f'<svg viewBox="0 0 560 380"><rect x="20" y="20" width="520" height="340" rx="36" {SK}/><path d="M240 130 L340 190 L240 250 Z" fill="{WH}"/><circle cx="476" cy="76" r="16" fill="{OR}"/></svg>',
    f'<svg viewBox="0 0 560 380"><rect x="90" y="10" width="380" height="360" rx="10" {SK}/><path id="scr" d="M150 290 C170 120 210 330 250 150 C270 60 300 320 330 190 C350 110 390 300 410 100 M190 250 C240 300 330 300 380 240" {SK} stroke="{OR}" stroke-dasharray="1500" stroke-dashoffset="1500"/></svg>',
    f'<svg viewBox="0 0 560 380"><path d="M40 20 V350 H540" {SK}/><path id="crash" d="M70 300 L170 230 L250 250 L330 110 L400 150 L510 330" {SK} stroke="{OR}" stroke-dasharray="900" stroke-dashoffset="900"/><path id="crar" d="M510 330 l-56 -8 M510 330 l-10 -56" {SK} stroke="{OR}"/></svg>',
]
LB = ["THE SHAKY VIDEO", "THE BAD DRAWING", "THE PITCH THAT FLOPPED"]
GX, GY, CS, GP = 88, 640, 76, 16
CELLS = "".join(f'<i id="c{n}" style="left:{GX + (n % 10) * (CS + GP)}px;top:{GY + (n // 10) * (CS + GP)}px"></i>' for n in range(100))
cx = lambda n: GX + (n % 10) * (CS + GP) + CS / 2
cy = lambda n: GY + (n // 10) * (CS + GP) + CS / 2
def sc(i, inner): return f'<div class="abs scene" id="sc{i}">{inner}</div>'
S1 = ('<div class="abs ctr t0" id="a1">NOBODY</div><div class="abs ctr t1" id="a2" style="top:440px;font-size:150px">REMEMBERS</div>'
      '<div class="abs ctr t1 blk" id="a3" style="top:620px;font-size:104px"><span>YOUR FIRST TRY.</span></div>')
S2 = ('<div class="abs ctr t0" id="not">NOT</div><div class="abs ctr mono nn" id="nn">01 / 03</div>'
      + "".join(f'<div class="abs card" id="k{i}"><div class="ic" id="ki{i}">{IC[i]}</div><div class="kl">{LB[i]}</div><div class="abs strike" id="ks{i}"></div></div>' for i in range(3)))
S3 = ('<div class="abs ctr lab" style="top:250px" id="p0">THE FIRST TRY</div>'
      '<div class="abs ctr t1" id="p1" style="top:330px;font-size:140px">ISN\'T THE</div><div class="abs ctr t1" id="p2" style="top:480px;font-size:170px"><span class="stw">PRODUCT.<i id="pst"></i></span></div>'
      '<div class="abs ctr t1" id="p3" style="top:800px;font-size:140px">IT\'S THE</div><div class="abs ctr t1 blk" id="p4" style="top:960px;font-size:230px"><span>PRICE.</span></div>'
      '<div class="abs tick" id="tk">TRY #001 / ADMIT ONE</div>')
S4 = ('<div class="abs ctr lab" style="top:250px" id="q0">PEOPLE ONLY SEE</div><div class="abs ctr t3 mono2" id="q1" style="top:320px;font-size:190px">TRY <span id="qn" class="or">001</span></div>'
      f'<div class="abs cells">{CELLS}</div>'
      f'<svg class="abs" style="left:0;top:0;width:{W}px;height:{H}px" viewBox="0 0 {W} {H}"><path id="arw" d="M{cx(0)} {cy(0)} L{cx(99)} {cy(99)}" fill="none" stroke="{WH}" stroke-width="6" stroke-dasharray="1300" stroke-dashoffset="1300"/></svg>')
S6 = ('<div class="abs ctr t1" id="u1" style="top:250px;font-size:150px">SO MAKE IT</div><div class="abs ctr t0 or" id="u2" style="top:410px;font-size:280px">UGLY.</div>'
      '<div class="abs ctr t1" id="u3" style="top:250px;font-size:150px">MAKE IT</div><div class="abs ctr t1 blk" id="u4" style="top:420px;font-size:230px"><span>TODAY.</span></div>')
body = (f'<canvas id="gl" width="720" height="1280" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px"></canvas>'
        + sc(1, S1) + sc(2, S2) + sc(3, S3) + sc(4, S4) + sc(6, S6)
        + '<div class="abs hud"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i>'
          '<div class="abs mono" style="left:64px;top:104px">FIRST TRY / A REMINDER</div><div class="abs mono" id="tc" style="right:64px;top:104px">00:00:00</div>'
          '<div class="abs mono" id="ix" style="left:64px;bottom:96px">01 / 05</div><div class="abs mono" style="right:64px;bottom:96px">MAKE IT UGLY</div></div>'
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

CSS += f"""
    #root .t0 {{ top: 230px; font-weight: 900; font-size: 230px; letter-spacing: -0.05em; line-height: 1; white-space: nowrap; }}
    #root .nn {{ top: 480px; font-size: 34px; color: {OR}; }}
    #root .card {{ left: 110px; top: 660px; width: 860px; display: flex; flex-direction: column; align-items: center; gap: 44px; opacity: 0; }}
    #root .card .ic {{ width: 780px; height: 530px; }}
    #root .card .ic svg {{ width: 100%; height: 100%; display: block; overflow: visible; }}
    #root .card .kl {{ font-family: "JetBrains Mono", monospace; font-weight: 800; font-size: 58px; letter-spacing: 0.02em; white-space: nowrap; }}
    #root .strike {{ left: -10px; top: 250px; width: 880px; height: 22px; background: {OR}; transform: rotate(-9deg) scaleX(0); transform-origin: 0 50%; }}
    #root .stw {{ position: relative; display: inline-block; }}
    #root .stw i {{ position: absolute; left: -3%; top: 46%; width: 106%; height: 22px; background: {OR}; transform: scaleX(0); transform-origin: 0 50%; }}
    #root .tick {{ left: 250px; top: 1330px; width: 580px; text-align: center; font-family: "JetBrains Mono", monospace; font-weight: 800; font-size: 38px; padding: 26px 0; border: 5px dashed {WH}; border-radius: 18px; opacity: 0; }}
    #root .cells i {{ position: absolute; width: {CS}px; height: {CS}px; background: rgba(243,239,232,0.13); }}
"""
SCN = [1, 2, 3, 4, 4, 6]
a('tl.set("#sc1", { opacity: 1 }, 0);')
for n in range(1, 6):
    tb = B[n]
    if SCN[n] != SCN[n - 1]:
        a(f'tl.set("#wipe", {{ transformOrigin: "50% 100%" }}, {tb - 0.24:.2f}); tl.fromTo("#wipe", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.22, ease: "expo.in", immediateRender: false }}, {tb - 0.22:.2f});')
        a(f'tl.set("#wipe", {{ transformOrigin: "50% 0%" }}, {tb:.2f}); tl.to("#wipe", {{ scaleY: 0, duration: 0.32, ease: "expo.out" }}, {tb + 0.02:.2f});')
        a(f'tl.set("#sc{SCN[n - 1]}", {{ opacity: 0 }}, {tb:.2f}); tl.set("#sc{SCN[n]}", {{ opacity: 1 }}, {tb:.2f});'); sx(tb - 0.24, "zoom_whoosh", 0.34)
    a(f'tl.call(() => {{ $("#ix").textContent = "0{min(n + 1, 5) if n < 4 else n} / 05"; }}, null, {tb:.2f});')
a('tl.call(() => { $("#ix").textContent = "01 / 05"; }, null, 0);')
a(f'(() => {{ const c = {{ t: 0 }}; tl.fromTo(c, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: () => {{ const s = Math.floor(c.t), f = Math.floor((c.t % 1) * 30); $("#tc").textContent = "00:" + String(s).padStart(2, "0") + ":" + String(f).padStart(2, "0"); if (film) film.render(c.t); }} }}, 0); }})();')
a('gsap.set(["#a1", "#a2", "#a3", "#not", "#nn", "#p0", "#p1", "#p2", "#p3", "#p4", "#q0", "#q1", "#u1", "#u2", "#u3", "#u4", "#crar"], { opacity: 0 });')
# 1 hook
smear("#a1", 0.05); smear("#a2", W1("remembers") - 0.12, 520); smear("#a3", W1("your") - 0.1); sx(0, "boom_open", 0.32); sx(W1("first"), "impact", 0.42)
# 2 not / not / not
smear("#not", B[1] + 0.02); a(f'tl.to("#nn", {{ opacity: 1, duration: 0.2 }}, {B[1] + 0.2:.2f});')
NT = [W1("not", i) for i in range(3)] + [B[2]]
for i in range(3):
    t0, t1 = NT[i], NT[i + 1]
    a(f'tl.call(() => {{ $("#nn").textContent = "0{i + 1} / 03"; }}, null, {t0:.2f});')
    a(f'tl.fromTo("#not", {{ scale: 1 }}, {{ scale: 1.14, duration: 0.12, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }}, {t0:.2f});'); sx(t0, "impact", 0.36)
    a(f'tl.fromTo("#k{i}", {{ opacity: 0, x: {520 if i % 2 else -520}, scaleX: 1.8, filter: "blur(22px)" }}, {{ opacity: 1, x: 0, scaleX: 1, filter: "blur(0px)", duration: 0.42, ease: "expo.out" }}, {t0 + 0.08:.2f});'); sx(t0 + 0.08, "swipe1", 0.3)
    a(f'tl.to("#ks{i}", {{ scaleX: 1, duration: 0.22, ease: "expo.out" }}, {t1 - 0.5:.2f});'); sx(t1 - 0.5, "scratch", 0.36)
    if i < 2: a(f'tl.to("#k{i}", {{ opacity: 0, x: {-460 if i % 2 else 460}, scaleX: 1.8, filter: "blur(22px)", duration: 0.24, ease: "expo.in" }}, {t1 - 0.2:.2f});')
a(f'tl.fromTo("#ki0", {{ x: -10, y: 6, rotation: -2 }}, {{ x: 12, y: -8, rotation: 2.4, duration: 0.07, yoyo: true, repeat: {int((NT[1] - NT[0]) / 0.07)}, ease: "steps(1)" }}, {NT[0] + 0.3:.2f});')
a(f'tl.to("#scr", {{ strokeDashoffset: 0, duration: 0.8, ease: "power1.inOut" }}, {NT[1] + 0.3:.2f});')
a(f'tl.to("#crash", {{ strokeDashoffset: 0, duration: 0.6, ease: "power2.in" }}, {NT[2] + 0.3:.2f});'); a(f'tl.to("#crar", {{ opacity: 1, duration: 0.1 }}, {NT[2] + 0.88:.2f});'); sx(NT[2] + 0.88, "clunk", 0.4)
# 3 not the product, the price
a(f'tl.to("#p0", {{ opacity: 1, duration: 0.3 }}, {B[2] + 0.1:.2f});')
smear("#p1", W1("isnt") - 0.12); smear("#p2", W1("product") - 0.1, 520)
a(f'tl.to("#pst", {{ scaleX: 1, duration: 0.25, ease: "expo.out" }}, {W1("product") + 0.35:.2f});'); sx(W1("product") + 0.35, "scratch", 0.38)
a(f'tl.to(["#p1", "#p2"], {{ opacity: 0.32, duration: 0.3 }}, {W1("its") - 0.1:.2f});')
smear("#p3", W1("its") - 0.08); smear("#p4", W1("price") - 0.12, 520); sx(W1("price") - 0.12, "impact", 0.46); sx(W1("price"), "kaching", 0.34)
a(f'tl.fromTo("#tk", {{ opacity: 0, y: 60, rotation: -6 }}, {{ opacity: 1, y: 0, rotation: -3, duration: 0.5, ease: "back.out(2)" }}, {W1("price") + 0.15:.2f});')
# 4 try 100
t4 = B[3]
a(f'tl.to("#q0", {{ opacity: 1, duration: 0.3 }}, {t4 + 0.1:.2f});'); smear("#q1", t4 + 0.12)
d4 = W1("hundred") + 0.15 - (t4 + 0.3)
for n in range(100):
    a(f'tl.to("#c{n}", {{ backgroundColor: "{OR}", duration: 0.12 }}, {t4 + 0.3 + (n / 99) ** 1.6 * d4:.3f});')
a(f'(() => {{ const o = {{ v: 1 }}; tl.fromTo(o, {{ v: 1 }}, {{ v: 100, duration: {d4:.2f}, ease: "power2.in", immediateRender: false, onUpdate: () => {{ $("#qn").textContent = String(Math.round(o.v)).padStart(3, "0"); }} }}, {t4 + 0.3:.2f}); }})();'); sx(t4 + 0.3, "count_fast", 0.34); sx(t4 + 1.3, "count_fast", 0.34)
th = W1("hundred") + 0.15
a(f'tl.to(".cells i", {{ opacity: 0.22, duration: 0.3 }}, {th:.2f}); tl.to("#c99", {{ opacity: 1, backgroundColor: "{WH}", scale: 1.7, duration: 0.35, ease: "back.out(3)", boxShadow: "0 0 50px rgba(255,255,255,0.9)" }}, {th:.2f});'); sx(th, "impact", 0.46); sx(th, "shimmer", 0.34)
# 5 without try one
t5 = B[4]
a(f'tl.call(() => {{ $("#q0").textContent = "YOU CAN\\u2019T REACH IT WITHOUT"; }}, null, {t5:.2f}); tl.call(() => {{ $("#q0").textContent = "PEOPLE ONLY SEE"; }}, null, 0);')
a(f'tl.call(() => {{ $("#qn").textContent = "001"; }}, null, {W1("surviving") - 0.1:.2f});')
a(f'tl.fromTo("#q1", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.14, yoyo: true, repeat: 1, immediateRender: false }}, {W1("surviving") - 0.1:.2f});')
a(f'tl.to("#c0", {{ opacity: 1, backgroundColor: "{OR}", scale: 1.7, duration: 0.35, ease: "back.out(3)", boxShadow: "0 0 50px rgba(255,90,31,0.9)" }}, {W1("surviving") - 0.1:.2f});'); sx(W1("surviving") - 0.1, "ping", 0.42)
a(f'tl.to("#arw", {{ strokeDashoffset: 0, duration: 0.9, ease: "power3.inOut" }}, {W1("reach") - 0.1:.2f});'); sx(W1("reach") - 0.1, "swipe2", 0.3)
a(f'tl.fromTo("#c0", {{ rotation: 0 }}, {{ rotation: 90, duration: 0.5, ease: "back.out(2)", immediateRender: false }}, {W1("one", 1):.2f});'); sx(W1("one", 1), "impact", 0.4)
# 6 make it ugly / make it today
smear("#u1", W1("make") - 0.12); smear("#u2", W1("ugly") - 0.1, 520); sx(W1("ugly") - 0.1, "impact", 0.46)
a(f'tl.fromTo("#u2", {{ rotation: -3, skewX: -8 }}, {{ rotation: 3, skewX: 8, duration: 0.07, yoyo: true, repeat: {int((W1("make", 1) - W1("ugly")) / 0.07)}, ease: "steps(1)", immediateRender: false }}, {W1("ugly") + 0.3:.2f});')
out("#u1", W1("make", 1) - 0.3); out("#u2", W1("make", 1) - 0.26, -420)
smear("#u3", W1("make", 1) - 0.05); smear("#u4", W1("today") - 0.12, 520); sx(W1("today") - 0.12, "impact", 0.5); sx(W1("today") + 0.2, "shimmer", 0.4)

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
{chr(10).join(aud)}
</div>
<script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>
""")
print("duration", DUR, "sfx", len(SFX))
print({k: round(v, 2) for k, v in at.items()})
