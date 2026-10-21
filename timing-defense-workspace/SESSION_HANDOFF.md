# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Current architecture
Primary lane:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- current candidate HEAD `cee455520fbee04002d2fb12f33dc24ffe129264`

Last fully closed checkpoint:
- **v0.38 Slice C / larger-party event kernel FULL PASS**
- branch `timing-defense-cloudflare-v038-slice-c-pass-20261022`
- HEAD `cbcddf35443ff901b4a30dd6621da5a984335fb5`

Active candidate:
- **v0.39 N3 Option B authority**
- branch `timing-defense-cloudflare-v039-n3-authority`
- expected health `0.39-cf.1`
- one-click automated validation pending

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

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CLOUDFLARE_V038_SLICE_C_PASS_2026-10-22.md`
5. `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`
6. `CLOUDFLARE_V037_SLICE_B_PASS_2026-10-21.md`

## Closed v0.36 decisions
N1 exact EXP:
- NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

N2 exact AI stage multiplier:
`1 + (stage - 1) * 0.035`.

Lv6 authority:
- Knight +12% damage
- Rogue 55% second dagger after +55 ms
- Tank +30% knockback
- Archer up to two strict-line 52% secondary hits
- Mage up to three nearby 50% splash hits

## Closed v0.37 Stage 3
- 12 enemies / 980 ms
- GRUNT 44% / RUNNER 34% / BRUTE 22%
- BRUTE base HP 900 / speed .040 / wall 180 / knock resist .38 / armor 1.00 / reward 14
- ordinary Stage 3 BRUTE HP 1247
- Stage 1 -> Shop -> Stage 2 -> Shop -> Stage 3 -> Shop
- Stage 4 locked

## Closed v0.38 Slice C
Event kernel:
- 512 retained authoritative events
- per-WebSocket `eventRunId` + `eventCursor`
- monotonic `event-batch`
- state snapshots do not carry the old fixed event tail
- explicit `event-gap`
- resume/eventFloor historical replay suppression retained

Automation PASS:
- SERVER 28/28
- v0.36 client regression
- v0.37 client regression
- event client
- larger-party simulation
- FINAL PASS

Coverage:
- 3H
- 4H
- 2H+2AI
- 3H+1AI
- host reconnect
- READY/START
- Team Shop/NEXT
- Stage 2 entry
- >24 event delivery
- no silent event loss

Final Samsung Browser 4H smoke:
- one real local host/player
- three simulated human WebSocket peers
- user reported no issues
- READY/START, remote attacks, Team Shop and NEXT -> Stage 2 all accepted

Exact full-PASS HEAD:
`cbcddf35443ff901b4a30dd6621da5a984335fb5`

## N3 — OPTION B FROZEN / v0.39 CANDIDATE ENABLED
Frozen contract:
- combo milestones 5 / 10 / 20 / 30 / every +10 after 30
- max raw-equivalent budgets 60 / 90 / 150 / 210
- Rogue 2/3/4/5 daggers
- Knight 67/33 intent
- Tank 60/20/20 intent
- Archer 70/30 strict-line intent
- Mage 55/15/15/15 intent
- exact budget allocator prevents rounding overshoot
- no EXP / charge / combo increment / ordinary proc crit / recursive class skill / recursive N3
- normal armor / kill / kill coin / contribution
- Rogue boss scalar 0.70
- generic N3 knockback uses NORMAL-equivalent base
- Tank retains Lv6/class knockback identity

v0.39 implementation:
- authoritative `type:n3` events
- dedicated delayed Rogue `n3Queue`
- N3 queue separate from Lv6 skill queue
- combat-end queue cleanup
- local legacy N3 mutator suppressed when multiplayer is active
- client renders server-confirmed N3 only
- candidate host debug arm endpoint for automated stress
- Stage 4 still blocked

## Active validation gate
One-click:
`/v039-validation-suite.html`

Must pass:
- complete v0.38 regression
- all-class N3 milestones 5/10/20/30/40
- exact budgets/geometry
- proc isolation
- unused secondary budget not redirected
- kill/coin/kill-coin/contribution
- Rogue boss scalar
- Tank Lv6 N3 knockback
- Lv6 Rogue + N3 coexistence
- heavy X/Y combo semantics
- four-human synchronized 30-combo stress

4H stress expected per observer:
- 4 ordinary hit events
- 4 Lv6 Rogue skill events
- 20 N3 events
- total 28 combat events
- no event-gap
- contiguous post-floor IDs
- all four combos -> 30

After automation PASS:
- one short Samsung Browser N3 presentation smoke only
- preserve v0.39 PASS checkpoint
- then Stage 4 SHIELD / armor

## AI FILL semantic
Configured AI filler positions remain fixed occupied positions. Humans do not dynamically displace them.

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred as one shared responsive layer.

## Governance
No numerical change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
