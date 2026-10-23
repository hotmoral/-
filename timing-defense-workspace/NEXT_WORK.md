# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes unauthorized

## Mandatory authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active dependency plan `legacy-game-structure/data/system_dependency_calibration_order_v0_19.yaml`
- P5 recovery `legacy-game-structure/112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
- P5 quantitative precheck `legacy-game-structure/114_P5_RUN_COIN_SHOP_QUANTITATIVE_PRECHECK_V0_1.md`
- revised P5 proposal `legacy-game-structure/115_P5_RUN_COIN_SHOP_REVISED_STRUCTURAL_PROPOSAL_V0_2.md`
- P4 closure `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`

Live remote wins.

---

# ACTIVE PACKAGE — P5

Current boundary:

**MATERIAL STRUCTURAL DECISION GATE — REVISED RUN COIN / SHOP PACKAGE A2**

Authority recovery and first quantitative precheck are complete. Do not tune/freeze values before the semantic decision.

---

# Revised recommended Package A2

```text
SHOP CADENCE
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
- after every cleared Stage except Tier final
- lightweight intermission
- buying optional
- immediate continue/ready possible

COIN OWNERSHIP
KILLER_ONLY_PERSONAL_MONSTER_COIN_BASELINE
- retain personal last-hit reward as the first simulation candidate
- all-human Stage-clear bonus remains a candidate income floor
- measure actual class/team kill-share divergence before replacing this rule

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

# Quantitative precheck that changed the recommendation

Killer-only coin risk is currently a watch, not a demonstrated defect.
Early 2P sensitivity gave approximately:

```text
55:45 kill share -> ~6% total coin gap
60:40 -> ~12.3%
70:30 -> ~26.2%
```

EXP is based on valid timing actions, not kill credit.

The much larger problem is legacy 50-Stage economy saturation:

```text
prototype Stage1..49 common clear reward = 17,395
all six legacy Rank10 tracks total cost = 16,350
single track can saturate around Stage16-18
HP+DEF can both saturate around Stage26
```

Therefore current reward/cost values are sensitivity seeds only and must be redesigned for the 50-Stage run.

---

# Still open after A2 approval

- exact monster coin values;
- exact Stage-clear bonus;
- exact shop costs;
- exact rank cap;
- exact effect per rank;
- generic wall-DR cap;
- exact shop UI/intermission timer;
- multiplayer HP/DEF normalization / encounter scaling;
- final EXP/P10R convergence.

---

# Immediately after approval

1. write approved P5 structural contract;
2. create deterministic P5 economy/shop fixture;
3. design a 50-Stage spend-capacity envelope rather than inherit prototype values;
4. compare:
   - ATTACK_HEAVY
   - CRIT_HEAVY
   - DEFENSE_HEAVY
   - BALANCED
   - SAVE_DELAY
   - ROLE_AWARE
5. re-measure P4 skill reach after shop feedback;
6. test:
   - SHOP_SATURATION_TOO_EARLY
   - SHOP_SNOWBALL
   - FORTIFICATION_ATTRITION_ERASURE
   - SHARED_DEF_PLAYER_COUNT_LEVERAGE
   - COIN_INCOME_CLASS_DIVERGENCE
   - DOMINANT_PURCHASE_POLICY
   - SHOP_SKILL_REACH_DISTORTION
7. repair structure/economy before hidden class corrections.

P6 remains blocked until P5 closes.
