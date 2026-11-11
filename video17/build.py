#!/usr/bin/env python3
""""Every Second on Earth" — 3D version. Three.js film (src/film.js -> assets/film.js via esbuild) drawn from timeline time,
with clean typography on top. Real NASA Blue Marble textures (via three-globe). Run: python3 build.py"""
import json, re, subprocess

VO = json.load(open("vo.json"))
ORDER = [f"r{i}" for i in range(1, 10)]
GAP = {"r1": 0.5, "r2": 0.45, "r3": 0.45, "r4": 0.45, "r5": 0.45, "r6": 0.5, "r7": 0.6, "r8": 0.6}
T, at = 0.35, {}
for k in ORDER:
    at[k] = T
    T += VO[k]["dur"] + GAP.get(k, 0.3)
DUR = round(T + 3.0, 2)
W, H = 1080, 1920
def w(k, word, nth=0):
    hits = [t for x, t in VO[k]["words"] if re.sub(r"[^a-z0-9]", "", x.lower()) == word]
    return round(at[k] + hits[nth], 2)

LAP = 0.3
K = dict(DUR=DUR, births=[round(w("r1", "four") + 0.05 + i * 0.28, 2) for i in range(4)], strike=w("r2", "strike") - 0.2, lapStart=w("r6", "circle") - 0.4, lap=LAP,
         at=dict(strikeCam=at["r2"] - 0.2, bee=at["r3"] - 0.3, blood=at["r4"] - 0.3, fly=at["r5"] - 0.3, light=at["r6"], sun=at["r7"] - 0.3, end=at["r8"] - 0.35))
CUT = [(K["at"]["bee"], "#fff"), (K["at"]["blood"], "#3a0508"), (K["at"]["fly"], "#000"), (K["at"]["sun"], "#fff3d0"), (K["at"]["end"], "#000")]

FACTS = [("f1", "4", "BABIES BORN", w("r1", "four") - 0.15, K["at"]["strikeCam"], None),
         ("f2", "40+", "LIGHTNING STRIKES", w("r2", "more") - 0.2, K["at"]["bee"], None),
         ("f3", "200", "WING BEATS", w("r3", "two") - 0.3, K["at"]["blood"], (200, 0.9, "Math.round(o.v)")),
         ("f4", "2,000,000", "NEW BLOOD CELLS · IN YOUR BODY", w("r4", "two") - 0.3, K["at"]["fly"], (2000000, 1.2, "Math.round(o.v).toLocaleString('en-US')")),
         ("f5", "30 km", "THROUGH SPACE", w("r5", "thirty") - 0.3, K["at"]["light"] - 0.3, (30, 0.9, "Math.round(o.v) + ' km'")),
         ("f6", "7×", "AROUND THE EARTH", K["lapStart"], K["at"]["sun"], None),
         ("f7", "4,000,000", "TONS OF THE SUN · BURNED", w("r7", "four") - 0.3, K["at"]["end"], (4000000, 1.2, "Math.round(o.v).toLocaleString('en-US')"))]
QW = "So what did you do with yours?".split()
body = f"""
    <canvas id="gl" width="720" height="1280" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px"></canvas>
    <div class="abs vig"></div>
    <div class="abs fade" id="fade"></div>
    <div class="abs ctr kick" id="kick">IN THE NEXT SECOND</div>
    {"".join(f'<div class="abs ctr fact" id="{i}"><div class="fn {"sm" if len(n) > 6 else ""}" id="{i}n">{n}</div><div class="fl">{l}</div></div>' for i, n, l, *_ in FACTS)}
    <div class="abs ctr big" id="all1">All of that.</div><div class="abs ctr big" id="all2">In <span>one second.</span></div>
    <div class="abs ctr qq" id="qq">{" ".join(f'<span class="qw" id="qw{i}">{x}</span>' + ("<br>" if i == 4 else "") for i, x in enumerate(QW))}</div>
"""
CSS = f"""
    #root {{ position: absolute; inset: 0; background: #000; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
    #root .abs {{ position: absolute; }}
    #root .ctr {{ left: 0; width: {W}px; text-align: center; }}
    #root .vig {{ inset: 0; background: radial-gradient(ellipse 75% 62% at 50% 46%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%); }}
    #root .fade {{ inset: 0; background: #000; opacity: 0; }}
    #root .kick {{ top: 236px; font-weight: 800; font-size: 46px; letter-spacing: 0.42em; text-indent: 0.42em; text-shadow: 0 2px 18px rgba(0,0,0,0.8); opacity: 0; }}
    #root .fact {{ top: 190px; opacity: 0; text-shadow: 0 4px 30px rgba(0,0,0,0.55), 0 0 2px rgba(0,0,0,0.5); }}
    #root .fn {{ font-weight: 900; font-size: 250px; letter-spacing: -0.04em; line-height: 1; font-variant-numeric: tabular-nums; }}
    #root .fn.sm {{ font-size: 170px; }}
    #root .fl {{ margin-top: 14px; font-weight: 700; font-size: 44px; letter-spacing: 0.3em; text-indent: 0.3em; }}
    #root .big {{ top: 300px; font-weight: 800; font-size: 120px; letter-spacing: -0.03em; opacity: 0; text-shadow: 0 4px 30px rgba(0,0,0,0.6); }}
    #root .big span {{ color: #ffd27a; }}
    #root .qq {{ top: 250px; font-weight: 800; font-size: 104px; line-height: 1.12; letter-spacing: -0.03em; text-shadow: 0 4px 30px rgba(0,0,0,0.6); }}
    #root .qw {{ display: inline-block; opacity: 0; }}
    #root #qw6 {{ color: #ffd27a; }}
"""
J = []; a = J.append
SFX = []; sx = lambda t, f, v=0.35: SFX.append((round(max(0, t), 2), f, v))
# set changes: quick dip through a colour while the camera pushes in / pulls out
for t0, col in CUT:
    a(f'tl.set("#fade", {{ backgroundColor: "{col}" }}, {t0 - 0.3:.2f});')
    a(f'tl.fromTo("#fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.26, ease: "power2.in", immediateRender: false }}, {t0 - 0.26:.2f});')
    a(f'tl.to("#fade", {{ opacity: 0, duration: 0.4, ease: "power2.out" }}, {t0:.2f});'); sx(t0 - 0.35, "zoom_whoosh", 0.32)
a('tl.fromTo("#fade", { opacity: 1, backgroundColor: "#000" }, { opacity: 0, duration: 0.7, ease: "power2.out" }, 0);')
a(f'tl.fromTo("#fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power2.in", immediateRender: false }}, {DUR - 0.6:.2f});')
a(f'tl.set("#fade", {{ backgroundColor: "#000" }}, {DUR - 0.65:.2f});')
a('tl.fromTo("#kick", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 0.25);')
a(f'tl.to("#kick", {{ opacity: 0, y: -14, duration: 0.35, ease: "power2.in" }}, {w("r1", "four") - 0.5:.2f});')
for i, n, l, t0, t1, cnt in FACTS:
    a(f'tl.fromTo("#{i}", {{ opacity: 0, y: 46, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power4.out" }}, {t0:.2f});')
    a(f'tl.to("#{i}", {{ opacity: 0, y: -24, duration: 0.3, ease: "power2.in" }}, {t1 - 0.42:.2f});')
    if cnt:
        end, d, fmt = cnt
        a(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {end}, duration: {d}, ease: "power3.out", immediateRender: false, onUpdate: () => {{ $("#{i}n").textContent = {fmt}; }} }}, {t0:.2f}); }})();')
        sx(t0, "count_fast", 0.28)
    sx(t0, "impact", 0.36)
a('tl.call(() => { $("#f6n").textContent = "0×"; }, null, 0);')
for i in range(7):
    a(f'tl.call(() => {{ $("#f6n").textContent = "{i + 1}×"; }}, null, {K["lapStart"] + (i + 1) * LAP:.2f});'); sx(K["lapStart"] + (i + 1) * LAP, "ui_tick2", 0.4)
for i, t0 in enumerate(K["births"]): sx(t0, "ping", 0.36)
for i in range(9): sx(K["strike"] + i * 0.33, "impact", 0.2)
sx(0, "boom_open", 0.35); sx(0.2, "space", 0.4); sx(K["at"]["bee"] + 0.1, "rustle", 0.3); sx(K["at"]["blood"] + 0.1, "heartbeat", 0.5); sx(K["at"]["blood"] + 1.6, "heartbeat", 0.5)
sx(K["at"]["fly"] + 0.1, "big_pass", 0.4); sx(K["lapStart"], "warp", 0.35); sx(K["at"]["sun"] + 0.1, "flare", 0.45); sx(K["at"]["sun"] + 0.2, "riser", 0.3); sx(K["at"]["end"] + 0.1, "cosmic", 0.4)
# finale typography
t8, t8b = at["r8"], w("r8", "in") - 0.15
a(f'tl.fromTo("#all1", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power4.out" }}, {t8:.2f});')
a(f'tl.to("#all1", {{ opacity: 0, y: -20, duration: 0.3, ease: "power2.in" }}, {t8b - 0.3:.2f});')
a(f'tl.fromTo("#all2", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power4.out" }}, {t8b:.2f});'); sx(w("r8", "second"), "clock_tick", 0.7); sx(t8b, "impact", 0.4)
a(f'tl.to("#all2", {{ opacity: 0, y: -20, duration: 0.3, ease: "power2.in" }}, {at["r9"] - 0.35:.2f});')
QT = [w("r9", x) for x in ("so", "what", "did", "you", "do", "with", "yours")]
for i, t0 in enumerate(QT):
    a(f'tl.fromTo("#qw{i}", {{ opacity: 0, y: 34 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, {t0 - 0.08:.2f});')
sx(QT[6], "shimmer", 0.4)

subprocess.run(["node_modules/.bin/esbuild", "src/film.js", "--bundle", "--format=iife", "--global-name=Film", "--minify", "--outfile=assets/film.js", "--log-level=warning"], check=True)
open("compositions/w.html", "w").write(f"""<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="w" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    {body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const R = document.querySelector('[data-composition-id="w"]') || document;
    const $ = (s) => R.querySelector(s);
    const clock = {{ t: 0 }}; let film = null;
    window.__hf = window.__hf || {{}}; window.__hf.buildReady = window.__hf.buildReady || {{}};
    window.__hf.buildReady["film"] = Film.init($("#gl"), {json.dumps(K)}).then((f) => {{ film = f; f.render(clock.t); }});
    tl.fromTo(clock, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: () => {{ if (film) film.render(clock.t); }} }}, 0);
{chr(10).join("    " + x for x in J)}
    window.__timelines["w"] = tl;
  </script>
</template>
""")

grp = []
for k in ORDER[:7]:
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
    #root .cap {{ left: 90px; width: 900px; top: 1520px; text-align: center; font-weight: 800; font-size: 58px; line-height: 1.15; color: #fff; }}
    #root .cap span {{ display: inline-block; background: rgba(0,0,0,0.55); padding: 6px 22px 10px; border-radius: 16px; }}
  </style>
  <div id="root" data-composition-id="cap" data-width="{W}" data-height="{H}">
{chr(10).join("    " + c for c in caps)}
  </div>
  <script>window.__timelines["cap"] = gsap.timeline({{ paused: true }});</script>
</template>
""")

dur = {f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/sfx/{f}.mp3"], capture_output=True, text=True).stdout) for f in {x[1] for x in SFX}}
aud = [f'  <audio id="vo-{k}" class="clip" src="assets/vo/{k}.mp3" data-start="{round(at[k], 2)}" data-duration="{round(VO[k]["dur"] - 0.01, 2)}" data-track-index="2" data-volume="1.8"></audio>' for k in ORDER]
aud += [f'  <audio id="sx{n}" class="clip" src="assets/sfx/{f}.mp3" data-start="{max(0, t)}" data-duration="{round(min(dur[f], DUR - t) - 0.01, 2)}" data-track-index="{10 + n}" data-volume="{v}"></audio>' for n, (t, f, v) in enumerate(SFX) if t < DUR - 0.2]
open("index.html", "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" />
<script src="assets/vendor/gsap.min.js"></script>
<script src="assets/film.js"></script>
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
