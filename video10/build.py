#!/usr/bin/env python3
""""Your Salary Is a Ceiling" — ~40 s vertical Short, DLF style, English, Sarah (passionate), no music. Run: python3 build.py"""
import json, re, subprocess

VO = json.load(open("vo.json"))
ORDER = [f"c{i}" for i in range(1, 11)]
GAP = {"c1": 0.25, "c3": 0.3, "c4": 0.15, "c6": 0.15, "c7": 0.45, "c8": 0.3, "c9": 0.3}
T, at = 0.12, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.12)
DUR = round(T + 1.0, 2)

def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)

E = dict(ceil=w("c1", "ceiling"), boss=w("c2", "boss"), three=w("c2", "three"), forty=w("c3", "forty"), desk=w("c3", "desk"), num=w("c3", "number"),
         watch=w("c4", "watch"), side=w("c4", "side"), hour=w("c5", "hour"), fifty=w("c5", "fifty"), six=w("c6", "six"), five=w("c6", "five"),
         twelve=w("c7", "twelve"), two=w("c7", "two"), more=w("c7", "more"), comb=w("c7", "combined"), they=w("c8", "they"), skills=w("c8", "skills"),
         never=w("c9", "never"), limit=w("c9", "limit"), build=w("c10", "build"), tonight=w("c10", "tonight"))

FIG = '<svg viewBox="0 0 80 130"><circle cx="40" cy="24" r="20" fill="{c}"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="{c}"/></svg>'
def C(id, cls, style, inner=""):
    return f'<div id="{id}" class="abs {cls} clip" data-start="0" data-duration="{DUR}" style="{style}">{inner}</div>'

TITLES = {"t1": "Your salary is a <i>ceiling</i>", "t2": "+3 % if you’re <i>lucky</i>", "t3": "Same <i>number</i>.", "t4": "One side <i>project</i>",
          "t5": "1 hour a <i>day</i>", "t6": "Beats 5 <i>raises</i>", "t7": "They set your <i>salary</i>", "t8": "You set your <i>skills</i>",
          "t9": "Never the <i>limit</i>.", "t10": "Build something. <i>Tonight.</i>"}
shards = "".join(f'<div class="sh" id="sh{i}" style="left:{i * 100}px;clip-path:polygon({(i * 37) % 50}% 0,100% {(i * 23) % 60}%,{(i * 61) % 100}% 100%,0 {(i * 41) % 80}%)"></div>' for i in range(8))
body = [C(k, "ctr title", "top:230px", v) for k, v in TITLES.items()] + [
    C("ceil", "", "left:140px;top:700px;width:800px;height:26px", '<div class="gl"></div>' + shards + '<div class="sal" id="sal">€3,000 / month</div>'),
    C("ground", "", "left:0;top:1100px;width:1080px;height:0;border-top:2px dashed rgba(255,255,255,0.32)"),
    C("desk", "", "left:420px;top:1010px;width:240px;height:90px", '<div style="position:absolute;left:0;top:0;width:240px;height:16px;background:#cfcfcf;border-radius:4px"></div><div style="position:absolute;left:20px;top:16px;width:12px;height:74px;background:#cfcfcf"></div><div style="position:absolute;right:20px;top:16px;width:12px;height:74px;background:#cfcfcf"></div>'),
    C("fig", "glow", "left:480px;top:905px;width:120px;height:195px", FIG.format(c="#fff")),
    C("raise", "", "left:760px;top:640px", '<span class="ch">+3 %</span>'),
    C("pills", "", "left:110px;top:780px;width:300px", '<div class="ch rel" id="pl0">40 h / week</div><div class="ch rel" id="pl1">Same desk</div><div class="ch rel" id="pl2">Same number</div>'),
    C("tower", "", "left:760px;top:700px;width:120px;height:400px", '<div class="tw" id="tw"></div>'),
    C("tlab", "", "left:690px;top:980px;width:260px;text-align:center", '<div class="small">Side project</div><div class="sv" id="sv">€0/mo</div>'),
    C("cmp", "", "left:110px;top:460px;width:860px", '<div class="row"><span>Last 5 raises</span><b>+€478/mo</b></div><div class="row hot"><span>Side project</span><b>+€2,000/mo</b></div>'),
    C("spot", "", "left:620px;top:0;width:400px;height:1100px;background:linear-gradient(180deg,rgba(255,255,255,0.2),rgba(255,255,255,0.03));clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)"),
    C("fl", "", "left:0;top:0;width:1080px;height:1920px;background:#fff"),
]
HIDE = [f"#t{i}" for i in range(2, 11)] + ["#desk", "#raise", "#pills", "#tower", "#tlab", "#cmp", "#spot", "#fl"]
CSS = """
    #root { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 60%, #161616 0%, #000 70%); font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }
    #root .abs { position: absolute; }
    #root .ctr { left: 0; width: 1080px; text-align: center; }
    #root .glow { filter: drop-shadow(0 0 16px rgba(255,255,255,0.55)); }
    #root svg { width: 100%; height: 100%; display: block; }
    #root .title { font-weight: 900; font-size: 98px; letter-spacing: -0.02em; text-transform: uppercase; line-height: 1.02; padding: 0 60px; filter: drop-shadow(0 0 18px rgba(255,255,255,0.45)); }
    #root .title i { font-family: "Playfair Display", serif; font-style: italic; font-weight: 400; text-transform: none; letter-spacing: 0; }
    #root .gl { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(200,230,255,0.55), rgba(200,230,255,0.15)); border: 2px solid rgba(220,240,255,0.9); border-radius: 6px; box-shadow: 0 0 30px rgba(200,230,255,0.45); }
    #root .sh { position: absolute; top: 0; width: 100px; height: 26px; background: rgba(210,235,255,0.75); opacity: 0; }
    #root .sal { position: absolute; left: 50%; top: -64px; transform: translateX(-50%); font-weight: 800; font-size: 34px; letter-spacing: 0.1em; text-transform: uppercase; background: #111; border: 2px solid #fff; border-radius: 999px; padding: 8px 24px; white-space: nowrap; }
    #root .ch { font-weight: 800; font-size: 32px; letter-spacing: 0.12em; text-transform: uppercase; color: #fff; background: #111; border: 2px solid #fff; border-radius: 999px; padding: 8px 22px; white-space: nowrap; display: inline-block; }
    #root .ch.rel { display: block; width: fit-content; margin-bottom: 18px; opacity: 0; font-size: 28px; }
    #root .tw { position: absolute; left: 0; bottom: 0; width: 120px; height: 400px; background: #fff; border-radius: 10px 10px 0 0; transform-origin: 50% 100%; transform: scaleY(0); box-shadow: 0 0 30px rgba(255,255,255,0.5); }
    #root .small { font-weight: 700; font-size: 28px; letter-spacing: 0.18em; text-transform: uppercase; color: #9a9a9a; }
    #root .sv { font-weight: 900; font-size: 60px; margin-top: 4px; }
    #root .row { display: flex; justify-content: space-between; align-items: center; padding: 18px 28px; border: 2px solid #555; border-radius: 18px; margin-bottom: 18px; font-weight: 800; font-size: 36px; text-transform: uppercase; letter-spacing: 0.06em; color: #9a9a9a; }
    #root .row b { font-size: 54px; color: #cfcfcf; letter-spacing: -0.02em; }
    #root .row.hot { border-color: #fff; color: #fff; box-shadow: 0 0 30px rgba(255,255,255,0.3); }
    #root .row.hot b { color: #fff; }
""" + "    " + ", ".join(f"#root {h}" for h in HIDE) + " { opacity: 0; }\n"

J = []; a = J.append
def swap(old, new, t, big=False):
    a(f'tl.to("#{old}", {{ opacity: 0, y: -40, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {t - 0.18:.2f});')
    a(f'tl.fromTo("#{new}", {{ opacity: 0, y: 40, scale: {1.35 if big else 1}, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: {0.2 if big else 0.32}, ease: "{"power4.in" if big else "power3.out"}" }}, {t:.2f});')
def side(t, a0, b0, h, dur=0.6):
    a(f'(() => {{ const o = {{ v: {a0} }}; tl.fromTo(o, {{ v: {a0} }}, {{ v: {b0}, duration: {dur}, ease: "power2.out", immediateRender: false, onUpdate: () => {{ $("#sv").textContent = "€" + Math.round(o.v).toLocaleString("en-US") + "/mo"; }} }}, {t:.2f}); }})();')
    a(f'tl.to("#tw", {{ scaleY: {h}, duration: {dur}, ease: "power2.out" }}, {t:.2f});')
    a(f'tl.to("#tlab", {{ y: {-400 * h - 20}, duration: {dur}, ease: "power2.out" }}, {t:.2f});')
# hook: the ceiling presses down
a(f'tl.fromTo("#ceil", {{ y: -60 }}, {{ y: 0, duration: 0.5, ease: "bounce.out" }}, {E["ceil"] - 0.2:.2f});')
a(f'tl.fromTo("#fig", {{ scaleY: 1 }}, {{ scaleY: 0.93, transformOrigin: "50% 100%", duration: 0.3 }}, {E["ceil"] + 0.2:.2f});')
swap("t1", "t2", E["three"])
a(f'tl.fromTo("#raise", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }}, {E["three"]:.2f});')
a(f'tl.to("#ceil", {{ y: -10, duration: 0.6, ease: "power2.out" }}, {E["three"] + 0.1:.2f});')
a(f'tl.to("#raise", {{ opacity: 0, duration: 0.3 }}, {E["forty"] - 0.2:.2f});')
swap("t2", "t3", E["forty"])
a(f'tl.fromTo("#desk", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {E["desk"] - 0.1:.2f});')
a(f'tl.fromTo("#pills", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {E["forty"]:.2f});')
for i, t in enumerate((E["forty"], E["desk"], E["num"])):
    a(f'tl.fromTo("#pl{i}", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.25 }}, {t:.2f});')
# side project grows
swap("t3", "t4", E["side"])
a(f'tl.to(["#pills", "#desk"], {{ opacity: 0, duration: 0.3 }}, {E["watch"]:.2f});')
a(f'tl.to("#fig", {{ x: -120, scaleY: 1, duration: 0.5, ease: "power2.inOut" }}, {E["watch"]:.2f});')
a(f'tl.fromTo(["#tower", "#tlab"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {E["side"]:.2f});')
swap("t4", "t5", E["hour"])
side(E["fifty"], 0, 50, 0.06)
side(E["five"], 50, 500, 0.35)
swap("t5", "t6", E["more"])
side(E["two"], 500, 2000, 1.0, 0.8)
a(f'tl.fromTo("#ceil", {{ x: 0 }}, {{ x: 8, duration: 0.05, yoyo: true, repeat: 5, ease: "none", immediateRender: false }}, {E["two"] + 0.7:.2f});')
a(f'tl.fromTo("#cmp", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {E["more"] + 0.3:.2f});')
a(f'tl.to("#tlab", {{ opacity: 0, duration: 0.25 }}, {E["more"] + 0.15:.2f});')
a(f'tl.to("#sal", {{ opacity: 0, duration: 0.25 }}, {E["two"]:.2f});')
# the ceiling shatters
a(f'tl.to(".gl", {{ opacity: 0, duration: 0.05 }}, {E["comb"]:.2f}); ')
for i in range(8):
    a(f'tl.fromTo("#sh{i}", {{ opacity: 1, x: 0, y: 0, rotation: 0 }}, {{ opacity: 0, x: {(i - 3.5) * 70}, y: {-200 - (i * 53) % 260}, rotation: {(i * 71) % 360 - 180}, duration: 1.1, ease: "power2.out", immediateRender: false }}, {E["comb"]:.2f});')
a(f'tl.fromTo("#fl", {{ opacity: 0 }}, {{ opacity: 0.35, duration: 0.04 }}, {E["comb"]:.2f}); tl.to("#fl", {{ opacity: 0, duration: 0.4 }}, {E["comb"] + 0.05:.2f});')
# they / you
a(f'tl.to("#cmp", {{ opacity: 0, duration: 0.3 }}, {E["they"] - 0.3:.2f});')
swap("t6", "t7", E["they"] - 0.2)
swap("t7", "t8", E["skills"] - 0.2)
a(f'tl.to("#fig", {{ keyframes: [{{ x: 0, y: -420, duration: 0.45, ease: "power2.out" }}, {{ x: 280, y: -400, duration: 0.3, ease: "power2.in" }}] }}, {E["skills"]:.2f});')
swap("t8", "t9", E["never"])
a(f'tl.to("#fig", {{ filter: "drop-shadow(0 0 40px rgba(255,255,255,0.95))", duration: 0.5 }}, {E["limit"]:.2f});')
swap("t9", "t10", E["tonight"] - 0.5, big=True)
a(f'tl.fromTo("#spot", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08 }}, {E["tonight"]:.2f});')
a(f'tl.fromTo("#fl", {{ opacity: 0 }}, {{ opacity: 0.35, duration: 0.04, immediateRender: false }}, {E["tonight"]:.2f}); tl.to("#fl", {{ opacity: 0, duration: 0.4 }}, {E["tonight"] + 0.05:.2f});')

open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="1080" data-height="1920" data-layout-allow-overlap>
    {chr(10).join("    " + b for b in body)}
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
    #root .cap {{ left: 90px; width: 900px; top: 1190px; text-align: center; font-weight: 800; font-size: 56px; line-height: 1.15; color: #fff; }}
    #root .cap span {{ display: inline-block; background: rgba(0,0,0,0.86); padding: 6px 22px 10px; border-radius: 16px; }}
  </style>
  <div id="root" data-composition-id="cap" data-width="1080" data-height="1920">
{chr(10).join("    " + c for c in caps)}
  </div>
  <script>window.__timelines["cap"] = gsap.timeline({{ paused: true }});</script>
</template>
""")

SFX = [(0.0, "boom_open", 0.45), (E["ceil"] - 0.05, "impact", 0.6), (E["three"], "pop", 0.45), (E["forty"], "swipe1", 0.4), (E["desk"], "pop", 0.35), (E["num"], "pop", 0.35),
       (E["side"], "zoom_whoosh", 0.45), (E["fifty"], "coin_jar", 0.7), (E["five"], "count_fast", 0.45), (E["two"], "count_fast", 0.5), (E["two"] + 0.7, "heartbeat", 0.5),
       (E["more"] + 0.3, "swipe2", 0.4), (E["comb"] - 0.02, "glass", 1.0), (E["comb"], "impact", 0.7), (E["skills"], "zoom_whoosh", 0.45), (E["limit"], "shimmer", 0.5),
       (E["tonight"] - 0.03, "spot", 0.9), (E["tonight"], "impact", 0.8)]
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
