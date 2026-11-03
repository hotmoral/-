# DeepHold I3K-A2 — Cloudflare mobile device QA
Source authority: private `hotmoral/DeepHold`, QA branch `qa/i3k-android-crowd-device-harness-v1` at `6f227d2a03a2f8750f469cafcb35787f48d2052d`.

This directory contains **only the validated QA-flag Vite build**. The existing `/deephold-i1/` playable snapshot and the Worker `/api/health` are untouched.

Visit: `/deephold-i1/qa/i3k-a2/?crowd-qa=1` on a physical landscape Android Chrome.
Choose control/P1/C5/C20S1/C50S3/P3/P4/P5 and 20/60/120 seconds. Start and operate joystick and the existing five skill buttons during sampling. Export JSON using the overlay. Run separate fresh-page samples for each scenario.

P1/P3/P4/P5 use 20/30 **real materialized** Gnawer hostiles. Hostiles have **QA-only 5,000HP**, and the player is protected from death. P5 adds artificial Phaser pulse/VFX load, not full projectile simulation. All Special 5 are Ferrix S3, not five different species. The exported `loadMaintained` flag must stay true to support sustained high-actor load; if it is false, the run is **not** a sustained performance PASS.

Automated QA source build [41734887819](https://github.com/hotmoral/DeepHold/actions/runs/41734887819) PASS; private packaging [41737049153](https://github.com/hotmoral/DeepHold/actions/runs/41737049153) PASS. Actual physical Android FPS/input/thermal gate remains PENDING until evidence from device is received.
