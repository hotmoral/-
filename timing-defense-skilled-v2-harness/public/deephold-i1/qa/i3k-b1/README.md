# DeepHold I3K-B1 Mobile Preview — Soulbound Follow and Formation

Run on physical Samsung Internet or Android Chrome in landscape:
https://timing-defense-skilled-v2-harness.sktjsek.workers.dev/deephold-i1/qa/i3k-b1/?crowd-qa=1

Scope:
- User-approved fixes: Common/Special follow moving player before continuing combat, complete returning to assigned slot after movement, disjoint Common 100 and Ferrix S3 5 formation points with stable indices across separate summons and losses.
- **UNCHANGED**: ordinary monster chase -> stop -> autoattack; original Common/Special approach -> stop -> attack, source damage/attack cadence, source movement speed; player controls/five skill buttons; archive/MP/Gem/recovery, original hosted DeepHold snapshot.
- Opt-in QA mode: compiled with `VITE_DEEPHOLD_CROWD_QA=1`, activated with `?crowd-qa=1`. Select c20s1/c50s3/p4/p5 and move the player with joystick while Soulbound fight; observe whether units disengage, follow, and resume when settled.
- Existing QA monster = real materialized Gnawer with 5000HP and respawn; player death suppressed; no temperature measurement API; P5 adds synthetic effects, **not full projectiles**.
- Existing QA actor attrition remains normal. Distinguish movement/formation visual acceptance from 105-active-actor sustained performance proof.

Evidence:
- Original behavior tests and strict build `41744524663` PASS
- Combined mobile browser P1/P4/P5 and artifact packaging `41744851621` PASS
- **No actual Android phone UI/controls/60FPS certification for the modified B1 preview**.
- Only static built public files; private source stays in `hotmoral/DeepHold`. Cloudflare Worker/API/other apps untouched.
