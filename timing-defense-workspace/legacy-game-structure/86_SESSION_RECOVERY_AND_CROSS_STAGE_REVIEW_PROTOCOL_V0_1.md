# Timing Defense — Session Recovery & Cross-Stage Review Protocol V0.1

Date: 2026-10-23 KST  
Status: **ACTIVE OPERATING PROTOCOL / USER-DIRECTED GOVERNANCE**

## 0. Purpose

This protocol prevents a new session from reconstructing the project from chat memory, one handoff note, or one stale legacy document.

The project is highly coupled. Before each material step, the assistant must verify consistency against upstream contracts, downstream dependencies, current authority, and production boundaries. The goal is to catch cheap structural defects early without re-running already-closed work unnecessarily.

This protocol governs **how to read, recover, review, and hand off** the project. It does not itself authorize gameplay, numerical, balance, or production changes.

---

# 1. Core operating principles

1. **Live remote wins.**
   - Always re-fetch the live `timing-defense-workspace` branch HEAD first.
   - Chat, memory, copied SHA values, and handoff prose are orientation aids only.

2. **Authority before detail.**
   - Determine which document/version currently supersedes older plans before using any historical `NEXT`, `ACTIVE`, or recommendation statement.
   - A passed simulation does not automatically promote a candidate to user-approved or frozen authority.

3. **Progressive deepening, not full re-audit every step.**
   - Recover the whole dependency spine once per new session.
   - For each work package, re-read only the upstream/downstream slices materially affected by that package.
   - Do not repeat closed validation unless there is a concrete trigger.

4. **Cross-stage consistency review is mandatory.**
   Before closing any material step, explicitly check:
   - upstream invariants;
   - current-phase contract;
   - downstream consumers;
   - cross-system feedback loops;
   - authority/supersession;
   - production boundary;
   - handoff impact.

5. **Diagnose before patching.**
   - Do not repair an EXP defect by changing monster HP without causal evidence.
   - Do not repair wall pressure by inflating Base HP automatically.
   - Do not repair progression deadlock by weakening Tier unlock rules automatically.
   - First classify the failing layer.

6. **User approval remains required for material design decisions.**
   Follow `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`.

---

# 2. Mandatory new-session recovery order

A new session must recover state in the following order.

## Phase A — live canonical state

1. Live branch HEAD: `timing-defense-workspace`
2. `../PROJECT_STATUS.md`
3. `../NEXT_WORK.md`
4. `../SESSION_HANDOFF.md`
5. this protocol: `86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
6. active machine-readable dependency plan: `data/system_dependency_calibration_order_v0_6.yaml`
7. latest user-approved routing/decision contract for the current gate

At the current boundary, that latest routing contract is:
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`

If a newer numbered contract or dependency-plan version exists on live remote, the newer live authority must be inspected before continuing.

## Phase B — structural spine

Read enough of the structural corpus to recover the game, not merely the current micro-task:

1. `README.md` — corpus map/history only; do **not** assume its old `NEXT` or old dependency-version references are current authority.
2. `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
3. `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
4. `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
5. `01_META_PROGRESSION.md`
6. `02_TIER_SYSTEM.md`
7. `03_STAGE_STRUCTURE_50.md`
8. `04_MONSTER_ENCOUNTER_MODEL.md`
9. `05_LEGACY_EVIDENCE_MAP.md`
10. `07_AUTHORING_DATA_SCHEMA.md`
11. `15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`

Purpose: restore the common coordinate system:

```text
Tier × Stage1..50 × Content Novelty × Run Player Power × Meta Progression
```

## Phase C — closed dependency foundations

Read the latest approved contracts that the active phase consumes.

Current minimum foundation set:
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `77_P3_TEN_STAGE_PERSISTENT_RUN_EXECUTION_REPORT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`

Do not re-run P1/P2/P3 simply because a new chat started. Revalidate only if a relevant contract/source changed or new evidence exposes a mismatch.

## Phase D — active-phase evidence pack

Read the documents directly feeding the exact current gate.

At the current boundary `P4-C1 — LV26 STRUCTURAL SKILL-CONTRACT DECISION`, minimum pack:
- `../PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`
- `20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
- `66_SKILLED_V2_CENTRAL_DESIGN_PRIOR_AND_HARNESS_CLOSURE_AMENDMENT_V0_1.md`
- `67_SKILLED_V2_CENTRAL_SEQUENCE_MODEL_V0_1.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `80_P4A_MARKER_ONLY_INVERSE_DESIGN_EXECUTION_REPORT_V0_1.md`
- `81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `83_P4B_MULTIPLAYER_TIMEBASE_PRECHECK_V0_1.md`
- `84_P4B_EXP_DECISION_REASSESSMENT_PROPOSAL_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`

Then recover the exact live/legacy source evidence required for each Lv26 skill. Historical descriptions alone are not authority.

## Phase E — production and harness truth

Verify current branch heads for:
- production gameplay branch;
- calibration harness branch;
- any source branch used as direct authority for the active decision.

Confirm whether relevant source changed since the last accepted report. If not, do not invent a need to re-run already-passed production/harness checks.

---

# 3. Supersession rule

When documents disagree, classify the disagreement before calling it a contradiction.

Preferred interpretation order:

1. live current status / latest approved routing contract;
2. latest machine-readable dependency plan;
3. user-approved structural contracts;
4. current bounded simulation authority;
5. current authoritative production source for runtime truth;
6. legacy implemented reference;
7. legacy analysis/candidate;
8. superseded/parked material.

Examples:
- `data/system_dependency_calibration_order_v0_6.yaml` supersedes older v0.1 execution-order references.
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md` supersedes the recommendation state in `82_P4B_EXP_STABILIZATION_DECISION_PROPOSAL_V0_1.md`.
- old README `NEXT` text is historical orientation if it conflicts with `PROJECT_STATUS/NEXT_WORK/SESSION_HANDOFF`.

Never promote an older concrete number simply because it is more detailed than a newer open decision.

---

# 4. Mandatory review lenses for every material step

Before executing or closing a material package, review it through these lenses.

## 4.1 Authority / provenance
- Is this observed, derived, candidate, proposed, user-approved, frozen, or production-authorized?
- Which document/source gives that status?
- Has a later document superseded it?

## 4.2 Upstream consistency
- Does the change preserve P1 lifecycle semantics?
- Does it preserve P2 modifier/effect semantics?
- Does it preserve current combat/targeting/role contracts?
- Does it preserve campaign/star/Tier invariants?

## 4.3 Downstream dependency
- Which later packages consume this result?
- Could a premature decision force rework in P5/P6/P7/P8/P10/P10R/P11+?
- Should a value remain parameterized instead of frozen now?

## 4.4 Cross-system feedback
Check the relevant loops, including:

```text
encounter pressure ↔ attack count ↔ EXP ↔ skill reach ↔ combat power
shop power ↔ kill speed ↔ EXP opportunity
permanent power ↔ kill speed ↔ EXP opportunity
stars ↔ difficulty ↔ future stars
achievements ↔ class soft-wall recovery
multiplayer composition/player count ↔ combat time ↔ XP opportunity ↔ progression rate
```

## 4.5 Player-experience / content identity
- Does the change preserve Tier identity rather than homogenizing encounters for a metric?
- Does a skill erase monster role expression before readable counterplay?
- Does novelty collide with first-teach or major power transition?
- Does ordinary difficulty remain compatible with the intended late soft-wall loop?

## 4.6 Class asymmetry / fairness
- Different class outcomes are allowed.
- Hard class lockout is not.
- Shared Stage data must remain viable across all five classes.
- Do not use hidden class XP correction unless separately approved.

## 4.7 Determinism / attribution
- Can the result be reproduced with versioned inputs and seeds?
- Can power/effect contributions be attributed to the correct source?
- Are we accidentally hiding one system's defect with another system's scalar?

## 4.8 Scope / cost
- Is this work necessary for the current gate?
- Can a smaller bounded test answer the question?
- Are we accidentally authoring exact launch content or freezing downstream numbers early?

## 4.9 Production boundary
- Is production gameplay/numerical change explicitly authorized?
- If not, keep planning/simulation isolated.

## 4.10 Handoff impact
- Did this step change current phase, next boundary, authority, dependency order, active watches, or branch checkpoints?
- If yes, update the handoff pack before ending the work tranche.

---

# 5. Revalidation triggers — avoid unnecessary repetition

Do **not** re-run a closed check solely because a new session starts.

Revalidation is required when at least one material trigger exists:
- relevant source/branch changed;
- a new relevant commit appeared;
- a new power/economy/meta layer was added and explicitly requires upstream recheck;
- simulator/runtime mismatch appears;
- deterministic replay/hash diverges;
- a prior WATCH becomes relevant to the new gate;
- a frozen/prospective contract explicitly requires a pre-use check;
- a newly recovered source contradicts the assumed authority.

If none apply, cite the existing PASS/approved evidence and continue.

---

# 6. Current P4-C1 review boundary

P4-C1 must not be reduced to five isolated skill descriptions.

For each class Lv26 contract, recover exact evidence and review at least:
- interaction with Lv6/11/16/21;
- P2 scalar-vs-effect-rule classification;
- targeting/retarget/proc ownership;
- crit inheritance policy where relevant;
- penetration/armor/mitigation ordering where relevant;
- knockback/control/zone semantics where relevant;
- monster role-expression impact;
- T4 Stage31–39 support/siege interaction;
- Lv26-to-Lv31 runway;
- future monster/T5+ extensibility;
- deterministic attribution;
- simulator/runtime parity implications.

Do not invent a generalized Lv26 power scalar.
Do not begin P4-C2 until P4-C1 is explicitly approved.

---

# 7. Handoff maintenance protocol

At the end of every meaningful work tranche, check whether these files require synchronization:

1. `../PROJECT_STATUS.md`
2. `../NEXT_WORK.md`
3. `../SESSION_HANDOFF.md`
4. active dependency YAML, **only if dependency order/state changed**
5. current phase contract/report
6. this protocol, **only if operating rules/read order changed**

Handoff must state:
- live canonical branch and re-fetch instruction;
- current phase and exact next boundary;
- latest user-approved decision;
- active watches/blockers;
- what is candidate vs frozen vs production-authorized;
- production/harness/source branch checkpoints where relevant;
- explicit prohibited next actions;
- mandatory read order for the next session.

Do not hard-code a branch HEAD as permanent truth. A handoff may record a checkpoint SHA, but must say live remote wins and the next session must re-fetch after all sync commits.

---

# 8. Session-close quality gate

Before considering a tranche ready for handoff, answer:

```text
1. Did we change semantics, values, dependency order, or only evidence?
2. Did any prior approved invariant become inconsistent?
3. Did we create a new downstream recheck obligation?
4. Did any WATCH become a blocker or get resolved?
5. Did production remain unchanged unless explicitly authorized?
6. Are status / next-work / handoff documents synchronized?
7. Can a new session recover the state without needing the user to explain what to read next?
```

If item 7 is NO, handoff work is incomplete.

---

# 9. Current exact boundary at protocol creation

Current live route at creation:

```text
R2 USER APPROVED
production gameplay/numerical changes unauthorized
P4-C1 — LV26 STRUCTURAL SKILL-CONTRACT DECISION = NEXT
P4-C2 = BLOCKED_PENDING_P4C1
P10R = mandatory later EXP / multiplayer-timebase reconvergence before permanent progression depends on final EXP behavior
```

This section is a checkpoint only. Future sessions must use live `PROJECT_STATUS`, `NEXT_WORK`, `SESSION_HANDOFF`, and the latest dependency plan to determine the actual boundary.