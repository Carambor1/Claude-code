import json, base64, urllib.request, subprocess
V = "EXAVITQu4vr4xnSDxMaL"  # Sarah, dramatic settings
L = {
 "r1": "[confident] In the next second, four babies will be born.",
 "r2": "Lightning will strike the Earth more than forty times.",
 "r3": "A bee will beat its wings two hundred times.",
 "r4": "Your body will build two million new blood cells.",
 "r5": "The planet will fly thirty kilometers through space.",
 "r6": "A beam of light could circle the Earth seven times.",
 "r7": "And the Sun will burn four million tons of itself.",
 "r8": "All of that, in one second.",
 "r9": "So what did you do with yours?",
}
out = {}
for k, t in L.items():
    body = json.dumps({"text": t, "model_id": "eleven_v4", "language_code": "en", "voice_settings": {"stability": 0.4, "similarity_boost": 0.85}}).encode()
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
