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
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_19.yaml`
6. `legacy-game-structure/112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
7. `legacy-game-structure/114_P5_RUN_COIN_SHOP_QUANTITATIVE_PRECHECK_V0_1.md`
8. `legacy-game-structure/115_P5_RUN_COIN_SHOP_REVISED_STRUCTURAL_PROPOSAL_V0_2.md`
9. `legacy-game-structure/113_P5_RUN_COIN_SHOP_STRUCTURAL_PROPOSAL_V0_1.md` — historical; superseded where conflicting
10. `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
11. `legacy-game-structure/110_P4D2_PROVISIONAL_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`
12. `legacy-game-structure/109_P4D2_EXACT_V05_AND_STAGE49_V02_REPLAY_ADMISSION_V0_1.md`
13. `legacy-game-structure/data/p4d2_v05_and_stage49_v02_exact_replay_admission_v0_1.json`
14. `legacy-game-structure/108_P4D2_STAGE46_LV31_ACQUISITION_FAIRNESS_PRECHECK_V0_1.md`
15. `legacy-game-structure/107_P4D2_ARCHER_SPLITTER_CHRONOLOGY_ROOT_CAUSE_V0_1.md`
16. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
17. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
18. `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
19. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
20. `legacy-game-structure/05_LEGACY_EVIDENCE_MAP.md`
21. production shop source lineage: `timing-defense-cloudflare-poc/src/v035-entry.js`, `v037-entry.js`, current `v045-sieger-entry.js`
22. current production/harness heads
23. older P4 evidence only if a concrete P5 feedback trigger requires it

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
P5 quantitative precheck = COMPLETE_DIRECTIONAL
P5 revised structural proposal A2 = READY
P5 = USER_DECISION_PENDING_REVISED_PACKAGE_A2
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
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

---

# P5 quantitative findings

Legacy/current shop evidence:

```text
categories: atk / crit / critdmg / hp / def / knock
personal human coin/ranks
finite ranks
rising costs
Stage-clear shop
all-human ready
killer-only monster coin
all-human Stage-clear reward
HP buy max+current
summed human DEF to shared wall
```

New quantitative interpretation:

```text
killer-only coin snowball = NOT DEMONSTRATED
EXP from kill credit = NO
actual kill-share divergence must be measured before replacing killer-only rule
```

Early 2P sensitivity:
- 55:45 last-hit share -> ~6% total coin gap
- 60:40 -> ~12.3%
- 70:30 -> ~26.2%

Primary economy problem under naive legacy extension:

```text
Stage1..49 common clear reward = 17,395
all six legacy Rank10 tracks total cost = 16,350
single track saturation ~= Stage16-18
HP+DEF saturation ~= Stage26
```

Therefore legacy reward/cost values must not be promoted to 50-Stage production.

---

# Revised recommended Package A2

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
+
KILLER_ONLY_PERSONAL_MONSTER_COIN_BASELINE
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

Important:
- doc115 supersedes doc113's default TEAM_DEATH_CREDIT recommendation;
- killer-only coin remains a baseline candidate, not frozen production truth;
- shop access may be every Stage, but must not become 49 long forced modal interruptions;
- Fortification semantic is recommended, legacy +100/rank is not;
- shared DEF/HP numerical player-count leverage stays open for P10.

No values frozen.

---

# If user approves A2

Immediately:
1. write approved P5 structural contract;
2. advance dependency plan to P5 simulation-active;
3. update PROJECT_STATUS / NEXT_WORK / SESSION_HANDOFF;
4. build deterministic 50-Stage spend-capacity/economy fixture;
5. implement simulation agents:
   - ATTACK_HEAVY
   - CRIT_HEAVY
   - DEFENSE_HEAVY
   - BALANCED
   - SAVE_DELAY
   - ROLE_AWARE
6. measure actual kill-share/coin/rank trajectories by class;
7. test category saturation, Fortification attrition erasure, shared DEF leverage and P4 skill-reach feedback;
8. do not modify production.

---

# Do not yet

- tune/freeze production coin values or prices;
- freeze rank cap/effect values;
- freeze generic wall DR cap;
- freeze shop UI timer/host-next behavior;
- freeze final EXP;
- solve P10 player-count scaling early;
- change/deploy production gameplay;
- reopen P4 without a concrete P5 feedback trigger.
