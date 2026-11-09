# Video workflow (agreed with the user)

- New video request → do NOT post progress in chat. Instead write it to the live page
  https://claude.ai/artifact/2dYRGf3pSttpCuSG6vgQut (source: tools/shorts-factory.html) via ArtifactData:
  - `pipeline/current`: { title, plan: [..], startedAt (ms), finishedAt (ms|null),
    stages: { Script|Voice|Sound FX|Animation|Check|Render|Upload: { status: pending|active|done, startedAt, est (min) } } }
  - `log/<id>`: { t (ms), stage, msg } — one entry per real step.
- Chat: only short replies; the finished video is still sent as a file.
- Defaults: English, female voice (ElevenLabs "Sarah", passionate/dramatic or calm for essays), no music, DLF/cryothum style.
- Never use [whispers] (or any whispering) in the voice. User asked to stop it.
- Stats log: video-stats.md
- Visual direction (from the user): more pictures/symbol icons, less on-screen text; cleaner, smoother transitions
  (e.g. one element morphs/moves into the next, consistent easing, no hard cuts or blur-swaps); icons carry the story.
- Look (from the user): dotted grid background + soft white glow on all graphics, like the reference videos.

## Videos-Ordner
Haupt-Ablage ist die Seite **Shorts Library** (https://claude.ai/artifact/4msEKa1pN6jDx3wbC9cpoK): neues Video als Asset hochladen und als Dokument `videos/vNN` eintragen ({n,title,hashtags,lang,duration,folders[motivation|finanzen|fakten|deutsch],assetId,url,posted:{tiktok,youtube}}).
Jedes fertige Video sofort als `Videos/NN - Titel.mp4` ablegen und in `Videos/README.md` eintragen (Tabelle + Titel + 5 Hashtags). Oben im README bleibt der Link zur Shorts Factory.
