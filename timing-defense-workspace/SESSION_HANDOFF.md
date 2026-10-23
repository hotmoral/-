# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory or copied SHAs alone. Always fetch live remote first.

Read/check in this order:
1. live branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_24.yaml`
6. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
7. `legacy-game-structure/124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
8. `legacy-game-structure/125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
9. `legacy-game-structure/126_P5_POST_SHOP_STAGE49_ENTRY_DEPTH_RECONVERGENCE_V0_1.md` — spatial proof only
10. `legacy-game-structure/127_P5_STAGE46_49_RIGHT_EDGE_TRAVEL_LEAD_PREFLIGHT_V0_1.md`
11. `legacy-game-structure/128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
12. `legacy-game-structure/data/p5_stage46_49_right_edge_lead_fixture_v0_1.json`
13. `legacy-game-structure/data/p5_stage46_49_right_edge_lead_preflight_summary_v0_1.json`
14. `legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json`
15. `tools/run_p5_stage46_49_right_edge_lead_preflight_v0_1.py`
16. `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`
17. `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
18. `tools/run_p4d2_stage49_full_rotation_probe_v0_3.py`
19. `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
20. current production/harness heads

Historical/supersession notes:
- doc113 is superseded where conflicting with docs115/116;
- doc114's `16350` full-shop figure is superseded by exact positive-JS-rounding `16360`;
- old Tank SIEGER-specific v0.5/v0.2 numerics are superseded directionally by doc121 pending v0.6/v0.3 exact replay;
- any old Fortification wording implying prior absolute damage is healed is superseded by doc125;
- doc126's row-level mid-field `spawnX` is a spatial-pressure proof only, not an implementation direction;
- user clarified all actual enemies should continue to enter from the right side; no mid-field pop-in.

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
P4 Tank Iron Wall/SIEGER correction = DIRECTIONAL PASS / EXACT V0.6/V0.3 PENDING
P5 A2 structural contract = USER_APPROVED
P5 economy-only preflight = DIRECTIONAL PASS
P5 clear/kill source mix = 70/30 WORKING CENTER / NOT FROZEN
P5 five-class fixed-rank shop combat = DIRECTIONAL COMPLETE
P5 KNOCK cross-class = DEFERRED_KERNEL_COVERAGE_GAP
P5 Fortification deficit invariant = CONFIRMED
P5 old Stage49 spawnX experiment = SPATIAL PRESSURE PROOF ONLY
P5 right-edge travel lead preflight = COMPLETE DIRECTIONALLY
P5 right-edge escorted Stage46-49 search = PROMISING DIRECTIONAL
P5 = ACTIVE / PACKET CHRONOLOGY + SOURCE-PATCHED RIGHT-EDGE RUNNER NEXT
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
```

No user decision is currently pending.

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

# Cross-class shop-method boundary

First current cross-class lane:

```text
ATK
FORTIFICATION
DEFENSE
```

Deferred:

```text
KNOCKBACK -> dedicated parity/inheritance lane
CRIT / CRITDMG -> attack-template policy-correct lane
```

Do not interpret missing Rogue/Archer/Mage push in the simplified P4 late kernel as product truth.

---

# Fortification invariant

```text
max += delta
current += delta
```

Existing absolute damage deficit remains unchanged.
Fortification adds usable reserve but does not heal old attrition.

---

# User clarification: actual spawn behavior

The user asked whether the previous `closer placement` meant earlier right-edge appearance or sudden mid-field spawn.

Canonical answer:

```text
NO MID-FIELD POP-IN.
Enemies continue to appear from the normal right edge.
```

Earlier pressure must be authored through schedule timing and escort relationships.

Doc126 is retained only because it proved that deeper role pressure could repair the post-shop Stage49 margin.

---

# Right-edge travel preflight

Equivalent untouched travel from normal x=.92:

```text
old SIEGER x=.48 -> ~9.78s lead
old durable x=.65 -> 6.75s lead
```

But a naked SIEGER cannot simply be moved 8–10s earlier.
At current shop diagnostic power it often dies in 2–3 ordinary roots, while those lead windows expose it to many more roots.

Therefore:

```text
MIDFIELD_POP_IN = REJECTED
NAKED_EARLY_SIEGER = REJECTED
ESCORT_OR_FRONTMOST_PROTECTION = REQUIRED
```

---

# Escorted Stage46–49 search

Best current gameplay direction:

```text
Stage46 = power revelation / relatively forgiving
Stage47 = transition / recovery room
Stage48 = first protected role pulse
Stage49 = stronger escorted second pulse
```

First diagnostic cadence family:

```text
46 ~5.8s
47 ~5.3s
48 ~4.9s
49 ~4.6s
```

Not production values.

Directional search lessons:

1. Too many durable front bodies protect SIEGER but can make defense-heavy Knight unfairly weak.
2. Weak escort trains alone can be cleared too quickly by attack-heavy Archer.
3. The remaining problem is relative packet chronology: which body is frontmost when the SIEGER reaches its role window.
4. Successful mastery does not require shop/Lv31 nerfs to remain survivable.
5. Repeated final failure can accumulate severe damage across Stage48–49, but attack-heavy Archer still has some overly safe chronology paths.

High watches:

```text
P5_ATK_HEAVY_ARCHER_REPEATED_FAILURE_MARGIN_WATCH
P5_DEFENSE_HEAVY_KNIGHT_OVERPRESSURE_WATCH
P5_RIGHT_EDGE_ESCORT_PACKET_CHRONOLOGY_WATCH
```

Repair order:

```text
relative spawn timing
-> frontmost escort composition
-> band/line alignment
-> first/second pulse spacing
-> durability sensitivity
-> class/shop coefficients last
```

Do NOT jump to:
- hidden Archer penalty;
- global shop nerf;
- Lv31 nerf;
- blanket monster HP inflation.

---

# Exact replay authority boundary

Current right-edge combat work is directional evidence only.

Pending exact/source-patched authority:
- `run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
- `run_p4d2_stage49_full_rotation_probe_v0_3.py`
- `run_p5_all_class_fixed_rank_shop_stage49_probe_v0_1.py`
- `run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`
- future Stage46–49 source-patched `spawnLeadSeconds` runner

Do not freeze current cadence, lead seconds, packet composition or shop scale.

---

# Exact next boundary

1. create source-patched Stage46–49 runner with normal right-edge spawn and schedule-only `spawnLeadSeconds`;
2. carry wall HP/deficit through Stage46→49;
3. refine Stage49 packet specifically against attack-heavy Archer while preserving defense-heavy Knight successful viability;
4. preserve one/two-miss recovery checks;
5. exact-admit pending runners when a valid checkout execution lane exists;
6. then KNOCK parity/inheritance;
7. then CRIT/CRITDMG policy;
8. then purchase-policy combat feedback and P4 EXP/Lv reach feedback;
9. final multiplayer P10; final EXP P10R.

No user decision is currently pending.
No production change is authorized.
