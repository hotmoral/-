# Timing Defense — P5 Stage46–49 Exact Execution / STAGE_SETTLED Boundary Result V0.1

Date: 2026-10-23 KST  
Status: **EXACT RUNNER ADMITTED / RESET-BOUNDARY RESERVE INTERPRETATION REJECTED / STAGE48 CURRENT DIAGNOSTIC PACKET NOT ADMISSION-READY / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
- `134_P5_KNIGHT_PENETRATION_ROBUST_IDENTITY_PROBE_V0_1.md`
- `135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
- `136_P5_IDENTITY_AWARE_STAGE46_49_INTEGRATED_RUNNER_PREFLIGHT_V0_1.md`

Production remains unchanged and unauthorized for gameplay/numerical modification.

---

## 1. Plain-language result

The newly authored integrated runner was executed from an exact GitHub checkout and passed its source-patch/import/determinism gate.

That execution then exposed a more important structural issue:

```text
60-second diagnostic window ends
but many Stage-owned enemies are still alive
```

The old first-pass integrated chain carried wall HP forward but discarded those living enemies at the synthetic boundary.
That makes its final wall reserve too optimistic for a real Stage-clear interpretation.

Approved P3 lifecycle semantics already define the correct order:

```text
last authored spawn
-> clear every remaining Stage-owned enemy
-> STAGE_SETTLED
-> Stage clear / shop
-> reset Stage-local enemy state
-> next Stage
```

Therefore:
- deleting residual enemies at 60 s is wrong;
- carrying those enemy instances directly into the next Stage wave is also wrong;
- further Stage46–49 reserve interpretation must use STAGE_SETTLED semantics.

---

## 2. Exact committed integrated-runner admission

Exact checkout execution was performed only on an isolated diagnostic branch created from workspace HEAD `7e3385a643b119e88be07e12929df1b8d87142d7`.
No production or canonical gameplay fixture was modified for the run.

GitHub Actions evidence:

```text
run id: 39949346908
committed runner: tools/run_p5_identity_aware_stage46_49_integrated_probe_v0_1.py
repeat #1 SHA256: 0d08f52ad5a25049e3379831bb4a41e7dc63256d7675d3743a1891dfba35a45b
repeat #2 SHA256: 0d08f52ad5a25049e3379831bb4a41e7dc63256d7675d3743a1891dfba35a45b
```

Admission:

```text
checkout-equivalent import/run = PASS
guarded source patch = PASS
repeat deterministic bytes = PASS
normal physical spawnX 0.92 = preserved
mid-field pop-in = absent
```

This closes the exact-execution admission that was pending in doc 136.

---

## 3. Targeted identity regression results

The exact run did not provide a trigger to reopen the directionally closed class-identity group.

Exact targeted references:

```text
Knight BALANCED       aligned 8.080 / dispersed 10.331
Knight DEFENSE_HEAVY  aligned 8.226 / dispersed 12.728
Archer BALANCED       aligned 3.580 / scatter 8.075
Archer ATTACK_HEAVY   aligned 3.580 / scatter 8.075
Mage BALANCED         cluster 3.780 / distributed 8.080
Tank finite mixed packet:
  0.20 -> 21.578 s
  0.25 -> 18.209 s
  0.30 -> 14.829 s
```

Interpretation remains:
- Knight penetration/frontline causality is present;
- Archer line dependence is strong;
- Mage density dependence is strong;
- Tank lower damage materially slows direct clear, but no coefficient is selected.

`SURVIVAL != CLEAR` remains mandatory.

---

## 4. Rogue exact integrated watch

At the current 40% shop diagnostic scale, exact analytic/runtime evidence confirms:

```text
fresh GRUNT  -> one Dagger Storm dagger can one-shot
fresh RUNNER -> one dagger can one-shot
fresh SHIELD -> one dagger does not one-shot
```

Representative raw/damage values remain approximately:

```text
BALANCED atk8          339.12
ATTACK_HEAVY atk9      347.76
DEFENSE_HEAVY atk6     321.84
ROLE_AWARE Rogue atk10 356.40
```

Distinct-target cleanup is therefore the important leakage metric.
The integrated run showed large multi-target cleanup in several Storms, especially in Stage46/47.

Classification remains:

```text
ROGUE_CORE_MULTIHIT_IDENTITY = PRESERVED
ROGUE_BROAD_CLEANUP_LEAKAGE = HIGH WATCH
ROGUE_RETARGET_CHANGE_AUTHORIZED = NO
```

Do not remove deterministic retarget as the first repair.

---

## 5. The boundary watch triggered materially

The first exact 60 s chain retained nonzero `endActive` across many class/stage combinations.
Tank commonly retained roughly 15–30 live enemies at synthetic boundaries; other classes also retained material backlog.

Therefore:

```text
P5_STAGE_BOUNDARY_BACKLOG_DISCARD_BIAS = TRIGGERED
```

The old reset-boundary final-wall values remain useful only as bounded stress-window diagnostics.
They are not admissible Stage-clear reserves.

A separate continuous-carry diagnostic also confirmed that residual backlog matters, but that model is **not** structurally admissible because P3 forbids enemy-instance leakage into the next Stage after settlement.

```text
DELETE_AT_60S = REJECTED AS STAGE-CLEAR MODEL
CARRY_ENEMIES_INTO_NEXT_STAGE = REJECTED AS STAGE-CLEAR MODEL
DRAIN_CURRENT_STAGE_TO_STAGE_SETTLED = REQUIRED
```

---

## 6. Exact STAGE_SETTLED diagnostic

A bounded diagnostic replay froze each Stage's authored 60 s spawn schedule, then stopped creating new enemies and allowed that Stage to drain until all Stage-owned enemies were cleared or the wall was buried.
Wall current/max/absolute deficit then carried into the next Stage; enemy instances did not.

Exact diagnostic evidence:

```text
run id: 39950165809
repeat #1 SHA256: 2680ec99b9aecbc27eca9c647b6c95057780306eab2acf884b511581d3a95e0d
repeat #2 SHA256: 2680ec99b9aecbc27eca9c647b6c95057780306eab2acf884b511581d3a95e0d
```

Important examples:

### Knight / Rogue
Representative profiles settle Stage46–49 with little or no wall damage in this current diagnostic recipe.
This is evidence that the current packet is not a balanced late-pressure authoring candidate.

### Tank
All 0.20 / 0.25 / 0.30 candidates can settle through Stage49 in the current recipe, but they differ materially in clear tail and wall reserve.
For BALANCED:

```text
0.20 final wall 1588.35
0.25 final wall 1859.22
0.30 final wall 2043.36
```

No coefficient is selected because these values are still coupled to a Stage48 packet now shown to be structurally contaminated by a test proxy.

### Archer
Representative profiles settle all four Stages with usable reserve; the old Archer issue remains a chronology/failure-budget watch rather than a class-identity defect.

### Mage
Current Stage48 is the material outlier:

```text
BALANCED      buried at ~67.375 s
ATTACK_HEAVY  buried at ~76.100 s
DEFENSE_HEAVY buried at ~71.200 s
ROLE_AWARE    survives but drops to ~226.1 wall
```

The current Stage48 candidate therefore fails its own all-class representative-success direction under proper STAGE_SETTLED semantics.

This is **not** sufficient evidence for a Mage buff.

---

## 7. Root cause: Stage48 is contaminated by a Knight-only test body

Current Stage48 diagnostic uses `ARMORED_DURABLE_PROXY`.
Doc 134 defines that body only to isolate Knight penetration causality:

```text
HP 1600
armor 0.55
```

The right-edge fixture itself states that it is a diagnostic proxy, not a new approved monster.

At the current Stage48 4.9 s repeated stress cadence, the 60 s authored schedule contains approximately:

```text
23 x ARMORED_DURABLE_PROXY
10 x CHARGER
10 x RUNNER
11 x SIEGER
```

So a Knight-specific high-durability/high-mitigation test body became a repeated all-class escort body.
That disproportionately pressures low-PEN Mage and contaminates the intended Stage48 role-pulse question.

This is a concrete cross-system consistency trigger and justifies reopening Stage48 packet construction without reopening global class identity.

---

## 8. Factor isolation

A temporary bounded factor-isolation diagnostic tested Stage48 only.
All tests remained at normal right-edge physical entry; no candidate was promoted.

Exact deterministic factor run:

```text
run id: 39951028213
repeat SHA256: a8e303f35b2e713cf7f7d1e2d1f98b91f865631c39c2f81bbd4157bc49e057f3
```

Key results:

### Current proxy packet
- Mage: 3/4 representative profiles buried; ROLE_AWARE survives with severe reserve loss.
- Tank: substantial wall contacts.
- Knight/Rogue/Archer: generally zero wall damage.
- SIEGER: generally **0 shots** for non-Mage classes.

### Replace proxy rows with real BRUTE
- all representative class/build cases essentially clear at full wall;
- SIEGER still 0 shots.

### Replace proxy rows with real SHIELD
- same qualitative result: essentially full wall;
- SIEGER still 0 shots.

### BRUTE + SHIELD mix
- same qualitative result;
- SIEGER still 0 shots.

### Slower SHIELD packet cycle
- same qualitative result;
- SIEGER still 0 shots.

### Half proxy repetition
- burial disappears;
- Mage still takes disproportionately large wall loss;
- SIEGER remains mostly 0 shots.

### One proxy row only
- pressure nearly disappears for all classes;
- SIEGER remains 0 shots.

Conclusion:

```text
CURRENT_STAGE48_PRESSURE_SOURCE = TEST_PROXY_THRESHOLD, NOT SIEGER ROLE UPTIME
SIMPLE_PROXY_TO_REAL_MONSTER_SUBSTITUTION = INSUFFICIENT
NEXT_REPAIR_AXIS = PACKET CHRONOLOGY / FRONTMOST SCREENING / RELATIVE ENTRY TIMING
```

Do not compensate by globally buffing escort HP or by nerfing classes.

---

## 9. What is and is not closed

Closed/admitted now:

```text
integrated runner exact import/run
source-patch fidelity for this runner
repeat determinism
class targeted regression directions
stage-boundary backlog is materially relevant
STAGE_SETTLED is the correct stage-transition interpretation
current Stage48 proxy packet is not admission-ready
simple BRUTE/SHIELD substitution is not enough
```

Still open:

```text
real-monster Stage48 escorted-SIEGER chronology candidate
Stage49 chronology after Stage48 is repaired
Tank 0.20/0.25/0.30 selection
Rogue broad-cleanup repair policy
exact real shop acquisition timing
later KNOCK / CRIT / CRITDMG lanes
```

No class coefficient, shop coefficient, monster stat, Stage48 packet or Stage49 packet is frozen here.

---

## 10. Exact next boundary

Do **not** continue isolated Stage49 tuning yet.

Next bounded work:

1. keep all enemies at physical right-edge spawnX `0.92`;
2. use existing approved/provisional real monster archetypes only for Stage48 chronology search;
3. vary **relative entry timing/frontmost screening**, not global durability first;
4. require that the SIEGER actually reaches role uptime in at least meaningful representative cases;
5. preserve all-class successful-play survivability with usable reserve;
6. preserve defense-heavy Knight viability and Mage AOE identity;
7. keep Tank slow-clear behavior visible;
8. then re-run the Stage46–49 STAGE_SETTLED chain;
9. only after a promising bounded candidate exists, present the candidate and tradeoffs to the user before adopting it as the working Stage48 direction.

Production remains unchanged.
