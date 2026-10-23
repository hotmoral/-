# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory or copied SHAs alone. Always fetch live remote first.

Read/check in this order:
1. live branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CHARACTER_PROFILE_RADAR_V1.md`
5. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
6. `legacy-game-structure/data/system_dependency_calibration_order_v0_26.yaml`
7. `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
8. `legacy-game-structure/130_P5_CLASS_IDENTITY_FINITE_PACKET_PROBE_PREFLIGHT_V0_1.md`
9. `legacy-game-structure/data/p5_class_identity_radar_invariants_v0_1.yaml`
10. `legacy-game-structure/data/p5_class_identity_radar_probe_fixture_v0_1.json`
11. `tools/run_p5_class_identity_radar_probe_v0_1.py`
12. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
13. `legacy-game-structure/124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
14. `legacy-game-structure/128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
15. `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`
16. `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
17. `tools/run_p4d2_stage49_full_rotation_probe_v0_3.py`
18. current production/harness heads

Historical/supersession notes:
- doc113 is superseded where conflicting with docs115/116;
- doc114's `16350` full-shop figure is superseded by exact positive-JS-rounding `16360`;
- any old Fortification wording implying prior absolute damage is healed is superseded by doc125;
- doc126's mid-field `spawnX` is spatial-pressure proof only, not implementation direction;
- all actual enemies must continue to enter from the normal right edge;
- character radar values are now an active balance-identity guard through doc129;
- wall survival alone must not be interpreted as Tank solo-clear quality.

Do not rerun closed P1/P2/P3/P4 wholesale solely because a new session starts.

---

# Branch checkpoints

Planning:
- `timing-defense-workspace`
- fetch exact live HEAD after recovery.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- current P5 work did not change it.

---

# Current exact phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 structural contract = USER_APPROVED
P5 five-class fixed-rank shop combat = DIRECTIONAL COMPLETE
P5 KNOCK cross-class = DEFERRED_KERNEL_COVERAGE_GAP
P5 Fortification deficit invariant = CONFIRMED
P5 right-edge escorted Stage46-49 search = PROMISING DIRECTIONAL
P5 class identity radar gate = USER-DIRECTED ACTIVE
P5 finite-packet identity runner + fixture = AUTHORED / EXECUTION PENDING
P5 = ACTIVE / COMMITTED IDENTITY PROBE EXECUTION NEXT
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
```

No user decision is currently pending.

---

# Radar identity authority

Approved character radar:

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

Interpretation:
- these are not literal hidden coefficient levels;
- high axes must remain causally visible strengths;
- low axes must remain materially visible weaknesses after skills/shop growth.

Current class status:

```text
Knight = STRUCTURALLY_ALIGNED_WITH_WATCH
Rogue  = STRUCTURALLY_ALIGNED_WITH_LV31_WAVE_CLEANUP_WATCH
Tank   = POSITIVE_CONTROL_IDENTITY_CONFIRMED / NEGATIVE_SOLO_THROUGHPUT_VALIDATION_GAP
Archer = CORE_LINE_IDENTITY_PRESENT / POST_SHOP_GENERALIST_CREEP_HIGH_WATCH
Mage   = STRONGLY_ALIGNED / LATE_PRESSURE_MARGIN_WATCH
```

User Tank clarification:

```text
Tank solo parity is not a target.
Tank should be excellent at survival/control but poor at enemy removal.
Late solo clear should be near-impractical under ordinary tempo or materially slower/frustrating than damage classes.
No absolute hard lockout is required.
```

Critical rule:

```text
TANK SURVIVAL != TANK CLEAR
WALL PRESERVATION != DAMAGE THROUGHPUT
```

---

# Finite-packet identity probe

Runner:
`tools/run_p5_class_identity_radar_probe_v0_1.py`

Fixture:
`legacy-game-structure/data/p5_class_identity_radar_probe_fixture_v0_1.json`

The runner reuses the existing P5 v0.2 shop-combat kernel.
It does not create a new combat model.

Current cross-class shop scope:

```text
ATK
FORTIFICATION
DEFENSE
```

KNOCK / CRIT / CRITDMG remain deferred.

Direct-clear predicate:

```text
all expected enemies killed by player
AND wallHits == 0
AND endActive == 0
AND wall survives
```

If false at maximum scan horizon, mark unfinished.

First interpretation order:

1. Tank mixed-solo direct clear time / unfinished rate / 30-60-90s backlog.
2. Archer ATTACK_HEAVY aligned line vs scatter.
3. Mage cluster vs distributed.
4. Rogue durable execution vs broad-wave cleanup leakage.
5. Knight aligned/frontline vs dispersed/off-axis and defense-heavy viability.

No exact pass threshold is frozen before first committed output.

---

# Current right-edge direction

```text
NO MID-FIELD POP-IN.
All enemies physically enter from normal right edge.
```

Best current gameplay direction:

```text
Stage46 = power revelation / relatively forgiving
Stage47 = transition / recovery room
Stage48 = first protected role pulse
Stage49 = stronger escorted second pulse
```

Do not resume Stage49 packet tuning until class-identity evidence exists.

---

# Existing + new watches

```text
P5_ATK_HEAVY_ARCHER_REPEATED_FAILURE_MARGIN_WATCH
P5_DEFENSE_HEAVY_KNIGHT_OVERPRESSURE_WATCH
P5_RIGHT_EDGE_ESCORT_PACKET_CHRONOLOGY_WATCH
P5_TANK_SURVIVAL_NOT_CLEAR_WATCH
P5_TANK_SOLO_CLEAR_THROUGHPUT_WATCH
P5_ROGUE_WAVE_CLEANUP_LEAKAGE_WATCH
P5_ARCHER_LINE_DEPENDENCE_WATCH
P5_MAGE_DENSITY_DEPENDENCE_WATCH
P5_KNIGHT_PENETRATION_CAUSALITY_WATCH
```

---

# Exact next boundary

1. execute committed `run_p5_class_identity_radar_probe_v0_1.py`;
2. persist raw JSON output and verify deterministic/direct-clear behavior;
3. classify Tank throughput first;
4. classify Archer/Mage/Rogue/Knight paired identity results;
5. integrate the useful metrics into a source-patched Stage46–49 right-edge runner with carried wall deficit;
6. only then return to Stage49 packet chronology tuning;
7. exact-admit pending P4/P5 fidelity runners when an execution lane is available;
8. then KNOCK parity/inheritance;
9. then CRIT/CRITDMG policy;
10. then purchase-policy combat feedback and P4 EXP/Lv reach feedback;
11. final multiplayer P10; final EXP P10R.

No user decision is currently pending.
No production change is authorized.
