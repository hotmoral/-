# Timing Defense — System Dependency & Calibration Order Review V0.1

Date: 2026-10-22 KST  
Status: **ACTIVE STRUCTURAL EXECUTION PLAN / NO NUMERICAL PRODUCTION FREEZE**

Depends on:
- `01_META_PROGRESSION.md`
- `02_TIER_SYSTEM.md`
- `03_STAGE_STRUCTURE_50.md`
- `06_SIMULATION_CALIBRATION_PLAN.md`
- `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
- `15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `21_MODEL_A_NOVELTY_BUDGET_AND_BOSS_PLACEHOLDERS_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `25_MODEL_A_META_PROGRESS_VOLUME_AND_SOFT_WALL_ENVELOPE_V0_1.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- `66_SKILLED_V2_CENTRAL_DESIGN_PRIOR_AND_HARNESS_CLOSURE_AMENDMENT_V0_1.md`
- `67_SKILLED_V2_CENTRAL_SEQUENCE_MODEL_V0_1.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`

Reference implementation/evidence:
- `DESIGN_DECISIONS.md`
- `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
- `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`
- `BALANCE_SIM_REPORT_V4_TEAM.md`

---

# 0. Review question

The project already has combat, class, monster, Tier, Stage, skill, star, achievement, shop, boss, multiplayer and progression concepts.

The question is not merely whether each subsystem exists.

The required question is:

> **In what order should semantics, data structures, candidate values, simulation, authoring and live implementation be performed so that coupled systems can converge with the least rework and the least attribution ambiguity?**

The answer is not a pure waterfall and not simultaneous full-detail design.

This document refines the existing `progressive deepening / iterative convergence` governance into an executable system dependency plan.

---

# 1. Executive verdict

The existing corpus has the correct high-level philosophy, but the current execution order is too coarse in four places.

## Gap A — Run-state lifecycle is not a dedicated prerequisite

Before multi-stage simulation, the project needs one explicit contract for what persists and resets across:
- attack/turn;
- encounter;
- Stage;
- shop/intermission;
- Tier attempt;
- account/session.

Without this, a synthetic Tier can accidentally embed arbitrary assumptions about base HP, combo, charge, EXP, coin, shop ranks or reconnect.

## Gap B — EXP/skill, shop and permanent power form a feedback loop

EXP is earned from valid timing events.
More damage can reduce the number of required attacks.
Therefore stronger shop/permanent power may reduce the number of EXP-producing events and shift skill reach later.

So this sequence is unsafe:

```text
freeze EXP -> later add shop/permanent power -> never revisit skill reach
```

Instead:

```text
provisional EXP/skill curve
 -> add shop
 -> re-check skill reach
 -> add meta power
 -> re-check skill reach again
```

Skill reach is a cross-system invariant, not a one-time calibration.

## Gap C — Boss and multiplayer cannot be treated as one late undifferentiated block

Boss/checkpoint mechanics change:
- Stage failure probability;
- run duration;
- timing-event/EXP opportunity;
- wall pressure;
- coin opportunity;
- 3-star probability.

Multiplayer changes:
- kill speed;
- wall pressure;
- class utility;
- shop ownership;
- star acquisition rate;
- achievement eligibility;
- dominant progression routes.

Therefore both require a bounded structural pass before permanent progression values are production-frozen.

## Gap D — Modifier stacking semantics must precede modifier values

Stars, achievements, shop, skills, combo, crit and defensive modifiers can produce multiplicative runaway if operation order is left implicit.

The exact values can stay open, but the **modifier pipeline and stack-policy schema must be defined before reward tuning**.

---

# 2. Design objective for work ordering

Minimize total expected rework.

For each system, ask:

```text
What upstream truth does this system consume?
What downstream system consumes its output?
Which values can remain parameters?
Which semantics must be fixed before the next layer can be trusted?
```

Three kinds of dependency are distinguished.

## 2.1 Semantic dependency
A downstream system cannot be interpreted until an upstream rule is known.

Example:
- star reward value cannot be evaluated if star calculation itself is ambiguous.

These should be closed early.

## 2.2 Numerical dependency
A downstream number depends on measured upstream behavior.

Example:
- achievement reward strength depends on the observed class soft-wall gap.

These values should be delayed.

## 2.3 Feedback dependency
A and B influence each other.

Example:
- shop damage changes kill speed;
- kill speed changes timing-event count;
- timing-event count changes EXP and skill reach;
- skill unlock changes damage again.

These are not solved by arbitrary ordering. They require a bounded convergence loop.

---

# 3. State-domain hierarchy — must be explicit before synthetic Tier work

The simulation and later runtime should distinguish at least five state domains.

## D0 — AccountPermanentState
Persists across all attempts.

Candidate contents:
- class Tier records;
- bestStars[class][tier];
- GlobalStarTotal derived/cache;
- broad star permanent modifiers;
- achievement completion records;
- targeted account/class permanent modifiers;
- unlocked titles;
- Tier unlock records.

## D1 — TierAttemptState / RunState
Reset when a new Tier attempt begins.

Confirmed direction:
- level starts at 1;
- EXP resets;
- run coin resets;
- run shop upgrades reset.

Must contain or explicitly reference:
- current Stage;
- base/wall HP state;
- combo;
- charge/heavy state;
- current level/EXP;
- coin;
- shop ranks;
- run mode / selected class;
- deterministic RNG state or replay identifiers.

## D2 — StageState
Reset/initialized at each Stage.

Examples:
- Stage intro/combat state;
- Stage encounter clock;
- current enemy set;
- Stage-local counters;
- Stage completion/failure event.

## D3 — Encounter/TurnState
Short-lived combat state.

Examples:
- current target/target availability;
- timing-square phase;
- Heavy X/Y phase;
- monster capability state;
- no-target/turnover state.

## D4 — Session/RoomState
Networking/reconnect state.

Examples:
- participants/slots;
- host authority;
- human/AI composition;
- reconnect identity;
- synchronized shop READY/NEXT.

### Required unresolved lifecycle decisions before multi-stage calibration

The following must not be silently assumed:
- exact base HP persistence/recovery policy across Stage/shop;
- charge persistence across Stage/shop;
- whether any Stage transition restores objective HP;
- shop healing semantics, if any;
- coin reward timing and ownership in SOLO/AI/TEAM;
- Tier-attempt failure/end semantics for reconnect;
- whether a Stage restart is a new attempt or an intra-attempt retry if such a feature exists.

Known current rule:
- combo survives Stage/shop/target-wait downtime unless a non-PERFECT timing judgment breaks it.

These lifecycle rules are **structural prerequisites** to a meaningful synthetic Tier.

---

# 4. Modifier evaluation pipeline — semantics before values

Before permanent reward values or shop values are tuned, the project needs one authoritative modifier pipeline.

Candidate conceptual order:

```text
1. Base class / weapon / objective stats
2. Account-wide permanent modifiers from stars
3. Target-class / account achievement modifiers
4. Tier-attempt entry-power snapshot
5. Run-local shop upgrades
6. Run level / unlocked class skill modifiers
7. Timing judgment / Heavy / P×P / combo / crit effects
8. Monster mitigation / armor / role-state interaction
9. Wall/base incoming-damage modifiers and shields
10. Final damage/control/objective result
```

This is a semantic ordering proposal, not a numeric freeze.

Required schema fields for every modifier source:
- `statId`
- `scope` (`ACCOUNT`, `CLASS`, `RUN`, `TEMPORARY`, etc.)
- `operation`
- `value`
- `stackPolicy`
- `sourceId`
- `version`

Rules:
- do not allow implicit multiplication simply because two systems both say `+X%`;
- title equip should remain cosmetic by default to avoid another hidden power state;
- stored permanent values and derived effective power must be separable;
- any multiplicative family needs an explicit cap/budget or sensitivity evidence.

The exact additive/multiplicative policy remains open, but **implicit operation order is not allowed**.

---

# 5. Critical feedback loops and how to break them safely

## L1 — Encounter pressure ↔ skill power

```text
encounter pressure
 -> attack count / duration
 -> EXP
 -> skill reach
 -> damage/control
 -> encounter pressure outcome
```

Method:
1. calibrate a provisional skill curve on a bounded run skeleton;
2. introduce additional power systems;
3. re-check skill-reach percentiles;
4. do not patch monster HP merely to hide a skill-reach defect.

## L2 — Shop power ↔ EXP

```text
shop damage/control
 -> fewer/more timing events
 -> EXP pace
 -> skill unlock timing
 -> further power
```

Method:
- compare multiple shop policies on paired seeds;
- require the skill reach-band to remain structurally acceptable across intended shop strategies;
- if not, classify whether the defect belongs to EXP design or shop leverage.

## L3 — Permanent power ↔ run-level curve

```text
stars/achievements
 -> higher entry power
 -> faster kills
 -> changed EXP opportunity
 -> shifted Lv milestones
```

Method:
- re-run Lv6/11/16/21/26/31 reach metrics for P0/P1/P2/P3 meta states;
- permanent growth must not accidentally make Lv31 consistently arrive too late because there are too few timing events.

## L4 — Stars ↔ difficulty snowball

```text
stars
 -> broad power
 -> easier later clears
 -> more stars
 -> more power
```

Method:
- star reward strength is derived from observed soft-wall movement, not chosen independently;
- evaluate first-class vs later-class power gap and route acceleration.

## L5 — Achievements ↔ class viability

```text
class soft wall
 -> achievement edge
 -> target-class power
 -> wall removal
```

Method:
- do not author exact sourceClass→targetClass stat/value before the soft-wall map and stat sensitivity matrix exist;
- no achievement may become a hidden mandatory key.

## L6 — Multiplayer ↔ progression economy

```text
more humans / AI
 -> different clear probability
 -> stars/achievements faster or slower
 -> permanent power
 -> future team/solo difficulty
```

Method:
- first stabilize multiplayer combat scaling with progression rewards abstracted;
- then run progression-credit/exploit audits before final permanent values freeze.

## L7 — Tier count ↔ permanent ladder length

```text
launch Tier count
 -> max stars
 -> star milestone count
 -> total permanent power
 -> later Tier difficulty
```

Method:
- Model A T1–T4 remains the bounded systems laboratory;
- use parameterized/normalized star-power envelopes before final Tier count;
- do not freeze the final absolute star milestone ladder until launch Tier count is explicitly decided.

---

# 6. Revised dependency DAG

```text
A. Frozen product/combat invariants
   + monster/class role contracts
   + provisional SKILLED_V2_CENTRAL design prior
                         |
                         v
B. RUN-STATE LIFECYCLE + MODIFIER PIPELINE CONTRACT
                         |
                         v
C. 10-STAGE PERSISTENT RUN KERNEL
   no permanent meta, no final shop tuning, no final boss, solo first
                         |
                         v
D. EXP / LEVEL / SKILL REACH CANDIDATE
   resolve enough Lv11–31 authority for 50-stage calibration
                         |
                         v
E. RUN COIN / SHOP CANDIDATE
   + shop policy agents
                         |
                         v
F. JOINT RUN-POWER CONVERGENCE
   encounter <-> EXP/skill <-> shop
                         |
                         v
G. BOSS/CHECKPOINT MECHANICAL PROXY
   enough to represent Stage10/30/50 pressure/economy
                         |
                         v
H. SOLO P0 50-STAGE FULL-TIER BASELINE
   5 classes x mastery profiles x seeds
                         |
                         v
I. SOFT-WALL MAP + STAT SENSITIVITY + TIER-UNLOCK SENSITIVITY
                         |
               +---------+---------+
               |                   |
               v                   v
J. MULTIPLAYER COMBAT       K. STAR REWARD ENVELOPE
   SCALING BASELINE            stars-only recovery
               |                   |
               +---------+---------+
                         v
L. ACHIEVEMENT REWARD GRAPH CANDIDATE
   after soft-wall + star + SOLO/TEAM semantics
                         |
                         v
M. ACCOUNT PROGRESSION / ROUTE SIM
   first-class / balanced / favorite / recovery / mastery / team routes
                         |
                         v
N. LAUNCH TIER-COUNT + TIER-UNLOCK DECISION GATE
                         |
                         v
O. EXACT CAMPAIGN/BOSS AUTHORING + FINAL RUN ECONOMY RECHECK
                         |
                         v
P. MULTIPLAYER PROGRESSION-CREDIT / EXPLOIT AUDIT
                         |
                         v
Q. FULL-SYSTEM STRESS + NUMERICAL FREEZE
                         |
                         v
R. PRODUCTION IMPLEMENTATION
```

This DAG is progressive deepening, not a one-pass waterfall.
Each downstream layer may reopen only the smallest relevant upstream candidate, not the whole project.

---

# 7. Work packages and exact order

## P0 — Current foundation closure

Status: **substantially complete**.

Includes:
- class roles;
- monster capabilities;
- role-expression contract;
- representative all-20 encounter library;
- current central skilled design prior;
- central all-20 540/540 structural PASS;
- historical 540/540 regression retained.

Not equivalent to full game balance.

Exit condition:
- no representative-role blocker to multi-stage work.

Current evidence: satisfied with watches.

---

## P1 — Run-State Lifecycle Contract

Goal:
remove ambiguity before connecting Stages.

Decisions/contracts:
- Tier-attempt reset boundary;
- Stage transition state transfer;
- base HP persistence/recovery;
- combo persistence;
- charge persistence;
- EXP/level persistence;
- coin/shop persistence;
- failure/end semantics;
- reconnect restoration boundary.

No balance tuning.

Exit:
- every field has `reset / persist / derive / authoritative-owner` semantics.

---

## P2 — Modifier Pipeline & Power Attribution Contract

Goal:
prevent hidden stacking and later rewrite.

Define:
- source scopes;
- operation order;
- stack policy schema;
- class-specific stat sensitivity measurement interface;
- effective-power snapshot/debug telemetry.

Do not freeze reward magnitudes.

Exit:
- a damage/control/wall event can explain which modifier sources produced it.

---

## P3 — 10-Stage Persistent Run Kernel

Goal:
validate persistence/state transitions before economy/meta coupling.

Initial exclusions:
- permanent star/achievement power OFF;
- final shop calibration OFF;
- boss unique novelty OFF;
- multiplayer OFF;
- exact launch-stage authoring OFF.

Include:
- persistent base HP according to P1;
- combo/charge according to P1;
- Stage intro/combat/clear/fail transitions;
- deterministic replay;
- provisional EXP/level state sufficient to test Lv6 timing.

Why 10 first:
- cheaper to debug lifecycle errors than 50-stage simulation;
- still crosses Lv6 target band and a checkpoint slot.

Exit:
- deterministic state continuity;
- no state leakage/reset ambiguity;
- failure semantics work;
- all five classes can run through the slice.

---

## P4 — Full Player-Power Spine Candidate

Goal:
calibrate EXP/level/skill reach before shop is allowed to dominate the result.

Use a 50-stage **synthetic skeleton**, not exact 200-stage launch authoring.

Required:
- Lv6/11/16/21/26/31 mechanics have sufficient simulation authority/candidate representation;
- Lv31 target remains Stage41–45;
- other milestone windows are calibrated candidates;
- Stage46–49 supplies meaningful post-Lv31 usage;
- Stage50 is not the first meaningful Lv31 use.

First pass:
- shop neutral/off;
- P0 permanent state;
- solo.

This is a provisional curve, not final EXP freeze.

Exit:
- milestone distributions are interpretable and no skill window is structurally compressed.

---

## P5 — Run Coin / Shop Candidate

Goal:
introduce within-run choice only after the basic level curve exists.

First decide structurally:
- shop cadence candidate(s): every-stage vs checkpoint vs selected-stage/fast-continue;
- coin award sources/timing;
- upgrade categories;
- purchase caps/ranks;
- wall HP/DEF semantics;
- AI/human ownership deferred where multiplayer-specific.

Then simulate strategy agents:
- ATTACK_HEAVY;
- CRIT_HEAVY;
- DEFENSE_HEAVY;
- BALANCED;
- SAVE/DELAY;
- role-aware candidate.

Do not tune only against one shop policy.

Exit:
- no single trivial dominant shop strategy under the bounded test set;
- shop does not create immediate runaway;
- data exposes coin earned/spent/unused and power contribution.

---

## P6 — Joint Run-Power Convergence Loop

Goal:
solve the first true coupled loop.

Repeat with paired deterministic seeds:

```text
EXP/skill candidate
 -> shop candidate
 -> Stage pressure
 -> resulting event count
 -> revised skill reach
```

Metrics:
- skill milestone P25/P50/P75/P90 by class/shop policy;
- timing-event count;
- coin income/spend;
- wall HP trajectory;
- clear/fail slope around skill unlocks;
- shop leverage by class;
- combo40 opportunity over persistent run.

Guardrails:
- do not fix late skill reach by blindly lowering monster HP;
- do not fix shop snowball by silently weakening player judgment model;
- classify cause first.

Exit:
- run-local power curve is stable enough that adding boss proxy does not require redesigning core progression.

---

## P7 — Boss / Checkpoint Mechanical Proxy

Goal:
represent boss/checkpoint impact before full-Tier outcome and star calibration.

Not final art/design.

Use current novelty contract:
- Stage10 checkpoint, boss optional;
- around Stage30 signature preview if needed;
- Stage50 Tier Final candidate;
- no unpreviewed mandatory unique grammar;
- T4 boss-only novelty LOW by default.

Important:
- boss mechanics can alter EXP opportunity and 3-star probability;
- therefore permanent reward values must not be frozen before this layer is represented.

The later user idea `weak-point exposure = faster line + much larger PERFECT region + short multihit reward window` remains **parked future boss-mechanic candidate**, not part of current baseline unless explicitly admitted later.

Exit:
- representative final/checkpoint pressure exists without novelty overload.

---

## P8 — Solo P0 Full-Tier Baseline

Goal:
establish the real fresh-account difficulty surface.

Configuration:
- 5 classes;
- P0 FRESH permanent state;
- run-local EXP/skills/shop ON;
- boss/checkpoint proxy ON as required;
- SOLO first;
- multiple deterministic sequence seeds;
- `SKILLED_V2_CENTRAL` design-prior profile plus bounding profiles.

Outputs:
- full-clear probability;
- fail Stage histogram;
- 0/1/2/3-star distribution;
- wall HP trajectory;
- skill reach;
- coin/shop state;
- class opportunity;
- combo40 reach/survival;
- retry pressure.

Difficulty authority:
- non-T1 central full clear normally `<60%` upper bound;
- T1 exception allowed;
- ordinary difficulty should not be mostly Stage1–19 0-star failures.

Exit:
- 5-class P0 soft-wall locations are measurable.

---

## P9 — Soft-Wall Map + Stat Sensitivity Matrix

Goal:
measure what kind of permanent help is actually needed before designing rewards.

For each class/Tier wall, measure marginal response to candidate stat families:
- attack;
- crit chance;
- crit damage;
- wall HP;
- defense;
- knockback/control;
- selected class-specific derived modifiers.

Measure not merely raw DPS, but:
- delta fail Stage;
- delta 1/2/3-star probability;
- delta wall damage;
- delta skill reach;
- delta role expression;
- class-specific efficiency.

This avoids assuming `+1%` has equal value across classes.

Tier unlock:
- run `CLEAR_LOCK` as first hypothesis;
- compare alternatives only if lane deadlock appears.

Exit:
- enough sensitivity evidence exists to size stars and achievements as bridges instead of arbitrary buffs.

---

## P10 — Multiplayer Combat Scaling Baseline

Goal:
stabilize combat scaling before progression rewards are finalized.

Prerequisite:
- solo P0 run-local system stable.

Separate from progression-credit rules.

Test:
- 2P / 3P / 4P;
- AI/human composition as needed;
- class combinations and duplicate classes;
- shop ownership/cadence candidates;
- wall pressure;
- specialist starvation;
- readability/entity budget.

Scaling priority remains:
1. event budget;
2. composition;
3. specialist count;
4. cadence/overlap;
5. limited durability changes.

Do not start with blanket HP inflation.

Exit:
- team-size combat no longer saturates trivially under intended pressure;
- role identities survive.

---

## P11 — Stars-Only Permanent Progression Candidate

Goal:
size broad account growth from observed wall gaps.

Input:
- P8 soft-wall distributions;
- P9 stat sensitivity;
- P10 multiplayer acquisition-rate constraints;
- current Tier-count candidate, still not necessarily final.

Principle:
- stars move a wall;
- stars do not skip whole Tier bands;
- broad power remains broad, predictable and non-consumable.

Run profiles:
- P0 FRESH;
- P1 BALANCED;
- P2 STAR_GROWN.

Mandatory re-check:
- Lv milestone reach under stronger entry power;
- first-class vs later-class difficulty;
- snowball rate;
- team-earned star acceleration.

Do not freeze absolute milestone list until launch Tier count is decided.

Exit:
- stars-only recovery works without runaway.

---

## P12 — Achievement / Cross-Class Reward Graph Candidate

Goal:
add targeted bridges only after stars-only behavior is understood.

Inputs:
- class soft-wall map;
- star recovery result;
- stat sensitivity matrix;
- SOLO/AI/TEAM semantics from multiplayer baseline;
- achievement truth contract.

Author:
- achievement family/list candidate;
- sourceClass → targetClass/account edges;
- stat family;
- provisional value;
- stack policy.

Guardrails:
- no circular deadlock;
- no mandatory achievement trap;
- no source-class self-snowball by default;
- solo mastery reward must not make TEAM/AI progression invalid;
- titles cosmetic by default.

Exit:
- targeted bridges solve actual measured gaps rather than invented ones.

---

## P13 — Account Progression / Route Simulation

Goal:
validate the coupled long-term progression engine.

Required routes:
- FIRST_CLASS;
- BALANCED_FIVE_CLASS;
- STAR_STACKED;
- FAVORITE_CLASS_FIRST;
- WEAK_CLASS_RECOVERY;
- ACHIEVEMENT_FOCUSED_SOLO;
- TEAM_ASSISTED;
- HIGH_MASTERY.

Outputs:
- class clear order;
- attempts and total Stage-play volume;
- stars over time;
- achievement unlock order;
- soft-wall recovery events;
- power over time;
- dominant route;
- deadlock;
- snowball;
- first-class vs fifth-class gap.

Acceptance:
- at least several rational routes remain viable;
- no single route is overwhelmingly dominant across ordinary profiles;
- blocked class can recover through intended cross-class progression;
- recovery does not become automatic trivialization.

---

## P14 — Launch Tier Count / Tier Unlock Decision Gate

Goal:
make decisions that were intentionally delayed until volume evidence exists.

Evaluate:
- 4 vs 5 vs 6 initial Tier launch volume;
- expected attempts and Stage-play time;
- max-star ladder length;
- novelty availability;
- future expansion room;
- cross-class grind burden;
- unlock deadlock/skip risk.

Only after this gate can the final absolute star milestone ladder and achievement content volume be frozen.

---

## P15 — Exact Campaign & Boss Authoring

Goal:
turn stable system envelopes into exact content.

Now author:
- exact per-Stage encounter schedule;
- exact monster frequency within approved envelopes;
- checkpoint/boss placement;
- boss signatures and earlier previews;
- final shop cadence;
- Tier finals;
- final novelty distribution.

Why late:
- exact authoring done earlier would be repeatedly invalidated by skill/shop/meta changes.

After authoring, rerun P8–P13 critical metrics, not the whole design process from zero.

---

## P16 — Multiplayer Progression-Credit / Exploit Audit

Goal:
connect combat multiplayer to permanent progression only after both sides exist.

Decide/validate:
- Tier eligibility;
- host/member Tier rule;
- star credit;
- selected-class credit;
- AI fill treatment;
- carry/exploit resistance;
- shop ownership;
- TEAM vs SOLO reward parity philosophy;
- SOLO_NO_AI achievement exclusion/inclusion truth.

Run route simulation again with team-assisted paths.

Exit:
- multiplayer does not create a progression bypass or force solo play.

---

## P17 — Full-System Stress / Numerical Freeze Gate

Full system:

```text
combat
+ encounter authoring
+ base HP
+ combo/heavy
+ EXP/level/skills
+ coin/shop
+ boss/checkpoints
+ stars
+ permanent stats
+ achievements
+ Tier unlock
+ multiplayer/AI progression rules
```

Stress axes:
- learning / average / skilled / high mastery;
- all five classes;
- P0/P1/P2/P3/overgrown;
- multiple shop strategies;
- solo/team/AI modes;
- first/favorite/balanced/recovery routes;
- adverse RNG seeds;
- stacking extremes.

Required defect checks:
- hard class lockout;
- shop snowball;
- permanent-stat snowball;
- achievement deadlock;
- dominant class-order route;
- multiplayer carry exploit;
- skill-reach inversion under high power;
- boss novelty overload;
- late-Tier trivialization;
- excessive early 0-star grind.

Only after this gate should exact numerical values be candidates for production freeze.

---

## P18 — Production implementation

Production implementation follows frozen contracts/values.

Rules:
- planning simulation never silently rewrites production;
- production source remains isolated until explicit authorization;
- every implementation slice receives a bounded contract and regression list;
- implementation convenience cannot redefine campaign semantics.

---

# 8. Two-stage freeze policy

To reduce rework, distinguish two freeze levels.

## Freeze A — Structural/Semantic Freeze
Can occur early.

Examples:
- state reset/persist rules;
- star outcome rule;
- class/Tier record meaning;
- modifier stack schema;
- achievement truth condition format;
- role-expression contracts;
- authoring field semantics.

These should be stable before numerical calibration.

## Freeze B — Numerical/Content Freeze
Must occur late.

Examples:
- exact EXP formula;
- exact shop price/value curve;
- exact permanent star values;
- exact achievement rewards;
- production monster HP/speed/coordinates;
- exact boss values;
- exact 200-stage schedule;
- multiplayer scaling coefficients.

Freeze B requires coupled-system evidence.

---

# 9. Complexity-control rules

## 9.1 Do not run full factorial matrices at every phase

Use progressive matrix expansion.

Early phase:
- central profile;
- five classes;
- a few deterministic seeds;
- baseline + extreme shop/meta policies.

Expand a dimension only when it materially affects the gate.

Full cross-system stress is reserved for P17.

## 9.2 Use paired deterministic seeds for candidate comparisons

When comparing:
- EXP curves;
- shop policies;
- reward values;
- encounter edits;

use the same scenario seeds where possible.
This reduces noise and makes attribution clearer.

## 9.3 Tune one semantic cause at a time

Examples:
- `skill reach late` does not authorize global monster HP reduction;
- `wall damage high` does not authorize universal base HP inflation;
- `achievement route deadlock` does not authorize arbitrary Tier unlock weakening.

First classify the causal layer.

## 9.4 Candidate values remain parameterized

A downstream simulator should consume explicit versioned parameters instead of copying constants into code.

## 9.5 Exact content authoring is delayed

Use representative recipes and synthetic Tier skeletons until the system envelopes converge.
Exact 200-stage authoring is a late content task, not a prerequisite to system calibration.

---

# 10. Recommended simulation matrix progression

## M1 — Run kernel
- 5 classes
- central sequence + small bounding seeds
- P0
- shop OFF
- solo
- 10 stages

## M2 — Skill spine
- 5 classes
- central/conservative/strong candidates as available
- P0
- shop OFF
- solo
- 50-stage synthetic skeleton

## M3 — Shop convergence
- M2 dimensions
- multiple shop policies
- paired seeds

## M4 — P0 full-Tier difficulty
- 5 classes
- mastery profiles
- shop policies reduced to representative policies
- boss proxy ON

## M5 — Meta sensitivity
- P0/P1/P2/P3
- stat perturbation grid
- selected classes/Tiers first, then expand

## M6 — Multiplayer combat
- 2/3/4P representative compositions
- shop ownership/cadence candidates
- no permanent reward credit yet

## M7 — Account routes
- route agents across classes/Tiers
- stars/achievements ON
- solo first, then team-assisted

## M8 — Full-system freeze
- broad stress matrix and adverse seeds

---

# 11. Current-corpus inconsistencies / stale boundaries found in this review

## C1 — `PROJECT_STATUS.md` and `NEXT_WORK.md`
They still describe the isolated calibration deployment/pilot as the active phase.
That boundary has been superseded by docs 66–69 and the central all-20 execution.

## C2 — corpus `README.md`
Its status/pipeline still says the critical role-expression rerun is next.
That work is already complete.

## C3 — old simulation execution order
`06_SIMULATION_CALIBRATION_PLAN.md` correctly places synthetic/full Tier before meta recovery, but does not explicitly separate:
- run-state lifecycle;
- EXP/skill calibration;
- shop calibration;
- joint run-power convergence.

## C4 — coarse boss/multiplayer placement
The older master graph groups run economy, boss and multiplayer too broadly.
This review splits them into:
- boss/checkpoint proxy before full-Tier outcome calibration;
- multiplayer combat scaling after stable solo run-local systems;
- multiplayer progression-credit after meta candidates exist.

These are planning refinements, not contradictions to the product premise.

---

# 12. Exact current next boundary after doc 69

Do **not** jump directly into a 10-stage simulator with undefined state semantics.

Next work is:

```text
P1 Run-State Lifecycle Contract
        +
P2 Modifier Pipeline / Power Attribution Contract
```

Then:

```text
P3 10-Stage Persistent Run Kernel
```

The first 10-stage slice is therefore a **state/persistence integration slice**, not yet a full economy/meta balance test.

Specifically it should not include:
- permanent star values;
- achievement reward values;
- final shop curve;
- final boss mechanics;
- multiplayer progression credit.

It should include enough persistent state to prove that later systems can be layered without changing the meaning of a run.

---

# 13. High-risk decisions to resolve earliest

Before P3 implementation, explicitly decide or parameterize:

1. base HP persistence/recovery between Stages;
2. charge persistence between Stage/shop transitions;
3. exact Tier-attempt failure/end boundary;
4. modifier operation/stack ordering;
5. shop cadence candidates to be tested later;
6. skill authority plan for Lv11–31 before full 50-stage calibration;
7. deterministic run-state/version/hash contract.

Do not yet decide exact reward magnitudes.

---

# 14. Final structural principle

The project should not attempt to balance every subsystem independently and then add them together.

The intended method is:

```text
freeze meaning
 -> isolate one power loop
 -> measure
 -> add the next coupled system
 -> re-measure upstream invariants
 -> keep only stable interactions
 -> author exact content late
 -> freeze numbers only after full-system stress
```

The primary invariant is not that every intermediate candidate remains unchanged.
The invariant is that each change has a known cause, bounded dependency set and deterministic evidence.

This is the execution model for subsequent Timing Defense system design unless explicitly superseded.
