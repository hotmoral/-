# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# ACTIVE PHASE — Class-aware Layer-A Combat Micro-Simulation

The large structure/authoring preflight tranche is now closed through:

```text
Master Campaign Spine
 -> Layer-0 structural validation PASS
 -> Tier encounter envelope PASS
 -> representative recipe static preflight PASS
 -> kinematic preflight PASS WITH WATCHES
 -> generic DPS sensitivity diagnostic COMPLETE
 -> Layer-A preflight admission PASS
```

Canonical admission review:
`legacy-game-structure/40_LAYER_A_PREFLIGHT_ADMISSION_REPORT_V0_1.md`

---

# Read first

1. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
2. `legacy-game-structure/40_LAYER_A_PREFLIGHT_ADMISSION_REPORT_V0_1.md`
3. `legacy-game-structure/39_FRONTMOST_DPS_SENSITIVITY_REPORT_V0_1.md`
4. `legacy-game-structure/37_REPRESENTATIVE_RECIPE_KINEMATIC_PREFLIGHT_REPORT_V0_1.md`
5. `legacy-game-structure/36_REPRESENTATIVE_RECIPE_STATIC_PREFLIGHT_REPORT_V0_1.md`
6. `legacy-game-structure/35_LAYERA0_ENCOUNTER_ENVELOPE_VALIDATION_REPORT_V0_1.md`
7. `legacy-game-structure/38_FORMATION_DEPTH_SCHEMA_AMENDMENT_V0_1.md`
8. `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
9. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`

Machine-readable inputs:
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

# User-confirmed structural truth

- 5 classes progress independently through Tiers.
- Same Tier/Stage content is shared across classes.
- Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad permanent account growth.
- achievements = targeted cross-class growth.
- recoverable soft walls are intentional; hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 does not expose all 9; higher Tiers introduce new monsters.
- future T5/T6/T7+ expansion remains open.
- non-T1 intended-entry `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60%.
- combo40 is skilled-achievable, not high-mastery-only.
- **Lv31 target unlock window = Stage41–45.**
- Stage46–49 = post-Lv31 mastery.
- Stage50 = final using an already-familiar Lv31 skill.

---

# Current bounded simulation spine — Model A

```text
T1: GRUNT / RUNNER / BRUTE
T2: +SHIELD / +FLYER
T3: +CHARGER / +SPLITTER
T4: +SUPPORTER / +SIEGER
T5+: future expansion
```

Status:
**default bounded simulation spine / NOT production freeze**

Model B fallback:
- T4 +SUPPORTER
- T5 +SIEGER

Only switch if lower-layer T4 evidence fails.

---

# Validation/preflight status

## Master campaign Layer-0
`PASS errors=0 warnings=0`

## Encounter envelope Layer-A0
`PASS errors=0 warnings=0`

## Representative recipe static preflight
PASS.
- 20 deterministic representative recipes
- max authored 4s density = 7
- max conservative effective 4s density = 10
- no current density WATCH/ERROR

## Kinematic preflight
PASS WITH WATCHES.

Confirmed:
- T3 representative CHARGER windup concurrency max1
- E10 focused siege vs E11 escorted siege geometry is mechanically distinct
- E19 durable-screened first SIEGER shot can be realized
- SUPPORTER aura opportunity exists in E09/E12/E16/E19

Discovered/fixed:
- `BACK` role cannot rely only on delayed spawn when unit speeds differ
- formation authoring now requires actual initial X-depth capability (`spawnXOffset` design direction)

## Generic frontmost-DPS sensitivity
Diagnostic complete.

Key finding:
- special capability pressure is highly throughput-sensitive
- SIEGER can fire multiple times under low generic DPS but zero times at medium/high probes
- CHARGER can be killed before windup under high throughput
- SUPPORTER aura uptime changes sharply with screen removal speed
- SPLITTER wall leakage changes sharply with throughput

Therefore production HP/count patching before class-aware simulation is prohibited.

---

# EXACT NEXT BOUNDARY

Next bounded tranche = **class-aware Layer-A combat micro-simulation**.

Order:
1. define deterministic action-trace representation,
2. represent class-specific normal/heavy/P×P/timing sequences,
3. run explicit model modes:
   - CURRENT_AUTHORITY
   - LEGACY_PARITY_CANDIDATE
   - FUTURE_SKILL_PLACEHOLDER only where required,
4. create/fill `SKILLED_V2_CONSERVATIVE/CENTRAL/STRONG` action traces or calibrated parameter sets,
5. simulate representative recipes × 5 classes,
6. measure kill order/frontline block/target reorder/wall damage,
7. measure CHARGER windup/complete/interrupt/erased-before-windup,
8. measure SPLITTER parent death/children/child occupancy,
9. measure SUPPORTER aura/screened-aura uptime,
10. measure SIEGER first-shot probability/shot count/screened firing uptime,
11. measure FLYER geometry opportunity,
12. classify class starvation/hard-lockout/power-cliff defects,
13. revise recipes/envelope,
14. only after Layer-A PASS build synthetic Tier slices.

Do NOT yet:
- assign exact recipes to all 200 launch candidate Stages,
- freeze production HP/speed/armor/wall damage,
- freeze final launch Tier count,
- freeze exact EXP formula,
- freeze star/achievement reward values,
- change live gameplay code,
- freeze boss/shop cadence,
- start detailed 3P/4P production balance.

## Governance
`Master Spine -> Layer0 -> Encounter Envelope -> Static/Kinematic/Sensitivity Preflight -> Class-aware Layer-A -> Synthetic Slice -> Full Tier -> Soft-wall Map -> Meta Recovery -> Explicit Freeze -> Implementation`.
