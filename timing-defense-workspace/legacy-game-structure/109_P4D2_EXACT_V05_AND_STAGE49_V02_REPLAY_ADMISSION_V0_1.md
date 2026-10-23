# Timing Defense — P4-D2 Exact v0.5 + Stage49 v0.2 Replay Admission V0.1

Date: 2026-10-23 KST  
Status: **EXACT LIVE-BLOB REPLAY ADMITTED / DIRECTIONAL STAGE49 RESULT CONFIRMED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Authority / context:
- `99_P4D2_TEMPORAL_CADENCE_FIDELITY_REVIEW_V0_1.md`
- `103_P4D2_TANK_BARRIER_FIDELITY_CORRECTION_V0_1.md`
- `105_P4D2_V03_REPLAY_FAILURE_AND_V04_RUNNER_CORRECTION_V0_1.md`
- `106_P4D2_STAGE49_FULL_ROTATION_DIRECTIONAL_PROBE_V0_1.md`
- `107_P4D2_ARCHER_SPLITTER_CHRONOLOGY_ROOT_CAUSE_V0_1.md`
- `108_P4D2_STAGE46_LV31_ACQUISITION_FAIRNESS_PRECHECK_V0_1.md`
- `data/p4d2_v05_and_stage49_v02_exact_replay_admission_v0_1.json`

---

# 0. Purpose

The prior full-rotation result was intentionally directional because the exact fidelity runner chain had not yet completed a committed-byte replay admission.

This document closes that methodology gap.

The exact replay was executed from files reconstructed from the **live remote Git blobs** and independently checked with `git hash-object` before execution.

This is stronger than a hand-retyped/local-equivalent reconstruction:
- every admitted source/fixture byte matched the live Git blob SHA;
- the committed replacement runners were then re-fetched and their remote blob SHAs matched the executed local bytes.

---

# 1. Runner correction history

```text
v0.2
= pre-Tank-barrier-correction historical evidence

v0.3
= FAIL_SOURCE_PATCH_GUARD
  assumed two shield-consumption sites had identical indentation

v0.4
= FAIL_SUBSTRING_PATCH_GUARD
  the 16-space wall token also matched as a substring inside the 20-space SIEGER line

v0.5
= PASS
  each absorb site anchored by preceding newline + exact indentation
```

The v0.4 failure was discovered by executing the exact live Stage46 blob, not by balance interpretation.

No gameplay rule changed between the intended v0.3/v0.4 correction and v0.5. The change is only source-guard fidelity.

---

# 2. Exact v0.5 dynamic-grammar admission

Executed live-byte identities:

```text
Stage46 kernel
5965833f80422bd6cae94fea738706baf99a06e8

v0.2 wrapper
aef5f348a089795c04b48d8ef6f9267d9726c504

v0.5 fidelity runner
8a548184272a71f3b17650f77e6d366533409e0c

base fixture
035f11f07e1b5f35d8ca5a73511bad92e065889c

grammar fixture
5d7a7d928242be1275474bf56ed86f1475e2c845
```

Full deterministic output SHA-256:

```text
29c5c7dc5a6c74f1e67f07d7eb0d8a3235e860817d7559227da26da192e2dae1
```

Primary all-success wall results:

```text
Knight 895
Rogue recovered-78ms lane 1850
Tank 2000
Archer 1575
Mage 2000
```

Tank barrier-corrected two-consecutive-miss range across four grammar starts:

```text
1857 .. 1981
```

This confirms that Tank's larger immediate mistake budget was not an artifact of the previous barrier downgrade bug.

---

# 3. Exact Stage49 full-rotation v0.2 admission

The original Stage49 v0.1 runner imported v0.4, so it is not executable after the v0.4 guard failure.

A v0.2 runner was created with **only the fidelity dependency moved to v0.5**.
The encounter fixture is unchanged.

Exact source identities:

```text
Stage49 v0.2 runner
1eb644766133d0a4e84130ab4d7be4c727cbee12

Stage49 fixture v0.1
d430fdcc43fc356b849083d7f31b01e1c2f5690d

v0.5 fidelity runner
8a548184272a71f3b17650f77e6d366533409e0c
```

Full deterministic output SHA-256:

```text
c033d7fea455476ae2c4b9c0ffe4f770885d135533fd899a04709eb7cd0d6e02
```

The exact replay reproduces the previously published directional Stage49 result.

## All-success

```text
Knight 1705
Rogue  2000
Tank   2000
Archer 2000
Mage   2000
```

## All finals missed

```text
Knight 34.025s burial
Rogue  29.100s burial
Tank   34.575s burial
Archer 57.025s burial
Mage   52.225s burial
```

## First burial under consecutive misses

```text
Knight: LINE4 / CLUSTER4 / FRONTLINE3 / DURABLE6 / TIME_BUDGET4
Rogue : LINE3 / CLUSTER4 / FRONTLINE4 / DURABLE3 / TIME_BUDGET3
Tank  : LINE6 / CLUSTER6 / FRONTLINE5 / DURABLE5 / TIME_BUDGET4
Mage  : TIME_BUDGET8; other starts survive the bounded 8-miss sweep with severe reserve loss
Archer: no burial inside the bounded 8-miss sweep, but several Stage50 reserve states are severe
```

One/two-miss full-rotation suites produced no success-monotonicity watch for any class.

---

# 4. Structural interpretation

The exact admission supports all of the important directional claims from document106:

```text
ALL_FIVE_ALL_SUCCESS_SURVIVE = YES
ALL_FIVE_ALL_FINALS_MISSED_BURY = YES
ONE_ISOLATED_MISS_RECOVERABLE = YES in the bounded Stage49 candidate
TANK_TIME_BUDGET_IDENTITY = PRESERVED
MAGE_CLUSTER_RECOVERY = PRESERVED
ROGUE_RECOVERED_CADENCE = PRESERVED
ARCHER_FULL_ROTATION_ONE_TWO_MISS_MONOTONICITY_ISSUE = NOT OBSERVED
```

It does **not** freeze:
- exact Stage49 authoring;
- exact mistake budgets;
- exact wall-reserve floor;
- durable proxy stats;
- Lv31 class coefficients;
- final EXP semantics.

---

# 5. Remaining watches after exact admission

Exact replay is no longer a P4-D2 blocker.

Still active:
- `STAGE49_TO_50_WALL_RESERVE_CONTINUITY_WATCH`;
- Archer SPLITTER chronology as an **explained authoring watch**, not a skill-power defect;
- Stage46 Lv31 acquisition fairness, numerically deferred to P10R under R2;
- multiplayer Rogue event-volume/performance watch;
- final multiplayer/timebase EXP watches.

---

# 6. P4-D2 closure implication

With exact replay admitted, the remaining open items are no longer unresolved P4-D2 structural design blockers:

- Archer chronology root cause is explained and has an authoring safeguard;
- Stage46 acquisition fairness is explicitly outside P4-D2 numerical freeze authority under approved R2 routing;
- Stage49->50 wall reserve is a downstream authoring/calibration watch rather than a missing class-mechanic contract.

Therefore P4-D2 is eligible for **provisional structural closure with watches**, subject to a final cross-stage closure review.
