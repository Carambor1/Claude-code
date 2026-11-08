# Video workflow (agreed with the user)

- New video request → do NOT post progress in chat. Instead write it to the live page
  https://claude.ai/artifact/2dYRGf3pSttpCuSG6vgQut (source: tools/shorts-factory.html) via ArtifactData:
  - `pipeline/current`: { title, plan: [..], startedAt (ms), finishedAt (ms|null),
    stages: { Script|Voice|Sound FX|Animation|Check|Render|Upload: { status: pending|active|done, startedAt, est (min) } } }
  - `log/<id>`: { t (ms), stage, msg } — one entry per real step.
- Chat: only short replies; the finished video is still sent as a file.
- Defaults: English, female voice (ElevenLabs "Sarah", passionate/dramatic), no music, 9:16, DLF-like style.
- Stats log: video-stats.md
