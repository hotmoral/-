# Timing Defense — P5→P6 Persistent-State Fidelity Bridge Result V0.1

Date: 2026-10-23 KST  
Status: **EXACT TEMP EXECUTION PASS / PERSISTENT-STATE CAUSE CHECK CLOSED / STAGE48 LOCAL NUMERIC TUNING PAUSED / P6 TRANSITION USER DECISION REQUIRED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
- `143_P5_SKILLED_V2_LATE_RUN_REINTERPRETATION_AND_P5_P6_FIDELITY_GATE_V0_1.md`

Production gameplay/numerical authority remains unchanged and unauthorized.

---

## 1. Why this bridge was required

The prior P5 Stage46–49 runner correctly represented many late-run systems, but did not carry the P3-approved timing state as one authoritative run state across Stages.

P1/P3 already require:
- combo persists through Stage/shop downtime;
- charge persists through Stage/shop downtime;
- Heavy occurs from charge state rather than a Stage-local periodic counter;
- Heavy consumes two judgments;
- PERFECT streak drives combo/N3;
- non-PERFECT judgment breaks combo;
- no-target downtime consumes no judgment and does not break combo.

The bridge therefore asks:

> Does restoring those approved persistence semantics materially change the P5 conclusion that central-skilled play is highly sensitive to P×P/Lv31-final frequency and strongly class-skewed in Stage46–47?

---

## 2. Bridge implementation boundary

Temporary branch:
- `timing-defense-workspace-temp-p5p6-fidelity`

The bridge reuses the current P5 late-run combat simulator and injects P3 state semantics rather than rewriting combat from scratch.

Included:
- one persistent SKILLED_V2 judgment RNG/state across Stage46→49;
- persistent combo;
- persistent charge;
- Heavy at `charge >= 3`;
- Heavy consumes X/Y judgments;
- only P×P produces CRITICAL/Lv31 final;
- P3 combo root-damage scalar;
- P3 N3 milestones/budgets;
- generated N3 hits do not recursively generate combo/charge/N3;
- existing P5 shop, class packages, Lv31 packages, SIEGER/CHARGER state, right-edge entry and wall carry;
- `HEAVY+` knockback corrected to authoritative `0.013`;
- fixed authored Stage schedule followed by bounded drain to STAGE_SETTLED;
- enemy instances do not cross Stage boundaries.

Current Stage48 diagnostic center was held constant:

```text
3 spatial ARMORED_DURABLE_PROXY bodies
+ 2 late GRUNT
+ 1 SIEGER
```

This remains diagnostic only and is not adopted.

The current fixed late-segment shop snapshot also remains diagnostic only.

---

## 3. Exact bridge run

GitHub Actions:

```text
run id: 39971985538
repeat deterministic bytes: PASS
SHA256: 0e74da5456cf9ef8fe011bddfec98e6c8656f43789794fad35e5434508ef4333
```

Screen:
- 20 deterministic skilled seeds;
- 5 classes;
- four legal Stage46 entry-charge states `0/1/2/3`;
- 400 central-skilled chains total;
- 20 all-PERFECT controls total;
- Stage46 entry combo initially `0` only as a late-segment boundary, not as a claimed full-run distribution.

Realized skilled judgment mix across the expanded screen:

```text
PERFECT 70.8421%
GOOD    19.5777%
NORMAL   9.5802%
```

Realized Heavy P×P/CRITICAL rate:

```text
56.1330%
```

This remains sufficiently aligned with the SKILLED_V2_CENTRAL design prior for causal use.

---

## 4. Entry-charge sensitivity result

All-PERFECT:

```text
charge 0 -> 5/5 through Stage49
charge 1 -> 5/5
charge 2 -> 5/5
charge 3 -> 5/5
```

Central skilled:

```text
charge 0 -> 48/100 through Stage49
charge 1 -> 45/100
charge 2 -> 42/100
charge 3 -> 44/100
```

Most importantly, Stage46 failure count was identical at every entry charge:

```text
charge 0 -> Stage46 failures 23
charge 1 -> Stage46 failures 23
charge 2 -> Stage46 failures 23
charge 3 -> Stage46 failures 23
```

Therefore:

```text
STAGE46_ENTRY_CHARGE_PHASE != PRIMARY_FAILURE_CAUSE
```

Exact Stage46 charge distribution from Stage1–45 is still future full-run fidelity, but it is not a plausible explanation for the current class-skewed failure surface.

---

## 5. Class separation persists after fidelity repair

Across the four entry-charge states, central-skilled Stage49 completion totals were:

```text
Mage   72 / 80
Archer 61 / 80
Rogue  25 / 80
Knight 20 / 80
Tank    1 / 80
```

All-PERFECT remained 20/20 overall across the four charge controls.

The bridge therefore strengthens rather than removes the prior causal finding:

```text
PERSISTENT_COMBO_CHARGE_REPAIR != RESOLUTION
REDUCED_PXP_LV31_FINAL_FREQUENCY REMAINS A DOMINANT SENSITIVITY
CURRENT_STAGE46_47_PRESSURE_RESPONSE IS STRONGLY CLASS_SKEWED
```

Tank remains the strongest anomaly relative to its survival/control identity.
This is not authorization to buff Tank.

---

## 6. Stage46 entry-combo upper-bound sensitivity

A second bounded diagnostic tested whether the bridge's `combo=0` Stage46 boundary was hiding the cause.

Exact run:

```text
run id: 39972649909
repeat deterministic bytes: PASS
SHA256: 9f12213fca7c3ef963a82fbc267b5a2830a8f789d9c5a1a1eb7264dd00a832f1
```

Conditions:
- central-skilled only;
- entry charge fixed at `0`;
- same 20 seeds × five classes;
- compare entry combo `0` vs `40`;
- `40` is an upper-bound sensitivity, not a claimed Stage46 entry candidate or distribution.

Result:

```text
combo 0  -> 48/100 through Stage49
combo 40 -> 48/100 through Stage49
```

Failure histogram was exactly unchanged:

```text
Stage46 23
Stage47 21
Stage49  8
```

Every class's through-Stage49 count was unchanged:

```text
Knight 5/20
Rogue  6/20
Tank   1/20
Archer 18/20
Mage   18/20
```

Therefore:

```text
STAGE46_ENTRY_COMBO_BOUNDARY != PRIMARY_FAILURE_CAUSE
```

A future full Stage1→45 simulation remains necessary for exact skill-reach and run-state distributions, but it is not required to explain away the present late-run class split.

---

## 7. What this closes

The following possible explanation is now rejected:

> The skilled regression is mainly an artifact of resetting combo/charge or choosing the wrong Stage46 entry timing phase.

Evidence now shows the regression persists under:
- approved cross-Stage combo persistence;
- approved cross-Stage charge persistence;
- P3 Heavy semantics;
- P3 combo scalar;
- P3 N3 milestones;
- four legal entry-charge states;
- an extreme combo40 entry upper-bound.

Thus the current problem sits above simple run-state fidelity.

---

## 8. What is not concluded

Do **not** infer any of the following from this bridge:
- Tank should be buffed;
- Knight/Rogue should be buffed;
- Mage/Archer should be nerfed;
- Stage46 should simply be weakened;
- P×P probability should be increased;
- Lv31 final packages should be reduced or increased;
- the current Stage48 armored packet should be adopted;
- the shop 40% center should be frozen;
- Stage46/47 exact authored counts are production-ready.

Those are coupled P6 questions.

---

## 9. Structural interpretation

The current late-run pressure was designed and iterated largely under an all-P×P upper-tail assumption.
Once central-skilled P×P frequency is restored, current Stage46–47 pressure interacts very differently with the five Lv31 packages.

The correct next question is therefore no longer:

> Which Stage48 SIEGER escort number should be changed next?

It is:

> Under one persistent run-state model, how should encounter pressure, Lv31 final frequency, class package throughput/control, shop leverage and wall attrition converge so intended skilled play preserves class identity without requiring near-all-P×P execution?

That is the already-defined purpose of P6 Joint Run-Power Convergence.

---

## 10. Recommended next boundary — user approval required

Recommended:

```text
PAUSE_LOCAL_STAGE48_TUNING
-> ENTER_P6_JOINT_RUN_POWER_CONVERGENCE
```

First P6 slice should remain bounded and causal:
1. keep SKILLED_V2_CENTRAL and persistent P3 run state fixed;
2. keep shop as explicit diagnostic profiles, not one hidden balance constant;
3. isolate Stage46–47 pressure response by class and by realized P×P/Lv31-final frequency;
4. distinguish damage-throughput, control, wall protection and geometry causes;
5. re-check attack/event count and Lv31/EXP feedback before changing exact monster values;
6. keep Stage48 armored/fodder/SIEGER work parked as evidence, not discarded;
7. return to Stage48 only after the common late-run power/pressure surface is credible;
8. stop for user approval before adopting exact class, monster, shop, EXP or Stage pressure values.

Alternative directions remain possible, but continuing local Stage48 tuning now is not recommended because upstream Stage46–47 central-skilled viability is already broken for several classes.
