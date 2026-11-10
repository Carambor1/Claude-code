#!/usr/bin/env python3
""""How Faceless TikTok Accounts Make Money" — ~68 s, native 9:16. Dotted grid, glowing white line icons, Sarah (confident).
A faceless figure + jar persist at the bottom; a 4-slot tracker on top; each method plays on the stage between. Run: python3 build.py"""
import json, re, subprocess

VO = json.load(open("vo.json"))
ORDER = ["r1"] + [f"r{i}" for i in range(3, 10)]
GAP = {"r1": 0.5, "r3": 0.4, "r4": 0.4, "r5": 0.4, "r6": 0.5, "r7": 0.5, "r8": 0.5}
T, at = 0.25, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.3)
DUR = round(T + 2.4, 2)
at["r2"] = round(at["r1"] + [t for x, t in VO["r1"]["words"] if x.startswith("Here")][0] - 0.15, 2)
W, H = 1080, 1920

def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)

S = 'fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
FIG = ('<svg viewBox="0 0 80 130"><circle cx="40" cy="24" r="20" fill="#fff"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="#fff"/>'
       '<g id="face"><circle cx="33" cy="21" r="2.6" fill="#000"/><circle cx="47" cy="21" r="2.6" fill="#000"/><path d="M32 30 q8 7 16 0" stroke="#000" stroke-width="2.4" fill="none" stroke-linecap="round"/></g></svg>')
FIGS = '<svg viewBox="0 0 80 130"><circle cx="40" cy="24" r="20" fill="#fff"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="#fff"/></svg>'
ICON = {
    "eye": f'<svg viewBox="0 0 160 100"><path d="M8 50 C40 8 120 8 152 50 C120 92 40 92 8 50 Z" {S}/><circle cx="80" cy="50" r="22" {S}/><circle cx="80" cy="50" r="8" fill="#fff"/></svg>',
    "link": f'<svg viewBox="0 0 140 140"><g transform="rotate(-45 70 70)"><rect x="6" y="50" width="72" height="40" rx="20" {S}/><rect x="62" y="50" width="72" height="40" rx="20" {S}/></g></svg>',
    "doc": f'<svg viewBox="0 0 110 140"><path d="M14 8 H72 L98 34 V132 H14 Z M72 8 V34 H98 M30 64 H82 M30 84 H82 M30 104 H62" {S}/></svg>',
    "deal": f'<svg viewBox="0 0 150 120"><path d="M14 46 H40 L104 14 V106 L40 74 H14 Z M40 74 L50 108 H66 L58 80 M120 40 C132 50 132 70 120 80" {S}/></svg>',
    "store": f'<svg viewBox="0 0 140 120"><path d="M14 52 V110 H126 V52 M8 50 L22 14 H118 L132 50 Z M8 50 a15.5 14 0 0 0 31 0 a15.5 14 0 0 0 31 0 a15.5 14 0 0 0 31 0 a15.5 14 0 0 0 31 0 M56 110 V78 H84 V110" {S}/></svg>',
    "phone": f'<svg viewBox="0 0 120 200"><rect x="6" y="6" width="108" height="188" rx="18" {S}/><path d="M48 22 H72" {S}/></svg>',
    "crown": f'<svg viewBox="0 0 140 110"><path d="M14 92 L22 30 L50 58 L70 18 L90 58 L118 30 L126 92 Z" {S}/></svg>',
    "cam": f'<svg viewBox="0 0 150 110"><rect x="8" y="22" width="96" height="70" rx="12" {S}/><path d="M104 48 L142 28 V86 L104 66" {S}/><path id="camS" d="M12 104 L138 8" {S} stroke-width="7"/></svg>',
    "mic": f'<svg viewBox="0 0 100 150"><rect x="30" y="8" width="40" height="78" rx="20" {S}/><path d="M14 66 a36 36 0 0 0 72 0 M50 102 V136 M28 136 H72" {S}/><path id="micS" d="M8 132 L92 14" {S} stroke-width="7"/></svg>',
    "box": f'<svg viewBox="0 0 120 110"><path d="M10 34 L60 10 L110 34 V84 L60 104 L10 84 Z M10 34 L60 56 L110 34 M60 56 V104" {S}/></svg>',
    "cart": f'<svg viewBox="0 0 140 110"><path d="M6 14 H28 L44 74 H112 L124 32 H34" {S}/><circle cx="54" cy="92" r="8" {S}/><circle cx="102" cy="92" r="8" {S}/></svg>',
    "truck": f'<svg viewBox="0 0 160 100"><path d="M8 20 H96 V74 H8 Z M96 40 H130 L150 58 V74 H96" {S}/><circle cx="40" cy="80" r="11" {S} fill="#000"/><circle cx="122" cy="80" r="11" {S} fill="#000"/></svg>',
    "bubble": f'<svg viewBox="0 0 130 120"><path d="M12 12 H118 V82 H62 L38 106 V82 H12 Z" {S}/><path d="M65 68 C40 50 46 30 65 42 C84 30 90 50 65 68 Z" fill="#fff"/></svg>',
    "grid": f'<svg viewBox="0 0 120 120"><rect x="10" y="10" width="100" height="100" rx="8" {S}/><path d="M10 44 H110 M50 44 V110" {S}/></svg>',
    "book": f'<svg viewBox="0 0 130 110"><path d="M65 22 C50 10 26 10 10 16 V96 C26 90 50 90 65 102 C80 90 104 90 120 96 V16 C104 10 80 10 65 22 Z M65 22 V102" {S}/></svg>',
    "sliders": f'<svg viewBox="0 0 120 120"><path d="M14 30 H106 M14 60 H106 M14 90 H106" {S}/><circle cx="40" cy="30" r="10" {S} fill="#000"/><circle cx="80" cy="60" r="10" {S} fill="#000"/><circle cx="52" cy="90" r="10" {S} fill="#000"/></svg>',
    "target": f'<svg viewBox="0 0 120 120"><circle cx="56" cy="64" r="48" {S}/><circle cx="56" cy="64" r="28" {S}/><circle cx="56" cy="64" r="8" fill="#fff"/><path id="arw" d="M56 64 L108 12 M90 12 H108 V30" {S}/></svg>',
    "cal": f'<svg viewBox="0 0 130 130"><rect x="10" y="22" width="110" height="98" rx="10" {S}/><path d="M10 50 H120 M40 10 V32 M90 10 V32" {S}/>' + "".join(f'<circle class="cd" cx="{36 + c * 29}" cy="{72 + r * 26}" r="7" fill="#fff"/>' for r in range(2) for c in range(3)) + '</svg>',
    "star": f'<svg viewBox="0 0 120 120"><path d="M60 10 L74 44 L110 47 L82 70 L91 106 L60 86 L29 106 L38 70 L10 47 L46 44 Z" {S}/></svg>',
    "jar": f'<svg viewBox="0 0 100 130"><path d="M22 10 H78 M28 10 V26 C14 34 12 46 12 60 V112 C12 120 18 124 26 124 H74 C82 124 88 120 88 112 V60 C88 46 86 34 72 26 V10" {S}/></svg>',
    "note": f'<svg viewBox="0 0 160 100"><rect x="6" y="14" width="148" height="72" rx="8" {S}/><circle cx="80" cy="50" r="18" {S}/><path d="M26 32 V68 M134 32 V68" {S}/></svg>',
    "heart": '<svg viewBox="0 0 100 90"><path d="M50 84 C6 52 14 10 50 30 C86 10 94 52 50 84 Z" fill="#fff"/></svg>',
}
def I(k, x, y, wd, h, id_="", extra="", cls=""):
    return f'<div class="abs {cls}" {"id=" + chr(34) + id_ + chr(34) if id_ else ""} style="left:{x}px;top:{y}px;width:{wd}px;height:{h}px;{extra}">{ICON[k]}</div>'
def SC(id, inner):
    return f'<div id="{id}" class="abs scn clip" data-start="0" data-duration="{DUR}" style="left:0;top:0;width:{W}px;height:{H}px">{inner}</div>'

JX, JY = 661, 1078          # coin landing spot (jar mouth)
COINS = []                   # (id, x, y)
def coins(pfx, n, x, y, glyph="€"):
    ids = []
    for i in range(n):
        cid = f"{pfx}{i}"; COINS.append(f'<div class="abs coin" id="{cid}" style="left:{x}px;top:{y}px">{glyph}</div>'); ids.append(cid)
    return ids

TR = ["eye", "link", "doc", "deal"]
SLX = [180, 380, 580, 780]
BARH = [90, 400, 500, 440]

RAIN = ((250, 300), (400, 230), (540, 190), (680, 240), (800, 310), (330, 180), (620, 170), (470, 280), (730, 200), (560, 300))
s1 = (I("cam", 110, 590, 170, 125, "cam") + I("mic", 830, 570, 110, 165, "mic")
      + '<div class="abs pill" id="nm" style="left:330px;top:960px;width:420px"><b>@</b><span class="nmw"><span id="nmt">username</span></span></div>'
      + "".join(f'<div class="abs coin rain" id="rn{i}" style="left:{x}px;top:{y}px">€</div>' for i, (x, y) in enumerate(RAIN)))
s2 = ('<div class="abs ctr t1" id="t1" style="top:590px">HOW FACELESS ACCOUNTS</div><div class="abs ctr t2" id="t2" style="top:650px">make money</div>'
      '<div class="abs ctr t3" id="t3" style="top:840px">4 WAYS</div>')
s3 = ('<div class="abs ctr mlabel">VIEWS</div>' + I("eye", 390, 490, 300, 188, "ey") + '<div class="abs ctr num" id="vw" style="top:694px">▶ 0</div>' + I("star", 730, 470, 110, 110, "st")
      + '<div class="abs" id="fol" style="left:120px;top:830px;width:400px;height:110px">'
      + "".join(f'<div class="abs" style="left:{i * 46}px;top:14px;width:50px;height:81px;opacity:{1 - i * 0.25}">{FIGS}</div>' for i in range(3))
      + '<div class="abs num" style="left:170px;top:8px">10K</div></div>'
      + '<div class="abs" id="vb" style="left:590px;top:846px;width:370px;height:90px"><div class="abs play"></div><div class="abs track"><i id="vbf"></i></div><div class="abs mark"></div><div class="abs mlab">1:00</div></div>')
c3 = coins("c3", 4, 518, 560)
s4 = ('<div class="abs ctr mlabel">AFFILIATE LINKS</div>' + I("link", 440, 470, 200, 200, "lk") + I("bubble", 110, 700, 160, 148, "bb") + I("box", 465, 706, 150, 138, "bx") + I("cart", 800, 710, 170, 134, "ct")
      + f'<svg class="abs" style="left:0;top:0;width:{W}px;height:{H}px" viewBox="0 0 {W} {H}"><path id="a1" d="M292 776 H440 M420 760 L440 776 L420 792" {S} stroke-dasharray="14 10"/><path id="a2" d="M636 776 H784 M764 760 L784 776 L764 792" {S}/></svg>'
     )
c4 = coins("c4", 3, 862, 640, "%")
s5 = ('<div class="abs ctr mlabel">DIGITAL PRODUCTS</div>' + I("doc", 455, 500, 170, 216, "d0") + '<div class="abs spk" id="dk" style="left:640px;top:470px">✦</div>'
      + I("grid", 150, 560, 180, 180, "p0") + I("book", 440, 570, 200, 169, "p1") + I("sliders", 750, 560, 180, 180, "p2")
      + "".join(I("doc", 470, 560, 140, 178, f"dc{i}") for i in range(3)) + I("doc", 470, 560, 140, 178, "d1"))
CPX = [(-270, 0), (270, 0), (0, 215)]
c5 = [coins(f"c5{i}", 1, 518 + dx, 630 + dy)[0] for i, (dx, dy) in enumerate(CPX)]
s6 = ('<div class="abs ctr mlabel">BRAND DEALS</div>' + I("deal", 430, 480, 220, 176, "mg") + I("phone", 450, 500, 180, 300, "ph") + I("crown", 485, 600, 110, 86, "cr")
      + I("store", 90, 600, 180, 154, "s0") + I("store", 810, 600, 180, 154, "s1b")
      + I("note", 240, 655, 100, 62, "n0") + I("note", 740, 655, 100, 62, "n1") + I("eye", 465, 836, 150, 94, "sey"))
c6 = coins("c6", 4, 518, 620)
s7 = "".join(f'<div class="abs bar {"dimb" if i == 0 else ""}" id="b{i}" style="left:{SLX[i] + 18}px;top:{920 - BARH[i]}px;height:{BARH[i]}px"></div>' for i in range(4)) + '<div class="abs base"></div>'
s8 = (I("target", 110, 560, 220, 220, "g0") + I("cal", 430, 560, 220, 220, "g1")
      + '<div class="abs" id="g2" style="left:750px;top:560px;width:220px;height:220px"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="6"/>'
        '<circle id="rg" cx="60" cy="60" r="50" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" transform="rotate(-90 60 60)" stroke-dasharray="314.2" stroke-dashoffset="314.2"/></svg><div class="abs n90" id="n90">0</div></div>'
      + f'<svg class="abs" style="left:0;top:0;width:{W}px;height:{H}px" viewBox="0 0 {W} {H}"><path id="k1" d="M346 670 H416" {S} stroke-dasharray="10 10"/><path id="k2" d="M666 670 H736" {S} stroke-dasharray="10 10"/></svg>'
      + '<div class="abs lab" id="l0" style="left:70px;top:810px;width:300px">ONE NICHE</div><div class="abs lab" id="l1" style="left:390px;top:810px;width:300px">EVERY DAY</div><div class="abs lab" id="l2" style="left:710px;top:810px;width:300px">90 DAYS</div>')
s9 = '<div class="abs qm" id="qm" style="left:730px;top:420px">?</div>'

body = [SC("s1", s1), SC("s2", s2), SC("s3", s3), SC("s4", s4), SC("s5", s5), SC("s6", s6), SC("s7", s7), SC("s8", s8), SC("s9", s9)]
persist = (
    f'<div id="trk" class="abs clip" data-start="0" data-duration="{DUR}" style="left:0;top:0;width:{W}px;height:{H}px">'
    + "".join(f'<div class="abs slot" id="sl{i}" style="left:{SLX[i]}px;top:300px"><div class="ic">{ICON[k]}</div></div>' for i, k in enumerate(TR)) + '</div>'
    f'<div id="base" class="abs clip" data-start="0" data-duration="{DUR}" style="left:0;top:0;width:{W}px;height:{H}px">'
    '<div class="abs ground" id="gr"></div>'
    f'<div class="abs" id="bank" style="left:640px;top:1092px;width:86px;height:112px">{ICON["jar"]}<div class="fill" id="jf"></div></div>'
    f'<div class="abs" id="you" style="left:470px;top:1010px;width:120px;height:195px"><div id="youi" style="width:100%;height:100%">{FIG}</div></div>'
    + "".join(COINS) + '</div>')

CSS = f"""
    #root {{ position: absolute; inset: 0; background-color: #000; background-image: radial-gradient(ellipse at 50% 38%, rgba(255,255,255,0.07), rgba(0,0,0,0) 62%), radial-gradient(rgba(255,255,255,0.16) 1.6px, transparent 1.8px); background-size: 100% 100%, 34px 34px; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
    #root .abs {{ position: absolute; }}
    #root .ctr {{ left: 0; width: {W}px; text-align: center; }}
    #root svg {{ width: 100%; height: 100%; display: block; overflow: visible; }}
    #root #lay {{ position: absolute; inset: 0; transform: translateY(60px) scale(1.14); transform-origin: 540px 300px; filter: drop-shadow(0 0 6px rgba(255,255,255,0.55)) drop-shadow(0 0 20px rgba(255,255,255,0.25)); }}
    #root .ground {{ left: 0; top: 1205px; width: {W}px; height: 0; border-top: 2px dashed rgba(255,255,255,0.3); }}
    #root .coin {{ color: #4ade80; width: 46px; height: 46px; border: 3px solid #4ade80; border-radius: 50%; background: #000; font-weight: 800; font-size: 26px; display: flex; align-items: center; justify-content: center; opacity: 0; }}
    #root .fill {{ position: absolute; left: 13%; right: 13%; bottom: 6%; height: 0; background: #4ade80; border-radius: 0 0 10px 10px; }}
    #root .slot {{ width: 120px; height: 120px; border: 3px solid #fff; border-radius: 50%; background: #000; display: flex; align-items: center; justify-content: center; opacity: 0; }}
    #root .slot .ic {{ width: 70px; height: 70px; display: flex; align-items: center; }}
    #root .slot svg [stroke] {{ stroke-width: 8; }}
    #root .mlabel {{ top: 454px; font-weight: 800; font-size: 34px; letter-spacing: 0.22em; color: #d8d8d8; }}
    #root .pill {{ height: 88px; border: 3px solid #fff; border-radius: 999px; display: flex; align-items: center; justify-content: center; gap: 10px; font-weight: 700; font-size: 46px; background: #000; }}
    #root .pill b {{ font-weight: 800; }}
    #root .nmw {{ display: inline-block; width: 230px; height: 58px; border-bottom: 3px dashed rgba(255,255,255,0.6); text-align: left; }}
    #root .t1 {{ font-weight: 800; font-size: 44px; letter-spacing: 0.16em; }}
    #root .t2 {{ font-family: "Playfair Display", "DejaVu Serif", Georgia, serif; font-style: italic; font-weight: 700; font-size: 140px; line-height: 1.1; }}
    #root .t3 {{ font-weight: 800; font-size: 40px; letter-spacing: 0.3em; color: #b8b8b8; }}
    #root .num {{ font-weight: 800; font-size: 84px; letter-spacing: -0.02em; white-space: nowrap; }}
    #root .play {{ left: 0; top: 16px; width: 0; height: 0; border-left: 44px solid #fff; border-top: 28px solid transparent; border-bottom: 28px solid transparent; }}
    #root .track {{ left: 70px; top: 34px; width: 290px; height: 20px; border: 3px solid #fff; border-radius: 10px; overflow: hidden; }}
    #root .track i {{ display: block; width: 100%; height: 100%; background: #fff; transform-origin: 0 50%; }}
    #root .mark {{ left: 244px; top: 18px; width: 0; height: 52px; border-left: 3px dashed #fff; }}
    #root .mlab {{ left: 204px; top: -30px; width: 80px; text-align: center; font-weight: 800; font-size: 32px; }}
    #root .spk {{ font-size: 60px; opacity: 0; }}
    #root .bar {{ width: 84px; background: #4ade80; border-radius: 14px 14px 0 0; transform-origin: 50% 100%; }}
    #root .bar.dimb {{ background: #000; border: 3px dashed rgba(255,255,255,0.7); border-bottom: 0; }}
    #root .base {{ left: 140px; top: 920px; width: 800px; height: 0; border-top: 3px solid #fff; }}
    #root .n90 {{ left: 0; top: 62px; width: 220px; text-align: center; font-weight: 800; font-size: 84px; letter-spacing: -0.03em; }}
    #root .lab {{ text-align: center; font-weight: 800; font-size: 32px; letter-spacing: 0.16em; color: #d0d0d0; }}
    #root .qm {{ font-weight: 900; font-size: 150px; opacity: 0; }}
    #root .fol {{ height: 96px; border: 3px solid #fff; border-radius: 999px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 46px; background: #000; }}
    #root .fol.on {{ background: #fff; color: #000; opacity: 0; }}
    #root .ht {{ opacity: 0; }}
    #root #s2, #root #s3, #root #s4, #root #s5, #root #s6, #root #s7, #root #s8, #root #s9, #root #gr, #root #bank {{ opacity: 0; }}
"""

J = []; a = J.append
def pop(sel, t, d=0.45, ease="back.out(2)", s0=0.5):
    a(f'tl.fromTo("{sel}", {{ opacity: 0, scale: {s0} }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "{ease}" }}, {t:.2f});')
def fade(sel, t, o=0, d=0.4):
    a(f'tl.to("{sel}", {{ opacity: {o}, duration: {d}, ease: "power2.inOut" }}, {t:.2f});')
def draw(sel, t, length, d=0.5, dash=None):
    a(f'tl.fromTo("{sel}", {{ strokeDasharray: "{length} {length}", strokeDashoffset: {length} }}, {{ strokeDashoffset: 0, duration: {d}, ease: "power2.out" }}, {t:.2f});')
FILL = [0]
def pay(ids, t, pct, stagger=0.13):
    """coins fly from where they sit into the jar; jar fills to pct"""
    for i, cid in enumerate(ids):
        t0 = t + i * stagger
        a(f'(() => {{ const e = $("#{cid}"); const dx = {JX} - parseFloat(e.style.left), dy = {JY} - parseFloat(e.style.top);'
          f' tl.fromTo(e, {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {t0:.2f});'
          f' tl.fromTo(e, {{ x: 0 }}, {{ x: dx, duration: 0.75, ease: "power1.inOut", immediateRender: false }}, {t0 + 0.2:.2f});'
          f' tl.fromTo(e, {{ y: 0 }}, {{ y: dy, duration: 0.75, ease: "back.in(1.4)", immediateRender: false }}, {t0 + 0.2:.2f});'
          f' tl.to(e, {{ opacity: 0, duration: 0.12 }}, {t0 + 0.9:.2f}); }})();')
    a(f'tl.fromTo("#jf", {{ height: "{FILL[0]}%" }}, {{ height: "{pct}%", duration: 0.6, ease: "power2.out", immediateRender: {"true" if FILL[0] == 0 else "false"} }}, {t + 0.95:.2f});')
    a(f'tl.fromTo("#bank", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.16, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {t + 0.95:.2f});')
    FILL[0] = pct
    return t + 0.95

SFX = []; sx = lambda t, f, v=0.35: SFX.append((round(t, 2), f, v))

# ---- scene cross-fades (stage scenes) with a gentle drift
SC_T = [("s1", 0), ("s2", at["r2"]), ("s3", at["r3"]), ("s4", at["r4"]), ("s5", at["r5"]), ("s6", at["r6"]), ("s7", at["r7"]), ("s8", at["r8"]), ("s9", at["r9"])]
for i, (sid, t) in enumerate(SC_T):
    nxt = SC_T[i + 1][1] if i + 1 < len(SC_T) else DUR
    if i: a(f'tl.fromTo("#{sid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power2.inOut" }}, {t - 0.2:.2f});')
    a(f'tl.fromTo("#{sid}", {{ scale: 0.985 }}, {{ scale: 1.02, duration: {nxt - t + 0.2:.2f}, ease: "none", immediateRender: false }}, {max(0, t - 0.2):.2f});')
    if i + 1 < len(SC_T): a(f'tl.to("#{sid}", {{ opacity: 0, duration: 0.5, ease: "power2.inOut" }}, {nxt - 0.45:.2f});')

# ---- persistent figure: big hero -> small "you" -> hidden for the chart -> hero again
BIG = "x: 10, y: -447, scale: 2.6"
a(f'tl.fromTo("#you", {{ {BIG} }}, {{ x: 0, y: 0, scale: 1, duration: 1.0, ease: "power3.inOut" }}, {at["r2"] - 0.35:.2f});')
a(f'tl.fromTo("#you", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.5, ease: "power2.inOut", immediateRender: false }}, {at["r7"] - 0.3:.2f});')
a(f'tl.fromTo("#you", {{ x: 0, y: 0, scale: 1 }}, {{ {BIG}, duration: 0.05, immediateRender: false }}, {at["r9"] - 0.6:.2f});')
a(f'tl.fromTo("#you", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.7, ease: "power2.out", immediateRender: false }}, {at["r9"] - 0.4:.2f});')
a(f'tl.fromTo("#youi", {{ scale: 0.86 }}, {{ scale: 1, duration: 0.9, ease: "power3.out", immediateRender: false }}, {at["r9"] - 0.4:.2f});')
a(f'tl.fromTo(["#gr", "#bank"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, {at["r2"] + 0.3:.2f});')
fade('#gr', at["r7"] - 0.3); fade('#bank', at["r7"] - 0.3)

# ---- S1 hook
e_face, e_paid = w("r1", "face"), w("r1", "paid"); e_name, e_voice = e_face + 0.3, e_face + 0.5
a('tl.fromTo("#youi", { scale: 0.9 }, { scale: 1, duration: 0.8, ease: "power3.out" }, 0);')
for sel, t in (("#cam", 0.1), ("#mic", 0.22), ("#nm", 0.34)): pop(sel, t)
a('gsap.set(["#camS", "#micS"], { strokeDasharray: "170 170", strokeDashoffset: 170 });')
draw("#camS", e_face - 0.2, 170, 0.35); a(f'tl.to("#face", {{ opacity: 0, duration: 0.35 }}, {e_face - 0.15:.2f});')
a(f'tl.fromTo("#youi", {{ scale: 1 }}, {{ scale: 1.05, duration: 0.14, yoyo: true, repeat: 1, immediateRender: false }}, {e_face - 0.1:.2f});')
a(f'tl.to("#nmt", {{ opacity: 0, x: -24, duration: 0.4, ease: "power2.in" }}, {e_name - 0.15:.2f});')
draw("#micS", e_voice - 0.1, 170, 0.35)
for sel in ("#cam", "#mic", "#nm"): fade(sel, e_paid - 0.7, 0.3, 0.4)
for i, (rx, ry) in enumerate(RAIN):
    t0 = e_paid - 0.6 + i * 0.13
    a(f'tl.fromTo("#rn{i}", {{ y: -80, x: 0, scale: 1.5 }}, {{ y: {690 - ry}, x: {(517 - rx) * 0.85:.0f}, scale: 0.7, duration: 0.85, ease: "power2.in" }}, {t0:.2f});')
    a(f'tl.fromTo("#rn{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12 }}, {t0:.2f});')
    a(f'tl.fromTo("#rn{i}", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.1, immediateRender: false }}, {t0 + 0.86:.2f});')
a(f'tl.fromTo("#youi", {{ scale: 1 }}, {{ scale: 1.07, duration: 0.2, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, {e_paid + 0.15:.2f});')
sx(0, "boom_open", 0.3); sx(e_face - 0.2, "scratch", 0.3); sx(e_name - 0.15, "swipe1", 0.28); sx(e_voice - 0.1, "scratch", 0.3)
sx(e_paid - 0.4, "coin_jar", 0.45); sx(e_paid + 0.1, "kaching", 0.4)

# ---- S2 title + tracker appears
sx(at["r2"] - 0.35, "zoom_whoosh", 0.3)
a(f'tl.fromTo("#t1", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }}, {at["r2"]:.2f});')
a(f'tl.fromTo("#t2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {at["r2"] + 0.25:.2f});')
a(f'tl.fromTo("#t3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {at["r2"] + 0.5:.2f});')
for i in range(4):
    t0 = at["r2"] + 0.45 + i * 0.14
    a(f'tl.fromTo("#sl{i}", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 0.35, scale: 1, duration: 0.4, ease: "back.out(2.2)" }}, {t0:.2f});'); sx(t0, "pop", 0.25)
# tracker states per method
for i, k in enumerate(("r3", "r4", "r5", "r6")):
    a(f'tl.to("#sl{i}", {{ opacity: 1, scale: 1.2, duration: 0.45, ease: "back.out(2)" }}, {at[k] - 0.1:.2f});'); sx(at[k] - 0.1, "up1" if i % 2 == 0 else "up2", 0.3)
    end = at[("r4", "r5", "r6", "r7")[i]] - 0.3
    a(f'tl.to("#sl{i}", {{ opacity: 0.6, scale: 1, duration: 0.4, ease: "power2.inOut" }}, {end:.2f});')

# ---- S3 views
e = {k: w("r3", k) for k in ("views", "ten", "pays", "videos", "minute")}; e["creator"] = w("r3", "tiktok")
pop("#ey", e["views"] - 0.1); sx(e["views"] - 0.1, "pop")
a(f'tl.fromTo("#vw", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {e["views"] + 0.2:.2f});')
a(f'(() => {{ const o = {{ v: 0 }}; const f = (n) => n >= 1e6 ? (n / 1e6).toFixed(1) + "M" : n >= 1e3 ? Math.round(n / 1e3) + "K" : String(Math.round(n));'
  f' tl.fromTo(o, {{ v: 0 }}, {{ v: 1200000, duration: {e["creator"] - e["views"] - 0.2:.2f}, ease: "power2.in", immediateRender: false, onUpdate: () => {{ $("#vw").textContent = "▶ " + f(o.v); }} }}, {e["views"] + 0.2:.2f}); }})();')
sx(e["views"] + 0.3, "count_fast", 0.25)
a(f'tl.fromTo("#fol", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, {e["ten"] - 0.1:.2f});'); sx(e["ten"] - 0.1, "ping", 0.3)
pop("#st", e["creator"] - 0.05); sx(e["creator"] - 0.05, "shimmer", 0.3)
a(f'tl.fromTo("#st", {{ rotation: -20 }}, {{ rotation: 0, duration: 0.6, ease: "back.out(2)" }}, {e["creator"] - 0.05:.2f});')
tj = pay(c3, e["pays"] - 0.15, 25); sx(tj - 0.1, "coin_jar", 0.45)
a(f'tl.fromTo("#vb", {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, {e["videos"] - 0.1:.2f});')
a(f'tl.fromTo("#vbf", {{ scaleX: 0 }}, {{ scaleX: 0.86, duration: {e["minute"] + 0.4 - e["videos"]:.2f}, ease: "none" }}, {e["videos"]:.2f});'); sx(e["minute"] - 0.1, "ui_tick2", 0.4)

# ---- S4 affiliate
e = {k: w("r4", k) for k in ("affiliate", "recommend", "product", "someone", "buys", "commission")}
pop("#lk", e["affiliate"] - 0.1); sx(e["affiliate"] - 0.1, "pop")
a(f'tl.to("#lk", {{ scale: 0.55, y: 10, duration: 0.5, ease: "power3.inOut" }}, {e["recommend"] - 0.3:.2f});')
a('gsap.set(["#bb", "#bx", "#ct", "#a1", "#a2"], { opacity: 0 });')
pop("#bb", e["recommend"] - 0.05); sx(e["recommend"] - 0.05, "pop", 0.3)
a(f'tl.to("#a1", {{ opacity: 1, duration: 0.3 }}, {e["product"] - 0.25:.2f});'); pop("#bx", e["product"] - 0.1); sx(e["product"] - 0.1, "pop", 0.3)
pop("#ct", e["someone"]); sx(e["someone"], "swipe2", 0.28)
a(f'tl.to("#a2", {{ opacity: 1, duration: 0.3 }}, {e["buys"] - 0.1:.2f});')
a(f'tl.fromTo("#ct", {{ scale: 1 }}, {{ scale: 1.14, duration: 0.16, yoyo: true, repeat: 1, immediateRender: false }}, {e["buys"]:.2f});'); sx(e["buys"], "kaching", 0.32)
tj = pay(c4, e["commission"] - 0.1, 50); sx(tj - 0.1, "coin_jar", 0.45)
# ---- S5 digital products
e = {k: w("r5", k) for k in ("digital", "once")}
ag = [w("r5", "again", i) for i in range(3)]
a('gsap.set(["#p0", "#p1", "#p2", "#d1", "#dc0", "#dc1", "#dc2"], { opacity: 0 });')
pop("#d0", e["digital"] - 0.1); sx(e["digital"] - 0.1, "pop")
a(f'tl.fromTo("#dk", {{ opacity: 0, scale: 0.3, rotation: -40 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }}, {e["digital"] + 0.15:.2f});'); sx(e["digital"] + 0.15, "shimmer", 0.28)
a(f'tl.to(["#d0", "#dk"], {{ opacity: 0, scale: 0.7, duration: 0.35, ease: "power2.inOut" }}, {e["once"] - 0.6:.2f});')
pop("#d1", e["once"] - 0.3, 0.5, "back.out(2.4)"); sx(e["once"] - 0.3, "impact", 0.3)
fl = 50
for i, (dx, dy) in enumerate(CPX):
    a(f'tl.fromTo("#dc{i}", {{ opacity: 0, x: 0, y: 0, scale: 1 }}, {{ opacity: 0.9, x: {dx}, y: {dy}, scale: 0.72, duration: 0.45, ease: "back.out(1.5)" }}, {ag[i] - 0.15:.2f});'); sx(ag[i] - 0.15, "swipe2" if i % 2 else "swipe1", 0.25)
    a(f'tl.fromTo("#d1", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.12, yoyo: true, repeat: 1, immediateRender: false }}, {ag[i] - 0.15:.2f});')
    fl += 8 if i < 2 else 9
    tj = pay([c5[i]], ag[i] + 0.2, fl); sx(ag[i] + 0.25, "kaching", 0.28)

# ---- S6 brand deals
e = {k: w("r6", k) for k in ("brand", "brands", "pay", "seen")}; e["page"] = w("r6", "own"); e["owns"] = w("r6", "niche")
a('gsap.set(["#ph", "#cr", "#s0", "#s1b", "#n0", "#n1", "#sey"], { opacity: 0 });')
pop("#mg", e["brand"] - 0.1); sx(e["brand"] - 0.1, "pop")
a(f'tl.fromTo("#mg", {{ rotation: -12 }}, {{ rotation: 0, duration: 0.6, ease: "back.out(2.5)" }}, {e["brand"] - 0.1:.2f});')
a(f'tl.to("#mg", {{ opacity: 0, scale: 0.6, duration: 0.4, ease: "power2.inOut" }}, {e["page"] - 0.55:.2f});')
pop("#ph", e["page"] - 0.2, 0.5); sx(e["page"] - 0.2, "swipe1", 0.26)
a(f'tl.fromTo("#cr", {{ opacity: 0, y: -120 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "bounce.out" }}, {e["owns"] - 0.1:.2f});'); sx(e["owns"] + 0.1, "ui_tick2", 0.4)
pop("#s0", e["brands"] - 0.15); pop("#s1b", e["brands"]); sx(e["brands"] - 0.15, "pop", 0.3); sx(e["brands"], "pop", 0.3)
for i, dx in enumerate((190, -190)):
    a(f'tl.fromTo("#n{i}", {{ opacity: 0, x: 0, scale: 1 }}, {{ opacity: 1, x: {dx * 0.2}, duration: 0.2 }}, {e["pay"] - 0.1 + i * 0.15:.2f});')
    a(f'tl.to("#n{i}", {{ x: {dx}, scale: 0.5, opacity: 0, duration: 0.6, ease: "power2.in" }}, {e["pay"] + 0.1 + i * 0.15:.2f});')
a(f'tl.fromTo("#ph", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.15, yoyo: true, repeat: 3, immediateRender: false }}, {e["pay"] + 0.6:.2f});'); sx(e["pay"] + 0.6, "kaching", 0.32)
pop("#sey", e["seen"] - 0.05, 0.4)
tj = pay(c6, e["seen"] + 0.35, 100); sx(tj - 0.1, "coin_jar", 0.45)

# ---- S7 twist: tracker drops down and becomes the chart
e = {k: w("r7", k) for k in ("views", "least", "real", "sell")}
sx(at["r7"] - 0.1, "heartbeat", 0.4)
for i in range(4):
    a(f'tl.to("#sl{i}", {{ y: 640, opacity: 1, scale: 1, duration: 0.9, ease: "power3.inOut" }}, {at["r7"] - 0.1 + i * 0.07:.2f});')
sx(at["r7"], "zoom_whoosh", 0.28)
a('gsap.set(["#b0", "#b1", "#b2", "#b3"], { scaleY: 0 });')
a(f'tl.to("#b0", {{ scaleY: 1, duration: 0.6, ease: "power2.out" }}, {e["views"] + 0.5:.2f});'); sx(e["views"] - 0.1, "up1", 0.3)
a(f'tl.to("#sl0", {{ opacity: 0.45, duration: 0.4 }}, {e["least"]:.2f});'); sx(e["least"], "ui_tick2", 0.4)
for i in (1, 2, 3):
    a(f'tl.to("#b{i}", {{ scaleY: 1, duration: 0.9, ease: "back.out(1.3)" }}, {e["real"] - 0.1 + (i - 1) * 0.16:.2f});')
    a(f'tl.to("#sl{i}", {{ scale: 1.15, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {e["sell"] - 0.05 + (i - 1) * 0.08:.2f});')
sx(e["real"] - 0.1, "riser", 0.25); sx(e["sell"] - 0.05, "impact", 0.42)
for i in range(4): a(f'tl.to("#sl{i}", {{ opacity: 0, duration: 0.4, ease: "power2.in" }}, {at["r8"] - 0.5:.2f});')

# ---- S8 method
e = {k: w("r8", k) for k in ("pick", "post", "every", "ninety")}
a('gsap.set(["#g0", "#g1", "#g2", "#k1", "#k2", "#l0", "#l1", "#l2", "#g1 .cd"], { opacity: 0 });')
pop("#g0", e["pick"] - 0.15); sx(e["pick"] - 0.15, "pop")
a(f'tl.fromTo("#arw", {{ x: 60, y: -60, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.35, ease: "power3.in" }}, {e["pick"] + 0.25:.2f});'); sx(e["pick"] + 0.55, "impact", 0.3)
a(f'tl.to("#l0", {{ opacity: 1, duration: 0.3 }}, {e["pick"] + 0.3:.2f});')
a(f'tl.to("#k1", {{ opacity: 1, duration: 0.3 }}, {e["post"] - 0.4:.2f});'); pop("#g1", e["post"] - 0.15); sx(e["post"] - 0.15, "pop")
a(f'tl.to("#l1", {{ opacity: 1, duration: 0.3 }}, {e["post"] + 0.3:.2f});')
for i in range(6):
    t0 = e["every"] - 0.1 + i * 0.12
    a(f'tl.fromTo($$("#g1 .cd")[{i}], {{ opacity: 0, scale: 0, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(3)" }}, {t0:.2f});'); sx(t0, "ui_tick2", 0.3)
a(f'tl.to("#k2", {{ opacity: 1, duration: 0.3 }}, {e["ninety"] - 0.45:.2f});'); pop("#g2", e["ninety"] - 0.2); sx(e["ninety"] - 0.2, "riser", 0.25)
a(f'tl.fromTo("#rg", {{ strokeDashoffset: 314.2 }}, {{ strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut" }}, {e["ninety"] - 0.1:.2f});')
a(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 90, duration: 1.1, ease: "power2.inOut", immediateRender: false, onUpdate: () => {{ $("#n90").textContent = Math.round(o.v); }} }}, {e["ninety"] - 0.1:.2f}); }})();')
a(f'tl.to("#l2", {{ opacity: 1, duration: 0.3 }}, {e["ninety"] + 0.4:.2f});'); sx(e["ninety"] + 0.95, "impact", 0.35)

# ---- S9 end
sx(at["r9"] - 0.45, "zoom_whoosh", 0.28)
a(f'tl.fromTo("#qm", {{ opacity: 0, scale: 0.3, rotation: -25 }}, {{ opacity: 1, scale: 1, rotation: 8, duration: 0.5, ease: "back.out(2.5)" }}, {at["r9"] + 0.1:.2f});')
for i in range(4):
    t0 = at["r9"] + 0.05 + i * 0.12
    a(f'tl.fromTo("#sl{i}", {{ y: 760, opacity: 0, scale: 0.4 }}, {{ y: 690, opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)", immediateRender: false }}, {t0:.2f});'); sx(t0, "pop", 0.28)
for n in range(8):
    i = n % 4; t0 = at["r9"] + 0.9 + n * 0.3
    a(f'tl.fromTo("#sl{i}", {{ scale: 1 }}, {{ scale: 1.28, duration: 0.15, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {t0:.2f});'); sx(t0, "ui_tick2", 0.3)
sx(at["r9"] + 0.1, "ping", 0.35)

open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    <div id="lay">
    {chr(10).join("    " + b for b in body)}
    {persist}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const R = document.querySelector('[data-composition-id="w"]') || document;
    const $ = (s) => R.querySelector(s), $$ = (s) => R.querySelectorAll(s);
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
    #root .cap {{ left: 90px; width: 900px; top: 1440px; text-align: center; font-weight: 800; font-size: 58px; line-height: 1.15; color: #fff; }}
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
