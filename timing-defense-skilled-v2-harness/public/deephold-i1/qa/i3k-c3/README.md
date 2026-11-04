# DeepHold — I3K-C3 Mobile Landscape Combat HUD

Isolated Android visual QA for user review; C3 source PR #60 is DRAFT and STACKED on unmerged C1 #58 and C2 #59. No original production game adoption.

New: For small LANDSCAPE phone displays (width at most 950 CSS px, height at most 520 CSS px), left Deep Core logistics collapses to one-line header + GEM; right Guide AI collapses to heading. Tap + beside either title to read all existing details; tap − to fold. Existing health/mana/level/carry, minimap, joystick, 5 skill buttons, Archive and skill acquire/upgrade actions are preserved. Wide landscape is unaffected. Player gold YOU locator and one Ferrix squad leader label from C2 preserved.

QA source build: `2c38d5b311e1668f7738000a7874d6e1646a7c03`.
- C3 source strict TS/Vite + responsive 823x384 compact/expand and 1280x800 desktop + C2/B1/B2: https://github.com/hotmoral/DeepHold/actions/runs/41816745114 SUCCESS.
- QA source strict default/QA builds + C3/C2/B1/B2 and P1/P4/P5/P4-SOAK/P5-SOAK Chromium: https://github.com/hotmoral/DeepHold/actions/runs/41816849994 SUCCESS.

Android landscape P5 SOAK:

https://timing-defense-skilled-v2-harness.sktjsek.workers.dev/deephold-i1/qa/i3k-c3/?crowd-qa=1&case=p5-soak&seconds=120

At 823x384 phone size, test folding/unfolding Core logistics and Guide AI, joystick and 5 skills before running the 120s soak; send JSON plus screen recording. QA protects summoned HP and clamps QA hostile HP to 1; this is NOT ordinary monster death/recovery economy. Headless Chromium is not real Android frame pacing.

Exactly seven NEW static assets in /deephold-i1/qa/i3k-c3/ only; original Cloudflare game and C1/C2/A2/B1/B2/SOAK previews remain untouched; no Worker changes.
