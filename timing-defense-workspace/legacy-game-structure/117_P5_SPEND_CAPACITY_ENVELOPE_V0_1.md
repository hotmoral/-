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

This document works in **normalized spend-capacity ratio space**.
It does not approve production coin denominations or shop costs.

---

# 1. Reference cost shape only

For sensitivity only, retain the legacy relative rank-cost shape:

```text
base next-rank costs:
40, 65, 100, 145, 200, 265, 340, 425, 520, 625

legacy category multipliers:
ATK      1.0
CRIT     1.1
CRITDMG  1.0
FORT     0.9
DEF      1.1
KNOCK    0.9
```

Nominal full Rank10 reference cost:

```text
ATK       2,725
CRIT      3,000
CRITDMG   2,725
FORT      2,450
DEF       3,000
KNOCK     2,450
TOTAL    16,350 nominal units
```

These are comparison units only.

---

# 2. First-pass full-run spend-capacity brackets

Test three successful-run nominal total spend capacities by Stage49:

```text
LOW     = 45% of full-shop nominal max cost = 7,357.5
CENTER  = 50%                              = 8,175.0
HIGH    = 55%                              = 8,992.5
```

Why this bracket:
- all three are materially below six-track full-max cost;
- a player can still specialize strongly;
- CENTER permits one favored track to reach Rank10 under some policies while leaving other tracks materially incomplete;
- balanced allocation remains around Rank7–8 at Stage49 in the first preflight;
- the bracket is wide enough to expose whether the economy is too restrictive or too generous.

These percentages are **calibration candidates, not approved final values**.

---

# 3. Stage-distribution sensitivity shape

For the first economy-only preflight, use the old Stage-clear formula only for its **relative backloaded distribution shape**:

```text
weight(stage) = 55 + 12 * stage
for Stage1..49
```

Then normalize the weights so total income equals LOW/CENTER/HIGH spend capacity.

This does not retain the old absolute clear reward.

CENTER cumulative nominal budget under this relative shape:

```text
through Stage10  ~568.7  ( 6.96% of final budget)
through Stage20 ~1701.3  (20.81%)
through Stage30 ~3397.8  (41.56%)
through Stage40 ~5658.4  (69.22%)
through Stage45 ~7000.1  (85.63%)
through Stage49  8175.0 (100.00%)
```

This shape is only a distribution sensitivity seed. Actual kill-coin + clear-coin composition is a later P5 layer.

---

# 4. CENTER balanced trajectory — first sanity check

Using the reference costs and CENTER normalized budget, a deterministic balanced policy produces approximately:

```text
Stage10: ATK2 / CRIT2 / CRITDMG2 / FORT2 / DEF1 / KNOCK2
Stage20: ATK4 / CRIT3 / CRITDMG3 / FORT4 / DEF3 / KNOCK4
Stage30: all six around Rank5
Stage40: ATK6 / CRIT6 / CRITDMG6 / FORT7 / DEF6 / KNOCK7
Stage45: all six around Rank7
Stage49: ATK8 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK8
```

This is directionally desirable because:
- the run still contains shop decisions after Stage40;
- balanced play does not saturate the shop;
- specialization remains possible.

---

# 5. Stage49 policy snapshots — CENTER sensitivity

Economy-only deterministic priority policies give these provisional Stage49 rank shapes:

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

Role-aware examples at CENTER:

```text
Knight: ATK8 / CRIT6 / CRITDMG6 / FORT8 / DEF6 / KNOCK10
Rogue:  ATK10 / CRIT7 / CRITDMG7 / FORT7 / DEF6 / KNOCK7
Tank:   ATK6 / CRIT6 / CRITDMG6 / FORT8 / DEF8 / KNOCK10
Archer: ATK9 / CRIT6 / CRITDMG9 / FORT7 / DEF6 / KNOCK7
Mage:   ATK10 / CRIT7 / CRITDMG7 / FORT7 / DEF6 / KNOCK7
```

Important:
- these are rank-allocation shapes only;
- they are not proof that the named policy is combat-optimal;
- CRIT value depends on final attack-template crit policies;
- ROLE_AWARE priorities are diagnostic heuristics, not recommended player builds.

---

# 6. LOW/HIGH boundary observation

At LOW=45%, balanced Stage49 remains roughly:

```text
ATK7 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK7
```

At HIGH=55%, balanced Stage49 remains roughly:

```text
ATK8 / CRIT7 / CRITDMG8 / FORT8 / DEF7 / KNOCK8
```

Even HIGH does not approach all-six maxout under balanced allocation.
Specialist policies may max one selected track, which is intentional if meaningful sacrifices remain elsewhere.

---

# 7. First-pass acceptance criteria

A candidate economy should satisfy all of the following before combat integration:

1. `FULL_SHOP_MAXOUT_ROUTINE = false` by Stage49.
2. Balanced intended-entry trajectories retain meaningful late purchases at Stage40/45/49.
3. Specialization can produce a visibly stronger selected track without also completing all other tracks.
4. At least two materially different purchase policies remain affordable/viable in rank space.
5. SAVE_DELAY is not automatically punished purely by price arithmetic; combat risk may still make it inferior contextually.
6. Fortification/DEF cannot be declared balanced from rank arithmetic alone; wall combat integration is mandatory.
7. Killer-only coin variation is applied as a later income-source perturbation around the spend-capacity envelope, not used to set hidden class prices.

---

# 8. Next work

Create a deterministic economy-only runner/fixture for:

```text
ratios: 0.45 / 0.50 / 0.55
policies: ATTACK_HEAVY / CRIT_HEAVY / DEFENSE_HEAVY / BALANCED / SAVE_DELAY / ROLE_AWARE
snapshots: Stage10 / 20 / 30 / 40 / 45 / 49
```

Then test kill-share income perturbations and candidate clear-vs-kill income mixes before integrating combat power.

No production values or code are authorized.