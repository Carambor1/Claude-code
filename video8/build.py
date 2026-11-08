#!/usr/bin/env python3
""""Nobody's Coming" — ~40 s vertical motivational Short in the DLF style. English, Sarah (passionate), no music.
Timeline from vo.json. Run: python3 build.py"""
import json, re, subprocess

VO = json.load(open("vo.json"))
ORDER = [f"n{i}" for i in range(1, 11)]
GAP = {"n1": 0.2, "n2": 0.1, "n3": 0.45, "n4": 0.3, "n5": 0.35, "n6": 0.3, "n7": 0.4, "n8": 0.3, "n9": 0.45}
T, at = 0.15, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.15)
DUR = round(T + 0.9, 2)

def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)

E = dict(parents=w("n2", "parents"), boss=w("n2", "boss"), algo=w("n2", "algorithm"), you=at["n3"],
         harsh=w("n4", "harsh"), freedom=w("n4", "freedom"), stop=w("n5", "stop"),
         perm=w("n6", "permission"), perf=w("n6", "perfect"), mon=w("n6", "monday"),
         hour=w("n7", "hour"), rep=w("n7", "rep"), page=w("n7", "page"), call=w("n7", "call"),
         six=w("n8", "six"), recog=w("n8", "recognize"), ask=w("n9", "ask"), smile=w("n9", "smile"),
         wait=w("n10", "waiting"), coming=w("n10", "coming"))

FIG = '<svg viewBox="0 0 80 130"><circle cx="40" cy="24" r="20" fill="{c}"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="{c}"/></svg>'
S = 'fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"'
ICON = {"hour": f'<circle cx="50" cy="50" r="38" {S}/><path d="M50 28v24l14 10" {S}/>',
        "rep": f'<path d="M14 36v28M26 28v44M74 28v44M86 36v28M26 50h48" {S}/>',
        "page": f'<path d="M50 26c-10-8-26-8-36-4v54c10-4 26-4 36 4c10-8 26-8 36-4V22c-10-4-26-4-36 4zM50 26v54" {S}/>',
        "call": f'<rect x="30" y="12" width="40" height="76" rx="8" {S}/><circle cx="50" cy="76" r="3" fill="#fff"/>'}

def C(id, cls, style, inner=""):
    return f'<div id="{id}" class="abs {cls} clip" data-start="0" data-duration="{DUR}" style="{style}">{inner}</div>'

TITLES = {"t1": "Nobody’s <i>coming</i>", "t2": "Not <i>them</i>.", "t3": "You.", "t4": "It’s <i>freedom</i>.",
          "t5": "Nobody can <i>stop</i> you", "t6": "No <i>excuses</i>.", "t7": "One <i>step</i> a day.",
          "t8": "6 months <i>later</i>", "t9": "They’ll <i>ask</i>.", "t10": "Nobody’s <i>coming</i>"}
chain = "".join(f'<div class="lk" id="lk{i}" style="left:{i * 34}px"></div>' for i in range(7))
segs = "".join(f'<div class="sg"><div class="sgf" id="sg{i}"></div></div>' for i in range(6))
body = [C(k, "ctr title" + (" huge" if k == "t3" else ""), "top:250px", v) for k, v in TITLES.items()] + [
    C("spot", "", "left:340px;top:0;width:400px;height:1100px;background:linear-gradient(180deg,rgba(255,255,255,0.22),rgba(255,255,255,0.03));clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)"),
    C("pool", "", "left:330px;top:1060px;width:420px;height:80px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,255,255,0.35),rgba(255,255,255,0) 70%)"),
    C("ground", "", "left:0;top:1100px;width:1080px;height:0;border-top:2px dashed rgba(255,255,255,0.32)"),
    C("gP", "", "left:70px;top:960px;width:220px;height:140px", f'<div class="ch" style="left:20px;top:-70px">Parents</div><div style="position:absolute;left:10px;top:10px;width:80px;height:130px">{FIG.format(c="#cfcfcf")}</div><div style="position:absolute;left:110px;top:20px;width:74px;height:120px">{FIG.format(c="#cfcfcf")}</div>'),
    C("gB", "", "left:820px;top:960px;width:160px;height:140px", f'<div class="ch" style="left:10px;top:-70px">Boss</div><div style="position:absolute;left:30px;top:10px;width:80px;height:130px">{FIG.format(c="#cfcfcf")}</div>'),
    C("gA", "", "left:770px;top:640px;width:240px;height:180px", f'<div class="ch" style="left:0;top:0">Algorithm</div><svg style="position:absolute;left:70px;top:60px;width:100px;height:100px" viewBox="0 0 100 100">{ICON["call"]}</svg>'),
    C("chain", "", "left:250px;top:1000px;width:240px;height:20px", chain),
    C("wl", "", "left:360px;top:820px;width:16px;height:280px;background:#fff;border-radius:6px"),
    C("wr", "", "left:704px;top:820px;width:16px;height:280px;background:#fff;border-radius:6px"),
    C("fig", "glow", "left:480px;top:905px;width:120px;height:195px", FIG.format(c="#fff")),
    C("star", "glow", "left:510px;top:820px;width:60px;height:60px", '<svg viewBox="0 0 80 80"><path d="M40 4 L49 30 L76 30 L54 47 L62 74 L40 58 L18 74 L26 47 L4 30 L31 30 Z" fill="#fff"/></svg>'),
    C("x6", "", "left:0;top:520px;width:1080px", "".join(f'<div class="xc" id="x{i}"><span>{t}</span><div class="xs" id="xs{i}"></div></div>' for i, t in enumerate(["Permission", "Perfect moment", "Monday"]))),
    C("ic", "", "left:140px;top:560px;width:800px;height:200px", "".join(f'<div class="icn" id="ic{k}"><svg viewBox="0 0 100 100">{ICON[k]}</svg></div>' for k in ("hour", "rep", "page", "call"))),
    C("segs", "", "left:160px;top:1128px;width:760px;height:14px", segs),
    C("crowd", "", "left:40px;top:930px;width:400px;height:170px", "".join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s * 1.62:.0f}px">{FIG.format(c="#9a9a9a")}</div>' for x, y, s in ((20, 40, 80), (120, 60, 68), (210, 40, 80))) + "".join(f'<div class="ch bub" id="bb{i}" style="left:{x}px;top:{y}px">{t}</div>' for i, (x, y, t) in enumerate(((0, -40, "How?"), (110, -90, "???"), (220, -40, "Wait…"))))),
    C("fl", "", "left:0;top:0;width:1080px;height:1920px;background:#fff"),
]
HIDE = [f"#t{i}" for i in range(2, 11)] + ["#spot", "#pool", "#chain", "#wl", "#wr", "#star", "#x6", "#ic", "#segs", "#crowd", "#fl", "#gA"]
CSS = """
    #root { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 60%, #161616 0%, #000 70%); font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }
    #root .abs { position: absolute; }
    #root .ctr { left: 0; width: 1080px; text-align: center; }
    #root .glow { filter: drop-shadow(0 0 16px rgba(255,255,255,0.55)); }
    #root svg { width: 100%; height: 100%; display: block; }
    #root .title { font-weight: 900; font-size: 104px; letter-spacing: -0.02em; text-transform: uppercase; line-height: 1.02; padding: 0 60px; filter: drop-shadow(0 0 18px rgba(255,255,255,0.45)); }
    #root .title i { font-family: "Playfair Display", serif; font-style: italic; font-weight: 400; text-transform: none; letter-spacing: 0; }
    #root .huge { font-size: 260px; top: 230px; }
    #root .ch { position: absolute; font-weight: 800; font-size: 28px; letter-spacing: 0.14em; text-transform: uppercase; color: #fff; background: #111; border: 2px solid #fff; border-radius: 999px; padding: 8px 20px; white-space: nowrap; }
    #root .lk { position: absolute; top: 0; width: 40px; height: 20px; border: 5px solid #cfcfcf; border-radius: 10px; }
    #root .xc { position: relative; margin: 0 auto 26px; width: fit-content; font-weight: 800; font-size: 48px; letter-spacing: 0.12em; text-transform: uppercase; padding: 14px 34px; border: 3px solid #fff; border-radius: 999px; background: #0d0d0d; }
    #root .xs { position: absolute; left: 14px; right: 14px; top: 50%; height: 8px; margin-top: -4px; background: #fff; border-radius: 4px; transform-origin: 0% 50%; transform: scaleX(0); }
    #root .icn { position: absolute; top: 0; width: 170px; height: 170px; }
    #root #ichour { left: 0; } #root #icrep { left: 210px; } #root #icpage { left: 420px; } #root #iccall { left: 630px; }
    #root .sg { float: left; width: 118px; height: 14px; margin-right: 10px; border-radius: 7px; background: #2a2a2a; overflow: hidden; }
    #root .sgf { width: 100%; height: 100%; background: #fff; transform-origin: 0% 50%; transform: scaleX(0); }
""" + "    " + ", ".join(f"#root {h}" for h in HIDE) + " { opacity: 0; }\n"

J = []; a = J.append
def title_swap(old, new, t, big=False):
    a(f'tl.to("#{old}", {{ opacity: 0, y: -40, filter: "blur(8px)", duration: 0.22, ease: "power2.in" }}, {t - 0.2:.2f});')
    a(f'tl.fromTo("#{new}", {{ opacity: 0, y: 40, scale: {1.4 if big else 1}, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: {0.18 if big else 0.32}, ease: "{"power4.in" if big else "power3.out"}" }}, {t:.2f});')
# hook: the others turn away
a(f'tl.fromTo("#gA", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {at["n2"] - 0.3:.2f});')
title_swap("t1", "t2", E["parents"])
for g, t, dx in (("gP", E["parents"], -60), ("gB", E["boss"], 60), ("gA", E["algo"], 60)):
    a(f'tl.to("#{g}", {{ opacity: 0.18, x: {dx}, duration: 0.45, ease: "power2.out" }}, {t:.2f});')
# YOU: spotlight slams on
title_swap("t2", "t3", E["you"], big=True)
a(f'tl.to(["#gP", "#gB", "#gA"], {{ opacity: 0, duration: 0.3 }}, {E["you"]:.2f});')
a(f'tl.fromTo(["#spot", "#pool"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08 }}, {E["you"]:.2f});')
a(f'tl.fromTo("#fl", {{ opacity: 0 }}, {{ opacity: 0.35, duration: 0.04 }}, {E["you"]:.2f}); tl.to("#fl", {{ opacity: 0, duration: 0.35 }}, {E["you"] + 0.05:.2f});')
a(f'tl.fromTo("#fig", {{ scale: 1, transformOrigin: "50% 100%" }}, {{ scale: 1.12, duration: 0.25, ease: "back.out(3)" }}, {E["you"]:.2f});')
# freedom: chain snaps
a(f'tl.fromTo("#chain", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {E["harsh"] - 0.3:.2f});')
title_swap("t3", "t4", E["freedom"])
for i in range(7):
    a(f'tl.to("#lk{i}", {{ x: {(i - 3) * 40}, y: {150 + (i % 3) * 40}, rotation: {(i * 53) % 180 - 90}, opacity: 0, duration: 0.7, ease: "power2.in" }}, {E["freedom"]:.2f});')
# nobody can stop you: walls fall
a(f'tl.fromTo(["#wl", "#wr"], {{ opacity: 0, scaleY: 0, transformOrigin: "50% 100%" }}, {{ opacity: 1, scaleY: 1, duration: 0.35, ease: "power3.out" }}, {at["n5"]:.2f});')
title_swap("t4", "t5", E["stop"])
a(f'tl.to("#wl", {{ rotation: -90, x: -140, transformOrigin: "50% 100%", opacity: 0, duration: 0.55, ease: "power2.in" }}, {E["stop"] + 0.1:.2f});')
a(f'tl.to("#wr", {{ rotation: 90, x: 140, transformOrigin: "50% 100%", opacity: 0, duration: 0.55, ease: "power2.in" }}, {E["stop"] + 0.18:.2f});')
# no excuses
title_swap("t5", "t6", E["perm"])
a(f'tl.fromTo("#x6", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {E["perm"] - 0.1:.2f});')
for i, t in enumerate((E["perm"], E["perf"], E["mon"])):
    a(f'tl.fromTo("#x{i}", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power3.out" }}, {t - 0.15:.2f});')
    a(f'tl.to("#xs{i}", {{ scaleX: 1, duration: 0.18, ease: "power2.out" }}, {t + 0.35:.2f});')
    a(f'tl.to("#x{i}", {{ opacity: 0.35, duration: 0.2 }}, {t + 0.55:.2f});')
a(f'tl.to("#x6", {{ opacity: 0, duration: 0.25 }}, {at["n7"] - 0.1:.2f});')
# one step a day
title_swap("t6", "t7", E["hour"])
a(f'tl.fromTo("#ic", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {E["hour"] - 0.1:.2f});')
for k in ("hour", "rep", "page", "call"):
    a(f'tl.fromTo("#ic{k}", {{ opacity: 0, scale: 0.4, y: 30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(2.5)" }}, {E[k] - 0.05:.2f});')
a(f'tl.to("#ic", {{ opacity: 0, y: -30, duration: 0.25 }}, {at["n8"] - 0.15:.2f});')
# six months later: walk the bar
a(f'tl.to(["#spot", "#pool"], {{ opacity: 0, duration: 0.3 }}, {at["n8"] - 0.2:.2f});')
title_swap("t7", "t8", E["six"])
a(f'tl.fromTo("#segs", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {at["n8"] - 0.2:.2f});')
a(f'tl.to("#fig", {{ x: -320, scale: 1, duration: 0.3, ease: "power2.inOut" }}, {at["n8"] - 0.55:.2f});')
walk = E["recog"] + 0.3 - E["six"]
for i in range(6):
    a(f'tl.to("#sg{i}", {{ scaleX: 1, duration: {walk / 6:.2f}, ease: "none" }}, {E["six"] + i * walk / 6:.2f});')
a(f'tl.to("#fig", {{ x: 320, duration: {walk:.2f}, ease: "none" }}, {E["six"]:.2f});')
for j in range(int(walk / 0.5)):
    a(f'tl.to("#fig", {{ y: -10, duration: 0.12, yoyo: true, repeat: 1, ease: "sine.out" }}, {E["six"] + j * 0.5:.2f});')
a(f'tl.fromTo("#star", {{ opacity: 0, scale: 0.3, x: 320 }}, {{ opacity: 1, scale: 1, x: 320, duration: 0.4, ease: "back.out(3)" }}, {E["recog"] + 0.3:.2f});')
a(f'tl.fromTo("#fig", {{ filter: "drop-shadow(0 0 16px rgba(255,255,255,0.55))" }}, {{ filter: "drop-shadow(0 0 40px rgba(255,255,255,0.95))", duration: 0.5, immediateRender: false }}, {E["recog"] + 0.3:.2f});')
# they'll ask
title_swap("t8", "t9", E["ask"])
a(f'tl.fromTo("#crowd", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {E["ask"] - 0.2:.2f});')
for i in range(3):
    a(f'tl.fromTo("#bb{i}", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }}, {E["ask"] + 0.15 + i * 0.22:.2f});')
a(f'tl.to("#segs", {{ opacity: 0, duration: 0.3 }}, {E["ask"]:.2f});')
# loop back to the opening frame
a(f'tl.to(["#crowd", "#star"], {{ opacity: 0, duration: 0.35 }}, {at["n10"] - 0.1:.2f});')
a(f'tl.to("#fig", {{ x: 0, duration: 0.6, ease: "power2.inOut", filter: "drop-shadow(0 0 16px rgba(255,255,255,0.55))" }}, {at["n10"]:.2f});')
title_swap("t9", "t10", at["n10"] + 0.25)

open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="1080" data-height="1920" data-layout-allow-overlap>
    {chr(10).join("    " + b for b in body)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
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
    #root .cap {{ left: 90px; width: 900px; top: 1190px; text-align: center; font-weight: 800; font-size: 56px; line-height: 1.15; color: #fff; }}
    #root .cap span {{ display: inline-block; background: rgba(0,0,0,0.86); padding: 6px 22px 10px; border-radius: 16px; }}
  </style>
  <div id="root" data-composition-id="cap" data-width="1080" data-height="1920">
{chr(10).join("    " + c for c in caps)}
  </div>
  <script>window.__timelines["cap"] = gsap.timeline({{ paused: true }});</script>
</template>
""")

SFX = [(0.0, "boom_open", 0.45), (E["parents"], "swipe1", 0.5), (E["boss"], "swipe2", 0.5), (E["algo"], "swipe1", 0.5),
       (E["you"] - 0.03, "spot", 1.0), (E["you"], "impact", 0.8), (E["freedom"] - 0.05, "chain", 0.9),
       (E["stop"] + 0.1, "impact", 0.45), (E["stop"] + 0.1, "zoom_whoosh", 0.45),
       (E["perm"] + 0.3, "strike", 0.7), (E["perf"] + 0.3, "strike", 0.7), (E["mon"] + 0.3, "strike", 0.7),
       (E["hour"] - 0.05, "pop", 0.5), (E["rep"] - 0.05, "pop", 0.5), (E["page"] - 0.05, "pop", 0.5), (E["call"] - 0.05, "pop", 0.5),
       (E["six"], "footsteps", 0.9), (E["six"] + 0.5, "riser", 0.45), (E["recog"] + 0.3, "shimmer", 0.6), (E["recog"] + 0.3, "impact", 0.5),
       (E["ask"], "murmur", 0.7), (at["n10"], "heartbeat", 0.6), (at["n10"] + 0.25, "swipe2", 0.4)]
dur = {f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/sfx/{f}.mp3"], capture_output=True, text=True).stdout) for f in {x[1] for x in SFX}}
aud = [f'  <audio id="vo-{k}" class="clip" src="assets/vo/{k}.mp3" data-start="{round(at[k], 2)}" data-duration="{round(VO[k]["dur"] - 0.01, 2)}" data-track-index="2" data-volume="1.8"></audio>' for k in ORDER]
aud += [f'  <audio id="sx{n}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(t, 2)}" data-duration="{round(min(dur[f], DUR - t) - 0.01, 2)}" data-track-index="{10 + n}" data-volume="{v}"></audio>' for n, (t, f, v) in enumerate(SFX)]
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
print("duration", DUR)
