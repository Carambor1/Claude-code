import json, base64, urllib.request, subprocess
V = "EXAVITQu4vr4xnSDxMaL"  # Sarah, dramatic settings
L = {
 "r1": "[calm] Earning more money won't make you rich.",
 "r2": "Imagine getting a raise. A big one. Twenty percent more, every single month.",
 "r3": "It feels like everything is about to change.",
 "r4": "A nicer apartment. A better car. Eating out a little more often. After all, you earned it.",
 "r5": "But there's something most people overlook.",
 "r6": "Your income went up. And so did everything else.",
 "r7": "A year later, the raise is gone. Not taken. Spent. Quietly. One upgrade at a time.",
 "r8": "It's called lifestyle inflation. Most people just call it normal.",
 "r9": "The problem begins when you measure your progress by what you earn, instead of what you keep.",
 "r10": "Because a bigger salary only raises the ceiling. It doesn't build the floor.",
 "r11": "This is why some people with modest incomes quietly become wealthy, while others earning twice as much never do.",
 "r12": "It's not about how much comes in. It's about how much stays.",
 "r13": "Earning more won't make you rich. Keeping more will.",
}
out = {}
for k, t in L.items():
    body = json.dumps({"text": t, "model_id": "eleven_v4", "language_code": "en", "voice_settings": {"stability": 0.55, "similarity_boost": 0.8}}).encode()
    r = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps?output_format=mp3_44100_128", data=body, headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    d = json.loads(urllib.request.urlopen(r, timeout=120).read())
    open(f"assets/vo/{k}.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    a = d.get("normalized_alignment") or d["alignment"]
    words, cur, st = [], "", None
    for ch, s in zip(a["characters"], a["character_start_times_seconds"]):
        if ch.isspace():
            if cur: words.append((cur, st)); cur = ""
        else:
            if not cur: st = s
            cur += ch
    if cur: words.append((cur, st))
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{k}.mp3"], capture_output=True, text=True).stdout)
    import re
    words = [(w, s0) for w, s0 in words if not re.fullmatch(r"\[[a-z]+\]", w)]
    out[k] = {"text": re.sub(r"\[[a-z]+\] ?", "", t), "dur": dur, "words": words}
json.dump(out, open("vo.json", "w"), indent=1)
print({k: round(v["dur"], 2) for k, v in out.items()})
