# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Canonical recovery rule
Always fetch live `timing-defense-workspace` HEAD first.
Live remote wins over memory/chat/handoff.

## Current executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`
- no gameplay/numerical implementation authorized after v0.45

---

# CURRENT PHASE

**Critical-Set Role-Expression V0.2 Rerun**

Broad campaign redesign is not the blocker.
Fine activation scans found viable CHARGER/SIEGER geometry candidates without global HP inflation.
The current task is now to rerun the 10 critical representative recipes with direct per-monster role telemetry and automatic five-class contract evaluation.

---

# Read first

1. `PROJECT_STATUS.md`
2. `NEXT_WORK.md`
3. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
4. `legacy-game-structure/48_ROLE_EXPRESSION_FINE_SCAN_REPORT_V0_1.md`
5. `legacy-game-structure/50_CROSS_BRACKET_ROLE_EXPRESSION_ROBUSTNESS_V0_1.md`
6. `legacy-game-structure/52_ROLE_METRICS_V0_2_INSTRUMENTATION.md`
7. `legacy-game-structure/49_E11_SIEGE_TIMING_ADJUSTMENT_REPORT_V0_1.md`
8. `legacy-game-structure/51_PASSIVE_ROLE_STRUCTURAL_ANCHOR_REPORT_V0_1.md`
9. `legacy-game-structure/46_ROLE_EXPRESSION_ADMISSION_AUDIT_V0_1.md`
10. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
11. `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`

Machine-readable:
- `legacy-game-structure/data/monster_role_expression_contract_v0_1.yaml`
- `legacy-game-structure/data/role_expression_activation_search_v0_1.yaml` — file name retained; content version V0.2
- `legacy-game-structure/data/role_expression_activation_window_candidates_v0_1.yaml`
- `legacy-game-structure/data/model_a_role_expression_geometry_overrides_v0_1.yaml`
- `legacy-game-structure/data/model_a_class_action_trace_bracket_v0_1.yaml`
- `legacy-game-structure/data/model_a_representative_recipes_v0_1.yaml`
- `legacy-game-structure/data/model_a_kinematic_anchor_v0_1.yaml`
- `legacy-game-structure/data/model_a_combat_sensitivity_anchor_v0_1.yaml`

Tools:
- `tools/simulate_class_aware_layer_a.py` — preserve V0.1 evidence
- `tools/simulate_class_aware_role_metrics_v0_2.py` — current role telemetry lane
- `tools/evaluate_role_expression_v0_2.py`
- `tools/scan_activation_window_candidates.py`
- `tools/probe_sieger_readability_budget.py`
- `tools/probe_passive_role_contract_anchors.py`
- `tools/validate_monster_role_expression_contract.py`
- prior Layer-0/static/kinematic tools remain available

---

# USER-CONFIRMED STRUCTURAL TRUTH

- 5 classes; independent class Tier progress.
- Same Tier/Stage combat content across all classes.
- Tier = exactly 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class progression.
- recoverable soft walls intended; hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 does not expose all 9; higher Tiers introduce new species.
- future T5/T6/T7+ expansion remains open.
- fitted non-T1 `SKILLED_V2_CENTRAL` full-clear should normally be <60%.
- combo40 is skilled-achievable, not high-mastery-only.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 is post-Lv31 mastery.
- Stage50 is final application, not Lv31 tutorial.
- intended encounters must not let monsters spawn and disappear before their role becomes meaningfully perceivable.

---

# MONSTER ROLE-EXPRESSION RULE

Do not collapse these concepts:

```text
1. MINIMUM ROLE EXPRESSION
2. READABLE COUNTERPLAY
3. FULL ENEMY ACTIVATION
```

Rules:
- #1 and #2 required in designated role-expression encounters.
- #3 not guaranteed; skilled play may prevent it.
- `PRE_EXPRESSION_DEATH_WITHOUT_READABLE_COUNTERPLAY` is invalid authoring.
- global HP inflation is not the first fix.
- geometry / cadence / screen timing first.

Examples:
- CHARGER windup visible -> player interrupts = VALID
- CHARGER deleted before any windup = INVALID intended CHARGER encounter
- SIEGER standoff/windup visible -> strong player kills before shot = VALID
- SIEGER routinely disappears before standoff/windup opportunity = INVALID

---

# CURRENT NINE-MONSTER CONTRACT

- GRUNT: baseline exempt
- RUNNER: speed changes arrival/front-order behavior
- BRUTE: meaningful durable frontline/screening
- SHIELD: mitigation changes effective damage/hit investment
- FLYER: vertical geometry changes line/splash/target opportunities
- CHARGER: visible windup + readable response window
- SPLITTER: split creates meaningful post-death population/target-state change
- SUPPORTER: aura affects at least one non-self target for meaningful interval
- SIEGER: standoff + readable first-shot opportunity

Future monsters must define:
`coreMechanic / minimumRoleExpression / readableCounterplay / failureClass / requiredMetrics`.

---

# MODEL A

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future expansion
```

Status:
**default bounded simulation spine / NOT production freeze**.

---

# FINE-SCAN RESULTS

All values below are diagnostic normalized offsets, NOT production coordinates.

## E07 CHARGER
Initial fine search was too narrow.

Current cross-bracket evidence:
- around `~0.54`, CONSERVATIVE/CENTRAL/STRONG all 5/5 classes observe windup
- all-profile role-expression region continues broadly to about `~0.64`
- some CONSERVATIVE runs allow completed charge and wall impact after readable windup; that is later difficulty/counterplay, not spawn-delete failure

Diagnostic anchor:
`~0.54`.

## E17 CHARGER
Best current three-bracket anchor:
`~0.49`.

At that probe:
- CONSERVATIVE 5/5 windup
- CENTRAL 5/5
- STRONG 5/5
- sampled wall damage = 0

## E11 SIEGER
CENTRAL all-five actual-shot window roughly `0.70..0.82`.

Low-change timing candidate near `~0.70`:
```text
SHIELD   0ms
BRUTE    250ms
GRUNT    750ms
GRUNT    1000ms
SIEGER   1550ms
```

Only the two ordinary GRUNTs move +250ms from the original representative candidate.
CENTRAL current probe gives five-class actual-shot expression with zero ordinary contact leak.

Under STRONG, some classes kill before the full 800ms shot completes. This is not automatically a role failure.
SIEGER readability-budget proxy shows every class still has bounded standoff/windup response-state survival.

E11 remains WATCH because weaker-trace temporal contact-wall pressure must be inspected using V0.2 event decomposition.

## E19 SIEGER
Current lower anchor:
`~0.70`.

CENTRAL:
- all-five actual-shot expression
- zero ordinary contact leak in current decomposition

STRONG:
- some shots prevented by fast removal
- all five still retain bounded response-state opportunity in readability proxy

---

# PASSIVE ROLE ANCHORS

Raw mechanics are sufficiently differentiated to measure rather than redesign:

RUNNER:
- speed .135 vs GRUNT .070 = ~1.93×
- common-spawn wall arrival lead ~6.33s

BRUTE:
- HP900 vs GRUNT320 = 2.8125×
- knock response .38 vs .85 = ~44.7% of GRUNT displacement response

SHIELD:
- armor multiplier .72 = 28% mitigation
- current simple raw-equivalent durability ~750
- representative hit counts materially exceed GRUNT

FLYER:
- distinct Y oscillation exists
- actual role value still depends on line/splash geometry telemetry

These are analysis anchors, not production coefficient freezes.

---

# V0.2 ROLE TELEMETRY

Existing V0.1 simulator must remain untouched for reproducibility.

V0.2 adds direct metrics:

RUNNER:
- distance advanced / alive / frontline

BRUTE:
- frontline time / hits / damage absorbed

SHIELD:
- mitigated hits / prevented damage / frontline

FLYER:
- Archer line-opportunity ms
- Mage splash-opportunity ms
- actual secondary hits

CHARGER:
- windup entries / visible ms / interrupt / completion / pre-windup erasure

SPLITTER:
- child alive/frontline ms
- split-driven target reorder
- peak-active delta

SUPPORTER:
- supporter alive ms
- unique aura targets
- screened-aura ratio

SIEGER:
- standoff/windup opportunity entries
- visible windup ms
- pre-opportunity erasure
- actual shot remains a separate outcome

Wall pressure:
- `wallDamageByType`
- `wallHitsByType`
- SIEGER shots use `SIEGER_SHOT`

Automatic evaluator:
`tools/evaluate_role_expression_v0_2.py`
can require all-five structural expression.

Exact minimum milliseconds/probabilities remain OPEN until fitted SKILLED_V2.

---

# PLAYER-TRACE AUTHORITY BOUNDARY

Current trace brackets:
- CONSERVATIVE 900ms / 40 PERFECT then GOOD
- CENTRAL 750ms / 55
- STRONG 600ms / 75

They are **not fitted SKILLED_V2**.
They are deterministic mechanics probes.

---

# EXACT NEXT BOUNDARY

Proceed with **10-recipe Critical-Set Role-Expression V0.2 Rerun**.

Order:
1. build a non-production candidate recipe dataset applying current diagnostic overrides
2. run 10 critical recipes × 3 trace brackets × 5 classes through V0.2
3. run contract evaluator with all-five structural requirement
4. inspect CHARGER visible-windup time
5. inspect SIEGER opportunity/windup time, not guaranteed shot
6. inspect ordinary contact wall-hit timing separately from special ability damage
7. confirm SPLITTER meaningful second state
8. confirm SUPPORTER normalized aura expression
9. confirm RUNNER/BRUTE/SHIELD/FLYER direct roles
10. patch only localized recipe geometry/cadence if failures remain
11. close critical-set role-expression admission
12. expand same audit to all 20 recipes
13. then return to fitted SKILLED_V2 harness
14. synthetic Tier slices only after player model is fitted or sufficiently bounded

Do NOT yet:
- author exact 200 launch Stages
- freeze production monster coefficients or entry coordinates
- freeze the current trace brackets as SKILLED_V2
- freeze final Tier count
- freeze EXP/star/achievement values
- change live gameplay code
- freeze boss/shop cadence
- begin detailed 3P/4P production balance

---

# HANDOFF DISCIPLINE

New session must:
1. fetch live `timing-defense-workspace` HEAD
2. read PROJECT_STATUS + NEXT_WORK + this file
3. read docs 45,48,50,52,49,51,46
4. inspect role contract + candidate geometry data
5. verify no newer remote changes
6. continue only from the V0.2 critical-set rerun boundary

Current tranche changes planning/corpus/data/analysis tools only.
No live gameplay source or production balance value was changed.
