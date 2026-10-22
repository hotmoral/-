# Timing Defense — P4-B Lv6→Lv21 Combat Feedback Execution Report V0.1

Date: 2026-10-23 KST  
Status: **P4-B DIVERGENCE FOUND / NEW USER DECISION GATE REQUIRED / NO NEW XP SEMANTICS AUTHORIZED**

Depends on:
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `80_P4A_MARKER_ONLY_INVERSE_DESIGN_EXECUTION_REPORT_V0_1.md`
- `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
- `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
- P3 persistent-run evidence

Machine-readable diagnostic:
- `data/p4b_combat_feedback_divergence_v0_1.json`

---

# 0. Admission question

Does the user-approved P4 baseline remain jointly feasible when real/current Lv6 power and exact v0.16 Lv11/Lv16/Lv21 parity mechanics are allowed to change kill speed and therefore the number of valid local timing turns that produce XP?

Approved baseline under test:

```text
valid completed local timing turn
 -> one quality-based XP_CREDIT award
 -> one universal EXP curve across all classes/Tiers
 -> no hidden class/Tier correction
```

P4-B answer:

**NO for the current common milestone windows under the bounded combat-feedback evidence.**

This is a diagnostic conflict, not permission to patch EXP, skills or encounters.

---

# 1. Why P4-A was not enough

P4-A intentionally disabled skill power and proved only that one universal curve is feasible when milestones are markers.

P4-B activates:
- Lv6 current authoritative effects;
- Lv11/Lv16/Lv21 exact v0.16 formulas as simulation-only parity candidates;
- no Lv26/Lv31 power.

The causal loop is:

```text
skill unlock
 -> class-specific combat efficiency changes
 -> kill speed / target availability changes
 -> valid timing-turn count changes
 -> later XP accumulation changes
 -> later milestone reach shifts
```

This is exactly the feedback loop P4-B was required to test.

---

# 2. Independent P3 cross-check

Before using the feedback response in the 50-Stage propagation, it was checked against the already-closed P3 first-10 Lv6 lanes.

P3 observed first-10 timing-turn change from forced Lv6:

```text
Knight   about -0.2%
Rogue    about -20.2%
Tank       0.0%
Archer   about -18.9%
Mage     about -14.7%
```

Bounded P4-B response model:

```text
Knight     0.0%
Rogue    -20.73%
Tank       0.0%
Archer   -19.64%
Mage     -19.27%
```

Interpretation:
- Knight/Rogue/Tank/Archer closely reproduce the independent P3 direction and magnitude;
- Mage is stronger by roughly 4.6 percentage points and therefore remains an explicit conservative WATCH;
- the early offensive-skill opportunity loss is not a purely hypothetical model artifact.

---

# 3. All-20 skill-step action-opportunity signal

Median action-count ratio versus the same representative encounter at Lv1:

| Class | Lv6 | Lv11 | Lv16 | Lv21 |
|---|---:|---:|---:|---:|
| Knight | 1.000 | 0.546 | 0.500 | 0.447 |
| Rogue | 0.636 | 0.633 | 0.633 | 0.500 |
| Tank | 1.000 | 1.000 | 1.000 | 0.521 |
| Archer | 0.675 | 0.658 | 0.552 | 0.435 |
| Mage | 0.650 | 0.544 | 0.449 | 0.429 |

The important structural asymmetry is not equal DPS.
It is **how many EXP-producing timing turns remain after each skill**.

Before Lv21:
- Tank Lv6/Lv11/Lv16 is mostly control/defense and therefore retains roughly all timing-turn opportunity;
- Rogue/Archer/Mage already remove substantial numbers of later turns through extra damage/coverage;
- Knight changes sharply at Lv11 penetration.

At Lv21 Tank also receives major offensive area control, so its future opportunity rate falls, but it already accumulated an earlier XP lead.

This is a legitimate class-identity consequence; P4-B does not classify the class skills themselves as numerically wrong.

---

# 4. Why simply adding more monsters/HP is not a complete fix

The user explicitly identified gameplay-natural encounter levers as preferable to hidden XP correction where possible.
That remains correct.

However, all classes play the **same Stage content**.
Adding more HP or more monsters generally increases available turns for every class.
It does not automatically remove the relative opportunity gap created by asymmetric skills.

The all-20 Lv6 range demonstrates the issue particularly clearly:
- Rogue action ratio versus Lv1 remains approximately `0.543..0.750` across the existing representative vocabulary;
- Archer approximately `0.571..0.938`;
- Mage approximately `0.444..0.846`;
- Tank approximately `0.933..1.071`.

Therefore local encounter authoring can and should adjust unhealthy individual Stage shapes, but forcing every Tier to counteract these class differences through HP/count/formation would risk turning progression calibration into class-suppression authoring.

Encounter identity remains primary.

---

# 5. P4-A midpoint anchors under combat feedback

The P4-A midpoint anchors were deliberately only starting candidates.
Once combat feedback is enabled they fail strongly.

Representative P50 examples using those starting anchors:

```text
Knight
T1: Lv6 7 / Lv11 13 / Lv16 22 / Lv21 36 / Lv26 >50 / Lv31 >50

Rogue
T4: Lv6 7 / Lv11 17 / Lv16 26 / Lv21 36 / Lv26 46 / Lv31 >50

Tank
T2: Lv6 6 / Lv11 11 / Lv16 18 / Lv21 26 / Lv26 41 / Lv31 >50

Mage
T3: Lv6 5 / Lv11 15 / Lv16 25 / Lv21 41 / Lv26 >50 / Lv31 >50
```

This does **not** mean those classes really should unlock at those exact Stages.
It means the marker-only threshold scale cannot survive actual skill-power feedback unchanged.

---

# 6. Can pure per-turn XP be rescued by refitting the six anchors?

A sequential best-compromise search was run while preserving:
- pure per-valid-turn XP source;
- one universal threshold per milestone;
- no class/Tier multiplier;
- current target windows.

Best approximate universal thresholds still left:

| Milestone | Approx threshold | Worst miss | Class×Tier misses |
|---|---:|---:|---:|
| Lv6 | 130.5 | 0 Stage | 0 |
| Lv11 | 233.0 | 1 | 1 |
| Lv16 | 328.0 | 3 | 7 |
| Lv21 | 457.25 | 4 | 15 |
| Lv26 | 539.5 | 5 | 7 |
| Lv31 | 656.5 | 5 | 8 |

Representative conflicts:

### Lv16 target 18–21
- Rogue T4 around Stage24;
- Mage T4 around Stage24;
- Tank T2 around Stage15.

### Lv21 target 25–28
- Mage T3/T4 around Stage32;
- Tank T1/T2/T3 around Stage21.

### Lv31 confirmed target 41–45
- Mage T3 around Stage50 and T2 around Stage49;
- Tank around Stage36–37 in several Tiers;
- Knight T3 around Stage46.

Therefore the problem is not solved by simply replacing the six P4-A anchor numbers.

---

# 7. Robustness check

The feedback magnitude was artificially attenuated toward marker-only behavior to test whether a modest modeling error could explain the conflict.

```text
feedback alpha 1.00 -> Lv31 worst miss 5 Stages
feedback alpha 0.75 -> Lv31 worst miss 3
feedback alpha 0.50 -> Lv31 worst miss 2
feedback alpha 0.25 -> Lv31 worst miss 1
```

Lv16/Lv21 show the same direction.

Because independent P3 evidence already places Rogue and Archer early feedback near the full-response estimate, treating the real system as only 25% of this effect is not supported.

Conclusion:

**P4-B divergence is robust enough to require a design decision rather than silent threshold tuning.**

---

# 8. Rejected automatic responses

P4-B does not authorize any of the following:

## Hidden class-specific EXP multiplier
Would make the curve fit but directly violates the approved universal-curve direction and obscures why progression moves.

## Hidden Tier-specific EXP multiplier
Would conceal encounter-opportunity shape instead of calibrating it.

## Nerf offensive skills solely to preserve attack count
Would make progression mechanics dictate class identity; not justified by this evidence.

## Inflate all Stage HP/count until turn counts converge
Same content is shared by every class, so this does not guarantee relative convergence and can flatten Tier identity / create HP-sponginess.

## Small flat Stage-clear XP patch
Exploratory values reduced the worst error only gradually and still left substantial misses. It also conflicts with the currently approved no-flat-stage-XP baseline unless explicitly re-approved.

---

# 9. Exploratory class-neutral normalization signal

One new direction was tested only as a **non-authoritative sensitivity probe**:

```text
Stage XP
= rawWeight × SUM(actual turn-quality credit)
+ (1 - rawWeight) × nominal Stage opportunity × mean actual turn quality
```

Meaning:
- timing quality still controls progression;
- efficient kills do not automatically erase most progression opportunity;
- the normalization is class-neutral and Tier-visible rather than a hidden class multiplier;
- Tier encounter flow does not need to become identical.

Reduced-order sensitivity:

| Raw per-turn share | Result against current milestone windows |
|---:|---|
| 100% | worst miss ~5 Stages |
| 75% | worst miss ~3 |
| 50% | worst miss ~2 |
| 25% | a few ~1-Stage misses remain |
| 10% | all tested windows jointly feasible |
| 0% | all tested windows jointly feasible |

This is **not** approval of 10%, 0%, or any blend.
The exact result depends on future full simulation, tail criteria, Lv26/Lv31 power and later shop/permanent-power coupling.

It does prove something narrower:

> a tiny generic bonus is unlikely to be enough if the current common milestone windows are retained; a meaningful opportunity-normalization component is directionally capable of solving the structural divergence.

---

# 10. P4-B classification

```text
P4B_UNIVERSAL_PURE_PER_TURN_WINDOW_CONFLICT
```

Supporting classifications:
- `EARLY_OFFENSIVE_SKILL_XP_SELF_DAMPING_LARGE`
- `DEFENSIVE_TANK_EARLY_XP_LEAD`
- `CONFIRMED_LV31_WINDOW_NOT_JOINTLY_FEASIBLE_UNDER_PURE_PER_TURN_BASELINE`

P4-B therefore cannot responsibly proceed straight into P4-C Lv26 with the old EXP-source baseline unchanged.
Lv26 power would be calibrated on top of an already-divergent progression spine.

---

# 11. Exact next boundary

A new user decision gate is required before P4-C.

Question:

> How should run-local EXP preserve timing mastery while preventing class combat efficiency from making the confirmed Lv31 Stage41–45 progression window structurally class-dependent?

The next document should compare real alternatives and recommend one.
No new EXP acquisition semantics are approved by this execution report.

Production remains untouched.
