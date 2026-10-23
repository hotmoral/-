# Timing Defense — P5 Remaining Shop Quantitative Review V0.1

Date: 2026-10-23 KST
Status: **QUANTITATIVE REVIEW / REVISES PROPOSAL RECOMMENDATION ONLY / USER DECISION STILL REQUIRED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
- `113_P5_RUN_COIN_SHOP_STRUCTURAL_PROPOSAL_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- live inherited prototype shop kernel at production HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`

---

# 0. Purpose

The prior proposal intentionally identified structural risks before numerical analysis. This review quantifies those risks using the legacy/prototype formulas only as sensitivity evidence.

It does **not** promote those legacy values into production balance.

Main revision:
- prior concern that killer-only monster coin necessarily creates a large snowball was overstated;
- retain killer-only coin as the current candidate until five-class kill-share simulation proves material unfairness.

---

# 1. Killer-only coin — quantified revision

Prototype Stage1-3 all-human clear rewards:

```text
Stage1 67
Stage2 79
Stage3 91
cumulative = 237 per human
```

Expected total monster reward pool across the same three prototype stages is approximately `193.2` coin.

Illustrative 2P last-hit shares:

```text
55:45 -> total personal coin about 343.3 vs 324.0  (~6% gap)
60:40 -> about 352.9 vs 314.3                   (~12.3% gap)
70:30 -> about 372.3 vs 295.0                   (~26.2% gap)
```

At a 60:40 split and legacy ATK costs, the practical result after Stage3 is roughly one ATK rank of separation, corresponding to about a 6.5% effective attack ratio between Rank4 and Rank3.

EXP is not awarded by last-hit. Valid timing actions award EXP; monster death awards coin. Therefore killer-only coin does not directly create faster level gain. Higher shop damage can even reduce later valid-turn opportunity by shortening fights, as already observed in P4 feedback analysis.

**Revised recommendation:**

```text
KEEP KILLER-ONLY MONSTER COIN AS A CANDIDATE
+ keep all-human Stage-clear income floor candidate
+ measure five-class kill-share / rank-gap persistence before changing ownership semantics
```

Do not replace it with team death credit merely from theoretical concern.

---

# 2. Bigger economy issue — prototype supply curve does not scale to 50 Stages

Legacy Stage-clear formula:

```text
55 + 12*Stage
```

If mechanically extrapolated through Stage49, all-human clear rewards alone total:

```text
17,395 coin per human
```

Legacy six-category Rank10 total cost using JavaScript `Math.round` category multipliers:

```text
ATK       2,725
CRIT      3,000
CRIT DMG  2,725
HP        2,455
DEF       3,000
KNOCK     2,455
TOTAL    16,360
```

Thus, with **zero monster kill coin**, the legacy clear-reward formula alone can buy all six Rank10 tracks by about Stage48.

Additional reference:
- all offense tracks total 8,450 coin; clear rewards alone reach this around Stage33;
- HP+DEF total 5,455 coin; clear rewards alone reach this around Stage26.

Therefore the dominant P5 economy problem is not currently last-hit ownership. It is that the prototype reward/cost curves were never designed for a 50-Stage Tier and must be recalibrated.

---

# 3. Every-Stage shop cadence — retain availability, reject mandatory long interruption

A 50-Stage Tier has up to 49 pre-next-stage shop opportunities.

Illustrative added interruption cost if every opportunity becomes a mandatory modal pause:

```text
3s each -> 147s (~2.45 min)
5s each -> 245s (~4.08 min)
8s each -> 392s (~6.53 min)
```

Therefore the mechanical cadence and UI interruption cadence must be separated.

**Revised recommendation:**

```text
EVERY_STAGE_SHOP_AVAILABILITY
not
EVERY_STAGE_MANDATORY_LONG_MENU
```

After each cleared Stage except Stage50:
- shop/quick-buy is available;
- purchase remains optional;
- immediate continue/READY is available;
- later UX should integrate this into the Stage-clear intermission rather than force 49 full menu sessions.

The final economy should target a purchase cadence substantially lower than one meaningful rank purchase every single Stage unless testing shows otherwise.

---

# 4. Fortification semantic — strengthened recommendation

Prototype HP purchase semantics:

```text
maxHP += delta
currentHP += same delta
```

This is structurally cleaner than describing it as ordinary healing.

Example:

```text
1200 / 2000
+100 Fortification
-> 1300 / 2100
```

Absolute missing HP remains `800` before and after. The purchase adds a new intact wall segment; it does not repair old missing HP.

Consequences:
- preserves accumulated absolute damage history;
- gives the purchased max-HP capacity immediate usable value;
- avoids the max-only paradox where new purchased capacity enters empty;
- still does not refill the wall or create automatic Stage healing.

Under legacy solo values, 10 HP ranks add 1000 max/current HP. Exact amount/cost/cap remain open.

**Recommendation remains:** Fortification = max HP increase + matched current increase.

---

# 5. Shared HP/DEF ownership — semantic direction good, multiplayer aggregation must remain open

One shared wall makes it coherent for defensive purchases to benefit the shared objective.

Recommended structural ownership:

```text
ATK / CRIT / CRIT DMG / KNOCK = personal combat modifiers
FORTIFICATION / DEF            = personal spending decisions that benefit the shared wall
```

But do **not** freeze the legacy multiplayer aggregation values in P5.

Legacy solo Rank10 reference:
- HP: +1000 wall max/current;
- DEF: 25pp generic DR;
- combined nominal full-health raw-damage tolerance: `3000 / 0.75 = 4000`, about 2x the base 2000 wall.

If four humans each contributed the full legacy values directly:
- shared max HP could become 6000;
- summed DEF reaches the prototype 60% cap;
- nominal raw-damage tolerance becomes `6000 / 0.40 = 15000`, 7.5x the base wall before accounting for multiplayer enemy scaling.

This does not prove the shared model is wrong. It proves that per-player contribution scaling/caps are inseparable from P10 multiplayer pressure/economy scaling.

**Recommendation:** preserve shared-wall benefit semantics, defer exact multiplayer aggregation/cap to P10/P10R.

---

# 6. Six categories — structurally coherent; prototype coefficients are not balanced for final use

Keep the category set as the first P5 candidate:

```text
ATK
CRIT CHANCE
CRIT DAMAGE
FORTIFICATION
DEFENSE
KNOCKBACK
```

But current prototype offense coefficients strongly favor ATK when considered alone.

With no other crit source:
- ATK Rank1: +8% outgoing scalar for 40 coin;
- CRIT Rank1: +2pp chance at base 1.5x proc multiplier, about +1% expected damage for 44 coin;
- CRIT-DMG Rank1 has zero expected value if crit chance is literally zero.

Legacy maxima under the same simplified baseline:
- ATK10 alone -> 1.80x damage scalar;
- CRIT10 alone -> about 1.10x expected damage;
- CRIT10 + CRIT-DMG10 -> about 1.40x expected damage;
- all three offense tracks maxed -> about 2.52x expected damage.

Final value depends on permanent crit sources, class hit plans and P2 crit policy, so this is not a final balance verdict. It is enough to reject blind reuse of the legacy coefficients.

Knockback/DEF/Fortification likewise require class/role-aware marginal-value simulation rather than nominal percentage comparison.

---

# 7. Revised P5 candidate package after quantitative review

```text
1. Shop mechanically available after every Stage except Stage50,
   but implemented later as optional/fast intermission, not a mandatory long menu.

2. Keep killer-only monster coin as the current candidate.
   Retain an all-human Stage-clear income floor candidate.
   Change ownership only if measured class kill-share creates persistent purchase-rank unfairness.

3. Fortification purchase increases max HP and current HP by the same realized amount.
   Treat this as adding intact wall capacity, not generic healing.

4. Personal wallets / personal offensive-control ranks remain.
   Defensive purchases benefit the shared wall.
   Exact multiplayer contribution aggregation/cap is deferred to P10/P10R.

5. Keep the six-category shop for P5 simulation.
   Rebuild reward, cost and effect curves for the 50-Stage economy; do not reuse prototype values by inertia.
```

User approval is still required before promoting this revised package into a structural P5 contract.
