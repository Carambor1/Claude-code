import json, base64, urllib.request, subprocess
V = "EXAVITQu4vr4xnSDxMaL"  # Sarah, dramatic settings
L = {
 "r1": "[confident] This account has no face. No name. No voice of its own. And it gets paid, every single month.",
 "r2": "Here's how faceless accounts actually make money.",
 "r3": "One. Views. Once you hit ten thousand followers, TikTok's Creator Rewards program pays you for videos longer than one minute.",
 "r4": "Two. Affiliate links. You recommend a product. Someone buys it. You earn a commission. And you never even touch the product.",
 "r5": "Three. Digital products. A template. A guide. A preset pack. You make it once, and sell it again, and again, and again.",
 "r6": "Four. Brand deals. When a page owns a niche, brands pay to be seen on it.",
 "r7": "[serious] But here's what nobody tells you. The views usually pay the least. The real money is in what you sell.",
 "r8": "[confident] So the method is simple. Pick one niche. Post every single day. And give it ninety days before you judge it.",
 "r9": "Nobody needs to see your face. They just need a reason to follow.",
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
