# Timing Defense — P5 All-Class Shop Combat Method Fidelity Review V0.1

Date: 2026-10-23 KST  
Status: **METHOD FIDELITY REVIEW COMPLETE / CROSS-CLASS KNOCKBACK LANE DEFERRED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
- `121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md`
- `122_P5_TANK_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `../combat_exact_v016.py`

---

# 0. Purpose

Before promoting the Tank-only fixed-rank shop probe into a five-class comparison, verify that every shop stat family is actually represented symmetrically enough in the current P4 late-game diagnostic kernel to support cross-class conclusions.

Result:

```text
ATK = usable in first cross-class lane
FORTIFICATION = usable in first cross-class lane
DEFENSE = usable in first cross-class lane
KNOCKBACK = NOT cross-class-authoritative in current P4 diagnostic kernel
CRIT / CRITDMG = intentionally separate because attack-template crit policy is effect-specific
```

---

# 1. Recovered shop family authority

P5 authority recovery maps the six categories to P2 typed families:

```text
ATK      -> attackPct / attackFlat
CRIT     -> critChancePp
CRITDMG  -> critDamageBonus
FORT     -> wallHpFlat / explicit matched repair semantic
DEF      -> generic wallDamageReductionPp
KNOCK    -> knockbackPct
```

Prototype legacy sensitivity anchors remain:

```text
ATK +8% / rank
CRIT +2pp / rank
CRITDMG +15% bonus / rank
FORT +100 max HP + matched current repair / rank
DEF +2.5pp / rank
KNOCK +10% / rank
```

These are sensitivity anchors only, not production values.

---

# 2. Cross-class KNOCKBACK fidelity mismatch

The exact v0.16 formula reference contains ordinary push behavior for all five classes:

- Knight pushes primary and penetrations;
- Rogue pushes primary/follow-up dagger targets;
- Tank pushes primary and heavy-area targets;
- Archer pushes primary/penetration/triple-shot targets;
- Mage pushes primary/splash/resonance targets.

The current simplified P4 Stage46/49 Lv31 mastery diagnostic kernel, however, explicitly executes `push()` only in Knight and Tank attack paths.

Therefore applying the P5 `knockbackPct` shop modifier directly to that kernel would produce an invalid cross-class comparison:

```text
Knight / Tank -> KNOCK shop has modeled gameplay effect
Rogue / Archer / Mage -> KNOCK shop would appear to have zero modeled effect
```

That would be a simulator coverage defect, not a product truth.

New watch:

```text
P5_KNOCKBACK_KERNEL_COVERAGE_GAP = ACTIVE
```

---

# 3. Why not silently patch KNOCK immediately

A blanket patch would risk inventing semantics for later generated effects.

Questions still distinct:
- ordinary/manual root hit knockback inheritance;
- penetration/splash generated-hit knockback;
- Lv26 generated effects;
- Lv31 final generated hits;
- whether every generated hit inherits generic shop knockback or only explicitly pushing hit templates.

P2 requires scalar stats and effect rules to remain separate. Therefore the first five-class shop comparison must not silently infer all generated-hit KNOCK behavior.

---

# 4. First five-class lane — corrected scope

The first cross-class fixed-rank Stage49 screen is restricted to:

```text
ATK
FORTIFICATION
DEFENSE
```

Excluded from cross-class authority:

```text
KNOCKBACK -> deferred to dedicated inheritance/parity lane
CRIT / CRITDMG -> deferred to policy-correct attack-template lane
```

This preserves attribution:
- ATK tests outgoing scalar power feedback;
- FORT tests max+matched-repair reserve leverage;
- DEF tests generic shared-wall mitigation;
- class skill/effect identities remain current P4 diagnostic structure.

Tank-only doc122 remains valid as an internal Tank sensitivity result because KNOCK was represented in that Tank kernel. It must not be generalized as cross-class KNOCK evidence.

---

# 5. Baseline fidelity requirement

Before interpreting shop effects, the all-class reconstruction must reproduce the current no-shop Stage49 diagnostic baselines:

```text
Knight all-success wall1705 / all-finals-missed burial34.025s
Rogue  all-success wall2000 / all-finals-missed burial29.100s
Tank   all-success wall2000 / corrected all-finals-missed burial34.700s
Archer all-success wall2000 / all-finals-missed burial57.025s
Mage   all-success wall2000 / all-finals-missed burial52.225s
```

Tank uses the corrected Iron Wall-on-SIEGER semantic from doc121.

---

# 6. Decision rule for the next result

Do not interpret a class surviving the 60-second shop-integrated Stage49 fixture as automatic shop overbalance.

First distinguish:

```text
A. defense reserve/DR leverage
B. offensive kill-order threshold from ATK
C. encounter-pressure margin after adding the P5 power layer
D. class-specific geometry/role interaction
E. simulator coverage gap
```

Repair order:
1. fix simulator fidelity/coverage gaps;
2. decompose ATK vs FORT vs DEF contribution;
3. recalibrate late encounter pressure with shop power present;
4. only then alter exact shop magnitudes;
5. do not introduce hidden per-class shop prices/corrections.

---

# 7. Boundary

Next:
- run all five classes at legacy-relative `30% / 40% / 50%` for ATK/FORT/DEF only;
- policies `ATTACK_HEAVY / DEFENSE_HEAVY / BALANCED / ROLE_AWARE`;
- all-success / one-miss / two-miss / all-finals-missed for all combinations;
- detailed eight-consecutive-miss sweep only at 40% for BALANCED and ROLE_AWARE;
- add Archer/Mage ATK-vs-defense ablation because their no-shop Stage49 margins are closest to the 60s boundary.

No production change is authorized.