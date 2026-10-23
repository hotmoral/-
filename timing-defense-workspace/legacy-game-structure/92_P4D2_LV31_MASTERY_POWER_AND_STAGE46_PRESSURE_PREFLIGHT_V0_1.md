# Timing Defense — P4-D2 Lv31 Mastery Power & Stage46 Pressure Preflight V0.1

Date: 2026-10-23 KST  
Status: **ACTIVE PREFLIGHT / EXECUTION AUTHORIZED / NO NUMERICAL FREEZE**

Authority:
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`

---

# 0. Purpose

P4-D2 no longer tries to fit a timid Lv31 into the old late-game pressure envelope.

It jointly evaluates:

```text
Lv31 final-skill power fantasy
<->
Stage46+ pressure regime capable of requiring/absorbing that power
```

The intended late-run experience is:
- Stage41..45: acquire Lv31;
- Stage46: pressure jumps sharply;
- without Lv31/P×P output, intended skilled play may be buried by wave accumulation;
- with Lv31 and maintained timing/combo quality, the player gets dramatic pressure-reset moments;
- Stage48..49 demand better timing of those resets;
- Stage50 is full-kit final application.

---

# 1. Execution lanes

## Lane A — acquisition fairness
Measure Lv31 possession probability at Stage46 entry under intended-skilled and high-mastery traces.

Candidate checkpoints only:
- 97%
- 98%
- 99%

Required outputs:
- P50/P75/P90/P95/P99 unlock Stage;
- Stage46 entry possession rate by class;
- Stage46 entry possession rate by player count/team composition once multiplayer is credible;
- missed-Lv31 cause attribution: timing quality vs class kill-speed feedback vs encounter opportunity vs retry/failure.

No exact possession target freezes in P4-D2.

## Lane B — final-skill power expression
Each class is tested as a strong final payoff, not a conservative increment.

Knight:
- two-pass broad frontline break;
- preserve bounded corridor identity;
- test second-wave damage/knockback strongly enough to create visible pressure reset.

Rogue:
- real Dagger Storm projectile counts `12 / 16 / 20`;
- `16` = working center;
- target persistence then deterministic retarget;
- test event cadence/readability and performance watch separately from balance.

Tank:
- battlefield pressure reset through strong knockback/control + wall protection;
- retain local Aftershock identity;
- test whether control actually creates survival space under Stage46+ pressure.

Archer:
- one strict-line unlimited-depth final arrow;
- aligned lines should be allowed to disappear dramatically;
- test whether formation geometry can keep later waves non-trivial without arbitrary target caps.

Mage:
- bounded but spectacular three-stage density collapse + final chain;
- large-cluster deletion is allowed/desired;
- SPLITTER transformation visibility remains an encounter-authoring watch, not an automatic nerf.

## Lane C — Stage46+ pressure absorption
Do not only raise HP.
Pressure candidates must vary:
- spawn density;
- formation depth;
- cadence overlap;
- protected SUPPORTER/SIEGER placement;
- CHARGER timing windows;
- SPLITTER population rebound;
- simultaneous front/back pressure where appropriate.

Primary structural test:

```text
ordinary Lv26 throughput < sustained Stage46+ inflow/pressure
Lv31 P×P pressure reset > critical accumulated pressure at skillful timing
```

This is not an exact inequality freeze; it is the desired combat shape.

---

# 2. Combo / P×P as mastery difficulty

Stage46+ must make final-skill access depend on maintaining timing execution, not merely owning Lv31.

Measure:
- P×P opportunity frequency;
- combo survival probability;
- time between successful pressure resets;
- accumulated monster count/pressure before each reset;
- failure cascade after a missed P×P;
- recovery possibility after one miss vs repeated misses.

Desired shape:
- one mistake can create real pressure;
- repeated mistakes should plausibly bury the player;
- perfect/near-perfect execution should feel decisively powerful;
- do not require an artificial `Lv31` check in code.

---

# 3. Class fairness rule

The gate may be hard in practice, but it must not be unfair because one class reaches Lv31 structurally later due to its own higher kill speed reducing EXP opportunities.

Therefore:
- no hidden class XP compensation is introduced in P4-D2;
- if Stage46 possession rates diverge materially by class, classify cause first;
- P10R remains mandatory before final EXP semantics;
- Stage46 pressure cannot be numerically frozen while acquisition fairness is unresolved.

---

# 4. Monster-role-expression rule

A spectacular Lv31 may erase a monster quickly after that monster has expressed its role. That is acceptable.

A failure occurs when authored encounters systematically prevent the monster from ever expressing its intended decision/telegraph before the player can meaningfully perceive it, unless the Stage itself is deliberately a post-mastery deletion showcase.

Therefore Stage46..49 should contain both:
- power-revelation moments where the player is allowed to annihilate a large wave;
- mastery-pressure moments where formation/timing makes the final skill choice matter.

Do not make all late Stages identical giant HP walls.

---

# 5. Rogue performance boundary

Rogue projectile volume is a design feature.

Performance policy:
- 12/16/20 real projectiles are all valid P4-D2 candidates;
- no candidate is rejected merely because it has more events than Lv21;
- later multiplayer stress must test worst-case simultaneous storms;
- if performance fails, first examine batching, event representation, projectile/VFX pooling and network payload strategy;
- reduce projectile count only if the implementation cannot meet runtime targets after reasonable engineering, or if combat readability/balance evidence favors fewer projectiles.

---

# 6. Acceptance classifications

Possible P4-D2 outcomes:

`PASS_WITH_WATCHES`
- class fantasies are strong;
- Stage46+ can absorb them structurally;
- no unavoidable class lockout/role contradiction;
- acquisition fairness remains deferred but bounded by active watches.

`REVISE_POWER_MAGNITUDE`
- final skill under-delivers or over-erases despite reasonable pressure design.

`REVISE_STAGE46_PRESSURE_GRAMMAR`
- skill power is compelling but current pressure grammar cannot produce meaningful mastery.

`REOPEN_SPECIFIC_LV31_STRUCTURE`
- only if a class's finite final-template semantics themselves cause a structural contradiction.

Do **not** reopen the whole Lv31 package because a provisional coefficient is wrong.

---

# 7. Stop conditions

Stop and return to user decision only if:
- a new class identity change is required;
- a code-level Lv31 requirement gate is proposed;
- hidden class/player-count XP correction is proposed;
- a final Stage46 possession threshold is to be frozen;
- final EXP semantics are being changed;
- production implementation/numerical freeze is proposed.

Otherwise P4-D2 may iterate provisional values and pressure candidates within the approved direction without repeated user approval.

---

# 8. Immediate execution order

```text
1. Preserve P4-D1 approved final-skill structures
2. Materialize bounded Lv31 candidate magnitudes
3. Start Rogue at 16 projectiles, bracket with 12/20
4. Build pressure-response probes for Stage46+ rather than exact authored Stages
5. Measure P×P reset vs sustained pressure
6. Check class/monster-role watches
7. Feed results into P4-E provisional spine closure
8. Keep final EXP convergence deferred to P10R
```

No production gameplay source is changed by this preflight.
