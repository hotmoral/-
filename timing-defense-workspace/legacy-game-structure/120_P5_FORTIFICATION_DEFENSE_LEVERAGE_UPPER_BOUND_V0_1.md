# Timing Defense — P5 Fortification / DEF Leverage Upper-Bound Review V0.1

Date: 2026-10-23 KST  
Status: **DEFENSIVE UPPER-BOUND SCREEN / LEGACY MAGNITUDE HIGH-RISK / FULL COMBAT INTEGRATION REQUIRED / NO NUMERICAL FREEZE**

Depends on:
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
- `119_P5_CLEAR_KILL_INCOME_MIX_SENSITIVITY_V0_1.md`
- P4 exact Stage49 full-rotation evidence

---

# 0. Purpose

Before implementing a full shop+combat kernel, screen how large Fortification/DEF could become if their defensive benefit is viewed in isolation.

This is intentionally an **optimistic upper bound for defense** because it does not yet penalize DEFENSE_HEAVY for its lower offensive investment.
Therefore it may identify obviously dangerous magnitudes, but it cannot prove a final balanced value.

---

# 1. Rank profiles from CENTER economy preflight

Representative Stage49 profiles:

```text
BALANCED:      FORT8 / DEF7
DEFENSE_HEAVY: FORT10 / DEF8
```

Reference late two-consecutive-miss low wall reserves from the admitted P4 Stage49 candidate:

```text
Knight 820
Rogue 340
Tank 1725
Archer 1700
Mage 1890
```

These values are diagnostic Stage49 pressure evidence, not launch authoring.

---

# 2. Defensive magnitude sensitivity

Test only as fractions of legacy magnitude:

```text
LOW      Fort +40/rank   DEF +1.0pp/rank
CENTER   Fort +60/rank   DEF +1.5pp/rank
HIGH     Fort +80/rank   DEF +2.0pp/rank
LEGACY   Fort +100/rank  DEF +2.5pp/rank
```

No candidate is approved.

Upper-bound approximation:

```text
stage49 start current wall = 2000 + retained Fortification repair
observed P4 wall loss *= (1 - generic DEF)
```

Caveats:
- actual P2 order applies generic DEF before unique class defense and shields;
- accumulated earlier Stage damage can consume/waste Fortification repair;
- lower offensive shop investment can increase enemy survival and future wall damage;
- therefore this arithmetic is not a combat substitute.

---

# 3. DEFENSE_HEAVY upper-bound snapshots

For FORT10 / DEF8:

```text
LOW:    start 2400 / DR 8%
Knight 1314 / Rogue 873 / Tank 2147 / Archer 2124 / Mage 2299

CENTER: start 2600 / DR 12%
Knight 1562 / Rogue 1139 / Tank 2358 / Archer 2336 / Mage 2503

HIGH:   start 2800 / DR 16%
Knight 1809 / Rogue 1406 / Tank 2569 / Archer 2548 / Mage 2708

LEGACY: start 3000 / DR 20%
Knight 2056 / Rogue 1672 / Tank 2780 / Archer 2760 / Mage 2912
```

Interpretation:
- legacy magnitude can transform very severe late mistake reserves into large surviving reserves in a defense-favorable upper bound;
- this is a strong warning against blindly carrying prototype +100 HP / +2.5pp DEF into the 50-Stage economy;
- even lower candidates are large enough that full combat feedback is mandatory.

---

# 4. BALANCED upper-bound snapshots

For FORT8 / DEF7:

```text
LOW:    start 2320 / DR 7%
Knight 1223 / Rogue 776

CENTER: start 2480 / DR 10.5%
Knight 1424 / Rogue 994

HIGH:   start 2640 / DR 14%
Knight 1625 / Rogue 1212

LEGACY: start 2800 / DR 17.5%
Knight 1827 / Rogue 1431
```

Even balanced investment can materially change late reserve if repair is fully retained.
Again, this is an upper-bound screen, not a final balance result.

---

# 5. Structural conclusion

```text
LEGACY_DEFENSIVE_MAGNITUDE_SAFE_TO_PROMOTE = NO
FORTIFICATION_SEMANTIC_DEFECT = NO
SHARED_DEF_SEMANTIC_DEFECT = NO
FULL_COMBAT_INTEGRATION_REQUIRED = YES
```

Do not remove Fortification repair or shared DEF based on this screen.
Instead calibrate magnitude/cost under real offensive opportunity cost and persistent wall damage.

---

# 6. Next full integration requirements

A valid P5 defensive simulation must include simultaneously:
- chosen shop policy and rank trajectory;
- ATK/CRIT/CRITDMG/KNOCK opportunity cost;
- P2 generic DEF order before Tank unique defense/shields;
- Fortification max increase and matched repair at purchase time, not one free Stage49 lump;
- persistent BaseHP across all simulated Stages;
- Stage49->50 reserve;
- actual enemy survival/kill timing changes caused by weaker offense;
- valid timing-action/EXP opportunity changes.

First defensive magnitude search should remain below/around the legacy envelope rather than assume legacy values.

No production value is frozen.