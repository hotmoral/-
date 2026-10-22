# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes remain unauthorized during planning/calibration

---

# ACTIVE PHASE — P4 FULL PLAYER POWER SPINE / USER DECISION GATE

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
 -> P4 EXP dependency analysis + reproducible diagnostic
 -> P4 methodology proposal complete
```

Current authority/proposal:
- `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `legacy-game-structure/71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/77_P3_TEN_STAGE_PERSISTENT_RUN_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/78_P4_FULL_PLAYER_POWER_SPINE_EXP_MODEL_PROPOSAL_V0_1.md` — **PROPOSED / NOT YET APPROVED**
- `legacy-game-structure/data/p4_exp_preproposal_diagnostics_v0_1.json`
- `tools/analyze_p4_exp_baseline_from_p3.py`

---

# P3 CLOSED STRUCTURALLY

Final result:

```text
30 / 30 primary persistent runs PASS
8 / 8 targeted fixtures PASS
```

P3 proved lifecycle/pipeline integration only.
It did not freeze EXP, Base HP, shop, exact Stage authoring, clear-rate balance, permanent progression, boss or multiplayer values.

---

# P4 ANALYSIS RESULT

Current reach windows:

```text
Lv6   Stage 5–7   candidate
Lv11  Stage11–14  candidate
Lv16  Stage18–21  candidate
Lv21  Stage25–28  candidate
Lv26  Stage32–36  candidate
Lv31  Stage41–45  USER-CONFIRMED
```

Reproducible preproposal diagnostic shows the old 10-Stage prototype absolute EXP curve is far too fast under current P3 conditions:

```text
old thresholds applied to P3 first-10:
Lv6   P50 Stage2
Lv11  P50 Stage6
Lv16  P50 Stage10
```

The old absolute scale is therefore rejected as current P4 authority.

The same diagnostic also confirms material self-feedback from offensive skill power:

```text
forced Lv6 event-opportunity delta in P3 first-10
Knight  ~ -0.2%
Rogue   ~ -20.2%
Tank      0.0%
Archer  ~ -18.9%
Mage    ~ -14.7%
```

This feedback must be measured before any catch-up/compensation rule is proposed.

---

# P4 PROPOSAL — AWAITING USER APPROVAL

Proposal:
`legacy-game-structure/78_P4_FULL_PLAYER_POWER_SPINE_EXP_MODEL_PROPOSAL_V0_1.md`

Recommended package:
1. valid completed local timing-turn EXP only; no kill/damage/passive/flat Stage-clear EXP and no hidden class compensation in the baseline;
2. one EXP grant per completed turn; Heavy X+Y gets one combined quality reward;
3. calibrate in dimensionless `XP_CREDIT`; legacy relative quality shape is primary candidate, absolute old EXP values discarded;
4. six cumulative milestone anchors (`A6/A11/A16/A21/A26/A31`) + transparent monotonic interpolation instead of old closed-form `levelNeed()`;
5. T1–T4 multi-schedule synthetic 50-Stage corpus, initially three legal timing-opportunity envelopes per Tier; no exact launch Stage authoring;
6. marker-only inverse-design first, then Lv6 authoritative + Lv11/16/21 exact legacy-parity mechanics as simulation-only feedback candidates; Lv26/Lv31 stay behind separate P4 decision gates;
7. fit first against P50 milestone windows while always recording P25/P50/P75/P90; exact tail cutoffs follow first evidence; Lv31 Stage41–45 remains structurally fixed;
8. one universal EXP curve across classes/Tiers; kill-speed-driven opportunity reduction is measured self-damping unless evidence proves structural failure. Any stabilizer/catch-up requires a later user decision.

Implementation is blocked until this package is approved or modified.

---

# After approval — intended P4 work order

```text
P4-A  build legal T1–T4 synthetic 50-Stage opportunity corpus
      + XP_CREDIT model
      + six milestone-anchor inverse design

P4-B  integrate Lv6 + Lv11/16/21 simulation candidates
      -> measure kill-speed / event-opportunity feedback
      -> refit/check reach distributions

P4-C  Lv26 analysis -> user decision -> bounded simulation contract
      -> rerun late reach to Lv31

P4-D  Lv31 analysis -> user decision -> bounded simulation contract
      -> Stage46–49 mastery / power-slope evidence

P4-E  percentile/tail review -> final P4 candidate decision
```

Only after P4 candidate closure does P5 shop/economy open.

---

# Do not yet

- implement/freeze P4-A/B methodology before user approval
- modify/deploy production v0.45 gameplay
- reuse old `60+12*(level-1)` as current level authority
- freeze exact EXP grant numbers or milestone thresholds
- add kill/damage/Stage-clear/catch-up EXP without a later evidence-backed approval
- use class-specific hidden EXP multipliers
- promote Lv11–21 legacy candidates to production authority
- invent Lv26/Lv31 numeric proxies
- freeze exact shop cadence/price/value curve
- freeze exact Base HP
- freeze permanent star/achievement values
- author exact 200 launch Stages
- freeze exact boss mechanics
- freeze multiplayer progression/scaling values
