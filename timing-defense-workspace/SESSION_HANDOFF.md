# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory or copied SHAs alone. Always fetch live remote first.

Read/check in this order:
1. live branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_20.yaml`
6. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
7. `legacy-game-structure/117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
8. `legacy-game-structure/118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
9. `legacy-game-structure/data/p5_shop_economy_spend_capacity_fixture_v0_1.json`
10. `tools/run_p5_shop_economy_spend_capacity_probe_v0_1.py`
11. `legacy-game-structure/115_P5_RUN_COIN_SHOP_REVISED_STRUCTURAL_PROPOSAL_V0_2.md`
12. `legacy-game-structure/114_P5_RUN_COIN_SHOP_QUANTITATIVE_PRECHECK_V0_1.md` — earlier 16350 rounding figure superseded by exact 16360 reference
13. `legacy-game-structure/112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
14. `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
15. `legacy-game-structure/110_P4D2_PROVISIONAL_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`
16. `legacy-game-structure/109_P4D2_EXACT_V05_AND_STAGE49_V02_REPLAY_ADMISSION_V0_1.md`
17. P4 older evidence only if a concrete P5 feedback trigger requires it
18. current production/harness heads

Historical P5 doc113 is design history and is superseded where it conflicts with docs115/116.
Do not rerun closed P1/P2/P3/P4 solely because a new session starts.

---

# Branch checkpoints

Planning:
- `timing-defense-workspace`
- fetch exact HEAD live after recovery.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- current P5 work did not change it.

---

# Current exact phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 authority recovery = COMPLETE
P5 A2 structural contract = USER_APPROVED
P5 spend-capacity envelope = CANDIDATE READY
P5 economy-only policy preflight = DIRECTIONAL PASS
P5 = ACTIVE / CLEAR-KILL MIX + WALL-PRESSURE INTEGRATION NEXT
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
```

No user decision is currently pending.

---

# P5 A2 approved truth

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
PERSONAL WALLETS
KILLER_ONLY PERSONAL ordinary-monster coin baseline
ALL-HUMAN Stage-clear income-floor candidate
FORTIFICATION = max HP + matched current repair
ATK/CRIT/CRITDMG/KNOCK personal
FORTIFICATION/DEF purchases contribute to shared wall
six categories retained
NO_ROUTINE_FULL_SHOP_MAXOUT_BY_STAGE49
```

Specialization may max/near-max selected tracks late if meaningful sacrifices remain elsewhere.
The contract does not yet require mathematical impossibility of all-max for every extreme outlier.

---

# Exact legacy cost-reference correction

Prototype cost code uses positive JavaScript `Math.round`.

```text
ATK 2725
CRIT 3000
CRITDMG 2725
FORT 2455
DEF 3000
KNOCK 2455
TOTAL 16360
```

Earlier 16350 text used banker-rounding on some `.5` values and is numerically superseded.

---

# Current economy working envelope

```text
45% = 7362 nominal units
50% = 8180 <- working center
55% = 8998
```

Economy-only result:
- no tested run maxed all six;
- 45% no tested strategy maxed even one track;
- 50% allows selected specialization to max a late track around Stage45–49;
- 50% balanced ends around Rank7–8;
- 55% remains far from whole-shop completion.

These are calibration ratios, not production values.

---

# Killer-only coin / income-mix next work

First source mix sensitivity:

```text
CLEAR/KILL
80/20
70/30 <- working center candidate
60/40
```

At total CENTER50, ±20% relative kill-share perturbation maps approximately to:

```text
80/20 -> 48%..52% total capacity
70/30 -> 47%..53%
60/40 -> 46%..54%
```

70/30 balanced rank-space remains broadly Rank7–8.
Use ±40% relative kill-share only as a stress lane.

No split is frozen.

---

# Exact next boundary

1. formalize/run clear-vs-kill income-mix sensitivity;
2. quantify rank divergence under moderate/stress kill-share perturbations;
3. integrate Fortification and generic DEF into persistent wall-pressure simulation;
4. reject attrition-erasing or trivial-defense curves;
5. run purchase-policy combat feedback;
6. recheck valid timing-event counts and P4 EXP/skill reach;
7. keep final 2/3/4P scaling at P10 and final EXP convergence at P10R.

Do not yet:
- freeze coin/reward/price/rank/effect values;
- freeze 70/30;
- freeze generic DR cap;
- modify production;
- reopen P4 without a concrete P5 feedback trigger.
