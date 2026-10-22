# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# Current planning phase

**Class-aware Layer-A Capability Window Calibration**

Upstream campaign structure remains sufficiently closed.
Model A remains the default bounded simulation spine, not a production freeze.

Primary campaign authority:
- `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Current Layer-A evidence:
- `41_CLASS_AWARE_ACTION_TRACE_MODEL_V0_1.md`
- `42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`
- `43_ABSOLUTE_ENTRY_DEPTH_AMENDMENT_V0_1.md`
- `44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`

---

# Core user-confirmed truth

- 5 classes progress independently through Tiers.
- Same Tier/Stage combat content is shared across classes.
- 1 Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intentional; hard class lockout forbidden.
- current 9 ordinary monsters are not lifetime final roster.
- T1 does not teach all 9; higher Tiers introduce new monsters.
- future Tier/monster expansion open.
- non-T1 intended-entry fitted `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60%.
- combo40 is skilled-achievable.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery.
- Stage50 is final, not Lv31 tutorial.

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

# Current validation chain

- Master Campaign Layer-0: PASS, errors=0 warnings=0
- Encounter Envelope Layer-A0: PASS, errors=0 warnings=0
- Representative recipe static preflight: PASS
- Kinematic preflight: PASS WITH WATCHES
- Generic DPS sensitivity: COMPLETE
- Class-aware CURRENT_AUTHORITY micro-sim V0.1: COMPLETE for critical subset
- Absolute entry-depth activation diagnostic: COMPLETE

---

# Class-aware V0.1 findings

Critical set:
- 10 representative recipes
- 3 deterministic trace brackets
- 5 classes
- CURRENT_AUTHORITY_LV6

CENTRAL bracket mean clear time over the critical set:
- Mage ~4.725 s
- Rogue ~5.016 s
- Archer ~5.700 s
- Knight ~8.100 s
- Tank ~8.400 s

These are not production balance targets because the trace bracket is not fitted SKILLED_V2.

Lv6 clear-time effect is highly asymmetric in this diagnostic:
- Mage/Rogue/Archer gain large throughput
- Knight gains modest raw throughput
- Tank may clear slower because control/knockback is utility rather than DPS

Therefore class evaluation must be multi-metric.

---

# Stateful capability defect

Default representative geometry currently fails to express some Tier-defining mechanics under the optimistic class-aware traces.

CHARGER:
- sampled T3 representative recipes: 0 windups across the critical class/trace sweep
- special bodies are erased before windup

SIEGER:
- E11/E19: 0 shots across the critical class/trace sweep

SUPPORTER:
- capability remains present but screened-aura duration varies sharply by class/throughput

SPLITTER:
- transformation occurs; no sampled child wall leak under the current optimistic brackets

This is a recipe/capability-expression issue, not permission to buff HP globally.

---

# Absolute entry-depth result

New authoring distinction:
- relative depth = FRONT/MID/BACK ordering inside formation
- absolute entry depth = where the whole encounter enters the battlefield

Current diagnostics show non-monotonic activation windows.

Examples, not production coordinates:
- T3_E17 CHARGER all-five windup visibility around ~0.45 X shift toward wall
- T4_E11 SIEGER broad activation around ~0.70–0.80
- T4_E19 broad activation around ~0.75–0.80
- excessive forward shift can remove capability again by exposing the special too early

Thus the next task is an activation envelope, not a single coordinate.

---

# Player-trace authority boundary

Current trace bracket:
- 900 ms / perfect streak 40
- 750 ms / perfect streak 55
- 600 ms / perfect streak 75

Status:
**CALIBRATION BRACKET NOT FITTED**

It must not be promoted to SKILLED_V2.
Actual controlled harness/telemetry still needs to fit:
- cadence
- timing outcomes by context
- combo survival
- heavy/P×P completion
- target-turnover recovery
- pressure degradation

---

# Current exact work

Now allowed:
1. CHARGER/SIEGER absolute entry-depth and spawn-time window authoring
2. five-class capability activation/interrupt/shot visibility tests
3. role-specific metrics beyond clear time
4. repeat critical micro-sim after geometry revision
5. then expand to all 20 representative recipes

Not allowed yet:
- exact 200-Stage schedule
- production monster coefficient freeze
- fitted SKILLED_V2 claims from current brackets
- live campaign patch
- final Tier count
- exact EXP/star/achievement values
- boss/shop freeze
- detailed 3P/4P production balance

No live gameplay code or production balance value was changed by this tranche.
