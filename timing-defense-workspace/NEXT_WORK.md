# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# ACTIVE PHASE — Class-aware Layer-A Capability Window Calibration

Completed chain:

```text
Master Campaign Spine
 -> Layer-0 PASS
 -> Tier encounter envelope PASS
 -> static recipe preflight PASS
 -> kinematic preflight PASS WITH WATCHES
 -> generic DPS sensitivity COMPLETE
 -> Layer-A admission PASS
 -> class-aware CURRENT_AUTHORITY micro-sim V0.1 COMPLETE
 -> absolute entry-depth activation diagnostic COMPLETE
```

Current key docs:
1. `legacy-game-structure/42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`
2. `legacy-game-structure/44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`
3. `legacy-game-structure/43_ABSOLUTE_ENTRY_DEPTH_AMENDMENT_V0_1.md`
4. `legacy-game-structure/41_CLASS_AWARE_ACTION_TRACE_MODEL_V0_1.md`
5. `legacy-game-structure/40_LAYER_A_PREFLIGHT_ADMISSION_REPORT_V0_1.md`
6. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Data/tools:
- `legacy-game-structure/data/model_a_class_action_trace_bracket_v0_1.yaml`
- `legacy-game-structure/data/model_a_representative_recipes_v0_1.yaml`
- `legacy-game-structure/data/model_a_kinematic_anchor_v0_1.yaml`
- `legacy-game-structure/data/model_a_combat_sensitivity_anchor_v0_1.yaml`
- `tools/simulate_class_aware_layer_a.py`
- `tools/sweep_special_activation_entry_depth.py`

---

# Current authoritative design truth

- same Tier/Stage content across all five classes
- class progression independent
- 50 Stage per Tier
- 0/1/2/3★ boundaries remain 1–19 / 20–39 / 40–49 / Stage50 clear
- stars broad account growth; achievements targeted cross-class growth
- recoverable soft walls allowed; hard class lockout forbidden
- Model A remains default bounded simulation spine:
  - T1 G/R/B
  - T2 +SH/F
  - T3 +C/SP
  - T4 +SUP/SI
- future T5+ expansion open
- non-T1 intended-entry fitted `SKILLED_V2_CENTRAL` full-clear target remains <60%
- combo40 must remain skilled-achievable
- Lv31 target window remains Stage41–45

---

# New class-aware findings

Critical subset:
- 10 representative recipes
- 3 unfitted deterministic trace brackets
- 5 classes
- CURRENT_AUTHORITY_LV6

Headline diagnostics:
- Mage/Rogue/Archer clear much faster than Knight/Tank in the current optimistic trace bracket.
- Tank clear time alone is a bad utility metric because knockback can lengthen combat while protecting the wall.
- default T3 CHARGER representative recipes produced **0 windups** across the critical trace/class sweep.
- default T4 E11/E19 SIEGER produced **0 shots** across the critical trace/class sweep.
- SUPPORTER remains active but screened-aura duration varies strongly by class/throughput.
- SPLITTER population transformation occurs, but current optimistic brackets produced no child wall leak in the sampled recipes.

These results are structural diagnostics, not production balance verdicts.

---

# Absolute entry-depth finding

Relative FRONT/MID/BACK depth is not sufficient.
The whole encounter's absolute entry position is a separate authoring axis.

Current diagnostic only:
- T3_E17 CHARGER all-five windup visibility emerged around ~0.45 X shift toward wall.
- T4_E11 SIEGER broad 5-class shot visibility appeared around ~0.70–0.80 X shift.
- T4_E19 broad 5-class shot visibility appeared around ~0.75–0.80 X shift.
- too much forward shift can remove capability again because the special becomes exposed/frontmost and dies during windup.

Therefore activation is **non-monotonic**.
These coordinates are NOT production values.

---

# EXACT NEXT BOUNDARY

Next bounded tranche = **stateful capability activation-window authoring**.

Order:
1. formalize absolute entry-depth candidate ranges for T3 CHARGER recipes,
2. preserve first-teach reaction/readability time,
3. preserve relative screen/backline order,
4. find CHARGER windows where windup is visible and interruptable rather than erased,
5. formalize SIEGER entry/spawn-time windows without unavoidable wall damage,
6. require SIEGER first-shot visibility across multiple classes while retaining class asymmetry,
7. rerun CURRENT_AUTHORITY five-class micro-sim,
8. add normalized role metrics for Tank control and Archer/Mage/Rogue geometry/throughput,
9. only after capability-expression PASS expand from critical subset to all 20 representative recipes,
10. then fit/collect actual SKILLED_V2 harness data,
11. synthetic Tier slice only after fitted or sufficiently bounded player model exists.

Do NOT yet:
- author exact 200 Stage campaign,
- freeze production HP/speed/armor/trigger/standoff values,
- promote the current 600/750/900 ms trace brackets to SKILLED_V2,
- freeze final Tier count,
- freeze EXP/star/achievement values,
- change live gameplay code,
- freeze boss/shop cadence,
- start detailed 3P/4P production balance.

Governance:
`structure -> encounter envelope -> class-aware capability expression -> fitted player model -> synthetic slice -> full Tier -> meta recovery -> explicit freeze -> implementation`.
