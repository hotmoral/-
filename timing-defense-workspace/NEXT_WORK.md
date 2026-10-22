# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes remain unauthorized during planning/calibration

---

# ACTIVE PHASE — P4 FULL PLAYER POWER SPINE CANDIDATE

Completed chain:

```text
Master Campaign Spine
 -> Layer-0 PASS
 -> encounter envelope PASS
 -> historical all-20 540/540
 -> provisional streak-aware SKILLED_V2_CENTRAL
 -> corrected central all-20 540/540
 -> P1 Run-State Lifecycle USER_APPROVED_STRUCTURAL_COMPLETE
 -> P2 Modifier Pipeline / Power Attribution USER_APPROVED_STRUCTURAL_COMPLETE
 -> P3 Ten-Stage Persistent Run Kernel P3_STRUCTURAL_PASS
```

Current authority:
- `legacy-game-structure/69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `legacy-game-structure/71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/77_P3_TEN_STAGE_PERSISTENT_RUN_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/system_dependency_calibration_order_v0_2.yaml`

---

# P3 CLOSED STRUCTURALLY

Final result:

```text
30 / 30 primary 10-Stage runs PASS
8 / 8 targeted fixtures PASS
```

Verified:
- deterministic replay;
- ten Stage settlements;
- continuous `SKILLED_V2_CENTRAL` state/RNG across the attempt;
- combo/charge/N3 Stage-boundary continuity;
- Base HP persistence and failure/retry reset;
- inter-Stage + mid-Stage snapshot/resume equivalence;
- P2 same-stat additive aggregation + source attribution;
- Stage-local TEMPORARY clearing;
- no stale StageState leakage;
- forced Lv6 transition plumbing across all five classes.

P3 did **not** freeze:
- EXP;
- actual Lv6 reach;
- Base HP balance;
- shop/economy;
- exact Stage1–10 authoring;
- difficulty/clear rate;
- permanent progression;
- boss/multiplayer values.

---

# EXACT NEXT BOUNDARY — P4

## P4 FULL_PLAYER_POWER_SPINE_CANDIDATE

Goal:
construct the first 50-Stage **synthetic** player-power spine and determine a provisional EXP/level model that can place skill milestones in acceptable Stage windows before real shop and permanent power are coupled in.

Current milestone targets:

```text
Lv6   Stage 5–7   calibration candidate
Lv11  Stage11–14  calibration candidate
Lv16  Stage18–21  calibration candidate
Lv21  Stage25–28  calibration candidate
Lv26  Stage32–36  calibration candidate
Lv31  Stage41–45  USER-CONFIRMED DIRECTION
```

Required P4 outputs:
1. synthetic 50-Stage event/opportunity spine;
2. provisional EXP earning model candidates;
3. provisional level-threshold curve candidates;
4. Lv6/11/16/21/26/31 reach distributions P25/P50/P75/P90;
5. post-unlock remaining Stage count and meaningful combat-event count;
6. pre/post unlock power slope by class;
7. attribution checks for encounter-pressure vs skill-power changes;
8. identification of compressed/late/early skill windows;
9. explicit P4 recommendation packet before any numerical closure.

---

# P4 first-pass constraints

Use:
- SOLO;
- shop `OFF/NEUTRAL`;
- P0/fresh permanent-power baseline;
- current provisional `SKILLED_V2_CENTRAL` as the central design-prior lane;
- current Model A 50-Stage macro/authoring windows;
- synthetic/representative encounter data, not exact launch authoring.

Do not yet add:
- tuned shop power;
- star/achievement stat power;
- boss-specific economy/novelty;
- multiplayer progression;
- exact 200 launch Stages.

---

# P4 material decisions that must not be silently closed

Before P4 numerical authority, analyze and present recommendations for at least:
- EXP source semantics within the current valid timing-event model;
- whether EXP is purely judgment/event based or has any additional source;
- exact/provisional level-threshold curve family;
- percentile acceptance criteria around each milestone window;
- how to represent Lv11/16/21/26/31 mechanics that are not equally authoritative today;
- whether class-specific EXP differences are permitted or prohibited;
- how overkill/faster-kill reduction of EXP opportunities is handled as a feedback invariant.

These require the user decision process:

```text
live canonical inspection
 -> dependency analysis
 -> calculation/simulation
 -> real alternatives
 -> recommendation + risks/reversibility
 -> USER DECISION
 -> then author/validate
```

---

# Do not yet

- modify/deploy production v0.45 gameplay
- freeze exact EXP formula without the P4 decision packet
- treat forced P3 Lv6 Stage6 as an actual reach result
- freeze exact shop cadence/price/value curve
- freeze exact Base HP
- freeze permanent star values
- freeze achievement reward graph/value
- author exact 200 launch Stages
- freeze exact boss mechanics
- freeze multiplayer scaling/progression credit
- silently resolve unresolved Lv26/Lv31 or multihit crit semantics
