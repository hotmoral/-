# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes unauthorized

## Mandatory authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active plan `legacy-game-structure/data/system_dependency_calibration_order_v0_22.yaml`
- A2 contract `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- economy envelope `legacy-game-structure/117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
- economy preflight `legacy-game-structure/118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
- income mix `legacy-game-structure/119_P5_CLEAR_KILL_INCOME_MIX_SENSITIVITY_V0_1.md`
- defense upper bound `legacy-game-structure/120_P5_FORTIFICATION_DEFENSE_LEVERAGE_UPPER_BOUND_V0_1.md`
- Tank fidelity correction `legacy-game-structure/121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md`
- Tank shop combat `legacy-game-structure/122_P5_TANK_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`

Live remote wins.

---

# ACTIVE PACKAGE — P5

**A2 APPROVED / FIVE-CLASS FIXED-RANK SHOP+COMBAT PROBE NEXT**

No user decision is pending.

Working analysis centers only:

```text
Stage49 spend capacity = 50% full-shop reference
sensitivity = 45% / 50% / 55%

CLEAR/KILL income = 70/30
sensitivity = 80/20 / 70/30 / 60/40

first combat effect magnitude center = 40% of legacy per-rank effects
sensitivity = 30% / 40% / 50%
```

None are production freezes.

---

# Approved A2 semantics

```text
shop every cleared Stage except Tier final, nonblocking
personal wallets
killer-only ordinary-monster coin baseline
all-human Stage-clear income-floor candidate
Fortification = max HP + matched current repair
personal ATK/CRIT/CRITDMG/KNOCK
personal FORT/DEF purchases contribute to shared wall
six categories
NO ROUTINE FULL-SHOP MAXOUT BY STAGE49
```

---

# Tank fidelity rule required by all next probes

Tank Lv11 Iron Wall applies to **all shared wall incoming**, including SIEGER shots:

```text
raw wall event
-> monster capability modifier
-> generic shop DEF
-> Tank Iron Wall x0.90
-> shield
-> BaseHP
```

Do not use old v0.5/v0.2 Tank SIEGER-specific numbers as current fidelity truth.
Committed v0.6 / Stage49 v0.3 exact replay remains pending; targeted reconstruction reproduced the old exact baseline before applying the correction.

---

# Exact next analysis

## 1. Five-class fixed-rank Stage49 combat

Classes:
- Knight
- Rogue
- Tank
- Archer
- Mage

Policies:
- ATTACK_HEAVY
- DEFENSE_HEAVY
- BALANCED
- ROLE_AWARE

First scalar families:
- ATK
- KNOCKBACK
- FORTIFICATION
- DEFENSE

Magnitude sensitivity:

```text
30% / 40% / 50% of legacy per-rank reference
```

CRIT / CRITDMG remain separate until attack-template crit inheritance is respected.

Required outputs:
- wall max/current reserve;
- burial time;
- kills / active backlog;
- ordinary wall hits;
- SIEGER shots;
- class mistake-budget behavior;
- comparison with corrected/no-shop same-class baseline.

Reject curves that:
- erase persistent attrition;
- allow repeated mastery failure without meaningful reserve loss;
- make DEFENSE_HEAVY universally dominant;
- destroy the approved Lv31 power/pressure relationship.

## 2. Purchase-time Fortification history

After the fixed-rank screen:
- buy Fortification at actual Stage/shop times;
- apply matched repair only when bought;
- carry current/max wall HP continuously;
- measure wasted repair at/near full HP;
- measure Stage49->50 reserve.

## 3. Shop-power feedback into P4 progression

Then re-measure:
- enemy kill timing;
- valid timing-action count;
- EXP opportunity;
- Lv6/11/16/21/26/31 reach drift.

---

# Do not yet

- freeze 50% spend capacity;
- freeze 70/30 income mix;
- freeze 40% shop effect scale;
- freeze exact coin/reward/price/rank/effect values;
- freeze generic wall-DR cap;
- assign fake universal CRIT value to multihit/final skills;
- solve final 2/3/4P scaling before P10;
- freeze final EXP before P10R;
- modify/deploy production gameplay.

P6 remains blocked pending P5 closure.
