# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# ACTIVE PHASE — Critical-Set Role-Expression V0.2 Rerun

Completed chain:

```text
Master Campaign Spine
 -> Layer-0 PASS
 -> Tier encounter envelope PASS
 -> static/kinematic/sensitivity preflight
 -> class-aware CURRENT_AUTHORITY V0.1
 -> Monster Role Expression Contract V0.1
 -> fine activation-window scan
 -> three-bracket robustness probe
 -> role-metrics instrumentation V0.2 READY
```

The blocker is no longer broad campaign structure and no longer "do CHARGER/SIEGER have any viable geometry?".

Current blocker:
> run the 10-recipe critical subset through V0.2 role telemetry and obtain a contract-based five-class PASS/acceptable-WATCH state.

---

# Read first

1. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
2. `legacy-game-structure/48_ROLE_EXPRESSION_FINE_SCAN_REPORT_V0_1.md`
3. `legacy-game-structure/50_CROSS_BRACKET_ROLE_EXPRESSION_ROBUSTNESS_V0_1.md`
4. `legacy-game-structure/52_ROLE_METRICS_V0_2_INSTRUMENTATION.md`
5. `legacy-game-structure/49_E11_SIEGE_TIMING_ADJUSTMENT_REPORT_V0_1.md`
6. `legacy-game-structure/51_PASSIVE_ROLE_STRUCTURAL_ANCHOR_REPORT_V0_1.md`
7. `legacy-game-structure/46_ROLE_EXPRESSION_ADMISSION_AUDIT_V0_1.md`
8. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
9. `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`

Machine-readable:
- `legacy-game-structure/data/monster_role_expression_contract_v0_1.yaml`
- `legacy-game-structure/data/role_expression_activation_search_v0_1.yaml` — now V0.2 content
- `legacy-game-structure/data/role_expression_activation_window_candidates_v0_1.yaml`
- `legacy-game-structure/data/model_a_role_expression_geometry_overrides_v0_1.yaml`
- `legacy-game-structure/data/model_a_class_action_trace_bracket_v0_1.yaml`
- `legacy-game-structure/data/model_a_representative_recipes_v0_1.yaml`

Tools:
- `tools/simulate_class_aware_layer_a.py` — V0.1 evidence-preserving simulator
- `tools/simulate_class_aware_role_metrics_v0_2.py` — new instrumentation lane
- `tools/evaluate_role_expression_v0_2.py`
- `tools/scan_activation_window_candidates.py` — separates SIEGER-shot damage from contact leak
- `tools/probe_sieger_readability_budget.py`
- `tools/probe_passive_role_contract_anchors.py`
- `tools/validate_monster_role_expression_contract.py`

---

# User-confirmed structural truth

- 5 classes; class Tier progression is independent.
- Same Tier/Stage combat content is shared by all classes.
- Tier = exactly 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class progression.
- recoverable soft walls intended; hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 does not expose all 9; higher Tiers add species.
- T5/T6/T7+ expansion remains open.
- fitted non-T1 `SKILLED_V2_CENTRAL` full-clear should normally be <60%.
- combo40 is skilled-achievable, not high-mastery-only.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application.
- intended encounters must not let a monster spawn and disappear before its role is meaningfully perceivable.

Role-expression rule:
```text
minimum role expression = required
readable counterplay     = required
full enemy activation    = NOT guaranteed
```

`PRE_EXPRESSION_DEATH_WITHOUT_READABLE_COUNTERPLAY` is invalid authoring.

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

# Fine activation results — diagnostic only

## CHARGER E07
Initial `0.20..0.40` search was too narrow.

Current evidence:
- all-five CENTRAL windup begins around `0.53`
- three-bracket all-five windup becomes robust around `~0.54`
- all-profile all-five region observed through roughly `0.64`

Current diagnostic anchor:
`~0.54`.

## CHARGER E17
Current strongest candidate:
`~0.49`.

At that probe:
- CONSERVATIVE 5/5 windup
- CENTRAL 5/5
- STRONG 5/5
- current probe wall damage = 0 for all three brackets

## SIEGER E11
All-five CENTRAL actual-shot window approximately `0.70..0.82`.

Low-change timing candidate:
```text
shift ~0.70
SHIELD 0ms
BRUTE 250ms
GRUNT 750ms
GRUNT 1000ms
SIEGER 1550ms
```

This removes the earlier CENTRAL ordinary contact leak while preserving all-five actual-shot expression.

Across brackets:
- actual shot completion is intentionally lower under STRONG
- readability proxy shows all five still reach a bounded standoff/windup opportunity
- weaker-trace wall-pressure timing remains WATCH until V0.2 wall-event classification is inspected

## SIEGER E19
Current lower candidate around `~0.70`.

CENTRAL:
- 5/5 actual-shot expression
- no ordinary contact leak at current probe anchor

STRONG:
- actual shots are prevented for some classes
- readability-budget proxy still shows all five structural response-state opportunity

---

# Passive-role anchors

Raw mechanical identities are sufficiently distinct to justify measurement rather than redesign:

- RUNNER: ~1.93× GRUNT speed; ~6.33s earlier common-spawn wall arrival in no-combat kinematic anchor
- BRUTE: 2.8125× GRUNT HP; same-hit knock displacement response ~44.7% of GRUNT
- SHIELD: 0.72 damage multiplier; 28% mitigation; ~750 raw-equivalent durability under current simple model
- FLYER: separate Y oscillation model exists; actual geometry value remains metric-dependent

Do NOT tune their global coefficients from these structural anchors.

---

# V0.2 role telemetry now available

New simulator records:

RUNNER:
- distance advanced
- alive/frontline time

BRUTE:
- frontline time
- hits received
- absorbed damage

SHIELD:
- mitigated hits
- prevented damage
- frontline time

FLYER:
- Archer line-opportunity ms
- Mage splash-opportunity ms
- actual secondary skill hits

CHARGER:
- windup entries
- windup visible ms
- interrupts/completions
- pre-windup erasure

SPLITTER:
- child alive ms
- child frontline ms
- split-driven target reorders
- peak-active delta

SUPPORTER:
- supporter alive ms
- unique aura target count
- screened-aura ratio

SIEGER:
- standoff/windup opportunity entries
- windup visible ms
- pre-opportunity erasure
- shot count remains separate outcome metric

Wall pressure:
- `wallDamageByType`
- `wallHitsByType`
- SIEGER shots keyed separately as `SIEGER_SHOT`

---

# EXACT NEXT BOUNDARY

Next bounded tranche:
**10-recipe Critical-Set Role-Expression V0.2 Rerun**.

Order:
1. apply diagnostic geometry overrides to a non-production candidate dataset
2. run 10 critical recipes × 3 trace brackets × 5 classes through V0.2
3. evaluate with `evaluate_role_expression_v0_2.py --require-all-five`
4. inspect CHARGER visible-windup ms, not charge completion only
5. inspect SIEGER opportunity/windup ms, not shot completion only
6. separate ordinary contact wall hits from intended special damage
7. verify SPLITTER children create a meaningful second state
8. verify SUPPORTER normalized aura is nontrivial in intended support encounters
9. verify RUNNER/BRUTE/SHIELD/FLYER direct role metrics
10. revise only localized recipe geometry/cadence if failures remain
11. require critical-set PASS/acceptable WATCH
12. then expand the same V0.2 audit to all 20 representative recipes
13. only after all-20 audit return to fitted SKILLED_V2 harness
14. synthetic Tier slices only after player model is fitted or sufficiently bounded

Do NOT yet:
- author exact 200 launch Stages
- freeze production HP/speed/armor/entry coordinates/trigger/standoff values
- promote current trace brackets to SKILLED_V2
- freeze final Tier count
- freeze exact EXP/star/achievement values
- change live gameplay code
- freeze boss/shop cadence
- start detailed 3P/4P production balance

Governance:
`structure -> encounter envelope -> role-expression contract -> candidate activation windows -> V0.2 critical audit -> all-20 audit -> fitted player model -> synthetic slice -> full Tier -> meta recovery -> explicit freeze -> implementation`.
