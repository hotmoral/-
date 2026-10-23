# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes unauthorized

## Mandatory authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active dependency plan `legacy-game-structure/data/system_dependency_calibration_order_v0_18.yaml`
- P5 recovery `legacy-game-structure/112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
- P5 proposal `legacy-game-structure/113_P5_RUN_COIN_SHOP_STRUCTURAL_PROPOSAL_V0_1.md`
- P4 closure `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`

Live remote wins.

---

# ACTIVE PACKAGE — P5

Current boundary:

**MATERIAL STRUCTURAL DECISION GATE — RUN COIN / SHOP PACKAGE**

Authority recovery is complete. Do not tune values before this semantic decision.

---

# Recommended Package A

```text
SHOP CADENCE
EVERY_STAGE_AVAILABLE_BUT_FAST_CONTINUE
- after every cleared Stage except Tier final
- lightweight intermission
- buying optional
- immediate READY/CONTINUE allowed

COIN OWNERSHIP
TEAM_DEATH_CREDIT_TO_EACH_ACTIVE_HUMAN_PERSONAL_WALLET
- no killer-only economy
- AI kills cannot steal human economy
- Stage-clear bonus remains a candidate source

WALL HP
FORTIFICATION_MAX_PLUS_MATCHED_CURRENT_REPAIR
- increase max HP
- repair current HP by same realized increase
- clamp at new max
- not full heal / not automatic Stage heal

SHARED WALL OWNERSHIP
personal offense/control purchases
personal HP/DEF purchases contribute to one shared wall
```

Six-category first contract candidate:

```text
ATK
CRIT CHANCE
CRIT DAMAGE
FORTIFICATION
DEFENSE
KNOCKBACK
```

Finite ranks and increasing marginal costs; exact rank cap/cost/effects open.

---

# Why Package A is recommended

Legacy killer-only coin creates an avoidable feedback loop:

```text
last-hit advantage
-> more coin
-> more offense
-> more last hits
```

This is especially unsafe now that class identities are intentionally asymmetric.

Fortification gives WALL HP immediate defensive value in a persistent no-auto-heal run without refilling the wall to full.

Every-Stage availability preserves the original continuous run-growth loop while fast-continue avoids making a purchase mandatory 49 times.

---

# User decision options

```text
A — approve recommended Package A

B — keep legacy killer-only economy + every-Stage shop baseline
    (not recommended)

C — checkpoint-only shop cadence
    + recommended team-death-credit economy
    + recommended Fortification semantic

D — request another structural alternative
```

Approval freezes only semantics/direction.

Still open after approval:
- exact monster coin values;
- exact Stage-clear bonus;
- exact shop costs;
- exact rank cap;
- exact effect per rank;
- generic wall-DR cap;
- exact shop UI/intermission timer;
- P10 multiplayer scaling.

---

# Immediately after approval

1. write approved P5 structural contract;
2. create deterministic shop/economy fixture;
3. seed legacy rank10/cost curve only as sensitivity inputs, not authority;
4. compare:
   - ATTACK_HEAVY
   - CRIT_HEAVY
   - DEFENSE_HEAVY
   - BALANCED
   - SAVE_DELAY
   - ROLE_AWARE
5. re-measure P4 skill reach after shop feedback;
6. test:
   - SHOP_SNOWBALL
   - SHOP_TRIVIAL_DOMINANT_STRATEGY
   - FORTIFICATION_ATTRITION_ERASURE
   - DEFENSE_SHARED_SCALING_RUNAWAY
   - COIN_INCOME_CLASS_DIVERGENCE
   - SHOP_SKILL_REACH_DISTORTION
7. repair structure/encounter/economy before hidden class corrections.

P6 remains blocked until P5 closes.
