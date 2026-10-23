# Timing Defense — P5 Run Coin / Shop Structural Proposal V0.1

Date: 2026-10-23 KST  
Status: **MATERIAL USER DECISION PROPOSAL / RECOMMENDATION PACKAGE A / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`

---

# 0. Decision package

P5 can proceed to bounded shop-agent simulation once three linked structural choices are decided:

1. shop cadence / interruption model;
2. monster-death coin ownership;
3. WALL HP purchase repair semantic.

Recommendation:

**PACKAGE A — EVERY-STAGE FAST SHOP + TEAM DEATH CREDIT + FORTIFICATION REPAIR**

Exact coin values, costs, rank effects, caps and timers remain completely open.

---

# 1. Decision 1 — shop cadence

## A — EVERY_STAGE_AVAILABLE_BUT_FAST_CONTINUE — RECOMMENDED

After every cleared Stage except the final Stage of the Tier:

```text
Stage clear
-> lightweight shop/intermission opportunity
-> purchase is optional
-> player may immediately READY/CONTINUE without buying
-> next Stage
```

Structural intent:
- coin remains tactically relevant throughout the 50-Stage run;
- the player can react to what happened in the immediately preceding Stage;
- run growth is felt continuously rather than only every long checkpoint;
- legacy Stage1-3 implementation evidence is preserved;
- the UI should be designed later so the shop is a brief intermission, not 49 mandatory long menu sessions.

Multiplayer:
- each human shops independently from their personal wallet;
- each human can mark READY;
- exact timeout/auto-start/host UX is later implementation work;
- P5 balance does not require freezing a host NEXT click.

## B — CHECKPOINT_ONLY

Example: every 5 Stages / only major checkpoints.

Pros:
- less interruption.

Cons:
- coin sits unusable for long intervals;
- weaker immediate adaptation;
- less continuous run-growth feel;
- departs from the implemented prototype loop.

Not recommended as primary structure.

## C — HYBRID LIMITED FULL SHOP

Every Stage may show summary/quick-buy, but full shop only at checkpoints.

Potentially useful later as UI optimization, but mechanically it creates two shop states before P5 has even proven the economy.
Not recommended for the first structural contract.

---

# 2. Decision 2 — monster-death coin ownership

## A — TEAM DEATH CREDIT / PERSONAL WALLETS — RECOMMENDED

Every authoritative ordinary-monster death grants its approved coin value to **each active human participant**, regardless of which player/AI delivered the killing hit.

```text
enemy dies
-> authoritative death reward determined
-> each active human's personal run coin += reward
```

Important:
- wallets remain personal;
- purchase choices remain personal;
- AI has no independent shop wallet in P5;
- an AI kill still produces the same human team death-credit event so AI cannot steal economy;
- reconnecting to the same authoritative run restores the same personal balance.

Why:
- removes kill-steal incentive;
- prevents offensive classes from getting an economy snowball merely because they last-hit more;
- allows Tank/control contribution to remain economically viable;
- deterministic attribution is simpler;
- each human has comparable purchasing opportunity under the same team encounter history.

Player-count warning:
- encounter count and future multiplayer scaling can alter per-player income;
- P10 must normalize/check player-count economy as part of combat scaling;
- this does not authorize final reward numbers now.

### Stage-clear bonus
Retain an **all-human Stage-clear bonus** as a candidate source in addition to death credit.
Its exact formula/value is open.

Role:
- provides a predictable income floor even when a Stage has unusual composition;
- decouples part of economy from monster count;
- makes SAVE/DELAY and timing of purchases easier to model.

## B — KILLER-ONLY COIN

Legacy behavior.

Rejected as default recommendation because it creates class/last-hit snowball and kill-steal incentives.

## C — SHARED TEAM WALLET

All coin enters one common pool.

Not recommended:
- introduces purchase-priority conflict between human players;
- makes one player's build choice consume another player's agency;
- requires additional ownership/voting rules.

## D — SPLIT DEATH REWARD AMONG HUMANS

Maintains a fixed total team coin amount but makes individual purchase capacity shrink as human count rises.
This becomes entangled with multiplayer scaling too early.
Not recommended for P5 baseline.

---

# 3. Decision 3 — WALL HP purchase semantic

## A — FORTIFICATION: MAX HP + MATCHED CURRENT REPAIR — RECOMMENDED

A WALL HP shop rank is explicitly a **Fortification** purchase:

```text
wallMaxHp += purchased flat/pct amount
wallCurrentHp += the same realized max-HP increase
clamped to new wallMaxHp
```

Example only, not a value approval:

```text
before: 1200 / 2000
purchase grants +100 max
result: 1300 / 2100
```

It is **not**:
- automatic Stage healing;
- refill-to-full;
- percentage restoration unless a later explicit rule says so.

Why recommended:
- max-only HP has weak immediate value in a persistent attrition run with no default healing source;
- matched repair gives defensive investment immediate usefulness;
- still preserves damage history because it repairs only the purchased amount;
- creates an intentional economy-vs-attrition choice before Stage50;
- legacy prototype already proves this interaction is technically straightforward.

Balance watch:
- if too efficient, repeated Fortification can erase Stage attrition and invalidate `STAGE49_TO_50_WALL_RESERVE_CONTINUITY_WATCH`;
- price/value/cap must therefore be calibrated, not assumed from v0.35.

## B — MAX HP ONLY

No repair.

Not recommended unless another reliable repair source exists.
After the wall is damaged, it can make new max capacity nearly dead value for the remainder of a no-heal run.

## C — SEPARATE MAX HP AND REPAIR PURCHASES

More granular, but adds another category and additional dominant-policy risks before the six-category shop is validated.
Could be revisited later if Package A produces poor tradeoffs.

## D — PERCENT/REFILL HEAL ON HP BUY

Too likely to erase persistent attrition and create threshold abuse.
Not recommended.

---

# 4. Shared wall ownership — recommended accompanying rule

If Package A is approved:

```text
ATK / CRIT / CRIT DMG / KNOCKBACK
= personal player run modifiers

WALL HP / FORTIFICATION
= personal purchase event contributing to the one shared wall state

DEFENSE
= personal rank contribution into one shared generic wall-DR bucket
```

P2 stacking remains authoritative:

```text
wallMaxHp = (baseWallHp + sum(flat sources)) * (1 + sum(pct sources))
genericWallDR = clamp(sum(wallDamageReductionPp), 0, capTBD)
```

Unique Tank/class defensive effects remain separate from generic DEF.

AI:
- no P5 shop purchases;
- AI presence must not consume a human wallet;
- final AI/player-count scaling is P10 work.

---

# 5. Six-category shop — recommended first contract

Keep:

```text
ATTACK
CRIT CHANCE
CRIT DAMAGE
FORTIFICATION (WALL HP)
DEFENSE
KNOCKBACK
```

No new category is needed before simulation evidence demands it.

Structural rank rule:

```text
finite ranks
monotonically increasing marginal cost
persistent during one Tier attempt
reset on new Tier attempt
```

Legacy rank10/cost curve may seed sensitivity only.

---

# 6. What Package A is intended to produce

Run loop:

```text
combat
-> team deaths generate fair personal coin opportunity
-> Stage clear adds predictable personal bonus
-> lightweight every-Stage shop
-> each player chooses offense / crit / control / shared defense / saving
-> READY/CONTINUE
-> next Stage with same run state
```

This creates a strategic question every Stage without requiring a purchase every Stage.

The important comparison later is not "did everyone spend all coin?" but:

```text
spend now
vs
save for higher-cost ranks
vs
offense
vs
shared survival
vs
class-specific control leverage
```

---

# 7. Required P5 simulation after approval

Agents:
- ATTACK_HEAVY
- CRIT_HEAVY
- DEFENSE_HEAVY
- BALANCED
- SAVE_DELAY
- ROLE_AWARE

At minimum measure:
- coin earned / unspent;
- purchases by category/rank;
- wall HP / wall reserve trajectory;
- clear/fail and clear time;
- kill share only as diagnostic, not coin ownership;
- shop leverage attribution;
- skill-reach shift from P4;
- class divergence;
- whether Fortification erases persistent attrition;
- whether DEF or ATK becomes a trivial universal dominant route;
- whether SAVE/DELAY can be rational rather than always wrong.

Failure labels:

```text
SHOP_SNOWBALL
SHOP_TRIVIAL_DOMINANT_STRATEGY
FORTIFICATION_ATTRITION_ERASURE
DEFENSE_SHARED_SCALING_RUNAWAY
COIN_INCOME_CLASS_DIVERGENCE
SHOP_SKILL_REACH_DISTORTION
SHOP_MENU_FREQUENCY_FATIGUE (later UX evidence)
```

---

# 8. User decision gate

Choose:

```text
A — approve recommended Package A
    every-Stage fast shop opportunity
    + team death credit to each human personal wallet
    + Stage-clear personal bonus candidate
    + Fortification=max increase + matched current repair
    + personal offense/control, shared HP/DEF contribution

B — keep legacy killer-only economy / every-Stage shop / legacy HP-heal concept as baseline
    (not recommended)

C — checkpoint-only shop direction
    while other recommended Package A economy/HP semantics remain

D — request another structural alternative before approval
```

Approval freezes only **semantics/direction**.
No prices, rewards, rank values, cap or exact UI timing are frozen.
