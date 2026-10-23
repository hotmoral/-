# Timing Defense — P5 Run Coin / Shop Quantitative Precheck V0.1

Date: 2026-10-23 KST  
Status: **DIRECTIONAL QUANTITATIVE REVIEW / REVISES PRIOR RISK EMPHASIS / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
- `113_P5_RUN_COIN_SHOP_STRUCTURAL_PROPOSAL_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- current prototype shop kernel inherited through v0.45

---

# 0. Purpose

Re-check the material P5 shop choices quantitatively after the user challenged the earlier assumption that killer-only coin would necessarily create a large class-economy snowball.

This document does not approve production values. It measures what the legacy prototype values would imply if naively extended into a 50-Stage Tier and updates risk priority accordingly.

---

# 1. Killer-only coin risk — DOWNGRADED

Prototype ordinary death rewards are granted to the killing human only, while Stage-clear rewards are granted to every human.

For the first three implemented Stages, using the prototype encounter composition and rewards:

```text
common Stage-clear reward cumulative ~= 237 coin per human
team-wide monster-death reward pool ~= 193.2 coin
```

Two-human sensitivity examples:

```text
55:45 last-hit share -> ~343.3 vs ~324.0 total coin (~6% gap)
60:40 last-hit share -> ~352.9 vs ~314.3 total coin (~12.3% gap)
70:30 last-hit share -> ~372.3 vs ~295.0 total coin (~26.2% gap)
```

At 60:40, all-in ATK purchasing under the legacy cost curve produces roughly one rank of separation around this early window rather than an explosive divergence.

The level/EXP system is not kill-credit based. Valid timing actions grant EXP; last hits grant coin. Therefore:

```text
more last hits != faster level-up
```

P4 feedback also showed a possible opposite effect: more offensive power can shorten target life, reduce later valid timing opportunities, and therefore reduce pure-turn EXP opportunity.

Updated classification:

```text
KILLER_ONLY_COIN = KEEP_AS_VALID_P5_CANDIDATE
CLASS_ECONOMY_SNOWBALL = WATCH / NOT YET DEMONSTRATED
TEAM_DEATH_CREDIT = no longer recommended by default solely from theory
```

Required later measurement:
- actual kill-share distribution by class/team composition;
- duration of any 1+ shop-rank separation;
- whether kill share materially changes purchase policy or clear outcome.

---

# 2. Bigger issue — legacy 50-Stage coin supply is far too large

Legacy Stage-clear formula:

```text
reward(stage) = 55 + 12 * stage
```

If naively extended through Stage49:

```text
Stage1..10  cumulative clear reward = 1,210
Stage1..20                              3,620
Stage1..30                              7,230
Stage1..40                             12,040
Stage1..45                             14,895
Stage1..49                             17,395
```

Legacy six-category full Rank10 cost:

```text
ATK       2,725
CRIT      3,000
CRITDMG   2,725
HP        2,450
DEF       3,000
KNOCK     2,450
TOTAL    16,350
```

Therefore common Stage-clear reward alone, with zero kill coin, exceeds the cost of maxing all six categories by approximately Stage48.

Single-category specialization also saturates too early:

```text
HP/KNOCK Rank10 cost 2,450 -> reachable around Stage16 from common clear reward alone
ATK/CRITDMG Rank10 2,725 -> around Stage17
CRIT/DEF Rank10 3,000 -> around Stage18
HP+DEF both Rank10 5,450 -> around Stage26
```

This would flatten the intended 50-Stage run-growth curve and create very early category saturation.

Updated priority:

```text
TOTAL_COIN_SUPPLY_AND_COST_CURVE = PRIMARY P5 ECONOMY RISK
LAST_HIT_DISTRIBUTION = SECONDARY WATCH
```

The legacy reward/cost values must not be promoted into 50-Stage production values.

---

# 3. Shop cadence — structurally viable, UX interruption is the real risk

Every-Stage access remains mechanically coherent because it allows immediate adaptation and continuous run growth.

However 49 forced modal stops would be unacceptable if each requires meaningful waiting.

Illustrative interruption cost only:

```text
3 sec average x 49 = 147 sec (~2m27s)
5 sec average x 49 = 245 sec (~4m05s)
10 sec average x 49 = 490 sec (~8m10s)
```

Therefore the mechanically preferred form is not `49 long shops`, but:

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
- lightweight intermission / quick shop
- purchase optional
- immediate continue/ready possible
- later UX may support quick-buy/preset behavior
```

Exact multiplayer timeout/host UX remains implementation work.

---

# 4. Fortification (max HP + matched current repair) — semantic is sound, values can dominate

Legacy HP rank:

```text
+100 wallMaxHp
+100 current wallHp, clamped to new max
```

At legacy Rank10 for one human:

```text
+1,000 max HP
up to +1,000 cumulative explicit repair
base wall 2,000 -> 3,000 max if fully invested
```

This is a coherent explicit repair mechanic and does not violate P1 because it is purchased, not automatic Stage healing.

But it can erase attrition if too cheap or too repeatable.

Multiplayer leverage is larger if each human's full HP investment stacks directly into the shared wall:

```text
1 human full HP ranks -> +1,000 max/repair budget
4 humans full HP ranks -> +4,000 max/repair budget before any scaling rule
```

Therefore:

```text
FORTIFICATION_SEMANTIC = KEEP AS STRONG CANDIDATE
LEGACY +100 PER RANK = NOT AUTHORIZED
MULTIPLAYER CONTRIBUTION SCALING/CAP = P10 dependency
STAGE49_TO_50_WALL_RESERVE_CONTINUITY_WATCH remains mandatory
```

---

# 5. Shared DEF — category valid, legacy values are highly player-count sensitive

Legacy DEF semantics:

```text
+2.5 percentage points generic wall DR per personal DEF rank
sum all human DEF ranks
cap 60%
```

Implications at Rank10:

```text
one human max DEF -> 25% generic DR
two humans max DEF -> 50%
three/four humans can reach the 60% prototype cap
```

At 60% DR, incoming raw wall damage is multiplied by 0.40, equivalent to a 2.5x raw-damage budget before considering wall HP growth, Tank unique defense, or barriers.

Example structural amplification if legacy values were naively combined:

```text
one human: wall 3,000 with 25% DR -> ~4,000 raw-damage budget
four humans: potentially wall 6,000 with 60% DR -> ~15,000 raw-damage budget
```

The latter is ~7.5x the base 2,000 raw wall budget before unique defensive effects.

Therefore shared DEF ownership is structurally coherent, but legacy per-rank value and cap cannot be frozen before multiplayer scaling.

```text
SHARED_DEF_OWNERSHIP = KEEP AS CANDIDATE
+2.5pp/rank AND cap60 = sensitivity seeds only
P10 must evaluate player-count normalization / encounter scaling / cap interaction
```

---

# 6. Six categories — retain for P5 simulation

Current six categories remain sufficient for first bounded simulation:

```text
ATK
CRIT CHANCE
CRIT DAMAGE
FORTIFICATION / WALL HP
DEFENSE
KNOCKBACK
```

No seventh category is justified yet.

Important class-asymmetry watches:
- CRIT value varies by attack-template crit policy and multihit structure;
- KNOCKBACK has much higher utility for some class/monster interactions;
- DEF/FORTIFICATION value compounds with Tank unique defensive effects;
- same nominal shop percentage must not be assumed to have equal class value.

These are expected asymmetries, not automatic defects.

---

# 7. Revised P5 recommendation after quantitative precheck

Recommended structural baseline for simulation:

```text
A. every Stage offers a fast/nonblocking shop opportunity
B. personal wallets remain
C. killer-only monster coin is retained as a baseline candidate, not rejected
D. all-human Stage-clear reward remains a candidate income floor
E. Fortification = max HP increase + matched explicit repair
F. DEF/Fortification purchases contribute to shared wall state
G. six shop categories retained
```

But DO NOT carry over the legacy economy values.

P5 numerical calibration must solve, in this order:

```text
1. target total spend capacity across 50 Stages
2. category saturation timing / desired max-rank reach
3. clear-reward vs kill-reward mix
4. marginal rank cost curve
5. Fortification repair efficiency
6. generic DEF leverage/cap
7. class-specific purchase strategy divergence
8. shop-power -> kill-speed/wall-survival -> valid-turn EXP feedback
```

Required policy agents:
- ATTACK_HEAVY
- CRIT_HEAVY
- DEFENSE_HEAVY
- BALANCED
- SAVE_DELAY
- ROLE_AWARE

Primary failure modes:
- SHOP_SATURATION_TOO_EARLY
- SHOP_SNOWBALL
- FORTIFICATION_ATTRITION_ERASURE
- SHARED_DEF_PLAYER_COUNT_LEVERAGE
- DOMINANT_PURCHASE_POLICY
- SHOP_POWER_EXP_FEEDBACK_DISTORTION

No production values are frozen by this review.
