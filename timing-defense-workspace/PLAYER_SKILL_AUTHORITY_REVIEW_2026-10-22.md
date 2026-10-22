# Timing Defense — Player Skill Authority Review

Date: 2026-10-22 KST
Status: **REVIEW COMPLETE / NO NEW SKILL IMPLEMENTATION AUTHORIZED BY THIS DOCUMENT**

## Purpose
After Monster Capability V1 closed all nine ordinary archetypes through v0.45, recover the exact player-skill progression truth before approximately-50-stage authoring/calibration.

This review does **not** invent or freeze new numerical values.

Classification used here:
- `FROZEN+AUTHORITATIVE` — approved contract and current Cloudflare server combat authority exist.
- `LEGACY-REFERENCE` — implemented/deployed in the legacy playable build with exact formulas and validation evidence, but not yet current Cloudflare server authority. Treat as parity candidate, not automatic production freeze.
- `DESIGNED-NOT-AUTHORITATIVE` — explicit design exists, but no legacy/current authoritative combat implementation at that milestone.
- `UNRESOLVED` — implementation-critical details remain underspecified and require product discussion before a final contract can be implemented/calibrated.

---

# 1. Source-of-truth findings

## Six-milestone roadmap exists
`SKILL_PLAN_LV6_31.md` defines the intended automatic milestones:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`.

`DESIGN_DECISIONS.md` also freezes the **roadmap/presentation direction** that all six milestones should be visible in character selection.

This does not by itself freeze every combat coefficient.

## Legacy implementation boundary is Lv21
`V016_IMPLEMENTATION_REPORT.md` and legacy `v016-core.js` show actual playable combat implementation through:
`Lv6 / Lv11 / Lv16 / Lv21`.

Lv26/Lv31 names are present in the six-slot roadmap/unlock list, but there are no `v016Has(26)` / `v016Has(31)` combat branches in the v0.16 playable authority baseline.

`CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md` explicitly classified:
- **Lv6–21 = migration/parity candidates**
- **Lv26/Lv31 = design-only for that migration preflight; do not invent implementation**.

`HANDOFF_FREEZE_2026-10-20_2334KST.md` likewise named later migration of **Lv6/Lv11/Lv16/Lv21 multiplayer effects server-side** as future work.

## Current Cloudflare boundary
Current `v036-entry.js` supplies Lv6 authority only. Its combat activation is based on `levelBefore >= 6`; it does not implement Lv11/Lv16/Lv21 progression branches.

v0.39 N3 is separately frozen/authoritative and is not a replacement for the class milestone skills.

---

# 2. Authority matrix

## Knight
| Level | Contract recovered | Current status |
|---|---|---|
| Lv6 | Enhanced Blade Wave: +12% blade-wave damage; projectile size +25% is presentation | **FROZEN+AUTHORITATIVE** for combat damage; presentation remains client-side |
| Lv11 | Breakthrough Slash: normal +1 penetration; heavy +2; secondary penetration 85% | **LEGACY-REFERENCE** / exact parity candidate |
| Lv16 | Sharp Edge: attack containing PERFECT +18% damage and +20% knockback | **LEGACY-REFERENCE** / exact parity candidate |
| Lv21 | Great Blade Wave: heavy +20% damage; up to 3 additional penetrations; legacy extra penetration damage remains 85%; giant crescent presentation | **LEGACY-REFERENCE** / exact parity candidate |
| Lv26 | Frontline Collapse: penetration no longer decays; each penetration raises knockback against next enemy +15% | **DESIGNED-NOT-AUTHORITATIVE**; structural idea is explicit but needs re-approval before production use |
| Lv31 | Heaven-Splitting Slash: P×P CRITICAL huge double blade wave / broad penetration / major knockback | **UNRESOLVED** for production: exact damage, penetration geometry/count, double-wave timing and “major” knockback magnitude are not fully specified |

## Rogue
| Level | Contract recovered | Current status |
|---|---|---|
| Lv6 | Double Dagger: second dagger 55% | **FROZEN+AUTHORITATIVE** |
| Lv11 | Weak-Point Detection: +6 percentage points native class proc-crit chance | **LEGACY-REFERENCE** / exact parity candidate |
| Lv16 | Assassin Rhythm: PERFECT-containing attack recovery 390ms -> 312ms (20% recovery reduction) | **LEGACY-REFERENCE** / exact parity candidate; requires authoritative action-cadence eligibility |
| Lv21 | Blade Barrage: heavy = main 100% + four 45% follow-up daggers; same-target uncapped; boss dagger scalar 0.70 | **LEGACY-REFERENCE** / exact parity candidate |
| Lv26 | Chain Throw: PERFECT adds tracking dagger against nearest secondary enemy for 45% | **DESIGNED-NOT-AUTHORITATIVE**; target/fallback/interaction contract should be explicitly re-approved |
| Lv31 | Dagger Storm: P×P CRITICAL launches 8 rapid tracking daggers over ~0.5s | **UNRESOLVED** for production: per-dagger damage and exact schedule/retarget semantics are not specified |

## Tank
| Level | Contract recovered | Current status |
|---|---|---|
| Lv6 | Impact Wave+: +30% knockback; +30% shockwave width is presentation | **FROZEN+AUTHORITATIVE** for combat knockback |
| Lv11 | Iron Wall: shared wall incoming damage -10%; multiple Tanks do not stack | **LEGACY-REFERENCE** / exact parity candidate |
| Lv16 | Perfect Guard: PERFECT refreshes wall shield to 80 for 3s; no stacking | **LEGACY-REFERENCE** / exact parity candidate |
| Lv21 | Ground Impact: broad heavy multi-target hit; heavy Tank knockback ×2.0 in exact v0.16 implementation | **LEGACY-REFERENCE** / exact parity candidate |
| Lv26 | Aftershock Zone: heavy leaves 1.5s zone; enemy movement -25% | **DESIGNED-NOT-AUTHORITATIVE** but implementation geometry/zone placement needs explicit contract before production use |
| Lv31 | Absolute Barrier: P×P CRITICAL battlefield-wide shockwave + 250 wall shield for 6s | **UNRESOLVED** for production: shockwave damage/knock/target semantics are not fully specified even though shield value/duration are proposed |

## Archer
| Level | Contract recovered | Current status |
|---|---|---|
| Lv6 | Piercing Arrow: up to 2 additional strict-line targets; current authoritative secondary coefficient 52% | **FROZEN+AUTHORITATIVE** |
| Lv11 | Strong Bow: projectile speed +25% presentation; base damage +10% combat | **LEGACY-REFERENCE** / exact parity candidate |
| Lv16 | Precision Penetration: PERFECT-containing arrow ignores armor and preserves 100% penetration damage | **LEGACY-REFERENCE** / exact parity candidate |
| Lv21 | Triple Shot: heavy = 100% + 65% + 65%; all arrows remain locked straight-line / non-seeking | **LEGACY-REFERENCE** / exact parity candidate |
| Lv26 | Impaling Shot: PERFECT penetration count +2 and preserves 100% rear-target damage | **DESIGNED-NOT-AUTHORITATIVE**; structurally fairly explicit but requires re-approval rather than silent port |
| Lv31 | Sky-Piercing Arrow: P×P CRITICAL huge high-speed arrow, battlefield line penetration without target-count limit, armor ignore | **UNRESOLVED** for production: exact damage/size/speed and battlefield collision bounds are not frozen |

## Mage
| Level | Contract recovered | Current status |
|---|---|---|
| Lv6 | Arcane Burst: 50% splash around impact | **FROZEN+AUTHORITATIVE** |
| Lv11 | Expanded Magic Circle: radius +35%; splash 50% -> 60% | **LEGACY-REFERENCE** / exact parity candidate |
| Lv16 | Resonance: PERFECT schedules ~180ms delayed 55% outer-ring explosion; original center excluded | **LEGACY-REFERENCE** / exact parity candidate |
| Lv21 | Greater Arcane Orb: heavy +20% damage; explosion radius ×1.6; slower/larger orb presentation | **LEGACY-REFERENCE** / exact parity candidate |
| Lv26 | Chain Explosion: if explosion catches at least 2 enemies, propagate secondary explosions to up to 2 enemies for 35% | **DESIGNED-NOT-AUTHORITATIVE**; exact propagation generation/target reuse rules need explicit contract |
| Lv31 | Arcane Collapse: P×P CRITICAL large magic circle + three-stage blast + chained secondary explosions | **UNRESOLVED** for production: stage timing, damage allocation, radii and chain limits are not fully specified |

---

# 3. Exact legacy Lv11–21 formulas available for parity

The legacy v0.16 implementation was not merely descriptive. `BALANCE_SIM_REPORT_V7_V016_EXACT.md` mirrored its exact formulas and found no numerical rebalance authorized from that report.

Recovered exact combat consequences:

### Lv11
- Knight: +1 normal / +2 heavy additional penetration targets, each legacy secondary at 85%.
- Rogue: +6 percentage-point native proc crit.
- Tank: wall incoming damage ×0.90, non-stacking across Tanks.
- Archer: base damage +10%; projectile travel speed +25% is presentation/time-of-flight behavior under the old client projectile model.
- Mage: splash radius ×1.35 and splash coefficient 0.60.

### Lv16
- Knight: any attack containing PERFECT ×1.18 damage and ×1.20 knockback.
- Rogue: qualifying PERFECT recovery 390ms -> 312ms; this is a recovery reduction, not a blanket 20% whole-cycle acceleration.
- Tank: qualifying PERFECT sets/refreshes 80 wall shield with true 3000ms expiry; no stacking.
- Archer: qualifying PERFECT armor ignore + 100% preserved penetration damage.
- Mage: qualifying PERFECT schedules delayed outer-ring blast at ~180ms, 55% coefficient, original center excluded.

### Lv21
- Knight: heavy ×1.20 and up to 3 additional penetrations; legacy extra penetrations remain 85%.
- Rogue: heavy main 100% + four follow-ups at 45% each.
- Tank: broad heavy multi-target impact; heavy knockback becomes ×2.0 in the v0.16 exact implementation.
- Archer: heavy triple shot 100% +65% +65%, strict locked straight-line semantics.
- Mage: heavy ×1.20, blast radius ×1.60; slower/larger projectile is presentation/time-of-flight behavior.

These are **exact legacy parity inputs**, not automatically re-frozen production values by this review.

---

# 4. Why the missing milestones matter before full 50-stage calibration

`BALANCE_SIM_REPORT_V3_SKILL_CURVE.md` found that under the then-accepted EXP rule, by Stage 10 at the Skilled profile the probability of reaching Lv21 was already approximately:
- Knight 96.4%
- Rogue 66.8%
- Archer 98.0%
- Mage 99.0%

Therefore an approximately-50-stage campaign cannot be calibrated credibly while pretending progression stops at current Cloudflare Lv6 authority.

Two separate blockers exist:

## Blocker A — Lv11/Lv16/Lv21 authority gap
These milestones have exact legacy playable formulas, but current multiplayer server authority does not implement them. A simulation calibrated against them while deployed gameplay lacks them would diverge materially.

## Blocker B — Lv26/Lv31 production contract gap
Given how early Lv21 was reachable in the old 10-stage progression, later milestones are likely to matter somewhere in a 50-stage campaign unless the future EXP curve is deliberately changed. Full late-campaign calibration therefore requires explicit Lv26/Lv31 product contracts or an explicit progression redesign that prevents/repositions those unlocks.

No assumption about final reach timing is frozen here because final stage pressure/economy/EXP pacing has not yet been calibrated.

---

# 5. Recommended implementation/decision boundary

## Slice P1 — Lv11 authoritative parity
Recommended first bounded implementation after explicit user approval.

Why first:
- exact legacy formulas exist,
- mostly composes with primitives already built through v0.45,
- gives an early regression boundary before timed-state complexity grows.

Required server consequences:
- Knight penetration geometry/damage,
- Rogue class proc-crit RNG,
- Tank shared wall -10% nonstack rule,
- Archer +10% base damage (speed is presentation under current event-at-action model unless projectile travel later becomes gameplay-relevant),
- Mage radius +35% / splash60%.

## Slice P2 — Lv16 authoritative parity
Higher novelty:
- `containsPerfect` contract across normal/heavy actions,
- Rogue server-side action-cadence eligibility / anti-early-action validation,
- timed shared wall shield state/expiry,
- Archer armor-ignore/preserved line damage,
- scheduled Mage outer-ring effect via authoritative due queue.

## Slice P3 — Lv21 authoritative parity
Heavy-transform milestone:
- Knight extra heavy penetration,
- Rogue scheduled 5-dagger heavy,
- Tank broad multi-target Ground Impact,
- Archer strict-line triple shot,
- Mage greater heavy orb damage/radius.

Current v0.38 event kernel, scheduled queues, authoritative monster geometry, and v0.40–45 capability layer provide much of the required infrastructure.

## Decision Gate P4 — Lv26/Lv31
Do **not** silently implement these from roadmap prose.

Before full late-campaign calibration, explicitly decide:
1. whether Lv26/31 remain the intended final milestones,
2. whether their structural skill identities remain as `SKILL_PLAN_LV6_31.md`,
3. which currently underspecified Lv31/Lv26 semantics need exact contracts,
4. whether their numeric coefficients are provisional simulation anchors or production-frozen values,
5. whether the final EXP curve still reaches these milestones within the ~50-stage campaign.

A structural authoring engine can be developed before this gate closes, but **final late-campaign numerical calibration/freeze should not**.

---

# 6. Recommended next action
The immediate next action is **discussion/approval of the parity strategy**, not code.

Recommended default:
- preserve Lv11/Lv16/Lv21 exact v0.16 combat formulas as parity candidates,
- port them server-authoritatively in three bounded slices P1/P2/P3 with full prior regression,
- leave Lv26/Lv31 as design-only/unresolved until their contracts are reviewed against the new 9-monster roster and 50-stage campaign goals,
- do not freeze new Lv26/Lv31 numbers now.

No numerical balance patch is authorized by this review.

## Governance
Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
