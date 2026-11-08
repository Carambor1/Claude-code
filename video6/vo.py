import json, base64, urllib.request, subprocess
V = "EXAVITQu4vr4xnSDxMaL"  # Sarah
L = {
 "h1": "Napoleon wasn't short.",
 "h2": "And that's not even the craziest thing you were taught.",
 "m1": "Napoleon was tiny.", "t1": "He was about one meter sixty-nine. Average for his time. British cartoons made him small.",
 "m2": "Vikings wore horned helmets.", "t2": "They didn't. The horns came from an opera costume in 1876.",
 "m3": "Goldfish have a three-second memory.", "t3": "Wrong. They can remember things for months.",
 "m4": "You can see the Great Wall of China from space.", "t4": "Not with your eyes. It's long, but only a few meters wide.",
 "m5": "Bulls hate the color red.", "t5": "Bulls can't even see red. They charge at the movement.",
 "m6": "Lightning never strikes the same place twice.", "t6": "The Empire State Building gets hit about twenty times a year.",
 "m7": "We only use ten percent of our brain.", "t7": "Brain scans show we use virtually all of it.",
 "e1": "So which one did you believe?",
}
out = {}
for k, t in L.items():
    body = json.dumps({"text": t, "model_id": "eleven_v4", "language_code": "en", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}).encode()
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
    out[k] = {"text": t, "dur": dur, "words": words}
json.dump(out, open("vo.json", "w"), indent=1)
print({k: round(v["dur"], 2) for k, v in out.items()})
