# DeepHold I3K-B2 squad-aware Soulbound Android QA

Open https://timing-defense-skilled-v2-harness.sktjsek.workers.dev/deephold-i1/qa/i3k-b2/?crowd-qa=1 in Android Chrome/Samsung Internet, landscape.

- **New compared to B1**: Common/Special prioritize the hostile that *actually hit the player* (up to 1800ms), then a hostile recently hit by the player (up to 1500ms). If neither applies, fight own nearby target, then respond to another Soulbound's active engagement if otherwise idle. All assistance stays within player-tether bounds.
- **B1 remains**: follow moving player first; continue returning to assigned formation positions even after player stops; unique fixed 100 Common/5 Special formation anchors.
- **Original rule preserved**: monster AND Soulbound approach, stop, attack; never attack mid-step. Source attack damage/cooldown/move speed, five skills, Archive/MP/Gem/recovery and player input unchanged.
- Compare visual behavior under C20S1, C50S3, P4 and P5. Move player while enemies fight, stop, then observe who the Soulbound target and whether previously idle allies join.
- This is a separate isolated built QA preview. Existing main game and previous A2/B1 previews remain unchanged.
- Browser tests: B1+B2 source tests and P1/P4/P5 QA `41748982170` PASS. Real device behavior has **NOT** been verified by the assistant; no production source merge. 105 active Soulbound may die during 120-second P5 combat, so `loadMaintained=false` is not a sustained capacity PASS.
- JSON still uses schema `deephold-i3k-a2-physical-v1`; identify this run by the **B2 URL**, not by `testBuild` alone.
