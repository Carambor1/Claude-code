import json, base64, urllib.request, subprocess
V = "EXAVITQu4vr4xnSDxMaL"  # Sarah, dramatic settings
L = {
 "s1": "[dramatic] This five-euro habit is worth three hundred sixty-four thousand euros.",
 "s2": "[whispers] And almost nobody does it.",
 "s3": "Five euros a day. One coffee. Put it away instead.",
 "s4": "That's eighteen hundred twenty-five euros a year.",
 "s5": "Invest it. Let's say seven percent a year.",
 "s6": "After ten years? Twenty-five thousand. Nice. But boring.",
 "s7": "Twenty years. Seventy-five thousand.",
 "s8": "Thirty years. A hundred seventy-two thousand.",
 "s9": "Forty years. [dramatic] Three hundred sixty-four thousand euros.",
 "s10": "But here's the crazy part. You only paid in seventy-three thousand.",
 "s11": "The other two hundred ninety-one thousand? Your money made that. On its own.",
 "s12": "And if you wait ten years to start, you lose almost two hundred thousand.",
 "s13": "[whispers] So... how much was that coffee, really?",
}
out = {}
for k, t in L.items():
    body = json.dumps({"text": t, "model_id": "eleven_v4", "language_code": "en", "voice_settings": {"stability": 0.2, "similarity_boost": 0.85}}).encode()
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
