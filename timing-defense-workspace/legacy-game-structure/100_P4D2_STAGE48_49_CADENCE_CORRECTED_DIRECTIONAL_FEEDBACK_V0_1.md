# Timing Defense — P4-D2 Stage48–49 Cadence-Corrected Directional Feedback V0.1

Date: 2026-10-23 KST  
Status: **FIDELITY-CHECKED DIRECTIONAL FEEDBACK / EXACT COMMITTED-RUNNER REPLAY STILL REQUIRED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Authority:
- `95_P4D2_STAGE46_STATEFUL_TEMPORAL_PRESSURE_PROBE_V0_1.md`
- `96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`
- `98_P4D2_STAGE48_49_GRAMMAR_RESET_PROXY_V0_1.md`
- `99_P4D2_TEMPORAL_CADENCE_FIDELITY_REVIEW_V0_1.md`
- `../PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`

Prepared replay assets:
- `../../tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_2.py`
- `data/p4d2_stage48_49_dynamic_rotating_grammar_fixture_v0_1.json`

Machine-readable directional summary:
- `data/p4d2_stage48_49_cadence_corrected_directional_summary_v0_1.json`

Expected full v0.2 JSON SHA-256 from the independent fidelity-checked reconstruction:

```text
63da011ac97fd809168d8ffc9c3a9721c9962a2ae3c3496aa91e0d2de0b592f8
```

The exact committed v0.2 runner still needs one-command execution in a repository checkout before this hash can be promoted to exact replay evidence.

---

# 0. Method validation

Before using the corrected local reconstruction for directional feedback, it was first run against the already accepted Stage46 all-success temporal fixture.

It reproduced the accepted document-95 baseline **exactly** for all five classes on:

```text
endWall
endActive
maxActive
kills
```

Reference match:

| Class | endWall | endActive | maxActive | kills |
|---|---:|---:|---:|---:|
| Knight | 1175 | 19 | 24 | 152 |
| Rogue | 1330 | 24 | 28 | 153 |
| Tank | 2000 | 9 | 16 | 174 |
| Archer | 2000 | 9 | 16 | 172 |
| Mage | 2000 | 4 | 13 | 179 |

This materially increases confidence that the reconstructed combat/effect semantics match the accepted kernel.

The Stage48–49 feedback below is still classified **directional** until the committed v0.2 runner produces the expected replay output.

---

# 1. Corrected methodology

Two fidelity corrections are active.

## Rogue cadence sensitivity

Common lane:

```text
root interval = 1.125s
```

Rogue legacy-recovery sensitivity:

```text
1.125 - 0.078 = 1.047s
```

The 78ms comes from recovered `390ms -> 312ms` Assassin Rhythm recovery authority.
This is not a production whole-cycle freeze.

## No-target clock

Corrected rule:

```text
NO_TARGET_OPPORTUNITIES_DO_NOT_BANK
```

Overdue attack opportunities are not stored and consumed as catch-up bursts after targets return.
No numeric reacquisition delay is frozen here.

Heavy/P×P opportunities are mapped to active pressure grammar by timestamp.

---

# 2. All-success result under current rotating grammar

Current grammar rotation:

```text
LINE_ESCORT
CLUSTER_CASCADE
FRONTLINE_BREACH
DURABLE_SCATTER
```

All P×P successful:

| Class / lane | End wall | End active |
|---|---:|---:|
| Knight common1.125 | 895 | 24 |
| Rogue common1.125 | 520 | 24 |
| **Rogue recovery1.047 sensitivity** | **1850** | **20** |
| Tank common1.125 | 2000 | 9 |
| Archer common1.125 | 1575 | 13 |
| Mage common1.125 | 2000 | 1 |

The Rogue swing is the important methodology result.
Omitting the recovered 78ms recovery effect made Rogue appear much weaker than the fidelity lane.

Therefore:

`ROGUE_CADENCE_OMISSION_WAS_MATERIAL = YES`

No evidence here justifies reducing Dagger Storm below the current 16-projectile center.

---

# 3. One missed P×P

Across the four grammar-aligned start points:

### Knight
- survives all four;
- end wall range `385..1100`.

### Rogue — common cadence
- buries in all four.

### Rogue — 78ms recovery sensitivity
- **survives all four**;
- end wall range `995..1180`.

This flips the earlier interpretation:

> one isolated Rogue mistake is not inherently terminal once recovered cadence authority is represented.

### Tank
- survives all four at wall `2000`.

### Archer
- survives all four;
- end wall `1575..1925`;
- several miss cases end **better** than the all-success path.

### Mage
- survives all four at wall `2000`.

---

# 4. Two consecutive missed P×P

### Knight
- buries from two of four grammar starts;
- survives the other two at wall `380` and `505`.

This is a useful mastery-pressure shape: two consecutive mistakes can become terminal depending on what pressure was active.

### Rogue — 78ms recovery sensitivity
- buries from **all four** grammar starts;
- burial approximately `53.1..56.375s`.

This closely matches the desired late-run rhythm:

```text
one isolated mistake -> recoverable
repeated mistake -> burial cascade
```

### Tank
- survives all four;
- wall `1833..1981`.

### Archer
- survives all four;
- wall `1775..2000`;
- success-monotonicity WATCH persists.

### Mage
- survives all four at wall `2000`.

Thus the current grammar is still too forgiving for Tank/Mage if `two consecutive misses` were treated as a universal target.
But universal identical error budgets are not required by contract.

---

# 5. Consecutive-miss sensitivity

Directional sweep of consecutive failed final opportunities:

| Class | First burial by start grammar |
|---|---|
| Knight | 2 / 2 / 3 / 3 misses |
| Rogue 78ms lane | 2 / 2 / 2 / 2 |
| Tank | 4 / 5 / 5 / 4 |
| Archer | one start buries at 7; other tested starts survive through 8 |
| Mage | some starts bury at 7–8; other tested starts survive through 8 |

When **every final opportunity is missed**, all five eventually fail inside the 60s stress:

```text
Knight 28.875s
Rogue  26.700s  (78ms recovery sensitivity)
Tank   31.200s
Archer 47.525s
Mage   59.800s
```

So the important structural requirement is met:

`NO_CLASS_CAN_IGNORE_LV31_PXP_INDEFINITELY = TRUE`

But the mastery error budget is highly class-dependent.

---

# 6. Archer success-monotonicity WATCH

Several Archer miss paths finish with **more** wall HP than the all-success path.
This must not be hidden or interpreted as “the ultimate is bad” without chronology inspection.

The likely causal family is path dependence:
- stronger/wider final removes different front bodies;
- SPLITTER parents can die earlier and create children earlier;
- next frontmost target/band changes;
- CHARGER/SIEGER state exposure changes;
- later attacks therefore follow a different target-order path.

Evidence supporting this interpretation:
- success/miss paths differ in SPLITTER parent/child counts and capability-expression counts in several runs;
- no-target banking is zero for Archer in these scenarios, so that artifact does not explain the nonmonotonicity.

Classification:

`LV31_ARCHER_SUCCESS_MONOTONICITY_CHRONOLOGY_WATCH = HIGH`

Next repair/inspection layer:
1. SPLITTER death/child-spawn chronology;
2. band/target order after wide-arrow deletion;
3. role-state exposure;
4. encounter ordering.

Do not reduce Archer width or damage merely because this path exists.

---

# 7. Tank/Mage tolerance

The current rotating grammar does not make one/two missed finals sufficiently consequential for Tank/Mage.

Do **not** solve this immediately by nerfing their Lv31 skills.

The first repair layer remains encounter grammar / temporal role pressure:
- staggered role threats rather than blanket spawn-count inflation;
- SIEGER standoff/shot opportunities that survive the instant reset window where appropriate;
- CHARGER timing windows;
- SPLITTER rebound arriving outside a successfully resolved collapse package;
- distributed/delayed durable pressure that cannot all be consumed by one instantaneous global/area reset.

A small exploratory pressure check also showed that simply shortening the global pressure cycle or adding generic extra bodies can kill Knight/Rogue first while Tank/Mage remain comfortable.
Therefore:

`NAIVE_GLOBAL_PRESSURE_SCALAR = REJECT_AS_NEXT_REPAIR_LAYER`

This reinforces the grammar-first policy.

---

# 8. Rogue conclusion

The most important balance correction from this pass is actually **not a gameplay-number change**.

Old apparent problem:

```text
Rogue loses after one missed final
```

Corrected interpretation:

```text
common-cadence simulator omitted a recovered Rogue cadence advantage
-> Rogue looked artificially fragile

78ms recovery sensitivity represented
-> one miss recoverable
-> two consecutive misses terminal
```

Therefore:
- keep 16-dagger working center;
- do not nerf projectile count;
- do not add hidden Rogue compensation;
- do not freeze 1.047s as production cadence.

---

# 9. P4-D2 status

The current evidence supports:

```text
Stage46 combat-based mastery gate philosophy = still sound
Archer wider corridor approval = still sound
Rogue16 center = still sound
rotating grammar direction = still sound
common-cadence class-fairness ranking = superseded by fidelity review
```

P4-D2 is **not closed yet**.

Remaining immediate work:
1. execute committed v0.2 runner and verify expected full-output hash;
2. isolate Archer chronology/nonmonotonicity;
3. construct a role/timing pressure probe that challenges Tank/Mage without blanket scalar inflation;
4. determine whether these are sufficient for provisional P4-D2 closure with watches.

No user decision is required at this point.
No production gameplay change is authorized.
