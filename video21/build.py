#!/usr/bin/env python3
""""I Carry the King" — 30 s devlog teaser, fully animated. Low-poly 3D film (src/film.js -> assets/film.js) plus overlays:
fake engine bar, anger meter, code window, end card, and big word-by-word captions with coloured keywords. Run: python3 build.py"""
import json, re, subprocess, os

VO = json.load(open("vo.json"))
ORDER = [f"r{i}" for i in range(1, 7)]
TEMPO = 1.08
for k in ORDER:
    if not os.path.exists(f"assets/vo/{k}_t.mp3"):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"assets/vo/{k}.mp3", "-af", f"atempo={TEMPO}", f"assets/vo/{k}_t.mp3"], check=True)
    VO[k]["dur"] /= TEMPO; VO[k]["words"] = [(x, t / TEMPO) for x, t in VO[k]["words"]]
GAP = {"r1": 0.3, "r2": 0.3, "r3": 0.35, "r4": 0.3, "r5": 0.3}
T, at = 0.25, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.3)
DUR = round(T + 2.2, 2)
W, H = 1080, 1920
norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if norm(x) == word]
    return round(at[k] + hits[nth], 2)
S2, S3, S4, S5, S6 = (round(at[f"r{i}"] - 0.15, 2) for i in range(2, 7))
K = dict(trip=w("r1", "ohne") - 0.05, vier=w("r2", "vier") - 0.1, koenig=w("r2", "knig") - 0.3, tragen=w("r2", "tragen") - 0.1,
         wackelt=at["r3"], wuetend2=w("r3", "wtend", 1), ab=w("r3", "ab"), kerkerCut=w("r3", "ab") + 0.12,
         brueckeCut=w("r4", "wackelige") - 0.15, burgCut=w("r4", "und") - 0.1, at=dict(s2=S2, s3=S3, s4=S4, s5=S5, s6=S6))
GOLD, RED = "#ffcf33", "#ff4b3e"
KEY = {"steamspiel": GOLD, "knig": GOLD, "kerker": RED, "wtend": RED, "gnse": GOLD, "brcken": GOLD, "burg": GOLD, "ki": GOLD, "steam": GOLD, "freunde": GOLD, "tragen": GOLD}
CODE = ["// carry_king.cs", "void Update() {", "  var wobble = sedan.Tilt(input);", "  king.anger += wobble * dt;", "  if (king.anger > 100f) {", "    Dungeon.Send(worstCarrier);", "    king.anger = 0f;", "  }", "}", "",
        "void OnGooseContact(Goose g) {", "  carriers.Panic(2.5f);", "  sedan.AddShake(g.rage);", "}", "", "bool BridgeHolds() =>", "  planks.All(p => p.intact)", "  && king.weight < 9000f;", "", "// TODO: castle on the mountain"]
CROWN = f'<svg viewBox="0 0 200 140"><path d="M14 124 L26 34 L66 78 L100 14 L134 78 L174 34 L186 124 Z" fill="{GOLD}"/><rect x="14" y="112" width="172" height="20" rx="6" fill="#e0a800"/><circle cx="26" cy="30" r="12" fill="{GOLD}"/><circle cx="100" cy="12" r="12" fill="{GOLD}"/><circle cx="174" cy="30" r="12" fill="{GOLD}"/><circle cx="100" cy="100" r="9" fill="{RED}"/></svg>'
body = (f'<canvas id="gl" width="720" height="1280" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px"></canvas>'
        '<div class="abs vig"></div>'
        '<div class="abs eng" id="eng"><span class="tab">Scene</span><span class="tab on">Game</span><div class="btns"><b id="pb"><i></i></b><b class="pz"></b><b class="st"></b></div><span class="tab r">Day 12</span></div>'
        '<div class="abs cur" id="cur"></div>'
        '<div class="abs meter" id="mt"><div class="mf" id="mf"></div><span>WUT</span></div>'
        '<div class="abs bars" id="bars">' + "".join(f'<i style="left:{60 + i * 120}px"></i>' for i in range(9)) + '</div>'
        '<div class="abs term" id="term"><div class="tb"><i></i><i></i><i></i><span>carry_king.cs — built with AI</span></div><div class="code">' + "".join(f'<div class="cl" id="cl{i}">{x.replace("<", "&lt;") or "&nbsp;"}</div>' for i, x in enumerate(CODE)) + '</div></div>'
        '<div class="abs day" id="day">TAG <b id="dn">1</b></div>'
        '<div class="abs end" id="end"><div class="crown" id="crw">' + CROWN + '</div><div class="t1" id="et1">I CARRY</div><div class="t2" id="et2">THE KING</div></div><div class="abs fol" id="fol">Folgen für Teil 2</div>')
CSS = f"""
    #root {{ position: absolute; inset: 0; background: #000; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
    #root .abs {{ position: absolute; }}
    #root .vig {{ inset: 0; background: radial-gradient(ellipse 80% 66% at 50% 46%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.38) 100%); }}
    #root .eng {{ left: 60px; top: 150px; width: 960px; height: 104px; border-radius: 26px; background: rgba(28,30,36,0.94); display: flex; align-items: center; gap: 12px; padding: 0 26px; box-shadow: 0 16px 40px rgba(0,0,0,0.4); font-weight: 700; font-size: 34px; }}
    #root .tab {{ padding: 12px 24px; border-radius: 14px; color: #9aa0ab; }}
    #root .tab.on {{ background: #3a3f4b; color: #fff; }}
    #root .tab.r {{ margin-left: auto; }}
    #root .btns {{ position: absolute; left: 380px; display: flex; gap: 14px; }}
    #root .btns b {{ width: 76px; height: 68px; border-radius: 14px; background: #3a3f4b; display: flex; align-items: center; justify-content: center; }}
    #root .btns b i {{ width: 0; height: 0; border-left: 28px solid #fff; border-top: 17px solid transparent; border-bottom: 17px solid transparent; }}
    #root .btns .pz::before {{ content: ""; width: 26px; height: 32px; border-left: 9px solid #9aa0ab; border-right: 9px solid #9aa0ab; }}
    #root .btns .st::before {{ content: ""; width: 30px; height: 30px; background: #9aa0ab; border-radius: 4px; }}
    #root .cur {{ left: 620px; top: 420px; width: 0; height: 0; border-left: 34px solid #fff; border-bottom: 34px solid transparent; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.6)); transform: rotate(8deg); }}
    #root .meter {{ left: 936px; top: 420px; width: 84px; height: 620px; border-radius: 42px; background: rgba(20,20,24,0.8); border: 5px solid #fff; overflow: hidden; opacity: 0; }}
    #root .mf {{ position: absolute; left: 0; right: 0; bottom: 0; height: 100%; background: linear-gradient(0deg, #ffb300, {RED}); transform-origin: 50% 100%; transform: scaleY(0.04); }}
    #root .meter span {{ position: absolute; left: 0; width: 100%; bottom: 20px; text-align: center; font-weight: 900; font-size: 26px; }}
    #root .bars {{ inset: 0; opacity: 0; }}
    #root .bars i {{ position: absolute; top: -40px; width: 34px; height: 2000px; background: linear-gradient(90deg, #17181c, #3c3f47 50%, #17181c); box-shadow: 8px 0 20px rgba(0,0,0,0.5); }}
    #root .term {{ left: 60px; top: 330px; width: 960px; height: 1080px; border-radius: 30px; background: rgba(16,18,24,0.96); box-shadow: 0 30px 80px rgba(0,0,0,0.55); overflow: hidden; opacity: 0; transform-origin: 0 0; }}
    #root .tb {{ height: 80px; background: #23262f; display: flex; align-items: center; gap: 14px; padding: 0 28px; font-family: "JetBrains Mono", monospace; font-size: 26px; color: #9aa0ab; }}
    #root .tb i {{ width: 22px; height: 22px; border-radius: 50%; background: #ff5f57; }} #root .tb i:nth-child(2) {{ background: #febc2e; }} #root .tb i:nth-child(3) {{ background: #28c840; }}
    #root .tb span {{ margin-left: 16px; }}
    #root .code {{ padding: 30px 36px; font-family: "JetBrains Mono", monospace; font-weight: 500; font-size: 35px; line-height: 1.38; color: #d6dae3; white-space: pre; }}
    #root .cl {{ opacity: 0; }}
    #root .day {{ left: 610px; top: 300px; padding: 16px 40px; border-radius: 60px; background: {GOLD}; color: #1b1400; font-weight: 900; font-size: 64px; opacity: 0; box-shadow: 0 14px 34px rgba(0,0,0,0.45); }}
    #root .end {{ inset: 0; background: #000; display: flex; flex-direction: column; align-items: center; opacity: 0; }}
    #root .crown {{ margin-top: 380px; width: 300px; height: 210px; opacity: 0; }}
    #root .crown svg {{ width: 100%; height: 100%; }}
    #root .t1 {{ margin-top: 30px; font-weight: 900; font-size: 170px; letter-spacing: -0.04em; line-height: 1; opacity: 0; }}
    #root .t2 {{ font-weight: 900; font-size: 190px; letter-spacing: -0.04em; line-height: 1.02; color: {GOLD}; opacity: 0; white-space: nowrap; }}
    #root .fol {{ left: 250px; width: 580px; text-align: center; top: 1500px; padding: 22px 0; border-radius: 60px; background: #fff; color: #000; font-weight: 800; font-size: 54px; opacity: 0; }}
    #root .cap {{ left: 0; top: 1190px; width: {W}px; text-align: center; font-weight: 900; font-size: 136px; letter-spacing: -0.03em; line-height: 1; text-transform: uppercase; -webkit-text-stroke: 14px #000; paint-order: stroke fill; text-shadow: 0 10px 0 rgba(0,0,0,0.55); white-space: nowrap; }}
    #root .cap.sm {{ font-size: 104px; }}
"""
J = []; a = J.append
SFX = []; sx = lambda t, f, v=0.35: SFX.append((round(max(0, t), 2), f, v))
# 1 hook: cursor clicks Play, the king flies
a('tl.fromTo("#eng", { y: -260 }, { y: 0, duration: 0.4, ease: "back.out(1.4)" }, 0);')
a('tl.fromTo("#cur", { x: 240, y: 300 }, { x: -200, y: -212, duration: 0.42, ease: "power3.out" }, 0.05);')
a(f'tl.to("#pb", {{ backgroundColor: "#2f7df6", scale: 0.86, duration: 0.08 }}, 0.5); tl.to("#pb", {{ scale: 1, duration: 0.15 }}, 0.58);'); sx(0.5, "ui_tick2", 0.6); sx(0, "boom_open", 0.25)
a(f'tl.to(["#eng", "#cur"], {{ opacity: 0, y: -80, duration: 0.3 }}, {S2 - 0.3:.2f});')
sx(K["trip"], "boing", 0.7); sx(K["trip"] + 0.05, "swipe2", 0.35)
# 2 idea
for i in range(4): sx(K["vier"] + i * 0.14, "pop", 0.4)
sx(K["koenig"] + 0.33, "impact", 0.6); sx(K["koenig"], "swipe1", 0.3); sx(S2, "zoom_whoosh", 0.3)
# 3 anger meter, dungeon bars
a(f'tl.fromTo("#mt", {{ opacity: 0, x: 120 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.6)" }}, {S3 + 0.1:.2f});')
a(f'tl.fromTo("#mf", {{ scaleY: 0.04 }}, {{ scaleY: 1, duration: {K["wuetend2"] + 0.3 - K["wackelt"]:.2f}, ease: "power1.in" }}, {K["wackelt"]:.2f});')
a(f'tl.fromTo("#mt", {{ rotation: -3 }}, {{ rotation: 3, duration: 0.06, yoyo: true, repeat: {int((K["kerkerCut"] - K["wuetend2"]) / 0.06)}, ease: "sine.inOut", immediateRender: false }}, {K["wuetend2"]:.2f});')
a(f'tl.to("#mt", {{ opacity: 0, duration: 0.15 }}, {K["kerkerCut"] - 0.05:.2f});'); sx(K["wackelt"], "riser", 0.4); sx(K["wuetend2"], "heartbeat", 0.5)
tk = w("r3", "kerker")
a(f'tl.fromTo("#bars", {{ opacity: 1, y: -2000 }}, {{ y: 0, duration: 0.22, ease: "power3.in", immediateRender: false }}, {tk + 0.05:.2f}); tl.to("#bars", {{ opacity: 0, duration: 0.2 }}, {S4 - 0.12:.2f});'); sx(tk + 0.2, "cell", 0.8); sx(K["kerkerCut"], "swipe1", 0.3)
# 4 geese / bridge / castle
sx(S4, "honk", 0.75); sx(K["brueckeCut"], "creak", 0.75); sx(K["burgCut"], "fanfare", 0.6); sx(K["brueckeCut"], "swipe2", 0.3); sx(K["burgCut"], "zoom_whoosh", 0.3)
# 5 code window, then the game behind it + day counter
a(f'tl.fromTo("#term", {{ opacity: 0, y: 200, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.3)" }}, {S5:.2f});'); sx(S5, "swipe1", 0.3); sx(S5 + 0.2, "typing", 0.6)
tj = w("r5", "jeden") - 0.15
for i in range(len(CODE)): a(f'tl.to("#cl{i}", {{ opacity: 1, duration: 0.05 }}, {S5 + 0.3 + i * (tj - S5 - 0.4) / len(CODE):.2f});')
a(f'tl.to("#term", {{ scale: 0.42, x: 30, y: -40, duration: 0.6, ease: "power4.inOut" }}, {tj:.2f});'); sx(tj, "zoom_whoosh", 0.3)
a(f'tl.fromTo("#day", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {tj + 0.25:.2f});')
a(f'(() => {{ const o = {{ v: 1 }}; tl.fromTo(o, {{ v: 1 }}, {{ v: 12, duration: {S6 - tj - 0.5:.2f}, ease: "none", immediateRender: false, onUpdate: () => {{ $("#dn").textContent = Math.round(o.v); }} }}, {tj + 0.3:.2f}); }})();')
for i in range(6): sx(tj + 0.4 + i * (S6 - tj - 0.6) / 6, "ui_tick2", 0.4)
a(f'tl.to(["#term", "#day"], {{ opacity: 0, duration: 0.2 }}, {S6 - 0.2:.2f});')
# 6 end card
TEND = w("r6", "name") - 0.25
a(f'tl.to("#end", {{ opacity: 1, duration: 0.3 }}, {TEND:.2f});')
a(f'tl.fromTo("#fol", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.6)" }}, {w("r6", "folg"):.2f});')
tn = w("r6", "i") - 0.1
a(f'tl.fromTo("#crw", {{ opacity: 0, y: -260, rotation: -25 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "bounce.out" }}, {tn - 0.3:.2f});'); sx(tn - 0.3, "fanfare", 0.45)
a(f'tl.fromTo("#et1", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {tn:.2f}); tl.fromTo("#et2", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {w("r6", "the") - 0.08:.2f});'); sx(tn, "impact", 0.5); sx(w("r6", "the") - 0.08, "impact", 0.55)
a(f'tl.fromTo("#fol", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.4, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, {w("r6", "king") + 0.3:.2f});')
# captions: one big word at a time
caps = []; n = 0
for k in ORDER:
    ws = VO[k]["words"]
    for i, (wd, t0) in enumerate(ws):
        if k == "r6" and i >= len(ws) - 4: break        # the title itself is the end card
        s0 = round(at[k] + t0 - 0.04, 2); e0 = round(at[k] + (ws[i + 1][1] if i + 1 < len(ws) else VO[k]["dur"] + 0.1) - 0.04, 2)
        txt = re.sub(r"[.,:…!?]", "", wd); col = KEY.get(norm(wd), "#fff")
        caps.append(f'<div id="cp{n}" class="abs cap {"sm" if len(txt) > 9 else ""} clip" data-start="{s0}" data-duration="{round(max(0.12, e0 - s0), 2)}" style="color:{col}">{txt}</div>')
        a(f'tl.fromTo("#cp{n}", {{ scale: 0.55, rotation: {(-4, 3, -2, 4)[n % 4]} }}, {{ scale: 1, rotation: {(-1.5, 1.5, 0, -1)[n % 4]}, duration: 0.16, ease: "back.out(3)" }}, {s0:.2f});'); n += 1

subprocess.run(["node_modules/.bin/esbuild", "src/film.js", "--bundle", "--format=iife", "--global-name=Film", "--minify", "--outfile=assets/film.js", "--log-level=warning"], check=True)
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
    let film = null; const clock = {{ t: 0 }};
    window.__hf = window.__hf || {{}}; window.__hf.buildReady = window.__hf.buildReady || {{}};
    window.__hf.buildReady["film"] = Film.init($("#gl"), {json.dumps(K)}).then((f) => {{ film = f; f.render(clock.t); }});
    tl.fromTo(clock, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: () => {{ if (film && clock.t < {w("r6", "name") + 0.2:.2f}) film.render(clock.t); }} }}, 0);
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
<script src="assets/film.js"></script>
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
