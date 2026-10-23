# Timing Defense — P5 Post-Shop Stage49 Entry-Depth Reconvergence V0.1

Date: 2026-10-23 KST  
Status: **PROMISING AUTHORING-FIRST RECONVERGENCE / DIAGNOSTIC DEPTHS ONLY / EXACT COMMITTED REPLAY PENDING / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `123_P5_ALL_CLASS_SHOP_COMBAT_METHOD_FIDELITY_REVIEW_V0_1.md`
- `124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
- `106_P4D2_STAGE49_FULL_ROTATION_DIRECTIONAL_PROBE_V0_1.md`

---

# 0. Problem after P5 shop power

At the 40% legacy-relative ATK/FORT/DEF diagnostic center, the original P4 Stage49 fixture remains meaningfully mastery-sensitive for Knight/Rogue/Tank but is too forgiving for Archer/Mage after shop ATK changes kill/order chronology.

This must not be repaired first by:
- nerfing Lv31 finals;
- hidden per-class shop prices;
- blanket HP/spawn inflation;
- removing the approved Archer wide corridor;
- undoing Rogue cadence or Tank defensive identity.

The approved repair order favors authoring/role timing before scalar inflation.

---

# 1. Inherited-deficit sensitivity

Because Fortification preserves absolute damage deficit (doc125), the fixed-rank Stage49 lane's optimistic assumption is `preStage49Deficit=0`.

At 40% BALANCED with max wall2320:

## Archer

Original shop-integrated all-finals-missed result:

```text
end wall1948
Stage49 damage consumed only ~372
```

The same combat chronology would require an inherited deficit of roughly `~1948` before Stage49 to reach zero during this stress.

Directional sensitivity:

```text
deficit1750 -> end wall198
~deficit2000 -> burial begins
```

That is too large to dismiss as ordinary carryover damage.

## Mage

Original all-finals-missed result:

```text
end wall1227.25
Stage49 damage consumed ~1092.75
```

Burial begins around inherited deficit `~1227`.

Therefore pre-Stage49 attrition alone is not an adequate structural repair, especially for Archer.

---

# 2. Archer low-order ATK breakpoint trace

A targeted trace compared BALANCED Archer all-finals-missed with very small ATK sensitivities while FORT/DEF were removed.

Relevant ordinary PERFECT raw before shop:

```text
base200 * Archer Lv11 1.10 = 220
```

At rank8, legacy ATK reference is `8 * 8% = 64%`; multiplying this by only ~3.55% of legacy magnitude gives ~+2.27% total ATK, enough to cross the FLYER diagnostic HP225 one-hit boundary.

Observed:

```text
ATK legacy-scale 0.03 -> total ATK +1.92% -> burial57.025s
ATK legacy-scale 0.04 -> total ATK +2.56% -> survives / wall765
```

Trace first causal ordering divergence:
- at `t=4.700`, the +2.56% path kills `FLYER_12` in that action;
- the +1.92% path leaves it alive until the `t=5.825` action;
- the freed next target/action changes the subsequent frontmost and penetration chronology;
- later kills, SIEGER exposure and wall contacts diverge substantially.

This does **not** mean FLYER HP should simply be increased. It proves the old Stage49 diagnostic is brittle around discrete late-power breakpoints and must be reconverged with shop power present.

New watch:

```text
P5_ARCHER_ATK_BREAKPOINT_CHRONOLOGY_WATCH = HIGH
```

---

# 3. Authoring-first axis tested

Instead of altering monster HP/damage or class/shop coefficients, test **entry depth** in the existing late-role grammar only.

Diagnostic coordinate convention:
- larger x = farther from wall;
- smaller x = deeper/closer entry;
- historical fixture default spawn x = 0.92.

Bounded candidate family:

```text
TIME_BUDGET_SIEGER SIEGER entry x ~= 0.45..0.55
DURABLE_SCATTER / TIME_BUDGET durable proxy entry x ~= 0.60..0.70
```

All other Stage49 bodies/HP/speed/skill coefficients remain unchanged.

This is a geometry/timing authoring sensitivity, not production coordinates.

---

# 4. Recommended diagnostic center

A useful bounded center was found around:

```text
TIME_BUDGET SIEGER entry x ~= 0.48
DURABLE_SCATTER + TIME_BUDGET durable entry x ~= 0.65
```

Again: **these numbers are not authoring freeze values.**

They demonstrate that the missing pressure axis can be recovered through role-entry timing/depth rather than player-power nerfs.

---

# 5. All-success result across all four shop policies

40% ATK/FORT/DEF lane.

All 20 class/policy combinations survive.

Approximate remaining-wall fractions by class across policies:

```text
Knight  ~78.6%..86.4%
Rogue   100%
Tank    100%
Archer  ~76.6%..79.0%
Mage    ~93.8%..94.3%
```

All-success still shows class asymmetry:
- Knight/Archer pay more wall reserve for the deeper role pressure;
- Rogue/Tank largely prevent wall damage;
- Mage retains strong successful-final recovery.

No exact Stage50 reserve floor is frozen.

---

# 6. One/two-miss recoverability

Across all four policies:

```text
ATTACK_HEAVY
DEFENSE_HEAVY
BALANCED
ROLE_AWARE
```

and all five classes:

```text
one missed final -> 0 burial cases
two consecutive missed finals -> 0 burial cases
```

Even the lowest two-miss surviving reserves remain above zero.

This preserves the approved mastery shape that an isolated or short mistake sequence is recoverable.

---

# 7. All-finals-missed result

## Knight / Rogue / Tank

All four purchase policies bury within the 60s fixture.
Approximate ranges:

```text
Knight ~29.75..32.53s
Rogue  ~32.03..32.15s
Tank   ~32.65..33.85s
```

This is strong pressure, but not produced by global HP/spawn inflation.

## Archer

Does not always bury within 60s, but reserve becomes severe:

```text
ATTACK_HEAVY  end306 / 2280  (~13.4%)
DEFENSE_HEAVY end872.8 / 2400 (~36.4%)
BALANCED      end171.7 / 2320  (~7.4%)
ROLE_AWARE    end306 / 2280   (~13.4%)
```

## Mage

```text
ATTACK_HEAVY  end282.5 / 2280 (~12.4%)
DEFENSE_HEAVY buried ~55.275s
BALANCED      end343.75 / 2320 (~14.8%)
ROLE_AWARE    end432.9 / 2280 (~19.0%)
```

Thus repeated total mastery failure no longer enters Stage50 healthy.

This meets the existing structural interpretation that all-finals-missed should either bury or leave a clearly non-viable reserve; exact reserve threshold remains open.

---

# 8. Consecutive-miss budgets at BALANCED / ROLE_AWARE

At the same diagnostic center:

### Knight
first burial appears roughly at 4–6 consecutive misses depending grammar.

### Rogue
roughly 5–6.

### Tank
roughly 5–6.

### Archer
- generally survives the bounded eight-miss sweep;
- BALANCED eight-miss reserves range roughly 460..1269 depending grammar;
- ROLE_AWARE `DURABLE_SCATTER` can bury at eight; other starts carry reduced reserve.

### Mage
- BALANCED `DURABLE_SCATTER` can bury at eight;
- other eight-miss starts retain widely varying reserve;
- ROLE_AWARE durable start can fall to near-zero without burial.

Identical error budgets are neither required nor desired.

---

# 9. Why this direction is preferable to scalar shop nerf

The authoring-depth candidate:
- keeps the shop visibly valuable;
- keeps Lv31 finals explosive;
- preserves Archer wide-corridor approval;
- preserves Tank larger time budget;
- preserves Mage cluster recovery;
- restores consequence to sustained P×P failure;
- avoids hidden class-specific prices;
- avoids blanket HP/spawn inflation;
- respects the established repair order of entry depth / relative depth / timing before durability scalars.

Therefore:

```text
POST_SHOP_PRESSURE_REPAIR_LAYER = AUTHORING ENTRY DEPTH / ROLE TIMING FIRST
```

---

# 10. Remaining cautions

This is not final Stage49 authoring because:
- x=.48/.65 are normalized diagnostic positions only;
- CRIT/CRITDMG are not yet integrated;
- cross-class KNOCK is not yet policy-correct;
- exact Stage46–48 shop-power pressure must also reconverge;
- Stage50 content/reserve floor is not frozen;
- multiplayer scaling remains P10;
- final EXP convergence remains P10R.

The newly committed P5 all-class runner also still needs exact checkout replay admission.

---

# 11. Verdict

```text
P5_POST_SHOP_STAGE49_PRESSURE_GAP = CONFIRMED
PRE_STAGE49_DEFICIT_ALONE = INSUFFICIENT_REPAIR_ESPECIALLY_ARCHER
ARCHER_LOW_ATK_BREAKPOINT = CONFIRMED_DIRECTIONALLY
GLOBAL_SHOP_NERF = REJECT_AS_NEXT_LAYER
HIDDEN_CLASS_SHOP_COMPENSATION = REJECT
ENTRY_DEPTH_ROLE_TIMING_REPAIR = PROMISING
ALL_SUCCESS_SURVIVES_20_OF_20_POLICY_CLASS_COMBOS = YES
ONE_MISS_BURIALS = 0
TWO_MISS_BURIALS = 0
ALL_FINALS_MISSED_ENTERS_STAGE50_HEALTHY = NO AT DIAGNOSTIC_CENTER
EXACT_AUTHORING_COORDINATES_FROZEN = NO
PRODUCTION_CHANGE = NO
```
