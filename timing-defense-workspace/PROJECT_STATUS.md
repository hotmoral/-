# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- current candidate watched HEAD: `0c96f038f6fcf7ec5e27e7d7fe0db38343a807c7`

Last fully closed checkpoint:
- **v0.37 Slice B / Stage 3 FULL PASS**
- branch `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`

Active candidate:
- **v0.38 Slice C / larger-party event kernel**
- branch `timing-defense-cloudflare-v038-slice-c-event-kernel`
- candidate HEAD `0c96f038f6fcf7ec5e27e7d7fe0db38343a807c7`
- expected health `0.38-cf.1`
- live validation pending

Preserved checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automated PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`
- v0.36 Slice A full PASS: `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- v0.37 Slice B full PASS: `timing-defense-cloudflare-v037-slice-b-pass-20261021`

Read first:
- `NEXT_WORK.md`
- `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`
- `CLOUDFLARE_V038_SLICE_C_CANDIDATE_2026-10-21.md`
- `CLOUDFLARE_V037_SLICE_B_PASS_2026-10-21.md`

---

# Closed Cloudflare gates
- v0.31/v0.32 waiting-room parity — PASS
- v0.33 Stage 1 authority — PASS
- v0.34 render/remote-projectile parity — PASS
- v0.35 reconnect / Team Shop / Stage 2 — PASS
- v0.36 N1/N2 + Lv6 authority — FULL PASS
- v0.37 Stage 3 + BRUTE — FULL PASS

## v0.36 frozen parity decisions
N1 exact EXP:
- NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

N2:
`AI damage × (1 + (stage - 1) * 0.035)`.

Lv6 authority:
- Knight +12% damage,
- Rogue 55% second dagger after +55 ms,
- Tank +30% knockback,
- Archer up to two strict-line 52% secondary hits,
- Mage up to three nearby 50% splash hits.

## v0.37 Stage 3 closed contract
- 12 enemies / 980 ms,
- GRUNT 44% / RUNNER 34% / BRUTE 22%,
- BRUTE base HP 900 / speed .040 / wall 180 / knock resist .38 / armor 1 / reward 14,
- ordinary Stage 3 BRUTE HP 1247 under existing HP rules,
- Stage 3 clear -> Team Shop,
- Stage 4 blocked.

---

# N3 — OPTION B APPROVED / FROZEN / NOT YET ENABLED
N3 is no longer an unresolved discussion item.

Frozen product contract:
- milestone triggers 5 / 10 / 20 / 30 / every +10 after 30,
- exact maximum budgets 60 / 90 / 150 / 210,
- same recovered class-specific burst geometry,
- deterministic remainder-safe allocation prevents over-budget rounding,
- no EXP / charge / combo / ordinary proc crit / recursive skill / recursive N3,
- normal armor, kill, kill coin and contribution attribution,
- existing boss scalars apply,
- generic N3 knockback uses NORMAL-equivalent base; milestone tier does not automatically escalate generic knockback,
- class identity multipliers remain authoritative.

Canonical contract:
`N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`

N3 implementation is intentionally gated on Slice C event-delivery PASS.

---

# Active Slice C candidate — v0.38
Purpose:
- larger-party baseline,
- remove dependency on the legacy 24-event snapshot tail before N3 is enabled.

Event kernel candidate:
- 512-event authoritative history,
- per-WebSocket `eventRunId` + `eventCursor` hibernation attachment,
- monotonic `event-batch` delivery,
- socket state snapshots contain zero event payload,
- explicit `event-gap` if retention continuity is impossible,
- reconnect floors at latest while preserving existing resume/eventFloor historical-replay suppression.

Live automation scenarios:
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI.

Checks include slots, host identity, READY/START, Stage1->Shop->Stage2, reconnect, contiguous event IDs, no gap, and >24 delivered events in 4H.

Validation gate:
- `/v038-validation-suite.html`
- v0.38 is **not PASS yet**.

Do not enable N3 or Stage 4 until Slice C closes.

---

# Following bounded work
1. Close Slice C automation + one final Samsung Browser smoke.
2. Implement N3 Option B as a dedicated authority slice with forced 5/10/20/30/40 tests for all five classes and four-player milestone stress.
3. Stage 4 SHIELD / armor.
4. Stage 5–6 boss + FLYER + authoritative Y geometry.
5. Stage 7–9 mixed stress.
6. Stage 10 final boss/result.
7. Lv11/16/21 authority with forced-level deterministic tests.

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred as a shared responsive-safety layer.

## Governance
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
