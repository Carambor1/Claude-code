#!/usr/bin/env python3
""""Earning More Won't Make You Rich" — ~72 s, 16:9 essay in the reference style: black, thin white line icons,
small uppercase labels, calm narration (Sarah). Scenes are groups cross-faded on the voice. Run: python3 build.py"""
import json, re, subprocess

VO = json.load(open("vo.json"))
ORDER = [f"r{i}" for i in range(1, 14)]
GAP = {"r1": 0.6, "r3": 0.4, "r4": 0.5, "r5": 0.5, "r7": 0.5, "r8": 0.6, "r10": 0.5, "r11": 0.5, "r12": 0.6}
T, at = 0.3, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.3)
DUR = round(T + 2.0, 2)
W, H = 1080, 1920

def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)

E = dict(rich=w("r1", "rich"), raise_=w("r2", "raise"), twenty=w("r2", "twenty"), change=w("r3", "change"), apt=w("r4", "apartment"), car=w("r4", "car"),
         eat=w("r4", "eating"), earned=w("r4", "earned"), overlook=w("r5", "overlook"), income=w("r6", "income"), else_=w("r6", "else"), gone=w("r7", "gone"),
         upgrade=w("r7", "upgrade"), lifestyle=w("r8", "lifestyle"), normal=w("r8", "normal"), earn=w("r9", "earn"), keep=w("r9", "keep"),
         ceiling=w("r10", "ceiling"), floor=w("r10", "floor"), modest=w("r11", "modest"), wealthy=w("r11", "wealthy"), twice=w("r11", "twice"),
         comes=w("r12", "comes"), stays=w("r12", "stays"), keeping=w("r13", "keeping"))
SCENES = [("s1", 0), ("s2", at["r2"]), ("s4", at["r4"]), ("s6", at["r6"]), ("s8", at["r8"]), ("s9", at["r9"]), ("s10", at["r10"]),
          ("s11", at["r11"]), ("s12", at["r12"]), ("s13", at["r13"])]

S = 'fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'
FIG = '<svg viewBox="0 0 80 130"><circle cx="40" cy="24" r="20" fill="#fff"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="#fff"/></svg>'
ICON = {
    "house": f'<svg viewBox="0 0 120 110"><path d="M10 50 L60 10 L110 50 V104 H10 Z M45 104 V70 H75 V104" {S}/></svg>',
    "car": f'<svg viewBox="0 0 160 90"><path d="M10 62 V48 L32 22 H112 L140 48 H152 V62 Z M40 22 L30 46 H128 M76 22 V46" {S}/><circle cx="44" cy="68" r="12" {S}/><circle cx="118" cy="68" r="12" {S}/></svg>',
    "plate": f'<svg viewBox="0 0 140 110"><circle cx="70" cy="55" r="40" {S}/><circle cx="70" cy="55" r="26" {S}/><path d="M14 18 V50 M8 18 V36 M20 18 V36 M14 50 V96 M126 18 C116 28 116 48 126 54 V96" {S}/></svg>',
    "jar": f'<svg viewBox="0 0 100 130"><path d="M22 10 H78 M28 10 V26 C14 34 12 46 12 60 V112 C12 120 18 124 26 124 H74 C82 124 88 120 88 112 V60 C88 46 86 34 72 26 V10" {S}/></svg>',
    "note": f'<svg viewBox="0 0 160 100"><rect x="6" y="14" width="148" height="72" rx="8" {S}/><circle cx="80" cy="50" r="18" {S}/><path d="M26 32 V68 M134 32 V68" {S}/></svg>',
    "crown": f'<svg viewBox="0 0 140 110"><path d="M14 92 L22 30 L50 58 L70 18 L90 58 L118 30 L126 92 Z M14 92 H126" {S}/><circle cx="22" cy="28" r="5" fill="#fff"/><circle cx="70" cy="16" r="5" fill="#fff"/><circle cx="118" cy="28" r="5" fill="#fff"/></svg>',
    "up": f'<svg viewBox="0 0 80 100"><path d="M40 92 V12 M12 40 L40 12 L68 40" {S}/></svg>',
    "bag": f'<svg viewBox="0 0 100 110"><path d="M14 36 H86 L80 104 H20 Z M34 36 V26 a16 16 0 0 1 32 0 V36" {S}/></svg>',
    "lamp": f'<svg viewBox="0 0 140 180"><path d="M40 170 H100 M70 170 V96 L30 50 M30 50 L10 70 L54 96 Z" {S}/></svg>',
}
def C(id, cls, style, inner=""):
    return f'<div id="{id}" class="abs {cls} clip" data-start="0" data-duration="{DUR}" style="{style}">{inner}</div>'
def card(id, lab, val, style):
    return C(id, "card", style, f'<div class="lab">{lab}</div><div class="val" id="{id}v">{val}</div>')

# chart geometry (s6/s7)
CX0, CY0, CW, CH = 520, 760, 720, 380
inc = [(0, 3000), (3, 3000), (3, 3600), (12, 3600)]
exp_ = [(0, 2900), (3, 2900), (5, 3150), (7, 3300), (9, 3500), (12, 3600)]
def pts(series): return " ".join(f"{CX0 + CW * m / 12:.0f},{CY0 - CH * (v - 2600) / 1200:.0f}" for m, v in series)

def I(k, x, y, w, h, extra="", id_=""):
    return f'<div class="abs" {"id=" + chr(34) + id_ + chr(34) if id_ else ""} style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}">{ICON[k]}</div>'
NOTE = lambda x, y, val, vid: f'<div class="abs money" style="left:{x}px;top:{y}px">{ICON["note"]}<span id="{vid}">{val}</span></div>'
body = [
    C("s1", "", "left:0;top:0;width:1920px;height:1080px",
      f'<div class="abs fig" style="left:900px;top:614px;width:90px;height:146px">{FIG}</div><div class="abs ground"></div>'
      + NOTE(830, 230, "€3,000", "s1v") + I("crown", 880, 420, 140, 110, "opacity:0", "s1p")),
    C("s2", "", "left:0;top:0;width:1920px;height:1080px",
      f'<div class="abs fig" id="s2f" style="left:900px;top:614px;width:90px;height:146px">{FIG}</div><div class="abs ground"></div>'
      + NOTE(830, 230, "€3,000", "s2v") + I("up", 1110, 250, 70, 90, "", "s2p")
      + "".join(f'<div class="abs spark" id="sp{i}" style="left:{x}px;top:{y}px">✦</div>' for i, (x, y) in enumerate(((840, 560), (1010, 590), (870, 660), (1040, 680))))),
    C("s4", "", "left:0;top:0;width:1920px;height:1080px",
      f'<div class="abs fig" style="left:900px;top:614px;width:90px;height:146px">{FIG}</div><div class="abs ground"></div>'
      + NOTE(830, 60, "€3,600", "s4v")
      + "".join(f'<div class="abs up" id="u{i}" style="left:{x}px;top:{y}px"><div class="ic" style="width:{iw}px;height:{ih}px">{ICON[k]}</div><div class="cost">{c}</div></div>'
                for i, (k, c, x, y, iw, ih) in enumerate((("house", "−€300", 560, 480, 130, 120), ("car", "−€200", 1150, 510, 170, 96), ("plate", "−€100", 1080, 300, 140, 110))))),
    C("s6", "", "left:0;top:0;width:1920px;height:1080px",
      f'<svg class="abs" style="left:0;top:0;width:1920px;height:1080px" viewBox="0 0 1920 1080">'
      f'<path d="M{CX0} {CY0 - CH - 30} V{CY0} H{CX0 + CW + 30}" {S} stroke-opacity="0.5"/>'
      f'<polyline id="lin" points="{pts(inc)}" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/>'
      f'<polyline id="lex" points="{pts(exp_)}" fill="none" stroke="#9a9a9a" stroke-width="4" stroke-dasharray="12 9" stroke-linejoin="round"/></svg>'
      + I("note", CX0 + CW + 20, int(CY0 - CH * 1000 / 1200) - 70, 90, 56) + I("bag", CX0 + CW + 34, int(CY0 - CH * 1000 / 1200) + 6, 60, 66)
      + f'<div class="abs" id="s7p" style="left:{CX0 + 40}px;top:300px;width:110px;height:143px">{ICON["jar"]}<div class="zero">€0</div></div>'),
    C("s8", "", "left:0;top:0;width:1920px;height:1080px",
      '<div class="abs balloon" id="s8a" style="left:760px;top:240px">'
      + f'<div class="abs" style="left:70px;top:150px;width:110px;height:100px">{ICON["house"]}</div><div class="abs" style="left:220px;top:160px;width:130px;height:74px">{ICON["car"]}</div><div class="abs" style="left:150px;top:40px;width:110px;height:86px">{ICON["plate"]}</div></div>'
      + '<div class="abs coin big" id="s8b" style="left:1240px;top:680px">€</div>'),
    C("s9", "", "left:0;top:0;width:1920px;height:1080px",
      f'<svg class="abs" style="left:660px;top:280px;width:600px;height:480px" viewBox="0 0 600 480"><path d="M300 70 V440 M220 440 H380" {S}/>'
      f'<g id="beam"><path d="M90 90 H510" {S}/><path d="M90 90 L50 210 H130 Z M510 90 L470 210 H550 Z" {S}/></g><circle cx="300" cy="60" r="12" fill="#fff"/></svg>'
      + I("note", 700, 430, 120, 75, "", "pe") + f'<div class="abs" id="pk" style="left:1130px;top:400px;width:80px;height:104px">{ICON["jar"]}</div>'),
    C("s10", "", "left:0;top:0;width:1920px;height:1080px",
      f'<div class="abs fig" style="left:900px;top:614px;width:90px;height:146px">{FIG}</div>'
      '<div class="abs ceil" id="ceil"></div>' + I("note", 900, 250, 100, 62, "", "ceilL")
      + "".join(f'<div class="abs blk" style="left:{560 + i * 100}px;top:766px"></div>' for i in range(8))
      + f'<div class="abs" style="left:1340px;top:770px;width:44px;height:57px;opacity:0.6">{ICON["jar"]}</div>'),
    C("s11", "", "left:0;top:0;width:1920px;height:1080px",
      f'<div class="abs fig" style="left:520px;top:614px;width:90px;height:146px">{FIG}</div><div class="abs fig dimf" style="left:1140px;top:614px;width:90px;height:146px">{FIG}</div><div class="abs ground"></div>'
      + I("note", 480, 300, 120, 75) + I("note", 1090, 280, 120, 75) + I("note", 1120, 320, 120, 75)
      + f'<div class="abs jar" style="left:660px;top:600px">{ICON["jar"]}<div class="fill" id="jA"></div></div><div class="abs jar" style="left:1260px;top:600px">{ICON["jar"]}<div class="fill" id="jB"></div></div>'),
    C("s12", "", "left:0;top:0;width:1920px;height:1080px",
      f'<svg class="abs" style="left:760px;top:200px;width:400px;height:300px" viewBox="0 0 400 300"><path d="M20 20 H380 L230 170 V280 H170 V170 Z" {S}/></svg>'
      + "".join(f'<div class="abs coin" id="c{i}" style="left:{820 + i * 55}px;top:150px">€</div>' for i in range(6)) +
      f'<div class="abs jar" style="left:890px;top:560px;width:140px;height:182px">{ICON["jar"]}<div class="fill" id="jS"></div></div>'),
    C("s13", "", "left:0;top:0;width:1920px;height:1080px",
      f'<div class="abs jar" id="ej" style="left:890px;top:200px;width:140px;height:182px">{ICON["jar"]}<div class="fill" style="height:70%"></div></div>'
      '<div class="abs ctr endw" id="e1" style="top:470px">Earn more.</div><div class="abs ctr endw" id="e2" style="top:470px">Keep more.</div>'),
]
SCENE_IDS = [s for s, _ in SCENES]
CSS = f"""
    #root {{ position: absolute; inset: 0; background: #000; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
    #root .abs {{ position: absolute; }}
    #root .ctr {{ left: 0; width: 1920px; text-align: center; }}
    #root svg {{ width: 100%; height: 100%; display: block; }}
    #root .fig {{ filter: drop-shadow(0 0 14px rgba(255,255,255,0.5)); }}
    #root .fig.dimf {{ opacity: 0.55; }}
    #root .ground {{ left: 0; top: 760px; width: 1920px; height: 0; border-top: 2px dashed rgba(255,255,255,0.3); }}
    #root .pill {{ font-weight: 700; font-size: 28px; letter-spacing: 0.18em; text-transform: uppercase; color: #fff; border: 2px solid #fff; border-radius: 999px; padding: 8px 22px; white-space: nowrap; background: #000; }}
    #root .card {{ width: 320px; border: 2px solid rgba(255,255,255,0.8); border-radius: 16px; padding: 18px 24px; text-align: center; }}
    #root .lab, #root .small {{ font-weight: 700; font-size: 28px; letter-spacing: 0.18em; text-transform: uppercase; color: #9a9a9a; }}
    #root .val {{ font-weight: 800; font-size: 72px; letter-spacing: -0.02em; margin-top: 4px; }}
    #root .spark {{ font-size: 40px; opacity: 0; }}
    #root .up {{ display: flex; flex-direction: column; align-items: center; gap: 10px; width: 220px; opacity: 0; }}
    #root .up .ic {{ width: 140px; height: 110px; }}
    #root .up .cost {{ font-weight: 800; font-size: 40px; }}
    #root .tl {{ fill: #fff; font: 700 28px Inter, sans-serif; letter-spacing: 0.14em; text-transform: uppercase; }}
    #root .tl.dim {{ fill: #9a9a9a; }}
    #root .word {{ font-weight: 800; font-size: 70px; letter-spacing: 0.04em; text-transform: uppercase; }}
    #root .pan {{ width: 120px; text-align: center; font-weight: 800; font-size: 32px; letter-spacing: 0.14em; text-transform: uppercase; }}
    #root .ceil {{ left: 520px; top: 330px; width: 880px; height: 0; border-top: 4px solid #fff; box-shadow: 0 0 20px rgba(255,255,255,0.5); }}
    #root .blk {{ width: 88px; height: 56px; border: 2px dashed rgba(255,255,255,0.45); border-radius: 6px; }}
    #root .bar {{ height: 26px; border: 2px solid #fff; border-radius: 13px; overflow: hidden; }}
    #root .bar i {{ display: block; height: 100%; background: #fff; }}
    #root .jar {{ width: 100px; height: 130px; }}
    #root .fill {{ position: absolute; left: 12%; right: 12%; bottom: 6%; height: 0; background: #fff; border-radius: 0 0 10px 10px; box-shadow: 0 0 18px rgba(255,255,255,0.6); }}
    #root .coin {{ width: 44px; height: 44px; border: 3px solid #fff; border-radius: 50%; font-weight: 800; font-size: 26px; display: flex; align-items: center; justify-content: center; opacity: 0; }}
    #root .money {{ width: 260px; height: 160px; }}
    #root .money svg {{ width: 260px; height: 160px; }}
    #root .money span {{ position: absolute; left: 0; top: 168px; width: 260px; text-align: center; font-weight: 800; font-size: 56px; letter-spacing: -0.02em; }}
    #root .zero {{ position: absolute; left: 0; top: 54px; width: 110px; text-align: center; font-weight: 800; font-size: 30px; }}
    #root .balloon {{ width: 400px; height: 400px; border: 3px solid #fff; border-radius: 50%; box-shadow: 0 0 30px rgba(255,255,255,0.25); }}
    #root .coin.big {{ width: 70px; height: 70px; font-size: 38px; opacity: 1; }}
    #root .endw {{ font-weight: 800; font-size: 96px; letter-spacing: 0.12em; text-transform: uppercase; }}
    #root #e2, #root #s7p, #root #s2p {{ opacity: 0; }}
    #root {", #root ".join("#" + s for s in SCENE_IDS[1:])} {{ opacity: 0; }}
"""

J = []; a = J.append
# scene cross-fades with a gentle drift
for i, (sid, t) in enumerate(SCENES):
    nxt = SCENES[i + 1][1] if i + 1 < len(SCENES) else DUR
    if i: a(f'tl.fromTo("#{sid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.7, ease: "power2.inOut" }}, {t - 0.25:.2f});')
    a(f'tl.fromTo("#{sid}", {{ scale: 0.98 }}, {{ scale: 1.02, duration: {nxt - t + 0.25:.2f}, ease: "none", immediateRender: false }}, {max(0, t - 0.25):.2f});')
    if i + 1 < len(SCENES): a(f'tl.to("#{sid}", {{ opacity: 0, duration: 0.6, ease: "power2.inOut" }}, {nxt - 0.4:.2f});')
# S1
a(f'(() => {{ const o = {{ v: 3000 }}; tl.fromTo(o, {{ v: 3000 }}, {{ v: 9000, duration: {E["rich"] - 0.5:.2f}, ease: "power2.in", immediateRender: false, onUpdate: () => {{ $("#s1v").textContent = "€" + Math.round(o.v).toLocaleString("en-US"); }} }}, 0.3); }})();')
a(f'tl.fromTo("#s1p", {{ opacity: 0, y: 14, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, {E["rich"] - 0.15:.2f});')
a(f'tl.to("#s1p", {{ opacity: 0.25, duration: 0.6 }}, {E["rich"] + 0.9:.2f});')
# S2: the raise
a(f'(() => {{ const o = {{ v: 3000 }}; tl.fromTo(o, {{ v: 3000 }}, {{ v: 3600, duration: 0.8, ease: "power2.out", immediateRender: false, onUpdate: () => {{ $("#s2v").textContent = "€" + Math.round(o.v).toLocaleString("en-US"); }} }}, {E["twenty"]:.2f}); }})();')
a(f'tl.fromTo("#s2p", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)" }}, {E["twenty"]:.2f});')
for i in range(4):
    a(f'tl.fromTo("#sp{i}", {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.out" }}, {E["change"] - 0.8 + i * 0.2:.2f});')
# S4: upgrades on their words
for i, k in enumerate(("apt", "car", "eat")):
    a(f'tl.fromTo("#u{i}", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {E[k] - 0.1:.2f});')
# S6/S7: the two lines draw together
for lid in ("lin", "lex"):
    a(f'tl.fromTo("#{lid}", {{ strokeDasharray: "{"2000 2000" if lid == "lin" else "12 9"}", strokeDashoffset: {2000 if lid == "lin" else 0}, opacity: {1 if lid == "lin" else 0} }}, {{ strokeDashoffset: 0, opacity: 1, duration: 1.6, ease: "power1.inOut" }}, {(E["income"] if lid == "lin" else E["else_"] - 0.5):.2f});')
a(f'tl.fromTo("#s7p", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {E["gone"]:.2f});')
# S8
a(f'tl.fromTo("#s8a", {{ scale: 0.35 }}, {{ scale: 1.15, duration: 2.6, ease: "power1.inOut" }}, {at["r8"]:.2f});')
a(f'tl.fromTo("#s8b", {{ scale: 1, opacity: 1 }}, {{ scale: 0.3, opacity: 0.2, duration: 2.6, ease: "power1.inOut" }}, {at["r8"]:.2f});')
# S9: the scale tips from EARN to KEEP
a(f'tl.fromTo("#beam", {{ rotation: 0, svgOrigin: "300 60" }}, {{ rotation: -8, duration: 0.6, ease: "power2.out" }}, {E["earn"] - 0.1:.2f});')
a(f'tl.to("#beam", {{ rotation: 9, duration: 0.8, ease: "back.out(1.6)" }}, {E["keep"] - 0.1:.2f});')
a(f'tl.fromTo("#pe", {{ y: 0 }}, {{ y: 36, duration: 0.6 }}, {E["earn"] - 0.1:.2f}); tl.to("#pe", {{ y: -40, opacity: 0.5, duration: 0.8 }}, {E["keep"] - 0.1:.2f});')
a(f'tl.fromTo("#pk", {{ y: 0 }}, {{ y: -36, duration: 0.6 }}, {E["earn"] - 0.1:.2f}); tl.to("#pk", {{ y: 40, duration: 0.8 }}, {E["keep"] - 0.1:.2f});')
# S10: ceiling rises, floor stays empty
a(f'tl.fromTo(["#ceil", "#ceilL"], {{ y: 80 }}, {{ y: -60, duration: 1.4, ease: "power2.out" }}, {E["ceiling"] - 1.0:.2f});')
# S11: two jars
a(f'tl.fromTo("#jA", {{ height: "0%" }}, {{ height: "80%", duration: 2.4, ease: "power1.inOut" }}, {E["modest"]:.2f});')
a(f'tl.fromTo("#jB", {{ height: "0%" }}, {{ height: "4%", duration: 1.0 }}, {E["twice"]:.2f});')
# S12: coins in, few stay
for i in range(6):
    a(f'tl.fromTo("#c{i}", {{ opacity: 0, y: 0 }}, {{ opacity: 1, y: {380 if i % 2 == 0 else 120}, x: {(2.5 - i) * 40 if i % 2 == 0 else 0}, duration: 0.9, ease: "power1.in" }}, {E["comes"] - 0.4 + i * 0.18:.2f});')
    if i % 2: a(f'tl.to("#c{i}", {{ opacity: 0, duration: 0.3 }}, {E["comes"] + 0.5 + i * 0.18:.2f});')
a(f'tl.fromTo("#jS", {{ height: "0%" }}, {{ height: "55%", duration: 1.2 }}, {E["stays"] - 0.5:.2f});')
# S13
a(f'tl.to("#e1", {{ opacity: 0, y: -10, duration: 0.4, ease: "power2.inOut" }}, {E["keeping"] - 0.3:.2f});')
a(f'tl.fromTo("#ej", {{ scale: 0.9 }}, {{ scale: 1.08, duration: 0.6, ease: "back.out(2)" }}, {E["keeping"]:.2f});')
a(f'tl.fromTo("#e2", {{ opacity: 0, scale: 1.12 }}, {{ opacity: 1, scale: 1, duration: 0.7, ease: "power2.out" }}, {E["keeping"]:.2f});')

open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    <div id="lay" style="position:absolute;left:-420px;top:280px;width:1920px;height:1080px;transform:scale(1.15);transform-origin:960px 540px">
    {chr(10).join("    " + b for b in body)}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const $ = (s) => document.querySelector(s);
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
    e = end if end is not None else grp[i + 1][0][0][1] - 0.05
    caps.append(f'<div id="cap{i}" class="abs cap clip" data-start="{s}" data-duration="{round(min(e, DUR - 0.05) - s, 2)}"><span>{" ".join(x for x, _ in ws)}</span></div>')
open("compositions/cap.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; }}
    #root .abs {{ position: absolute; }}
    #root .cap {{ left: 90px; width: 900px; top: 1240px; text-align: center; font-weight: 800; font-size: 54px; line-height: 1.15; color: #fff; }}
    #root .cap span {{ display: inline-block; background: rgba(0,0,0,0.86); padding: 6px 22px 10px; border-radius: 16px; }}
  </style>
  <div id="root" data-composition-id="cap" data-width="{W}" data-height="{H}">
{chr(10).join("    " + c for c in caps)}
  </div>
  <script>window.__timelines["cap"] = gsap.timeline({{ paused: true }});</script>
</template>
""")

SFX = [(0.0, "boom_open", 0.3), (0.3, "count_fast", 0.3), (E["rich"] - 0.15, "shimmer", 0.35), (E["twenty"], "count_fast", 0.35), (E["twenty"] + 0.8, "coin_jar", 0.5),
       (E["change"] - 0.8, "shimmer", 0.35), (E["apt"] - 0.1, "pop", 0.35), (E["car"] - 0.1, "pop", 0.35), (E["eat"] - 0.1, "pop", 0.35),
       (E["overlook"], "heartbeat", 0.4), (E["income"], "swipe1", 0.3), (E["gone"], "impact", 0.35), (E["lifestyle"] - 0.1, "zoom_whoosh", 0.3),
       (E["keep"] - 0.1, "ui_tick2", 0.4), (E["ceiling"] - 1.0, "swipe2", 0.3), (E["modest"], "coin_jar", 0.45), (E["comes"] - 0.4, "coin_jar", 0.35),
       (E["keeping"], "impact", 0.45), (E["keeping"] + 0.1, "shimmer", 0.35)]
dur = {f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/sfx/{f}.mp3"], capture_output=True, text=True).stdout) for f in {x[1] for x in SFX}}
aud = [f'  <audio id="vo-{k}" class="clip" src="assets/vo/{k}.mp3" data-start="{round(at[k], 2)}" data-duration="{round(VO[k]["dur"] - 0.01, 2)}" data-track-index="2" data-volume="1.8"></audio>' for k in ORDER]
aud += [f'  <audio id="sx{n}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(t, 2)}" data-duration="{round(min(dur[f], DUR - t) - 0.01, 2)}" data-track-index="{10 + n}" data-volume="{v}"></audio>' for n, (t, f, v) in enumerate(SFX)]
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
print("duration", DUR)
