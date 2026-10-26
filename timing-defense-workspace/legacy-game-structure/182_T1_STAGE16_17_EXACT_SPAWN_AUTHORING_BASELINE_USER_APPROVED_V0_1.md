# Timing Defense — T1 Stage16–17 Exact Spawn Authoring Baseline User Approved V0.1

Date: 2026-10-26 KST  
Status: **USER APPROVED AUTHORING BASELINE WITH WATCHES / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `180_T1_WAVE_A_EXACT_SPAWN_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`
- `181_T1_CONTIGUOUS_15_25_B1_DYNAMIC_ADMISSION_AND_CLOSURE_V0_1.md`
- `data/t1_contiguous_15_25_b1_stage16_17_candidate_v0_1.yaml`

---

# 0. User decision

On 2026-10-26 KST the user explicitly approved the Stage16 and Stage17 exact spawn candidates as canonical T1 authoring baseline WITH WATCHES.

Approved decision:

```text
ADOPT_STAGE16_17_AS_CANONICAL_T1_AUTHORING_BASELINE_WITH_WATCHES
```

This approval closes:

```text
T1_B1_STAGE16_17_AUTHORING_ADOPTION_DECISION_GATE
```

---

# 1. Exact adopted source

Candidate source:

`data/t1_contiguous_15_25_b1_stage16_17_candidate_v0_1.yaml`

Exact candidate SHA256 used by the closed B1 evidence:

`b9abc507c5ccdc20bc19c5681ba92cead920326fa9d04c1acf5b2ed90ff91465`

Exact materialized Stage15–25 window SHA256:

`f769dd79e750882a6b7a75dad18bfdbc514da546b183587ec2ed909e50b2ed0f`

---

# 2. Adopted Stage16 recipe

```text
Stage16
BRUTE ×4
0 / 1400 / 2800 / 4200 ms
F02 / CD02 / C1 / BULWARK
entryBaseX = 0.92
```

Exact Y placements:

```text
0 ms     BRUTE y=0.46
1400 ms  BRUTE y=0.44
2800 ms  BRUTE y=0.48
4200 ms  BRUTE y=0.46
```

Authoring intent:

```text
DURABLE FRONT / BULWARK READ
```

---

# 3. Adopted Stage17 recipe

```text
Stage17
GRUNT ×5
0 / 300 / 600 / 3000 / 3300 ms
F01 / CD03 / C1 / BASELINE
entryBaseX = 0.92
```

Exact Y placements:

```text
0 ms     GRUNT y=0.46
300 ms   GRUNT y=0.44
600 ms   GRUNT y=0.48
3000 ms  GRUNT y=0.45
3300 ms  GRUNT y=0.47
```

Authoring intent:

```text
RECOVERY / DECOMPRESSION BEFORE STAGE18 FIRST BRUTE MIX
```

---

# 4. Evidence retained with approval

B1 dynamic closure remains authority:

```text
100 / 100 persistent cases completed through Stage25
1100 Stage rows
terminal failures = 0
persistent state continuity = PASS
deterministic replay = PASS
settlement and carry invariants = PASS
Stage17 recovery = SUPPORTED
Stage25 objective-pressure relief = SUPPORTED
Lv16 timing-opportunity collision = RECONFIRMED / WATCH
Stage21-24 objective pressure = CLASS-SKEWED / WATCH
B1 = PASS_WITH_WATCHES
```

Final admitted evidence:

```text
workflow run  40254326926
artifact      12622340036
exact HEAD    e5b12a2c386de719c97dc020aeef9ffdbd9b1b3a
artifact SHA256
2f940ebea4c8b2be008e937d45e46f10595ec106b847f49af5ce1dc1b77b3acf
```

The superseded v0.1 stale-SHA guard failure remains non-balance evidence and must not be reopened without a real trigger.

---

# 5. What is now canonical

For Stage16 and Stage17 only, the following exact authoring properties are now canonical authority:

- spawn count;
- spawn timestamp;
- monster type;
- Y placement;
- listed formation/cadence/complexity/pressure-tag interpretation.

This authority joins the already user-approved Wave A exact-spawn baseline and Stage49–50 structural authoring baseline.

---

# 6. What this approval does NOT freeze or authorize

This approval does **not** authorize or freeze:

- production deployment;
- class scalars;
- monster scalars;
- shop values;
- EXP values or curve;
- exact Lv16 activation Stage;
- exact Lv21 activation Stage;
- P×P values;
- Archer Lv31 exact width;
- Mage Lv31 exact numerical centers;
- the complete T1 Stage1–50 exact recipe set.

Current progression reach authority remains band-based:

```text
Lv16 = Stage18–21 calibration-candidate reach band
Lv21 = Stage25–28 calibration-candidate reach band
```

---

# 7. Watches retained

```text
T1_RUNNER_LV6_PEDAGOGIC_COLLISION_WATCH
T1_BRUTE_LV16_CALIBRATION_COLLISION_WATCH
T1_RUNNER_HIGH_PRESSURE_LV16_TAIL_WATCH
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
T4_SUPPORTER_SIEGER_LEARNING_DENSITY_WATCH
TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH
T1_STAGE49_50_OBJECTIVE_PRESSURE_ROTATION_WATCH
```

No new watch is created by this approval.

---

# 8. Next bounded package selection

With Stage16/17 adopted, Stage15–25 is now a canonical contiguous exact-authoring window.

The next smallest high-value contiguous gap is:

```text
Stage26 / Stage27 / Stage28
```

Reason:

- Stage25 is already exact and user-approved;
- Stage29/30/31 are already exact and user-approved through Wave A;
- filling only Stage26–28 would create a contiguous exact Stage15–31 window;
- Stage26–28 cover the unresolved tail of the Lv21 Stage25–28 calibration-candidate reach band;
- the package therefore provides lifecycle value without broad-fill authoring.

Next package identifier:

```text
T1_C1_STAGE26_28_CONTIGUOUS_BRIDGE_AUTHORING
```

The next step is bounded structural recovery/preflight for Stage26–28 before any exact recipe is proposed.
