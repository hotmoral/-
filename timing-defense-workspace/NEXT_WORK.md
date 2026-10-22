# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Closed implementation gates
1. Cloudflare DO PoC — **PASS**
2. v0.31/v0.32 waiting room — **PASS**
3. v0.33 Stage1 authority — **PASS**
4. v0.34 render/remote projectile parity — **PASS**
5. v0.35 reconnect/Team Shop/Stage2 — **PASS**
6. v0.36 N1/N2 + Lv6 — **FULL PASS**
7. v0.37 Stage3 + BRUTE regression fixture — **FULL PASS**
8. v0.38 larger-party/event kernel — **FULL PASS**
9. v0.39 N3 — **FULL PASS**
10. Monster Capability Foundation V1 — **PASS**
11. v0.40 SHIELD — **FULL PASS**
12. v0.41 FLYER — **FULL PASS**
13. v0.42 CHARGER — **FULL PASS**
14. v0.43 SPLITTER — **FULL PASS**
15. v0.44 SUPPORTER — **FULL PASS**
16. v0.45 SIEGER — **FULL PASS**
17. Player Skill Authority Review — **COMPLETE / DECISION GATE OPEN**

## Exact latest executable checkpoint
- branch `timing-defense-cloudflare-v045-sieger-pass-20261022`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`
- live run/job `39725993894` / `119649887564`

SIEGER closure report:
`CLOUDFLARE_V045_SIEGER_CAPABILITY_PASS_2026-10-22.md`

Player-skill authority review:
`PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`

---

# Campaign direction
Do **not** reconstruct legacy Stage4→10 as production content.

Final direction remains approximately 50 stages with tier identities, S/E/X pressure grammar, 2/3/4-player composition scaling, re-authored monster combinations, and deterministic simulation before production balance freeze.

Stage1–3 remain regression fixtures only.

---

# Monster Capability V1 — MECHANICAL FOUNDATION COMPLETE
All nine ordinary archetypes now have a server-authoritative mechanical foundation:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Current capability coefficients remain **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN** unless separately approved.

Bosses remain a separate capability-composition layer.

---

# Player-skill authority review — recovered truth

## Current authoritative
- Lv6 class skills: **FROZEN+AUTHORITATIVE** through v0.36 and later regressions.
- N3 combo milestone system: **FROZEN+AUTHORITATIVE** through v0.39 and later regressions.

## Exact legacy parity candidates
Legacy v0.16 actually implemented/deployed and v7 exact simulation mirrored:
- Lv11
- Lv16
- Lv21

These are **LEGACY-REFERENCE / parity candidates**, not silently re-frozen by the review.

`CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md` previously classified Lv6–21 as migration candidates and explicitly left Lv26/Lv31 design-only.

## Design-only / unresolved later milestones
- Lv26: explicit class concepts and several proposed coefficients exist, but no playable authority implementation existed.
- Lv31: final identity concepts exist, but multiple implementation-critical damage/geometry/timing details remain underspecified.

Do not silently implement Lv26/Lv31 from roadmap prose.

---

# Active decision gate — post-Lv6 parity strategy

No code should be written for Lv11+ until this product decision is explicit.

Recommended default:
**adopt the exact v0.16 Lv11/Lv16/Lv21 combat formulas as parity candidates and port them server-authoritatively in three bounded slices; keep Lv26/Lv31 out of implementation until their contracts are reviewed against the new 9-monster roster and approximately-50-stage campaign.**

If approved, implementation order:

### P1 — Lv11 authoritative parity
- Knight: +1 normal / +2 heavy penetration, legacy secondary 85%
- Rogue: +6 percentage-point native proc crit
- Tank: shared wall incoming damage -10%, nonstack
- Archer: +10% base damage; projectile-speed change remains presentation/time-of-flight unless later made gameplay-relevant
- Mage: radius ×1.35, splash 60%

### P2 — Lv16 authoritative parity
- Knight: PERFECT-containing ×1.18 damage / ×1.20 knock
- Rogue: qualifying recovery 390ms -> 312ms with server action-cadence validation
- Tank: 80 wall shield / 3000ms refresh, nonstack
- Archer: PERFECT armor-ignore / preserved 100% penetration damage
- Mage: delayed ~180ms 55% outer-ring resonance, center excluded

### P3 — Lv21 authoritative parity
- Knight: heavy ×1.20 / up to3 extra penetrations, legacy secondary 85%
- Rogue: heavy 100% + four 45% follow-ups
- Tank: broad heavy multi-target / heavy knockback ×2.0
- Archer: strict-line triple heavy 100%+65%+65%
- Mage: heavy ×1.20 / blast radius ×1.60

Each slice must retain all v0.39–v0.45 regression gates.

### P4 — Lv26/Lv31 product-contract review
Before full late-campaign calibration, explicitly resolve:
- whether the six-milestone roadmap remains final,
- structural skill identities,
- underspecified Lv26/Lv31 semantics,
- provisional simulation coefficients versus production-frozen values,
- expected unlock timing under the final 50-stage EXP curve.

---

# Why this blocks final calibration
Under the old accepted EXP rule, `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md` found Lv21 was already commonly reached by Stage10 at Skilled proficiency. Therefore an approximately-50-stage calibration using only current Lv6 server authority would materially misrepresent player power.

The authoring **infrastructure** may be designed before Lv26/Lv31 final freeze, but final late-campaign numerical calibration/freeze should wait until later skill contracts and progression timing are resolved.

---

# After parity decision
If P1/P2/P3 are approved and closed:
1. review/freeze the structural Lv26/Lv31 contract or explicitly redesign the later progression,
2. build approximately-50-stage tier/S-E-X authoring model,
3. generate deterministic 2/3/4-player candidate recipes,
4. run large simulation for pressure/density/role opportunity/clear envelope,
5. classify/report/discuss,
6. patch only after explicit decision,
7. explicitly freeze production monster/stage values.

## Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`

## Governance
No unapproved numerical change:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
