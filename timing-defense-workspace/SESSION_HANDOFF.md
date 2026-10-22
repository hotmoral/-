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

**Class-aware Layer-A Capability Window Calibration**

Broad campaign redesign is not the blocker anymore.
The current blocker is making CHARGER/SIEGER/SUPPORTER/SPLITTER capability expression robust under actual class behavior before synthetic Tier slices.

Read first:
1. `PROJECT_STATUS.md`
2. `NEXT_WORK.md`
3. `legacy-game-structure/42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`
4. `legacy-game-structure/44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`
5. `legacy-game-structure/43_ABSOLUTE_ENTRY_DEPTH_AMENDMENT_V0_1.md`
6. `legacy-game-structure/41_CLASS_AWARE_ACTION_TRACE_MODEL_V0_1.md`
7. `legacy-game-structure/40_LAYER_A_PREFLIGHT_ADMISSION_REPORT_V0_1.md`
8. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
9. `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`

Machine-readable:
- `legacy-game-structure/data/model_a_class_action_trace_bracket_v0_1.yaml`
- `legacy-game-structure/data/model_a_representative_recipes_v0_1.yaml`
- `legacy-game-structure/data/model_a_kinematic_anchor_v0_1.yaml`
- `legacy-game-structure/data/model_a_combat_sensitivity_anchor_v0_1.yaml`

Tools:
- `tools/simulate_class_aware_layer_a.py`
- `tools/sweep_special_activation_entry_depth.py`
- previous Layer-0/static/kinematic/sensitivity tools remain available

---

# USER-CONFIRMED STRUCTURAL TRUTH

- 5 classes; class-specific independent Tier progress.
- Same Tier/Stage combat content across classes.
- 1 Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars broad permanent account growth.
- achievements targeted cross-class growth.
- recoverable soft walls intended; hard class lockout forbidden.
- current 9 ordinary monsters are V1 foundation, not lifetime final roster.
- T1 does not expose all 9; higher Tiers introduce new monsters.
- future T5+ expansion remains open.
- non-T1 intended-entry fitted `SKILLED_V2_CENTRAL` full-clear should normally be <60%.
- combo40 is skilled-achievable, not high-mastery-only.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 is post-Lv31 mastery.
- Stage50 is final application, not Lv31 tutorial.

---

# MODEL A

Default bounded simulation spine:

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future expansion
```

NOT production frozen.
Model B remains fallback only if T4 lower-layer evidence fails.

---

# COMPLETED VALIDATION CHAIN

```text
Master Campaign Layer-0 PASS
 -> Encounter Envelope Layer-A0 PASS
 -> Static recipe PASS
 -> Kinematic PASS WITH WATCHES
 -> Generic DPS sensitivity COMPLETE
 -> Layer-A admission PASS
 -> Class-aware CURRENT_AUTHORITY micro-sim V0.1 COMPLETE
 -> Absolute entry-depth activation diagnostic COMPLETE
```

---

# CLASS-AWARE ACTION MODEL

Current exact authority included:
- base timing/heavy/combo damage
- Lv6 class authority
- N3 milestone authority
- current provisional v0.45 monster capability semantics

Excluded from headline V0.1:
- Lv11/16/21 parity candidate
- Lv26/31 future placeholder
- production meta/shop modifiers

Current trace bracket:
- CONSERVATIVE: 900 ms, 40 PERFECT judge streak then GOOD
- CENTRAL: 750 ms, 55 PERFECT judge streak then GOOD
- STRONG: 600 ms, 75 PERFECT judge streak then GOOD

These are **not fitted SKILLED_V2**.
They are optimistic deterministic mechanics probes with zero target-reacquire delay.

Do not use them to claim production clear probability.

---

# CRITICAL MICRO-SIM RESULT

10 critical recipes × 3 trace brackets × 5 classes = 150 CURRENT_AUTHORITY_LV6 diagnostic runs.

CENTRAL mean clear time over this subset:
- Mage ~4.725s
- Rogue ~5.016s
- Archer ~5.700s
- Knight ~8.100s
- Tank ~8.400s

This is diagnostic only.
Tank must not be evaluated by clear time alone because knockback/control can lengthen combat while protecting the wall.

Lv6 throughput delta is highly asymmetric:
- Mage/Rogue/Archer large
- Knight modest
- Tank utility-oriented and sometimes slower by clear-time metric

This requires multi-metric class opportunity analysis later.

---

# STATEFUL CAPABILITY FINDING

## CHARGER
Default critical T3 recipes:
- total observed windups across current class/trace sweep = 0
- CHARGER bodies are removed before windup

Result:
**default recipe geometry does not currently test CHARGER capability.**

## SIEGER
Default E11/E19:
- total shots across current class/trace sweep = 0

Result:
**default recipe geometry does not currently test SIEGER objective pressure.**

## SUPPORTER
Capability exists, but screened aura varies strongly by class/throughput.
Examples across brackets/classes:
- E12 ~0.155s to 11.855s
- E16 ~0.005s to 4.720s
- E19 ~1.205s to 5.405s

## SPLITTER
Parent->children transformation works.
Current optimistic critical traces produced no sampled child wall leak.

---

# ABSOLUTE ENTRY DEPTH

New structural distinction:

```text
relative depth = who is FRONT/MID/BACK inside formation
absolute entry depth = where the whole encounter starts on X
```

Both are required.

Diagnostic only, not production coordinates:
- T3_E17 all-five CHARGER windup visibility around ~0.45 X forward shift
- T4_E11 broad 5-class SIEGER shot visibility around ~0.70–0.80
- T4_E19 broad 5-class SIEGER shot visibility around ~0.75–0.80
- around ~0.85, SIEGER exposure can collapse again because it becomes too exposed and is deleted before firing

Thus capability activation is non-monotonic.
Do not use “closer = harder” as a scalar rule.

---

# EXACT NEXT BOUNDARY

Proceed with **stateful capability activation-window authoring**.

Order:
1. define bounded absolute entry-depth ranges for T3 E07/E17 CHARGER,
2. preserve reaction time and readable windup,
3. ensure interruption opportunity exists without making CHARGER trivial,
4. define SIEGER entry/spawn-time ranges that allow first-shot visibility without unavoidable wall damage,
5. preserve actual screening order,
6. rerun all five classes with CURRENT_AUTHORITY,
7. add role metrics:
   - Tank: wall-danger/control/interrupt value
   - Archer: line secondary realization
   - Mage: density/splash realization
   - Rogue: durable-target execution
   - Knight: generalist/current damage; later penetration only in parity mode
8. after critical capability-expression PASS, expand to all 20 representative recipes,
9. then fit/collect controlled SKILLED_V2 harness data,
10. synthetic Tier slices only after the player model is fitted or sufficiently bounded.

Do NOT yet:
- author exact 200 launch stages,
- freeze production monster coefficients,
- freeze the current trace brackets as SKILLED_V2,
- freeze final Tier count,
- freeze EXP/star/achievement values,
- change live gameplay code,
- freeze boss/shop cadence,
- start detailed 3P/4P production balance.

---

# HANDOFF DISCIPLINE

New session must:
1. fetch live branch HEAD,
2. read this handoff + PROJECT_STATUS + NEXT_WORK,
3. read docs 41–44,
4. verify no newer remote changes,
5. continue from capability activation-window calibration only.

Current tranche changes planning/corpus/data/analysis tools only.
No live gameplay source or production balance value was changed.
