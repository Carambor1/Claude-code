#!/usr/bin/env python3
""""Everything You Learned in School Was Wrong" — vertical Short, English, female voice, no music.
Timeline is derived from the voice durations (vo.json). Run: python3 vo.py (once), then python3 build.py"""
import json, os, subprocess

VO = json.load(open("vo.json"))
S = 'fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'
ICON = {
    1: f'<path d="M10 120 Q100 20 190 120 Q100 95 10 120 Z" {S}/><circle cx="100" cy="72" r="9" fill="#fff"/>',
    2: f'<path d="M50 130 V95 A50 50 0 0 1 150 95 V130 Z M50 95 Q20 85 18 40 Q40 70 60 75 M150 95 Q180 85 182 40 Q160 70 140 75" {S}/>',
    3: f'<path d="M30 80 Q90 20 150 80 Q90 140 30 80 Z M150 80 L185 50 L185 110 Z" {S}/><circle cx="62" cy="72" r="7" fill="#fff"/>',
    4: f'<path d="M10 140 V70 H35 V50 H60 V70 H85 V50 H110 V70 H135 V50 H160 V70 H190 V140 Z" {S}/><path d="M10 105 H190" {S}/>',
    5: f'<path d="M60 70 Q30 60 20 25 Q50 45 70 50 M140 70 Q170 60 180 25 Q150 45 130 50 M65 55 Q100 40 135 55 L125 120 Q100 145 75 120 Z" {S}/><circle cx="85" cy="85" r="6" fill="#fff"/><circle cx="115" cy="85" r="6" fill="#fff"/>',
    6: '<path d="M115 5 L50 90 H95 L75 155 L150 60 H105 Z" fill="#fff"/>',
    7: f'<path d="M100 30 C70 10 30 30 35 65 C10 80 20 120 50 125 C60 150 95 150 100 130 C105 150 140 150 150 125 C180 120 190 80 165 65 C170 30 130 10 100 30 Z M100 30 V130" {S}/>',
}
TRUTH = {1: ("1.69 m", "Average height for his era"), 2: ("1876", "The horns came from an opera"), 3: ("Months", "That's how long they remember"),
         4: ("~6 m", "Wide. Far too thin to see"), 5: ("No red", "They see movement, not colour"), 6: ("~20×", "Empire State Building, every year"),
         7: ("~100%", "Of your brain is in use")}
MYTH = {i: VO[f"m{i}"]["text"].rstrip(".") for i in range(1, 8)}

# ------------------------------------------------ timeline from the voice
T, vo_at, ev = 0.15, {}, {}
vo_at["h1"] = T; T += VO["h1"]["dur"] + 0.15
vo_at["h2"] = T; ev["h2"] = T; T += VO["h2"]["dur"] + 0.35
for i in range(1, 8):
    ev[f"in{i}"] = T
    vo_at[f"m{i}"] = T + 0.35
    me = vo_at[f"m{i}"] + VO[f"m{i}"]["dur"]
    ev[f"stamp{i}"] = me + 0.25
    ev[f"flip{i}"] = ev[f"stamp{i}"] + 0.8
    vo_at[f"t{i}"] = ev[f"flip{i}"] + 0.3
    te = vo_at[f"t{i}"] + VO[f"t{i}"]["dur"]
    ev[f"out{i}"] = te + 0.35
    T = te + 0.55
ev["end"] = T + 0.2
vo_at["e1"] = T + 0.9
DUR = round(vo_at["e1"] + VO["e1"]["dur"] + 3.2, 2)

# ------------------------------------------------ markup
def clip(id, cls, style, inner=""):
    return f'<div id="{id}" class="abs {cls} clip" data-start="0" data-duration="{DUR}" style="{style}">{inner}</div>'

cards = []
for i in range(1, 8):
    st, ln = TRUTH[i]
    cards.append(clip(f"c{i}", "card", "",
        f'<div class="face front" data-layout-allow-overlap><div class="tag">Myth #{i}</div><svg class="ic" viewBox="0 0 200 160">{ICON[i]}</svg>'
        f'<div class="myth">“{MYTH[i]}”</div><div class="stamp" id="st{i}" data-layout-allow-overlap>Wrong</div></div>'
        f'<div class="face back"><div class="tag">Truth</div><div class="stat" id="sv{i}">{st}</div><div class="line">{ln}</div></div>'))
dots = "".join(f'<span class="dot" id="d{i}"></span>' for i in range(1, 8))
minis = "".join(f'<div class="mini" id="mn{i}"><svg viewBox="0 0 200 160">{ICON[i]}</svg><span class="ms">Wrong</span></div>' for i in range(1, 8))

body = "\n    ".join([
    clip("hk-ic", "", "left:390px;top:420px;width:300px;height:240px", f'<svg viewBox="0 0 200 160" style="width:100%;height:100%">{ICON[1]}</svg>'),
    clip("hk-t", "ctr big glow", "top:720px;font-size:104px;line-height:1.05", "Napoleon<br>wasn’t short."),
    clip("hk-7", "ctr big glow", "top:620px;font-size:110px;line-height:1.05", "7 things<br>school got<br>wrong"),
    clip("top", "ctr", "top:200px", f'<div class="small">School myths</div><div class="dots">{dots}</div>'),
] + cards + [
    clip("fl", "", "left:0;top:0;width:1080px;height:1920px;background:#fff"),
    clip("q", "ctr big glow", "top:250px;font-size:84px;line-height:1.1", "Which one did<br>you believe?"),
    clip("grid", "", "left:84px;top:540px;width:912px;height:400px", minis),
    clip("blk", "", "left:0;top:0;width:1080px;height:1920px;background:#000"),
])

CSS = """
    #root { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, #161616 0%, #000 72%); font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }
    #root .abs { position: absolute; }
    #root .ctr { left: 0; width: 1080px; text-align: center; }
    #root .big { font-weight: 900; letter-spacing: -0.03em; }
    #root .glow { filter: drop-shadow(0 0 16px rgba(255,255,255,0.5)); }
    #root .small { font-weight: 700; font-size: 30px; letter-spacing: 0.22em; text-transform: uppercase; color: #9a9a9a; }
    #root .dots { margin-top: 18px; display: flex; justify-content: center; gap: 16px; }
    #root .dot { width: 22px; height: 22px; border-radius: 50%; border: 3px solid #555; }
    #root .card { left: 140px; top: 440px; width: 800px; height: 660px; transform-style: preserve-3d; }
    #root .face { position: absolute; inset: 0; border: 4px solid #fff; border-radius: 30px; background: #0b0b0b; backface-visibility: hidden; -webkit-backface-visibility: hidden;
                  display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 50px; text-align: center; box-shadow: 0 0 50px rgba(255,255,255,0.12); }
    #root .back { transform: rotateY(180deg); background: #f2f2f2; color: #000; }
    #root .tag { position: absolute; top: 34px; font-weight: 800; font-size: 30px; letter-spacing: 0.24em; text-transform: uppercase; color: #9a9a9a; }
    #root .back .tag { color: #555; }
    #root .ic { width: 230px; height: 184px; margin-bottom: 30px; }
    #root .myth { font-weight: 800; font-size: 60px; line-height: 1.12; }
    #root .stat { font-weight: 900; font-size: 170px; letter-spacing: -0.04em; line-height: 1; }
    #root .line { font-weight: 700; font-size: 44px; margin-top: 26px; line-height: 1.2; }
    #root .stamp { position: absolute; left: 150px; top: 300px; width: 500px; padding: 6px 0 10px; border: 10px solid #fff; border-radius: 18px; font-weight: 900; font-size: 100px;
                   letter-spacing: 0.06em; text-transform: uppercase; color: #fff; background: rgba(0,0,0,0.6); transform: rotate(-12deg); opacity: 0; }
    #root .mini { position: relative; float: left; width: 210px; height: 160px; margin: 0 9px 22px 9px; border: 3px solid #fff; border-radius: 18px; background: #0b0b0b; }
    #root .mini svg { position: absolute; left: 55px; top: 24px; width: 100px; height: 80px; opacity: 0.55; }
    #root .mini .ms { position: absolute; left: 22px; top: 52px; width: 166px; border: 5px solid #fff; border-radius: 10px; font-weight: 900; font-size: 38px; text-transform: uppercase; text-align: center; transform: rotate(-12deg); background: rgba(0,0,0,0.6); }
    #root #mn5 { margin-left: 123px; }
    #root .card, #root #hk-7, #root #top, #root #fl, #root #q, #root #grid, #root #blk { opacity: 0; }
"""

js = ['    const tl = gsap.timeline({ paused: true });']
a = js.append
# hook
a(f'tl.fromTo("#hk-ic", {{ y: 0 }}, {{ y: -14, duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut" }}, 0.4);')
a(f'tl.to(["#hk-ic", "#hk-t"], {{ opacity: 0, y: -30, duration: 0.35, ease: "power2.in" }}, {ev["h2"] + 0.9});')
a(f'tl.fromTo("#hk-7", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, {ev["h2"] + 1.15});')
a(f'tl.to("#hk-7", {{ opacity: 0, scale: 0.4, y: -480, duration: 0.45, ease: "power3.in" }}, {ev["in1"] - 0.3});')
a(f'tl.fromTo("#top", {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {ev["in1"] - 0.05});')
for i in range(1, 8):
    c = f"#c{i}"
    a(f'tl.fromTo("{c}", {{ opacity: 0, x: 900, rotation: 10 }}, {{ opacity: 1, x: 0, rotation: (i => i % 2 ? -1.5 : 1.5)({i}), duration: 0.5, ease: "power3.out" }}, {ev[f"in{i}"]});')
    a(f'tl.fromTo("#d{i}", {{ backgroundColor: "rgba(255,255,255,0)", borderColor: "#555" }}, {{ backgroundColor: "#ffffff", borderColor: "#ffffff", duration: 0.2 }}, {ev[f"in{i}"] + 0.2});')
    a(f'tl.fromTo("{c}", {{ scale: 1 }}, {{ scale: 1.035, duration: {ev[f"stamp{i}"] - ev[f"in{i}"] - 0.5:.2f}, ease: "none" }}, {ev[f"in{i}"] + 0.5});')
    # stamp: slam + shake + flash
    a(f'tl.fromTo("#st{i}", {{ opacity: 0, scale: 2.4 }}, {{ opacity: 1, scale: 1, duration: 0.14, ease: "power4.in" }}, {ev[f"stamp{i}"] - 0.14});')
    a(f'tl.fromTo("{c}", {{ x: 0 }}, {{ x: 14, duration: 0.04, yoyo: true, repeat: 5, ease: "none" }}, {ev[f"stamp{i}"]});')
    a(f'tl.fromTo("#fl", {{ opacity: 0 }}, {{ opacity: 0.18, duration: 0.04, immediateRender: false }}, {ev[f"stamp{i}"]});')
    a(f'tl.to("#fl", {{ opacity: 0, duration: 0.25 }}, {ev[f"stamp{i}"] + 0.05});')
    # flip to the truth
    a(f'tl.fromTo("{c}", {{ rotationY: 0, transformPerspective: 1800 }}, {{ rotationY: 180, duration: 0.55, ease: "power3.inOut" }}, {ev[f"flip{i}"]});')
    a(f'tl.fromTo("#sv{i}", {{ scale: 0.6 }}, {{ scale: 1, duration: 0.45, ease: "back.out(2.4)" }}, {ev[f"flip{i}"] + 0.45});')
    # out
    a(f'tl.to("{c}", {{ x: -1000, rotation: -12, opacity: 0, duration: 0.45, ease: "power3.in" }}, {ev[f"out{i}"]});')
# ending
a(f'tl.to("#top", {{ opacity: 0, duration: 0.3 }}, {ev["end"]});')
a(f'tl.fromTo("#q", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }}, {vo_at["e1"] - 0.1});')
a(f'tl.fromTo("#grid", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {ev["end"] + 0.2});')
a(f'tl.fromTo("#grid .mini", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.35, stagger: 0.09, ease: "back.out(2)" }}, {ev["end"] + 0.2});')
a(f'tl.fromTo("#grid .ms", {{ opacity: 0, scale: 2 }}, {{ opacity: 1, scale: 1, duration: 0.12, stagger: 0.09, ease: "power4.in" }}, {ev["end"] + 0.45});')
a(f'tl.fromTo("#grid", {{ scale: 1 }}, {{ scale: 1.04, duration: 3, ease: "sine.inOut", immediateRender: false }}, {ev["end"] + 1.2});')
a(f'tl.fromTo("#blk", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.0 }}, {DUR - 1.05});')
a('    window.__timelines["w"] = tl;')
open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}
  </style>
  <div id="root" data-composition-id="w" data-width="1080" data-height="1920">
    {body}
  </div>
  <script>
{chr(10).join("    " + x for x in js)}
  </script>
</template>
""")

# ------------------------------------------------ captions
caps, grp = [], []
for k, st in vo_at.items():
    cur = []
    for w, t in VO[k]["words"]:
        cur.append((w, st + t))
        if len(cur) >= 3 or w[-1] in ".,?:!":
            grp.append([cur, None]); cur = []
    if cur:
        grp.append([cur, None])
    grp[-1][1] = st + VO[k]["dur"]
for i, (ws, end) in enumerate(grp):
    s = round(ws[0][1] - 0.05, 2)
    e = end if end is not None else grp[i + 1][0][0][1] - 0.05
    caps.append(f'<div id="cap{i}" class="abs cap clip" data-start="{s}" data-duration="{round(e - s, 2)}"><span>{" ".join(w for w, _ in ws)}</span></div>')
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

# ------------------------------------------------ sound
sfx = [(0.0, "boom_open", 0.5), (ev["h2"] + 1.1, "pop", 0.5), (ev["in1"] - 0.3, "up2", 0.5)]
for i in range(1, 8):
    sfx += [(ev[f"in{i}"], "swipe1" if i % 2 else "swipe2", 0.6), (ev[f"in{i}"] + 0.2, "ui_tick2", 0.4),
            (ev[f"stamp{i}"] - 0.03, "stamp", 1.0), (ev[f"stamp{i}"], "impact", 0.35),
            (ev[f"flip{i}"], "flip", 0.8), (ev[f"flip{i}"] + 0.45, "pop", 0.5), (ev[f"out{i}"], "cardout", 0.6)]
sfx += [(ev["end"] + 0.2 + 0.09 * j, "ui_tick2", 0.35) for j in range(7)] + [(ev["end"] + 0.45 + 0.09 * j, "stamp", 0.45) for j in range(0, 7, 2)]
dur = {f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/sfx/{f}.mp3"], capture_output=True, text=True).stdout) for f in {x[1] for x in sfx}}
aud = [f'      <audio id="vo-{k}" class="clip" src="assets/vo/{k}.mp3" data-start="{round(s, 2)}" data-duration="{round(VO[k]["dur"] - 0.01, 2)}" data-track-index="2" data-volume="1.8"></audio>' for k, s in vo_at.items()]
aud += [f'      <audio id="sx{n}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(t, 2)}" data-duration="{round(min(dur[f], DUR - t) - 0.01, 2)}" data-track-index="{10 + n}" data-volume="{v}"></audio>' for n, (t, f, v) in enumerate(sfx)]
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
print("duration", DUR, "| captions", len(caps), "| sfx", len(sfx))
