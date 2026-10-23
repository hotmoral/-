# Timing Defense — Session Handoff

Updated: 2026-10-24 KST

## 0. Recovery rule — mandatory
Always fetch the live remote first. Never reconstruct current state from chat, memory, copied SHA, or an old handoff paragraph. Live GitHub canonical state wins.

The user must not have to re-explain the factual project state, dependency ordering or reasoning method.

---

# 1. Mandatory read/check order
1. live `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_35.yaml`
5. `legacy-game-structure/138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`
6. `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
7. `legacy-game-structure/02_TIER_SYSTEM.md`
8. `legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`
9. `legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
10. `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
11. `legacy-game-structure/91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
12. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
13. `legacy-game-structure/135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
14. `legacy-game-structure/144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`
15. `legacy-game-structure/147_ENCOUNTER_COMPOSITION_CLASS_RESPONSE_MATRIX_V0_1.md`
16. `legacy-game-structure/148_ENCOUNTER_OPPORTUNITY_DISTRIBUTION_FRAMEWORK_PROPOSAL_V0_1.md`
17. `legacy-game-structure/149_P6_FORMAL_ENTRY_AND_FIRST_CAUSAL_SLICE_AUTHORIZATION_V0_1.md`
18. **latest:** `legacy-game-structure/150_P6_STAGE46_47_FIRST_CAUSAL_CONVERGENCE_RESULT_V0_1.md`
19. current production/harness heads
20. only then the exact source required for the user-approved next P6 unit

Do not rerun closed work merely because a new chat/session started.

---

# 2. Mandatory cognition sequence

```text
Tier / Stage purpose
-> monster availability / novelty
-> encounter family / composition / formation / chronology / geometry
-> class identity / skill state
-> run-state persistence
-> mastery / judgment model
-> shop/economy
-> attack count / EXP / skill-reach feedback
-> target order / objective pressure
-> STAGE_SETTLED / wall carry
-> later-stage consequences
-> Tier unlock / meta / multiplayer impact
```

Root-cause order:

```text
source/simulator fidelity
-> lifecycle/state
-> encounter composition/geometry/chronology
-> class/package semantics
-> shop/feedback
-> exact scalar last
```

Use the smallest bounded probe that distinguishes the cause. Deep review does not mean repeating closed work.

---

# 3. Approval rule
Important design/content/numerical/work-boundary decisions must not be silently applied.

Approval is required before:
- choosing the next P6 repair/convergence axis after S1;
- changing exact Stage46/47 pressure;
- class buff/nerf;
- P×P/judgment probability change;
- shop numerical freeze;
- EXP rule change;
- selecting/adopting Tier count or monster availability/unlock ladder;
- exact Tier1 roster / Stage1-50 authoring;
- armored/hardened/new-monster adoption;
- Stage48/49 packet adoption;
- production gameplay change.

Diagnostic/instrumentation/fidelity work may proceed independently if gameplay semantics are unchanged.

---

# 4. Branch checkpoints

Planning/canonical:
- `timing-defense-workspace`
- always re-fetch live HEAD

Production:
- `timing-defense-cloudflare-do-poc`
- last verified `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`

P6-S1 temp branch:
- `timing-defense-workspace-temp-p6-stage46-47-causal`
- execution HEAD `8cfcd43ad8e7565d359903d76fea629e9ab1959f`
- no planning/production authority
- do not promote temp runner/workflows automatically

Other recent temp branches remain historical diagnostic evidence only.

---

# 5. Current exact phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 shop = USER APPROVED
P5 class identity group = DIRECTIONALLY CLOSED
P5 mastery reinterpretation = COMPLETE
P5->P6 fidelity bridge = EXACT TEMP PASS
entry charge/combo primary-cause checks = CLOSED
Stage46/47 armored count/chronology/band diagnostics = COMPLETE / NO ADOPTION
encounter-composition response matrix = COMPLETE
armored exact-coordinate microtuning = STOPPED
Stage48 local tuning = PAUSED
P6 = FORMALLY ENTERED / USER APPROVED
P6-S1 = COMPLETE / CAUSAL CLASSIFICATION / USER DECISION GATE
Tier count / exact monster unlock ladder / exact T1 roster = DEFERRED UNTIL P6 CONVERGENCE
Tier1 Stage1-50 authoring = NOT STARTED
production = UNCHANGED / UNAUTHORIZED
```

---

# 6. User-approved campaign/P6 ordering
The user explicitly chose:

```text
P6 convergence first
-> then use P6 evidence to constrain Tier structure / monster unlock order
-> then author actual Tier1 Stage1-50 according to Tier availability rules
```

Do not return to exact Tier/unlock authoring before this P6 boundary is resolved unless the user changes direction.

Stable campaign philosophy remains:
- T1 starts with a limited monster subset;
- higher Tiers add new roles;
- returning monsters gain new composition/formation/cadence meanings;
- current nine ordinary monsters + temporary armored proxy are diagnostic vocabulary, not final T1 roster.

---

# 7. User difficulty interpretation — preserve
The user considers the current central-skilled late-segment completion around the mid-40% range plausibly appropriate because all-PERFECT retains a 100% path in the tested controls.

Therefore:
```text
DO NOT default to raising global skilled completion.
DO NOT infer class scalar imbalance from one specialty-biased encounter family.
```

No exact percentage is frozen.

---

# 8. Closed prerequisite findings

## P5->P6 fidelity bridge
Run `39971985538`, exact repeat PASS.
- all-PERFECT `20/20` through Stage49;
- charge0/1/2/3 skilled through49 `48/45/42/44` of 100;
- Stage46 failures `23/100` for every entry charge;
- across charge states Mage `72/80`, Archer `61/80`, Rogue `25/80`, Knight `20/80`, Tank `1/80`.

Entry-combo `39972649909`:
- combo0 `48/100`;
- combo40 `48/100`.

Therefore:
```text
STAGE46_ENTRY_CHARGE_PHASE != PRIMARY_FAILURE_CAUSE
STAGE46_ENTRY_COMBO_BOUNDARY != PRIMARY_FAILURE_CAUSE
PERSISTENT_COMBO_CHARGE_REPAIR != RESOLUTION
```

## Encounter composition
Doc147 established:
```text
ENCOUNTER_COMPOSITION_ADVANTAGE = MATERIAL_CONFIRMED_CAUSE
CURRENT_STAGE46_47_CLASS_SPREAD != PROOF_OF_INTRINSIC_CLASS_NUMERIC_IMBALANCE
```

Mage density and Archer line specializations are strongly expressed by current late pressure; Knight/Rogue/Tank need other pressure families to express their own advantages.

Sparse armored count/chronology/band diagnostics are closed; no more exact-coordinate microtuning until real authoring.

---

# 9. P6 formal entry
Doc149 records user approval.

First slice fixed:
- SKILLED_V2_CENTRAL;
- persistent combo/charge/judgment state;
- Heavy X/Y;
- P×P-only Lv31 final;
- STAGE_SETTLED;
- wall carry;
- current class semantics;
- normal right-edge entry;
- paired deterministic seeds;
- no gameplay-semantic mutation.

---

# 10. P6-S1 exact execution

Run:
```text
39983816058
```
Result SHA256:
```text
9564363cee66e4f6a3fc2ea42329cd7f47c08050e2ae09366c48b3f616054cce
```
Exact-byte repeat:
```text
PASS
```

Volume:
```text
20 skilled seeds × 5 classes × 4 shop profiles = 400 skilled chains
20 all-PERFECT controls
Stage46->47
```

Profiles:
- BALANCED
- ATTACK_HEAVY
- DEFENSE_HEAVY
- ROLE_AWARE

These are fixed late-segment snapshots, not real purchase histories.

---

# 11. P6-S1 shop result

Stage47 skilled completion:

```text
BALANCED      A19 M19 R9 K7 T2 = 56/100
ATTACK_HEAVY  A19 M19 R9 K7 T2 = 56/100
DEFENSE_HEAVY A18 M17 R9 K7 T2 = 53/100
ROLE_AWARE    A19 M20 R9 K7 T2 = 57/100
```

Across profiles:
```text
Archer 75/80
Mage   75/80
Rogue  36/80
Knight 28/80
Tank    8/80
```

Conclusion:
```text
FIXED_LATE_SHOP_PROFILE != PRIMARY_CURRENT_CLASS_SPLIT_CAUSE
```

Do not generalize this to actual purchase-history feedback.

---

# 12. P×P-conditioned result

BALANCED descriptive bins:

```text
HIGH >0.65:
A 5/5, M 5/5, R 6/7, K 5/6, T 2/6

MID >0.40 <=0.65:
A 7/7, M 9/9, R 3/7, K 2/7, T 0/4

LOW <=0.40:
A 7/8, M 5/6, R 0/6, K 0/7, T 0/10
```

Aggregate:
```text
HIGH 23/29
MID  21/34
LOW  12/37
```

Refined causal interpretation:
```text
PXP exposure = strong overall mastery/difficulty sensitivity
PXP alone = insufficient to explain class split
class split = PXP/mastery × class package × encounter composition/geometry
```

Do not change P×P probability to fit current content.

---

# 13. Stage46 causal telemetry
BALANCED skilled means:

```text
Mage   damage~49982 maxActive~14.95 wallLoss~115  push~0.021
Archer damage~49289 maxActive~17.00 wallLoss~565  push~0.026
Rogue  damage~46315 maxActive~18.15 wallLoss~909  push=0
Knight damage~44678 maxActive~18.20 wallLoss~948  push~0.529
Tank   damage~28514 maxActive~26.20 wallLoss~1676 push~6.641
```

Stage46 failures:
```text
Archer 0
Mage   0
Rogue  5
Knight 5
Tank  13
```

Interpretation:
- current Stage46 is removal-heavy and density/line-friendly;
- raw total damage alone does not explain wall reserve;
- Tank has very large displacement, so control is present;
- in this packet, control does not substitute for removal quickly enough to prevent backlog/wall loss.

This is not universal Tank balance authority.

---

# 14. Timing-event / EXP feedback
BALANCED mean judgments consumed in attempted Stage46–47:

```text
Archer ~152.65
Mage   ~149.95
Rogue  ~123.15
Knight ~121.05
Tank    ~77.05
```

This demonstrates outcome-dependent timing-event opportunity divergence.
It does not directly calibrate Lv6–31 because Stage46–47 assumes Lv31 already and early failure truncates events.

A progression-relevant P6 slice is still needed before exact EXP/Tier-unlock authoring.

---

# 15. Current decision gate

## A — recommended first
**P6 paired pressure-family convergence.**
Keep run-power/mastery/shop semantics fixed and compare a small paired set:
- dense/aligned/high-volume;
- durable/distributed;
- control/objective-value pressure.

Goal:
- verify class advantage rotates with encounter family;
- distinguish legitimate specialty from intrinsic power defect;
- generate reusable evidence for future Tier opportunity distribution.

No exact Tier1 content authored.

## B — required after/alongside A
**P6 shop/EXP feedback** in a progression-relevant earlier window or synthetic run.
Measure actual timing-event count, EXP, milestone reach and shop feedback.

## C — not recommended yet
Numerically tune current Stage46/47 values to narrow the class spread.
This risks fitting a specialty-biased diagnostic packet and erasing class identity.

Recommended sequence:
```text
A -> B -> Tier/unlock candidate -> exact T1 Stage1-50
```

No post-S1 option adopted until user approval.

---

# 16. Session-close quality gate
Before handoff:
1. re-fetch live canonical HEAD;
2. verify production/harness unchanged unless explicitly authorized;
3. separate evidence from adopted semantics/values;
4. sync status/next/handoff/active dependency plan when boundary changes;
5. do not repeat closed P6-S1 without source/simulator trigger;
6. explain simply before technical detail;
7. stop at the current user decision gate.
