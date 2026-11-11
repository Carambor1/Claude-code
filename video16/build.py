#!/usr/bin/env python3
""""Every Second on Earth" — cut-paper collage, stop-motion feel, 9:16. Each fact is a coloured paper sheet dropping on the pile.
New design language: warm paper, flat cut shapes with hard shadows, poster numerals, stepped motion and a constant 8 fps "boil".
Run: python3 build.py"""
import json, re, subprocess, math, random

VO = json.load(open("vo.json"))
ORDER = [f"r{i}" for i in range(1, 10)]
GAP = {"r1": 0.5, "r2": 0.45, "r3": 0.45, "r4": 0.45, "r5": 0.45, "r6": 0.5, "r7": 0.6, "r8": 0.5}
T, at = 0.35, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.3)
DUR = round(T + 2.6, 2)
W, H = 1080, 1920
def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)
random.seed(11)
CREAM, INK, RED, BLUE, YEL, TEAL, NAVY, PINK, GRN, ORG, SKY = "#f3e9d2", "#1b1b1e", "#e4572e", "#2e5eaa", "#ffc914", "#17bebb", "#1d2b53", "#f497a9", "#5aa469", "#f77f00", "#9bd1e5"

def tape(txt, x, y, rot=-2, bg="#fffaf0", fg=INK, size=46, id_=""):
    n = 7; z = ",".join(f"{(0 if i % 2 else 2.2):.1f}% {i * 100 / n:.1f}%" for i in range(n + 1)); z2 = ",".join(f"{(100 if i % 2 else 97.8):.1f}% {100 - i * 100 / n:.1f}%" for i in range(n + 1))
    return (f'<div class="abs cut" {"id=" + chr(34) + id_ + chr(34) if id_ else ""} style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"><div class="boil"><div class="tape" style="background:{bg};color:{fg};font-size:{size}px;clip-path:polygon({z},{z2})">{txt}</div></div></div>')
def num(txt, x, y, color, size=380, id_="", rot=-3):
    return f'<div class="abs" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"><div class="boil"><div class="num" id="{id_}" style="color:{color};font-size:{size}px">{txt}</div></div></div>'
def disc(x, y, d, color, inner="", id_="", cls=""):
    return f'<div class="abs disc {cls}" {"id=" + chr(34) + id_ + chr(34) if id_ else ""} style="left:{x - d / 2}px;top:{y - d / 2}px;width:{d}px;height:{d}px;background:{color}">{inner}</div>'
def earth(x, y, d, id_):
    blobs = "".join(f'<i style="left:{l}%;top:{t}%;width:{bw}%;height:{bh}%;transform:rotate({r}deg)"></i>' for l, t, bw, bh, r in ((8, 14, 42, 34, -20), (50, 8, 30, 22, 15), (56, 40, 36, 44, 25), (14, 58, 30, 30, 40), (40, 30, 16, 14, 0)))
    return f'<div class="abs cut" id="{id_}" style="left:{x - d / 2}px;top:{y - d / 2}px;width:{d}px;height:{d}px"><div class="earth">{blobs}</div></div>'
def watch(x, y, r, pfx):
    ticks = "".join(f'<i style="transform:rotate({i * 30}deg) translateY(-{r * 0.7:.0f}px)"></i>' for i in range(12))
    return (f'<div class="abs" id="{pfx}" style="left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px"><div class="boil" style="width:100%;height:100%">'
            f'<div class="abs cut" style="left:{r - r * 0.13:.0f}px;top:{-r * 0.2:.0f}px;width:{r * 0.26:.0f}px;height:{r * 0.3:.0f}px;background:{INK};border-radius:10px"></div>'
            f'<div class="abs disc cut" style="inset:0;background:{RED}"></div><div class="abs disc" style="inset:{r * 0.16:.0f}px;background:#fffaf0"></div>'
            f'<div class="abs wt" style="left:{r}px;top:{r}px">{ticks}</div>'
            f'<div class="abs hand" id="{pfx}h" style="left:{r - r * 0.035:.0f}px;top:{r * 0.3:.0f}px;width:{r * 0.07:.0f}px;height:{r * 0.7:.0f}px"></div>'
            f'<div class="abs disc" style="left:{r - r * 0.08:.0f}px;top:{r - r * 0.08:.0f}px;width:{r * 0.16:.0f}px;height:{r * 0.16:.0f}px;background:{INK}"></div></div></div>')

# ---------- scenes
S = {}
S[0] = (CREAM, tape("EVERY SECOND ON EARTH", 150, 250, -3, BLUE, "#fff", 54) + watch(540, 800, 340, "w0") + tape("THE NEXT SECOND", 280, 1230, 2.5, YEL, INK, 60, "t0"))
SKIN = ("#f6c9a0", "#d9a273", "#a86f43", "#f0b98d")
def baby(i, x, y, d=250):
    return (f'<div class="abs" id="bb{i}" style="left:{x - d / 2}px;top:{y - d / 2}px;width:{d}px;height:{d}px"><div class="boil" style="width:100%;height:100%"><div class="abs disc cut" style="inset:0;background:{SKIN[i]}"></div>'
            f'<div class="abs curl" style="left:{d * 0.42:.0f}px;top:{-d * 0.08:.0f}px"></div>'
            f'<div class="abs eye" style="left:{d * 0.26:.0f}px;top:{d * 0.4:.0f}px"></div><div class="abs eye" style="left:{d * 0.62:.0f}px;top:{d * 0.4:.0f}px"></div>'
            f'<div class="abs disc" style="left:{d * 0.12:.0f}px;top:{d * 0.54:.0f}px;width:{d * 0.16:.0f}px;height:{d * 0.16:.0f}px;background:{PINK};opacity:0.8"></div><div class="abs disc" style="left:{d * 0.72:.0f}px;top:{d * 0.54:.0f}px;width:{d * 0.16:.0f}px;height:{d * 0.16:.0f}px;background:{PINK};opacity:0.8"></div>'
            f'<div class="abs disc" style="left:{d * 0.38:.0f}px;top:{d * 0.6:.0f}px;width:{d * 0.24:.0f}px;height:{d * 0.24:.0f}px;background:{(BLUE, TEAL, RED, GRN)[i]};border:8px solid #fffaf0"></div></div></div>')
BPOS = ((300, 900), (760, 830), (350, 1240), (790, 1180))
S[1] = (YEL, num("4", 90, 200, INK, 520, "n1") + tape("BABIES BORN", 500, 330, 3, RED, "#fff", 56) + "".join(baby(i, x, y) for i, (x, y) in enumerate(BPOS)))
def cloud(x, y, s, c):
    return f'<div class="abs cut" style="left:{x}px;top:{y}px;width:{420 * s:.0f}px;height:{200 * s:.0f}px"><div class="boil" style="width:100%;height:100%"><div class="abs disc" style="left:0;top:35%;width:45%;height:65%;background:{c}"></div><div class="abs disc" style="left:24%;top:0;width:50%;height:100%;background:{c}"></div><div class="abs disc" style="left:56%;top:28%;width:44%;height:72%;background:{c}"></div><div class="abs" style="left:14%;top:60%;width:72%;height:40%;background:{c};border-radius:40px"></div></div></div>'
BOLTS = ((250, 520, 1.0), (640, 560, 1.15), (430, 500, 0.85), (800, 540, 0.9), (150, 560, 0.8), (540, 520, 1.2))
def bolt(i, x, y, s): return f'<div class="abs bolt cut" id="bo{i}" style="left:{x}px;top:{y}px;width:{170 * s:.0f}px;height:{560 * s:.0f}px"></div>'
S[2] = (NAVY, "".join(bolt(i, *b) for i, b in enumerate(BOLTS)) + cloud(60, 330, 1.25, "#e8e6e1") + cloud(520, 300, 1.2, "#cfcdc8") + cloud(300, 250, 0.9, "#fffaf0")
        + f'<div class="abs disc cut" style="left:-360px;top:1180px;width:1800px;height:1800px;background:{GRN}"></div>'
        + num("40+", 120, 760, YEL, 330, "n2") + tape("LIGHTNING STRIKES", 250, 1290, -2.5, "#fffaf0", INK, 54) + '<div class="abs flash" id="fl"></div>')
S[3] = (SKY, num("200", 80, 210, INK, 360, "n3") + tape("WING BEATS", 560, 560, 3, YEL, INK, 56)
        + '<div class="abs" id="bee" style="left:300px;top:760px;width:480px;height:420px"><div class="boil" style="width:100%;height:100%">'
          f'<div class="abs wing" id="wg0" style="left:150px;top:-60px"></div><div class="abs wing" id="wg1" style="left:250px;top:-70px"></div>'
          f'<div class="abs cut" style="left:440px;top:210px;width:0;height:0;border-left:70px solid {INK};border-top:24px solid transparent;border-bottom:24px solid transparent"></div>'
          f'<div class="abs beeb cut"><i style="left:26%"></i><i style="left:52%"></i><i style="left:78%"></i></div>'
          f'<div class="abs disc cut" style="left:-40px;top:130px;width:190px;height:190px;background:{INK}"></div><div class="abs disc" style="left:10px;top:180px;width:46px;height:46px;background:#fffaf0"></div></div></div>'
        + "".join(f'<div class="abs disc dotp" style="left:{820 - i * 70}px;top:{1300 + int(40 * math.sin(i))}px;width:22px;height:22px;background:{INK}"></div>' for i in range(8))
        + f'<div class="abs" style="left:800px;top:1180px;width:260px;height:260px"><div class="boil" style="width:100%;height:100%">' + "".join(f'<div class="abs disc cut" style="left:{90 + 80 * math.cos(a * 1.2566):.0f}px;top:{90 + 80 * math.sin(a * 1.2566):.0f}px;width:100px;height:100px;background:{RED}"></div>' for a in range(5)) + f'<div class="abs disc" style="left:85px;top:85px;width:110px;height:110px;background:{YEL}"></div></div></div>')
CELLS = sorted([(160 + c * 152 + random.randint(-18, 18), 760 + r * 128 + random.randint(-16, 16)) for r in range(5) for c in range(6)], key=lambda p: (p[0] - 540) ** 2 + (p[1] - 1010) ** 2)
S[4] = (RED, "".join(f'<div class="abs cell cut" id="ce{i}" style="left:{x - 62}px;top:{y - 62}px"><i></i></div>' for i, (x, y) in enumerate(CELLS))
        + num("0", 70, 230, "#fffaf0", 200, "n4", -2) + tape("NEW BLOOD CELLS · IN YOUR BODY", 110, 500, 2, INK, "#fffaf0", 46))
STARS = "".join(f'<div class="abs star" style="left:{random.randint(30, 1040)}px;top:{random.randint(120, 1500)}px;transform:scale({random.uniform(0.5, 1.3):.2f}) rotate(45deg)"></div>' for _ in range(34))
S[5] = (INK, STARS + f'<div class="abs orbit"></div>' + earth(0, 0, 330, "e5") + '<div class="abs ruler cut" id="rl"><b></b></div>'
        + num("30 km", 110, 230, CREAM, 250, "n5") + tape("THROUGH SPACE", 420, 520, -3, TEAL, INK, 56))
S[6] = ("#5f4bb6", "".join(f'<div class="abs ringl" id="rg{i}" style="left:{540 - (300 + i * 26)}px;top:{860 - (300 + i * 26) * 0.42:.0f}px;width:{(300 + i * 26) * 2}px;height:{(300 + i * 26) * 0.84:.0f}px"></div>' for i in range(7))
        + earth(540, 860, 380, "e6") + '<div class="abs" style="left:540px;top:860px;width:0;height:0;transform:scaleY(0.42)"><div class="abs" id="arm" style="left:0;top:0;width:0;height:0"><div class="abs disc" id="ld" style="left:330px;top:-60px;width:120px;height:120px;background:#fff3b0;border:14px solid ' + YEL + ';box-shadow:0 0 0 10px rgba(255,201,20,0.35)"></div></div></div>'
        + num("0×", 110, 220, YEL, 380, "n6") + tape("AROUND THE EARTH", 380, 545, 3, "#fffaf0", INK, 54))
RAYS = "".join(f'<i style="transform:rotate({i * 22.5}deg) translateY(-400px)"></i>' for i in range(16))
CH = [(math.cos(a), math.sin(a)) for a in (0.3, 1.1, 1.9, 2.8, 3.6, 4.4, 5.2, 5.9)]
S[7] = ("#c1121f", f'<div class="abs" id="rays" style="left:540px;top:860px;width:0;height:0">{RAYS}</div>' + "".join(f'<div class="abs chunk cut" id="ck{i}" style="left:{540 - 35}px;top:{860 - 35}px"></div>' for i in range(8))
        + f'<div class="abs" style="left:240px;top:560px;width:600px;height:600px"><div class="boil" style="width:100%;height:100%"><div class="abs disc cut" style="inset:0;background:{YEL}"></div><div class="abs disc" style="inset:60px;background:#ffd94a"></div></div></div>'
        + num("0", 60, 210, "#fffaf0", 190, "n7", -2) + tape("TONS OF ITSELF · BURNED", 250, 1300, -2.5, INK, YEL, 52))
MINI = (("4", "BABIES", YEL, INK), ("40+", "STRIKES", NAVY, YEL), ("200", "WING BEATS", SKY, INK), ("2M", "BLOOD CELLS", RED, "#fffaf0"), ("30 km", "FLOWN", INK, CREAM), ("7×", "AROUND EARTH", "#5f4bb6", YEL), ("4M t", "OF SUN", "#c1121f", "#fffaf0"))
MPOS = ((180, 380, -7), (540, 300, 3), (900, 390, 8), (150, 800, 5), (930, 810, -6), (290, 1230, -4), (790, 1240, 6))
S[8] = (CREAM, "".join(f'<div class="abs mini cut" id="mi{i}" style="left:{x - 150}px;top:{y - 150}px;background:{bg};color:{fg};--r:{r}deg"><b>{n}</b><span>{l}</span></div>' for i, ((n, l, bg, fg), (x, y, r)) in enumerate(zip(MINI, MPOS)))
        + watch(540, 800, 210, "w8") + tape("ALL IN ONE SECOND", 250, 1420, -2, INK, YEL, 60, "t8"))
QW = (("SO", 130, 330, -5, "#fffaf0", INK, 120), ("WHAT", 400, 310, 3, YEL, INK, 150), ("DID", 110, 590, 4, RED, "#fff", 130), ("YOU", 440, 570, -3, "#fffaf0", INK, 150), ("DO", 800, 600, 6, TEAL, INK, 120), ("WITH", 300, 850, -2, INK, CREAM, 150), ("YOURS?", 130, 1090, -4, YEL, INK, 220))
S[9] = (BLUE, watch(930, 1440, 110, "w9") + "".join(f'<div class="abs cut" id="q{i}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)"><div class="boil"><div class="chip" style="background:{bg};color:{fg};font-size:{sz}px">{t}</div></div></div>' for i, (t, x, y, r, bg, fg, sz) in enumerate(QW)))

ROT = [0, -1.6, 1.3, -1.1, 1.7, -1.4, 1.2, -1.8, 0.8, -1.0]
body = "".join(f'<div class="abs sheet" id="s{i}" style="background:{S[i][0]}"><div class="abs in">{S[i][1]}</div></div>' for i in range(10))
CSS = f"""
    #root {{ position: absolute; inset: 0; background: {CREAM}; font-family: "Inter", sans-serif; color: {INK}; overflow: hidden; }}
    #root .abs {{ position: absolute; }}
    #root .sheet {{ left: -70px; top: -70px; width: 1220px; height: 2060px; box-shadow: 0 0 60px rgba(0,0,0,0.45); overflow: hidden; }}
    #root .in {{ left: 70px; top: 170px; width: {W}px; height: {H}px; }}
    #root .cut {{ filter: drop-shadow(0 12px 0 rgba(0,0,0,0.2)); }}
    #root .disc {{ border-radius: 50%; }}
    #root .tape {{ font-weight: 900; letter-spacing: 0.04em; padding: 14px 44px; white-space: nowrap; }}
    #root .num {{ font-weight: 900; letter-spacing: -0.05em; line-height: 0.9; white-space: nowrap; text-shadow: 0 12px 0 rgba(0,0,0,0.2); font-variant-numeric: tabular-nums; }}
    #root .chip {{ font-weight: 900; letter-spacing: -0.03em; line-height: 1; padding: 14px 34px 20px; white-space: nowrap; }}
    #root .wt i {{ position: absolute; left: -6px; top: -22px; width: 12px; height: 44px; background: {INK}; border-radius: 4px; }}
    #root .hand {{ background: {INK}; border-radius: 10px; transform-origin: 50% 100%; }}
    #root .curl {{ width: 44px; height: 44px; border: 10px solid {INK}; border-radius: 50%; border-bottom-color: transparent; }}
    #root .eye {{ width: 30px; height: 16px; border-bottom: 9px solid {INK}; border-radius: 0 0 30px 30px; }}
    #root .bolt {{ background: {YEL}; clip-path: polygon(55% 0, 100% 0, 62% 38%, 92% 38%, 18% 100%, 44% 52%, 12% 52%); opacity: 0; }}
    #root .flash {{ inset: -80px; background: #fff; opacity: 0; }}
    #root .beeb {{ left: 60px; top: 90px; width: 400px; height: 270px; border-radius: 50%; background: {YEL}; overflow: hidden; }}
    #root .beeb i {{ position: absolute; top: 0; width: 15%; height: 100%; background: {INK}; }}
    #root .wing {{ width: 170px; height: 260px; border-radius: 50%; background: rgba(255,255,255,0.88); transform-origin: 50% 100%; box-shadow: 0 10px 0 rgba(0,0,0,0.12); }}
    #root .cell {{ width: 124px; height: 124px; border-radius: 50%; background: #9d0208; opacity: 0; }}
    #root .cell i {{ position: absolute; inset: 30px; border-radius: 50%; background: #c8232c; }}
    #root .star {{ width: 16px; height: 16px; background: {CREAM}; }}
    #root .orbit {{ left: -700px; top: 760px; width: 2400px; height: 2400px; border-radius: 50%; border: 8px dashed rgba(243,233,210,0.5); }}
    #root .earth {{ width: 100%; height: 100%; border-radius: 50%; background: #2f7fd6; overflow: hidden; position: relative; }}
    #root .earth i {{ position: absolute; background: {GRN}; border-radius: 46% 54% 60% 40%; }}
    #root .ruler {{ left: 90px; top: 1400px; height: 64px; width: 900px; background: {CREAM}; transform-origin: 0 50%; }}
    #root .ruler b {{ position: absolute; inset: 0; background: repeating-linear-gradient(90deg, {INK} 0 6px, transparent 6px 45px); clip-path: inset(0 0 55% 0); }}
    #root .ringl {{ border: 9px solid {YEL}; border-radius: 50%; opacity: 0; }}
    #root #rays i {{ position: absolute; left: -46px; top: -70px; width: 0; height: 0; border-left: 46px solid transparent; border-right: 46px solid transparent; border-bottom: 140px solid {ORG}; }}
    #root .chunk {{ width: 70px; height: 70px; background: {YEL}; clip-path: polygon(10% 20%, 70% 0, 100% 50%, 60% 100%, 0 70%); opacity: 0; }}
    #root .mini {{ width: 300px; height: 300px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; transform: rotate(var(--r)); opacity: 0; }}
    #root .mini b {{ font-weight: 900; font-size: 104px; letter-spacing: -0.04em; line-height: 1; }}
    #root .mini span {{ font-weight: 800; font-size: 30px; letter-spacing: 0.08em; }}
    #root .grain {{ inset: 0; background: url(assets/grain.png); background-size: 540px 960px; mix-blend-mode: multiply; opacity: 0.9; pointer-events: none; }}
    #root .capw {{ left: 0; top: 1650px; width: {W}px; display: flex; justify-content: center; }}
    #root .capw .tape {{ font-size: 54px; background: #fffaf0; color: {INK}; padding: 12px 36px 14px; box-shadow: 0 10px 0 rgba(0,0,0,0.22); }}
"""
J = []; a = J.append
SFX = []; sx = lambda t, f, v=0.35: SFX.append((round(max(0, t), 2), f, v))
def pop(sel, t, d=0.3, steps=4, rot=0):
    a(f'tl.fromTo("{sel}", {{ opacity: 0, scale: 0.2, rotation: {rot - 14} }}, {{ opacity: 1, scale: 1, rotation: {rot}, duration: {d}, ease: "steps({steps})" }}, {t:.2f});')
def count(sel, t, d, end, fmt="Math.round(o.v).toLocaleString('en-US')", steps=10):
    a(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {end}, duration: {d:.2f}, ease: "steps({steps})", immediateRender: false, onUpdate: () => {{ $("{sel}").textContent = {fmt}; }} }}, {t:.2f}); }})();')

# sheets drop onto the pile
DROP = {1: w("r1", "four") - 0.45, 2: at["r2"] - 0.35, 3: at["r3"] - 0.35, 4: at["r4"] - 0.35, 5: at["r5"] - 0.35, 6: at["r6"] - 0.35, 7: at["r7"] - 0.35, 8: at["r8"] - 0.35, 9: at["r9"] - 0.3}
for i in range(1, 10):
    fx = (-1) ** i * 260
    a(f'tl.fromTo("#s{i}", {{ y: -2300, x: {fx}, rotation: {(-1) ** i * 11} }}, {{ y: 0, x: 0, rotation: {ROT[i]}, duration: 0.42, ease: "steps(5)" }}, {DROP[i]:.2f});')
    sx(DROP[i], "paper_slide", 0.5); sx(DROP[i] + 0.36, "clunk", 0.4)
    if i > 1: a(f'tl.set("#s{i - 2}", {{ visibility: "hidden" }}, {DROP[i] + 0.45:.2f});')

# S0: the stopwatch ticks once
e_sec = w("r1", "second")
a(f'tl.fromTo("#w0h", {{ rotation: 0 }}, {{ rotation: 6, duration: 0.12, ease: "steps(2)" }}, {e_sec:.2f});'); sx(e_sec, "clock_tick", 0.7); sx(0.05, "paper_fold1", 0.4)
a(f'tl.fromTo("#w0", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.1, yoyo: true, repeat: 1, ease: "steps(2)" }}, {e_sec:.2f});')
a('tl.fromTo("#w0", { scale: 0.3, rotation: -30 }, { scale: 1, rotation: 0, duration: 0.4, ease: "steps(5)" }, 0.0);')
pop("#t0", 0.35, 0.3, 4, 2.5)
# S1 babies
for i in range(4):
    t0 = w("r1", "four") + 0.05 + i * 0.26
    pop(f"#bb{i}", t0, 0.24, 3); sx(t0, "pop", 0.4)
pop("#n1", DROP[1] + 0.45, 0.25, 3)
# S2 lightning
t0 = w("r2", "strike") - 0.1
FL = [(0, 0), (1, 0.22), (2, 0.44), (3, 0.62), (4, 0.82), (5, 1.0), (1, 1.2), (0, 1.36), (3, 1.52), (2, 1.7), (5, 1.86), (4, 2.02), (1, 2.2)]
for n, (i, dt) in enumerate(FL):
    a(f'tl.set("#bo{i}", {{ opacity: 1 }}, {t0 + dt:.2f}); tl.set("#bo{i}", {{ opacity: 0 }}, {t0 + dt + 0.14:.2f});')
    a(f'tl.set("#fl", {{ opacity: 0.2 }}, {t0 + dt:.2f}); tl.set("#fl", {{ opacity: 0 }}, {t0 + dt + 0.06:.2f});')
    if n % 2 == 0: sx(t0 + dt, "impact", 0.3)
pop("#n2", w("r2", "more") - 0.1, 0.25, 3); sx(w("r2", "forty"), "stamp", 0.4)
# S3 bee
tb = DROP[3] + 0.4
for k in (0, 1):
    a(f'tl.fromTo("#wg{k}", {{ rotation: {-34 + k * 14} }}, {{ rotation: {22 + k * 14}, duration: 0.05, yoyo: true, repeat: {int((at["r4"] - tb) / 0.05)}, ease: "steps(1)" }}, {tb:.2f});')
a(f'tl.fromTo("#bee", {{ x: 620, y: 160 }}, {{ x: 0, y: 0, duration: 0.7, ease: "steps(7)" }}, {tb - 0.1:.2f});')
a(f'tl.to("#bee", {{ y: -36, duration: 0.4, yoyo: true, repeat: 5, ease: "steps(4)" }}, {tb + 0.65:.2f});'); sx(tb, "rustle", 0.35)
count("#n3", w("r3", "two") - 0.25, 0.7, 200, steps=8); sx(w("r3", "two") - 0.25, "count_fast", 0.3); sx(w("r3", "hundred") + 0.3, "stamp", 0.4)
# S4 blood cells double
tc = w("r4", "build") - 0.2; waves = [1, 2, 4, 8, 16, 30]; prev = 0
for wv, n in enumerate(waves):
    for i in range(prev, n):
        pop(f"#ce{i}", tc + wv * 0.24 + (i - prev) * 0.004, 0.16, 2)
    sx(tc + wv * 0.24, "pop", 0.3 + wv * 0.02); prev = n
count("#n4", DROP[4] + 0.4, w("r4", "million") + 0.3 - DROP[4] - 0.4, 2000000, steps=12); sx(w("r4", "million") + 0.3, "stamp", 0.4)
# S5 earth flies along its orbit
t5 = DROP[5] + 0.35; d5 = at["r6"] - t5 - 0.3
a(f'tl.fromTo("#e5", {{ x: 60, y: 1290, rotation: -30 }}, {{ x: 1010, y: 800, rotation: 60, duration: {d5:.2f}, ease: "steps({int(d5 * 9)})" }}, {t5:.2f});'); sx(t5, "swipe1", 0.3)
a(f'tl.fromTo("#rl", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {d5 - 0.3:.2f}, ease: "steps({int(d5 * 8)})" }}, {t5 + 0.1:.2f});')
count("#n5", DROP[5] + 0.4, w("r5", "kilometers") - DROP[5] - 0.4, 30, fmt="Math.round(o.v) + ' km'", steps=8); sx(w("r5", "thirty") - 0.3, "count_fast", 0.3); sx(w("r5", "kilometers"), "stamp", 0.4)
# S6 light laps the Earth seven times
t6 = w("r6", "circle") - 0.35; lap = 0.26
a(f'tl.fromTo("#arm", {{ rotation: 90 }}, {{ rotation: {90 + 360 * 7}, duration: {lap * 7:.2f}, ease: "none" }}, {t6:.2f});')
for i in range(7):
    a(f'tl.set("#rg{i}", {{ opacity: 1 }}, {t6 + (i + 1) * lap:.2f});'); a(f'tl.call(() => {{ $("#n6").textContent = "{i + 1}×"; }}, null, {t6 + (i + 1) * lap:.2f});'); sx(t6 + (i + 1) * lap, "ui_tick2", 0.42)
a('tl.call(() => { $("#n6").textContent = "0×"; }, null, 0);'); sx(t6, "zoom_whoosh", 0.3); sx(t6 + 7 * lap, "stamp", 0.42)
# S7 the Sun burns
t7 = DROP[7] + 0.3
a(f'tl.fromTo("#rays", {{ rotation: 0 }}, {{ rotation: 135, duration: {at["r8"] - t7:.2f}, ease: "steps({int((at["r8"] - t7) * 8)})" }}, {t7:.2f});')
for i, (cx, cy) in enumerate(CH):
    for rep in range(3):
        tk = w("r7", "burn") - 0.2 + i * 0.09 + rep * 0.75
        a(f'tl.fromTo("#ck{i}", {{ opacity: 1, x: {cx * 250:.0f}, y: {cy * 250:.0f}, scale: 1.2, rotation: 0 }}, {{ x: {cx * 620:.0f}, y: {cy * 620:.0f}, scale: 0.2, rotation: 200, opacity: 0, duration: 0.7, ease: "steps(6)", immediateRender: false }}, {tk:.2f});')
count("#n7", DROP[7] + 0.4, w("r7", "tons") - DROP[7] - 0.4, 4000000, steps=14); sx(w("r7", "burn") - 0.2, "riser", 0.3); sx(w("r7", "tons"), "stamp", 0.42)
# S8 recap collage + the second tick
for i in range(7):
    t0 = DROP[8] + 0.4 + i * 0.11
    a(f'tl.fromTo("#mi{i}", {{ opacity: 0, scale: 2.2, rotation: {MPOS[i][2] + 25} }}, {{ opacity: 1, scale: 1, rotation: {MPOS[i][2]}, duration: 0.2, ease: "steps(3)" }}, {t0:.2f});'); sx(t0, "flip", 0.35)
e8 = w("r8", "second")
a(f'tl.fromTo("#w8h", {{ rotation: 0 }}, {{ rotation: 6, duration: 0.12, ease: "steps(2)" }}, {e8:.2f});'); sx(e8, "clock_tick", 0.75)
a(f'tl.fromTo("#w8", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.1, yoyo: true, repeat: 1, ease: "steps(2)" }}, {e8:.2f});')
pop("#t8", w("r8", "in") - 0.1, 0.25, 3, -2)
# S9 the question, word by word
QT = (w("r9", "so"), w("r9", "what"), w("r9", "did"), w("r9", "you"), w("r9", "do"), w("r9", "with"), w("r9", "yours"))
for i, t0 in enumerate(QT):
    a(f'tl.fromTo("#q{i}", {{ opacity: 0, scale: 2.4 }}, {{ opacity: 1, scale: 1, duration: 0.16, ease: "steps(2)" }}, {max(t0 - 0.06, DROP[9] + 0.3):.2f});'); sx(max(t0 - 0.06, DROP[9] + 0.3), "stamp" if i == 6 else "pop", 0.42 if i == 6 else 0.3)
a(f'tl.fromTo("#q6", {{ rotation: -4 }}, {{ rotation: -1, duration: 0.3, yoyo: true, repeat: 7, ease: "steps(2)", immediateRender: false }}, {QT[6] + 0.3:.2f});')
for n in range(1, 6):
    tk = QT[6] + 0.1 + n * 0.5
    if tk < DUR - 0.2:
        a(f'tl.to("#w9h", {{ rotation: {n * 6}, duration: 0.1, ease: "steps(2)" }}, {tk:.2f});'); sx(tk, "clock_tick", 0.55)

# captions as paper strips
grp = []
for k in ORDER:
    cur = []
    for wd, t in VO[k]["words"]:
        cur.append((wd, at[k] + t))
        if len(cur) >= 3 or wd[-1] in ".,?:!":
            grp.append([cur, None]); cur = []
    if cur: grp.append([cur, None])
    grp[-1][1] = at[k] + VO[k]["dur"]
caps = []
for i, (ws, end) in enumerate(grp):
    s0 = round(ws[0][1] - 0.05, 2)
    e2 = end if end is not None else grp[i + 1][0][0][1] - 0.05
    caps.append(f'<div id="cap{i}" class="abs capw clip" data-start="{s0}" data-duration="{round(min(e2, DUR - 0.05) - s0, 2)}"><div class="tape" style="transform:rotate({(-1.5, 1.2, -0.8, 1.6)[i % 4]}deg)">{" ".join(x for x, _ in ws)}</div></div>')

open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    {body}
    {chr(10).join(caps)}
    <div class="abs grain" data-layout-ignore></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const R = document.querySelector('[data-composition-id="w"]') || document;
    const $ = (s) => R.querySelector(s);
    const boil = Array.from(R.querySelectorAll(".boil"));
    const hash = (n) => {{ const x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); }};
    const clock = {{ t: 0 }};
    const frame = (t) => {{ const k = Math.floor(t * 8); boil.forEach((el, i) => {{ const r = (hash(k * 13 + i * 7) - 0.5) * 2.2, x = (hash(k * 5 + i * 3) - 0.5) * 6, y = (hash(k * 11 + i * 17) - 0.5) * 6; el.style.transform = "translate(" + x.toFixed(1) + "px," + y.toFixed(1) + "px) rotate(" + r.toFixed(2) + "deg)"; }}); }};
    tl.fromTo(clock, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: () => frame(clock.t) }}, 0);
    frame(0);
{chr(10).join("    " + x for x in J)}
    window.__timelines["w"] = tl;
  </script>
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
{chr(10).join(aud)}
</div>
<script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>
""")
print("duration", DUR, "sfx", len(SFX))
print({k: round(v, 2) for k, v in at.items()})
