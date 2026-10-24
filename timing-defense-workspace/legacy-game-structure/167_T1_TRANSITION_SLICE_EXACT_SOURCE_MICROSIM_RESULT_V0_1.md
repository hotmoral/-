# 167 — T1 Transition Slice Exact-Source Micro-Sim Result v0.1

Status: **EXACT-SOURCE ADMISSION PASS / ONE RUNNER LIFECYCLE DEFECT FOUND+CORRECTED / REPRESENTATIVE PRESSURE UNDERSHOOT / NO PRODUCTION FREEZE**

## 1. Scope

This report closes the exact-source execution required by `165` and `166` for the bounded T1 representative transition recipes only:

```text
A Stage5 RUNNER teach × Lv6 OFF/ON
B Stage18 BRUTE first mix × Lv16 OFF/ON
C Stage20->23 sequential
D Stage39->45 sequential / Lv31 before 41, 43 or 45
E Stage46->50 sequential / Lv31 active
```

It does not authorize:
- a full Stage1-50 exact recipe freeze;
- production monster/shop/EXP/P×P scalar changes;
- class buffs/nerfs;
- Tank damage normalization;
- production gameplay changes.

Compact machine-readable summary:
`data/t1_transition_slice_exact_source_microsim_summary_v0_1.json`

---

## 2. Exact execution evidence

Final admitted run:

```text
workflow run = 40074583842
job = 120815112194
artifact = 12552383686
head SHA = 61a4dc2fbef1bcf9bf6c48bee857bdbf2304d0d3
artifact ZIP SHA256 = 368d51ae76a45fd4b2fcbfb9e794246ace508e6a975b54a9f286a05e5fb36227
recipe source SHA256 = afd4c57e94ea797ab14954f67ecc576b202eeed4ca953162e0080892db1083a7
seeds = 101 / 211 / 307
```

Final admission:

```text
exactRecipeIdentity = PASS
stageSettledOrTerminalFailure = PASS
noEnemyCarryAtSettledBoundary = PASS
noTransientLeakageAtSettledBoundary = PASS
persistentStateContinuity = PASS
deterministicReplay = PASS
pairedIsolation = PASS
explicitSkillStateTrace = PASS
lifecycleFailures = 0
pairFailures = 0
replayFailures = 0
```

Therefore combat output from the corrected runner is admissible as bounded diagnostic evidence.

---

## 3. Important runner defect found before balance interpretation

The first exact-source run (`40074386004`) appeared to pass all automated admission gates, but manual causal review found a concrete anomaly:

```text
Stage18 / Tank / Lv16 ON
settled about exactly 3 seconds later than OFF
with no meaningful removal difference
```

Root cause was not balance.

The original runner's `stage_settled()` waited for:
- Stage-local `wallShield` to expire;
- Stage-local `Aftershock` zones to expire.

That conflicts with approved lifecycle authority:
- Stage-local temporary effects clear at `STAGE_SETTLED`;
- Lv26 Aftershock explicitly expires at timer end **or STAGE_SETTLED, whichever is earlier**.

Thus the first run is classified:

```text
FALSE_PASS_SETTLEMENT_ORDERING
NO_BALANCE_INTERPRETATION_FROM_INITIAL_RUN
```

Minimal fidelity bridge:
`tools/run_t1_transition_slice_microsim_settlement_fix_v0_1.py`

Corrected behavior:
- authored spawns must be complete;
- zero live enemy required;
- delayed combat-event queue must drain;
- Stage-local passive residue such as shield/Aftershock is cleared at the Stage boundary rather than holding an empty Stage open.

The corrected exact-source rerun passed all gates.

This is an example of the required review philosophy working as intended: lifecycle defect was corrected before any scalar or class conclusion.

---

## 4. Group A — Stage5 RUNNER teach × Lv6

All classes / all seeds:

```text
outcome = STAGE_SETTLED
wall damage = 0
wall reserve = 2000 diagnostic sentinel
```

Mean settled time, OFF -> ON:

```text
Archer 5.100 -> 4.367 s
Knight 5.100 -> 5.100 s
Mage   5.100 -> 5.100 s
Rogue  5.100 -> 4.188 s
Tank   5.100 -> 5.100 s
```

Interpretation:
- Lv6 does not globally erase the RUNNER teach;
- Rogue and Archer shorten the interaction modestly;
- Tank changes control/knockback, not removal time;
- Knight/Mage do not cross a meaningful breakpoint in this sparse teach recipe.

Decision:

```text
T1_RUNNER_LV6_PEDAGOGIC_COLLISION_WATCH = remains WATCH, not FAIL
```

Do not increase RUNNER HP merely to make every class show the same OFF/ON delta.

---

## 5. Group B — Stage18 BRUTE first mix × Lv16

All classes / all seeds:

```text
outcome = STAGE_SETTLED
wall damage = 0
```

Mean settled time, OFF -> ON:

```text
Archer 10.633 -> 8.433 s
Knight  9.900 -> 9.533 s
Mage   10.267 -> 7.453 s
Rogue  11.073 -> 10.648 s
Tank   17.233 -> 17.233 s
```

BRUTE/frontline dwell changes are strongest for Archer and Mage:

```text
Archer frontline block 6.378 -> 3.717 s
Mage   frontline block 5.882 -> 4.115 s
```

Interpretation:
- Lv16 clearly changes the first-mix reading for Archer and Mage;
- however BRUTE is not instant-erased and the Stage still consumes multiple timing actions;
- Knight/Rogue changes are modest;
- Tank Lv16 does not alter removal chronology in a no-wall-contact Stage after the settlement correction.

Decision:

```text
T1_BRUTE_LV16_CALIBRATION_COLLISION_WATCH = MATERIAL / causal trace review retained
not yet AUTHORING_FAIL
```

The correct next question is whether BRUTE role readability is too short for Archer/Mage, not whether those classes should be nerfed.

---

## 6. Group C — Stage20->23 gate / first high-pressure ramp

All 5 classes × 3 seeds × all four Stages:

```text
STAGE_SETTLED = all
wallDamage > 0 rows = 0
```

Mean settled times by class:

```text
Stage20: Archer10.267 Knight10.633 Mage10.420 Rogue12.022 Tank18.333
Stage21: Archer 4.400 Knight 4.767 Mage 3.847 Rogue 5.522 Tank 8.433
Stage22: Archer 7.433 Knight 8.433 Mage 7.880 Rogue 9.280 Tank16.867
Stage23: Archer 7.333 Knight 6.967 Mage 7.880 Rogue 9.280 Tank16.500
```

Stage21 is labeled RUNNER first high pressure but is dynamically among the shortest Stages in the slice.

Interpretation:
- the intended vocabulary contrast is visible;
- but the authored pressure envelope is too short/light to create objective pressure under the current diagnostic anchors;
- Tank's longer removal time is acceptable identity evidence, not a kill-parity failure;
- no class reaches a wall-pressure decision at all.

Classification:

```text
STAGE20_23_REPRESENTATIVE_PRESSURE_CAPACITY = UNDERSHOOT_CANDIDATE
```

Repair should begin with composition/chronology/cadence/overlap, not scalar inflation.

---

## 7. Group D — Stage39->45 / 2-star gate and Lv31 acquisition runway

Every row across:
- five classes;
- three seeds;
- three Lv31 activation-position variants;
- seven Stages;

settled successfully.

```text
rows = 315
wallDamage > 0 rows = 0
```

Dynamic Stage-shape means across activation variants:

```text
Stage39 mean settled 12.506 s / mean peak active 4.267
Stage40 mean settled  7.114 s / mean peak active 4.067
Stage41 mean settled  7.608 s / mean peak active 1.733
Stage42 mean settled  6.090 s / mean peak active 2.222
Stage43 mean settled  5.702 s / mean peak active 3.133
Stage44 mean settled  4.945 s / mean peak active 4.400
Stage45 mean settled  7.436 s / mean peak active 3.289
```

Important positive result:

```text
Stage39 -> Stage40 -> Stage41 mean peak active
4.267 -> 4.067 -> 1.733
```

Therefore the intended Stage41 acquisition relief is dynamically visible as a large concurrency reduction, not only as a static density label.

Lv31 activation before Stage41 / 43 / 45 changes class-specific chronology, but does not create any wall-risk distinction in the current recipe set because all variants remain far from objective pressure.

Interpretation:
- macro shape / relief direction = supported;
- pressure capacity = too weak to calibrate acquisition fairness or mastery tension.

Classification:

```text
STAGE41_RELIEF_SHAPE = SUPPORTED
STAGE39_45_OBJECTIVE_PRESSURE_CAPACITY = UNDERSHOOT_CANDIDATE
LV31_REACH_POSITION_BALANCE_INFERENCE = PREMATURE
```

---

## 8. Group E — Stage46->50 post-Lv31 mastery/final

All five classes × three seeds × all five Stages:

```text
STAGE_SETTLED = all
wallDamage > 0 rows = 0
final wall reserve = full diagnostic sentinel in every case
```

Mean settled times:

```text
Stage46: Archer7.700 Knight9.580 Mage8.493 Rogue9.508 Tank12.467
Stage47: Archer6.967 Knight6.280 Mage5.860 Rogue5.515 Tank 6.233
Stage48: Archer4.033 Knight4.540 Mage3.660 Rogue4.305 Tank 4.400
Stage49: Archer7.700 Knight7.840 Mage8.060 Rogue5.000 Tank 9.900
Stage50: Archer7.700 Knight4.400 Mage3.660 Rogue3.775 Tank 9.900
```

This conflicts directionally with the already-approved Stage46+ mastery-gate intent in `91`:
- Stage46 should be a major pressure-regime step-up;
- Lv31/P×P mastery should be functionally meaningful for survival/pressure management;
- Stage48-49 should create meaningful mastery pressure;
- Stage50 should apply the whole learned kit rather than collapse into a very short cleanup for several classes.

The current representative recipes do not provide enough pressure capacity to test that contract.

Classification:

```text
STAGE46_50_MASTERY_PRESSURE_CAPACITY = CLEAR UNDERSHOOT
```

This is an encounter-authoring finding, not a class-balance finding.

---

## 9. Cross-slice conclusion

The exact-source execution supports two separate statements at once:

### Structural shape is generally readable
- Stage5 RUNNER teach exists;
- Stage18 BRUTE mix persists long enough to observe, though Archer/Mage Lv16 compression is material;
- Stage39->41 relief shape is visible;
- class identities produce different removal/control chronologies.

### Pressure capacity is insufficient
Across Groups C/D/E:

```text
wall-damage rows = 0
```

Therefore current representative recipes cannot yet answer:
- intended soft-wall strength;
- wall-reserve attrition;
- Tank objective-protection value under actual danger;
- Stage46+ mastery-pressure adequacy;
- Lv31 reach-position fairness under pressure.

A recipe that never threatens the objective cannot validate those dimensions.

---

## 10. Repair order

Do **not** start by raising monster HP/damage globally.

Bounded repair order:

```text
1. composition
2. chronology / spawn ordering
3. cadence
4. bounded overlap / pulse length
5. formation geometry
6. exact scalar sensitivity last
```

Constraints to preserve:
- T1 roster remains GRUNT/RUNNER/BRUTE only;
- no new ordinary mechanic Stage41-50;
- Stage41 remains explicit relief;
- Stage20/40 reward boundaries do not become arbitrary difficulty cliffs;
- Stage46+ should become a genuine mastery pressure regime;
- no class parity forcing;
- Tank kill parity not required;
- right-edge spawn / no midfield pop-in;
- authored 4s density guard must be rechecked after any repair;
- do not expand to full 50-Stage exact authoring yet.

---

## 11. Exact next bounded work

Create a **representative pressure-shape revision only** for the affected diagnostic neighborhoods:

```text
C: Stage20-23
D: Stage39-45, preserving Stage41 relief
E: Stage46-50
```

Stage5 remains unchanged for now.

Stage18 should remain unchanged while Archer/Mage Lv16 causal trace/readability is inspected; do not confound the collision question with a simultaneous recipe rewrite.

After candidate pressure-shape revision:
1. static density/signature audit;
2. exact-source rerun through the corrected settlement bridge;
3. compare objective pressure, chronology and class-opportunity dimensions;
4. scalar sensitivity only if composition/cadence/geometry cannot produce the required pressure.

---

## 12. Decision state

```text
exactCanonicalSourceExecution = COMPLETE
runnerAdmission = PASS_AFTER_SETTLEMENT_FIDELITY_CORRECTION
initialExactRun = SUPERSEDED_FALSE_PASS_SETTLEMENT_ORDERING
Stage5Lv6Collision = WATCH_NOT_FAIL
Stage18Lv16Collision = MATERIAL_WATCH
Stage41ReliefShape = SUPPORTED
Stage20_23PressureCapacity = UNDERSHOOT_CANDIDATE
Stage39_45PressureCapacity = UNDERSHOOT_CANDIDATE
Stage46_50MasteryPressureCapacity = CLEAR_UNDERSHOOT
fullT1ExactRecipeFreeze = DEFERRED
productionNumericalFreeze = NO
productionGameplayChange = UNAUTHORIZED
```
