# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory or copied SHAs alone. Always fetch live remote first.

Read/check in this order:
1. live branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_23.yaml`
6. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
7. `legacy-game-structure/117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
8. `legacy-game-structure/118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
9. `legacy-game-structure/119_P5_CLEAR_KILL_INCOME_MIX_SENSITIVITY_V0_1.md`
10. `legacy-game-structure/121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md`
11. `legacy-game-structure/122_P5_TANK_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
12. `legacy-game-structure/123_P5_ALL_CLASS_SHOP_COMBAT_METHOD_FIDELITY_REVIEW_V0_1.md`
13. `legacy-game-structure/124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
14. `legacy-game-structure/125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
15. `legacy-game-structure/126_P5_POST_SHOP_STAGE49_ENTRY_DEPTH_RECONVERGENCE_V0_1.md`
16. `legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_directional_summary_v0_1.json`
17. `legacy-game-structure/data/p5_post_shop_stage49_entry_depth_fixture_v0_1.json`
18. `legacy-game-structure/data/p5_post_shop_stage49_entry_depth_directional_summary_v0_1.json`
19. `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_1.py`
20. `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`
21. `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
22. `tools/run_p4d2_stage49_full_rotation_probe_v0_3.py`
23. `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
24. prior P4 exact admission docs109–110 only when replay provenance is needed
25. current production/harness heads

Historical/supersession notes:
- doc113 is superseded where conflicting with docs115/116;
- doc114's `16350` full-shop figure is superseded by exact positive-JS-rounding `16360`;
- v0.5 / Stage49 v0.2 remain historical exact replay evidence, but Tank SIEGER-specific numerics are superseded directionally by doc121 pending v0.6/v0.3 exact replay;
- any text in docs120/122/earlier handoff implying approved Fortification reduces existing absolute damage deficit or has purchase-time repair wastage is superseded by doc125;
- all-class KNOCK conclusions must respect doc123's kernel-coverage gap.

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
P5 clear/kill source mix = 70/30 WORKING CENTER SUPPORTED / NOT FROZEN
P5 five-class fixed-rank shop combat = DIRECTIONAL COMPLETE
P5 cross-class KNOCK = DEFERRED_KERNEL_COVERAGE_GAP
P5 Fortification deficit invariant = CONFIRMED
P5 post-shop Stage49 entry-depth reconvergence = PROMISING DIRECTIONAL
P5 = ACTIVE / EXACT REPLAY + STAGE46–48 POST-SHOP RECONVERGENCE NEXT
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
NO_ROUTINE_FULL_SHOP_MAXOUT_BY_STAGE49
```

No exact numerical value is frozen.

---

# Economy working centers — NOT FROZEN

```text
full-shop Rank10 reference = 16360
spend capacity: 45% / 50% working center / 55%
income source: 80/20 / 70/30 working center / 60/40
```

CENTER50 + 70/30 keeps moderate ±20% relative kill-share wallet variation around ~47%..53% full-shop capacity.
No tested economy-only policy maxed all six tracks.

---

# Tank fidelity correction

Tank Lv11 Iron Wall is shared-wall incoming ×0.90 and has no SIEGER exception.

Corrected directional no-shop Stage49 Tank:

```text
all success wall2000
one miss wall2000
two-miss minimum1732.5
all-finals-missed burial34.700s
first burial LINE6 / CLUSTER6 / FRONTLINE5 / DURABLE5 / TIME_BUDGET5
```

P4 structural closure remains intact.
Exact committed v0.6 / Stage49 v0.3 replay is pending.

---

# Cross-class shop-method boundary

Legacy exact formulas show ordinary push behavior for all classes, but the current simplified P4 late kernel models explicit `push()` only in Knight/Tank paths.

Therefore first five-class P5 shop authority uses:

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

Do not interpret zero modeled KNOCK value for Rogue/Archer/Mage as product truth.

---

# Fortification invariant — important correction

Approved formula:

```text
max += delta
current += delta
```

For absolute damage deficit `D=max-current`:

```text
D'=(max+delta)-(current+delta)=D
```

Therefore:
- Fortification adds immediately usable durability;
- it does not heal old accumulated absolute damage;
- Fort purchase timing alone does not create `repair wastage` if incoming-damage history is otherwise identical;
- order still matters if the wall dies before a later purchase;
- ATK/DEF timing matters because it changes future incoming damage history.

The fixed-rank Stage49 lane is optimistic because it starts with pre-Stage49 deficit0.

---

# Five-class fixed-rank result

No-shop reconstruction reproduced current class baselines before shop effects.

At 30/40/50 legacy-relative ATK/FORT/DEF screens:
- Knight/Rogue/Tank remain mastery-sensitive;
- Archer/Mage become too forgiving in the original Stage49 fixture;
- Defense-heavy is not universally dominant;
- the major Archer/Mage driver is ATK changing kill/frontmost/SIEGER chronology.

Archer low-order breakpoint watch:

```text
ordinary PERFECT before shop = 220
FLYER diagnostic HP = 225
rank8 ATK at legacy-scale .03 -> +1.92% -> burial57.025s
rank8 ATK at legacy-scale .04 -> +2.56% -> one-hit threshold crossed -> survives wall765 in ATK-only stress
```

This is encounter brittleness, not an instruction to raise FLYER HP.

---

# Post-shop Stage49 reconvergence

Authoring-first role-entry timing/depth was tested before scalar inflation.

Diagnostic search:

```text
TIME_BUDGET SIEGER x ~= .45..55
DURABLE/TIME_BUDGET durable x ~= .60..70
```

Promising center:

```text
SIEGER x ~= .48
durable x ~= .65
```

These are **not production coordinates**.

At 40% ATK/FORT/DEF across ATTACK_HEAVY / DEFENSE_HEAVY / BALANCED / ROLE_AWARE and all five classes:

```text
all-success: 20/20 survive
one missed final: 0 burials
two consecutive missed finals: 0 burials
```

All-finals-missed:
- Knight/Rogue/Tank bury across policies;
- Archer/Mage bury or carry severe/non-healthy Stage50 reserve;
- class mistake budgets remain asymmetric.

Thus the current repair direction is:

```text
AUTHORING ENTRY DEPTH / ROLE TIMING FIRST
NOT global shop nerf
NOT hidden per-class shop compensation
NOT Lv31 power nerf
```

---

# Exact replay authority boundary

Directional reconstruction is strong but current committed runners have not yet received exact checkout execution/admission.

Pending:
- `run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
- `run_p4d2_stage49_full_rotation_probe_v0_3.py`
- `run_p5_all_class_fixed_rank_shop_stage49_probe_v0_1.py`
- `run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`

Do not promote x=.48/.65 or common40% to freeze/production authority.

---

# Exact next boundary

1. exact committed replay when a valid checkout execution lane exists;
2. carry shop power backward into Stage46–48 and test authoring reconvergence across the full Lv31 mastery window;
3. model ATK/DEF acquisition timing and inherited wall deficit; do not build a fake Fort repair-wastage model;
4. resolve KNOCK cross-class inheritance/parity;
5. resolve CRIT/CRITDMG template policies;
6. re-run purchase-policy combat feedback and P4 EXP/skill-reach feedback;
7. final multiplayer normalization at P10;
8. final EXP convergence at P10R.

Do not yet freeze:
- 50% spend capacity;
- 70/30 source mix;
- 40% common shop scale;
- x=.48/.65 entry depths;
- exact coin/reward/price/rank/effect values;
- generic DR cap;
- KNOCK inheritance;
- universal CRIT policy;
- final EXP;
- production implementation.
