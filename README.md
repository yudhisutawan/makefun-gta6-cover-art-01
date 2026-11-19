# Vice Cover Studio

[![make.fun competition](https://make.fun/badges/competition/gta6-cover-art-01.svg)](https://make.fun/bounty/gta6-cover-art-01) [![make.fun reward](https://make.fun/badges/reward/gta6-cover-art-01.svg)](https://make.fun/bounty/gta6-cover-art-01#reward)

Vice Cover Studio turns photos and a caption into GTA 6-style multi-panel cover art in the browser, offline, with photos never leaving the machine.

## What it does

- Three layouts: Sunset Strip (3 panels), Vice Grid (4 panels), and Vice Poster (3 panels).
- Load any photo and crop or reposition it per panel.
- Add bold caption lettering and an editable subtitle.
- Choose Sunset, Neon, Noir, or Palm Dusk colour grades.
- Export PNGs in wide 1920 × 1080, square 1080 × 1080, and portrait 1080 × 1350 sizes, with seeded film grain and deterministic screenshot scenes.

## Try it

```sh
node serve.ts
```

Open <http://127.0.0.1:8080/>. Capture the deterministic screenshots with:

```sh
/home/hatch/workspace/research/airdrop-agent/.venv/bin/python tools/shots.py
```

Hand in the entry and check its package limits with:

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
node tools/check.mjs out
```

## Files

- `app/` — offline editor, renderer, shot runner, and sample photos.
- `tools/make-samples.py` — reproducible procedural sample art generator.
- `tools/shots.py` — deterministic browser screenshot capture.
- `tools/smoke.py` — browser interaction and export smoke check.
- `tools/check.mjs` — package gate validation.
- `main.ts` — builds the output hand-in folder and dossier.
- `serve.ts` — local development server.
- `shots.json` — screenshot scene definitions.

The artwork is original and drawn in code. Vice Cover Studio is not affiliated with Rockstar Games.

---

Referred by make.fun code **2fnbbcz4**: [this make.fun bounty](https://make.fun/bounty/gta6-cover-art-01) · [use the referral link](https://make.fun/r/2fnbbcz4)
