import json, base64, urllib.request, subprocess
V = "EXAVITQu4vr4xnSDxMaL"  # Sarah, dramatic settings
L = {
 "c1": "[passionate] Your salary is a ceiling.",
 "c2": "Your boss decides what you're worth. Every year. Three percent, if you're lucky.",
 "c3": "Forty hours a week. Same desk. Same number.",
 "c4": "Now watch what happens with one side project.",
 "c5": "One hour a day. First month? Fifty euros.",
 "c6": "Month six. Five hundred.",
 "c7": "Month twelve. Two thousand. More than your last five raises combined.",
 "c8": "Your salary stops where they say. Your skills stop where you say.",
 "c9": "[confident] The ceiling was never the limit.",
 "c10": "[passionate] So build something. Tonight.",
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
