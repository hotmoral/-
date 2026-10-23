# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## 0. Recovery rule — mandatory

Always fetch the live remote first.
Do not reconstruct current state from chat, memory, copied SHA, or one old paragraph.
Live GitHub canonical state always wins.

The user must **not** have to re-explain either:
1. the factual project state; or
2. the reasoning method used to analyze it.

A new session must recover not only *what* is open, but *why* prior directions were accepted/rejected and what authority each result has.

---

# 1. Mandatory read/check order

1. live `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`
5. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
6. `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
7. `legacy-game-structure/data/system_dependency_calibration_order_v0_31.yaml`
8. `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
9. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
10. `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
11. `legacy-game-structure/79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
12. `legacy-game-structure/91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
13. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
14. `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
15. `legacy-game-structure/135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
16. `legacy-game-structure/137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
17. `legacy-game-structure/142_P5_STAGE48_FODDER_CHAIN_AND_GLOBAL_STANDOFF_BOUNDARY_RESULT_V0_1.md`
18. **latest:** `legacy-game-structure/143_P5_SKILLED_V2_LATE_RUN_REINTERPRETATION_AND_P5_P6_FIDELITY_GATE_V0_1.md`
19. `CHARACTER_PROFILE_RADAR_V1.md`
20. current production/harness heads
21. only then exact source/runner files needed for the next bounded unit

For broad recovery, also read master progression/content docs 01/02/03/04/06/07/08/15/16/22/25/31 as needed.

Do not rerun closed P1/P2/P3/P4 or the whole class-identity group merely because a chat restarted.

---

# 2. Mandatory cognition sequence

Before touching the current local task, reconstruct:

```text
Tier / Stage purpose
-> content novelty / monster role
-> class identity / skills
-> run-state persistence
-> player mastery / judgment model
-> shop/economy growth
-> attack count / EXP / skill-reach feedback
-> encounter geometry / chronology / frontmost order
-> wall pressure / SIEGER exposure
-> STAGE_SETTLED
-> carried wall deficit
-> later-Stage consequences
-> downstream P6/meta/multiplayer impact
```

Then classify the problem:

```text
source/simulator fidelity?
lifecycle/state semantics?
geometry/chronology/frontmost ordering?
class/package semantics?
shop/feedback interaction?
exact numerical balance?
```

Repair order:

```text
fidelity
-> lifecycle/state
-> geometry/chronology
-> package/class semantics
-> shop/feedback
-> exact scalar last
```

Use the smallest bounded probe that distinguishes the cause.
Do not confuse deep review with repeated work.

At every material slice check:
- upstream invariants;
- downstream consumers;
- feedback loops;
- class identity/fairness;
- deterministic attribution;
- scope/cost;
- authority level;
- production boundary;
- whether canonical handoff state changed.

---

# 3. Important-decision approval rule — mandatory

The user explicitly requires:

> Important design/content/numerical/work-boundary decisions must not be silently applied. Analyze first, explain simply, then obtain user approval before adoption.

Approval is required before:
- changing project phase/work direction (including P5→P6 transition);
- adopting a Stage48/49 packet;
- approving a new monster/elite/hardened state;
- adopting exact monster/class/shop/EXP values;
- changing SIEGER standoff/windup/cadence;
- selecting Tank damage scalar;
- opening buff/resistance/skill-like monster mechanics as an adopted direction;
- changing approved structural contracts;
- production gameplay changes.

Diagnostic/instrumentation/fidelity work may proceed independently when gameplay semantics remain unchanged.

Before approval request, provide:
- exact question;
- why now;
- constraints;
- evidence;
- real alternatives/tradeoffs;
- recommendation;
- risks/reversibility;
- what remains open.

---

# 4. Communication rule — mandatory

Explain in easy Korean first:

```text
문제가 뭔지
-> 왜 그런지
-> 다음에 뭘 볼지
-> 무엇은 아직 결정/적용하지 않았는지
```

Technical detail can follow.

---

# 5. Branch checkpoints

Planning/canonical:
- `timing-defense-workspace`
- always re-fetch live HEAD; copied SHA is only a checkpoint

Production:
- `timing-defense-cloudflare-do-poc`
- last verified `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`

Temporary diagnostic branch:
- `timing-defense-workspace-temp-check`
- no planning/production authority
- do not promote temp scripts/workflows automatically

---

# 6. Current exact phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE / STAGE_SETTLED + run-state authority
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 = USER_APPROVED
P5 class identity group = DIRECTIONALLY CLOSED
P5 limited armored/hardened frontline exploration = USER APPROVED
P5 GRUNT-like fodder chronology = DIAGNOSTICALLY VALID
P5 global SIEGER standoff movement = STRONGLY DISFAVORED AS PRIMARY REPAIR
P5 prior Stage46->49 survival results = ALL-PERFECT / EFFECTIVELY ALL-P×P UPPER BOUND
P5 central-skilled diagnostics = upstream Stage46/47 failure exposed
P5 current runner = PARTIAL FIDELITY FOR FINAL SKILLED BALANCE
CURRENT = USER DECISION GATE ON BOUNDED P5→P6 FIDELITY BRIDGE
full P6 convergence = NOT STARTED
production = UNCHANGED / UNAUTHORIZED
```

No Stage48 packet, hardened monster, elite system, exact SIEGER standoff, class scalar or production value is approved.

---

# 7. Stable structural truths

## P1 run-state continuity
Within one Tier attempt:
- Base HP/Base Max HP persist;
- level/EXP/coin/shop ranks persist;
- combo persists across Stage/shop/target-wait downtime unless a non-PERFECT judgment breaks it;
- charge persists across Stage/shop/intermission;
- an in-progress Heavy X→Y resolves before transition.

New Tier attempt resets run-local state.

## P3 Stage transition

```text
last authored spawn
+ zero live Stage-owned enemies
+ authorized action/effect drained
+ no unresolved delayed Stage transient
= STAGE_SETTLED
-> Stage clear/shop
-> reset Stage-local enemies/transients
-> next Stage
```

Wall current/max/absolute deficit persists.
Enemy instances do not leak into the next Stage.

## P5 A2 shop
- every cleared non-final Stage: shop available but nonblocking;
- personal wallets;
- ordinary kill coin baseline to killing human;
- all-human Stage-clear income-floor candidate;
- ATK/CRIT/CRITDMG/KNOCK personal;
- FORTIFICATION/DEF shared wall;
- Fortification preserves absolute damage deficit;
- no routine full-shop maxout by Stage49.

40% shop effect and economy centers remain diagnostic only.

## Class identity guards

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

Rules:
- high axes remain causal strengths;
- low axes remain real limitations;
- `SURVIVAL != CLEAR`;
- Tank solo parity not required;
- no hard class lockout;
- no global Archer nerf / Mage buff for bad encounter authoring;
- no Tank buff/nerf from partial-fidelity skilled results;
- Rogue deterministic retarget not first repair axis.

---

# 8. Stage48 evidence still valid

## Old repeated proxy packet
Rejected. It reused `ARMORED_DURABLE_PROXY`—a Knight penetration isolation body—as repeated all-class escort and contaminated Mage/Tank pressure.

Old diagnostic anchor only:

```text
HP 1600
armor 0.55
knockResist 0.65
speed 0.04
wall 160
```

Never treat these as production values.

## Armored/hardened exploration axis
The user approved the **direction only**.
Dual purpose:
1. slow late Mage/Archer ordinary-volume erasure;
2. buy protected SIEGER time.

No exact stat/count/identity approved.

## Low density
Spatial separation helps; excessive early temporal separation hurts.
Representative earlier evidence:

```text
Archer SIEGER life ~6.825 -> ~9.075 s
Archer death x ~0.613 -> ~0.512
Knight life ~2.325 -> ~4.575 s
Mage ~7.2 s in tested two-body spatial case
```

Mage differs because approved Lv31 chain semantics can reach later live/unhit targets.
Do not change Mage package semantics merely to protect SIEGER.

## Fodder/cheap-target hypothesis
User proposed cheap bodies to spend Mage follow-up target opportunities before SIEGER.
Validated as a chronology axis:

```text
FODDER_COUNT_ALONE != SOLUTION
TYPE + ORDER + ARRIVAL_PHASE + SPATIAL_DENSITY = CAUSAL
```

GRUNT2 helped; GRUNT3 showed little extra benefit in the tested band.
Fast fragile bodies first often disappeared too early.
One durable body + trailing GRUNT can be efficient.

## Current clean diagnostic center
Probe only:

```text
3 spatial armored diagnostic bodies
+ 2 GRUNT
+ 1 SIEGER
```

Not approved.

## Global standoff
No tested threshold simultaneously gave all-class Stage48 SIEGER firing and preserved current Stage46→49 reserve.
Global standoff movement is not the current primary repair.
`0.38` itself is not frozen.

See doc142 for exact values/runs.

---

# 9. Critical mastery reinterpretation

The user asked whether recent results were skilled or all PERFECT.
Source audit found the P5 late-run simulator used:

```text
ordinary = PERFECT
successful Heavy = CRITICAL
current chain heavy misses = none
```

Therefore previous Stage46→49 survival/reserve values are **all-PERFECT/effectively all-P×P upper-bound evidence**, not central-skilled baseline results.

Do not describe old `BALANCED` results as skilled play. `BALANCED` was a shop profile.

---

# 10. SKILLED_V2_CENTRAL diagnostic result

Canonical central model:
- streak-aware two-state deterministic sequence;
- intended marginal 70% PERFECT / 20% GOOD / 10% NORMAL;
- Heavy consumes two judgments;
- P+P alone = CRITICAL and Lv31 final-package gate;
- not empirical population telemetry.

Expanded run:

```text
run id 39968100989
repeat determinism PASS
SHA256 ec4ed61d8288b9a2bb2e1575bf5f8d4e1191fdbabcae9a5d11cae9b7cde8d6c9
```

20 seeds × five classes = 100 cases.
Realized mix:

```text
PERFECT ~72.37%
GOOD    ~18.45%
NORMAL   ~9.19%
P×P Heavy/CRITICAL ~58.06%
```

Outcome:

```text
through Stage49 = 45/100
fail Stage46 = 26
fail Stage47 = 21
fail Stage48 = 0
fail Stage49 = 8
```

Per class through Stage49:

```text
Knight 3/20
Rogue  4/20
Tank   2/20
Archer 18/20
Mage   18/20
```

Interpretation:
- Stage48 is not the main failure point in this skilled screen;
- upstream Stage46/47 and P×P/Lv31-final dependence dominate;
- exact percentages are not final balance authority because runner state fidelity is incomplete.

---

# 11. Factor isolation — dominant cause

Run:

```text
39968400953
repeat determinism PASS
SHA256 1ae220cb0bbebd388f9c014a9208335c4b8eeb895b4163109e78895f95b4a420
```

Stage46→47, 20 seeds × five classes:

```text
ALL_PERFECT control                         -> pass
ordinary central, Heavy forced P×P          -> 100/100 through47
ordinary PERFECT, Heavy central/P×P variable -> 63/100 through47
full central                                -> 58/100 through47
```

Tank with ordinary PERFECT but central Heavy frequency:

```text
0/20 through47
```

Causal conclusion:

```text
ORDINARY_NONPERFECT_QUALITY_ALONE != PRIMARY_CAUSE
REDUCED_PXP_LV31_FINAL_FREQUENCY = DOMINANT_CURRENT_SENSITIVITY
```

Do not repair this with immediate Tank buff, Stage46 nerf, SIEGER change or generic HP reduction.

---

# 12. Simulator fidelity gap — current top blocker

P1 requires combo and charge continuity across Stage/shop.
The current P5 Stage46→49 runner was built for shop/class/chronology diagnosis, not as a complete P1/P3 run-state simulator.

Current P5 late-run runner is missing/incomplete for final skilled authority:
- canonical charge carried between Stages;
- canonical combo carried between Stages;
- full combo damage bonus pipeline;
- full N3 milestone behavior;
- one unified persistent skilled judgment state combined with P4-D2 Lv31 + P5 shop.

Existing P3 kernel already contains:
- persistent combo;
- persistent charge;
- SKILLED_V2 judgment state/RNG;
- charge-driven Heavy;
- combo bonus;
- N3 milestones;
- deterministic run-state continuity.

Current P5 runner contains:
- P4-D2 Lv31 packages;
- P5 shop snapshot/effects/attribution;
- Stage46→49 right-edge encounter chronology;
- STAGE_SETTLED and wall carry.

There is not yet one runner combining both sets faithfully.

This is why central-skilled survival percentages above are causal evidence, not final balance numbers.

---

# 13. Dependency-order meaning

Canonical doc70 defines:

```text
P3 persistent run kernel
-> P4 player-power spine
-> P5 shop candidate
-> P6 joint run-power convergence
```

P6 explicitly exists to evaluate:

```text
EXP/skill
-> shop
-> Stage pressure
-> resulting event count
-> revised skill reach
```

with wall trajectory, class/shop policy, timing-event count and combo40 opportunity.

The current skilled result is therefore a genuine P5→P6 coupling signal, not merely another Stage48 scalar issue.

---

# 14. Exact current decision gate

Do not perform further important Stage48 tuning or phase transition until user chooses.

### A — RECOMMENDED
Open a bounded **P5→P6 fidelity bridge**.

Minimum bridge requirements:
- persistent combo;
- persistent charge / charge-driven Heavy;
- persistent SKILLED_V2 judgment state;
- combo bonus and N3;
- P4-D2 Lv31 P×P packages;
- P5 shop snapshot/attribution;
- Stage46→49 right-edge encounters;
- STAGE_SETTLED;
- carried wall deficit;
- paired deterministic ALL_PERFECT vs SKILLED_V2 comparison.

After bridge admission, return to Stage48 armored+fodder analysis on the faithful baseline.

Important:
- this does NOT formally close P5;
- this does NOT automatically start full P6 convergence;
- this does NOT approve any balance number.

### B
Continue Stage48 micro-tuning on current partial runner.
Risk: optimize against wrong player-power surface and redo work.

### C
Close P5 immediately and enter full P6 convergence.
Risk: phase jump larger than necessary.

Recommendation: **A**.

No option adopted yet.

---

# 15. Session-close / next-session quality gate

Before handing off or resuming:

```text
1. re-fetch live canonical HEAD
2. confirm active plan is v0.31
3. confirm production/harness unchanged unless authorized
4. distinguish all-PERFECT upper-bound evidence from SKILLED_V2 evidence
5. distinguish causal diagnostics from final balance authority
6. preserve P1 combo/charge continuity contract
7. preserve STAGE_SETTLED and wall deficit
8. do not resume Stage48 scalar tuning before current fidelity gate is resolved
9. stop for user approval on A/B/C
10. after any meaningful group, sync PROJECT_STATUS / NEXT_WORK / SESSION_HANDOFF / dependency plan
```
