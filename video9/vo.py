import json, base64, urllib.request, subprocess
V = "EXAVITQu4vr4xnSDxMaL"  # Sarah, dramatic settings
L = {
 "p1": "[passionate] The first thousand euros is the hardest money you'll ever make.",
 "p2": "Sounds wrong. Watch.",
 "p3": "Month one. Zero. Nobody's impressed.",
 "p4": "Month three. Two hundred. You want to quit.",
 "p5": "Month eight. One thousand. Finally.",
 "p6": "But here's what nobody tells you. You didn't just make a thousand euros.",
 "p7": "You learned how to sell. How to save. How to show up.",
 "p8": "So the next thousand? Four months.",
 "p9": "Then two. Then one.",
 "p10": "Same person. Different skills.",
 "p11": "[confident] Ten thousand doesn't start at ten thousand. It starts at your first euro.",
 "p12": "[passionate] So go make it. Today.",
}
out = {}
for k, t in L.items():
    body = json.dumps({"text": t, "model_id": "eleven_v4", "language_code": "en", "voice_settings": {"stability": 0.0, "similarity_boost": 0.85}}).encode()
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
