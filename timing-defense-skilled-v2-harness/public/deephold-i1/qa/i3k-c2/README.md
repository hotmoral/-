# DeepHold I3K-C2 — Player locator & reduced Ferrix labels

**New isolated physical Android QA page. Source is unmerged, draft PR #59 based on C1 draft PR #58.**

Visuals only:
- Original C1 monster-source bodies, team-tinted ally markings and compact Ferrix original anatomy retained.
- Player gets bright gold diamond ground locator, stable YOU badge, depth 12 above Ferrix Special bodies at depth 10.
- Only one named Ferrix squad leader (lowest living formation slot); when it disappears, next surviving actor takes the label/HP. The other 4 preserve Ferrix source bodies and gold/purple ground rings but suppress redundant label/HP unless hit, when HP appears for ~1.8 seconds.
- Neither game physics, attack/range, identity/Archive, movement, B1 rejoin, B2 combat assist, five manual skills nor left/right HUD changes.

Source build SHA: 7cea4121fae475b62722d8a5749863393fab86c2. Strict default/QA build and browser regressions PASS: https://github.com/hotmoral/DeepHold/actions/runs/41800983750 . Headless browser pacing is not physical Android evidence.

Android Chrome/Samsung Browser landscape:

https://timing-defense-skilled-v2-harness.sktjsek.workers.dev/deephold-i1/qa/i3k-c2/?crowd-qa=1&case=p5-soak&seconds=120

Tap 측정 시작; move joystick/use skills and check whether gold YOU marker remains visible and only one Ferrix S3 label remains. For 120-second P5 SOAK share JSON and optionally short screen recording. Earlier C1 real Chrome: 105+30 held, rAF 61.5 FPS mean, p95 16.7ms/p99 16.8ms, max 33.3ms, zero 1s hitches. Do not attribute differences to C2 without repeated runs. SOAK suppresses Soulbound damage and clamps QA hostile HP; hit-only HP not evaluated in SOAK.

Seven added static files ONLY in deephold-i1/qa/i3k-c2; existing routes and Worker untouched. Assistant cannot independently verify live Worker HTTP here.
