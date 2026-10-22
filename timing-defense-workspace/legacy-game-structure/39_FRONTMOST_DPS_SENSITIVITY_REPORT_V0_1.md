# Timing Defense — Frontmost DPS Sensitivity Report V0.1

Date: 2026-10-22 KST  
Status: **GENERIC COMBAT SENSITIVITY / NOT SKILLED-V2 OR PRODUCTION BALANCE**

Inputs:
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/model_a_kinematic_anchor_v0_1.yaml`
- `data/model_a_combat_sensitivity_anchor_v0_1.yaml`
- `tools/simulate_frontmost_dps_sensitivity.py`

---

# 0. 목적

SKILLED_V2 exact action profile을 아직 임의로 만들지 않은 상태에서, 대표 recipe가 **전열 제거 속도 변화에 얼마나 민감한지**를 검사한다.

이 시뮬레이션은 player skill profile이 아니다.
단일 frontmost target에 연속 raw DPS를 넣는 추상 probe다.

검사 질문:
- special capability가 낮은 DPS에서만 겨우 발동하는가?
- screen 제거 속도에 따라 SUPPORTER/SIEGER uptime이 얼마나 변하는가?
- SPLITTER child population이 어느 처리량에서 wall leak으로 변하는가?
- CHARGER가 high throughput에서 telegraph 자체를 보여주기 전에 삭제되는가?

---

# 1. Sweep model

Generic raw DPS probes:
```text
120 / 240 / 480 raw DPS
```

Included:
- frontmost-X target only
- current provisional HP/armor/wall-damage anchors
- SPLITTER children on parent death
- SUPPORTER aura movement effect
- CHARGER state timing
- SIEGER standoff/repeated shot

Excluded:
- crit
- knockback
- class skills
- N3
- heavy timing
- actual SKILLED_V2 action trace

Therefore these results are **mechanic sensitivity**, not difficulty/clear-rate authority.

---

# 2. T3 SPLITTER sensitivity

## T3_E08_M SPLIT_FLOOD

| Raw DPS | End time | Wall damage | Split children |
|---:|---:|---:|---:|
| 120 | ~16.14s | 170 | 4 |
| 240 | ~9.53s | 0 | 4 |
| 480 | ~4.80s | 0 | 4 |

Finding:
- population transformation still occurs across sweep,
- but low throughput allows meaningful child/wall leakage,
- medium+ throughput clears the current provisional package before wall damage.

## T3_E15_M REPLICATE_RUSH

| Raw DPS | End time | Wall damage | Split children |
|---:|---:|---:|---:|
| 120 | ~14.70s | 40 | 4 |
| 240 | ~7.58s | 0 | 4 |
| 480 | ~3.84s | 0 | 4 |

Interpretation:
REPLICATE pressure is strongly throughput-sensitive, but the mechanic itself remains visible because parent death still creates children.

---

# 3. CHARGER sensitivity

## T3_E13_H RUSH_BREACH

| Raw DPS | End time | Wall damage | Max simultaneous windups |
|---:|---:|---:|---:|
| 120 | ~11.85s | 0 | 1 |
| 240 | ~5.93s | 0 | 0 |
| 480 | ~2.99s | 0 | 0 |

Finding:
At medium/high generic throughput, current recipe can delete CHARGER before it reaches its trigger/windup.

This does not automatically mean the recipe is wrong because:
- the sweep has no class-specific target timing,
- no real action cadence,
- provisional HP/speed values.

But it creates an explicit lower-layer requirement:
> CHARGER teaching/high-pressure recipes must preserve a meaningful telegraph opportunity under intended-entry SKILLED_V2, not only under low throughput.

Failure candidate:
`CHARGER_MECHANIC_ERASED_BY_THROUGHPUT`.

---

# 4. SUPPORTER sensitivity

## T4_E09_M SUPPORT_COLUMN

| Raw DPS | End | Aura | Screened aura | Wall dmg |
|---:|---:|---:|---:|---:|
| 120 | ~13.10s | ~3.92s | ~3.92s | 0 |
| 240 | ~6.56s | ~3.70s | ~3.70s | 0 |
| 480 | ~3.29s | ~1.01s | ~1.01s | 0 |

Result:
Standard support recipe retains visible aura opportunity at low/medium throughput and compresses at very high throughput.

## T4_E12_M BUFFED_BULWARK

| Raw DPS | End | Aura | Screened aura | Wall dmg |
|---:|---:|---:|---:|---:|
| 120 | ~20.55s | ~18.52s | ~18.52s | 370 |
| 240 | ~13.86s | ~11.05s | ~11.05s | 0 |
| 480 | ~6.94s | ~4.71s | ~4.71s | 0 |

Result:
E12 is intentionally a high protected-aura recipe, but its effective pressure changes drastically with throughput.

This is a **calibration WATCH**, not a static structural failure.

---

# 5. CASCADE sensitivity

## T4_E16_M CASCADE

| Raw DPS | End | Wall dmg | Aura | Split children |
|---:|---:|---:|---:|---:|
| 120 | ~17.47s | 100 | ~3.52s | 2 |
| 240 | ~10.70s | 0 | ~3.52s | 4 |
| 480 | ~5.39s | 0 | ~1.81s | 4 |

Interpretation:
- low DPS can allow one parent/package to leak before all split events resolve,
- medium DPS creates full child transformation but no wall damage,
- very high DPS shortens the aura window materially.

This is exactly why authored count alone cannot define CASCADE difficulty.

---

# 6. SIEGER sensitivity

## T4_E11_M ESCORT_SIEGE

| Raw DPS | End | Siege shots | First shot | Wall dmg |
|---:|---:|---:|---:|---:|
| 120 | ~23.43s | 2 | ~20.47s | 150 |
| 240 | ~11.73s | 0 | — | 0 |
| 480 | ~5.87s | 0 | — | 0 |

## T4_E19_M FORTRESS

| Raw DPS | End | Siege shots | First shot | Aura | Screened aura | Wall dmg |
|---:|---:|---:|---:|---:|---:|---:|
| 120 | ~23.10s | 3 | ~17.95s | ~17.87s | ~15.53s | 225 |
| 240 | ~11.56s | 0 | — | ~8.50s | ~7.33s | 0 |
| 480 | ~5.79s | 0 | — | ~3.81s | ~3.22s | 0 |

Core finding:
> Current provisional SIEGER recipes are extremely throughput-sensitive.

At generic 240+ raw DPS, the protected package can be stripped before SIEGER fires at all.

That means production calibration cannot judge SIEGER by spawn count alone.
Required metrics:
- first-shot probability
- shot count distribution
- screened firing uptime
- screen removal time
- class-specific rear-target opportunity

New failure candidate:
`SIEGE_MECHANIC_ERASED_BY_THROUGHPUT`.

---

# 7. Structural interpretation

The sensitivity sweep does **not** invalidate Model A or the representative recipes.

What it proves:
1. special capability pressure depends heavily on actual player throughput,
2. kinematic intent alone is insufficient,
3. production HP/count changes must not be made before class-aware action simulation,
4. SUPPORTER/SIEGER calibration must use uptime/activation metrics,
5. CHARGER must be checked for telegraph visibility under real skilled throughput,
6. SPLITTER must be checked by effective population and child wall pressure.

---

# 8. Why no immediate numeric patch

It would be premature to respond by:
- increasing SIEGER HP,
- increasing CHARGER HP,
- adding more SUPPORTERs,
- increasing SPLITTER count.

The current sweep lacks:
- SKILLED_V2 real action cadence,
- class skills,
- N3,
- knockback/control,
- shop/run progression.

A global numeric patch now could overcorrect one class and create later snowball.

Correct next step:
**class-aware Layer-A combat micro-simulation**.

---

# 9. Verdict

**GENERIC DPS SENSITIVITY = PASS AS DIAGNOSTIC / HIGH CALIBRATION SENSITIVITY CONFIRMED**

No structural blocker found.
However, special capability uptime is now a first-class calibration axis before exact Stage scheduling.
