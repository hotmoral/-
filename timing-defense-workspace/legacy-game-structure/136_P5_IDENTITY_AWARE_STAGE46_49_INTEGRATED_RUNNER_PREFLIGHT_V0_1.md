# Timing Defense — P5 Identity-Aware Stage46–49 Integrated Runner Preflight V0.1

Date: 2026-10-23 KST  
Status: **RUNNER AUTHORED / STATIC PREFLIGHT COMPLETE / CHECKOUT-EXACT EXECUTION PENDING / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `123_P5_ALL_CLASS_SHOP_COMBAT_METHOD_FIDELITY_REVIEW_V0_1.md`
- `125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
- `127_P5_STAGE46_49_RIGHT_EDGE_TRAVEL_LEAD_PREFLIGHT_V0_1.md`
- `128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `132_P5_TANK_CONTROL_CLEAR_PARETO_DIRECTION_V0_1.md`
- `133_P5_ROGUE_DAGGER_STORM_BROAD_CLEANUP_BREAKPOINT_V0_1.md`
- `134_P5_KNIGHT_PENETRATION_ROBUST_IDENTITY_PROBE_V0_1.md`
- `135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`

New assets:
- `data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json`
- `../../tools/run_p5_identity_aware_stage46_49_integrated_probe_v0_1.py`

---

## 0. Recovery / boundary result

Live recovery before this slice confirmed:

```text
workspace handoff HEAD = 13510fda477cd1c78a632b155052510fbd31c3cd
production HEAD        = ea22cc279603394dc4b439b6fdbb0c83aff4299a
harness HEAD           = 063a9ac9986ba9a8028beb31a5b4c733c9bfa863
```

The canonical next boundary remained exactly:

```text
P5 identity-aware Stage46->49 normal-right-edge integration
```

No previously closed class-identity group was reopened.

---

## 1. Existing committed P5 shop-runner source-patch issue

The existing `run_p5_all_class_fixed_rank_shop_stage49_probe_v0_1.py` and `v0_2.py` build their patched simulator from:

```python
src = inspect.getsource(stage46.simulate)
```

They then attempt to replace:

```python
actual = min(m.hp, float(raw) * ...)
```

That line belongs to the module-level `stage46.hit()` function, not to `stage46.simulate()`.

Normal Python `inspect.getsource(stage46.simulate)` returns the `simulate()` definition only; it does not include the preceding module-level `hit()` definition.

Therefore that exact ATK source replacement is not a sound execution basis for the new integrated lane.

This does **not** invalidate the previously closed directional identity conclusions because those documents already distinguish independent directional reconstruction from committed-runner exact replay and explicitly keep exact replay pending.

Repair applied in the new runner:

```text
ATK shop scaling
-> guarded global hit wrapper
-> original stage46.hit remains the damage/kill/splitter implementation

simulate source patch
-> only lines actually owned by simulate()
-> schedule selection
-> starting wall current
-> DEF incoming damage
-> barrier source fidelity
-> no-target timing telemetry
-> Rogue storm package telemetry
```

The old runner files remain untouched as historical artifacts.

---

## 2. Right-edge schedule contract

The new runner does not support row-level `spawnX` authoring.

Hard contract:

```text
physical spawnX = 0.92
mid-field pop-in = forbidden
```

For Stage48/49 authored rows:

```text
spawn time = reference time + referenceOffset - spawnLeadSeconds
```

A diagnostic warmup/reference offset prevents negative spawn times.

`spawnLeadSeconds` therefore changes only **when** the enemy begins its travel, not **where** it appears.

Stage46/47 retain their inherited pressure-pattern structure with the current directional cadence candidates. Stage48/49 use the escorted diagnostic packets from the accepted right-edge direction fixture.

---

## 3. Wall continuity contract

The runner carries one external wall state through:

```text
Stage46 -> Stage47 -> Stage48 -> Stage49
```

For every transition it records:

```text
max wall HP
current wall HP
absolute damage deficit = max - current
```

No stage reset to full HP is allowed.

Fortification semantic remains:

```text
max += delta
current += delta
absolute deficit unchanged
```

Current first integrated lane uses one fixed late-segment shop snapshot throughout the four diagnostic windows. Therefore max HP does not change inside this first chain, but the runner carries it explicitly so later acquisition-history work cannot silently reset it.

---

## 4. Shop temporal boundary

No canonical Stage46–49 purchase history is frozen.

Inventing a per-stage purchase path in this slice would mix an unapproved economy-path assumption into the class-identity / encounter-chronology question.

Therefore the first integrated lane deliberately uses:

```text
FIXED_LATE_SEGMENT_POWER_ISOLATION
```

Representative profiles:
- BALANCED
- ATTACK_HEAVY
- DEFENSE_HEAVY
- ROLE_AWARE

Diagnostic shop scale:

```text
0.40 legacy-relative
```

This is not a production recommendation and does not close:
- real ATK acquisition-time feedback;
- real DEF acquisition-time feedback;
- wallet path optimization;
- purchase-order behavior.

Those remain later fidelity work after the identity/chronology lane is executable.

---

## 5. Tank integrated sensitivity

Only Tank Lv31 enemy-damage contribution is varied:

```text
0.20
0.25
0.30
```

Unchanged:

```text
knockback
slow
barrier
Iron Wall
battlefield-reset control structure
```

The runner measures Stage46–49 wall reserve/contact/backlog/SIEGER exposure while the finite identity regression separately measures mixed-packet direct-clear throughput.

No coefficient can be selected from the finite packet alone.

---

## 6. Rogue Dagger Storm telemetry

Deterministic retarget remains unchanged.

Per storm the runner records:
- distinct target IDs hit;
- distinct target IDs killed;
- distinct target types hit/killed;
- fresh ordinary-target dagger events.

It also reports analytic fresh one-dagger breakpoints for:

```text
GRUNT
RUNNER
SHIELD
```

At the 40% diagnostic center, the current representative ATK ranks imply:

```text
BALANCED atk8        -> one dagger vs fresh GRUNT ~= 339.12
ATTACK_HEAVY atk9    -> ~= 347.76
DEFENSE_HEAVY atk6   -> ~= 321.84
ROLE_AWARE Rogue atk10 -> ~= 356.40
```

Current GRUNT HP is 320.

Therefore all four representative 40% profiles cross the fresh-GRUNT one-dagger threshold, including DEFENSE_HEAVY by a narrow margin.

RUNNER is already below one-dagger raw damage; SHIELD remains above one-dagger damage in these profiles.

This strengthens the need to measure **distinct targets cleaned per storm**, not merely whether a one-shot breakpoint exists.

Active guard remains:

```text
ROGUE_STORM_SINGLE_DAGGER_ORDINARY_ONESHOT_NOT_ROUTINE
```

No retarget removal is authorized.

---

## 7. Identity regression package

The new runner includes targeted regressions only; it does not rerun the closed diagnostic group from scratch.

### Knight
Uses the refined HP1600 / armor0.55 durable proxy pair:

```text
aligned    [0,0,0,0,0]
dispersed [-2,-1,0,1,2]
```

Profiles:
- BALANCED
- DEFENSE_HEAVY

Reference direction remains aligned faster than dispersed.

### Archer
Profiles:
- BALANCED
- ATTACK_HEAVY

Pair:
- aligned line
- scatter

Reference direction remains aligned materially faster than scatter.

### Mage
Profile:
- BALANCED

Pair:
- cluster
- distributed

Reference direction remains cluster materially faster than distributed.

### Tank
The existing mixed finite packet is replayed at:

```text
0.20 / 0.25 / 0.30
```

SURVIVAL is not treated as CLEAR.

---

## 8. Stage-boundary backlog bias made explicit

The inherited P4/P5 recipes are bounded **60-second stress windows**, not exact launch-stage scripts.

The first integrated runner carries wall state between those windows but does not transplant living diagnostic mobs across the synthetic stage boundary.

Therefore:

```text
endActive is always recorded
```

and the new watch is:

```text
P5_STAGE_BOUNDARY_BACKLOG_DISCARD_BIAS = ACTIVE
```

Interpretation rule:
- if `endActive` is small/non-material, the wall-chain directional comparison remains useful;
- if `endActive` is material, do not interpret the resulting Stage49 reserve as an exact stage-clear reserve;
- resolve stage-boundary/backlog fidelity before any numerical freeze.

This makes the abstraction visible instead of silently discarding it.

---

## 9. Validation performed in this slice

Completed:
- live canonical/branch recovery;
- production/harness HEAD recheck;
- existing source-patch mismatch isolated;
- new integration fixture authored;
- new source-patched integrated runner authored;
- local Python syntax compilation of the authored runner content passed;
- right-edge contract encoded as a hard validation;
- production/harness left untouched.

Not yet claimed:

```text
checkout-exact import/run PASS
exact output hash
Stage46-49 numerical verdict
Tank coefficient selection
Stage49 chronology retune
```

The current execution environment cannot clone GitHub (`github.com` DNS resolution unavailable), so a checkout-equivalent execution was not fabricated or inferred.

---

## 10. Current classification / next boundary

```text
CLASS_IDENTITY_GROUP = DIRECTIONALLY_CLOSED
IDENTITY_AWARE_STAGE46_49_RUNNER = AUTHORED
STATIC_PREFLIGHT = COMPLETE
RIGHT_EDGE_CONTRACT = ENCODED
WALL_CURRENT_MAX_DEFICIT_CARRY = ENCODED
TANK_020_025_030 = ENCODED
ROGUE_DISTINCT_TARGET_TELEMETRY = ENCODED
KNIGHT_ARCHER_MAGE_REGRESSIONS = ENCODED
CHECKOUT_EXACT_EXECUTION = PENDING
PRODUCTION_CHANGE = NO
NUMERICAL_FREEZE = NO
```

Exact next order:
1. checkout-equivalent import/run of the new runner;
2. if a guarded source patch fails, repair simulator fidelity only;
3. inspect Stage46→49 chain results, especially Tank survival-vs-clear and Rogue distinct-target cleanup;
4. confirm Knight/Archer/Mage directional regressions remain intact;
5. inspect `endActive` to determine whether stage-boundary backlog fidelity must be raised before interpretation;
6. only then refine Stage49 escort/frontmost chronology;
7. production changes remain separately approval-gated.
