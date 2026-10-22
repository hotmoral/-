# Timing Defense — Ten-Stage Persistent Run Kernel Proposal V0.1

Date: 2026-10-23 KST  
Status: **PROPOSED / AWAITING USER APPROVAL / NO NUMERICAL FREEZE**

Depends on:
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `26_MODEL_A_T1_T4_MACRO_SKELETON_V0_1.md`
- `28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/skilled_v2_central_sequence_candidate_v0_1.yaml`

---

# 0. Decision boundary

P3 is not a difficulty-calibration phase and not launch Stage authoring.
Its purpose is to prove that approved P1 run-state semantics and P2 modifier/attribution semantics remain coherent across repeated Stage transitions, failure/retry, snapshot/resume and early skill-state changes.

This proposal intentionally avoids freezing:
- exact EXP formula;
- exact Base HP;
- final shop cadence/economy;
- permanent star/achievement values;
- boss design;
- exact launch Stage recipes;
- multiplayer progression rules.

No P3 kernel implementation should begin until the material choices below are approved.

---

# 1. Key consistency finding — old T1 skeleton is stale for current Model A

`11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md` was authored under the older all-nine-monsters-in-T1 direction.
Current active Model A instead uses:

```text
T1: GRUNT / RUNNER / BRUTE
T2: + SHIELD / FLYER
T3: + CHARGER / SPLITTER
T4: + SUPPORTER / SIEGER
```

Current T1 windows are:
- Stage1–3: GRUNT baseline;
- Stage4–9: RUNNER introduction / mix;
- Stage10: GRUNT/RUNNER checkpoint;
- BRUTE first teach is later, Stage15–17 candidate.

Therefore P3 must not reuse the stale 11-document Stage1–10 schedule.

Recommendation:
> use a **T1-shaped synthetic integration slice** consistent with current Model A, but explicitly mark it as test fixture data rather than exact production Stage authoring.

---

# 2. P3 decision A — identity of the 10-stage slice

## Option A1 — exact launch-style T1 authoring now
Not recommended.

Why:
- exact Stage data is intentionally downstream;
- any later EXP/shop/skill change would cause needless re-authoring;
- P3 only needs enough combat variety to exercise state continuity.

## Option A2 — arbitrary stress mix from all 20 recipes
Not recommended as primary lane.

Why:
- would violate current T1 availability/teaching grammar;
- role stress would contaminate lifecycle debugging;
- all-20 role expression is already separately validated.

## Option A3 — current-Model-A T1-shaped synthetic fixture
**RECOMMENDED.**

Use only currently valid first-10 vocabulary:
- GRUNT baseline;
- RUNNER teach/mix;
- no BRUTE before its current Stage15–17 window;
- no boss at Stage10 because checkpoint boss is optional and boss mechanics are P7 downstream.

Suggested fixture grammar, not production Stage lock:

```text
S1  E01 baseline
S2  E01 baseline
S3  E01 baseline
S4  E01 transition
S5  E02 RUNNER teach
S6  E02 RUNNER teach
S7  E02 RUNNER consolidation
S8  E02 mixed
S9  separated E01 -> E02
S10 separated E02 -> E01 checkpoint
```

Reuse existing validated representative recipe anchors rather than inventing new monster coefficients.
Exact repetition/count/cadence in this fixture is test-only.

---

# 3. P3 decision B — EXP / Level / Lv6 handling

P3 needs to exercise level/skill state, but the exact EXP curve is deliberately P4 work.

## Option B1 — import legacy/current EXP formula and call it provisional
Not recommended.

Risk:
- silently anchors future campaign to a formula that was explicitly meant to be re-derived from desired skill windows.

## Option B2 — disable level progression entirely
Too weak.

Risk:
- P3 would fail to test LEVEL-scope modifier transitions and class Lv6 activation across Stage boundaries.

## Option B3 — dual deterministic test lanes
**RECOMMENDED.**

Primary lanes:

### Lane L0 — `LV1_CONTINUITY`
- level fixed at 1;
- EXP formula disabled;
- records valid timing-event count / EXP-eligible event count for later P4 use;
- tests pure run-state continuity.

### Lane L1 — `FORCED_LV6_TRANSITION`
- no EXP formula;
- deterministic test hook activates Lv6 at Stage6 start;
- tests that LEVEL-scope/effect-rule changes become active and remain attributable without pretending Stage6 is an empirically calibrated unlock result.

Consequence:
- P3 should report **Lv6 transition plumbing evidence**, not `Lv6 reach evidence`.
- actual Lv6 reach distribution moves cleanly to P4, where the EXP curve belongs.

This is a process correction to the previous P3 output label, not a change to the desired Lv6 Stage5–7 candidate window.

---

# 4. P3 decision C — shop / coin / inter-stage handling

Shop cadence and economy are P5 downstream.

## Option C1 — reuse legacy every-Stage shop
Not recommended.

It would accidentally turn a prototype cadence into campaign architecture.

## Option C2 — remove coin/shop state entirely from P3
Insufficient.

P1 explicitly says run coin/shop ranks persist within an attempt, so persistence/reconnect fields still need validation.

## Option C3 — neutral transition + sentinel persistence fixtures
**RECOMMENDED.**

Primary 10-stage lane:
- no shop UI/purchase decision;
- no coin reward tuning;
- `shopPolicy = OFF/NEUTRAL`;
- each Stage crosses a logical `STAGE_TRANSITION` boundary, not a product shop cadence.

Targeted fixture tests:
- inject nonzero `runCoin` and `shopRanks` sentinel state;
- cross Stage transition and snapshot/resume;
- assert values persist unchanged;
- sentinel values are test constants only and must never be interpreted as balance candidates.

This validates P1 without pre-empting P5.

---

# 5. P3 decision D — temporary combat effects at Stage boundary

P1 explicitly preserved combo/charge but did not yet classify all short-duration player combat effects.
P2 introduced `TEMPORARY` effect scope.

Examples:
- Tank short-duration wall shield;
- slow/control zone;
- pending projectile/secondary hit;
- delayed outer-ring or dagger queue in later skill modes.

Three possible policies:

## D1 — timers keep running through intermission/shop
Not recommended.

Problem:
- shop/menu duration changes future combat strength;
- player thinking time becomes balance-relevant.

## D2 — timers pause and resume in next Stage
Not recommended as default.

Problem:
- short combat buffs can be banked indefinitely through intermission;
- a 3-second combat shield may reappear minutes later.

## D3 — current-stage combat temporary state settles, then clears
**RECOMMENDED.**

Rule:
- already-authorized action effects are allowed to settle before Stage transition finalizes;
- once the Stage settlement barrier is reached, ordinary short-lived `TEMPORARY` combat effects do not carry into the next Stage;
- later mechanics that are explicitly designed to persist across Stage boundaries must use an explicit RUN/inter-stage-persistent contract rather than inheriting TEMPORARY behavior by accident.

This does not alter P1 combo/charge persistence; those are explicit RunState fields.

---

# 6. P3 decision E — Stage settlement barrier

Immediate transition on the exact frame the last monster dies is unsafe once Heavy, delayed hits and post-action procs exist.
Carrying unresolved action state into the next Stage is also unsafe.

**RECOMMENDED settlement contract:**

```text
last authored Stage spawn has occurred
+ no live Stage-owned enemy remains
+ stop accepting new current-Stage player turns
+ drain already-authorized current action/effect resolution
+ no unresolved half-Heavy / delayed current-Stage hit / Stage-owned combat transient remains
= STAGE_SETTLED
-> reset StageState
-> advance Stage number
```

Invariants:
- started Heavy X->Y completes as already approved;
- delayed effects from an already-authorized action may finish current-Stage resolution;
- no projectile/delayed hit/temporary zone leaks into the next Stage;
- Stage transition itself does not reset combo/charge/Base HP/run identity.

### Terminal ambiguity stop condition
P3 should **not silently freeze** a same-timestamp `Base HP <= 0` versus final-clear precedence if current authority does not already decide it unambiguously.
If such a collision is produced, classify:
`SIMULTANEOUS_TERMINAL_COLLISION_OPEN_DECISION`
and return to the user with evidence before changing product semantics.

Similarly, attempt failure is terminal; P3 should not infer that unresolved future action events can revive a destroyed base unless explicitly approved later.

---

# 7. P3 decision F — player-model and RNG continuity

Previous all-20 execution exposed a real seed-prefix defect when short scenarios restarted the same player sequence repeatedly.

**RECOMMENDATION:**
- one SKILLED_V2_CENTRAL player-model stream per Tier attempt;
- never reset its FOCUS/BASE state at each Stage;
- never restart the same short PRNG prefix at each Stage;
- snapshot/resume must preserve the player-model RNG/state exactly;
- use deterministic named/substream ownership where randomness is required so player-judgment sampling and combat-proc sampling do not silently shift each other.

Suggested conceptual streams:
- `JUDGMENT`
- `COMBAT_PROC`
- `STAGE_FIXTURE` only if future fixture randomization is introduced

For current fixed Stage recipes, authoring itself need not consume RNG.

The existing 1100ms action interval may remain only as:
`BOUNDED_CURRENT_MECHANIC_SIMULATION_CONTROL_NOT_SKILL_FIT`.

---

# 8. Primary execution matrix recommendation

P3 is structural, so a huge Monte Carlo is unnecessary.

Recommended primary matrix:

```text
5 classes
× 3 existing base seeds [101, 211, 307]
× 2 power lanes [LV1_CONTINUITY, FORCED_LV6_TRANSITION]
= 30 persistent 10-stage runs
```

This is enough to:
- cross repeated Stage boundaries;
- exercise all five class Lv6 identities in the forced lane;
- keep player sequence variability;
- preserve paired deterministic comparison.

Do not interpret 30-run clear rate as production difficulty evidence.
The main fixture should be intentionally nonterminal for integration; if ordinary fixture pressure causes frequent failure, first classify whether the **fixture** is unsuitable before proposing game balance changes.

Base HP for the primary nonterminal lane remains a configurable **TEST_ONLY sentinel**, not a balance candidate.
A separate low-HP failure fixture validates attempt termination/reset.

---

# 9. Mandatory targeted fixtures

Besides the 30 primary runs, use bounded deterministic contract tests.

## F1 — charge continuity
End one Stage with charge ready; next Stage first valid attack must consume the preserved Heavy state according to the approved charge grammar.

## F2 — combo continuity / N3 boundary
Cross a Stage boundary with combo near a milestone and verify the next PERFECT can legitimately cross the N3 milestone without a Stage reset.
N3 remains isolated under its frozen contract.

## F3 — failure / retry reset
Use deliberately low test Base HP to force failure.
Assert:
- attempt terminates;
- new retry starts Stage1;
- level/EXP/coin/shop/combo/charge reset;
- permanent account fixture state remains.

## F4 — snapshot/resume equivalence
Take deterministic snapshots at:
- inter-Stage boundary;
- mid-Stage;
- after player-model state has advanced.
Resume and require final trace/hash equality with uninterrupted execution.

## F5 — modifier aggregation / attribution
Inject sentinel ACCOUNT + CLASS_PERMANENT + RUN modifiers to the same stat.
Assert additive P2 aggregation and exact per-source attribution ledger entries.
No sentinel magnitude becomes a balance candidate.

## F6 — temporary-effect boundary
Create a short-lived TEMPORARY combat effect near Stage settlement.
Assert the approved boundary policy exactly.

## F7 — no transient leakage
At `STAGE_SETTLED`, assert zero stale:
- target identity;
- enemy instance;
- monster capability state;
- unresolved action queue item;
- Stage-local timer;
- Stage-local temporary combat object.

---

# 10. Power Attribution requirements in P3

Every material event needed for P3 validation should carry enough attribution to reconcile:
- player attack damage;
- class Lv6 effect contribution;
- combo transform;
- N3 targeted fixture contribution;
- wall damage;
- generic/unique/shield contribution where active in a fixture;
- Base HP delta.

Per Stage, the ledger totals must reconcile with state deltas.

Required audit concept:

```text
sum(realized Base HP damage ledger)
== startBaseHp - endBaseHp
```

subject only to explicitly recorded healing/max-HP changes, which are OFF in the primary P3 lane.

---

# 11. P3 acceptance gates

P3 should be considered structurally PASS only if:

1. identical input versions + seed + class + power lane produce identical final hash and trace;
2. 10 Stage transitions complete without hidden reset/leak in the primary lane;
3. Base HP, combo and charge obey P1 exactly;
4. forced Lv6 activation changes only authorized LEVEL/effect paths and is visible in attribution;
5. neutral Stage transitions do not mutate coin/shop state;
6. snapshot/resume is equivalent to uninterrupted execution;
7. targeted failure/retry fixture exactly matches P1 reset semantics;
8. P2 same-stat additive aggregation and ledger reconciliation pass;
9. no stale StageState/transient combat state crosses `STAGE_SETTLED` unless explicitly RUN-scoped;
10. no P3 result is promoted into final EXP/shop/Base-HP/difficulty numbers.

Possible classifications:
- `P3_STRUCTURAL_PASS`
- `STATE_LEAK`
- `STAGE_TRANSITION_RESET_DEFECT`
- `SNAPSHOT_REPLAY_DIVERGENCE`
- `PLAYER_SEQUENCE_RESEED_DEFECT`
- `ATTRIBUTION_RECONCILIATION_DEFECT`
- `TEMPORARY_SCOPE_LEAK`
- `FAIL_RETRY_RESET_DEFECT`
- `SIMULTANEOUS_TERMINAL_COLLISION_OPEN_DECISION`

---

# 12. What P3 must not claim

Even after a PASS, P3 must not claim:
- T1 Stage1–10 exact launch design is final;
- Lv6 actually reaches Stage6 under final EXP;
- Base HP balance is correct;
- skilled clear rate is calibrated;
- combo40 frequency is final;
- shop/economy is balanced;
- Stage10 boss policy is decided;
- permanent progression is balanced;
- multiplayer semantics beyond P1 are decided.

P3 is an integration admission gate into P4.

---

# 13. Requested user decisions

Approve or modify the following package:

1. **T1-shaped synthetic first-10 fixture** using current Model A and only GRUNT/RUNNER in the main lane; no BRUTE/boss yet.
2. **Dual power lanes**: LV1 continuity + forced Lv6 at Stage6, with no exact EXP formula and no Lv6 reach claim.
3. **No real shop/economy in P3**: neutral Stage-transition boundary plus sentinel coin/shop persistence tests.
4. **Stage-local TEMPORARY combat effects settle then clear at Stage boundary by default**; only explicitly RUN-scoped effects may persist.
5. **Stage settlement barrier** drains already-authorized current-action effects before transition and forbids transient carryover.
6. **One continuous SKILLED_V2_CENTRAL stream/RNG state across the whole attempt**, not per-Stage reseeding.
7. **30-run primary matrix + bounded targeted fixtures**, with P3 evaluated as structural integration rather than balance calibration.
8. Change the P3 dependency output label from `provisional_lv6_reach_evidence` to **`lv6_transition_plumbing_evidence`**, leaving actual reach calibration to P4.

Only after user approval should the P3 kernel/data/validator be implemented.
