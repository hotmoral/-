# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Current architecture
Primary lane:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- current N3 device-smoke candidate HEAD `f9e824eac87cc2fe39d80a75b345ce5aa8f574ce`

Last fully closed checkpoint:
- **v0.38 Slice C / larger-party event kernel FULL PASS**
- branch `timing-defense-cloudflare-v038-slice-c-pass-20261022`
- HEAD `cbcddf35443ff901b4a30dd6621da5a984335fb5`

Active candidate:
- **v0.39 N3 Option B authority**
- implementation branch `timing-defense-cloudflare-v039-n3-authority`
- health `0.39-cf.1`
- automated-live validation PASS
- automation checkpoint `timing-defense-cloudflare-v039-automation-pass-20261022`
- automation-validated watched HEAD `201ac36ac8ec97a3e033976cdea13c3fd2fe03c6`
- final Samsung Browser presentation/input smoke remains

## Preserved checkpoints
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automation PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`
- v0.36 Slice A full PASS: `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- v0.37 Slice B full PASS: `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- v0.38 automation PASS: `timing-defense-cloudflare-v038-automation-pass-20261022`
- v0.38 Slice C full PASS: `timing-defense-cloudflare-v038-slice-c-pass-20261022`
- v0.39 N3 automation PASS: `timing-defense-cloudflare-v039-automation-pass-20261022`

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CLOUDFLARE_V039_N3_AUTOMATION_PASS_2026-10-22.md`
5. `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`
6. `CLOUDFLARE_V038_SLICE_C_PASS_2026-10-22.md`

## Closed v0.36 decisions
N1 exact EXP:
- NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28

N2 exact AI stage multiplier:
`1 + (stage - 1) * 0.035`

Lv6 authority:
- Knight +12% damage
- Rogue 55% second dagger after +55 ms
- Tank +30% knockback
- Archer up to two strict-line 52% secondary hits
- Mage up to three nearby 50% splash hits

## Closed v0.37 Stage 3
- 12 enemies / 980 ms
- GRUNT 44% / RUNNER 34% / BRUTE 22%
- BRUTE base HP 900 / speed .040 / wall 180 / knock resist .38 / armor 1 / reward 14
- ordinary Stage 3 BRUTE HP 1247
- Stage 3 clear -> Team Shop
- Stage 4 locked

## Closed v0.38 Slice C
Event kernel:
- 512 retained authoritative events
- per-WebSocket `eventRunId` + `eventCursor`
- monotonic `event-batch`
- state snapshots no longer carry a fixed event tail
- explicit `event-gap`
- resume/eventFloor replay suppression preserved

Automation:
- SERVER 28/28 PASS
- v0.36 client regression PASS
- v0.37 client regression PASS
- event client PASS
- larger-party PASS
- FINAL PASS

Party coverage:
- 3H / 4H / 2H+2AI / 3H+1AI
- host reconnect
- READY/START
- Team Shop/NEXT
- >24 events delivered without silent loss

Final Samsung Browser 4H smoke was user-confirmed PASS.

## N3 — OPTION B FROZEN / v0.39 AUTOMATION PASS
Contract:
- combo milestones 5 / 10 / 20 / 30 / every +10 after 30
- max budgets 60 / 90 / 150 / 210
- Rogue 2/3/4/5 daggers
- Knight 67/33
- Tank 60/20/20
- Archer 70/30 strict line
- Mage 55/15/15/15
- remainder-safe exact allocation
- no EXP / charge / combo / ordinary crit / recursive skill / recursive N3
- normal armor / kill / kill coin / contribution
- frozen boss scalars
- generic knockback NORMAL-equivalent
- Tank retains class/Lv6 knockback identity

Implementation:
- authoritative `type:n3` events
- delayed Rogue N3 uses dedicated `n3Queue`, separate from Lv6 skill queue
- delayed queue cleared when combat ends
- legacy local v0.18 N3 mutator suppressed in multiplayer
- client renders only server-confirmed N3 events
- candidate host debug-arm endpoint supports forced-combo tests
- Stage 4 remains blocked

Automated live validation is no longer user-driven.
Workflow:
`.github/workflows/timing-defense-v039-live-validation.yml`

Corrected GitHub Actions run:
- run `39686204069`
- job `119520775498`
- Cloudflare health 0.39-cf.1 PASS
- Chromium validation PASS
- artifact evidence uploaded

Live result:
- V038 FULL REGRESSION PASS
- N3 SERVER 57/57 PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- FINAL PASS

Four-human worst-case stress:
- four Lv6 Rogues, combo29 -> simultaneous PERFECT
- 4 ordinary hits + 4 Lv6 second daggers + 20 N3 daggers
- 28 combat events per observer
- no event-gap
- contiguous post-floor IDs
- all combos -> 30

The first Actions run timeout was caused by an incorrect Playwright `waitForFunction` argument position and did not represent a gameplay/N3 failure. The runner was fixed and the corrected run passed.

## Immediate next boundary — one Samsung Browser N3 presentation/input smoke
Candidate helper:
- `?n3smoke=1`
- when host combat has a monster, automatically arms humans to Lv6/combo29
- badge: `N3 ARMED · PERFECT 1회`
- normal access unaffected

Use `peerbot=1` so no PC is required.
Select Rogue, start the run, wait for N3 ARMED, then land one PERFECT.

Accept only presentation/input:
- local host remains Rogue
- simulated peer remains separate human
- timing input works
- N3 Rogue multi-dagger burst is visually coherent
- no obvious duplicate-projectile storm, flicker, Canvas corruption or blocked controls
- gameplay continues afterward

Do not manually recheck numerical/N3 delivery contracts; GitHub Actions owns those gates.

After smoke PASS:
- preserve v0.39 full-PASS branch at exact watched smoke HEAD
- write full PASS report
- move to Stage 4 SHIELD / armor

## Validation policy
Default:
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`.

## AI FILL semantic
Configured AI filler positions remain fixed occupied positions. Humans do not dynamically displace them.

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred as one shared responsive layer.

## Governance
No numerical change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
