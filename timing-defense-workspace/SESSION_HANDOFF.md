# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Current architecture
Primary lane:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- current smoke-candidate HEAD `cbcddf35443ff901b4a30dd6621da5a984335fb5`

Last fully closed checkpoint:
- v0.37 Slice B / Stage 3 + BRUTE — **FULL PASS**
- branch `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`

Active candidate:
- v0.38 Slice C / larger-party event kernel
- automation validated on HEAD `1afb125c86fc5c085c6b1246dec77b36a1d30159`
- automation PASS checkpoint `timing-defense-cloudflare-v038-automation-pass-20261022`
- final Samsung Browser 4H presentation smoke pending

## Preserved checkpoints
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automated PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`
- v0.36 Slice A full PASS: `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- v0.37 Slice B full PASS: `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- v0.38 Slice C automation PASS: `timing-defense-cloudflare-v038-automation-pass-20261022`

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CLOUDFLARE_V038_SLICE_C_AUTOMATION_PASS_2026-10-22.md`
5. `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`
6. `CLOUDFLARE_V038_SLICE_C_CANDIDATE_2026-10-21.md`
7. `CLOUDFLARE_V037_SLICE_B_PASS_2026-10-21.md`

## Closed v0.36 decisions
N1 exact EXP:
- NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

N2 exact AI stage multiplier:
`1 + (stage - 1) * 0.035`.

Lv6 authority:
- Knight +12% damage,
- Rogue 55% second dagger after +55 ms,
- Tank +30% knockback,
- Archer up to two strict-line 52% secondary hits,
- Mage up to three nearby 50% splash hits.

## Closed v0.37 Stage 3
Exact encounter:
- 12 enemies / 980 ms,
- GRUNT 44% / RUNNER 34% / BRUTE 22%.

BRUTE:
- HP 900 base,
- speed .040,
- wall damage 180,
- knock resist .38,
- armor 1.00,
- reward 14,
- Stage 3 ordinary HP 1247 under existing HP rules.

Flow:
- Stage 1 -> Shop,
- Stage 2 -> Shop,
- host NEXT -> Stage 3,
- Stage 3 -> Shop,
- Stage 4 locked.

Automated and Samsung Browser smoke evidence both PASS.

## N3 — OPTION B APPROVED / FROZEN / NOT YET ENABLED
Frozen contract:
- milestone triggers at 5 / 10 / 20 / 30 / every +10 after 30,
- exact max budgets 60 / 90 / 150 / 210,
- Rogue 2/3/4/5 daggers,
- Knight 67/33 primary-secondary intent,
- Tank 60/20/20 intent,
- Archer 70/30 strict-line intent,
- Mage 55/15/15/15 intent,
- deterministic remainder-safe allocation prevents over-budget rounding,
- no EXP / charge / combo / ordinary proc crit / recursive class skill / recursive N3,
- normal armor / kill / kill coin / contribution attribution,
- frozen boss scalars remain,
- generic N3 knockback uses NORMAL-equivalent base; milestone tier itself does not escalate generic knockback,
- class multipliers still apply; Tank retains class knockback identity.

Canonical:
`N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`

Implementation remains blocked until Slice C full PASS.

## v0.38 Slice C automation PASS
Event kernel:
- 512 retained authoritative events,
- per-WebSocket `eventRunId` + `eventCursor` hibernation attachment,
- monotonic `event-batch` delivery,
- state broadcasts carry no legacy event tail,
- explicit `event-gap` on impossible continuity,
- existing resume/eventFloor historical replay suppression retained.

Validated suite version:
`0.38-cf.3-validation-suite`

Exact automation evidence:
- SERVER 28/28 PASS,
- V036 CLIENT REGRESSION PASS,
- V037 CLIENT REGRESSION PASS,
- EVENT CLIENT PASS,
- LARGER PARTY PASS,
- FINAL PASS.

Exact validated deployment HEAD:
`1afb125c86fc5c085c6b1246dec77b36a1d30159`

Coverage:
- 3H,
- 4H,
- 2H+2AI,
- 3H+1AI,
- fixed slot occupancy,
- host identity / reconnect,
- READY / START,
- synchronized Stage 1,
- Team Shop,
- Stage 2 entry,
- contiguous event IDs,
- no unexpected event-gap,
- >24 event delivery without silent loss.

Earlier two visible `push` failures were validation-harness failures, not validated gameplay failures. Final root cause was a validation-page JS typo where `checks` was not initialized on `result` before `result.checks.push(...)`. cf.3 fixed that and hardened diagnostics.

## Immediate next boundary — final Slice C device smoke
Current watched smoke-candidate HEAD:
`cbcddf35443ff901b4a30dd6621da5a984335fb5`

Candidate-only single-device 4H harness:
- query `partybot=3`,
- local phone is the real host/player,
- `SIM-A` ARCHER,
- `SIM-M` MAGE,
- `SIM-T` TANK,
- all are distinct HUMAN WebSocket sessions,
- simulated peers auto READY in lobby and Team Shop,
- simulated peers send ordinary timing action packets during combat,
- smoke overlay appears only during combat.

Manual acceptance is presentation/input only:
- 4 humans render correctly in waiting room,
- local READY/START accessible,
- remote human attacks display without obvious flicker/burst/canvas corruption,
- local timing input works,
- Team Shop shows four humans without controls being obscured,
- simulated peers READY,
- host NEXT reaches Stage 2.

Do not re-check exact combat numbers manually; automation already covers correctness.

## After Slice C full PASS
Dedicated N3 authority slice:
- forced combo 5/10/20/30/40 on all five classes,
- exact budget and geometry tests,
- proc isolation,
- kill/coin/contribution and boss scalar assertions,
- synchronized four-player milestone stress,
- one Samsung Browser presentation smoke.

Then Stage 4 SHIELD / armor.

## AI FILL semantic
Current filler positions remain fixed occupied positions.
Humans do not dynamically displace configured AI filler.

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred as one shared responsive layer.

## Governance
No numerical change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
