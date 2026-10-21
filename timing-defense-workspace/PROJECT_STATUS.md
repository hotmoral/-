# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- current smoke-candidate HEAD: `cbcddf35443ff901b4a30dd6621da5a984335fb5`

Last fully closed checkpoint:
- **v0.37 Slice B / Stage 3 FULL PASS**
- branch `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`

Active candidate:
- **v0.38 Slice C / larger-party event kernel**
- implementation branch `timing-defense-cloudflare-v038-slice-c-event-kernel`
- automation-validated deployment HEAD `1afb125c86fc5c085c6b1246dec77b36a1d30159`
- automation PASS checkpoint `timing-defense-cloudflare-v038-automation-pass-20261022`
- final Samsung Browser 4H presentation smoke pending

Preserved checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automated PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`
- v0.36 Slice A full PASS: `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- v0.37 Slice B full PASS: `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- v0.38 Slice C automation PASS: `timing-defense-cloudflare-v038-automation-pass-20261022`

Read first:
- `NEXT_WORK.md`
- `CLOUDFLARE_V038_SLICE_C_AUTOMATION_PASS_2026-10-22.md`
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
Frozen product contract:
- milestone triggers 5 / 10 / 20 / 30 / every +10 after 30,
- exact maximum budgets 60 / 90 / 150 / 210,
- recovered class-specific burst geometry retained,
- deterministic remainder-safe allocation prevents over-budget rounding,
- no EXP / charge / combo / ordinary proc crit / recursive skill / recursive N3,
- normal armor, kill, kill coin and contribution attribution,
- existing boss scalars apply,
- generic N3 knockback uses NORMAL-equivalent base; milestone tier does not automatically escalate generic knockback,
- class identity multipliers remain authoritative.

Canonical contract:
`N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`

N3 implementation remains intentionally gated on Slice C full PASS.

---

# Active Slice C — automation PASS / final device smoke pending
Purpose:
- larger-party baseline,
- remove dependency on the legacy 24-event snapshot tail before N3 is enabled.

Event kernel:
- 512-event authoritative history,
- per-WebSocket `eventRunId` + `eventCursor` hibernation attachment,
- monotonic `event-batch` delivery,
- socket state snapshots carry no legacy event tail,
- explicit `event-gap` if retention continuity is impossible,
- reconnect floors at latest while preserving existing resume/eventFloor historical-replay suppression.

Automation PASS evidence on `1afb125c86fc5c085c6b1246dec77b36a1d30159`:
- SERVER 28/28 PASS,
- v0.36 client regression PASS,
- v0.37 client regression PASS,
- event client PASS,
- larger-party simulation PASS,
- FINAL PASS.

Larger-party automated coverage:
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI,
- fixed slots,
- host identity/reconnect,
- READY/START,
- Stage 1 -> Team Shop -> Stage 2,
- contiguous event IDs,
- no unexpected event-gap,
- >24 event delivery without silent loss.

Post-automation smoke candidate:
- watched HEAD `cbcddf35443ff901b4a30dd6621da5a984335fb5`,
- adds candidate-only `?partybot=3` single-device smoke harness,
- local phone remains the real host/player,
- three simulated HUMAN WebSocket sessions join as ARCHER/MAGE/TANK,
- test overlays are hidden outside combat and do not alter server authority/balance.

Final Slice C gate:
- one Samsung Browser 4H render/input smoke only.

Do not enable N3 or Stage 4 until that smoke closes Slice C.

---

# Following bounded work
1. Close Slice C with one final Samsung Browser 4H smoke.
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
