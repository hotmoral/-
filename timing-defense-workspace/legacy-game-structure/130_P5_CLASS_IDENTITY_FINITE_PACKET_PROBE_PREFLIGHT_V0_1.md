# Timing Defense — P5 Class Identity Finite-Packet Probe Preflight V0.1

Date: 2026-10-23 KST  
Status: **RUNNER + FIXTURE AUTHORED / EXECUTION PENDING / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `data/p5_class_identity_radar_invariants_v0_1.yaml`
- `124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `../tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`

Assets:
- `data/p5_class_identity_radar_probe_fixture_v0_1.json`
- `../tools/run_p5_class_identity_radar_probe_v0_1.py`

---

# 0. Purpose

The recent late-game probes mostly answered whether the wall survived a stress horizon.
That is insufficient for the radar identity gate, especially for Tank.

This bounded probe adds a finite-packet question:

```text
How long does each class take to actually kill the whole packet?
Did any enemy reach the wall instead?
Was the packet still unfinished at the scan horizon?
```

Therefore:

```text
SURVIVED != DIRECT CLEAR
```

---

# 1. Reused combat authority

The runner reuses the existing P5 all-class v0.2 diagnostic kernel rather than inventing a new combat model.

Current cross-class shop scope remains:

```text
ATK
FORTIFICATION
DEFENSE
```

Still deferred:

```text
KNOCKBACK
CRIT
CRITDMG
```

The probe keeps the normal right-edge physical spawn point `x=0.92`.

No class/shop/monster coefficient is changed by this runner.

---

# 2. Direct-clear definition

A finite packet counts as a direct clear only when:

```text
all expected enemies are killed by the player
AND wall contact count == 0
AND active backlog == 0
AND wall is not buried
```

If the class merely survives while enemies remain alive, that is not a clear.
If enemies disappear because they reached the wall, that is also not a direct-clear success for this identity metric.

The runner searches the first deterministic duration where the direct-clear predicate becomes true.
If it is still false at the scenario's maximum scan horizon, the result is `unfinishedWithinMaxScan=true`.

No clear-time threshold is frozen in V0.1.

---

# 3. Paired identity scenarios

## Knight

```text
KNIGHT_ALIGNED_FRONT
vs
KNIGHT_DISPERSED_FRONT
```

Same broad threat family, different alignment.
Goal: verify penetration/frontline structure is a material reason for success.

## Rogue

```text
ROGUE_DURABLE_SINGLE
vs
ROGUE_BROAD_WAVE
```

Goal: verify durable-target multihit execution remains a defining strength while broad wave cleanup does not become an accidental AOE/PEN replacement.

The packets do not have equal total HP; this is a leakage-direction probe, not a normalized DPS benchmark.

## Tank

```text
TANK_MIXED_SOLO
```

All five classes run the same mixed durable/role packet.
The runner compares Tank direct-clear time to the finite clear times of Knight/Rogue/Archer/Mage.

Key outputs:
- Tank direct clear time;
- unfinished within 180 s;
- end backlog at 30/60/90 s;
- wall reserve;
- damage-class median clear time;
- Tank-to-damage-class clear-time ratio.

This is the first P5 lane where Tank enemy-removal throughput is explicitly separated from survival.

## Archer

```text
ARCHER_ALIGNED_LINE
vs
ARCHER_SCATTER
```

Run at BALANCED and additionally ATTACK_HEAVY.
Goal: check whether shop ATK is erasing the intended dependence on line alignment.

## Mage

```text
MAGE_CLUSTER
vs
MAGE_DISTRIBUTED
```

Goal: preserve the known density advantage / distributed-durable weakness.

---

# 4. Current fixture profiles

All classes run BALANCED at the current `40% legacy-relative` diagnostic magnitude.
Additional stress profiles:

```text
Knight -> DEFENSE_HEAVY
Tank   -> ROLE_AWARE
Archer -> ATTACK_HEAVY
```

These are analysis centers only, not production recommendations.

Snapshots are collected at:

```text
30 s
60 s
90 s
```

Tank mixed-solo clear scan extends to 180 s.
Other scenarios scan up to 120 s.

---

# 5. Execution boundary

The runner and fixture are now authored, but this document does **not** claim combat results yet.

Required before interpreting output:
1. execute the committed runner against the committed dependencies;
2. verify source-guard/import compatibility with the current P5 v0.2 kernel;
3. persist the raw JSON result;
4. inspect whether direct-clear monotonicity holds after all finite packet rows spawn;
5. then classify each radar identity without freezing thresholds from one fixture.

If execution reveals a kernel/runner mismatch, fix fidelity first rather than interpreting partial output.

---

# 6. Expected interpretation, not a pass threshold

Desired qualitative shape:

```text
Knight -> aligned/frontline should show meaningful penetration benefit
Rogue  -> durable execution strong; broad wave should not become universal cleanup
Tank   -> wall survival strong but actual direct-clear substantially slower / often unfinished
Archer -> aligned line materially better than scatter, including ATTACK_HEAVY
Mage   -> clustered packet materially better than distributed packet
```

Do not force identical class clear times.
Do not turn these statements into exact percentages before the first committed result exists.

---

# 7. Next

1. execute `run_p5_class_identity_radar_probe_v0_1.py` and save exact raw result;
2. classify Tank solo throughput first because it closes the largest current validation gap;
3. inspect Archer ATTACK_HEAVY aligned-vs-scatter difference;
4. inspect Mage cluster-vs-distributed and Rogue durable-vs-wave leakage;
5. then integrate the useful identity metrics into the Stage46–49 source-patched right-edge runner;
6. only after that return to Stage49 packet chronology refinement.

No production change is authorized.
