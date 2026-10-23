# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production checkpoint
- branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes remain unauthorized

## Operating authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active dependency plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_20.yaml`
- live remote always wins
- do not rerun closed PASS/APPROVED work without a concrete trigger

---

# Current phase

**P4 PROVISIONAL STRUCTURAL COMPLETE_WITH_WATCHES / P5 A2 USER_APPROVED — ECONOMY PREFLIGHT ACTIVE**

```text
P0..P3 structural foundation complete
-> P4 player-power spine provisional structural complete with watches
-> P4-E complete; final EXP deferred to P10R
-> P5 authority recovery complete
-> P5 quantitative precheck complete
-> A2 USER APPROVED
-> 50-Stage spend-capacity envelope built
-> economy-only policy preflight directional PASS
-> clear/kill income-mix + wall-pressure integration NEXT
```

Latest P5 authority:
- `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `legacy-game-structure/117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
- `legacy-game-structure/118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
- `legacy-game-structure/data/p5_shop_economy_spend_capacity_fixture_v0_1.json`
- `tools/run_p5_shop_economy_spend_capacity_probe_v0_1.py`
- historical proposal/recovery: docs112–115; doc113 is superseded where conflicting.

---

# P4 stable closure facts

- 5 classes: Knight / Rogue / Tank / Archer / Mage.
- Tier = 50 Stages; BaseHP persists; no automatic Stage heal.
- Lv31 acquisition target direction Stage41–45; Stage46+ mastery pressure.
- strong class-defining Lv31 finals remain finite/deterministic/attributable.
- Archer wider straight gameplay corridor USER APPROVED.
- Stage49 complementary rotation exact-admitted.
- durable high-HP/high-armor pressure supported diagnostically, not a new-monster approval.
- BRUTE carrying/using SHIELD-like protection remains parked for later monster design.
- final EXP remains OPEN / P10R mandatory.

P4 exact replay identities remain in docs109–111 and must not be rerun without a trigger.

---

# P5 A2 — USER APPROVED STRUCTURE

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
+
PERSONAL WALLETS
+
KILLER_ONLY_PERSONAL ordinary-monster coin baseline
+
ALL-HUMAN Stage-clear income-floor candidate
+
FORTIFICATION = max HP increase + matched current repair
+
PERSONAL ATK/CRIT/CRITDMG/KNOCK
+
PERSONAL PURCHASES CONTRIBUTING TO SHARED FORTIFICATION/DEF
+
SIX SHOP CATEGORIES
```

Six categories:

```text
ATTACK
CRIT CHANCE
CRIT DAMAGE
FORTIFICATION
DEFENSE
KNOCKBACK
```

New user-approved economy direction:

```text
NO_ROUTINE_FULL_SHOP_MAXOUT_BY_STAGE49
```

Meaning:
- ordinary successful intended-entry runs must retain meaningful late allocation choices;
- specialization may max/near-max selected tracks if other tracks are sacrificed;
- six-track full max must not be the routine/expected Stage49 state.

No exact coin/reward/price/rank-effect/cap is frozen.

---

# Correct legacy cost reference

The prototype cost function uses positive-value JavaScript `Math.round`.
Correct nominal Rank10 full-shop sensitivity cost:

```text
ATK 2725
CRIT 3000
CRITDMG 2725
FORT 2455
DEF 3000
KNOCK 2455
TOTAL 16360
```

Earlier 16350 text came from banker-rounding on some `.5` values and is superseded numerically. Structural conclusions are unchanged.

---

# P5 spend-capacity preflight

First bounded sensitivity:

```text
LOW45    = 7,362 nominal units
CENTER50 = 8,180
HIGH55   = 8,998
```

All are ratio-space candidates only.

Economy-only result:
- no tested 45/50/55 policy maxed all six tracks;
- LOW45 maxed no single track;
- CENTER50 permits selected late specialization maxes around Stage45–49 while balanced remains Rank7–8;
- HIGH55 still preserves incomplete nonfavored tracks;
- balanced CENTER Stage49 ≈ `ATK8 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK8`.

Working direction:

```text
WORKING_SPEND_CAPACITY_CENTER = 50%
SENSITIVITY = 45%..55%
```

Not a numerical freeze.

---

# Killer-only coin / income mix

Kill credit does not directly grant EXP. Current evidence does not demonstrate a large first-order killer-only snowball.

Next income-source sensitivity:

```text
CLEAR/KILL
80/20
70/30 <- working center candidate
60/40
```

At CENTER50 with a ±20% relative kill-share perturbation:
- 80/20 -> whole-wallet ~48%..52%
- 70/30 -> ~47%..53%
- 60/40 -> ~46%..54%

For 70/30, balanced Stage49 stays broadly Rank7–8. Even ±40% relative kill-share stress gives ~44%..56% total capacity and does not approach full-shop maxout.

`70/30` is a working candidate only, not frozen.

---

# P5 next boundary

1. formalize clear/kill income-mix sensitivity and class/player-count perturbations;
2. integrate Fortification + DEF with representative wall-pressure combat;
3. reject any curve that erases attrition or trivializes Stage49->50 reserve;
4. compare ATTACK_HEAVY / CRIT_HEAVY / DEFENSE_HEAVY / BALANCED / SAVE_DELAY / ROLE_AWARE under combat feedback;
5. re-measure valid timing-event count / EXP / P4 skill-reach drift;
6. keep P10 multiplayer normalization and P10R final EXP convergence downstream.

P6 remains blocked until P5 closes.

No user decision is currently pending.
No production change is authorized.
