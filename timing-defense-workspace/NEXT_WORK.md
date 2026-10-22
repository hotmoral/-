# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# ACTIVE PHASE — SKILLED_V2 Controlled Harness / Player-Model Fitting

Completed lower-layer chain:

```text
Master Campaign Spine
 -> Layer-0 PASS
 -> Tier encounter envelope PASS
 -> static/kinematic/sensitivity preflight
 -> class-aware CURRENT_AUTHORITY V0.1
 -> Monster Role Expression Contract
 -> fine activation calibration
 -> Role Metrics V0.2
 -> Critical 10-Recipe Role Audit PASS_WITH_WATCHES
 -> All-20 Representative Role Audit PASS_WITH_WATCHES
```

Current representative encounter geometry is now sufficient to stop broad role-expression tuning.
The next blocker is the player model itself.

---

# Read first

1. `legacy-game-structure/54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
2. `legacy-game-structure/53_CRITICAL_ROLE_EXPRESSION_V0_2_RERUN_REPORT_V0_1.md`
3. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
4. `legacy-game-structure/52_ROLE_METRICS_V0_2_INSTRUMENTATION.md`
5. `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
6. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Machine-readable candidate overlays:
- `legacy-game-structure/data/model_a_critical_role_expression_candidates_v0_1.yaml` — content V0.2
- `legacy-game-structure/data/model_a_additional10_role_expression_candidates_v0_1.yaml`
- `legacy-game-structure/data/model_a_class_action_trace_bracket_v0_1.yaml`
- `legacy-game-structure/data/monster_role_expression_contract_v0_1.yaml`

Tools:
- `tools/materialize_critical_role_candidates.py` — generalized role-candidate materializer
- `tools/simulate_class_aware_role_metrics_v0_2.py`
- `tools/evaluate_role_expression_v0_2.py`
- previous Layer-0 / role-expression diagnostic tools remain evidence tools

---

# User-confirmed structural truth

- 5 classes; independent class Tier progression.
- Same Tier/Stage combat content across classes.
- Tier = 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class progression.
- recoverable soft walls intended; hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 does not expose all 9; higher Tiers introduce species.
- future T5/T6/T7+ and additional monsters remain open.
- fitted non-T1 `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60%.
- combo40 is skilled-achievable, not high-mastery-only.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application.
- intended monster roles must be perceivable before deletion; successful enemy activation is not guaranteed.

---

# Current Model A

```text
T1: GRUNT / RUNNER / BRUTE
T2: +SHIELD / +FLYER
T3: +CHARGER / +SPLITTER
T4: +SUPPORTER / +SIEGER
T5+: future expansion
```

Status:
**default bounded simulation spine / NOT production freeze**.

---

# Role-expression admission status

## Critical 10
`PASS_WITH_WATCHES`.

## Full 20 representative recipes
`PASS_WITH_WATCHES`.

Audit population:
```text
20 recipes × 3 deterministic brackets × 5 classes = 300 combat rows
36 designated recipe-role pairs × 15 rows = 540 structural role checks
540 / 540 structural role gates PASS
```

Important:
- current brackets are NOT fitted SKILLED_V2
- exact minimum readable ms/rates remain OPEN
- candidate coordinates/timings are NOT production values

Remaining WATCHES include:
- E20 CHARGER lower-tail readable window ~250ms
- FLYER geometry lower tails ~255–325ms
- modest RUNNER advance in some high-pressure rows
- conservative wall pressure after SIEGER response opportunity

These do not justify more geometry tuning before player calibration.

---

# EXACT NEXT BOUNDARY

Next bounded tranche = **SKILLED_V2 controlled harness and fitting preparation**.

Order:
1. define machine-readable H0–H5 harness cases from the existing measurement protocol
2. define event/telemetry schema for timing, combo, heavy/P×P, turnover, pressure context
3. preserve user anchor: combo40 must be ordinary skilled-achievable, not tail-only
4. separate `SKILLED_V2_CONSERVATIVE / CENTRAL / STRONG` from `HIGH_MASTERY_STRESS`
5. fit or bound:
   - action cadence
   - PERFECT/GOOD/NORMAL/MISS by context
   - combo survival
   - heavy completion / P×P completion
   - target-turnover reacquisition
   - pressure degradation
6. validate fitted traces against role-expression candidates so strong play does not falsely erase mechanics
7. only after the player model is sufficiently fitted/bounded, build a 10-Stage synthetic Tier slice
8. then expand toward full Tier and the `<60%` non-T1 skilled-clear gate

Do NOT yet:
- author exact 200 launch Stages
- freeze production monster coefficients or candidate entry coordinates
- promote current 600/750/900ms brackets to SKILLED_V2
- freeze final Tier count
- freeze exact EXP/star/achievement values
- change live gameplay code
- freeze boss/shop cadence
- start detailed 3P/4P production balance

Governance:
`structure -> encounter envelope -> role-expression PASS -> fitted player model -> synthetic slice -> full Tier -> soft-wall/meta recovery -> explicit freeze -> implementation`.
