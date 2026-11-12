#!/usr/bin/env python3
""""Why you can't stop scrolling" — liquid-glass look: frosted translucent panels over a slow colour field, soft spring motion,
a morphing glass capsule that names each chapter. Everything is DOM + GSAP (seek-safe). Run: python3 build.py"""
import json, re, subprocess, math

VO = json.load(open("vo.json"))
ORDER = [f"r{i}" for i in range(1, 8)]
import os
TEMPO = 1.08
for k in ORDER:
    if not os.path.exists(f"assets/vo/{k}_t.mp3"):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"assets/vo/{k}.mp3", "-af", f"atempo={TEMPO}", f"assets/vo/{k}_t.mp3"], check=True)
    VO[k]["dur"] /= TEMPO; VO[k]["words"] = [(x, t / TEMPO) for x, t in VO[k]["words"]]
GAP = {"r1": 0.35, "r2": 0.35, "r3": 0.35, "r4": 0.4, "r5": 0.4, "r6": 0.5}
T, at = 0.3, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.3)
DUR = round(T + 2.6, 2)
W, H = 1080, 1920
def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)
B = [0] + [round(at[f"r{i}"] - 0.3, 2) for i in range(2, 8)] + [DUR]

THUMB = ["#c9d1e0,#8b95ab", "#aab4c8,#6f7a92", "#dfe4ee,#9aa4b8", "#b8c1d3,#7b859c", "#cfd6e4,#8f99af", "#a3adc2,#69748c"]
def fcard(i): return (f'<div class="fc"><div class="th" style="background:linear-gradient(135deg,{THUMB[i % 6]})"></div>'
                      f'<div class="ln"><i style="width:{70 + (i * 37) % 30}%"></i><i style="width:{40 + (i * 53) % 35}%"></i></div></div>')
FEED = "".join(fcard(i) for i in range(26))
GLY = {"dash": '<div class="gw"><div class="dash"></div></div>', "heart": '<div class="gw"><svg viewBox="0 0 100 90"><path d="M50 84 C6 52 14 10 50 30 C86 10 94 52 50 84 Z" fill="#ff6b81"/></svg></div>'}
REEL = lambda i, last: f'<div class="abs glass reel" id="rl{i}"><div class="strip" id="st{i}">' + "".join(GLY["dash"] for _ in range(9)) + GLY[last] + '</div></div>'
ICOL = ["#eef1f7", "#c7cedc", "#dfe4ee", "#b4bdcf", "#eef1f7", "#c7cedc", "#dfe4ee", "#b4bdcf", "#eef1f7"]
APPS = "".join(f'<div class="abs glass app" id="ap{i}" style="left:{150 + (i % 3) * 280}px;top:{600 + (i // 3) * 250}px"><i style="background:{ICOL[i]}"></i>'
               + (f'<b class="badge" id="bd{i}">{n}</b>' if (n := {0: 3, 2: 12, 4: 1, 5: 7, 7: 99}.get(i)) else "") + '</div>' for i in range(9))
def row(i, label, ctl): return f'<div class="row" id="rw{i}"><span>{label}</span>{ctl}</div>'
TOG = lambda i, on: f'<div class="tog {"on" if on else ""}" id="tg{i}"><i id="tk{i}"></i></div>'
def sc(i, inner): return f'<div class="abs scene" id="sc{i}">{inner}</div>'
TITLES = [("You&rsquo;re not weak.", "It was built this way."), ("The feed", "never ends."), ("Rewards", "are random."), ("Autoplay decides", "for you."), ("Red means", "urgent."), ("Add your", "own stop."), ("It&rsquo;s not you.", "It&rsquo;s the design.")]
ISL = [("Why you scroll", 430), ("1 &nbsp;Endless feed", 470), ("2 &nbsp;Random rewards", 560), ("3 &nbsp;Autoplay", 380), ("4 &nbsp;Red badges", 430), ("Your move", 340), ("", 96)]
def title(i): return f'<div class="abs ctr ttl" id="tt{i}"><div class="l1" id="tt{i}a">{TITLES[i][0]}</div><div class="l2" id="tt{i}b">{TITLES[i][1]}</div></div>'
S = {}
S[0] = title(0) + f'<div class="abs glass phone" id="ph"><div class="feedw"><div class="feed" id="feed">{FEED}</div></div><div class="abs sbar"><i id="sth"></i></div></div><div class="abs glass thumb" id="thb"></div>'
S[1] = title(1) + '<div class="abs glass chip" id="ch1" style="left:110px;top:1380px">Page 1 of &infin;</div>'
S[2] = title(2) + REEL(0, "dash") + REEL(1, "dash") + REEL(2, "heart") + '<div class="abs glass chip" id="ch2" style="left:270px;top:1200px">boring &middot; boring &middot; <b>great</b></div><div class="abs spin" id="spn"></div>'
S[3] = title(3) + ('<div class="abs glass vid" id="v0"><div class="play"></div></div><div class="abs glass vid" id="v1"><div class="play"></div></div>'
                   '<div class="abs glass next" id="nx"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="8"/><circle id="nxr" cx="50" cy="50" r="42" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-dasharray="264" stroke-dashoffset="264" transform="rotate(-90 50 50)"/></svg><b id="nxn">3</b><span>Up next</span></div>')
S[4] = title(4) + APPS
S[5] = title(5) + '<div class="abs glass panel" id="pn">' + row(0, "Autoplay", TOG(0, True)) + row(1, "Grayscale", TOG(1, False)) + row(2, "Timer", '<div class="tm" id="tm">20:00</div>') + '</div>'
S[6] = '<div class="abs glass plate" id="pl"></div>' + title(6)
SVGI = {
    "heart": '<svg viewBox="0 0 100 100"><path d="M50 86 C8 54 16 14 50 34 C84 14 92 54 50 86 Z" fill="#ff6b81"/></svg>',
    "bell": '<svg viewBox="0 0 100 100"><path d="M50 12 C32 12 26 26 26 42 V60 L16 74 H84 L74 60 V42 C74 26 68 12 50 12 Z M40 80 a10 10 0 0 0 20 0 Z" fill="#fff"/></svg>',
    "chat": '<svg viewBox="0 0 100 100"><path d="M14 18 H86 V68 H48 L28 86 V68 H14 Z" fill="#fff"/></svg>',
    "star": '<svg viewBox="0 0 100 100"><path d="M50 8 L62 38 L94 40 L69 60 L78 92 L50 74 L22 92 L31 60 L6 40 L38 38 Z" fill="#fff"/></svg>',
    "play": '<svg viewBox="0 0 100 100"><path d="M32 18 L82 50 L32 82 Z" fill="#fff"/></svg>',
    "check": '<svg viewBox="0 0 100 100"><path d="M22 52 L42 72 L78 30" fill="none" stroke="#fff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "moon": '<svg viewBox="0 0 100 100"><path d="M64 12 A40 40 0 1 0 88 62 A32 32 0 0 1 64 12 Z" fill="#fff"/></svg>',
    "clock": '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="36" fill="none" stroke="#fff" stroke-width="10"/><path d="M50 30 V52 L64 62" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/></svg>',
}
PCOL = {"heart": "#5a6379", "bell": "#ff453a", "chat": "#5a6379", "star": "#6b7489", "play": "#4d566b", "check": "#30d158", "moon": "#5a6379", "clock": "#6b7489", "txt": "#5a6379"}
POPS = []; XS = {i: "" for i in range(7)}
def pop(scene, kind, x, y, size, t, txt=None, col=None, out=None, drift=None, rot=0):
    pid = f"pp{len(POPS)}"
    c = col or PCOL[kind]
    if txt: XS[scene] += f'<div class="abs gl2 tx" id="{pid}" style="left:{x}px;top:{y}px;--c:{c};font-size:{size}px">{txt}</div>'
    else: XS[scene] += f'<div class="abs gl2" id="{pid}" style="left:{x - size / 2}px;top:{y - size / 2}px;width:{size}px;height:{size}px;--c:{c}">{SVGI[kind]}</div>'
    POPS.append((pid, t, out, drift, rot)); return pid
KIN = ["heart", "chat", "star", "play", "heart", "chat", "star", "heart", "play", "chat"]
# 0 hook: a storm of likes and alerts around the phone, later snapped to a neat grid ("built that way")
HOOK = [(150, 700, 150), (930, 760, 170), (120, 960, 130), (960, 1010, 140), (200, 1220, 170), (900, 1250, 150), (110, 1420, 140), (960, 1450, 130),
        (300, 600, 110), (790, 590, 120), (60, 830, 110), (1010, 890, 110), (250, 1500, 120), (820, 1510, 130), (540, 560, 120), (540, 1560, 110)]
GRIDP = [(130, 700), (950, 700), (130, 900), (950, 900), (130, 1100), (950, 1100), (130, 1300), (950, 1300), (310, 580), (770, 580), (130, 1500), (950, 1500), (310, 1520), (770, 1520), (540, 560), (540, 1540)]
HID = [pop(0, KIN[i % 10], x, y, s, 0.06 + i * 0.12, rot=(-1) ** i * 12) for i, (x, y, s) in enumerate(HOOK)]
J1 = pop(0, "txt", 60, 1345, 44, 1.5, txt="just 1 more", rot=-6); J2 = pop(0, "txt", 690, 640, 44, 2.0, txt="just 1 more", rot=5)
BD = pop(0, "txt", 395, 1395, 54, w("r1", "built") + 0.05, txt="by design", col="#3d465c")
S[0] += f'<svg class="abs" id="bp" style="left:0;top:0;width:{W}px;height:{H}px;opacity:0" viewBox="0 0 {W} {H}">' + "".join(f'<path d="M{x} 520 V1600" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="10 12"/>' for x in (130, 310, 540, 770, 950)) + "".join(f'<path d="M60 {y} H1020" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="10 12"/>' for y in (580, 700, 900, 1100, 1300, 1500)) + '</svg>'
# 1 endless: cards overflow the phone, a counter, and a "The End" card that gets flicked away
FLY = [(40, 0.0, 1.0), (760, 0.5, 1.25), (-60, 1.1, 0.85), (820, 1.7, 1.1), (20, 2.4, 1.2), (780, 3.0, 0.9), (-30, 3.6, 1.15), (800, 4.1, 1.0)]
S[1] += "".join(f'<div class="abs gl2 fly" id="fy{i}" style="left:{x}px;top:1620px;--c:{("#5a6379", "#4d566b", "#6b7489", "#454e63")[i % 4]};transform:scale({sc})"><i></i><u></u></div>' for i, (x, dl, sc) in enumerate(FLY))
S[1] += '<div class="abs glass endc" id="endc">The End</div><div class="abs glass chip" id="cnt1" style="left:610px;top:1380px">Posts <b id="cn1">0</b></div>'
# 2 rewards
S[2] += '<div class="abs glass meter" id="mt"><i id="mtf"></i><span>REWARD</span></div>'
BUR = [(math.cos(a * 0.449 + 0.2), math.sin(a * 0.449 + 0.2)) for a in range(14)]
# 3 autoplay: a queue behind the player and the clock running away
S[3] = S[3].replace('<div class="abs glass vid" id="v0">', '<div class="abs gl2 vq" id="vq1" style="--c:#454e63"></div><div class="abs gl2 vq" id="vq0" style="--c:#5a6379"></div><div class="abs glass vid" id="v0">')
# 4 badges: banners
S[4] += '<div class="abs glass ban" id="bn0" style="top:1375px"><b></b><span>3 new likes</span></div><div class="abs glass ban" id="bn1" style="top:1500px"><b></b><span>Someone you know posted</span></div>'
# 5 your move: a timer ring
S[5] += '<div class="abs glass ringc" id="rc"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="9"/><circle id="rcr" cx="50" cy="50" r="40" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-dasharray="251" stroke-dashoffset="251" transform="rotate(-90 50 50)"/></svg><b>20</b></div>'
# pops for the later scenes
for (x, y), wd in zip(((70, 1120), (790, 1130), (430, 1150)), ("most", "posts", "boring")): pop(2, "txt", x, y, 44, w("r3", wd) - 0.08, txt="meh", rot=(-6, 5, -3)[len(POPS) % 3])
TG = w("r3", "great") + 0.12
for i, (cx, cy) in enumerate(BUR): pop(2, ("heart", "star")[i % 2], 840, 885, 84 + (i % 3) * 22, TG + i * 0.015, drift=(cx * (330 + i % 4 * 60), cy * (330 + i % 4 * 60), 1.1))
for i, (x, y) in enumerate(((610, 610), (930, 640), (700, 1110))): pop(2, "txt", x, y, 50, TG + 0.15 + i * 0.12, txt="+1", col="#3d465c", rot=(-8, 6, -4)[i])
for i, (lab, wd, col) in enumerate((("23:41", "decides", "#5a6379"), ("00:58", "for", "#5a6379"), ("02:17", "can", "#ff453a"))): pop(3, "txt", 130, 1235 + i * 125, 52, w("r4", wd) - 0.05 + (0.25 if i == 2 else 0), txt=lab, col=col, rot=(-4, 3, -2)[i])
BELLS = [pop(4, "bell", x, y, s, w("r5", "badges") + 0.1 + i * 0.15) for i, (x, y, s) in enumerate(((75, 560, 110), (1005, 570, 120), (75, 1300, 100)))]
for i, wd in enumerate(("autoplay", "grayscale", "timer")): pop(5, "check", 1000, 759 + i * 190, 100, w("r6", wd) + 0.25)
for i, k in enumerate(("check", "clock", "moon")): pop(6, k, 380 + i * 160, 1230, 130, w("r7", "its", 1) + 0.25 + i * 0.14)
BLOBS = [("#46516d", 60, 380, 1200), ("#39435c", 760, 220, 1100), ("#566589", 800, 1150, 1300), ("#2f384e", 60, 1300, 1050), ("#6c7a9c", 440, 820, 800), ("#3c4763", 300, 1750, 1100), ("#4c5a7c", 900, 1700, 900)]
bg = '<div class="abs" id="bg">' + "".join(f'<div class="abs blob" id="bl{i}" style="left:{x - s // 2}px;top:{y - s // 2}px;width:{s}px;height:{s}px;background:radial-gradient(circle,{c} 0%,{c}00 68%)"></div>' for i, (c, x, y, s) in enumerate(BLOBS)) + '</div>'
body = bg + "".join(sc(i, S[i] + XS[i]) for i in range(7)) + '<div class="abs glass isl" id="isl"><span id="islt">Why you scroll</span></div>'
CSS = f"""
    #root {{ position: absolute; inset: 0; background: linear-gradient(170deg, #1b1f2a 0%, #10131b 50%, #171a24 100%); font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
    #root .abs {{ position: absolute; }}
    #root .ctr {{ left: 0; width: {W}px; text-align: center; }}
    #root #bg {{ inset: 0; }}
    #root .blob {{ border-radius: 50%; opacity: 0.8; }}
    #root .scene {{ inset: 0; opacity: 0; }}
    #root .glass {{ background: radial-gradient(120% 70% at 8% 0%, rgba(255,255,255,0.34), rgba(255,255,255,0) 60%), linear-gradient(140deg, rgba(255,255,255,0.22), rgba(255,255,255,0.07) 55%, rgba(255,255,255,0.14)); -webkit-backdrop-filter: blur(30px) saturate(170%); backdrop-filter: blur(30px) saturate(170%); border: 2px solid rgba(255,255,255,0.45); box-shadow: inset 0 2.5px 0 rgba(255,255,255,0.7), inset 0 -1.5px 0 rgba(255,255,255,0.14), inset 0 0 40px rgba(255,255,255,0.06), 0 34px 90px rgba(0,0,0,0.38); }}
    #root .isl {{ left: 325px; top: 132px; width: 430px; height: 96px; border-radius: 48px; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
    #root .isl span {{ font-weight: 600; font-size: 40px; letter-spacing: -0.01em; white-space: nowrap; }}
    #root .ttl {{ top: 300px; z-index: 5; }}
    #root .ttl div {{ font-weight: 700; font-size: 104px; letter-spacing: -0.035em; line-height: 1.08; white-space: nowrap; text-shadow: 0 6px 40px rgba(0,0,0,0.35); opacity: 0; }}
    #root .ttl .l2 {{ color: rgba(255,255,255,0.72); }}
    #root .phone {{ left: 280px; top: 620px; width: 520px; height: 860px; border-radius: 86px; overflow: hidden; }}
    #root .feedw {{ position: absolute; left: 34px; right: 54px; top: 34px; bottom: 34px; overflow: hidden; border-radius: 56px; }}
    #root .fc {{ height: 190px; margin-bottom: 22px; border-radius: 40px; background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.25); display: flex; align-items: center; gap: 22px; padding: 0 24px; }}
    #root .fc .th {{ width: 130px; height: 130px; border-radius: 30px; flex: none; }}
    #root .fc .ln {{ flex: 1; display: flex; flex-direction: column; gap: 18px; }}
    #root .fc .ln i {{ display: block; height: 20px; border-radius: 10px; background: rgba(255,255,255,0.55); }}
    #root .sbar {{ right: 22px; top: 70px; bottom: 70px; width: 10px; border-radius: 5px; background: rgba(255,255,255,0.18); }}
    #root .sbar i {{ position: absolute; left: 0; top: 0; width: 10px; height: 120px; border-radius: 5px; background: rgba(255,255,255,0.9); }}
    #root .thumb {{ left: 610px; top: 1250px; width: 120px; height: 120px; border-radius: 50%; opacity: 0; }}
    #root .chip {{ height: 104px; padding: 0 44px; border-radius: 52px; display: flex; align-items: center; font-weight: 600; font-size: 46px; letter-spacing: -0.01em; white-space: nowrap; opacity: 0; }}
    #root .chip b {{ color: #fff; font-weight: 800; text-shadow: 0 0 22px rgba(255,255,255,0.7); }}
    #root .reel {{ top: 720px; width: 250px; height: 330px; border-radius: 60px; overflow: hidden; }}
    #root #rl0 {{ left: 115px; }} #root #rl1 {{ left: 415px; }} #root #rl2 {{ left: 715px; }}
    #root .strip {{ position: absolute; left: 0; top: 0; width: 100%; }}
    #root .gw {{ height: 330px; display: flex; align-items: center; justify-content: center; }}
    #root .gw svg {{ width: 150px; height: 135px; filter: drop-shadow(0 0 26px rgba(255,107,129,0.7)); }}
    #root .gw .dash {{ width: 120px; height: 26px; border-radius: 13px; background: rgba(255,255,255,0.5); }}
    #root .spin {{ left: 495px; top: 600px; width: 90px; height: 90px; border-radius: 50%; border: 9px solid rgba(255,255,255,0.25); border-top-color: #fff; opacity: 0; }}
    #root .vid {{ left: 140px; top: 650px; width: 800px; height: 520px; border-radius: 64px; }}
    #root .play {{ position: absolute; left: 350px; top: 200px; width: 0; height: 0; border-left: 110px solid rgba(255,255,255,0.92); border-top: 62px solid transparent; border-bottom: 62px solid transparent; }}
    #root .next {{ left: 590px; top: 1230px; width: 350px; height: 150px; border-radius: 75px; display: flex; align-items: center; gap: 22px; padding: 0 24px; opacity: 0; }}
    #root .next svg {{ width: 104px; height: 104px; flex: none; }}
    #root .next b {{ position: absolute; left: 24px; width: 104px; text-align: center; font-weight: 700; font-size: 48px; }}
    #root .next span {{ font-weight: 600; font-size: 42px; white-space: nowrap; }}
    #root .app {{ width: 220px; height: 220px; border-radius: 56px; opacity: 0; }}
    #root .app i {{ position: absolute; inset: 56px; border-radius: 50%; opacity: 0.9; }}
    #root .badge {{ position: absolute; right: -26px; top: -26px; min-width: 84px; height: 84px; padding: 0 22px; border-radius: 42px; background: #ff3b30; font-weight: 700; font-size: 46px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(255,59,48,0.6); transform: scale(0); }}
    #root .panel {{ left: 110px; top: 650px; width: 860px; border-radius: 70px; padding: 14px 54px; opacity: 0; }}
    #root .row {{ height: 190px; display: flex; align-items: center; justify-content: space-between; font-weight: 600; font-size: 60px; letter-spacing: -0.02em; border-bottom: 1.5px solid rgba(255,255,255,0.2); }}
    #root .row:last-child {{ border-bottom: 0; }}
    #root .tog {{ position: relative; width: 170px; height: 100px; border-radius: 50px; background: rgba(120,120,128,0.5); }}
    #root .tog.on {{ background: #30d158; }}
    #root .tog i {{ position: absolute; left: 8px; top: 8px; width: 84px; height: 84px; border-radius: 50%; background: #fff; box-shadow: 0 6px 16px rgba(0,0,0,0.3); }}
    #root .tog.on i {{ transform: translateX(70px); }}
    #root .tm {{ font-weight: 700; font-size: 60px; font-variant-numeric: tabular-nums; padding: 12px 34px; border-radius: 40px; background: rgba(255,255,255,0.2); opacity: 0.35; }}
    #root .plate {{ left: 90px; top: 560px; width: 900px; height: 520px; border-radius: 90px; opacity: 0; }}
    #root #tt6 {{ top: 690px; }}
    #root .gl2 {{ border-radius: 34%; background: radial-gradient(120% 80% at 15% 0%, rgba(255,255,255,0.55), rgba(255,255,255,0) 55%), linear-gradient(150deg, color-mix(in srgb, var(--c) 86%, #fff), color-mix(in srgb, var(--c) 78%, #000)); border: 2.5px solid rgba(255,255,255,0.6); box-shadow: inset 0 3px 0 rgba(255,255,255,0.55), 0 18px 44px rgba(0,0,0,0.35); display: flex; align-items: center; justify-content: center; opacity: 0; }}
    #root .gl2 svg {{ width: 56%; height: 56%; }}
    #root .gl2.tx {{ border-radius: 999px; padding: 16px 38px 20px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; }}
    #root .fly {{ width: 330px; height: 150px; border-radius: 40px; justify-content: flex-start; gap: 20px; padding: 0 22px; }}
    #root .fly i {{ width: 100px; height: 100px; border-radius: 26px; background: rgba(255,255,255,0.85); flex: none; }}
    #root .fly u {{ flex: 1; height: 22px; border-radius: 11px; background: rgba(255,255,255,0.8); }}
    #root .endc {{ left: 360px; top: 960px; width: 360px; height: 150px; border-radius: 46px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 60px; opacity: 0; }}
    #root .chip b {{ margin-left: 16px; font-variant-numeric: tabular-nums; }}
    #root .meter {{ left: 190px; top: 1330px; width: 700px; height: 96px; border-radius: 48px; overflow: hidden; opacity: 0; }}
    #root .meter i {{ position: absolute; inset: 0; background: linear-gradient(90deg, rgba(255,255,255,0.55), #fff); transform-origin: 0 50%; transform: scaleX(0.06); }}
    #root .meter span {{ mix-blend-mode: difference; position: absolute; left: 0; top: 0; width: 100%; line-height: 92px; text-align: center; font-weight: 700; font-size: 40px; letter-spacing: 0.24em; }}
    #root .vq {{ left: 140px; top: 650px; width: 800px; height: 520px; border-radius: 64px; opacity: 0; }}
    #root .ban {{ left: 150px; width: 780px; height: 112px; border-radius: 40px; display: flex; align-items: center; gap: 24px; padding: 0 30px; font-weight: 600; font-size: 44px; white-space: nowrap; opacity: 0; }}
    #root .ban b {{ width: 62px; height: 62px; border-radius: 18px; background: #ff3b30; flex: none; }}
    #root .ringc {{ left: 430px; top: 1290px; width: 220px; height: 220px; border-radius: 50%; display: flex; align-items: center; justify-content: center; opacity: 0; }}
    #root .ringc svg {{ position: absolute; inset: 22px; width: 176px; height: 176px; }}
    #root .ringc b {{ font-weight: 700; font-size: 64px; }}
    #root .capw {{ left: 0; top: 1640px; width: {W}px; display: flex; justify-content: center; }}
    #root .capw div {{ font-weight: 600; font-size: 50px; letter-spacing: -0.01em; padding: 18px 44px 22px; border-radius: 52px; white-space: nowrap; background: rgba(20,20,28,0.42); -webkit-backdrop-filter: blur(24px) saturate(160%); backdrop-filter: blur(24px) saturate(160%); border: 1.5px solid rgba(255,255,255,0.28); box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.4); }}
"""
J = []; a = J.append
SFX = []; sx = lambda t, f, v=0.3: SFX.append((round(max(0, t), 2), f, v))
def rise(sel, t, d=0.7, y=40):
    a(f'tl.fromTo("{sel}", {{ opacity: 0, y: {y}, filter: "blur(14px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: {d}, ease: "power4.out" }}, {t:.2f});')
def spring(sel, t, d=0.7, s0=0.6):
    a(f'tl.fromTo("{sel}", {{ opacity: 0, scale: {s0} }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "back.out(1.6)" }}, {t:.2f});')

# background drifts for the whole film
for i, (dx, dy) in enumerate(((160, 220), (-200, 260), (-180, -240), (220, -160), (120, 200), (200, -140), (-220, -120))):
    a(f'tl.fromTo("#bl{i}", {{ x: 0, y: 0, scale: 1 }}, {{ x: {dx}, y: {dy}, scale: 1.18, duration: {DUR / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);')
# scenes dissolve with a soft scale + blur; the capsule morphs
SMAP = [0, 0, 2, 3, 4, 5, 6]            # feed scene (0) stays under chapter 1
a('tl.set("#sc0", { opacity: 1 }, 0);')
for n in range(1, 7):
    tb = B[n]
    if n == 1:
        a(f'tl.to("#tt0", {{ opacity: 0, y: -30, filter: "blur(12px)", duration: 0.35, ease: "power2.in" }}, {tb - 0.3:.2f}); tl.set("#sc1", {{ opacity: 1 }}, {tb:.2f});')
    else:
        prev = [f"#sc{SMAP[n - 1]}"] + (["#sc1"] if n == 2 else [])
        a(f'tl.to({json.dumps(prev)}, {{ opacity: 0, scale: 1.05, filter: "blur(16px)", duration: 0.38, ease: "power2.in" }}, {tb - 0.3:.2f});')
        a(f'tl.fromTo("#sc{n}", {{ opacity: 0, scale: 0.93, filter: "blur(16px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.7, ease: "power4.out" }}, {tb + 0.02:.2f});')
    txt, wd = ISL[n]
    a(f'tl.to("#islt", {{ opacity: 0, duration: 0.15 }}, {tb - 0.2:.2f}); tl.call(() => {{ $("#islt").innerHTML = {json.dumps(txt)}; }}, null, {tb - 0.04:.2f});')
    a(f'tl.to("#isl", {{ width: {wd}, x: {(430 - wd) / 2}, duration: 0.65, ease: "back.out(1.5)" }}, {tb - 0.08:.2f}); tl.to("#islt", {{ opacity: 1, duration: 0.3 }}, {tb + 0.12:.2f});'); sx(tb - 0.1, "swipe1", 0.22); sx(tb + 0.05, "pop", 0.26)
a('tl.call(() => { $("#islt").innerHTML = "Why you scroll"; }, null, 0);')
a('tl.fromTo("#isl", { y: -220 }, { y: 0, duration: 0.8, ease: "back.out(1.4)" }, 0.05);')

# ---- 0 hook + 1 endless feed (one phone)
rise("#tt0a", 0.08, 0.5); rise("#tt0b", w("r1", "you", 1) + 0.05, 0.5)
a('tl.fromTo("#ph", { opacity: 0, y: 90, scale: 0.86 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.5)" }, 0);'); sx(0, "swipe2", 0.26)
ts = w("r1", "built") - 0.3
a(f'tl.to("#bp", {{ opacity: 1, duration: 0.4 }}, {ts:.2f});'); sx(ts, "zoom_whoosh", 0.3)
for i, pid in enumerate(HID):
    (x0, y0, s0), (gx, gy) = HOOK[i], GRIDP[i]
    a(f'tl.to("#{pid}", {{ x: {gx - x0}, y: {gy - y0}, rotation: 0, scale: {110 / s0:.2f}, duration: 0.6, ease: "back.out(1.5)" }}, {ts + i * 0.02:.2f});')
    if i % 4 == 0: sx(ts + 0.2 + i * 0.02, "ui_tick2", 0.3)
for pid in (J1, J2): a(f'tl.to("#{pid}", {{ opacity: 0, scale: 0.5, duration: 0.25 }}, {ts:.2f});')
a(f'tl.fromTo("#ph", {{ rotation: 0 }}, {{ rotation: 1.6, duration: 0.07, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }}, 0.7);')
a(f'tl.fromTo("#feed", {{ y: 0 }}, {{ y: -{212 * 20}, duration: {B[2]:.2f}, ease: "none" }}, 0);')
a(f'tl.fromTo("#sth", {{ y: 0 }}, {{ y: 300, duration: {B[1]:.2f}, ease: "power1.out" }}, 0);')
a(f'tl.to("#sth", {{ y: 150, height: 60, duration: 1.1, ease: "power2.inOut" }}, {w("r2", "never") - 0.1:.2f}); tl.to("#sth", {{ y: 90, height: 34, duration: 1.4, ease: "power2.inOut" }}, {w("r2", "no"):.2f});')
for k in range(int(B[2] / 1.15)):
    t0 = 0.5 + k * 1.15
    a(f'tl.fromTo("#thb", {{ opacity: 0, y: 0, scale: 0.8 }}, {{ opacity: 0.9, y: -60, scale: 1, duration: 0.22, ease: "power2.out", immediateRender: false }}, {t0:.2f}); tl.to("#thb", {{ y: -330, opacity: 0, duration: 0.5, ease: "power2.in" }}, {t0 + 0.22:.2f});'); sx(t0 + 0.2, "ui_tick2", 0.16)
rise("#tt1a", w("r2", "feed") - 0.15); rise("#tt1b", w("r2", "never") - 0.1)
spring("#ch1", w("r2", "last") - 0.15); sx(w("r2", "last") - 0.15, "pop", 0.3)
# ---- 2 slot machine
rise("#tt2a", w("r3", "rewards") - 0.15); rise("#tt2b", w("r3", "random") - 0.1)
t_spin = w("r3", "most") - 0.3
for i, stop in enumerate((w("r3", "boring") + 0.25, w("r3", "boring") + 0.55, w("r3", "great") + 0.15)):
    a(f'tl.fromTo("#st{i}", {{ y: 0 }}, {{ y: -{330 * 9}, duration: {stop - t_spin:.2f}, ease: "power3.out" }}, {t_spin:.2f});'); sx(stop - 0.1, "clunk", 0.34)
sx(t_spin, "count_fast", 0.3)
a(f'tl.fromTo("#spn", {{ opacity: 0, rotation: 0 }}, {{ opacity: 1, rotation: 720, duration: 1.2, ease: "power1.inOut" }}, {t_spin - 0.5:.2f}); tl.to("#spn", {{ opacity: 0, duration: 0.2 }}, {t_spin + 0.7:.2f});')
tg = w("r3", "great") + 0.15
a(f'tl.to("#rl2", {{ scale: 1.1, boxShadow: "inset 0 2px 0 rgba(255,255,255,0.7), 0 0 80px rgba(255,255,255,0.45)", duration: 0.5, ease: "back.out(2.2)" }}, {tg:.2f});'); sx(tg, "kaching", 0.34); sx(tg, "shimmer", 0.3)
a(f'tl.to(["#rl0", "#rl1", "#rl2"], {{ y: -14, duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {w("r3", "slot"):.2f});')
# ---- 3 autoplay
rise("#tt3a", w("r4", "autoplay") - 0.15); rise("#tt3b", w("r4", "for") - 0.1)
a('gsap.set("#v1", { x: 1000, opacity: 1 });')
tn = w("r4", "autoplay") + 0.2; te = w("r4", "can") - 0.15
spring("#nx", tn - 0.1)
a(f'tl.to("#nxr", {{ strokeDashoffset: 0, duration: {te - tn:.2f}, ease: "none" }}, {tn:.2f});')
for k, lab in enumerate(("3", "2", "1")):
    a(f'tl.call(() => {{ $("#nxn").textContent = "{lab}"; }}, null, {tn + k * (te - tn) / 3:.2f});'); sx(tn + k * (te - tn) / 3, "ui_tick2", 0.34)
a(f'tl.to("#v0", {{ x: -1000, duration: 0.7, ease: "power4.inOut" }}, {te:.2f}); tl.to("#v1", {{ x: 0, duration: 0.7, ease: "power4.inOut" }}, {te:.2f});'); sx(te, "zoom_whoosh", 0.3)
# ---- 4 red badges
rise("#tt4a", w("r5", "red") - 0.15); rise("#tt4b", w("r5", "urgent") - 0.1)
for i in range(9): spring(f"#ap{i}", B[4] + 0.1 + i * 0.05, 0.6, 0.5)
for k, i in enumerate((0, 2, 4, 5, 7)):
    t0 = w("r5", "badges") - 0.2 + k * 0.22
    a(f'tl.to("#bd{i}", {{ scale: 1, duration: 0.5, ease: "back.out(3)" }}, {t0:.2f});'); sx(t0, "ping", 0.3)
    a(f'tl.to("#bd{i}", {{ scale: 1.22, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {w("r5", "urgent") + k * 0.07:.2f});')
# ---- 5 your own stop
rise("#tt5a", w("r6", "add") - 0.15); rise("#tt5b", w("r6", "own") - 0.1)
a(f'tl.fromTo("#pn", {{ opacity: 0, y: 120, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "power4.out" }}, {B[5] + 0.15:.2f});')
t0 = w("r6", "autoplay") - 0.1
a(f'tl.to("#tk0", {{ x: 0, duration: 0.4, ease: "back.out(1.6)" }}, {t0:.2f}); tl.to("#tg0", {{ backgroundColor: "rgba(120,120,128,0.5)", duration: 0.3 }}, {t0:.2f});'); sx(t0, "ui_tick2", 0.45)
t1 = w("r6", "grayscale") - 0.1
a(f'tl.to("#tk1", {{ x: 70, duration: 0.4, ease: "back.out(1.6)" }}, {t1:.2f}); tl.to("#tg1", {{ backgroundColor: "#30d158", duration: 0.3 }}, {t1:.2f});'); sx(t1, "ui_tick2", 0.45)
a(f'tl.to("#bg", {{ filter: "grayscale(1) brightness(0.7)", duration: 0.9, ease: "power2.inOut" }}, {t1 + 0.1:.2f});'); sx(t1 + 0.1, "swipe2", 0.26)
a(f'tl.to("#tg1", {{ backgroundColor: "#b9b9c0", duration: 0.9 }}, {t1 + 0.3:.2f});')
t2 = w("r6", "timer") - 0.15
a(f'tl.to("#tm", {{ opacity: 1, scale: 1.12, duration: 0.3, ease: "back.out(2)" }}, {t2:.2f}); tl.to("#tm", {{ scale: 1, duration: 0.3 }}, {t2 + 0.3:.2f});'); sx(t2, "clock_tick", 0.6)
a(f'(() => {{ const o = {{ v: 1200 }}; tl.fromTo(o, {{ v: 1200 }}, {{ v: 1197, duration: {B[6] - t2 - 0.3:.2f}, ease: "none", immediateRender: false, onUpdate: () => {{ const s = Math.ceil(o.v); $("#tm").textContent = String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0"); }} }}, {t2 + 0.3:.2f}); }})();')
# ---- 6 it's the design
a(f'tl.fromTo("#pl", {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.9, ease: "back.out(1.3)" }}, {B[6] + 0.05:.2f});')
rise("#tt6a", w("r7", "its") - 0.05); rise("#tt6b", w("r7", "its", 1) - 0.05); sx(w("r7", "design"), "shimmer", 0.34); sx(w("r7", "its") - 0.05, "impact", 0.3)
a(f'tl.to("#bg", {{ filter: "grayscale(0) brightness(1)", duration: 1.6, ease: "power2.inOut" }}, {w("r7", "design") + 0.1:.2f});')
a(f'tl.to("#isl", {{ y: -220, duration: 0.5, ease: "power2.in" }}, {B[6] + 0.1:.2f});')
sx(0, "boom_open", 0.24)

# ---- generic pops
for n, (pid, t, out, drift, rot) in enumerate(POPS):
    a(f'tl.fromTo("#{pid}", {{ opacity: 0, scale: 0, rotation: {rot - 28} }}, {{ opacity: 1, scale: 1, rotation: {rot}, duration: 0.5, ease: "back.out(2.6)" }}, {t:.2f});')
    if drift: a(f'tl.to("#{pid}", {{ x: {drift[0]:.0f}, y: {drift[1]:.0f}, opacity: 0, rotation: {rot + 90}, duration: {drift[2]}, ease: "power2.out" }}, {t + 0.1:.2f});')
    if out: a(f'tl.to("#{pid}", {{ opacity: 0, scale: 0.4, duration: 0.3 }}, {out:.2f});')
    if not drift and n % 2 == 0: sx(t, "pop", 0.26)
    elif not drift: sx(t, "ui_tick", 0.3)
# 1 extras
a(f'tl.to({json.dumps(["#" + p for p in HID] + ["#" + BD, "#bp"])}, {{ opacity: 0, scale: 0.4, duration: 0.35, ease: "power2.in" }}, {B[1] - 0.25:.2f});')
for i, (x, dl, scl) in enumerate(FLY):
    t0 = B[1] + 0.1 + dl * 0.6; d = 2.4 / scl
    a(f'tl.fromTo("#fy{i}", {{ y: 0, opacity: 0.95 }}, {{ y: -2150, opacity: 0.95, duration: {d:.2f}, ease: "none", repeat: {max(0, int((B[2] - t0) / d) - 0)}, immediateRender: false }}, {t0:.2f});')
a(f'tl.fromTo("#cnt1", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, {B[1] + 0.3:.2f});')
a(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 248, duration: {B[2] - B[1] - 0.6:.2f}, ease: "none", immediateRender: false, onUpdate: () => {{ $("#cn1").textContent = Math.round(o.v); }} }}, {B[1] + 0.3:.2f}); }})();')
te1 = w("r2", "no") - 0.2
a(f'tl.fromTo("#endc", {{ opacity: 0, scale: 0.5, rotation: -6 }}, {{ opacity: 1, scale: 1, rotation: -3, duration: 0.5, ease: "back.out(2)" }}, {te1:.2f});'); sx(te1, "pop", 0.34)
a(f'tl.to("#endc", {{ x: 620, y: -520, rotation: 46, opacity: 0, duration: 0.55, ease: "power2.in" }}, {w("r2", "page") + 0.15:.2f});'); sx(w("r2", "page") + 0.15, "swipe2", 0.34)
# 2 extras
a(f'tl.fromTo("#mt", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power4.out" }}, {B[2] + 0.35:.2f});')
a(f'tl.to("#mtf", {{ scaleX: 0.16, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {w("r3", "most"):.2f}); tl.to("#mtf", {{ scaleX: 1, duration: 0.5, ease: "back.out(1.6)" }}, {TG:.2f});'); sx(TG, "riser", 0.26)
# 3 extras
a(f'tl.fromTo("#vq0", {{ opacity: 0, y: 0, scale: 1 }}, {{ opacity: 0.8, y: -52, scale: 0.92, duration: 0.6, ease: "back.out(1.6)" }}, {B[3] + 0.25:.2f}); tl.fromTo("#vq1", {{ opacity: 0, y: 0, scale: 1 }}, {{ opacity: 0.6, y: -100, scale: 0.84, duration: 0.6, ease: "back.out(1.6)" }}, {B[3] + 0.35:.2f});')
a(f'tl.to("#vq0", {{ y: 0, scale: 1, opacity: 0, duration: 0.7, ease: "power4.inOut" }}, {te:.2f}); tl.to("#vq1", {{ y: -52, scale: 0.92, opacity: 0.8, duration: 0.7, ease: "power4.inOut" }}, {te:.2f});')
# 4 extras
for i, (wd, nth, x0) in enumerate((("red", 1, 1100), ("even", 0, -1100))):
    tbn = w("r5", wd, nth) - 0.1
    a(f'tl.fromTo("#bn{i}", {{ opacity: 0, x: {x0} }}, {{ opacity: 1, x: 0, duration: 0.7, ease: "back.out(1.3)" }}, {tbn:.2f});'); sx(tbn, "ping", 0.36)
for pid in BELLS: a(f'tl.fromTo("#{pid}", {{ rotation: -16 }}, {{ rotation: 16, duration: 0.09, yoyo: true, repeat: {int((B[5] - w("r5", "urgent")) / 0.09)}, ease: "sine.inOut", immediateRender: false }}, {w("r5", "urgent"):.2f});')
a(f'tl.fromTo("#sc4", {{ x: 0 }}, {{ x: 9, duration: 0.05, yoyo: true, repeat: 11, ease: "sine.inOut", immediateRender: false }}, {w("r5", "urgent"):.2f});')
# 5 extras
a(f'tl.fromTo("#rc", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(2)" }}, {t2 - 0.1:.2f}); tl.to("#rcr", {{ strokeDashoffset: 40, duration: {B[6] - t2:.2f}, ease: "power2.out" }}, {t2:.2f});')

# captions as glass capsules
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
    caps.append(f'<div id="cap{i}" class="abs capw clip" data-start="{s0}" data-duration="{round(min(e2, DUR - 0.05) - s0, 2)}"><div>{" ".join(x for x, _ in ws)}</div></div>')

open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    {body}
    {chr(10).join(caps)}
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
{chr(10).join(aud)}
</div>
<script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>
""")
print("duration", DUR, "sfx", len(SFX))
print({k: round(v, 2) for k, v in at.items()})
