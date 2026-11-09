#!/usr/bin/env python3
""""Your First €1,000" — ~42 s vertical Short, DLF style, English, Sarah (passionate), no music. Run: python3 build.py"""
import json, re, subprocess

VO = json.load(open("vo.json"))
ORDER = [f"p{i}" for i in range(1, 13)]
GAP = {"p1": 0.15, "p2": 0.25, "p5": 0.45, "p6": 0.15, "p7": 0.3, "p9": 0.3, "p10": 0.35, "p11": 0.3}
T, at = 0.12, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.12)
DUR = round(T + 1.0, 2)

def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)

E = dict(hardest=w("p1", "hardest"), wrong=at["p2"], m1=w("p3", "one"), nobody=w("p3", "nobodys"), m3=w("p4", "three"), two=w("p4", "two"),
         quit=w("p4", "quit"), m8=w("p5", "eight"), k1=w("p5", "one"), fin=w("p5", "finally"), tells=w("p6", "tells"), didnt=w("p6", "didnt"),
         sell=w("p7", "sell"), save=w("p7", "save"), show=w("p7", "show"), nextk=w("p8", "next"), four=w("p8", "four"),
         two2=w("p9", "two"), one2=w("p9", "one"), same=at["p10"], ten=w("p11", "ten"), first=w("p11", "first"), today=w("p12", "today"))

FIG = '<svg viewBox="0 0 80 130"><circle cx="40" cy="24" r="20" fill="{c}"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="{c}"/></svg>'
def C(id, cls, style, inner=""):
    return f'<div id="{id}" class="abs {cls} clip" data-start="0" data-duration="{DUR}" style="{style}">{inner}</div>'

TITLES = {"t1": "The first <i>€1,000</i>", "t2": "Sounds <i>wrong</i>.", "t3": "Month <i>one</i>", "t4": "Month <i>three</i>", "t5": "Month <i>eight</i>",
          "t6": "Nobody tells you <i>this</i>", "t7": "New <i>skills</i>", "t8": "The next <i>€1,000</i>", "t9": "Same <i>person</i>.",
          "t10": "€10,000 starts at <i>€1</i>", "t11": "Go make it. <i>Today.</i>"}
BARS = [(8, "€1k #1"), (4, "€1k #2"), (2, "€1k #3"), (1, "€1k #4")]
bars = "".join(f'<div class="br" id="br{i}"><span class="bl">{lab}</span><div class="bt"><div class="bf" id="bf{i}" style="width:{m * 82}px"></div></div><span class="bm">{m} mo</span></div>' for i, (m, lab) in enumerate(BARS))
body = [C(k, "ctr title", "top:230px", v) for k, v in TITLES.items()] + [
    C("cnt", "ctr money", "top:470px", "€0"),
    C("goal", "", "left:240px;top:640px;width:600px;height:16px", '<div class="gt"><div class="gf" id="gf"></div></div><div class="gl">Goal · €1,000</div>'),
    C("spot", "", "left:340px;top:0;width:400px;height:1100px;background:linear-gradient(180deg,rgba(255,255,255,0.2),rgba(255,255,255,0.03));clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)"),
    C("ground", "", "left:0;top:1100px;width:1080px;height:0;border-top:2px dashed rgba(255,255,255,0.32)"),
    C("ghost", "", "left:300px;top:905px;width:120px;height:195px", FIG.format(c="#4a4a4a")),
    C("fig", "glow", "left:480px;top:905px;width:120px;height:195px", FIG.format(c="#fff")),
    C("crowd", "", "left:40px;top:950px;width:330px;height:150px", "".join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s * 1.62:.0f}px">{FIG.format(c="#8a8a8a")}</div>' for x, y, s in ((20, 30, 74), (130, 40, 68))) + '<div class="ch" id="b0" style="left:0;top:-48px">meh</div><div class="ch" id="b1" style="left:120px;top:-90px">lol</div>'),
    C("star", "glow", "left:510px;top:820px;width:60px;height:60px", '<svg viewBox="0 0 80 80"><path d="M40 4 L49 30 L76 30 L54 47 L62 74 L40 58 L18 74 L26 47 L4 30 L31 30 Z" fill="#fff"/></svg>'),
    C("sk", "", "left:0;top:0;width:1080px;height:1920px", '<div class="ch big" id="sk0" style="left:220px;top:820px">Sell</div><div class="ch big" id="sk1" style="left:690px;top:780px">Save</div><div class="ch big" id="sk2" style="left:640px;top:960px">Show up</div>'),
    C("bars", "", "left:120px;top:470px;width:840px", bars),
    C("fl", "", "left:0;top:0;width:1080px;height:1920px;background:#fff"),
]
HIDE = [f"#t{i}" for i in range(2, 12)] + ["#spot", "#ghost", "#crowd", "#star", "#sk", "#bars", "#fl"]
CSS = """
    #root { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 60%, #161616 0%, #000 70%); font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }
    #root .abs { position: absolute; }
    #root .ctr { left: 0; width: 1080px; text-align: center; }
    #root .glow { filter: drop-shadow(0 0 16px rgba(255,255,255,0.55)); }
    #root svg { width: 100%; height: 100%; display: block; }
    #root .title { font-weight: 900; font-size: 100px; letter-spacing: -0.02em; text-transform: uppercase; line-height: 1.02; padding: 0 60px; filter: drop-shadow(0 0 18px rgba(255,255,255,0.45)); }
    #root .title i { font-family: "Playfair Display", serif; font-style: italic; font-weight: 400; text-transform: none; letter-spacing: 0; }
    #root .money { font-weight: 900; font-size: 150px; letter-spacing: -0.03em; line-height: 1; filter: drop-shadow(0 0 20px rgba(255,255,255,0.5)); }
    #root .gt { width: 600px; height: 16px; border-radius: 8px; background: #262626; overflow: hidden; }
    #root .gf { width: 100%; height: 100%; background: #fff; transform-origin: 0% 50%; transform: scaleX(0); box-shadow: 0 0 14px #fff; }
    #root .gl { margin-top: 14px; text-align: center; font-weight: 700; font-size: 28px; letter-spacing: 0.18em; text-transform: uppercase; color: #9a9a9a; }
    #root .ch { position: absolute; font-weight: 800; font-size: 28px; letter-spacing: 0.14em; text-transform: uppercase; color: #fff; background: #111; border: 2px solid #fff; border-radius: 999px; padding: 8px 20px; white-space: nowrap; }
    #root .ch.big { font-size: 40px; padding: 12px 30px; box-shadow: 0 0 24px rgba(255,255,255,0.3); }
    #root .br { display: grid; grid-template-columns: 150px 1fr 110px; align-items: center; gap: 18px; margin-bottom: 34px; opacity: 0; }
    #root .bl, #root .bm { font-weight: 800; font-size: 32px; letter-spacing: 0.06em; text-transform: uppercase; }
    #root .bm { text-align: right; }
    #root .bt { height: 46px; }
    #root .bf { height: 46px; border-radius: 10px; background: #fff; transform-origin: 0% 50%; transform: scaleX(0); box-shadow: 0 0 18px rgba(255,255,255,0.4); }
""" + "    " + ", ".join(f"#root {h}" for h in HIDE) + " { opacity: 0; }\n"

J = []; a = J.append
def swap(old, new, t, big=False):
    a(f'tl.to("#{old}", {{ opacity: 0, y: -40, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {t - 0.18:.2f});')
    a(f'tl.fromTo("#{new}", {{ opacity: 0, y: 40, scale: {1.35 if big else 1}, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: {0.2 if big else 0.32}, ease: "{"power4.in" if big else "power3.out"}" }}, {t:.2f});')
def money(t, a0, b0, dur, ease="power2.out"):
    a(f'(() => {{ const o = {{ v: {a0} }}; tl.fromTo(o, {{ v: {a0} }}, {{ v: {b0}, duration: {dur}, ease: "{ease}", immediateRender: false, onUpdate: () => {{ $("#cnt").textContent = "€" + Math.round(o.v).toLocaleString("en-US"); }} }}, {t:.2f}); }})();')
# hook
a(f'tl.fromTo("#cnt", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 }}, {E["hardest"]:.2f});')
swap("t1", "t2", E["wrong"])
# month one: nobody's impressed
swap("t2", "t3", E["m1"])
a(f'tl.fromTo("#crowd", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {E["nobody"] - 0.1:.2f});')
for i in range(2):
    a(f'tl.fromTo("#b{i}", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }}, {E["nobody"] + 0.2 + i * 0.25:.2f});')
# month three: €200, wants to quit
swap("t3", "t4", E["m3"])
money(E["two"], 0, 200, 0.6)
a(f'tl.to("#gf", {{ scaleX: 0.2, duration: 0.6, ease: "power2.out" }}, {E["two"]:.2f});')
a(f'tl.to("#fig", {{ scaleY: 0.9, x: 40, rotation: 8, transformOrigin: "50% 100%", opacity: 0.6, duration: 0.5 }}, {E["quit"]:.2f});')
# month eight: €1,000, finally
swap("t4", "t5", E["m8"])
a(f'tl.to("#crowd", {{ opacity: 0, duration: 0.3 }}, {E["m8"]:.2f});')
money(E["k1"] - 0.6, 200, 1000, 1.0, "power3.in")
a(f'tl.to("#gf", {{ scaleX: 1, duration: 1.0, ease: "power3.in" }}, {E["k1"] - 0.6:.2f});')
a(f'tl.to("#fig", {{ scaleY: 1, x: 0, rotation: 0, opacity: 1, duration: 0.4, ease: "back.out(2)" }}, {E["k1"] + 0.3:.2f});')
a(f'tl.fromTo(["#spot", "#star"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {E["k1"] + 0.4:.2f});')
a(f'tl.fromTo("#fl", {{ opacity: 0 }}, {{ opacity: 0.3, duration: 0.04 }}, {E["k1"] + 0.4:.2f}); tl.to("#fl", {{ opacity: 0, duration: 0.4 }}, {E["k1"] + 0.45:.2f});')
a(f'tl.fromTo("#cnt", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.18, yoyo: true, repeat: 1, immediateRender: false }}, {E["k1"] + 0.4:.2f});')
# the twist: skills
swap("t5", "t6", E["tells"])
a(f'tl.to(["#cnt", "#goal"], {{ opacity: 0.25, duration: 0.4 }}, {E["didnt"]:.2f});')
swap("t6", "t7", E["sell"] - 0.3)
a(f'tl.fromTo("#sk", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {E["sell"] - 0.1:.2f});')
for i, k in enumerate(("sell", "save", "show")):
    a(f'tl.fromTo("#sk{i}", {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }}, {E[k] - 0.05:.2f});')
a(f'tl.to("#fig", {{ filter: "drop-shadow(0 0 40px rgba(255,255,255,0.95))", duration: 0.5 }}, {E["show"]:.2f});')
# the next thousands get faster
a(f'tl.to(["#sk", "#cnt", "#goal", "#star", "#spot"], {{ opacity: 0, duration: 0.3 }}, {at["p8"] - 0.1:.2f});')
swap("t7", "t8", E["nextk"])
a(f'tl.fromTo("#bars", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {at["p8"]:.2f});')
for i, t in enumerate((at["p8"] + 0.1, E["four"], E["two2"], E["one2"])):
    a(f'tl.fromTo("#br{i}", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.25 }}, {t - 0.05:.2f});')
    a(f'tl.to("#bf{i}", {{ scaleX: 1, duration: {0.5 if i == 0 else 0.3}, ease: "power2.out" }}, {t:.2f});')
# same person, different skills
swap("t8", "t9", E["same"])
a(f'tl.to("#bars", {{ opacity: 0, duration: 0.3 }}, {E["same"]:.2f});')
a(f'tl.fromTo("#ghost", {{ opacity: 0, x: 0 }}, {{ opacity: 1, x: -40, duration: 0.5 }}, {E["same"] + 0.1:.2f});')
a(f'tl.to("#fig", {{ x: 60, duration: 0.5 }}, {E["same"] + 0.1:.2f});')
a(f'tl.to("#sk", {{ opacity: 1, duration: 0.3 }}, {E["same"] + 1.0:.2f});')
# €10,000 starts at €1
swap("t9", "t10", E["ten"])
a(f'tl.to(["#ghost", "#sk"], {{ opacity: 0, duration: 0.3 }}, {E["ten"]:.2f});')
a(f'tl.to("#cnt", {{ opacity: 1, duration: 0.3 }}, {E["ten"]:.2f});')
money(E["ten"], 1000, 10000, 0.8)
money(E["first"] - 0.3, 10000, 1, 0.7, "power2.in")
a(f'tl.fromTo("#cnt", {{ scale: 1 }}, {{ scale: 1.2, duration: 0.18, yoyo: true, repeat: 1, immediateRender: false }}, {E["first"] + 0.4:.2f});')
# go
swap("t10", "t11", E["today"] - 0.6, big=True)
a(f'tl.to("#cnt", {{ opacity: 0, duration: 0.2 }}, {E["today"] - 0.6:.2f});')
a(f'tl.fromTo("#spot", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, immediateRender: false }}, {E["today"]:.2f});')
a(f'tl.fromTo("#fl", {{ opacity: 0 }}, {{ opacity: 0.35, duration: 0.04, immediateRender: false }}, {E["today"]:.2f}); tl.to("#fl", {{ opacity: 0, duration: 0.4 }}, {E["today"] + 0.05:.2f});')
a(f'tl.to("#fig", {{ x: 0, scale: 1.12, transformOrigin: "50% 100%", duration: 0.3, ease: "back.out(3)" }}, {E["today"]:.2f});')

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

SFX = [(0.0, "boom_open", 0.45), (E["hardest"], "impact", 0.4), (E["wrong"], "swipe1", 0.45), (E["nobody"] + 0.2, "murmur", 0.6),
       (E["two"], "count_fast", 0.4), (E["quit"], "heartbeat", 0.6), (E["k1"] - 0.6, "count_fast", 0.5), (E["k1"] + 0.38, "kaching", 0.9),
       (E["k1"] + 0.4, "spot", 0.6), (E["tells"], "swipe2", 0.45), (E["sell"] - 0.05, "pop", 0.5), (E["save"] - 0.05, "pop", 0.5), (E["show"] - 0.05, "pop", 0.5),
       (E["show"], "shimmer", 0.5), (at["p8"] + 0.1, "zoom_whoosh", 0.45), (E["four"], "pop", 0.5), (E["two2"], "pop", 0.5), (E["one2"], "pop", 0.55),
       (E["same"], "swipe1", 0.4), (E["ten"], "count_fast", 0.5), (E["ten"] + 0.75, "kaching", 0.6), (E["first"] - 0.3, "zoom_whoosh", 0.4),
       (E["first"] + 0.4, "impact", 0.5), (E["today"] - 0.03, "spot", 0.9), (E["today"], "impact", 0.8)]
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
