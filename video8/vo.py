import json, base64, urllib.request, subprocess
V = "EXAVITQu4vr4xnSDxMaL"  # Sarah, dramatic settings
L = {
 "n1": "[passionate] [confident] Nobody's coming to save you!",
 "n2": "Not your parents. Not your boss. Not the algorithm.",
 "n3": "[shouting] YOU!",
 "n4": "[confident] Sounds harsh? It's not. It's freedom.",
 "n5": "Because if nobody's coming... nobody can stop you either.",
 "n6": "[passionate] No permission. No perfect moment. No Monday.",
 "n7": "One hour a day. One rep. One page. One call.",
 "n8": "Six months from now, you'll be someone they don't recognize.",
 "n9": "They'll ask how. You'll just smile.",
 "n10": "[passionate] So stop waiting. Because nobody's coming...",
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
