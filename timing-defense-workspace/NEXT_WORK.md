# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes unauthorized

## Mandatory authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active plan `legacy-game-structure/data/system_dependency_calibration_order_v0_20.yaml`
- A2 contract `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- spend envelope `legacy-game-structure/117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
- economy preflight `legacy-game-structure/118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
- fixture `legacy-game-structure/data/p5_shop_economy_spend_capacity_fixture_v0_1.json`
- runner `tools/run_p5_shop_economy_spend_capacity_probe_v0_1.py`

Live remote wins.

---

# ACTIVE PACKAGE — P5

**A2 STRUCTURAL APPROVED / ECONOMY PREFLIGHT ACTIVE**

No user decision is pending.

Approved semantics:

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
PERSONAL WALLETS
KILLER_ONLY PERSONAL ORDINARY-MONSTER COIN BASELINE
ALL-HUMAN STAGE-CLEAR FLOOR CANDIDATE
FORTIFICATION = MAX + MATCHED CURRENT REPAIR
PERSONAL OFFENSE/CONTROL
PERSONAL PURCHASES -> SHARED FORTIFICATION/DEF
SIX SHOP CATEGORIES
NO ROUTINE FULL-SHOP MAXOUT BY STAGE49
```

---

# Current working economy envelope

Correct legacy sensitivity reference uses JavaScript Math.round:

```text
full Rank10 six-track cost = 16,360 nominal units
```

Candidate Stage49 spend capacity:

```text
45% = 7,362
50% = 8,180 <- working center
55% = 8,998
```

Economy-only preflight:
- all-six maxout = false in every tested policy;
- CENTER balanced ends around Rank7–8;
- selected specialization can max one late track around Stage45–49;
- broad tradeoffs remain.

No values frozen.

---

# Exact next analysis

## A. Income-source mix
Test at fixed total capacity first:

```text
CLEAR/KILL = 80/20, 70/30, 60/40
working center candidate = 70/30
```

Apply kill-share perturbations:
- moderate ±20% relative to equal-share expectation;
- stress ±40% where useful;
- solo / 2P / 4P interpretation only as sensitivity until P10.

Reject if class/player kill-share produces persistent multi-rank divergence large enough to dominate purchase strategy.

## B. Fortification / DEF wall-pressure integration
Use representative persistent-wall pressure including late Stage49-like reserve concerns.

Measure:
- current/max wall HP trajectory;
- repair purchased vs damage taken;
- generic DEF prevented damage;
- Stage49->50 reserve;
- whether DEFENSE_HEAVY trivially dominates;
- whether Fortification erases attrition.

Do not fix this by hidden per-class prices.

## C. Purchase-policy combat feedback
Compare:
- ATTACK_HEAVY
- CRIT_HEAVY
- DEFENSE_HEAVY
- BALANCED
- SAVE_DELAY
- ROLE_AWARE

Then measure valid timing-action count, EXP opportunity, skill-reach drift and clear/fail behavior.

---

# Do not yet

- freeze exact coin values;
- freeze exact Stage-clear reward;
- freeze 70/30;
- freeze price/rank/effect values;
- freeze generic wall-DR cap;
- solve final multiplayer scaling before P10;
- freeze final EXP before P10R;
- modify/deploy production gameplay;
- reopen P4 without a concrete P5 feedback trigger.

P6 remains blocked pending P5 closure.
