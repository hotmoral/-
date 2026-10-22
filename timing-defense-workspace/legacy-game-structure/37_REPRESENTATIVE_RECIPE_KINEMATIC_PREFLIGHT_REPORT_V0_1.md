# Timing Defense — Representative Recipe Kinematic Preflight Report V0.1

Date: 2026-10-22 KST  
Status: **MOVEMENT/GEOMETRY PREFLIGHT / NO COMBAT-BALANCE FREEZE**

Inputs:
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/model_a_kinematic_anchor_v0_1.yaml`
- `tools/simulate_recipe_kinematics.py`

Live reference only:
- v0.45 capability chain
- `monster-capability-v1.js` coefficients explicitly marked provisional
- inherited spawn range reference from v0.35

---

# 0. 목적

Damage/kill을 넣기 전에 recipe의 전술 의도가 실제 movement/position에서 성립하는지 확인한다.

특히:
- CHARGER windup concurrency
- SUPPORTER aura opportunity / screened aura
- SIEGER first-shot timing / screen 여부
- formation X-depth 필요성
을 검사한다.

이 단계는 production balance가 아니라 geometry/kinematic sanity check다.

---

# 1. Provisional movement anchors

현재 live capability-test reference:

| Type | Provisional movement anchor |
|---|---|
| GRUNT | .070 |
| RUNNER | .135 |
| BRUTE | .040 |
| SHIELD | .057 |
| FLYER | .100 + Y oscillation |
| CHARGER | .060 / charge .210 / windup650ms |
| SPLITTER | .065 / child .115 |
| SUPPORTER | .055 / aura speed×1.18 / radius .18 |
| SIEGER | .045 / standoff .38 / windup800ms / repeat2200ms |

World preflight:
- wallX=.155
- deterministic spawnX=1.075
- 10ms integration

These values are NOT production balance authority.

---

# 2. Important structural defect found — backline depth

Initial recipe model used:
- spawn time
- Y
but effectively the same base X.

Problem:
SUPPORTER speed(.055) > BRUTE speed(.040).
Therefore a later SUPPORTER can still overtake a BRUTE and become exposed, even if authoring calls it `BACK`.

Conclusion:
> backline formation intent cannot rely only on spawn delay.

Formation requires an initial X-depth candidate.

This aligns with the existing formation schema's `depth/arrivalOffset` intent.

---

# 3. First formation X-depth candidates

Not production coordinates.

| Formation | Protected type | X offset candidate |
|---|---|---:|
| F06 SCREEN_BACKLINE | SUPPORTER | +.030 |
| F06 SCREEN_BACKLINE | SIEGER | +.100 |
| F07 ESCORT_COLUMN | SUPPORTER | +.120 |
| F07 ESCORT_COLUMN | SIEGER | +.120 |
| F08 SPLIT_AXIS | SIEGER | +.080 |
| F09 REPLICATION_CLUSTER | SUPPORTER | +.020 |

`+` means farther from wall / deeper backline relative to common spawn anchor.

F09 initially tried +.080 but CASCADE aura overlap fell to ~1.35s, weakening the intended support+replication interaction.
It was revised to +.020, giving ~3.52s screened-aura opportunity in the current representative recipe.

---

# 4. CHARGER telegraph concurrency

Movement-only no-interrupt preflight:

| Recipe | Charger count | Max simultaneous windups |
|---|---:|---:|
| T3_E07_M | 1 | 1 |
| T3_E13_H | 2 | 1 |
| T3_E17_M | 1 | 1 |
| T3_E20_L | 1 | 1 |

Interpretation:
- T3 E13_H uses two CHARGERs but current offsets stagger the telegraphs rather than overlapping them.
- good first high-pressure candidate because danger increases without simultaneous unreadable windup spam.

No combat interrupt modeled yet.

---

# 5. SUPPORTER kinematic opportunity

| Recipe | Formation | Aura-any opportunity | Screened-aura opportunity | Interpretation |
|---|---|---:|---:|---|
| T4_E09_M | F06 | ~3.92s | ~3.92s | standard readable support window |
| T4_E12_M | F07 | ~18.52s | ~18.52s | intentionally high BUFFED_BULWARK uptime; combat-balance WATCH |
| T4_E16_M | F09 | ~3.52s | ~3.52s | CASCADE interaction exists without excessive depth |
| T4_E19_M | F07 | ~18.91s | ~18.72s | FORTRESS high support uptime; expected high-complexity WATCH |

Interpretation:
- E09/E16 provide bounded standard support exposure.
- E12/E19 intentionally produce long protected aura opportunity and must be constrained by actual kill/screen simulation.

New lower-layer watch:
`SUPPORTER_UPTIME_TOO_HIGH` for E12/E19 candidate if combat sim confirms near-continuous effective aura.

---

# 6. SIEGER first-shot/screen behavior

| Recipe | Formation | First shot | Frontmost at shot | Screened? | Intended question |
|---|---|---:|---|---|---|
| T4_E10_M SIEGE_LINE | F06 | ~19.97s | SIEGER | No | focused siege, direct exposure |
| T4_E11_M ESCORT_SIEGE | F07 | ~20.47s | BRUTE | Yes | screen must be cleared while siege fires |
| T4_E18_M DUAL_AXIS | F08 | ~21.03s | SIEGER | No | aerial + siege dual-axis, not primarily durable screen |
| T4_E19_M FORTRESS | F07 | ~17.95s | BRUTE | Yes | high-complexity protected siege |

This is a strong structural result:
- E10 and E11 are mechanically distinct under actual movement.
- E18 remains dual-axis rather than accidentally becoming another escort-siege.
- E19 achieves the desired durable-screened first siege shot after depth offsets.

---

# 7. What kinematic preflight excludes

- player damage/kill time
- knockback
- CHARGER interrupt
- SPLITTER parent death and children
- Lv6/N3/Lv11+ damage
- actual Stage pressure
- actual clear/fail

Therefore screen/aura durations above are not final gameplay uptimes.
Combat can shorten them substantially.

---

# 8. New authoring implication

Formation data must include depth/X information in addition to:
- Y offset
- spawn timing
- nominal FRONT/MID/BACK role

A production authoring schema should be able to express something equivalent to:
```text
spawnXOffset / depthOffset
```
without changing runtime target authority.

The player still targets actual frontmost X; authoring only shapes positions.

---

# 9. Verdict

**KINEMATIC PREFLIGHT = PASS WITH WATCHES**

PASS:
- CHARGER telegraph concurrency bounded in representative recipes
- E10 focused siege vs E11 escorted siege distinction exists
- E19 durable-screened siege can be produced
- E09/E16 support interaction exists

WATCH:
- E12/E19 support aura uptime may be too long once real combat is modeled
- actual kill/knockback may materially change screen exposure
- SPLITTER still needs death-timing combat sim

Next required layer:
**Layer-A combat micro-simulation**, using candidate player-action profiles and provisional capability values without production freeze.
