# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# Current planning phase

**Critical-Set Role-Expression V0.2 Rerun**

Upstream campaign structure remains sufficiently closed.
Model A remains the default bounded simulation spine, not a production freeze.

Primary campaign authority:
- `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Current monster-role authority:
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `48_ROLE_EXPRESSION_FINE_SCAN_REPORT_V0_1.md`
- `50_CROSS_BRACKET_ROLE_EXPRESSION_ROBUSTNESS_V0_1.md`
- `52_ROLE_METRICS_V0_2_INSTRUMENTATION.md`

---

# Core user-confirmed truth

- 5 classes progress independently through Tiers.
- Same Tier/Stage combat content is shared across classes.
- 1 Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intentional; hard class lockout forbidden.
- current 9 ordinary monsters are V1 foundation, not lifetime final roster.
- T1 does not teach all 9; higher Tiers introduce new monsters.
- future Tier/monster expansion open.
- fitted non-T1 `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60%.
- combo40 is skilled-achievable.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery.
- Stage50 is final, not Lv31 tutorial.
- intended encounters must not allow a monster to spawn and disappear before its role is meaningfully perceivable.

Role-expression interpretation:
```text
minimum role expression = required
readable counterplay     = required
full enemy activation    = not guaranteed
```

Skilled counterplay after readable expression is valid.
`PRE_EXPRESSION_DEATH_WITHOUT_READABLE_COUNTERPLAY` is invalid authoring.

---

# Model A

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future expansion
```

Fallback Model B remains available only if T4 lower-layer evidence fails.

---

# Validation chain

- Master Campaign Layer-0: PASS, errors=0 warnings=0
- Encounter Envelope Layer-A0: PASS, errors=0 warnings=0
- Representative recipe static preflight: PASS
- Kinematic preflight: PASS WITH WATCHES
- Generic DPS sensitivity: COMPLETE
- Class-aware CURRENT_AUTHORITY micro-sim V0.1: COMPLETE for critical subset
- Monster Role Expression Contract V0.1: ESTABLISHED
- Fine activation-window scan: COMPLETE
- Three-bracket role-expression robustness probe: COMPLETE
- Passive-role structural anchor audit: COMPLETE
- Role-metrics V0.2 instrumentation: READY
- Critical-set V0.2 rerun: NEXT

---

# Current activation candidates — diagnostic only

These are normalized simulation offsets, not production coordinates.

## CHARGER E07
Earlier `0.20..0.40` search was too narrow.

Current evidence:
- all-five CENTRAL windup begins around ~0.53
- three-bracket all-five windup is robust around ~0.54
- broad all-profile role-expression region observed through roughly ~0.64

Current diagnostic anchor:
`~0.54`.

## CHARGER E17
Current strongest diagnostic anchor:
`~0.49`.

At this point under the current unfitted brackets:
- CONSERVATIVE 5/5 visible windup
- CENTRAL 5/5
- STRONG 5/5
- sampled wall damage = 0

## SIEGER E11
CENTRAL all-five actual-shot window approximately `0.70..0.82`.

Low-change timing candidate near `~0.70`:
```text
SHIELD 0ms
BRUTE 250ms
GRUNT 750ms
GRUNT 1000ms
SIEGER 1550ms
```

Only the two ordinary GRUNTs are delayed +250ms from the original representative recipe.
This removes the prior CENTRAL ordinary contact leak while preserving all-five actual-shot expression.

Actual shot completion is lower for STRONG traces, but SIEGER readability-budget probing shows all five classes still reach a bounded standoff/windup response state. This is valid skilled counterplay, not automatic role erasure.

E11 remains WATCH until V0.2 temporal wall-pressure evidence is inspected across brackets.

## SIEGER E19
Current lower diagnostic anchor:
`~0.70`.

CENTRAL:
- 5/5 actual-shot expression
- current decomposition shows no ordinary contact leak at anchor

STRONG:
- actual shot may be prevented by faster classes
- readability-budget proxy still shows five-class response-state opportunity

---

# Actual activation vs role opportunity

For CHARGER/SIEGER:

```text
role opportunity != full ability success
```

Therefore:
- CHARGER minimum gate = visible windup + response window, not completed charge
- SIEGER minimum gate = standoff/windup opportunity, not guaranteed shot

Strong players preventing the full ability after reading it is desirable mastery reward.

---

# Passive-role structural anchors

Current provisional mechanics are sufficiently separated to measure rather than redesign:

- RUNNER: speed ~1.93× GRUNT; no-combat common-spawn wall arrival ~6.33s earlier
- BRUTE: HP 2.8125× GRUNT; same-hit knock displacement response ~44.7% of GRUNT
- SHIELD: damage multiplier 0.72, 28% mitigation, ~750 raw-equivalent durability in current simple model
- FLYER: distinct Y oscillation model; actual combat geometry value still needs temporal role metrics

These are structural anchors only, not production balance freezes.

---

# Role Metrics V0.2

Existing V0.1 simulator is preserved unchanged for evidence reproducibility.

New analysis lane:
- `tools/simulate_class_aware_role_metrics_v0_2.py`
- `tools/evaluate_role_expression_v0_2.py`

V0.2 records:

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
- actual secondary hits

CHARGER:
- windup entries
- windup visible ms
- interrupts/completions
- pre-windup erasure

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
- windup visible ms
- pre-opportunity erasure
- shot count remains separate outcome metric

Wall pressure:
- `wallDamageByType`
- `wallHitsByType`
- SIEGER shot damage separated as `SIEGER_SHOT`

Important:
V0.2 is analysis tooling only and has not changed live gameplay semantics.

---

# Player-trace authority boundary

Current deterministic brackets remain unfitted:
- CONSERVATIVE: 900ms, PERFECT streak40 then GOOD
- CENTRAL: 750ms, streak55
- STRONG: 600ms, streak75

These are NOT `SKILLED_V2` production profiles.
They are mechanics probes.

---

# Current exact work

Now allowed:
1. apply diagnostic role-expression geometry overrides to a non-production candidate dataset
2. run 10 critical recipes × 3 brackets × 5 classes through V0.2
3. evaluate five-class minimum role expression automatically
4. inspect temporal wall-pressure ordering
5. make only localized geometry/cadence adjustments if failures remain
6. require critical-set PASS / acceptable WATCH
7. expand the same audit to all 20 representative recipes
8. then return to fitted SKILLED_V2 harness work

Not allowed yet:
- exact 200-Stage schedule
- production monster coefficient or entry-coordinate freeze
- fitted SKILLED_V2 claims from current brackets
- live campaign patch
- final Tier count
- exact EXP/star/achievement values
- boss/shop freeze
- detailed 3P/4P production balance

No live gameplay code or production balance value was changed by the current planning tranche.
