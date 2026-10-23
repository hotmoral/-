# Timing Defense — P5 Stage48 SIEGER Protection-Time Diagnostic V0.1

Date: 2026-10-23 KST  
Status: **OBSERVED / BOUNDED DIAGNOSTIC / NO CANDIDATE ADOPTION / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
- `137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`

Temporary diagnostic execution only:
- branch `timing-defense-workspace-temp-check`
- run id `39954298666`
- no planning/production authority

---

## 0. Plain-language question

Why does SIEGER fail to perform its role when Stage48 uses only real existing monsters as escorts?

The immediate question was narrowed to:

> How far does SIEGER actually travel before dying under the contaminated proxy packet versus real-monster screens?

This diagnostic did not change monster stats, class stats, shop values, Stage48 cadence, spawnX, SIEGER windup, or production gameplay.

---

## 1. Instrumentation fix

The previous temporary death-position probe failed before producing evidence because monster IDs such as `SIEGER_3` were incorrectly cast to integer.

Fix:

```text
int(target.id) -> str(target.id)
```

This was an instrumentation-only defect.
It did not indicate a combat/runtime mismatch.

The corrected workflow completed successfully.

---

## 2. Fixed physical contract

All tested enemies still entered from the normal right edge:

```text
spawnX = 0.92
```

Current diagnostic SIEGER anchor:

```text
speed = 0.045
siege threshold x <= 0.38
```

Therefore a SIEGER starting at `0.92` requires approximately:

```text
(0.92 - 0.38) / 0.045 = 12.0 seconds
```

of uninterrupted forward travel to reach the siege line before considering the additional windup itself.

This 12.0 s is a derived diagnostic travel budget from the current provisional anchor, not a production-frozen value.

---

## 3. Compared packets

Compared:

1. `CURRENT_PROXY_PACKET`
   - still contains repeated `ARMORED_DURABLE_PROXY`
   - known contaminated baseline

2. `BRUTE_PAIR_LONG_LEAD`
3. `BRUTE_TRAIN_FOUR`
4. `BRUTE_SPLITTER_LAYER`

The real-monster variants use existing real archetypes only and preserve normal right-edge entry.

The current Stage48 4.9 s cycle was held fixed to isolate screening/chronology behavior.
No tested variant is adopted.

---

## 4. Main observed result

### Real-monster screens
Across all tested real-monster variants:

```text
SIEGER windups = 0
SIEGER shots   = 0
```

The SIEGER is being killed while still in `ADVANCE` state.

Best observed minimum death X by class across the tested real-monster variants:

```text
Knight  ~0.7389
Rogue   ~0.7287
Tank    ~0.4451
Archer  ~0.7209
Mage    ~0.7929
```

Approximate forward-travel time represented by those best cases:

```text
Knight  ~4.0 s
Rogue   ~4.25 s
Tank    ~10.55 s
Archer  ~4.42 s
Mage    ~2.82 s
```

Against a ~12.0 s travel requirement to x=0.38, the approximate remaining shortfall is:

```text
Knight  ~8.0 s
Rogue   ~7.75 s
Tank    ~1.45 s
Archer  ~7.58 s
Mage    ~9.18 s
```

These are bounded diagnostic calculations, not acceptance thresholds.

### Current proxy packet
The contaminated proxy packet behaved differently in some classes.

Notably for Mage:

```text
SIEGER reached x=0.38
windups = 3
shots = 1
```

The Mage case then buried the wall, consistent with doc137's finding that the proxy packet creates excessive Mage-specific pressure.

Other classes still often kill SIEGER well before meaningful siege uptime even in the proxy packet.

---

## 5. Causal interpretation

The current evidence rejects this explanation:

```text
SIEGER reaches siege line but loses during the 0.8 s windup
```

Reason:
- tested real-monster packets produced zero windups;
- the SIEGER usually dies far before x=0.38.

The stronger current interpretation is:

```text
REAL_MONSTER_STAGE48_FAILURE
= insufficient protected travel time before SIEGER becomes attackable/exposed
NOT primarily SIEGER windup duration
```

For Knight/Rogue/Archer/Mage, the shortfall is large enough that tiny +/-1 s entry-time nudges are unlikely to be an efficient first search axis by themselves.

Tank is different:
- Tank's low removal throughput/control lets SIEGER approach much closer to the siege line;
- this is consistent with Tank's intended negative solo-throughput identity;
- it must not be used as proof that the Stage packet is healthy for all classes.

---

## 6. What this does NOT authorize

This result does **not** authorize:
- increasing SIEGER HP;
- reducing SIEGER windup;
- increasing BRUTE/SHIELD HP;
- buffing Mage;
- nerfing Archer/Rogue/Knight;
- selecting Tank 0.25;
- changing Stage48 cadence;
- adopting any tested real-monster packet;
- changing production.

The user requires important design/numerical decisions to be presented and approved before adoption.

---

## 7. Refined next diagnostic boundary

Do not brute-force a large parameter grid.

Next bounded question:

> Can existing real monsters create the required SIEGER protection-time budget through **sequential frontmost handoff / layered pulse chronology**, without stat inflation and without proxy contamination?

Measure directly:
- SIEGER spawn time;
- SIEGER death / first-windup time;
- SIEGER x at death;
- number/type of live bodies physically ahead of SIEGER over time;
- frontmost-owner timeline;
- screen-handoff gaps;
- time for which SIEGER is exposed as the effective frontmost/attackable target;
- wall-contact source split;
- class-specific differences in that timeline.

Prefer a few deliberately constructed chronology families over broad combinatorial search.

A promising **diagnostic candidate** should first demonstrate meaningful SIEGER role opportunity in representative cases while preserving:
- normal-right-edge entry;
- all-class viable successful play;
- defense-heavy Knight viability;
- Tank slow-clear identity;
- Rogue low-AOE limitation;
- Archer line dependence;
- Mage density dependence;
- STAGE_SETTLED lifecycle and carried wall deficit.

Only after evidence exists should a concrete Stage48 working packet be proposed to the user for approval.

---

## 8. Current classification

```text
SIEGER_DEATH_POSITION_INSTRUMENTATION = PASS
REAL_MONSTER_SCREEN_WINDUP_CASES = 0
REAL_MONSTER_SCREEN_SHOT_CASES = 0
PRIMARY_CURRENT_FAILURE = PROTECTED_TRAVEL_TIME_SHORTFALL
SIEGER_WINDUP_CHANGE_JUSTIFIED = NO
GLOBAL_DURABILITY_INFLATION_JUSTIFIED = NO
NEW_STAGE48_PACKET_APPROVED = NO
NEXT = BOUNDED_LAYERED_SCREEN_HANDOFF_TIMELINE_DIAGNOSTIC
PRODUCTION_CHANGE = NONE
```
