# Timing Defense — P6 Shop ATK / EXP Opportunity Bidirectional Feedback Result V0.1

Date: 2026-10-24 KST  
Status: **P6-B1 DIAGNOSTIC COMPLETE / BIDIRECTIONAL SHOP→EXP FEEDBACK CONFIRMED / TANK ROLE INTERPRETATION REFINED / EXACT SKILL-REACH SHIFT OPEN / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `151_P6_ENCOUNTER_FAMILY_ROTATION_AND_TANK_OBJECTIVE_ATTRIBUTION_RESULT_V0_1.md`
- `150_P6_STAGE46_47_FIRST_CAUSAL_CONVERGENCE_RESULT_V0_1.md`
- `144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`
- `124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `CHARACTER_PROFILE_RADAR_V1.md`

Production gameplay remains unchanged and unauthorized.

---

## 1. Player-facing Tank identity clarification

The approved class-selection radar is not a literal hidden-stat table. It is a player-facing readability / identity contract.

Approved Tank radar:

```text
ATK 2 / CRIT 1 / AGI 1 / KNOCK 5 / PEN 1 / AOE 3
```

User clarification during P6:

> Tank is not intended to be a monster-killing class. If its control / defense / wall-protection role is functioning, low removal by itself is not a defect.

Therefore the open Tank watch is narrowed to:

```text
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
```

It asks only:
- does Tank displacement/control materially reduce wall pressure?
- do barriers / Iron Wall / slow materially protect the objective?
- does the class retain a credible survival/control specialty without requiring removal parity?

It does **not** ask:
- whether Tank kill throughput should match other classes;
- whether Tank should have the same clear rate on every encounter family;
- whether low removal should be repaired with ATK buffs.

P6-A already showed push/barrier/slow/Iron Wall are functional and materially protect the wall. That evidence remains valid.
The previous broader `TANK_MASTERY_PACKAGE_TO_OBJECTIVE_CONVERSION_WATCH` wording is therefore refined rather than treated as a damage-balance blocker.

No Tank scalar change is authorized.

---

## 2. P6-B1 question

P4 identified a structural feedback:

```text
more combat power
-> faster removal
-> fewer valid local timing turns
-> fewer later EXP opportunities
```

P5 added a shop that can alter player power and objective survival.
P4-E explicitly required remeasurement after shop integration.

P6-B1 asks a narrower causal question before exact skill-reach propagation:

> Holding the current late-run combat surface, SKILLED_V2 state, FORT/DEF shop ranks, class package, encounter, and run-state semantics fixed, how does the ATTACK component of the existing BALANCED shop snapshot alter valid timing-action opportunity and provisional XP_CREDIT?

This is an attribution probe, not a final shop policy test.

---

## 3. Exact execution

Temporary branch:

```text
timing-defense-workspace-temp-p6-shop-exp-opportunity
```

Source base:

```text
timing-defense-workspace-temp-p5p6-fidelity@0c334efed0af8ddcdef4eb93c34146ecfa7dadf5
```

Main B1 workflow:

```text
run 40029402035
job 120673610122
```

Result:

```text
SUCCESS
exact-byte repeat: PASS
SHA256: 83b5e1630231fb38426ae878cd3f2b6e7f3cd99894a44bac8416d0f23d614788
```

Cumulative cohort summary:

```text
run 40029618307
job 120674332432
SUCCESS
```

Diagnostic temp head after summary tooling:

```text
7d83360da97cf0add2256c0b391d1dac7e9cd9a6
```

No temp runner/workflow is promoted as production or canonical execution code by this result.

---

## 4. Paired design

### Skilled lane

```text
20 deterministic SKILLED_V2_CENTRAL seeds
× 5 classes
× 2 paired shop-ATK variants
= 200 late-run chains
```

Plus:

```text
1 ALL_PERFECT ceiling control
× 5 classes
× 2 variants
= 10 controls
```

Stage scope:

```text
46 -> 49
```

Paired variants:

```text
ATK_OFF
- keep existing BALANCED FORT rank
- keep existing BALANCED DEF rank
- force ATK rank = 0

ATK_ON
- existing BALANCED ATK/FORT/DEF diagnostic ranks
```

Held fixed:
- SKILLED_V2_CENTRAL sequence semantics;
- persistent combo/charge;
- Heavy X/Y consumes two judgments but remains one root action;
- P×P-only CRITICAL/Lv31 final semantics;
- current class packages;
- current diagnostic encounters;
- current right-edge entry;
- STAGE_SETTLED;
- wall current/max/absolute deficit carry;
- shop effect scale `0.40` as diagnostic only;
- entry charge `0` and entry combo boundary `0`, both already closed as primary late-run class-split causes.

Only the ATK component was isolated.
CRIT/CRITDMG/KNOCK are not represented in this cross-class P5 bridge and are not silently approximated.

---

## 5. EXP attribution semantics

The P4 methodology candidate was preserved exactly for diagnostic attribution:

```text
NORMAL   1.000
GOOD     1.500
PERFECT  2.250
HEAVY    1.250
HEAVY+   1.750
GREAT    2.250
SUPER    2.875
CRITICAL 3.500
```

Important:

```text
one valid completed root timing action
-> one XP_CREDIT award
```

A Heavy action consumes X/Y judgments but still contributes exactly one EXP award.

The bridge already records:
- `rootActions`;
- `judgmentsConsumed`;
- `heavyActions`;
- P×P/CRITICAL exposure;
- persistent charge/combo state.

P6-B1 only added judgment tracing and post-hoc tier reconstruction for attribution. Combat semantics were not changed.

These XP_CREDIT values remain provisional and are not numerically frozen.

---

## 6. Skilled survival / progression-extension effect

Through Stage49:

```text
ATK_OFF 17/100
ATK_ON  48/100
```

Paired outcome changes:

```text
survival promotions: 31
survival regressions: 0
```

Per class:

```text
Archer  5/20 -> 18/20  (+13 promoted pairs)
Knight  2/20 ->  5/20  (+3)
Mage    6/20 -> 18/20  (+12)
Rogue   4/20 ->  6/20  (+2)
Tank    0/20 ->  1/20  (+1)
```

Interpretation boundary:
- this is a severe late-run diagnostic surface;
- Tank low removal is intentional and this result does not authorize a Tank damage buff;
- this does not define desired class clear-rate parity;
- this only shows that shop ATK can prevent failure and therefore expose later timing actions that would otherwise never occur.

---

## 7. Clean within-stage opportunity compression

To isolate `faster removal -> fewer timing actions`, means use only paired Stage cases where **both ATK_OFF and ATK_ON settle that Stage**.

Overall:

```text
Stage46
root actions: 61.250 -> 59.531
compression: ~2.81%
XP_CREDIT:   141.635 -> 137.691
compression: ~2.78%
paired settled n=64

Stage47
root actions: 63.154 -> 60.154
compression: ~4.75%
XP_CREDIT:   149.216 -> 143.303
compression: ~3.96%
paired settled n=26

Stage48
root actions: 14.500 -> 12.423
compression: ~14.32%
XP_CREDIT:    31.534 -> 27.120
compression: ~14.00%
paired settled n=26

Stage49
root actions: 59.647 -> 57.235
compression: ~4.04%
XP_CREDIT:   142.404 -> 136.735
compression: ~3.98%
paired settled n=17
```

Stage48 must not be generalized because the current armored/proxy Stage48 packet remains diagnostic and unadopted.

Among ordinary late stages, the self-damping signal is generally low-single-digit overall on this diagnostic surface.

Class sensitivity is not equal.
Rogue shows the largest clean late opportunity compression among the classes with usable paired samples, roughly 7–8% on several stages.
Archer is near 1% or lower in the comparable surviving pairs.
This is descriptive, not a reason to apply class-specific EXP correction.

---

## 8. Cumulative cohort decomposition

### 8.1 Same-path cohort — both variants survive through Stage49

17 skilled pairs survive the whole Stage46–49 chain in both variants.

```text
ATK_OFF mean root actions = 194.941
ATK_ON  mean root actions = 186.765
net = -4.19%

ATK_OFF mean XP_CREDIT = 460.846
ATK_ON  mean XP_CREDIT = 442.904
net = -3.89%
```

This is the cleanest current cumulative late-run estimate of shop-ATK self-damping when survival-path truncation is removed.

Per class, both-through49 cohort:

```text
Archer n=5   root actions ~-0.92% / XP ~-0.82%
Knight n=2   root actions ~-4.24% / XP ~-3.94%
Mage   n=6   root actions ~-4.24% / XP ~-4.28%
Rogue  n=4   root actions ~-8.21% / XP ~-7.19%
Tank   n=0   no skilled pure-compression estimate
```

Tank n=0 is not interpreted as a role defect; the current late surface is removal-heavy and the Tank identity contract does not require removal parity.

### 8.2 Survival-promotion cohort

31 skilled pairs fail before Stage49 with ATK_OFF but survive through Stage49 with ATK_ON.

```text
ATK_OFF mean root actions = 116.323
ATK_ON  mean root actions = 196.194
net = +68.66%

ATK_OFF mean XP_CREDIT = 254.742
ATK_ON  mean XP_CREDIT = 434.020
net = +70.38%
```

This does **not** mean ATK increases XP per survived Stage.
It means ATK prevents a failure boundary, exposing later Stages and therefore creating additional future timing opportunities.

### 8.3 All 100 paired skilled cases, including survival extension

```text
ATK_OFF mean root actions = 104.660
ATK_ON  mean root actions = 139.440
net = +33.23%

ATK_OFF mean XP_CREDIT = 235.430
ATK_ON  mean XP_CREDIT = 311.989
net = +32.52%
```

This aggregate is outcome-conditioned and must not be used as a per-Stage EXP multiplier.

---

## 9. ALL_PERFECT ceiling control

All five classes survive through Stage49 in both variants.
Therefore survival-extension contamination is absent in this small ceiling control.

Cumulative:

```text
root actions: 190.4 -> 184.2   (~-3.26%)
XP_CREDIT:   487.9 -> 471.7   (~-3.32%)
```

This independently preserves the expected self-damping direction when both paths complete.

---

## 10. P6-B1 causal conclusion

The prior one-direction shorthand:

```text
more shop power -> fewer timing turns -> less EXP
```

is incomplete once run failure/progression is modeled.

Current evidence requires:

```text
shop ATK
├─ faster removal inside a survived Stage
│  -> fewer valid timing actions
│  -> less EXP opportunity
│  -> SELF-DAMPING PATH
│
└─ stronger objective survival / deeper progression
   -> additional later Stages become reachable
   -> more valid timing actions become available
   -> more total EXP opportunity
   -> SURVIVAL-EXTENSION PATH
```

Therefore:

```text
SHOP_ATK_TO_EXP_FEEDBACK = BIDIRECTIONAL / OUTCOME-CONDITIONED
```

and specifically:

```text
SHOP_POWER_DOES_NOT_SUPPORT_A_MONOTONIC_GLOBAL_EXP_DELAY_ASSUMPTION
```

Any future full-run skill-reach model must represent both paths instead of applying a flat negative EXP multiplier from shop power.

---

## 11. What B1 does NOT prove

B1 does not prove:
- exact Lv6/Lv11/Lv16/Lv21/Lv26/Lv31 reach shifts;
- that Lv31 should move from the user-confirmed 41–45 target;
- that current shop ATK effect scale should be adopted;
- that BALANCED is the final purchase policy;
- that all shop categories have the same feedback sign/magnitude;
- that Stage48 proxy content belongs in Tier1;
- that Tank requires more damage;
- that class-specific EXP correction is needed;
- that current late clear rates should be equalized;
- any production gameplay value.

Reasons exact skill reach remains open:
- this slice starts after Lv31 is assumed available;
- fixed late shop ranks are not Stage1–45 purchase history;
- exact Tier1 Stage1–50 authoring is intentionally not yet frozen;
- only ATK/FORT/DEF are currently safe in the shared P5 cross-class bridge;
- P4 XP_CREDIT numbers remain provisional;
- the historical P4-B combat-feedback result was retained as result data/report, but no reproducible P4-B runner is present in the historical canonical tree.

---

## 12. Historical P4-B reproducibility audit

P4-B result data was introduced by:

```text
c32dfd9dd45eaeec01ab53ea0cdafc3fd6233c7c
```

The historical tree at that point contains:
- `data/p4b_combat_feedback_divergence_v0_1.json`;
- P4-A inverse-design runner/validator;
- P3 kernel;
- prior combat/role simulators.

It does **not** contain a dedicated reproducible P4-B propagation runner.
The following commit added the P4-B report, not a runner.

Therefore P6 must not silently reconstruct exact skill-reach shifts by inventing a linear mapping from:
- nominal shop ATK%;
- the current Stage46–49 ~4% clean opportunity compression;
- or the old P4-B median action ratios.

P5 already showed ATK can change kill order / chronology nonlinearly.

---

## 13. B2 decision boundary

P6-B1 is complete.
The next unresolved question is:

> What bounded, reproducible model should be authorized to estimate **Stage1–45 shop-history × skill-power × combat-opportunity × EXP × skill-reach** before exact Tier1 Stage1–50 content is authored?

Legitimate methods include, but are not yet adopted here:

### B2-A — rebuild/recover a bounded P4-B-style synthetic combat-feedback runner, then inject P5 stage-by-stage shop trajectories
Pros:
- closest continuity with old P4-B evidence;
- can remain independent of final exact Tier1 authoring.

Risk:
- old P4-B runner was not retained, so reconstruction requires an explicit methodology contract and fidelity checks.

### B2-B — first author a provisional full Stage1–50 combat fixture and run actual shop/EXP jointly
Pros:
- more direct combat chronology.

Risk:
- violates the current approved dependency ordering if it effectively freezes Tier1 content before P6 convergence / Tier unlock work.

### B2-C — stop exact skill-reach propagation now and carry the feedback watch until later exact authoring
Pros:
- no synthetic assumption introduced.

Risk:
- leaves P6 progression convergence unresolved before Tier/unlock authoring.

No B2 method is selected by this document.

**Decision is required before adopting a new synthetic propagation method.**

---

## 14. Current boundary

Closed:

```text
P6-B1_ATK_COMPONENT_ATTRIBUTION = COMPLETE
SHOP_ATK_WITHIN_STAGE_SELF_DAMPING = CONFIRMED
SHOP_ATK_SURVIVAL_EXTENSION_PATH = CONFIRMED
SHOP_ATK_EXP_FEEDBACK = BIDIRECTIONAL / OUTCOME-CONDITIONED
TANK_LOW_REMOVAL_BY_ITSELF = NOT_A_DEFECT
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH = ACTIVE_NARROW_WATCH
```

Open:

```text
P6-B2 exact/provisional progression-relevant skill-reach propagation methodology
```

No final EXP rule, shop coefficient, class coefficient, Tank scalar, encounter packet, Tier count, monster unlock ladder, or production change is authorized.