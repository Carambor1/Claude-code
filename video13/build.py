#!/usr/bin/env python3
""""How Faceless Accounts Make Money" v3 — story cut, native 9:16. One faceless video hits 1M views -> what it pays ->
why pages sell instead -> example math -> niches -> question. Dotted grid, glowing line icons, green = money. Run: python3 build.py"""
import json, re, subprocess, os

TEMPO = 1.06
VO = json.load(open("vo.json"))
ORDER = ["r1", "r2", "r3", "r4", "r5", "r6", "r8", "r9"]
for k in ORDER:
    if not os.path.exists(f"assets/vo/{k}_t.mp3"):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"assets/vo/{k}.mp3", "-af", f"atempo={TEMPO}", f"assets/vo/{k}_t.mp3"], check=True)
    VO[k]["dur"] /= TEMPO; VO[k]["words"] = [(x, t / TEMPO) for x, t in VO[k]["words"]]
GAP = {"r1": 0.35, "r2": 0.4, "r3": 0.35, "r4": 0.3, "r5": 0.35, "r6": 0.45, "r8": 0.4}
T, at = 0.2, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.3)
DUR = round(T + 2.3, 2)
W, H = 1080, 1920
G = "#4ade80"

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


ICON.update({
    "globe": f'<svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="50" {S}/><ellipse cx="60" cy="60" rx="22" ry="50" {S}/><path d="M10 60 H110 M18 34 H102 M18 86 H102" {S}/></svg>',
    "hour": f'<svg viewBox="0 0 120 120"><path d="M26 10 H94 M26 110 H94 M34 10 C34 48 86 72 86 110 M86 10 C86 48 34 72 34 110" {S}/></svg>',
    "spark": f'<svg viewBox="0 0 120 120"><path d="M52 14 C56 48 68 60 102 64 C68 68 56 80 52 114 C48 80 36 68 2 64 C36 60 48 48 52 14 Z" {S}/><path d="M98 8 V32 M86 20 H110" {S}/></svg>',
    "flame": f'<svg viewBox="0 0 120 120"><path d="M60 112 C28 112 20 82 36 60 C42 70 50 70 50 58 C50 36 62 26 66 8 C90 30 102 58 94 84 C90 100 78 112 60 112 Z" {S}/></svg>',
})
JX, JY = 661, 1078
COINS = []
def coins(pfx, n, x, y, glyph="$"):
    ids = []
    for i in range(n):
        cid = f"{pfx}{i}"; COINS.append(f'<div class="abs coin" id="{cid}" style="left:{x}px;top:{y}px">{glyph}</div>'); ids.append(cid)
    return ids

HEARTS = ((170, 960, 96), (820, 980, 110), (260, 1000, 70), (770, 950, 84), (90, 990, 80), (900, 1000, 70), (300, 960, 90), (720, 990, 76), (190, 1000, 64), (850, 960, 90))
s1 = ('<div class="abs ctr vnum" id="vw">▶ 0</div><div class="abs ctr vlab" id="vl">VIEWS</div>'
      + I("cam", 110, 610, 150, 110, "cam") + I("mic", 840, 590, 96, 144, "mic")
      + "".join(f'<div class="abs ht" id="h{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{int(s * 0.9)}px">{ICON["heart"]}</div>' for i, (x, y, s) in enumerate(HEARTS))
      + '<div class="abs qd" id="qd" style="left:760px;top:420px">$?</div>')
s2 = (I("eye", 330, 462, 140, 88, "e2") + '<div class="abs num" id="m2" style="left:490px;top:456px">1M</div>'
      + f'<svg class="abs" style="left:0;top:0;width:{W}px;height:{H}px" viewBox="0 0 {W} {H}"><path id="ar2" d="M540 578 V664 M518 642 L540 664 L562 642" {S}/></svg>'
      + '<div class="abs ctr amt" id="am" style="top:680px">$400 – $1,000</div><div class="abs ctr tiny" id="am2" style="top:806px">CREATOR-REPORTED · NOT OFFICIAL</div>'
      + '<div class="abs chip" id="ch0" style="left:95px;top:880px"><div class="ci" style="width:44px;height:72px">' + FIGS + '</div>10K</div>'
      + '<div class="abs chip" id="ch1" style="left:415px;top:880px"><div class="ci" style="width:62px;height:62px">' + ICON["globe"] + '</div><span class="ck">✓</span></div>'
      + '<div class="abs chip" id="ch2" style="left:735px;top:880px"><div class="ci pl"></div>1:00+</div>')
c2 = coins("c2", 3, 518, 720)
s3 = (I("eye", 390, 560, 300, 188, "e3")
      + f'<svg class="abs" style="left:0;top:0;width:{W}px;height:{H}px" viewBox="0 0 {W} {H}"><path id="e3s" d="M380 770 L700 540" {S} stroke-width="9"/></svg>'
      + I("cart", 400, 540, 280, 220, "ct3") + '<div class="abs coin xl" id="cn3" style="left:640px;top:470px">$</div>')
s4 = ('<div class="abs ctr mlabel">AFFILIATE LINK</div>' + I("link", 465, 500, 150, 150, "lk") + I("bubble", 110, 720, 160, 148, "bb") + I("box", 465, 726, 150, 138, "bx") + I("cart", 800, 730, 170, 134, "ct")
      + f'<svg class="abs" style="left:0;top:0;width:{W}px;height:{H}px" viewBox="0 0 {W} {H}"><path id="a1" d="M292 796 H440 M420 780 L440 796 L420 812" {S} stroke-dasharray="14 10"/><path id="a2" d="M636 796 H784 M764 780 L784 796 L764 812" {S}/></svg>')
c4 = coins("c4", 3, 862, 660, "%")
s5 = ('<div class="abs ctr mlabel">DIGITAL PRODUCT</div>' + "".join(I("doc", 460, 560, 160, 204, f"dc{i}") for i in range(3)) + I("doc", 460, 560, 160, 204, "d1")
      + '<div class="abs spk" id="dk" style="left:640px;top:520px">✦</div>')
CPX = [(-280, 30), (280, 30), (0, 190)]
c5 = [coins(f"c5{i}", 1, 518 + dx, 640 + dy)[0] for i, (dx, dy) in enumerate(CPX)]
s6 = ('<div class="abs ctr mlabel" id="ml6">EXAMPLE MATH</div>'
      + '<div class="abs" id="row6" style="left:0;top:0;width:1080px;height:1000px">'
      + "".join(f'<div class="abs pp" id="pp{i}" style="left:{148 + i * 80}px;top:520px;width:50px;height:81px">{FIGS}</div>' for i in range(10))
      + '<div class="abs ctr num sm" id="in6" style="top:622px">1 in 1,000</div>'
      + I("doc", 330, 716, 84, 107, "d6") + '<div class="abs num sm" id="x6" style="left:440px;top:728px">× <span class="g">$20</span></div></div>'
      + '<div class="abs ctr amt big" id="tot">$0</div>'
      + '<div id="cmp" class="abs" style="left:0;top:0;width:1080px;height:1000px"><div class="abs base" style="left:240px;top:800px;width:600px"></div>'
      + '<div class="abs bar dimb" id="q0" style="left:330px;top:782px;height:18px;width:110px"></div><div class="abs bar" id="q1" style="left:640px;top:440px;height:360px;width:110px"></div>'
      + I("eye", 335, 690, 100, 63, "qe") + '</div>')
c6 = coins("c6", 6, 518, 800)
NICHE = (("note", "MONEY FACTS", 200, 125), ("hour", "HISTORY", 165, 165), ("spark", "AI TOOLS", 165, 165), ("flame", "MOTIVATION", 165, 165))
NPOS = ((310, 490), (770, 490), (310, 750), (770, 750))
s7 = '<div class="abs ctr mlabel">WORKS WITHOUT A FACE</div>' + "".join(
    f'<div class="abs tile" id="n{i}" style="left:{x - 170}px;top:{y}px"><div class="ti" style="width:{iw}px;height:{ih}px">{ICON[k]}</div><div class="tl">{lab}</div></div>'
    for i, ((k, lab, iw, ih), (x, y)) in enumerate(zip(NICHE, NPOS)))
s8 = '<div class="abs qm" id="qm" style="left:730px;top:420px">?</div>'
SLX = [180, 380, 580, 780]
body = [SC("s1", s1), SC("s2", s2), SC("s3", s3), SC("s4", s4), SC("s5", s5), SC("s6", s6), SC("s7", s7), SC("s8", s8)]
persist = (
    f'<div id="trk" class="abs clip" data-start="0" data-duration="{DUR}" style="left:0;top:0;width:{W}px;height:{H}px">'
    + "".join(f'<div class="abs slot" id="sl{i}" style="left:{SLX[i]}px;top:990px"><div class="ic">{ICON[k[0]]}</div></div>' for i, k in enumerate(NICHE)) + '</div>'
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
    #root #face {{ display: none; }}
    #root .g {{ color: {G}; }}
    #root .ground {{ left: 0; top: 1205px; width: {W}px; height: 0; border-top: 2px dashed rgba(255,255,255,0.3); }}
    #root .coin {{ color: {G}; width: 46px; height: 46px; border: 3px solid {G}; border-radius: 50%; background: #000; font-weight: 800; font-size: 26px; display: flex; align-items: center; justify-content: center; opacity: 0; }}
    #root .coin.xl {{ width: 110px; height: 110px; font-size: 64px; border-width: 5px; }}
    #root .fill {{ position: absolute; left: 13%; right: 13%; bottom: 6%; height: 0; background: {G}; border-radius: 0 0 10px 10px; }}
    #root .slot {{ width: 120px; height: 120px; border: 3px solid #fff; border-radius: 50%; background: #000; display: flex; align-items: center; justify-content: center; opacity: 0; }}
    #root .slot .ic {{ width: 70px; height: 70px; display: flex; align-items: center; }}
    #root .slot svg [stroke] {{ stroke-width: 8; }}
    #root .mlabel {{ top: 440px; font-weight: 800; font-size: 34px; letter-spacing: 0.22em; color: #d8d8d8; }}
    #root .vnum {{ top: 250px; font-weight: 900; font-size: 104px; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }}
    #root .vlab {{ top: 372px; font-weight: 800; font-size: 32px; letter-spacing: 0.4em; color: #c8c8c8; }}
    #root .qd {{ font-weight: 900; font-size: 130px; color: {G}; opacity: 0; }}
    #root .qm {{ font-weight: 900; font-size: 150px; opacity: 0; }}
    #root .num {{ font-weight: 800; font-size: 84px; letter-spacing: -0.02em; white-space: nowrap; }}
    #root .num.sm {{ font-size: 68px; }}
    #root .amt {{ font-weight: 900; font-size: 104px; letter-spacing: -0.03em; color: {G}; white-space: nowrap; }}
    #root .amt.big {{ top: 836px; font-size: 132px; opacity: 0; font-variant-numeric: tabular-nums; }}
    #root .tiny {{ font-weight: 700; font-size: 28px; letter-spacing: 0.16em; color: #a8a8a8; }}
    #root .chip {{ width: 250px; height: 92px; border: 3px solid #fff; border-radius: 999px; background: #000; display: flex; align-items: center; justify-content: center; gap: 14px; font-weight: 800; font-size: 44px; opacity: 0; }}
    #root .chip .ci {{ display: flex; align-items: center; }}
    #root .chip .pl {{ width: 0; height: 0; border-left: 34px solid #fff; border-top: 22px solid transparent; border-bottom: 22px solid transparent; }}
    #root .chip .ck {{ color: {G}; font-size: 52px; }}
    #root .spk {{ font-size: 60px; opacity: 0; }}
    #root .pp {{ opacity: 0.3; }}
    #root .bar {{ background: {G}; border-radius: 14px 14px 0 0; transform-origin: 50% 100%; }}
    #root .bar.dimb {{ background: #fff; border-radius: 6px 6px 0 0; }}
    #root .base {{ height: 0; border-top: 3px solid #fff; }}
    #root .tile {{ width: 340px; display: flex; flex-direction: column; align-items: center; gap: 18px; opacity: 0; }}
    #root .tile .ti {{ display: flex; align-items: center; height: 168px; }}
    #root .tile .tl {{ font-weight: 800; font-size: 36px; letter-spacing: 0.16em; }}
    #root .ht {{ opacity: 0; }}
    #root #s2, #root #s3, #root #s4, #root #s5, #root #s6, #root #s7, #root #s8, #root #gr, #root #bank, #root #cmp {{ opacity: 0; }}
"""

J = []; a = J.append
def pop(sel, t, d=0.45, ease="back.out(2)", s0=0.5):
    a(f'tl.fromTo("{sel}", {{ opacity: 0, scale: {s0} }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "{ease}" }}, {t:.2f});')
def fade(sel, t, o=0, d=0.4):
    a(f'tl.to("{sel}", {{ opacity: {o}, duration: {d}, ease: "power2.inOut" }}, {t:.2f});')
def draw(sel, t, length, d=0.5):
    a(f'tl.fromTo("{sel}", {{ strokeDasharray: "{length} {length}", strokeDashoffset: {length} }}, {{ strokeDashoffset: 0, duration: {d}, ease: "power2.out" }}, {t:.2f});')
FILL = [0]
def pay(ids, t, pct, stagger=0.12):
    for i, cid in enumerate(ids):
        t0 = t + i * stagger
        a(f'(() => {{ const e = $("#{cid}"); const dx = {JX} - parseFloat(e.style.left), dy = {JY} - parseFloat(e.style.top);'
          f' tl.fromTo(e, {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {t0:.2f});'
          f' tl.fromTo(e, {{ x: 0 }}, {{ x: dx, duration: 0.7, ease: "power1.inOut", immediateRender: false }}, {t0 + 0.2:.2f});'
          f' tl.fromTo(e, {{ y: 0 }}, {{ y: dy, duration: 0.7, ease: "back.in(1.4)", immediateRender: false }}, {t0 + 0.2:.2f});'
          f' tl.to(e, {{ opacity: 0, duration: 0.12 }}, {t0 + 0.85:.2f}); }})();')
    a(f'tl.fromTo("#jf", {{ height: "{FILL[0]}%" }}, {{ height: "{pct}%", duration: 0.6, ease: "power2.out", immediateRender: {"true" if FILL[0] == 0 else "false"} }}, {t + 0.9:.2f});')
    a(f'tl.fromTo("#bank", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.16, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {t + 0.9:.2f});')
    FILL[0] = pct
    return t + 0.9
SFX = []; sx = lambda t, f, v=0.35: SFX.append((round(max(0, t), 2), f, v))

SC_T = [("s1", 0), ("s2", at["r2"]), ("s3", at["r3"]), ("s4", at["r4"]), ("s5", at["r5"]), ("s6", at["r6"]), ("s7", at["r8"]), ("s8", at["r9"])]
for i, (sid, t) in enumerate(SC_T):
    nxt = SC_T[i + 1][1] if i + 1 < len(SC_T) else DUR
    if i: a(f'tl.fromTo("#{sid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.55, ease: "power2.inOut" }}, {t - 0.2:.2f});')
    a(f'tl.fromTo("#{sid}", {{ scale: 0.985 }}, {{ scale: 1.02, duration: {nxt - t + 0.2:.2f}, ease: "none", immediateRender: false }}, {max(0, t - 0.2):.2f});')
    if i + 1 < len(SC_T): a(f'tl.to("#{sid}", {{ opacity: 0, duration: 0.45, ease: "power2.inOut" }}, {nxt - 0.42:.2f});')

# persistent figure
BIG = "x: 10, y: -447, scale: 2.6"
a(f'tl.fromTo("#you", {{ {BIG} }}, {{ x: 0, y: 0, scale: 1, duration: 1.0, ease: "power3.inOut" }}, {at["r2"] - 0.4:.2f});')
a(f'tl.fromTo("#you", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.3, ease: "power2.inOut", immediateRender: false }}, {at["r9"] - 0.6:.2f});')
a(f'tl.fromTo("#you", {{ x: 0, y: 0, scale: 1 }}, {{ {BIG}, duration: 0.05, immediateRender: false }}, {at["r9"] - 0.28:.2f});')
a(f'tl.fromTo("#you", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "power2.out", immediateRender: false }}, {at["r9"] - 0.2:.2f});')
a(f'tl.fromTo("#youi", {{ scale: 0.86 }}, {{ scale: 1, duration: 0.8, ease: "power3.out", immediateRender: false }}, {at["r9"] - 0.2:.2f});')
a(f'tl.fromTo(["#gr", "#bank"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, {at["r2"] + 0.2:.2f});')
fade('#gr', at["r9"] - 0.6, 0, 0.3); fade('#bank', at["r9"] - 0.6, 0, 0.3)

# ---- S1 hook: views race to a million from frame one
e_mil, e_views, e_how, e_pay = w("r1", "million"), w("r1", "views"), w("r1", "how"), w("r1", "pay")
a('tl.fromTo("#youi", { scale: 0.92 }, { scale: 1, duration: 0.6, ease: "power3.out" }, 0);')
a(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 1200 }}, {{ v: 1000000, duration: {e_views + 0.25:.2f}, ease: "power3.in", onUpdate: () => {{ $("#vw").textContent = "▶ " + Math.round(o.v).toLocaleString("en-US"); }} }}, 0); }})();')
a(f'tl.fromTo("#vw", {{ scale: 1 }}, {{ scale: 1.14, duration: 0.18, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {e_views + 0.25:.2f});')
a('gsap.set(["#camS", "#micS"], { strokeDasharray: "170 170", strokeDashoffset: 0 });')
for sel, t in (("#cam", 0.15), ("#mic", 0.3)): pop(sel, t)
fade("#cam", e_how - 0.5, 0.25); fade("#mic", e_how - 0.5, 0.25)
for i in range(len(HEARTS)):
    t0 = 0.05 + i * 0.42
    a(f'tl.fromTo("#h{i}", {{ opacity: 0, y: 60, scale: 0.4 }}, {{ opacity: 0.95, y: -90, scale: 1, duration: 0.7, ease: "power1.out" }}, {t0:.2f});')
    a(f'tl.to("#h{i}", {{ opacity: 0, y: -200, x: {(-1) ** i * 26}, duration: 0.9, ease: "power1.in" }}, {t0 + 0.7:.2f});')
    if i % 2 == 0: sx(t0, "pop", 0.18)
a(f'tl.fromTo("#qd", {{ opacity: 0, scale: 0.3, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: 6, duration: 0.5, ease: "back.out(2.5)" }}, {e_how:.2f});')
a(f'tl.fromTo("#qd", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {e_pay - 0.2:.2f});')
sx(0, "boom_open", 0.3); sx(0.1, "count_fast", 0.3); sx(1.6, "count_fast", 0.3); sx(e_mil - 0.6, "riser", 0.28); sx(e_views + 0.25, "impact", 0.42); sx(e_how, "ping", 0.38)

# ---- S2 what TikTok pays
e = {k: w("r2", k) for k in ("tiktok", "creators", "four", "dollars", "ten", "eligible", "videos")}
sx(at["r2"] - 0.4, "zoom_whoosh", 0.3)
a('gsap.set(["#am", "#am2", "#ar2"], { opacity: 0 });')
pop("#e2", at["r2"] + 0.1); a(f'tl.fromTo("#m2", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.4 }}, {at["r2"] + 0.2:.2f});')
a(f'tl.to("#ar2", {{ opacity: 1, duration: 0.3 }}, {e["creators"]:.2f});'); draw("#ar2", e["creators"], 200, 0.5)
pop("#am", e["four"] - 0.15, 0.5, "back.out(2.2)", 0.6); sx(e["four"] - 0.15, "kaching", 0.38)
a(f'tl.to("#am2", {{ opacity: 1, duration: 0.4 }}, {e["four"] + 0.5:.2f});')
tj = pay(c2, e["dollars"] - 0.1, 12); sx(tj - 0.1, "coin_jar", 0.42)
for i, k in enumerate(("ten", "eligible", "videos")):
    pop(f"#ch{i}", e[k] - 0.12); sx(e[k] - 0.12, "ui_tick2", 0.42)

# ---- S3 they don't live on views -> they sell
e = {k: w("r3", k) for k in ("smart", "dont", "views", "they", "sell")}
a('gsap.set(["#ct3", "#e3s"], { opacity: 0 });')
pop("#e3", at["r3"] + 0.1); sx(at["r3"] + 0.1, "swipe1", 0.26)
a(f'tl.to("#e3s", {{ opacity: 1, duration: 0.1 }}, {e["dont"] - 0.05:.2f});'); draw("#e3s", e["dont"] - 0.05, 400, 0.35); sx(e["dont"] - 0.05, "scratch", 0.32)
a(f'tl.to("#e3", {{ opacity: 0.3, duration: 0.4 }}, {e["dont"] + 0.2:.2f});')
a(f'tl.to(["#e3", "#e3s"], {{ opacity: 0, scale: 0.6, duration: 0.35, ease: "power2.in" }}, {e["they"] - 0.3:.2f});')
pop("#ct3", e["sell"] - 0.25, 0.5, "back.out(2.4)", 0.4); sx(e["sell"] - 0.25, "impact", 0.42)
pop("#cn3", e["sell"], 0.4, "back.out(3)", 0.3); sx(e["sell"], "kaching", 0.36)

# ---- S4 affiliate link
e = {k: w("r4", k) for k in ("affiliate", "someone", "buys", "earn", "commission")}
a('gsap.set(["#bb", "#bx", "#ct", "#a1", "#a2"], { opacity: 0 });')
pop("#lk", e["affiliate"] - 0.2); sx(e["affiliate"] - 0.2, "up1", 0.3)
pop("#bb", e["affiliate"] + 0.35); sx(e["affiliate"] + 0.35, "pop", 0.3)
a(f'tl.to("#a1", {{ opacity: 1, duration: 0.3 }}, {e["affiliate"] + 0.6:.2f});'); pop("#bx", e["affiliate"] + 0.75); sx(e["affiliate"] + 0.75, "pop", 0.3)
pop("#ct", e["someone"] - 0.05); sx(e["someone"] - 0.05, "swipe2", 0.28)
a(f'tl.to("#a2", {{ opacity: 1, duration: 0.3 }}, {e["buys"] - 0.15:.2f});')
a(f'tl.fromTo("#bx", {{ x: 0 }}, {{ x: 330, scale: 0.6, y: -6, duration: 0.5, ease: "power2.inOut", immediateRender: false }}, {e["buys"]:.2f});'); sx(e["buys"] + 0.4, "kaching", 0.32)
tj = pay(c4, e["earn"] - 0.1, 35); sx(tj - 0.1, "coin_jar", 0.45)

# ---- S5 digital product
e = {k: w("r5", k) for k in ("digital", "once", "sell")}
ag = [e["sell"], w("r5", "again", 0), w("r5", "again", 1)]
a('gsap.set(["#d1", "#dc0", "#dc1", "#dc2"], { opacity: 0 });')
pop("#d1", e["digital"] - 0.15, 0.5, "back.out(2.4)"); sx(e["digital"] - 0.15, "up2", 0.3)
a(f'tl.fromTo("#dk", {{ opacity: 0, scale: 0.3, rotation: -40 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }}, {e["once"] - 0.3:.2f});'); sx(e["once"] - 0.3, "shimmer", 0.3)
fl = 35
for i, (dx, dy) in enumerate(CPX):
    a(f'tl.fromTo("#dc{i}", {{ opacity: 0, x: 0, y: 0, scale: 1 }}, {{ opacity: 0.9, x: {dx}, y: {dy}, scale: 0.66, duration: 0.42, ease: "back.out(1.5)" }}, {ag[i] - 0.15:.2f});'); sx(ag[i] - 0.15, "swipe2" if i % 2 else "swipe1", 0.25)
    a(f'tl.fromTo("#d1", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.12, yoyo: true, repeat: 1, immediateRender: false }}, {ag[i] - 0.15:.2f});')
    fl += 8 if i < 2 else 9
    pay([c5[i]], ag[i] + 0.15, fl); sx(ag[i] + 0.2, "kaching", 0.28)

# ---- S6 the math
e = {k: w("r6", k) for k in ("math", "one", "thousand", "guide", "thats", "dollars", "from", "same")}
e["twenty"] = w("r6", "twenty"); e["twenty2"] = w("r6", "twenty", 1)
a('gsap.set(["#in6", "#d6", "#x6"], { opacity: 0 });'); sx(at["r6"], "heartbeat", 0.35)
for i in range(10):
    a(f'tl.fromTo("#pp{i}", {{ opacity: 0, y: 14 }}, {{ opacity: 0.3, y: 0, duration: 0.25 }}, {e["math"] + 0.3 + i * 0.04:.2f});')
a(f'tl.to("#pp6", {{ opacity: 1, scale: 1.35, duration: 0.35, ease: "back.out(3)" }}, {e["one"]:.2f});'); sx(e["one"], "ping", 0.36)
a(f'tl.to("#in6", {{ opacity: 1, duration: 0.3 }}, {e["thousand"] - 0.25:.2f});')
pop("#d6", e["twenty"] - 0.15); a(f'tl.to("#x6", {{ opacity: 1, duration: 0.3 }}, {e["twenty"]:.2f});'); sx(e["twenty"] - 0.15, "pop", 0.32)
a(f'tl.to("#tot", {{ opacity: 1, duration: 0.25 }}, {e["thats"]:.2f});')
a(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 20000, duration: {e["dollars"] - e["thats"] + 0.1:.2f}, ease: "power2.out", immediateRender: false, onUpdate: () => {{ $("#tot").textContent = "$" + Math.round(o.v).toLocaleString("en-US"); }} }}, {e["thats"]:.2f}); }})();')
sx(e["thats"], "count_fast", 0.32); sx(e["dollars"] + 0.05, "kaching", 0.45); sx(e["dollars"] + 0.05, "impact", 0.4)
a(f'tl.fromTo("#tot", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.2, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {e["dollars"] + 0.05:.2f});')
tj = pay(c6, e["dollars"] + 0.15, 100, 0.09); sx(tj - 0.1, "coin_jar", 0.5)
a(f'tl.to(["#row6", "#ml6"], {{ opacity: 0, duration: 0.35 }}, {e["from"] - 0.4:.2f});')
a(f'tl.to("#cmp", {{ opacity: 1, duration: 0.35 }}, {e["from"] - 0.2:.2f});')
a(f'tl.fromTo("#q0", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.3 }}, {e["from"] - 0.1:.2f});')
a(f'tl.fromTo("#q1", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.9, ease: "back.out(1.2)" }}, {e["from"] + 0.1:.2f});'); sx(e["from"] + 0.1, "riser", 0.26); sx(e["same"] + 0.2, "shimmer", 0.3)

# ---- S7 niches
ws = (w("r8", "money"), w("r8", "history"), w("r8", "ai"), w("r8", "motivation"))
for i, t0 in enumerate(ws):
    a(f'tl.fromTo("#n{i}", {{ opacity: 0, y: 30, scale: 0.7 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(2)" }}, {t0 - 0.12:.2f});'); sx(t0 - 0.12, "up1" if i % 2 == 0 else "up2", 0.3)
sx(at["r8"], "swipe1", 0.26)

# ---- S8 question
sx(at["r9"] - 0.3, "zoom_whoosh", 0.28)
a(f'tl.fromTo("#qm", {{ opacity: 0, scale: 0.3, rotation: -25 }}, {{ opacity: 1, scale: 1, rotation: 8, duration: 0.5, ease: "back.out(2.5)" }}, {at["r9"] + 0.1:.2f});')
for i in range(4):
    t0 = at["r9"] + 0.05 + i * 0.12
    a(f'tl.fromTo("#sl{i}", {{ y: 70, opacity: 0, scale: 0.4 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, {t0:.2f});'); sx(t0, "pop", 0.28)
for n in range(9):
    i = n % 4; t0 = at["r9"] + 0.85 + n * 0.3
    if t0 > DUR - 0.5: break
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
aud = [f'  <audio id="vo-{k}" class="clip" src="assets/vo/{k}_t.mp3" data-start="{round(at[k], 2)}" data-duration="{round(VO[k]["dur"] - 0.01, 2)}" data-track-index="2" data-volume="1.8"></audio>' for k in ORDER]
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
