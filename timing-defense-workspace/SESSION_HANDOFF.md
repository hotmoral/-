# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory or copied SHAs alone. Always fetch live remote first.

Read/check in this order:
1. live branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_22.yaml`
6. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
7. `legacy-game-structure/117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
8. `legacy-game-structure/118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
9. `legacy-game-structure/119_P5_CLEAR_KILL_INCOME_MIX_SENSITIVITY_V0_1.md`
10. `legacy-game-structure/120_P5_FORTIFICATION_DEFENSE_LEVERAGE_UPPER_BOUND_V0_1.md`
11. `legacy-game-structure/121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md`
12. `legacy-game-structure/122_P5_TANK_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
13. `legacy-game-structure/data/p5_shop_economy_spend_capacity_fixture_v0_1.json`
14. `legacy-game-structure/data/p5_tank_fixed_rank_shop_stage49_fixture_v0_1.json`
15. `tools/run_p5_shop_economy_spend_capacity_probe_v0_1.py`
16. `tools/run_p5_tank_fixed_rank_shop_stage49_probe_v0_1.py`
17. `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
18. `tools/run_p4d2_stage49_full_rotation_probe_v0_3.py`
19. `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
20. prior P4 exact admission docs109–110 when exact replay provenance is needed
21. current production/harness heads

Historical notes:
- doc113 is superseded where conflicting with docs115/116;
- doc114's earlier `16350` cost figure used banker-rounding and is superseded by exact positive-JS-rounding `16360`;
- v0.5 / Stage49 v0.2 remain historical exact replay evidence, but Tank SIEGER-specific numerics are superseded directionally by doc121 until v0.6/v0.3 exact replay is admitted.

Do not rerun closed P1/P2/P3/P4 wholesale solely because a new session starts.

---

# Branch checkpoints

Planning:
- `timing-defense-workspace`
- fetch exact live HEAD after recovery.

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
P4 Tank Iron Wall/SIEGER targeted correction = DIRECTIONAL PASS / EXACT V0.6/V0.3 PENDING
P5 A2 structural contract = USER_APPROVED
P5 economy-only preflight = DIRECTIONAL PASS
P5 clear/kill source mix = 70/30 WORKING CENTER SUPPORTED / NOT FROZEN
P5 Tank fixed-rank combat = DIRECTIONAL PASS_WITH_MAGNITUDE_WARNING
P5 = ACTIVE / FIVE-CLASS FIXED-RANK SHOP+COMBAT NEXT
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
```

No user decision is currently pending.

---

# A2 approved truth

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

No exact numerical value is frozen.

---

# Economy working centers — NOT FROZEN

Correct full-shop Rank10 legacy sensitivity cost:

```text
16360 nominal units
```

Spend capacity:

```text
45% = 7362
50% = 8180 <- working center
55% = 8998
```

Income source:

```text
80/20 clear/kill
70/30 <- working center
60/40
```

CENTER50 + 70/30 keeps moderate ±20% relative kill-share wallet variation around ~47%..53% full-shop capacity.

---

# Tank fidelity correction

Recovered Tank Lv11 Iron Wall is shared-wall incoming x0.90 and has no SIEGER exception.

Corrected no-shop Stage49 Tank diagnostic:

```text
all success wall2000
one miss wall2000
two-miss minimum1732.5
all-finals-missed burial34.700s
first burial: LINE6 / CLUSTER6 / FRONTLINE5 / DURABLE5 / TIME_BUDGET5
```

This preserves P4 structural closure.
Committed v0.6 / Stage49 v0.3 exact replay is still pending.

---

# Tank shop combat result

CENTER50 fixed Stage49 profiles were tested with ATK/KNOCK/FORT/DEF while CRIT/CRITDMG were intentionally omitted.
Fortification was fully retained as starting Stage49 reserve, so this is defense-favorable.

Legacy-relative common effect scale screen:

```text
40% / 60% / 80% / 100%
```

All-finals-missed burial across tested profiles:

```text
40% roughly 38.25..38.75s
60% roughly 38.25..39.43s
80% roughly 41.63..51.15s
100% roughly 46.23..58.33s
```

At 80–100%, many late-start failure streaks survive 16 missed finals in the bounded 60s fixture.
Therefore legacy full magnitude is not a safe first 50-Stage shop center.

Next five-class common-scale search:

```text
30% / 40% / 50%
working diagnostic center = 40%
```

This does not mean final ATK/KNOCK/FORT/DEF must share one scale.

---

# Exact next boundary

1. fixed-rank Stage49 shop+combat across all five classes at 30/40/50%;
2. policies ATTACK_HEAVY / DEFENSE_HEAVY / BALANCED / ROLE_AWARE;
3. ATK/KNOCK/FORT/DEF first scalar lane;
4. CRIT/CRITDMG separate policy-correct lane later;
5. evaluate wall reserve, max wall, burial, kills, active backlog, wall hits, SIEGER shots and class mistake budgets;
6. then implement purchase-time Fortification history across Stages;
7. then feed shop power back into timing-event count / EXP / Lv milestone reach;
8. final multiplayer normalization remains P10; final EXP convergence remains P10R.

Do not yet freeze:
- 50% spend capacity;
- 70/30 source mix;
- 40% common effect scale;
- coin/reward/price/rank/effect values;
- generic DR cap;
- final EXP;
- production implementation.
