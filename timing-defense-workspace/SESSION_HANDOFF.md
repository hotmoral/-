# Timing Defense — Session Handoff

Updated: 2026-10-21 KST

## Current architecture
Primary lane:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- current candidate HEAD `0c96f038f6fcf7ec5e27e7d7fe0db38343a807c7`

Last fully closed checkpoint:
- v0.37 Slice B / Stage 3 + BRUTE — **FULL PASS**
- branch `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`

Active candidate:
- v0.38 Slice C / larger-party event kernel
- branch `timing-defense-cloudflare-v038-slice-c-event-kernel`
- expected health `0.38-cf.1`
- live automated validation pending

## Preserved checkpoints
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automated PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`
- v0.36 Slice A full PASS: `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- v0.37 Slice B full PASS: `timing-defense-cloudflare-v037-slice-b-pass-20261021`

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`
5. `CLOUDFLARE_V038_SLICE_C_CANDIDATE_2026-10-21.md`
6. `CLOUDFLARE_V037_SLICE_B_PASS_2026-10-21.md`
7. `CLOUDFLARE_V036_SLICE_A_PASS_2026-10-21.md`

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
N3 is no longer deferred.

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

Implementation is intentionally blocked until Slice C event delivery is PASS.

## Active v0.38 Slice C candidate
Purpose:
- validate 3–4 participant multiplayer baseline,
- remove the old 24-event snapshot-tail dependency before N3.

Event kernel:
- 512 retained authoritative events,
- per-WebSocket `eventRunId` + `eventCursor` stored in hibernation attachment,
- monotonic `event-batch` delivery,
- socket `state` broadcasts carry no event tail,
- explicit `event-gap` on impossible continuity,
- existing v0.35 resume/eventFloor historical replay suppression retained,
- reconnect socket in active run floors at latest,
- pre-run socket begins a new run at event 0.

Live simulation scenarios:
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI.

Checks:
- fixed slot occupancy,
- host identity,
- READY/START,
- synchronized run roster,
- Stage 1 -> Team Shop -> Stage 2,
- host reconnect in 4H,
- contiguous event IDs,
- no event-gap,
- >24 delivered events in 4H.

One-click gate:
`/v038-validation-suite.html`

v0.38 is **not PASS yet**.
Do not enable N3 or Stage 4 until this gate and one final device smoke pass.

## AI FILL semantic
Current filler positions are fixed occupied positions.
Humans do not dynamically displace configured AI filler.
Do not silently change this semantic inside Slice C.

## Next after Slice C PASS
Dedicated N3 authority slice:
- forced combo 5/10/20/30/40 on all five classes,
- exact budget and geometry tests,
- proc-isolation assertions,
- kill/coin/contribution and boss-scalar assertions,
- synchronized four-player milestone stress,
- one final Samsung Browser presentation smoke.

Then Stage 4 SHIELD / armor.

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains deferred as one shared responsive layer.

## Governance
No numerical change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
