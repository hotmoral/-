# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Canonical recovery rule
Always re-read live `timing-defense-workspace` HEAD first.
Live remote wins over memory/chat/handoff.

## Current executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`
- no gameplay/numerical implementation authorized after v0.45

---

# CRITICAL CURRENT DIRECTION

The large campaign-structure + encounter-preflight tranche is complete through **Layer-A admission**.

Current phase:
**Class-aware Layer-A Combat Micro-Simulation**

Do NOT resume broad campaign redesign or exact 200-Stage authoring.
The blocker is now the class-aware player/action model and capability uptime under real class behavior, not the campaign spine.

---

# Read first

1. `PROJECT_STATUS.md`
2. `NEXT_WORK.md`
3. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
4. `legacy-game-structure/40_LAYER_A_PREFLIGHT_ADMISSION_REPORT_V0_1.md`
5. `legacy-game-structure/39_FRONTMOST_DPS_SENSITIVITY_REPORT_V0_1.md`
6. `legacy-game-structure/37_REPRESENTATIVE_RECIPE_KINEMATIC_PREFLIGHT_REPORT_V0_1.md`
7. `legacy-game-structure/36_REPRESENTATIVE_RECIPE_STATIC_PREFLIGHT_REPORT_V0_1.md`
8. `legacy-game-structure/35_LAYERA0_ENCOUNTER_ENVELOPE_VALIDATION_REPORT_V0_1.md`
9. `legacy-game-structure/38_FORMATION_DEPTH_SCHEMA_AMENDMENT_V0_1.md`
10. `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
11. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`

Machine-readable data:
- `legacy-game-structure/data/model_a_campaign_spine_v0_1.yaml`
- `legacy-game-structure/data/model_a_encounter_envelope_v0_1.yaml`
- `legacy-game-structure/data/model_a_representative_recipes_v0_1.yaml`
- `legacy-game-structure/data/model_a_kinematic_anchor_v0_1.yaml`
- `legacy-game-structure/data/model_a_combat_sensitivity_anchor_v0_1.yaml`

Tools:
- `tools/validate_campaign_spine.py`
- `tools/validate_encounter_envelope.py`
- `tools/analyze_representative_recipes.py`
- `tools/simulate_recipe_kinematics.py`
- `tools/simulate_frontmost_dps_sensitivity.py`

---

# USER-CONFIRMED STRUCTURAL TRUTH

- 5 classes: Knight / Rogue / Tank / Archer / Mage.
- Each class progresses independently through Tiers.
- Same Tier/Stage combat content is shared by all classes.
- 1 Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad account-wide permanent progression.
- achievements = targeted cross-class progression.
- recoverable soft walls are intentional.
- hard class lockout forbidden.
- current 9 ordinary monsters are V1 mechanical foundation, not lifetime final roster.
- T1 should not expose all 9.
- higher Tiers should introduce new monster types.
- future T5/T6/T7+ expansion remains open.
- non-T1 intended-entry `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60%.
- combo40 is skilled-achievable, not high-mastery-only.
- **Lv31 target unlock window = Stage41–45.**
- Stage46–49 is post-Lv31 mastery.
- Stage50 is final using an already-familiar Lv31.

---

# CURRENT MODEL A

```text
T1: G/R/B                Foundation / Timing & Frontline
T2: +SH/F                Mitigation / Geometry
T3: +C/SP                Burst / Transformation
T4: +SUP/SI              Formation / Siege
T5+: future content      Expansion
```

Status:
**default bounded simulation spine / NOT production freeze**

Fallback Model B:
- T4 +SUPPORTER
- T5 +SIEGER
- only if T4 lower-layer evidence fails.

---

# PLAYER POWER SPINE

First calibration candidate:
- Lv6 5–7
- Lv11 11–14
- Lv16 18–21
- Lv21 25–28
- Lv26 32–36
- Lv31 **41–45**

Only Lv31 window is user-confirmed.

Late-band contract:
```text
31–39 pressure / soft-wall build
40     2★ gate
41–45  Lv31 Ascension
46–49  post-Lv31 mastery
50     Tier Final
```

---

# VALIDATION CHAIN COMPLETED

## 1. Master Campaign Layer-0
PASS: `errors=0 warnings=0`.

## 2. Encounter Envelope Layer-A0
PASS: `errors=0 warnings=0`.

Legal encounter library grows:
- T1 3 archetypes
- T2 7
- T3 13
- T4 current E01–E20 full library

## 3. Representative static recipe preflight
PASS.
- 20 recipes
- max authored 4s=7
- max conservative effective 4s=10
- no density WATCH/ERROR

Static validation also caught and fixed one actual progression leak:
- T3 E17 initially used CD06 ESCORT
- CD06 is reserved as T4 cadence novelty
- recipe changed to CD07 LATE_INSERT

## 4. Kinematic preflight
PASS WITH WATCHES.

Confirmed:
- representative CHARGER simultaneous windup max1
- E10 focused siege differs from E11 escorted siege under actual movement
- E19 can create durable-screened first SIEGER shot
- E09/E16 have bounded SUPPORTER aura opportunity

Discovered:
`BACK` metadata + spawn delay alone cannot preserve actual backline geometry when speeds differ.

Resolution:
- formation authoring needs explicit initial X-depth capability (`spawnXOffset` design direction)
- target authority remains actual frontmost X; no manual target override

## 5. Generic frontmost-DPS sensitivity
Diagnostic complete.

Not a SKILLED_V2 model.
Raw probes: 120/240/480 DPS only for sensitivity.

Key findings:
- SIEGER can fire under low throughput and zero times under medium/high probes
- CHARGER can die before reaching windup under high throughput
- SUPPORTER aura duration changes sharply as screen removal speed changes
- SPLITTER wall leakage changes sharply with throughput

Conclusion:
capability uptime is a first-class calibration metric.
Do NOT respond by immediately buffing HP/count.

---

# FORMATION DEPTH DESIGN DIRECTION

Current simulation-only X-depth candidates:
- F06 SUPPORTER +.030
- F06 SIEGER +.100
- F07 SUPPORTER +.120
- F07 SIEGER +.120
- F08 SIEGER +.080
- F09 SUPPORTER +.020

These are NOT production coordinates.
They only prove tactical intent can be represented geometrically.

Canonical amendment:
`38_FORMATION_DEPTH_SCHEMA_AMENDMENT_V0_1.md`

---

# SOFT-WALL / META PRINCIPLE

Full-clear rate alone is insufficient.
Failure location determines star progression.

Preferred ordinary loop:
```text
late fail -> 1★/2★
 -> other classes progress
 -> permanent growth
 -> return
 -> previous wall becomes attainable
```

Avoid ordinary difficulty dominated by Stage1–19 0★ failure.

First Tier-unlock simulation hypothesis:
`CLEAR_LOCK` = same class Stage50 clear required to unlock next Tier.
Still OPEN.

---

# EXACT NEXT BOUNDARY

Proceed with **class-aware Layer-A combat micro-simulation**, not exact campaign schedules.

Required work:
1. deterministic action-trace representation,
2. explicit class normal/heavy/P×P behavior,
3. CURRENT_AUTHORITY / LEGACY_PARITY_CANDIDATE / FUTURE_SKILL_PLACEHOLDER separation,
4. SKILLED_V2 conservative/central/strong action traces or calibrated parameter sets,
5. representative recipes × five classes,
6. kill order / frontline block / target reorder / wall pressure,
7. CHARGER windup/completion/interrupt/erased-before-windup,
8. SPLITTER parent/children/population pressure,
9. SUPPORTER aura/screened-aura uptime,
10. SIEGER first-shot probability/shot count/screened firing uptime,
11. FLYER geometry opportunity,
12. class starvation/hard-lockout detection,
13. revise envelope,
14. only after PASS build synthetic Tier slices.

Do NOT yet:
- author exact 200 launch Stages,
- freeze production monster coefficients,
- freeze final Tier count,
- freeze EXP formula,
- freeze star/achievement reward values,
- change live gameplay code,
- freeze boss/shop cadence,
- start detailed 3P/4P production balance.

---

# PARKED / SUPERSEDED

Historical evidence only:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`

Do not resume these as current authority.

---

# Handoff discipline

New session must:
1. fetch live `timing-defense-workspace` HEAD,
2. read this handoff + PROJECT_STATUS + NEXT_WORK,
3. read Matrix V0.2 and Layer-A admission report,
4. verify no newer remote changes,
5. continue only from class-aware Layer-A boundary.

Current tranche changed planning/corpus/data/analysis tooling only.
No live gameplay code or production balance number was changed.
