# Timing Defense — P5 Tank Fixed-Rank Shop Combat Preflight V0.1

Date: 2026-10-23 KST  
Status: **TANK-ONLY DIRECTIONAL COMBAT PREFLIGHT / LEGACY MAGNITUDE TOO GENEROUS / NEXT SEARCH 30-50% / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
- `120_P5_FORTIFICATION_DEFENSE_LEVERAGE_UPPER_BOUND_V0_1.md`
- `121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md`

Assets:
- `data/p5_tank_fixed_rank_shop_stage49_fixture_v0_1.json`
- `../../tools/run_p5_tank_fixed_rank_shop_stage49_probe_v0_1.py`

---

# 0. Scope

This is the first combat-integrated shop screen for Tank only.

It combines:
- corrected Tank Lv11 Iron Wall on ordinary wall contact + SIEGER shots;
- v0.5 no-target/no-bank + Lv31 barrier non-downgrade semantics;
- Stage49 complementary rotation fixture;
- fixed Stage49 shop-rank snapshots from the CENTER50 economy envelope;
- ATK / KNOCKBACK / FORTIFICATION / generic DEF together.

It intentionally omits CRIT / CRIT DAMAGE from this first lane because final per-attack-template crit policy is effect-specific.

Fortification is modeled as **fully retained Stage49 starting reserve**, therefore this lane is defense-favorable and acts as an upper bound compared with a real purchase-time persistent run.

---

# 1. Baseline fidelity

The focused reconstruction first reproduced the prior admitted Tank Stage49 v0.5/v0.2 result exactly, then applied the Iron Wall/SIEGER correction documented in doc121.

Corrected no-shop baseline:

```text
all success: wall2000 / active11
one miss: wall2000 across starts
two consecutive miss minimum: wall1732.5
all finals missed from beginning: burial34.700s
```

Corrected first burial consecutive-miss counts:

```text
LINE 6
CLUSTER 6
FRONTLINE 5
DURABLE 5
TIME_BUDGET_SIEGER 5
```

This is the comparison baseline for the shop screen.

---

# 2. CENTER50 fixed Stage49 rank profiles

First scalar-lane profiles:

```text
ATTACK_HEAVY
ATK9 / KNOCK7 / FORT7 / DEF6

DEFENSE_HEAVY
ATK6 / KNOCK8 / FORT10 / DEF8

BALANCED
ATK8 / KNOCK8 / FORT8 / DEF7

ROLE_AWARE_TANK
ATK6 / KNOCK10 / FORT8 / DEF8
```

CRIT ranks are ignored in this lane rather than assigned fake value.

---

# 3. Effect-magnitude sensitivity

The first screen scales all four legacy per-rank magnitudes together:

```text
legacy reference:
ATK +8% / rank
KNOCK +10% / rank
FORT +100 max+matched repair / rank
DEF +2.5pp / rank

screened scale:
40% / 60% / 80% / 100%
```

This common scale is a diagnostic only. Final stat families do not need to share one percentage scale.

---

# 4. All-success result

All tested profiles/scales survive all-success Stage49 pressure.

At 40% magnitude:

```text
ATTACK_HEAVY start/end wall 2280
DEFENSE_HEAVY 2400
BALANCED 2320
ROLE_AWARE_TANK 2320
```

No wall pressure reaches the wall on all-success paths in this Tank lane, so retained Fortification reserve remains visible.

This is expected and does not by itself prove Fortification balance.

---

# 5. All-finals-missed stress

Burial time when every final is missed from the beginning:

```text
                40%      60%      80%      100%
ATTACK_HEAVY    38.375   38.250   50.350   57.550
DEFENSE_HEAVY   38.750   38.725   50.200   46.225
BALANCED        38.750   38.825   51.150   58.325
ROLE_AWARE      38.250   39.425   41.625   57.225
```

No tested profile becomes literally immortal when every final is missed from Stage start.

However 80–100% legacy magnitude can delay collapse by roughly 7–24 seconds relative to the corrected no-shop 34.700s baseline.

Because the Stage49 fixture lasts only 60 seconds, that is a very large late-run leverage signal.

---

# 6. Repeated-miss budget after earlier success

The stronger warning appears when the player has already banked successful finals and then begins a long failure streak.

At 40%:
- most grammar starts first bury around 6–7 consecutive misses;
- this is only a moderate extension over the no-shop 5–6-miss Tank baseline;
- some very late FRONTLINE starts can survive longer simply because insufficient Stage time remains, so burial-count comparisons must be read together with Stage49->50 reserve.

At 60%:
- several profiles/grammar starts survive beyond eight misses;
- some late starts remain alive even at sixteen misses with very low reserve.

At 80–100%:
- many starts survive sixteen consecutive missed finals;
- this is too forgiving to use as a first production center under the retained-repair upper-bound assumption.

Classification:

```text
LEGACY_80_TO_100_PERCENT_MAGNITUDE = HIGH_RISK_FOR_TANK_ERROR_BUDGET
LEGACY_40_PERCENT_MAGNITUDE = PLAUSIBLE_FIRST_SEARCH_CENTER
LEGACY_60_PERCENT_MAGNITUDE = UPPER-WATCH / NOT REJECTED YET
```

---

# 7. Important non-monotonic timing note

All-finals-missed burial time is not perfectly monotonic across common effect scale/profile.

Reason:
- ATK/KNOCK changes kill/order/reposition chronology;
- SIEGER shot counts and ordinary wall hits change;
- stronger knockback can delay some bodies while leaving role pressure alive longer;
- Fortification/DEF changes reserve separately.

Therefore do not tune one scalar from burial time alone.
Use:
- wall reserve;
- kills;
- active backlog;
- SIEGER shots;
- wall hits;
- mistake-budget distribution.

---

# 8. Next search envelope

For the first **five-class** fixed-rank shop+combat probe, narrow the common legacy-relative magnitude sensitivity to:

```text
30% / 40% / 50%
working diagnostic center = 40%
```

Rationale:
- 40% gives Tank meaningful shop growth without erasing sustained-failure danger;
- 60% already produces long forgiving tails in this defense-favorable lane;
- 80–100% is too generous as a first search region;
- exact families can later diverge rather than sharing one scale.

No 40% production value is approved.

---

# 9. Next required integration

1. run 30/40/50% fixed-rank scalar lane across all five classes;
2. include ATK/KNOCK/FORT/DEF where applicable through P2 semantics;
3. keep CRIT/CRITDMG separate until explicit attack-template policy is respected;
4. compare ATTACK_HEAVY / DEFENSE_HEAVY / BALANCED / ROLE_AWARE;
5. measure Stage49->50 wall reserve and active backlog, not burial alone;
6. then model Fortification purchase timing across multiple Stages rather than granting all retained repair at Stage49;
7. only after that revisit per-rank family magnitudes.

No production implementation is authorized.