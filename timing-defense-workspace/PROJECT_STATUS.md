# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- current candidate HEAD: `cee455520fbee04002d2fb12f33dc24ffe129264`

Last fully closed checkpoint:
- **v0.38 Slice C / larger-party event kernel FULL PASS**
- branch `timing-defense-cloudflare-v038-slice-c-pass-20261022`
- HEAD `cbcddf35443ff901b4a30dd6621da5a984335fb5`

Active candidate:
- **v0.39 N3 Option B authority**
- branch `timing-defense-cloudflare-v039-n3-authority`
- candidate/watch HEAD `cee455520fbee04002d2fb12f33dc24ffe129264`
- expected health `0.39-cf.1`
- automated validation pending

Preserved checkpoints:
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

Read first:
- `NEXT_WORK.md`
- `CLOUDFLARE_V038_SLICE_C_PASS_2026-10-22.md`
- `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`
- `CLOUDFLARE_V037_SLICE_B_PASS_2026-10-21.md`

---

# Closed Cloudflare gates
- v0.31/v0.32 waiting-room parity — PASS
- v0.33 Stage 1 authority — PASS
- v0.34 render/remote projectile parity — PASS
- v0.35 reconnect / Team Shop / Stage 2 — PASS
- v0.36 N1/N2 + Lv6 authority — FULL PASS
- v0.37 Stage 3 + BRUTE — FULL PASS
- v0.38 larger-party/event-delivery kernel — FULL PASS

## v0.36 frozen parity
N1 exact EXP:
- NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

N2:
`AI damage × (1 + (stage - 1) * 0.035)`.

Lv6 authority:
- Knight +12% damage
- Rogue 55% second dagger after +55 ms
- Tank +30% knockback
- Archer up to two strict-line 52% secondary hits
- Mage up to three nearby 50% splash hits

## v0.37 Stage 3 frozen contract
- 12 enemies / 980 ms
- GRUNT 44% / RUNNER 34% / BRUTE 22%
- BRUTE base HP 900 / speed .040 / wall 180 / knock resist .38 / armor 1 / reward 14
- ordinary Stage 3 BRUTE HP 1247 under existing HP rules
- Stage 3 clear -> Team Shop
- Stage 4 blocked

## v0.38 Slice C closure
Validated event kernel:
- 512 retained authoritative events
- per-WebSocket `eventRunId` + `eventCursor`
- monotonic `event-batch`
- state snapshots no longer depend on `events.slice(-24)`
- explicit `event-gap` on impossible continuity
- resume/eventFloor historical replay suppression preserved

Automation:
- SERVER 28/28 PASS
- v0.36 client regression PASS
- v0.37 client regression PASS
- event client PASS
- larger-party simulation PASS
- FINAL PASS

Party coverage:
- 3H
- 4H
- 2H+2AI
- 3H+1AI
- host reconnect
- READY/START
- Stage 1 -> Shop -> Stage 2
- >24 event delivery without silent loss

Samsung Browser 4H single-device smoke was user-confirmed PASS with one real host plus three simulated human peers. Exact full-PASS HEAD: `cbcddf35443ff901b4a30dd6621da5a984335fb5`.

---

# N3 — OPTION B APPROVED / FROZEN / NOW IN v0.39 CANDIDATE
Frozen product contract:
- trigger at combo 5 / 10 / 20 / 30 / every +10 after 30
- exact raw-equivalent max budgets 60 / 90 / 150 / 210
- Rogue 2/3/4/5 daggers
- Knight 67/33 primary-secondary intent
- Tank 60/20/20 intent
- Archer 70/30 strict-line intent
- Mage 55/15/15/15 intent
- deterministic remainder-safe allocation
- no EXP / charge / combo / ordinary crit / recursive class skill / recursive N3
- normal armor, kill, kill coin and contribution attribution
- frozen boss scalars apply, including Rogue 0.70
- generic N3 knockback uses NORMAL-equivalent base
- Tank retains independently-authoritative knockback identity

Canonical contract:
`N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`

v0.39 candidate implementation:
- server-authoritative N3 events use `type: n3`
- delayed Rogue milestone daggers use a dedicated `n3Queue`, separate from Lv6 skill queue
- N3 queues are cleared when combat ends
- legacy local N3 damage/projectile mutation is suppressed in network mode
- client renders server-confirmed N3 events only
- candidate host-only debug arming endpoint supports automated combo stress
- Stage 4 remains blocked

Validation gate:
- prior v0.38 full regression
- deterministic all-class milestones 5/10/20/30/40
- exact budgets / geometry / proc isolation
- kill/coin/contribution
- Rogue boss scalar
- Tank Lv6 knockback identity
- Lv6 Rogue coexistence
- synchronized 4H 30-combo stress: 4 primary hits + 4 Lv6 second daggers + 20 N3 daggers = 28 combat events per observing client
- one final Samsung Browser N3 presentation smoke

---

# Following bounded work
1. Close v0.39 N3 authority.
2. Stage 4 SHIELD / armor.
3. Stage 5–6 boss + FLYER + authoritative Y geometry.
4. Stage 7–9 mixed-roster stress.
5. Stage 10 final boss/result.
6. Lv11/16/21 authority with forced-level deterministic tests.

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred as a shared responsive-safety layer.

## Governance
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
