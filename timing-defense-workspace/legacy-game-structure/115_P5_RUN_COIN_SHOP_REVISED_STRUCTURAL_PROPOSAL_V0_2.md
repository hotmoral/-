# Timing Defense — P5 Run Coin / Shop Revised Structural Proposal V0.2

Date: 2026-10-23 KST  
Status: **MATERIAL USER DECISION PROPOSAL / SUPERSEDES DOC113 WHERE CONFLICTING / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
- `113_P5_RUN_COIN_SHOP_STRUCTURAL_PROPOSAL_V0_1.md`
- `114_P5_RUN_COIN_SHOP_QUANTITATIVE_PRECHECK_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`

Supersession rule:
- where this document conflicts with doc113, this V0.2 proposal wins;
- doc113 is retained as design history.

---

# 0. Revised recommendation package

**PACKAGE A2 — EVERY-STAGE FAST SHOP + PERSONAL KILL CREDIT + FORTIFICATION REPAIR**

Structural recommendation:
1. every cleared Stage except final offers a lightweight, nonblocking shop opportunity;
2. personal wallets remain;
3. ordinary-monster kill coin remains killer-only as the baseline candidate;
4. all-human Stage-clear reward remains a candidate predictable income floor;
5. Fortification raises max wall HP and repairs current HP by the same realized increase;
6. personal DEF/Fortification purchases contribute to the shared wall state;
7. six-category shop remains the first simulation contract.

No legacy numerical value is approved.

---

# 1. Why kill coin changed from V0.1 recommendation

Doc113 recommended team death credit from a theoretical class-snowball concern.
The user challenged whether the effect would actually be large because class roles may not create extreme last-hit separation and EXP is not kill-credit based.

Doc114 quantitative precheck found:
- early prototype kill-coin differences are modest under 55:45 or 60:40 last-hit splits;
- level/EXP is granted by valid timing action, not kill credit;
- current evidence does not demonstrate a large killer-only economy defect;
- the much larger 50-Stage risk is total coin supply / category saturation.

Therefore:

```text
KILLER_ONLY_COIN = retained baseline candidate
TEAM_DEATH_CREDIT = no longer default recommendation
```

Watch rather than preemptively replace:
- actual kill-share distribution by class;
- persistent rank separation;
- kill-steal incentive in real multiplayer;
- whether control-oriented classes become materially underfunded.

---

# 2. Every-Stage shop recommendation

Mechanically retain Stage-clear -> shop opportunity -> next Stage.

But the production UX intent is:

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
```

Requirements:
- purchase optional;
- immediate continue/ready possible;
- not 49 long mandatory menu stops;
- later UX can add quick-buy/preset/compact intermission behavior;
- multiplayer waiting policy remains downstream implementation work.

---

# 3. Fortification recommendation

Recommended semantic:

```text
wallMaxHp += purchased realized max-HP increase
wallCurrentHp += same realized amount
clamp to new max
```

This is explicit purchased repair, not automatic Stage healing.

Keep semantic, calibrate magnitude/cost/cap.
Legacy `+100 per rank` is not production authority.

---

# 4. Shared wall ownership recommendation

```text
ATK / CRIT / CRITDMG / KNOCK
= personal run modifiers

FORTIFICATION / DEF
= personal purchase decisions contributing to one shared wall state
```

This is structurally coherent with the shared objective.

However player-count leverage is substantial under legacy values, so P5 may validate solo/base semantics while P10 remains responsible for final 2/3/4P scaling/normalization/cap interactions.

---

# 5. Six-category first simulation contract

Retain:

```text
ATTACK
CRIT CHANCE
CRIT DAMAGE
FORTIFICATION
DEFENSE
KNOCKBACK
```

No additional shop category before evidence demands it.

Exact rank cap, effect size, cost curve and caps are open.

---

# 6. Numerical policy — legacy values explicitly rejected for 50-Stage carryover

The current prototype reward/cost curve is a sensitivity seed only.

Doc114 showed:
- common Stage-clear coin alone reaches ~17,395 by Stage49;
- all six legacy Rank10 tracks cost ~16,350 total;
- single tracks can saturate around Stage16-18;
- HP+DEF can both saturate around Stage26.

Therefore P5 simulation must redesign economy around intended 50-Stage spend capacity rather than scale current values by inertia.

---

# 7. Next analysis after user approval

Once Package A2 is approved, bounded simulation should compare:

```text
ATTACK_HEAVY
CRIT_HEAVY
DEFENSE_HEAVY
BALANCED
SAVE_DELAY
ROLE_AWARE
```

For each class and representative Tier pressure:
- earned coin by source;
- kill-share distribution;
- rank trajectory by Stage;
- purchase saturation timing;
- wall reserve;
- clear/fail and clear time;
- valid timing-event count;
- EXP/skill-reach shift;
- dominant purchase policy;
- Fortification attrition erasure;
- shared DEF leverage.

P5 must not freeze production numbers before this comparison.
