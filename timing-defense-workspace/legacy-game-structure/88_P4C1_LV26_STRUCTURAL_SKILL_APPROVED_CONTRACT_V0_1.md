# Timing Defense — P4-C1 Lv26 Structural Skill Approved Contract V0.1

Date: 2026-10-23 KST  
Status: **USER APPROVED DIRECTION / STRUCTURAL CONTRACT / P4-C2 PROVISIONAL NUMBERS ONLY / NO PRODUCTION IMPLEMENTATION**

Depends on:
- `87_P4C1_LV26_STRUCTURAL_SKILL_CONTRACT_PROPOSAL_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `../SKILL_PLAN_LV6_31.md`
- `../PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`

---

# 0. User decision

The user explicitly approved proposal 87 Option A on 2026-10-23 KST.

Approval meaning:
- the Lv26 **structural execution semantics** below become the working P4 contract;
- the roadmap coefficients are admitted only as `P4C2_PROVISIONAL_SIMULATION_INPUT`;
- those coefficients are **not `NUMERIC_FROZEN`** and may be tuned after measured evidence;
- the structural contract may be transparently reopened if later evidence exposes a material contradiction, but it must not be silently changed;
- production gameplay implementation remains unauthorized.

This approval does **not** approve/freeze Lv31, final EXP semantics, shop/Base HP, stars/achievements, boss values, multiplayer scaling, exact campaign authoring, or production numerical values.

---

# 1. Global Lv26 rules — USER APPROVED

1. All five Lv26 mechanics remain P2 **effect rules**. No generic `Lv26 +X% power` proxy is permitted.
2. Every generated Lv26 effect belongs to one valid local root timing action and retains deterministic parent/source attribution.
3. Generated Lv26 effects do not independently grant EXP, charge, or combo.
4. Generated Lv26 effects do not recursively generate another Lv26 effect or recursively generate lower class-skill trees unless a later explicit contract reopens that behavior.
5. Generated Lv26 effects do not independently trigger N3; the root action may still trigger N3 through the existing N3 contract.
6. `PERFECT-containing action` reuses the existing legacy family: normal PERFECT qualifies; Heavy qualifies when either X or Y judgment is PERFECT.
7. Default generated-damage crit policy is `PARENT_ROLL_INHERITED`; no second ordinary proc-crit roll.
8. Each realized target applies its own armor/mitigation/boss scalar independently under P2.
9. No Lv26 skill introduces free manual targeting. Target selection remains authoritative and deterministic.
10. Current roadmap numeric values are provisional P4-C2 inputs only.

---

# 2. Knight — Frontline Collapse

Approved semantics:
- Lv26 changes Lv11/Lv21 additional-penetration damage coefficient from legacy `0.85` to `1.00`.
- Lv26 does not add penetration count.
- primary target keeps the root action's ordinary knockback basis.
- additional penetration targets receive additive next-target knockback steps:
  - extra #1: `×1.15`
  - extra #2: `×1.30`
  - extra #3: `×1.45`
- the step resets each root action.
- Lv16 PERFECT knockback transform composes before the Lv26 penetration step; target/boss resistance applies afterward.
- additional penetration hits inherit the parent crit result and do not reroll ordinary proc crit.

Numeric status:
- `+15% per penetration step` = `P4C2_PROVISIONAL_SIMULATION_INPUT`, not production numeric freeze.

P4-C2 watches:
- screen lifetime;
- CHARGER interruption;
- SIEGER repositioning / first-shot opportunity;
- T4 SUPPORTER/SIEGER role expression;
- timing-turn opportunity loss from faster clearing.

---

# 3. Rogue — Chain Throw

Approved semantics:
- exactly one Chain Throw dagger may be created per qualifying PERFECT-containing root action.
- it is not generated once per Double Dagger/Blade Barrage hit.
- preferred target is the nearest live non-primary enemy relative to the authoritative primary impact, with deterministic tie-break.
- if no secondary enemy exists, no Chain Throw dagger is generated; there is no primary-target fallback.
- if the selected target dies before resolution, the dagger may retarget once using the same secondary-target rule while still excluding the root primary target.
- if no valid target remains, the dagger expires.
- boss dagger scalar applies if the realized target is a boss.
- the dagger cannot itself create Double Dagger, Blade Barrage, Chain Throw, EXP, charge, or combo.
- crit policy is parent inherited.

Numeric status:
- `45%` = `P4C2_PROVISIONAL_SIMULATION_INPUT`.

P4-C2 watches:
- secondary-target availability / expiration rate;
- accidental guaranteed backline deletion;
- SUPPORTER/SIEGER exposure;
- timing-turn opportunity loss.

---

# 4. Tank — Aftershock Zone

Approved semantics:
- each completed Heavy root action creates one authoritative Stage-local Aftershock Zone.
- center = authoritative primary Ground Impact location.
- footprint inherits Ground Impact geometry rather than introducing a new independent radius family now.
- scope = `TEMPORARY / STAGE_LOCAL`.
- zone expires at timer end or `STAGE_SETTLED`, whichever is earlier; it never carries into the next Stage/shop.
- a live zone must be restorable on mid-Stage snapshot/reconnect from authoritative state.
- Aftershock uses one non-stacking slow family across overlapping Tank zones. Overlap can extend coverage in space/time, but not stack the slow magnitude.
- movement composition is explicit:

```text
phase translational speed
× SUPPORTER movement multiplier when active
× AFTERSHOCK movement multiplier when covered
```

- FLYER authoritative Y oscillator is not re-timed; only forward/translational movement is slowed.
- CHARGER ADVANCE/CHARGE translation is slowed; WINDUP timer is unchanged; slow does not itself count as knockback interrupt/cancel.
- SIEGER ADVANCE/reposition is slowed; WINDUP/COOLDOWN/fire cadence and shot damage are unchanged.
- Aftershock deals no damage.

Numeric status:
- duration `1.5s` and movement multiplier `0.75` (`-25%`) = `P4C2_PROVISIONAL_SIMULATION_INPUT`.

P4-C2 watches:
- target-lifetime extension and possible EXP-opportunity increase;
- SIEGER approach/reposition timing;
- SUPPORTER aura exposure;
- CHARGER movement-state interaction;
- snapshot/Stage-settlement invariants.

---

# 5. Archer — Impaling Shot

Approved semantics:
- on a PERFECT-containing Archer root action, Lv26 adds `+2` maximum additional penetration targets to each qualifying arrow.
- Lv16 remains the only transform that grants PERFECT armor-ignore and 100% penetration-damage preservation.
- the Lv26 wording about `100% rear-target damage` is interpreted as reaffirming that the newly extended rear penetrations inherit the existing Lv16 preservation; it is **not** a second damage multiplier.
- with Lv6+Lv26, one qualifying arrow can hit the primary plus up to four additional strict-line targets.
- Lv21 Triple Shot arrows inherit the +2 extension because the legacy side arrows already inherit Lv6/Lv16 penetration rules.
- locked straight-line / no-homing / no off-line retarget semantics remain unchanged.
- mitigation remains per target except where Lv16 armor-ignore applies.

Numeric status:
- `+2 penetration` = `P4C2_PROVISIONAL_SIMULATION_INPUT`.

P4-C2 watches:
- deep-line screen deletion;
- T4 protected SUPPORTER/SIEGER exposure;
- class-role overlap with Knight;
- timing-turn opportunity loss.

---

# 6. Mage — Chain Explosion

Approved semantics:
- Lv26 is evaluated once per root Mage action.
- the immediate root explosion package consists of the primary impact plus immediate Arcane Burst results.
- the package qualifies when it hits at least two distinct enemies; the primary counts.
- Lv16 delayed Resonance does not independently trigger Lv26.
- after immediate root-package damage plus resulting death/spawn consequences are resolved, select up to two current live enemies that were not already hit by that root package.
- newly spawned SPLITTER children may therefore be eligible if alive and not already root-hit. This is forward secondary resolution, not retroactive damage to children from the parent hit.
- each selected target receives exactly one Chain Explosion hit.
- Chain Explosion is one-generation only.
- chain hits do not generate Arcane Burst, Resonance, another Chain Explosion, EXP, charge, or combo.
- there is no same-target fallback.
- crit policy is parent inherited; each realized target resolves its own mitigation.

Numeric status:
- `35%` coefficient / `max 2 targets` = `P4C2_PROVISIONAL_SIMULATION_INPUT`.

P4-C2 watches:
- SPLITTER transformation/population readability;
- density scaling and event-volume growth;
- chain eligibility after death/spawn ordering;
- timing-turn opportunity loss.

---

# 7. Cross-stage consistency result

The approved package is compatible at the structural level with:
- P1 run lifecycle;
- P2 effect/attribution pipeline;
- P3 `STAGE_SETTLED` temporary-effect boundary;
- current system-driven targeting;
- Monster Capability V1;
- current role-expression contract;
- Model-A T4 late-band grammar;
- future T5+ roster expansion.

Approval does not prove balance. It only removes ambiguity so P4-C2 can measure the actual effects deterministically.

---

# 8. Next boundary

P4-C1 = **USER_APPROVED_STRUCTURAL_COMPLETE**.

Next:

`P4-C2 — LV26 BOUNDED PROVISIONAL POWER FEEDBACK`

P4-C2 must use paired deterministic comparisons and must separate:
1. old formula-fidelity / action-opportunity sensitivity evidence from
2. current nine-roster role-interaction probes.

Do not promote old five-monster pressure lanes to current production balance authority.
Do not claim final EXP convergence.
Do not modify production gameplay.

After P4-C2 closes, the next gate is P4-D1 Lv31 structural review/decision.