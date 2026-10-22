# Timing Defense — P3 Ten-Stage Persistent Run Execution Report V0.1

Date: 2026-10-23 KST  
Status: **P3 STRUCTURAL PASS / 30 OF 30 PRIMARY / 8 OF 8 TARGETED / NOT BALANCE CALIBRATION**

Depends on:
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `75_TEN_STAGE_PERSISTENT_RUN_KERNEL_PROPOSAL_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`

Machine-readable inputs/evidence:
- `data/p3_persistent_run_kernel_contract_v0_1.yaml`
- `data/p3_ten_stage_fixture_v0_1.json`
- `data/p3_execution_summary_v0_1.json`
- `../tools/run_p3_persistent_kernel_v0_1.py`
- `../tools/validate_p3_persistent_kernel_v0_1.py`

---

# 0. Admission question

Can the approved P1 run-state lifecycle and P2 modifier/attribution semantics survive a deterministic multi-Stage run without hidden Stage resets, player-model reseeding, snapshot divergence, temporary-effect leakage, failure/retry defects, or attribution ambiguity?

Result:

**YES for the approved bounded P3 structural scope.**

This result does not establish:
- final EXP or Lv6 reach;
- final Base HP;
- production difficulty or clear rate;
- exact T1 Stage1–10 content;
- shop/economy values;
- permanent progression;
- boss behavior;
- multiplayer scaling/progression.

---

# 1. Exact executed canonical inputs

The final accepted execution used byte-identical local copies of the canonical files below.

Git blob SHAs:

```text
runner
  tools/run_p3_persistent_kernel_v0_1.py
  a9395716166185dd253685991a074dfdac3bf3c7

validator
  tools/validate_p3_persistent_kernel_v0_1.py
  f7f4d183c58220435bb7d33aa7add58dd858023b

fixture
  legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json
  cf809f34991fabd94037a8f5a3205731b3447451
```

Machine-readable execution summary currently has repository blob SHA:

```text
dfc41367ae756d55496e05a9bdcca9f5a732e61b
```

The fixture pins only the P3-required subset of already-existing candidate/reference inputs:
- E01 baseline recipe;
- E02 rush recipe;
- GRUNT/RUNNER movement anchors;
- GRUNT/RUNNER HP/wall-damage anchors;
- provisional streak-aware `SKILLED_V2_CENTRAL` state model;
- current Lv6/N3 structural behavior required for plumbing tests.

The kernel is intentionally a **bounded structural integration kernel**, not a replacement for the full Layer-A role simulator. Geometry-sensitive Lv6 secondary targeting in this first-10 fixture is used only to prove effect-path activation and attribution; P3 does not claim production class-balance parity from this kernel.

---

# 2. Primary execution matrix

Approved matrix:

```text
5 classes
× 3 base seeds [101, 211, 307]
× 2 lanes [LV1_CONTINUITY, FORCED_LV6_TRANSITION]
= 30 persistent 10-Stage runs
```

Final result:

```text
primary runs                     30 / 30 PASS
10 Stage settlements             30 / 30 PASS
deterministic replay             30 / 30 PASS
continuous player-model stream   30 / 30 PASS
LV1 lane Lv6 attribution          0 unexpected entries
forced-Lv6 lane attribution      positive in every class/seed lane
```

The primary lane uses:
- test-only Base HP sentinel `100000`;
- no exact EXP formula;
- no real shop/economy;
- Stage6 forced Lv6 only in the dedicated transition-plumbing lane;
- current `1100ms` action interval only as `BOUNDED_CURRENT_MECHANIC_SIMULATION_CONTROL_NOT_SKILL_FIT`.

No primary-run clear percentage is admitted as difficulty evidence.

---

# 3. Lv6 attribution evidence

Across the 15 forced-Lv6 primary runs, the validator found the following Level-effect attribution-entry counts:

```text
Knight  208
Rogue    90
Tank    209
Archer  116
Mage     96
```

Interpretation:
- every class activated an authorized Lv6 effect path after the Stage6 test hook;
- the LV1 lane produced no Lv6 attribution;
- this proves transition/plumbing separation;
- these counts are **not** relative skill-power measurements because encounter geometry, action count and effect multiplicity differ by class.

No actual Lv6 reach claim is made.
P4 retains authority for EXP/skill-reach calibration.

---

# 4. Player-model continuity

The P3 run owns one `SKILLED_V2_CENTRAL` player-model state/RNG stream for the whole Tier attempt.

For every Stage boundary the validator checked:

```text
nextStage.judgmentRngStart == previousStage.judgmentRngEnd
nextStage.expEligibleEventsStart == previousStage.expEligibleEventsEnd
```

Result:

```text
30 / 30 primary runs continuous
```

Therefore the earlier all-20 short-prefix reseeding defect is not reproduced in the persistent-run kernel.

`COMBAT_PROC` has a separate deterministic seed domain so future proc draws do not need to move the judgment stream.

---

# 5. Combo / charge / N3 continuity

Targeted fixtures crossed actual `STAGE_SETTLED` boundaries.

## F1 — CHARGE_CONTINUITY
PASS.

A preserved ready-charge state survived Stage settlement and the next valid attack consumed the Heavy path rather than silently resetting charge.

## F2 — COMBO_N3_BOUNDARY
PASS.

Combo `4` survived Stage settlement; the next PERFECT crossed the combo-5 milestone and triggered the existing N3 path.

This verifies that Stage transition is not an implicit combo/N3 barrier.

### Long-run combo diagnostic

All 30 primary synthetic runs reached combo40 at least once.

```text
combo40 observed = 30 / 30
```

This is useful structural evidence that persistent Stage continuity does not make combo40 impossible.
It is **not** a production probability/frequency target because:
- the player model remains a provisional design prior;
- the fixture is synthetic;
- no fitted encounter-context degradation is active;
- the Stage slice is deliberately long enough to exercise persistent state.

---

# 6. Failure / retry

## F3 — FAILURE_RETRY_RESET
PASS.

The fixture used deliberately low test Base HP and a test-only damage-suppression modifier so a real monster wall hit caused attempt failure.

After retry, P1 reset semantics were verified:

```text
Stage     -> 1
Level     -> 1
EXP       -> 0
Run coin  -> 0
Shop rank -> empty
Combo     -> 0
Charge    -> 0
Base HP   -> fresh-attempt full sentinel
```

Account-permanent sentinel state remained unchanged.

The low HP and suppression modifier are test controls only.

---

# 7. Snapshot / resume

## F4 — SNAPSHOT_RESUME_EQUIVALENCE
PASS.

Two boundaries were tested:
1. inter-Stage snapshot after Stage5;
2. mid-Stage snapshot after the player-model stream had already advanced.

In both cases, restored execution matched uninterrupted deterministic execution under the kernel hash comparison.

This is simulator-level state-serialization evidence only.
It does not choose production storage technology, retention, reconnect timeout or multiplayer host migration.

---

# 8. P2 modifier and attribution integration

## F5 — MODIFIER_AGGREGATION_ATTRIBUTION
PASS.

Test-only attack modifiers:

```text
ACCOUNT          +10%
CLASS_PERMANENT  +20%
RUN              +30%
```

were processed through the approved same-stat additive bucket.
For a base value 100, the structural test result was:

```text
100 × (1 + .10 + .20 + .30) = 160
```

The realized attack ledger retained all three source IDs separately.

This validates P2 operation semantics and source attribution.
The `10/20/30%` values are test sentinels and are not reward/shop candidates.

---

# 9. Temporary-effect and Stage settlement boundary

## F6 — TEMPORARY_EFFECT_BOUNDARY
PASS.

A Stage-local temporary effect was present before settlement and absent afterward.

## F7 — NO_TRANSIENT_LEAKAGE
PASS.

A newly initialized next Stage contained no stale:
- enemy instance;
- pending queue;
- Stage-local temporary object;
- prior Stage clock/index state.

The kernel drains already-authorized queued effects before `STAGE_SETTLED`, then clears ordinary Stage-local temporary state.
Combo, charge, Base HP and persistent run state are not cleared by this barrier.

No simultaneous final-clear/Base-HP-zero collision occurred, so its precedence remains an OPEN decision exactly as approved.

---

# 10. Base HP attrition continuity

The primary fixture intentionally produced no wall damage because it is an integration lane, not a difficulty lane.
That is not used as evidence that wall pressure is correct.

A separate additional diagnostic was therefore added.

## F8 — BASE_HP_ATTRITION_CONTINUITY
PASS.

Test-only setup:
- Base HP sentinel = `5000`;
- attack PCT_ADD test modifier = `-0.99`, only to force wall contacts without changing monster anchors.

Observed:

```text
start              5000
after first Stage  4490
after next Stage   3980
```

Most importantly:

```text
nextStage.baseHpStart == previousStage.baseHpEnd
```

and ledger HP damage reconciled with the Base HP delta.

The values `5000`, `-0.99`, `4490`, and `3980` are structural test evidence only and carry no balance authority.

---

# 11. Final validator result

Byte-identical canonical runner/validator/fixture execution:

```json
{"recordType":"P3_VALIDATION","result":"PASS","errors":[],"primaryRuns":30,"targetedFixtures":8,"lv6AttributionByClass":{"knight":208,"rogue":90,"tank":209,"archer":116,"mage":96},"combo40ObservedRuns":30,"warning":"Structural test only; no balance number frozen."}
```

Final P3 classification:

```text
P3_STRUCTURAL_PASS
```

---

# 12. What P3 proved

P3 now provides executable evidence for:
- deterministic ten-Stage state continuity;
- Base HP persistence plumbing;
- combo persistence;
- charge/Heavy persistence;
- N3 milestone continuity;
- failure/retry reset semantics;
- inter-Stage and mid-Stage snapshot/resume equivalence;
- continuous player-model RNG ownership;
- forced Lv6 Level/effect activation and attribution for all five classes;
- P2 same-stat additive aggregation;
- Power Attribution source traceability;
- Stage-local temporary-effect clearing;
- StageState/transient non-leakage.

---

# 13. What remains explicitly unproved/open

P3 does not prove or decide:
- final EXP formula;
- Lv6 actual Stage distribution;
- Lv11/16/21/26/31 reach;
- exact Base HP;
- real wall-pressure difficulty;
- shop cadence/price/value;
- exact coin economy;
- production clear/fail rates;
- exact T1 Stage1–10 authoring;
- Stage10 boss design;
- permanent star/achievement values;
- multiplayer scaling/credit;
- production persistence implementation;
- simultaneous terminal collision precedence.

These remain downstream decision/calibration work.

---

# 14. Closure and next boundary

P3 exit conditions are satisfied for the approved structural scope.

Therefore:

```text
P3 TEN_STAGE_PERSISTENT_RUN_KERNEL
= STRUCTURAL COMPLETE / PASS
```

Next work package:

```text
P4 FULL_PLAYER_POWER_SPINE_CANDIDATE
```

P4 must analyze and propose a provisional 50-Stage EXP/skill-reach model under shop-neutral / P0-permanent-power conditions.
It must preserve:
- Lv31 target window Stage41–45 as user-confirmed direction;
- Lv6/11/16/21/26 windows as calibration candidates until evidence/approval;
- no exact launch Stage authoring;
- no final shop or permanent-power tuning.

Material P4 numerical/design decisions require analysis -> recommendation -> user approval before closure.
