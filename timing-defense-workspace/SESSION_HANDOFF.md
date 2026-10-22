# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Current architecture
Primary lane: **Cloudflare Workers + Durable Objects event-driven multiplayer**.

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- validated HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`

Last executable checkpoint:
- **v0.45 SIEGER FULL PASS**
- branch `timing-defense-cloudflare-v045-sieger-pass-20261022`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- live run/job `39725993894` / `119649887564`

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
5. `MONSTER_CAPABILITY_CONTRACT_V1.md`
6. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
7. `CLOUDFLARE_V045_SIEGER_CAPABILITY_PASS_2026-10-22.md`
8. `SKILL_PLAN_LV6_31.md`
9. `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`
10. `V016_IMPLEMENTATION_REPORT.md`
11. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
12. `DESIGN_DECISIONS.md`

---

# Closed foundations
- v0.36: exact EXP/N2/Lv6 authority.
- v0.38: 512-event multiplayer/reconnect kernel.
- v0.39: N3 frozen and authoritative.
- Monster Capability V1: all nine ordinary archetypes mechanically authoritative through v0.45.

Nine ordinary archetypes:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Current monster capability coefficients are still **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN**.

Do not reconstruct legacy Stage4→10 as production campaign content. Stage1–3 are regression fixtures only. Final direction remains approximately 50 stages with tier/S-E-X authoring and deterministic 2/3/4-player simulation/calibration.

---

# v0.45 SIEGER closure
Checkpoint `timing-defense-cloudflare-v045-sieger-pass-20261022` @ `ea22cc279603394dc4b439b6fdbb0c83aff4299a`.

Validated:
- exact standoff arrival,
- ADVANCE/WINDUP/COOLDOWN authoritative state,
- instantaneous FIRE event,
- repeated wall shots while monster remains alive,
- team DEF,
- knock/reposition/fresh windup,
- SUPPORTER approach-only interaction,
- no premature stage clear,
- reconnect/late replay/event monotonicity,
- SIEGER **20/20 PASS**,
- complete prior browser/WebSocket regression PASS.

Initial live workflow failure was an outdated 18-check expectation only; deployed gameplay diagnostics were already 20/20. The gate was corrected without gameplay/numerical changes and rerun SUCCESS.

No Samsung Browser smoke was required because no visible authored SIEGER encounter/final telegraph presentation exists yet.

---

# Player Skill Authority Review — COMPLETE / DECISION REQUIRED
Canonical review:
`PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`

Six intended milestones exist:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`.

## Current truth
- **Lv6:** FROZEN+AUTHORITATIVE in Cloudflare.
- **Lv11/Lv16/Lv21:** exact legacy v0.16 playable formulas exist and were v7-simulated; current status is LEGACY-REFERENCE / parity candidate, not current server authority.
- **Lv26:** DESIGNED-NOT-AUTHORITATIVE; no playable implementation existed.
- **Lv31:** final identity concepts exist but production implementation is UNRESOLVED because critical numerical/geometry/timing details remain unspecified.

Old migration preflight explicitly classified Lv6–21 as migration candidates and Lv26/Lv31 as design-only. Legacy `v016-core.js` has no Lv26/Lv31 combat branches.

## Recommended parity strategy — NOT YET APPROVED
Do not code Lv11+ until explicit approval.

Recommended:
1. port exact legacy **Lv11** formulas as bounded server-authority slice P1,
2. port exact legacy **Lv16** formulas as bounded slice P2,
3. port exact legacy **Lv21** formulas as bounded slice P3,
4. leave **Lv26/Lv31** design-only until reviewed against the new monster roster and approximately-50-stage structure,
5. do not production-freeze new Lv26/Lv31 values yet.

### P1 Lv11 candidate
- Knight: +1 normal / +2 heavy penetration, secondary 85%.
- Rogue: +6 percentage-point native proc crit.
- Tank: shared wall incoming -10%, nonstack.
- Archer: +10% base damage; old +25% projectile speed is presentation/time-of-flight unless later made gameplay relevant.
- Mage: radius×1.35 / splash60%.

### P2 Lv16 candidate
- Knight: PERFECT-containing ×1.18 damage / ×1.20 knock.
- Rogue: recovery390→312ms with authoritative cadence validation.
- Tank: 80 wall shield / 3s refresh, nonstack.
- Archer: PERFECT armor-ignore / 100% preserved penetration.
- Mage: ~180ms delayed 55% outer-ring blast, center excluded.

### P3 Lv21 candidate
- Knight: heavy×1.20 / up to3 extra penetrations, legacy secondary85%.
- Rogue: heavy 100% + four45% follow-ups.
- Tank: broad heavy multi-target / heavy knock×2.0.
- Archer: strict-line triple shot 100+65+65.
- Mage: heavy×1.20 / radius×1.60.

Why this matters: under the old accepted EXP model Lv21 was already commonly reachable by Stage10, so an approximately-50-stage calibration using only current Lv6 authority would materially understate player power.

Do not infer final Lv26/Lv31 reach timing until the final EXP/campaign progression is calibrated.

---

# Exact next boundary
**Product decision, not implementation:** approve/reject/modify the recommended Lv11/Lv16/Lv21 exact parity strategy.

If approved, start P1 Lv11 from exact v0.45 PASS checkpoint and retain all existing regression gates.

After P1/P2/P3 closure:
- review/freeze Lv26/Lv31 structural contracts or redesign later progression,
- build approximately-50-stage tier/S-E-X authoring model,
- generate 2/3/4-player candidate recipes,
- run deterministic simulation,
- classify/report/discuss,
- explicitly freeze production numbers only after decision.

## Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`.

## Governance
No numerical change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
