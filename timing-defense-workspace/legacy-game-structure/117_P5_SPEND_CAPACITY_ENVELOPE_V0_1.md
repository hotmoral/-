# Timing Defense — P5 50-Stage Spend-Capacity Envelope V0.1

Date: 2026-10-23 KST  
Status: **BOUNDED ECONOMY PREFLIGHT / CANDIDATE ENVELOPE / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `114_P5_RUN_COIN_SHOP_QUANTITATIVE_PRECHECK_V0_1.md`
- P2 modifier contract

---

# 0. Purpose

Translate the approved constraint `NO_ROUTINE_FULL_SHOP_MAXOUT_BY_STAGE49` into a bounded first-pass search space before selecting actual coin prices/rewards.

This document works in **normalized spend-capacity ratio space**. It does not approve production coin denominations or shop costs.

---

# 1. Reference cost shape only

Sensitivity seed:

```text
base next-rank costs:
40, 65, 100, 145, 200, 265, 340, 425, 520, 625

legacy category multipliers:
ATK 1.0 / CRIT 1.1 / CRITDMG 1.0 / FORT 0.9 / DEF 1.1 / KNOCK 0.9
```

The live prototype uses positive-value JavaScript `Math.round`. Under that exact rounding contract:

```text
ATK       2,725
CRIT      3,000
CRITDMG   2,725
FORT      2,455
DEF       3,000
KNOCK     2,455
TOTAL    16,360 nominal units
```

Earlier `16,350` precheck text came from Python banker-rounding on some `.5` values and is corrected here. This 10-unit correction does not change the structural conclusion.

---

# 2. First-pass full-run spend-capacity brackets

```text
LOW     = 45% of full-shop nominal max cost = 7,362
CENTER  = 50%                              = 8,180
HIGH    = 55%                              = 8,998
```

Why this bracket:
- all three are materially below six-track full-max cost;
- a player can still specialize strongly;
- CENTER permits one favored track to reach Rank10 under some policies while leaving other tracks incomplete;
- balanced allocation remains around Rank7–8 at Stage49;
- the bracket is wide enough to expose too-restrictive vs too-generous behavior.

These are calibration candidates, not approved final values.

---

# 3. Stage-distribution sensitivity shape

Use the legacy Stage-clear formula only for its **relative backloaded shape**:

```text
weight(stage) = 55 + 12 * stage
Stage1..49
```

Normalize the weights to the selected total spend capacity. This does not retain the old absolute reward.

CENTER cumulative nominal budget:

```text
through Stage10  ~569.0  ( 6.96%)
through Stage20 ~1702.3  (20.81%)
through Stage30 ~3399.9  (41.56%)
through Stage40 ~5661.8  (69.22%)
through Stage45 ~7004.4  (85.63%)
through Stage49  8180.0 (100.00%)
```

---

# 4. CENTER balanced trajectory — sanity check

```text
Stage10: ATK2 / CRIT2 / CRITDMG2 / FORT2 / DEF1 / KNOCK2
Stage20: ATK4 / CRIT3 / CRITDMG3 / FORT4 / DEF3 / KNOCK4
Stage30: all six around Rank5
Stage40: ATK6 / CRIT6 / CRITDMG6 / FORT7 / DEF6 / KNOCK7
Stage45: all six around Rank7
Stage49: ATK8 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK8
```

The run still contains meaningful late purchases and balanced play does not saturate the shop.

---

# 5. Stage49 policy snapshots — CENTER sensitivity

```text
ATTACK_HEAVY
ATK9 / CRIT6 / CRITDMG9 / FORT7 / DEF6 / KNOCK7

CRIT_HEAVY
ATK8 / CRIT9 / CRITDMG8 / FORT6 / DEF6 / KNOCK7

DEFENSE_HEAVY
ATK6 / CRIT6 / CRITDMG6 / FORT10 / DEF8 / KNOCK8

BALANCED
ATK8 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK8

SAVE_DELAY (no spending before Stage20, then balanced)
ATK8 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK8
```

Role-aware diagnostic examples:

```text
Knight: ATK8 / CRIT6 / CRITDMG6 / FORT8 / DEF6 / KNOCK10
Rogue:  ATK10 / CRIT7 / CRITDMG7 / FORT7 / DEF6 / KNOCK7
Tank:   ATK6 / CRIT6 / CRITDMG6 / FORT8 / DEF8 / KNOCK10
Archer: ATK9 / CRIT6 / CRITDMG9 / FORT7 / DEF6 / KNOCK7
Mage:   ATK10 / CRIT7 / CRITDMG7 / FORT7 / DEF6 / KNOCK7
```

These are rank-allocation shapes only, not combat-optimal build claims.

---

# 6. LOW/HIGH observation

Balanced Stage49:

```text
LOW45%:  ATK7 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK7
HIGH55%: ATK8 / CRIT7 / CRITDMG8 / FORT8 / DEF7 / KNOCK8
```

Specialist policies may max one selected track; that is allowed if meaningful sacrifices remain elsewhere.

---

# 7. Killer-only income perturbation

A first sensitivity around the CENTER wallet uses `47% / 50% / 53%` full-shop spend capacity to approximate modest last-hit wallet divergence around the center.

Balanced Stage49 remains around Rank7–8 across that range. Therefore the current first-order saturation risk remains total economy scale, not modest killer-only variation.

This is not a final multiplayer kill-share model.

---

# 8. First-pass acceptance criteria

1. `FULL_SHOP_MAXOUT_ROUTINE = false` by Stage49.
2. Balanced intended-entry trajectories retain meaningful purchases at Stage40/45/49.
3. Specialization may produce a selected maxed track without completing all other tracks.
4. Multiple materially different policies remain viable in rank space.
5. SAVE_DELAY is not arithmetically invalid by price structure alone.
6. Fortification/DEF require combat integration before balance claims.
7. Killer-only variation must be measured, not hidden with class-specific prices.

---

# 9. Next work

Create and run a deterministic economy-only fixture/runner for ratios `0.45 / 0.50 / 0.55`, CENTER perturbations `0.47 / 0.50 / 0.53`, policies `ATTACK_HEAVY / CRIT_HEAVY / DEFENSE_HEAVY / BALANCED / SAVE_DELAY / ROLE_AWARE`, snapshots `10 / 20 / 30 / 40 / 45 / 49`.

Then test actual clear-vs-kill income mixes before combat-power integration.

No production values or code are authorized.