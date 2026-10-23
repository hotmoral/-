# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production checkpoint
- branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes remain unauthorized

## Operating authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active dependency plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_18.yaml`
- live remote always wins
- do not rerun closed PASS/APPROVED work without a concrete trigger

---

# Current phase

**P4 PROVISIONAL STRUCTURAL COMPLETE_WITH_WATCHES / P5 USER DECISION PENDING — RUN COIN / SHOP STRUCTURE**

Current chain:

```text
P0..P3 structural foundation complete
-> P4 player-power spine provisional structural complete with watches
-> P4-D2 exact v0.5 + Stage49 v0.2 replay admitted
-> P4-E complete; final EXP deferred to P10R
-> P5 shop/coin authority recovery COMPLETE
-> P5 structural proposal PACKAGE A RECOMMENDED
-> user decision pending before numerical shop simulation
```

Latest P5 authority:
- `legacy-game-structure/112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
- `legacy-game-structure/113_P5_RUN_COIN_SHOP_STRUCTURAL_PROPOSAL_V0_1.md`

P4 closure authority:
- `legacy-game-structure/109_P4D2_EXACT_V05_AND_STAGE49_V02_REPLAY_ADMISSION_V0_1.md`
- `legacy-game-structure/110_P4D2_PROVISIONAL_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`
- `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`

---

# P4 stable closure facts

- Lv31 identities remain strong/class-defining and finite/deterministic/attributable.
- Archer wider real gameplay corridor is USER APPROVED; no homing/bending/off-line retarget.
- Stage46+ real combat mastery-gate direction supported.
- Stage49 complementary rotation exact-admitted:
  - all-success wall: Knight1705 / Rogue2000 / Tank2000 / Archer2000 / Mage2000
  - all-finals-missed burial: Knight34.025 / Rogue29.100 / Tank34.575 / Archer57.025 / Mage52.225 seconds.
- Tank is a time-budget/control class; identical class mistake budgets are not required.
- durable high-HP/high-armor pressure axis is supported diagnostically but is not a new-monster approval.
- BRUTE carrying/using SHIELD-like protection remains parked for later monster design.
- Archer SPLITTER nonmonotonicity root cause is explained chronology, not a skill-width/power defect.
- BaseHP persists across stages; no automatic stage heal.

Exact replay authority:

```text
v0.5 runner blob
8a548184272a71f3b17650f77e6d366533409e0c
v0.5 output SHA-256
29c5c7dc5a6c74f1e67f07d7eb0d8a3235e860817d7559227da26da192e2dae1

Stage49 v0.2 runner blob
1eb644766133d0a4e84130ab4d7be4c727cbee12
Stage49 output SHA-256
c033d7fea455476ae2c4b9c0ffe4f770885d135533fd899a04709eb7cd0d6e02
```

EXP:
- pure per-valid-turn EXP remains diagnostic only;
- Stage46 97/98/99 possession checkpoints are sensitivity only;
- no hidden class/Tier XP patch;
- final EXP/timebase convergence mandatory at P10R.

---

# P5 authority recovery result

Stable upstream:
- run coin exists and is run-local;
- coin/shop ranks persist within the Tier attempt;
- coin/shop reset on a new attempt;
- six legacy categories map cleanly to P2 stat families:
  `ATK / CRIT / CRIT DMG / WALL HP / DEF / KNOCKBACK`;
- finite ranks + escalating costs are structurally appropriate;
- exact values/costs/rank cap remain open.

Legacy/current implementation evidence:
- shop-after-every-Stage implemented through Stage1-3 prototype chain;
- personal human wallets and independent purchases;
- monster kill coin currently goes only to the killing human;
- Stage-clear reward goes to each human;
- HP purchase increases shared max HP and current HP together;
- DEF ranks from all humans sum into shared generic wall DR;
- v0.45 SIEGER path still reads summed human DEF ranks.

These implementation details are references, not final production authority.

---

# P5 identified structural risks

## Killer-only coin
Can create:

```text
more last hits -> more coin -> more offense -> still more last hits
```

This conflicts with approved class asymmetry and can economically starve Tank/control contribution.

## WALL HP purchase
Legacy `max+current` is an explicit repair event, not merely max-HP growth. P1 allows explicit shop healing but did not previously approve its semantic.

## Shared DEF/HP
Structurally coherent for one shared wall, but player-count leverage must remain a P10 scaling watch; no multiplayer numerical freeze in P5.

## 50-Stage shop cadence
Legacy shop-after-every-Stage is proven only as implementation reference. The evidence map explicitly marks 50-Stage cadence as OPEN_DECISION.

---

# Recommended P5 Package A — USER DECISION PENDING

```text
1. EVERY_STAGE_AVAILABLE_BUT_FAST_CONTINUE
   - lightweight shop opportunity after every cleared Stage except Tier final
   - purchase optional; immediate READY/CONTINUE allowed

2. TEAM_DEATH_CREDIT / PERSONAL WALLETS
   - every authoritative enemy death credits each active human's personal run wallet
   - killer identity does not change coin income
   - AI kills also generate the human team death-credit event
   - all-human Stage-clear bonus retained as candidate source; values open

3. FORTIFICATION WALL HP
   - max HP increases by purchased amount
   - current HP receives the same realized increase, clamped to new max
   - not full heal and not automatic Stage healing

4. ownership
   - ATK/CRIT/CRITDMG/KNOCK = personal modifiers
   - FORTIFICATION/DEF = personal purchases contributing to the one shared wall
```

Alternatives:
- B: legacy killer-only baseline (not recommended)
- C: checkpoint-only shop while keeping recommended economy/HP semantics
- D: request another structural alternative.

Approval freezes semantics only. No coin amounts, prices, rank values/caps, DR cap, or exact UI timing.

---

# Current decision gate

**Awaiting user decision: A / B / C / D from document113.**

After approval:
- draft approved P5 structural contract;
- build bounded shop simulation fixture;
- compare ATTACK_HEAVY / CRIT_HEAVY / DEFENSE_HEAVY / BALANCED / SAVE_DELAY / ROLE_AWARE;
- measure SHOP_SNOWBALL, dominant strategy, Fortification attrition erasure, shared-defense runaway, class coin divergence and P4 skill-reach drift.

No production change is authorized.
