# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory or copied SHAs alone.
Always fetch live remote first.

Read/check in this order:
1. live branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_18.yaml`
6. `legacy-game-structure/112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
7. `legacy-game-structure/113_P5_RUN_COIN_SHOP_STRUCTURAL_PROPOSAL_V0_1.md`
8. `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
9. `legacy-game-structure/110_P4D2_PROVISIONAL_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`
10. `legacy-game-structure/109_P4D2_EXACT_V05_AND_STAGE49_V02_REPLAY_ADMISSION_V0_1.md`
11. `legacy-game-structure/data/p4d2_v05_and_stage49_v02_exact_replay_admission_v0_1.json`
12. `legacy-game-structure/108_P4D2_STAGE46_LV31_ACQUISITION_FAIRNESS_PRECHECK_V0_1.md`
13. `legacy-game-structure/107_P4D2_ARCHER_SPLITTER_CHRONOLOGY_ROOT_CAUSE_V0_1.md`
14. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
15. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
16. `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
17. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
18. `legacy-game-structure/05_LEGACY_EVIDENCE_MAP.md`
19. production shop source lineage: `timing-defense-cloudflare-poc/src/v035-entry.js`, `v037-entry.js`, current `v045-sieger-entry.js`
20. current production/harness heads
21. older P4 evidence only if a concrete P5 feedback trigger requires it

Do not rerun closed P1/P2/P3/P4 solely because a new session starts.
Live remote always wins.

---

# Branch checkpoints

Planning:
- `timing-defense-workspace`
- exact HEAD must be fetched live after sync.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- current work did not change it.

---

# Current exact phase / boundary

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P4-E = COMPLETE
P5 authority recovery = COMPLETE
P5 structural proposal = READY
P5 = USER_DECISION_PENDING_STRUCTURAL_PACKAGE
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
```

Current decision:

```text
A — recommended Package A
B — legacy killer-only baseline
C — checkpoint-only cadence + recommended economy/HP semantics
D — request alternative
```

---

# P4 facts that remain authoritative

- strong class-defining Lv31 finals; bounded/deterministic effect graphs.
- Archer wider real gameplay corridor USER APPROVED.
- Stage46+ real combat mastery-gate direction supported.
- exact v0.5 fidelity runner admitted.
- exact Stage49 complementary rotation admitted.
- durable high-HP/high-armor pressure supported diagnostically; not a new monster.
- Archer SPLITTER chronology root cause explained; authoring watch only.
- Stage46 97/98/99 Lv31 possession remains sensitivity only; final EXP P10R mandatory.
- BaseHP persists across Stages; no automatic Stage heal.

Exact replay identities:

```text
v0.5 runner blob 8a548184272a71f3b17650f77e6d366533409e0c
v0.5 output SHA256 29c5c7dc5a6c74f1e67f07d7eb0d8a3235e860817d7559227da26da192e2dae1
Stage49 v0.2 runner blob 1eb644766133d0a4e84130ab4d7be4c727cbee12
Stage49 output SHA256 c033d7fea455476ae2c4b9c0ffe4f770885d135533fd899a04709eb7cd0d6e02
```

---

# P5 authority recovery facts

Legacy/prototype implementation repeatedly used:

```text
categories:
atk / crit / critdmg / hp / def / knock

personal human coin/ranks
finite ranks
rising costs
Stage-clear shop
all-human ready
```

Current/inherited semantics include:
- killing human only receives monster reward coin;
- every human receives Stage-clear reward;
- HP buy adds shared max HP and current HP together;
- all human DEF ranks sum into shared generic wall DR;
- v0.45 SIEGER wall shot still reads the shared summed DEF ranks.

These are implementation references, not final production authority.

Legacy evidence explicitly says whether the 50-Stage production run should shop after every Stage is OPEN_DECISION.

---

# Recommended Package A

```text
EVERY_STAGE_AVAILABLE_BUT_FAST_CONTINUE
+
TEAM_DEATH_CREDIT_TO_EACH_ACTIVE_HUMAN_PERSONAL_WALLET
+
ALL-HUMAN_STAGE_CLEAR_BONUS_CANDIDATE
+
FORTIFICATION_MAX_PLUS_MATCHED_CURRENT_REPAIR
```

Ownership:

```text
ATK / CRIT / CRITDMG / KNOCK = personal run modifiers
FORTIFICATION / DEF = personal purchase contribution to shared wall
AI = no P5 shop wallet/purchases
```

Why:
- eliminates last-hit economic snowball/kill-steal incentive;
- preserves Tank/control economic viability;
- keeps continuous every-Stage run-growth loop without forcing a purchase;
- gives HP investment immediate value in a persistent no-auto-heal run without full refill;
- keeps six-category prototype grammar and P2 stat families coherent.

No values frozen.

---

# If user approves A

Immediately:
1. write approved P5 structural contract;
2. advance dependency plan to P5 simulation-active;
3. update PROJECT_STATUS / NEXT_WORK / SESSION_HANDOFF;
4. create deterministic P5 economy/shop fixture using legacy values only as sensitivity seeds;
5. implement simulation agents:
   - ATTACK_HEAVY
   - CRIT_HEAVY
   - DEFENSE_HEAVY
   - BALANCED
   - SAVE_DELAY
   - ROLE_AWARE
6. measure shop leverage, wall reserve, clear/fail, coin spend, class divergence and P4 skill-reach shift;
7. specifically watch:
   - SHOP_SNOWBALL
   - SHOP_TRIVIAL_DOMINANT_STRATEGY
   - FORTIFICATION_ATTRITION_ERASURE
   - DEFENSE_SHARED_SCALING_RUNAWAY
   - COIN_INCOME_CLASS_DIVERGENCE
   - SHOP_SKILL_REACH_DISTORTION
8. do not modify production.

If user chooses B/C/D, canonicalize that decision first and then continue within that boundary.

---

# Do not yet

- tune/freeze coin values or prices;
- freeze rank cap/effect values;
- freeze generic wall DR cap;
- freeze shop UI timer/host-next behavior;
- freeze final EXP;
- solve P10 player-count scaling early;
- change/deploy production gameplay;
- reopen P4 without a concrete P5 feedback trigger.
