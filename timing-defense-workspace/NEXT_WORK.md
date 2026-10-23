# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes unauthorized

## Mandatory authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active plan `legacy-game-structure/data/system_dependency_calibration_order_v0_23.yaml`
- A2 contract `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- economy envelope `legacy-game-structure/117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
- income mix `legacy-game-structure/119_P5_CLEAR_KILL_INCOME_MIX_SENSITIVITY_V0_1.md`
- Tank fidelity correction `legacy-game-structure/121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md`
- cross-class method review `legacy-game-structure/123_P5_ALL_CLASS_SHOP_COMBAT_METHOD_FIDELITY_REVIEW_V0_1.md`
- all-class fixed-rank result `legacy-game-structure/124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- Fortification invariant correction `legacy-game-structure/125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
- post-shop entry-depth result `legacy-game-structure/126_P5_POST_SHOP_STAGE49_ENTRY_DEPTH_RECONVERGENCE_V0_1.md`
- entry-depth fixture `legacy-game-structure/data/p5_post_shop_stage49_entry_depth_fixture_v0_1.json`
- entry-depth summary `legacy-game-structure/data/p5_post_shop_stage49_entry_depth_directional_summary_v0_1.json`
- P5 all-class runner `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`

Live remote wins.

---

# ACTIVE PACKAGE — P5

**A2 APPROVED / FIVE-CLASS FIXED-RANK DIRECTIONAL COMPLETE / POST-SHOP STAGE49 AUTHORING RECONVERGENCE PROMISING**

No user decision is pending.

Working analysis centers only:

```text
Stage49 spend capacity = 50% full-shop reference
sensitivity = 45% / 50% / 55%

CLEAR/KILL income = 70/30
sensitivity = 80/20 / 70/30 / 60/40

legacy-relative effect-scale diagnostic center = 40%
sensitivity = 30% / 40% / 50%
```

None are production freezes.

---

# Current structural corrections

## Fortification

Approved semantic:

```text
max += delta
current += delta
```

Existing absolute deficit is preserved:

```text
(max+delta) - (current+delta) = max-current
```

Therefore do not build a Fortification `repair wastage` model or claim that Fortification erases prior damage.
The late-run temporal question is inherited wall deficit plus ATK/DEF timing, not Fort healing chronology.

## Cross-class KNOCK

Current P4 late diagnostic kernel does not model ordinary push symmetrically for all five classes.
Therefore:

```text
first cross-class shop lane = ATK / FORT / DEF
KNOCK = deferred dedicated parity/inheritance lane
CRIT / CRITDMG = deferred attack-template policy lane
```

---

# Completed five-class fixed-rank finding

In the original P4 Stage49 fixture, after ordinary shop ATK/FORT/DEF is introduced:
- Knight/Rogue/Tank retain sustained-failure danger;
- Archer/Mage become too forgiving under all-finals-missed;
- DEFENSE_HEAVY is not universally dominant;
- Archer/Mage shift is primarily ATK-driven kill/frontmost/SIEGER chronology.

Do not repair via:
- global shop nerf first;
- hidden per-class shop prices/corrections;
- Lv31 nerfs;
- blanket HP/spawn inflation.

---

# Promising Stage49 reconvergence direction

Bounded diagnostic entry-depth sensitivity:

```text
TIME_BUDGET_SIEGER SIEGER x ~= 0.45..0.55
DURABLE/TIME_BUDGET durable x ~= 0.60..0.70
```

Current useful center for directional testing:

```text
SIEGER x ~= 0.48
durable x ~= 0.65
```

**Not production coordinates.**

At 40% ATK/FORT/DEF across all 20 class/policy combinations:

```text
all success survives = 20/20
one miss burials = 0
two consecutive miss burials = 0
```

All-finals-missed:
- Knight/Rogue/Tank bury;
- Archer/Mage do not enter Stage50 healthy; they bury or carry severe reserve loss.

This supports:

```text
AUTHORING ENTRY DEPTH / ROLE TIMING BEFORE PLAYER-POWER NERF
```

---

# Exact next execution order

## 1. Exact replay admission when checkout execution is available

Run and compare committed assets:
- `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
- `tools/run_p4d2_stage49_full_rotation_probe_v0_3.py`
- `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_1.py`
- `tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2.py`

Do not claim exact new-runner authority until this happens.

## 2. Stage46–48 post-shop reconvergence

Do not tune only Stage49.
Carry the shop layer backward through:
- Stage46–47 power revelation;
- Stage48 mastery;
- Stage49 mastery.

Test whether role-entry depth/timing remains a valid repair language without making first successful Lv31 use feel weak.

## 3. Temporal shop feedback

Model:
- ATK acquisition timing;
- DEF acquisition timing;
- inherited wall damage deficit;
- death before later shop opportunities;
- shop-rank trajectories from the current economy envelope.

Fortification itself uses deficit invariance; no fake repair-wastage model.

## 4. Deferred stat-family lanes

After the above structural pass:
- KNOCK cross-class inheritance/parity;
- CRIT/CRITDMG explicit attack-template policies.

## 5. Progression feedback

Then re-measure:
- kill timing;
- valid timing-action count;
- EXP opportunity;
- Lv6/11/16/21/26/31 reach drift.

Final multiplayer normalization remains P10; final EXP convergence remains P10R.

---

# Do not yet

- freeze 50% spend capacity;
- freeze 70/30 income mix;
- freeze 40% common effect scale;
- freeze x=.48/.65 authoring coordinates;
- freeze exact coin/reward/price/rank/effect values;
- freeze generic wall-DR cap;
- assign universal KNOCK behavior before inheritance/parity review;
- assign fake universal CRIT policy;
- solve final 2/3/4P scaling before P10;
- freeze final EXP before P10R;
- modify/deploy production gameplay.

P6 remains blocked pending P5 closure.
