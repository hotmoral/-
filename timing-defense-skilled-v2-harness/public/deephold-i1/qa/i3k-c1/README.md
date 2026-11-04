# DeepHold I3K-C1 — original monster silhouette for revived Soulbound

**This is the visual QA preview ONLY.** The candidate source implementation is in private draft PR [#58](https://github.com/hotmoral/DeepHold/pull/58), NOT merged to main.

- Visuals: Common revived use source monster bodies of Gnawer (burrow, pack, brute), Ironback (spider, web-stalker, armorling), Chain Lantern (watcher, fanatic, gem-harvester) with a cool ally palette, original silhouette at 90% visual scale, teal underfoot ring. Default Common labels and health bars hidden; shown about 1.8s on taking damage.
- Five Ferrix S3 revived retain the **original Ferrix boss anatomy** at compact scale, a gold/purple hex-ring badge and short names, not the previous giant round placeholder.
- No new PNG artwork exists: this implementation reuses **source Phaser shape constructors** on both monster and Soulbound paths.
- No changes to attack source cadence, damage, AI, physics/hit radius, movement, B1 rejoin, B2 target sharing, Soul ownership, skills, rewards or original enemy draw output.
- QA build commit: `b827a678efa07d5281b67dc9258dccdd59cdf3b8`; validated run [41789721180](https://github.com/hotmoral/DeepHold/actions/runs/41789721180) passes strict normal/QA TS/Vite builds, B1/B2 regressions and A2 P1/P4/P5/SOAK Chromium smoke. 105 actor renderer source run [41789247167](https://github.com/hotmoral/DeepHold/actions/runs/41789247167) SUCCESS.
- `p5-soak` intentionally suppresses Soulbound deaths and clamps QA monster HP to 1 while preserving actual combat targeting/attack/VFX so 100+5+30 remain present; **this is not production game balance**. Extra pulse VFX synthetic; actual projectile stress unverified.
- Physical Android FPS and visual acceptance **PENDING**; headless CI FPS is not phone performance.

**Run in Android Chrome landscape:**

https://timing-defense-skilled-v2-harness.sktjsek.workers.dev/deephold-i1/qa/i3k-c1/?crowd-qa=1&case=p5-soak&seconds=120

Tap **측정 시작**. Move joystick, use skills and inspect source-silhouette distinction/size/markers, then share JSON plus a short screen recording if possible. Compare the previously provided Chrome 149 old-visual P5 SOAK baseline: 63.5 average rAF FPS, p95 16.8ms, p99 25ms, max 50ms, 105+30 held 120s, subjective heat normal. Check the new build independently. Do not merge draft PR #58 pending user's visual approval.

Publication does not modify any other route, original game, old A2/B1/B2/soak QA or Cloudflare Worker.
