# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production checkpoint
- branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes remain unauthorized

## Operating authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active dependency plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_23.yaml`
- live remote always wins
- do not rerun closed PASS/APPROVED work without a concrete trigger

---

# Current phase

**P4 PROVISIONAL STRUCTURAL COMPLETE_WITH_WATCHES / P5 A2 USER_APPROVED — FIVE-CLASS SHOP INTEGRATION DIRECTIONALLY COMPLETE / POST-SHOP LATE-PRESSURE RECONVERGENCE PROMISING**

```text
P0..P3 structural foundation complete
-> P4 player-power spine provisional structural complete with watches
-> P5 authority recovery complete
-> A2 USER APPROVED
-> spend-capacity preflight complete directionally
-> clear/kill income-mix sensitivity complete
-> Tank Iron Wall/SIEGER fidelity defect corrected directionally
-> Tank fixed-rank shop+combat preflight complete
-> five-class fixed-rank Stage49 shop+combat complete directionally
-> cross-class KNOCK fidelity gap isolated; KNOCK deferred
-> Fortification damage-deficit invariant corrected/canonicalized
-> post-shop Stage49 entry-depth/role-timing reconvergence PROMISING
-> exact committed replay + Stage46–48 post-shop reconvergence NEXT
```

No user decision is currently pending.

Latest P5 authority/evidence:
- `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `legacy-game-structure/117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
- `legacy-game-structure/118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
- `legacy-game-structure/119_P5_CLEAR_KILL_INCOME_MIX_SENSITIVITY_V0_1.md`
- `legacy-game-structure/121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md`
- `legacy-game-structure/122_P5_TANK_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `legacy-game-structure/123_P5_ALL_CLASS_SHOP_COMBAT_METHOD_FIDELITY_REVIEW_V0_1.md`
- `legacy-game-structure/124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `legacy-game-structure/125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
- `legacy-game-structure/126_P5_POST_SHOP_STAGE49_ENTRY_DEPTH_RECONVERGENCE_V0_1.md`
- `legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_directional_summary_v0_1.json`
- `legacy-game-structure/data/p5_post_shop_stage49_entry_depth_directional_summary_v0_1.json`
- `legacy-game-structure/data/p5_post_shop_stage49_entry_depth_fixture_v0_1.json`
- `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_1.py`
- `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`

---

# Stable upstream truth

- 5 classes: Knight / Rogue / Tank / Archer / Mage.
- Tier = 50 Stages.
- BaseHP persists across Stages; no automatic Stage heal.
- Lv31 acquisition direction = Stage41–45; Stage46+ mastery pressure.
- strong class-defining Lv31 finals remain bounded/deterministic/attributable.
- Archer wider straight gameplay corridor remains USER APPROVED.
- final EXP remains OPEN / P10R mandatory.
- production remains unchanged.

---

# P5 A2 — USER APPROVED

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
PERSONAL WALLETS
KILLER_ONLY PERSONAL ordinary-monster coin baseline
ALL-HUMAN Stage-clear income-floor candidate
FORTIFICATION = max HP increase + matched current increase
ATK/CRIT/CRITDMG/KNOCK = personal
FORTIFICATION/DEF = personal purchases contributing to shared wall
six shop categories
NO_ROUTINE_FULL_SHOP_MAXOUT_BY_STAGE49
```

No exact coin/reward/price/rank-effect/cap is frozen.

---

# Economy working centers — NOT FROZEN

Correct full-shop Rank10 legacy sensitivity cost:

```text
16360 nominal units
```

Spend capacity:

```text
45% = 7362
50% = 8180 <- working center
55% = 8998
```

Income source:

```text
80/20 clear/kill
70/30 <- working center
60/40
```

CENTER50 + 70/30 keeps moderate ±20% relative kill-share variation around ~47%..53% full-shop capacity.
No tested 45/50/55 economy-only policy maxed all six tracks.

---

# Cross-class shop-combat method correction

The current P4 late diagnostic kernel does not model ordinary push symmetrically across all five classes:
- Knight/Tank explicitly execute push paths;
- Rogue/Archer/Mage ordinary push behavior exists in the exact legacy reference but is not represented symmetrically in the simplified late kernel.

Therefore the first authoritative cross-class P5 lane is restricted to:

```text
ATK
FORTIFICATION
DEFENSE
```

Deferred:

```text
KNOCKBACK -> P5_KNOCKBACK_KERNEL_COVERAGE_GAP
CRIT / CRITDMG -> explicit attack-template policy lane required
```

Tank-only KNOCK sensitivity remains useful internally but is not cross-class evidence.

---

# Fortification semantic correction

Approved formula:

```text
wallMaxHp += delta
wallCurrentHp += delta
```

Therefore existing absolute damage deficit is invariant:

```text
D = max - current
D' = (max + delta) - (current + delta) = D
```

Canonical consequence:

```text
FORTIFICATION_ERASES_PRIOR_ATTRITION = FALSE
FORTIFICATION_ADDS_USABLE_RESERVE = TRUE
```

The fixed-rank Stage49 probe is optimistic because it starts with **pre-Stage49 damage deficit = 0**, not because Fortification healed prior damage.

Old language implying purchase-time repair wastage / old-damage erasure is superseded by doc125.

Active replacement watches:
- `FORTIFICATION_TOTAL_RESERVE_LEVERAGE`
- `PRE_STAGE49_DAMAGE_DEFICIT_CONTINUITY`
- `FORTIFICATION_DEATH_CHECK_TIMING`
- `SHARED_FORTIFICATION_PLAYER_COUNT_LEVERAGE`

---

# Five-class fixed-rank Stage49 result

At legacy-relative `30% / 40% / 50%`, four CENTER50 policy rank profiles were tested with ATK/FORT/DEF.

No-shop directional reconstruction first reproduced:

```text
Knight  success1705 / all-final-miss burial34.025s
Rogue   success2000 / burial29.100s
Tank    success2000 / corrected burial34.700s
Archer  success2000 / burial57.025s
Mage    success2000 / burial52.225s
```

Key result:
- Knight/Rogue/Tank remain mastery-sensitive at all 30/40/50 screens;
- Archer/Mage survive 60s all-finals-missed in the original Stage49 fixture after shop power;
- DEFENSE_HEAVY is not universally dominant;
- the Archer/Mage survival shift is driven primarily by **ATK changing kill/frontmost/SIEGER chronology**, not by generic DEF alone.

Thus:

```text
COMMON_40_PERCENT = useful diagnostic center
COMMON_40_PERCENT = NOT production recommendation
GLOBAL_SHOP_NERF = REJECT AS NEXT REPAIR LAYER
HIDDEN_CLASS_SHOP_COMPENSATION = REJECT AS NEXT REPAIR LAYER
```

---

# Archer low-order ATK breakpoint

A targeted trace found a brittle threshold in the old Stage49 diagnostic:

```text
Archer ordinary PERFECT before shop = 200 * 1.10 = 220
FLYER diagnostic HP = 225
```

With rank8 ATK:
- legacy-scale 0.03 -> total ATK +1.92% -> still buries at57.025s;
- legacy-scale 0.04 -> total ATK +2.56% -> crosses one-hit FLYER threshold and survives with wall765 in ATK-only stress.

First chronology divergence appears when the +2.56% path kills a FLYER one action earlier, freeing subsequent frontmost/penetration order and reducing later SIEGER/wall exposure.

Interpretation:
- do not simply raise FLYER HP;
- the late encounter recipe must be reconverged with shop power present.

Watch:
`P5_ARCHER_ATK_BREAKPOINT_CHRONOLOGY_WATCH = HIGH`

---

# Post-shop Stage49 authoring-first reconvergence

Repair order followed the existing principle: role timing / entry depth before blanket durability inflation.

Promising diagnostic family:

```text
TIME_BUDGET_SIEGER SIEGER entry x ~= 0.45..0.55
DURABLE_SCATTER/TIME_BUDGET durable entry x ~= 0.60..0.70
```

Useful directional center:

```text
TIME_BUDGET SIEGER x ~= 0.48
DURABLE/TIME_BUDGET durable x ~= 0.65
```

These are normalized diagnostic coordinates only — **not production authoring values**.
No monster HP/speed/wall damage, class coefficient or shop coefficient was changed.

At 40% ATK/FORT/DEF across 5 classes × 4 policies:

```text
all-success survival = 20/20
one-miss burials = 0
2-consecutive-miss burials = 0
```

All-finals-missed:
- Knight/Rogue/Tank bury in all policies;
- Archer/Mage either bury or enter Stage50 with severe reserve loss rather than healthy reserve;
- identical mistake budgets are not required.

Classification:

```text
POST_SHOP_PRESSURE_REPAIR_LAYER = AUTHORING ENTRY DEPTH / ROLE TIMING FIRST
ENTRY_DEPTH_ROLE_TIMING_DIRECTION = PROMISING
LV31_POWER_NERF_REQUIRED = NO
```

---

# Replay authority boundary

Current directional results are high-confidence reconstruction evidence, but new committed runners are not yet exact-admitted.

Pending exact checkout replay:
- `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
- `tools/run_p4d2_stage49_full_rotation_probe_v0_3.py`
- `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_1.py`
- `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`

Do not promote current diagnostic entry depths or 40% shop magnitude to production/freeze authority from directional evidence alone.

---

# Exact next boundary

1. exact committed replay of current Tank/P5 all-class/entry-depth runners when a valid checkout execution lane is available;
2. carry shop power into Stage46–48 and test whether the same authoring-language direction holds before final Stage49 authoring;
3. model ATK/DEF acquisition timing + inherited pre-Stage49 damage deficit; Fort purchase-time repair-wastage simulation is not needed;
4. create a policy-correct cross-class KNOCK inheritance lane;
5. create explicit CRIT/CRITDMG attack-template policy lane;
6. then re-measure purchase-policy combat feedback, valid timing-event count, EXP opportunity and Lv milestone reach;
7. final multiplayer normalization remains P10; final EXP convergence remains P10R.

P6 remains blocked pending P5 closure.
No user decision is currently pending.
No production change is authorized.
