#!/usr/bin/env python3
""""Don't Quit the Pirate Token" — ~38 s, fan video vertical Short, DLF style, English, Sarah (passionate), no music. Run: python3 build.py"""
import json, re, subprocess

VO = json.load(open("vo.json"))
ORDER = [f"k{i}" for i in range(1, 11)]
GAP = {"k1": 0.4, "k2": 0.2, "k4": 0.25, "k5": 0.3, "k7": 0.5, "k8": 0.3, "k9": 0.35}
T, at = 0.12, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.12)
DUR = round(T + 1.0, 2)

def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)

E = dict(token=w("k1", "token"), tiny=w("k2", "tiny"), most=at["k3"], quit=w("k3", "quit"), rig=w("k4", "rigged"), imp=w("k4", "impossible"),
         waste=w("k4", "waste"), never=w("k5", "never"), zero=w("k5", "zero"), round_=w("k6", "round"), ticket=w("k6", "ticket"), chance=w("k6", "chance"),
         ones=at["k7"], stop=w("k7", "stop"), kids=w("k8", "kids"), did=w("k8", "did"), say=w("k9", "say"), gave=w("k9", "gave"), no=at["k10"],
         drop=w("k10", "drop"), waiting=w("k10", "waiting"))

FIG = '<svg viewBox="0 0 80 130"><circle cx="40" cy="24" r="20" fill="{c}"/><path d="M6 130 V94 a34 34 0 0 1 68 0 V130 Z" fill="{c}"/></svg>'
def C(id, cls, style, inner=""):
    return f'<div id="{id}" class="abs {cls} clip" data-start="0" data-duration="{DUR}" style="{style}">{inner}</div>'

TITLES = {"t1": "The Pirate <i>Token</i>", "t2": "The odds? <i>Tiny.</i>", "t3": "Most people <i>quit</i>.", "t4": "Never <i>zero</i>.",
          "t5": "Every try is a <i>ticket</i>", "t6": "They didn’t <i>stop</i>.", "t7": "Your kids will <i>ask</i>.", "t8": "“I gave <i>up</i>”?",
          "t9": "Drop in <i>again</i>."}
crowd = "".join(f'<div class="cw" id="cw{i}" style="left:{x}px">{FIG.format(c="#8a8a8a")}</div>' for i, x in enumerate((60, 170, 760, 870, 960)))
tickets = "".join(f'<div class="tk" id="tk{i}" style="left:{(i % 6) * 120}px;top:{(i // 6) * 70}px">#{(i + 1) * 40}</div>' for i in range(12))
body = [C(k, "ctr title", "top:200px", v) for k, v in TITLES.items()] + [
    C("rays", "", "left:-260px;top:120px;width:1600px;height:1600px;background:repeating-conic-gradient(from 0deg, rgba(255,214,110,0.18) 0deg 8deg, rgba(0,0,0,0) 8deg 24deg);border-radius:50%;-webkit-mask:radial-gradient(circle, #000 20%, transparent 62%);mask:radial-gradient(circle, #000 20%, transparent 62%)"),
    C("tok", "", "left:190px;top:470px;width:700px;height:700px", '<img src="assets/token.png" alt="" style="width:100%;height:100%;display:block"><div class="sweep" id="sweep"></div>'),
    C("note", "ctr", "top:1310px;font-size:26px;color:#7a7a7a;letter-spacing:0.08em", "Fan video · not affiliated with Epic Games"),
    C("bar", "", "left:140px;top:600px;width:800px", '<div class="bt"><div class="dot" id="dot"></div></div><div class="small" style="margin-top:16px;text-align:center">Your chance per round</div>'),
    C("ground", "", "left:0;top:1100px;width:1080px;height:0;border-top:2px dashed rgba(255,255,255,0.32)"),
    C("crowd", "", "left:0;top:960px;width:1080px;height:140px", crowd),
    C("fig", "glow", "left:480px;top:905px;width:120px;height:195px", FIG.format(c="#fff")),
    C("chips", "", "left:0;top:0;width:1080px;height:1920px", '<div class="ch" id="q0" style="left:120px;top:560px">It’s rigged</div><div class="ch" id="q1" style="left:560px;top:660px">Impossible</div><div class="ch" id="q2" style="left:220px;top:780px">Waste of time</div>'),
    C("cnt", "ctr", "top:440px", '<div class="small">Attempts</div><div class="money" id="cn">#1</div>'),
    C("tks", "", "left:180px;top:700px;width:720px;height:150px", tickets),
    C("spot", "", "left:340px;top:0;width:400px;height:1100px;background:linear-gradient(180deg,rgba(255,255,255,0.2),rgba(255,255,255,0.03));clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)"),
    C("kid", "", "left:660px;top:990px;width:68px;height:110px", FIG.format(c="#cfcfcf")),
    C("kb", "", "left:470px;top:780px;width:520px", '<div class="bub">Did you get the Pirate Token?</div>'),
    C("ib", "", "left:180px;top:700px;width:420px", '<div class="bub">I gave up…</div><div class="stp" id="stp">No.</div>'),
    C("fl", "", "left:0;top:0;width:1080px;height:1920px;background:#fff"),
]
HIDE = [f"#t{i}" for i in range(2, 10)] + ["#bar", "#crowd", "#chips", "#cnt", "#tks", "#spot", "#kid", "#kb", "#ib", "#fl", "#ground", "#fig"]
CSS = """
    #root { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 50%, #1e1506 0%, #000 70%); font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }
    #root .abs { position: absolute; }
    #root .ctr { left: 0; width: 1080px; text-align: center; }
    #root .glow { filter: drop-shadow(0 0 16px rgba(255,255,255,0.55)); }
    #root svg { width: 100%; height: 100%; display: block; }
    #root .title { font-weight: 900; font-size: 98px; letter-spacing: -0.02em; text-transform: uppercase; line-height: 1.02; padding: 0 60px; filter: drop-shadow(0 0 18px rgba(255,210,110,0.45)); }
    #root .title i { font-family: "Playfair Display", serif; font-style: italic; font-weight: 400; text-transform: none; letter-spacing: 0; color: #ffd66b; }
    #root #tok { overflow: hidden; border-radius: 24px; -webkit-mask: radial-gradient(circle, #000 55%, transparent 72%); mask: radial-gradient(circle, #000 55%, transparent 72%); }
    #root .sweep { position: absolute; top: -20%; left: -60%; width: 40%; height: 140%; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,240,0.55), rgba(255,255,255,0)); transform: rotate(18deg); mix-blend-mode: screen; }
    #root .small { font-weight: 700; font-size: 28px; letter-spacing: 0.18em; text-transform: uppercase; color: #9a9a9a; }
    #root .money { font-weight: 900; font-size: 140px; letter-spacing: -0.03em; line-height: 1; filter: drop-shadow(0 0 20px rgba(255,214,110,0.5)); }
    #root .bt { position: relative; height: 34px; border-radius: 17px; border: 2px solid #555; background: #0c0c0c; }
    #root .dot { position: absolute; left: 6px; top: 6px; width: 18px; height: 18px; border-radius: 50%; background: #ffd66b; box-shadow: 0 0 18px #ffd66b, 0 0 40px #ffb627; }
    #root .cw { position: absolute; top: 0; width: 86px; height: 140px; }
    #root .ch { position: absolute; font-weight: 800; font-size: 36px; letter-spacing: 0.1em; text-transform: uppercase; color: #fff; background: #111; border: 2px solid #fff; border-radius: 999px; padding: 10px 26px; white-space: nowrap; }
    #root .tk { position: absolute; width: 104px; height: 56px; border-radius: 10px; background: linear-gradient(135deg, #ffe58a, #c88a17); color: #2a1a02; font-weight: 900; font-size: 24px; display: flex; align-items: center; justify-content: center; opacity: 0; box-shadow: 0 0 14px rgba(255,200,80,0.4); }
    #root .bub { display: inline-block; font-weight: 800; font-size: 40px; line-height: 1.15; background: #fff; color: #000; border-radius: 26px; padding: 18px 28px; box-shadow: 0 0 30px rgba(255,255,255,0.3); }
    #root .stp { position: absolute; left: 60px; top: -10px; font-weight: 900; font-size: 120px; text-transform: uppercase; color: #fff; border: 10px solid #fff; border-radius: 18px; padding: 0 30px; background: rgba(0,0,0,0.75); transform: rotate(-12deg); opacity: 0; }
""" + "    " + ", ".join(f"#root {h}" for h in HIDE) + " { opacity: 0; }\n"

J = []; a = J.append
def swap(old, new, t, big=False):
    a(f'tl.to("#{old}", {{ opacity: 0, y: -40, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {t - 0.18:.2f});')
    a(f'tl.fromTo("#{new}", {{ opacity: 0, y: 40, scale: {1.35 if big else 1}, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: {0.2 if big else 0.32}, ease: "{"power4.in" if big else "power3.out"}" }}, {t:.2f});')
# hook: the token, rays spinning, shine sweeping
a(f'tl.fromTo("#rays", {{ rotation: 0 }}, {{ rotation: 40, duration: {DUR}, ease: "none" }}, 0);')
a(f'tl.fromTo("#tok", {{ scale: 0.9 }}, {{ scale: 1.04, duration: {E["tiny"]:.2f}, ease: "sine.inOut" }}, 0);')
for t in (0.4, E["token"] + 0.1):
    a(f'tl.fromTo("#sweep", {{ x: 0 }}, {{ x: 1300, duration: 0.9, ease: "power2.inOut", immediateRender: false }}, {t:.2f});')
a(f'tl.fromTo("#fl", {{ opacity: 0 }}, {{ opacity: 0.25, duration: 0.04 }}, {E["token"]:.2f}); tl.to("#fl", {{ opacity: 0, duration: 0.4 }}, {E["token"] + 0.05:.2f});')
# the odds: one tiny dot on a huge bar
swap("t1", "t2", E["tiny"] - 0.3)
a(f'tl.to(["#tok", "#rays"], {{ opacity: 0, scale: 0.5, duration: 0.4, ease: "power2.in" }}, {E["tiny"] - 0.3:.2f});')
a(f'tl.fromTo("#bar", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {E["tiny"]:.2f});')
a(f'tl.fromTo("#dot", {{ scale: 1 }}, {{ scale: 1.6, duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {E["tiny"] + 0.3:.2f});')
# most people quit
swap("t2", "t3", E["most"])
a(f'tl.to("#bar", {{ opacity: 0, duration: 0.3 }}, {E["most"]:.2f});')
a(f'tl.fromTo(["#ground", "#fig", "#crowd"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {E["most"]:.2f});')
for i in range(5):
    a(f'tl.to("#cw{i}", {{ x: {-300 if i < 2 else 300}, opacity: 0, duration: 0.7, ease: "power1.in" }}, {E["quit"] - 0.3 + i * 0.12:.2f});')
# excuses
for i, k in enumerate(("rig", "imp", "waste")):
    a(f'tl.fromTo("#q{i}", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }}, {E[k] - 0.05:.2f});')
a(f'tl.fromTo("#chips", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {E["rig"] - 0.1:.2f});')
a(f'tl.to(["#t3"], {{ opacity: 0.25, duration: 0.3 }}, {E["rig"]:.2f});')
# never zero
swap("t3", "t4", E["never"])
a(f'tl.to("#chips", {{ opacity: 0, scale: 0.8, duration: 0.3 }}, {E["never"]:.2f});')
a(f'tl.to("#bar", {{ opacity: 1, duration: 0.3 }}, {E["never"]:.2f});')
a(f'tl.fromTo("#dot", {{ scale: 1 }}, {{ scale: 2.2, duration: 0.25, yoyo: true, repeat: 1, ease: "back.out(3)", immediateRender: false }}, {E["zero"]:.2f});')
# every try is a ticket
swap("t4", "t5", E["round_"])
a(f'tl.to("#bar", {{ opacity: 0, duration: 0.3 }}, {E["round_"]:.2f});')
a(f'tl.fromTo(["#cnt", "#tks"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {E["round_"]:.2f});')
a(f'(() => {{ const o = {{ v: 1 }}; tl.fromTo(o, {{ v: 1 }}, {{ v: 480, duration: {E["chance"] - E["round_"] + 0.6:.2f}, ease: "power1.in", immediateRender: false, onUpdate: () => {{ $("#cn").textContent = "#" + Math.round(o.v); }} }}, {E["round_"]:.2f}); }})();')
span = E["chance"] - E["round_"] + 0.4
for i in range(12):
    a(f'tl.fromTo("#tk{i}", {{ opacity: 0, y: -40, rotation: -10 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.2, ease: "back.out(2)" }}, {E["round_"] + 0.2 + i * span / 12:.2f});')
for j in range(int(span / 0.35)):
    a(f'tl.to("#fig", {{ y: -14, duration: 0.1, yoyo: true, repeat: 1 }}, {E["round_"] + j * 0.35:.2f});')
# they didn't stop
swap("t5", "t6", E["stop"] - 0.5)
a(f'tl.to(["#cnt", "#tks"], {{ opacity: 0, duration: 0.3 }}, {E["ones"]:.2f});')
a(f'tl.fromTo("#spot", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {E["stop"]:.2f});')
a(f'tl.to("#fig", {{ filter: "drop-shadow(0 0 40px rgba(255,255,255,0.95))", duration: 0.4 }}, {E["stop"]:.2f});')
# your kids will ask
swap("t6", "t7", E["kids"])
a(f'tl.to("#spot", {{ opacity: 0, duration: 0.4 }}, {E["kids"]:.2f});')
a(f'tl.fromTo("#kid", {{ opacity: 0, x: 120 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "power2.out" }}, {E["kids"]:.2f});')
a(f'tl.fromTo("#kb", {{ opacity: 0, scale: 0.6, transformOrigin: "70% 100%" }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }}, {E["did"] - 0.1:.2f});')
# "I gave up?" -> NO.
swap("t7", "t8", E["gave"] - 0.4)
a(f'tl.to("#kb", {{ opacity: 0, duration: 0.25 }}, {E["say"]:.2f});')
a(f'tl.fromTo("#ib", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)" }}, {E["gave"] - 0.3:.2f});')
a(f'tl.to("#fig", {{ scaleY: 0.9, transformOrigin: "50% 100%", opacity: 0.6, filter: "drop-shadow(0 0 0px rgba(255,255,255,0))", duration: 0.4 }}, {E["gave"]:.2f});')
a(f'tl.fromTo("#stp", {{ opacity: 0, scale: 2.4 }}, {{ opacity: 1, scale: 1, duration: 0.14, ease: "power4.in" }}, {E["no"] - 0.1:.2f});')
# drop in again: the token returns
swap("t8", "t9", E["drop"])
a(f'tl.to(["#ib", "#kid", "#ground", "#fig"], {{ opacity: 0, duration: 0.3 }}, {E["drop"]:.2f});')
a(f'tl.to(["#tok", "#rays"], {{ opacity: 1, scale: 1.05, duration: 0.5, ease: "back.out(1.6)" }}, {E["drop"]:.2f});')
a(f'tl.fromTo("#fl", {{ opacity: 0 }}, {{ opacity: 0.4, duration: 0.04, immediateRender: false }}, {E["drop"]:.2f}); tl.to("#fl", {{ opacity: 0, duration: 0.5 }}, {E["drop"] + 0.05:.2f});')
a(f'tl.fromTo("#sweep", {{ x: 0 }}, {{ x: 1300, duration: 0.9, ease: "power2.inOut", immediateRender: false }}, {E["waiting"]:.2f});')

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

SFX = [(0.0, "boom_open", 0.5), (0.35, "shimmer", 0.6), (E["token"], "kaching", 0.7), (E["token"], "impact", 0.5), (E["tiny"], "pop", 0.4),
       (E["quit"] - 0.3, "footsteps", 0.6), (E["rig"] - 0.05, "pop", 0.45), (E["imp"] - 0.05, "pop", 0.45), (E["waste"] - 0.05, "pop", 0.45), (E["zero"], "impact", 0.45),
       (E["round_"], "count_fast", 0.45), (E["round_"] + 1.2, "coin_jar", 0.5), (E["stop"], "spot", 0.7), (E["kids"], "heartbeat", 0.55), (E["did"] - 0.1, "pop", 0.4),
       (E["gave"] - 0.3, "pop", 0.35), (E["no"] - 0.13, "stamp", 1.0), (E["no"], "impact", 0.6), (E["drop"] - 0.03, "zoom_whoosh", 0.5), (E["drop"], "kaching", 0.8), (E["waiting"], "shimmer", 0.6)]
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
