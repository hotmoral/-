# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production checkpoint
- branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes remain unauthorized

## Operating authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active dependency plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_22.yaml`
- live remote always wins
- do not rerun closed PASS/APPROVED work without a concrete trigger

---

# Current phase

**P4 PROVISIONAL STRUCTURAL COMPLETE_WITH_WATCHES / P5 A2 USER_APPROVED — FIVE-CLASS FIXED-RANK SHOP+COMBAT PROBE NEXT**

```text
P0..P3 structural foundation complete
-> P4 player-power spine provisional structural complete with watches
-> P5 authority recovery complete
-> A2 USER APPROVED
-> spend-capacity preflight PASS directionally
-> clear/kill income-mix sensitivity complete
-> defensive upper-bound screen complete
-> Tank Iron Wall/SIEGER fidelity defect corrected directionally
-> Tank fixed-rank shop+combat preflight complete
-> five-class fixed-rank Stage49 shop+combat probe NEXT
```

Latest authority/evidence:
- `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `legacy-game-structure/117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
- `legacy-game-structure/118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
- `legacy-game-structure/119_P5_CLEAR_KILL_INCOME_MIX_SENSITIVITY_V0_1.md`
- `legacy-game-structure/120_P5_FORTIFICATION_DEFENSE_LEVERAGE_UPPER_BOUND_V0_1.md`
- `legacy-game-structure/121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md`
- `legacy-game-structure/122_P5_TANK_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `legacy-game-structure/data/p5_shop_economy_spend_capacity_fixture_v0_1.json`
- `legacy-game-structure/data/p5_tank_fixed_rank_shop_stage49_fixture_v0_1.json`
- `tools/run_p5_shop_economy_spend_capacity_probe_v0_1.py`
- `tools/run_p5_tank_fixed_rank_shop_stage49_probe_v0_1.py`

---

# Stable upstream truth

- 5 classes: Knight / Rogue / Tank / Archer / Mage.
- Tier = 50 Stages.
- BaseHP persists across Stages; no automatic Stage heal.
- Lv31 acquisition direction = Stage41–45; Stage46+ mastery pressure.
- strong class-defining Lv31 finals remain bounded/deterministic/attributable.
- final EXP remains OPEN / P10R mandatory.
- production remains unchanged.

---

# P5 A2 — USER APPROVED

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
PERSONAL WALLETS
KILLER_ONLY PERSONAL ordinary-monster coin baseline
ALL-HUMAN Stage-clear income-floor candidate
FORTIFICATION = max HP increase + matched current repair
ATK/CRIT/CRITDMG/KNOCK = personal
FORTIFICATION/DEF = personal purchases contributing to shared wall
six shop categories
NO_ROUTINE_FULL_SHOP_MAXOUT_BY_STAGE49
```

Specialization may max/near-max selected tracks late if meaningful sacrifices remain elsewhere.
No exact coin/reward/price/rank-effect/cap is frozen.

---

# Exact legacy shop sensitivity reference

Prototype positive-value JavaScript `Math.round` cost semantics:

```text
ATK 2725
CRIT 3000
CRITDMG 2725
FORT 2455
DEF 3000
KNOCK 2455
TOTAL 16360
```

Earlier `16350` text used banker-rounding on some `.5` values and is numerically superseded.

---

# Working 50-Stage economy envelope — NOT FROZEN

```text
LOW45    = 7362 nominal units
CENTER50 = 8180 <- working center
HIGH55   = 8998
```

Economy-only results:
- no tested policy maxed all six tracks;
- CENTER balanced Stage49 ≈ `ATK8 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK8`;
- selected specialization can max one favored late track around Stage45–49;
- broad allocation tradeoffs remain.

---

# Clear / kill income source sensitivity — NOT FROZEN

Candidates:

```text
80/20
70/30 <- working center supported
60/40
```

At total CENTER50 with ±20% relative kill-share deviation:

```text
80/20 -> ~48%..52% total capacity
70/30 -> ~47%..53%
60/40 -> ~46%..54%
```

For 70/30, moderate kill-share divergence changes the Stage49 balanced total rank count only modestly in the first arithmetic preflight.
Killer-only coin remains a valid baseline candidate; class/team kill-share remains an active combat-integrated watch.

---

# Tank Iron Wall / SIEGER fidelity correction

Recovered Lv11 contract:

```text
Tank Iron Wall = shared wall incoming x0.90 / multiple Tanks nonstack
```

Historical P4 kernel applied this to ordinary wall contact but omitted it from SIEGER wall shots. No contract authorizes that exception.

Targeted independent revalidation first reproduced the old admitted Tank baseline, then corrected the SIEGER path:

```text
no-shop all success: wall2000 unchanged
one miss: wall2000 unchanged
two-miss min: 1725 -> 1732.5
all-finals-missed burial: 34.575s -> 34.700s
TIME_BUDGET_SIEGER first burial: 4 misses -> 5 misses
```

Other grammar first-burial counts remain structurally unchanged.

Classification:

```text
P4 structural closure reopen = NO
old Tank SIEGER-specific numerics = superseded
v0.6 / Stage49 v0.3 committed exact replay = PENDING
```

P5 must use the corrected semantic:

```text
generic shop DEF
-> Tank Iron Wall x0.90
-> shield
-> BaseHP
```

---

# Tank fixed-rank shop+combat preflight

CENTER50 Stage49 rank profiles were combined with ATK/KNOCK/FORT/DEF while CRIT/CRITDMG were deliberately excluded from the first scalar lane.
Fortification was modeled as fully retained Stage49 reserve, making this an intentionally defense-favorable upper bound.

Legacy per-rank effect magnitudes were scaled together at `40 / 60 / 80 / 100%` only as a diagnostic.

Key finding:
- corrected no-shop Tank all-finals-missed burial = 34.700s;
- at 40% shop-effect magnitude, tested profiles still bury around 38.25–38.75s if every final is missed from the beginning;
- at 80–100%, collapse can move near the end of the 60s fixture and many late-start failure streaks survive 16 missed finals;
- legacy 80–100% magnitude is therefore high-risk as a first 50-Stage shop center.

Next common search range:

```text
30% / 40% / 50% of legacy per-rank magnitudes
working diagnostic center = 40%
```

This is not a production numerical freeze and final stat families need not share one scale.

---

# Exact next boundary

1. run fixed-rank Stage49 shop+combat across all five classes at 30/40/50%;
2. compare ATTACK_HEAVY / DEFENSE_HEAVY / BALANCED / ROLE_AWARE;
3. keep CRIT/CRITDMG in a separate policy-correct lane rather than assigning fake universal value;
4. measure wall reserve, backlog, kills, SIEGER shots, wall hits and failure budget;
5. then model Fortification purchase timing across multiple Stages rather than granting all repair at Stage49;
6. then recheck shop feedback on valid timing-event count / EXP / P4 skill reach;
7. keep final multiplayer normalization at P10 and final EXP convergence at P10R.

P6 remains blocked pending P5 closure.
No user decision is currently pending.
No production change is authorized.
