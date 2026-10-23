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
6. `legacy-game-structure/data/system_dependency_calibration_order_v0_25.yaml`
7. `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
8. `legacy-game-structure/data/p5_class_identity_radar_invariants_v0_1.yaml`
9. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
10. `legacy-game-structure/124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
11. `legacy-game-structure/125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
12. `legacy-game-structure/127_P5_STAGE46_49_RIGHT_EDGE_TRAVEL_LEAD_PREFLIGHT_V0_1.md`
13. `legacy-game-structure/128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
14. `legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json`
15. `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`
16. `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
17. `tools/run_p4d2_stage49_full_rotation_probe_v0_3.py`
18. `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
19. current production/harness heads

Historical/supersession notes:
- doc113 is superseded where conflicting with docs115/116;
- doc114's `16350` full-shop figure is superseded by exact positive-JS-rounding `16360`;
- any old Fortification wording implying prior absolute damage is healed is superseded by doc125;
- doc126's mid-field `spawnX` is spatial-pressure proof only, not implementation direction;
- all actual enemies must continue to enter from the normal right edge;
- class selection radar values are now a balance-identity guard through doc129, not merely presentation metadata.

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
P5 class identity radar invariant gate = USER-DIRECTED ACTIVE
P5 = ACTIVE / IDENTITY METRIC INTEGRATION INTO SOURCE-PATCHED RIGHT-EDGE RUNNER NEXT
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

# A2 approved truth

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
PERSONAL WALLETS
KILLER_ONLY PERSONAL ordinary-monster coin baseline
ALL-HUMAN Stage-clear income-floor candidate
FORTIFICATION = max HP + matched current increase
ATK/CRIT/CRITDMG/KNOCK personal
FORTIFICATION/DEF purchases contribute to shared wall
six categories retained
NO_ROUTINE FULL-SHOP MAXOUT BY STAGE49
```

No exact numerical value is frozen.

Working centers remain analysis-only:

```text
full-shop Rank10 reference = 16360
spend capacity = 45% / 50% center / 55%
income source = 80/20 / 70/30 center / 60/40
cross-class ATK/FORT/DEF diagnostic magnitude = 30/40/50%, center40
```

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

Naked early SIEGER is rejected. Escort/frontmost chronology is the promising pressure tool.

Existing encounter watches:

```text
P5_ATK_HEAVY_ARCHER_REPEATED_FAILURE_MARGIN_WATCH
P5_DEFENSE_HEAVY_KNIGHT_OVERPRESSURE_WATCH
P5_RIGHT_EDGE_ESCORT_PACKET_CHRONOLOGY_WATCH
```

New identity watches:

```text
P5_TANK_SURVIVAL_NOT_CLEAR_WATCH
P5_TANK_SOLO_CLEAR_THROUGHPUT_WATCH
P5_ROGUE_WAVE_CLEANUP_LEAKAGE_WATCH
P5_ARCHER_LINE_DEPENDENCE_WATCH
P5_MAGE_DENSITY_DEPENDENCE_WATCH
P5_KNIGHT_PENETRATION_CAUSALITY_WATCH
```

---

# Source-patched runner requirements

The next Stage46–49 runner must:
- keep every mob at normal `spawnX=0.92`;
- implement earlier pressure using schedule-only `spawnLeadSeconds`;
- carry wall current/max/deficit through Stage46→49;
- preserve no-target/no-bank, Rogue cadence sensitivity, Tank barrier non-downgrade and Tank Iron Wall on SIEGER;
- keep current cross-class shop scope to ATK/FORT/DEF until policy-correct KNOCK/CRIT lanes;
- measure class identity, not just wall survival.

Mandatory new outputs:

```text
stageClearTime
unfinishedAtHorizon
totalKills
totalDamage
endActiveBacklog
uniqueTargetsPerRootPackage
secondaryDamageShare
penetrationHitCount / penetrationDamageShare
controlDisplacementOrSlowTime
wallContactsPrevented
formationTag / alignmentTag / densityTag
```

Paired probes:

```text
Knight: aligned/frontline vs dispersed/off-axis
Rogue: one durable normal vs broad weak/multi-direction wave
Tank: wall survival vs actual solo completion time/backlog
Archer: aligned line vs staggered/scatter/off-corridor
Mage: clustered durable vs distributed durable
```

Do not freeze pass thresholds before collecting first comparable distributions.

---

# Exact replay authority boundary

Current right-edge combat work is directional evidence only.

Pending exact/source-patched authority:
- `run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
- `run_p4d2_stage49_full_rotation_probe_v0_3.py`
- `run_p5_all_class_fixed_rank_shop_stage49_probe_v0_1.py`
- `run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`
- future Stage46–49 source-patched runner with identity metrics

---

# Exact next boundary

1. integrate radar identity metrics into the Stage46–49 source-patched right-edge runner;
2. measure Tank actual solo finish time/backlog;
3. run paired identity probes for Knight/Rogue/Archer/Mage;
4. only after identity output exists, refine Stage49 chronology against attack-heavy Archer without destroying defense-heavy Knight or other class identities;
5. preserve one/two-miss recovery checks and carried wall deficit;
6. exact-admit pending fidelity runners when valid execution is available;
7. then KNOCK parity/inheritance;
8. then CRIT/CRITDMG policy;
9. then purchase-policy combat feedback and P4 EXP/Lv reach feedback;
10. final multiplayer P10; final EXP P10R.

No user decision is currently pending.
No production change is authorized.
