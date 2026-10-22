# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# ACTIVE PHASE — Bounded Simulation Authoring

The Master Campaign Spine tranche is now **closed enough for bounded simulation input authoring**.

Read first:
1. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
2. `legacy-game-structure/30_LAYER0_MODEL_A_VALIDATION_REPORT_V0_1.md`
3. `legacy-game-structure/28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`
4. `legacy-game-structure/29_MODEL_A_TIER_PRESSURE_COMPLEXITY_ENVELOPE_V0_1.md`
5. `legacy-game-structure/22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
6. `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
7. `legacy-game-structure/25_MODEL_A_META_PROGRESS_VOLUME_AND_SOFT_WALL_ENVELOPE_V0_1.md`
8. `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
9. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
10. `legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`

Machine-readable:
- `legacy-game-structure/data/model_a_campaign_spine_v0_1.yaml`
- `tools/validate_campaign_spine.py`

---

# User-confirmed structural truth

- 5 classes progress independently through Tiers.
- Same Tier/Stage combat content is shared across classes.
- Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls are intentional.
- hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 should not expose all 9.
- higher Tiers introduce new monsters.
- future T5/T6/T7+ monster/Tier expansion remains open.
- non-T1 intended-entry `SKILLED_V2` full-Tier clear <60%.
- combo40 = skilled-achievable, not high-mastery-only.
- **Lv31 target unlock window = Stage41–45.**
- Stage46–49 = post-Lv31 mastery-use band.
- Stage50 = final using an already-familiar Lv31 skill.

---

# Current bounded simulation spine — Model A

Status:
**ADMITTED FOR BOUNDED SIMULATION / NOT PRODUCTION FREEZE**

```text
T1: GRUNT / RUNNER / BRUTE
T2: +SHIELD / +FLYER
T3: +CHARGER / +SPLITTER
T4: +SUPPORTER / +SIEGER
T5+: future expansion
```

Model B fallback:
- T4 +SUPPORTER
- T5 +SIEGER

Only switch if lower-layer T4 testing fails.

Layer-0 result:
```text
PASS errors=0 warnings=0
```

---

# Player power spine candidate

- Lv6: Stage5–7
- Lv11: 11–14
- Lv16: 18–21
- Lv21: 25–28
- Lv26: 32–36
- Lv31: **41–45**

Late band:
```text
31–39 pressure / soft wall
40     2★ gate
41–45  Lv31 Ascension
46–49  post-Lv31 mastery
50     Tier Final
```

Only Lv31 window is user-confirmed.
Other reach bands remain calibration candidates.

---

# Soft-wall principle

Do not create desired difficulty mainly via repeated Stage1–19 failure.

Preferred ordinary soft-wall shape:
```text
late fail -> 1★/2★
 -> other-class progression
 -> permanent growth
 -> return
 -> blocked class advances/clears
```

Tier unlock first simulation hypothesis:
`CLEAR_LOCK` = same class must clear Stage50 to unlock next Tier.
This is not frozen.

---

# Parked / superseded for active planning

- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`

Historical evidence only.

---

# EXACT NEXT BOUNDARY

Next bounded tranche = **Tier encounter-authoring envelope**, still not production balance.

Order:
1. map encounter archetypes E01–E20 to Tier availability under Model A roster limits,
2. remove/disable archetypes that reference unavailable monsters in earlier Tiers,
3. define Tier-specific formation availability,
4. define Tier-specific cadence availability,
5. convert LOW/MED/HIGH pressure envelopes to bounded candidate frequency ranges,
6. define complexity-frequency ranges by Tier,
7. create representative encounter recipes per Tier using candidate values only,
8. run static burst/entity/readability checks,
9. Layer-A micro-sim for representative recipes,
10. revise before any 50-Stage exact schedule.

Do not yet:
- freeze production HP/speed/armor/wall damage,
- assign exact recipes to all 200 launch candidate Stages,
- implement live campaign code,
- freeze star reward coefficients,
- invent achievement reward values,
- expand 3P/4P detailed balance,
- freeze boss/shop cadence.

## Governance
`master spine -> Layer0 PASS -> encounter envelope -> micro-sim -> synthetic slices -> full Tier sim -> soft-wall map -> meta recovery -> explicit freeze -> implementation`.
