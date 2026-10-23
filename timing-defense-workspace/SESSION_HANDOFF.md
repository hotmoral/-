# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## 0. Recovery rule — mandatory

Always fetch live remote first.
Do not reconstruct current state from chat, memory, copied SHA, or one old handoff paragraph.

The user must **not** have to re-explain the project reasoning method in a new session.
A new session must recover both:
1. the current factual/project state; and
2. the **way the project must be reasoned about**.

Live remote always wins.

---

# 1. Mandatory read/check order

1. live `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`
5. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
6. `CHARACTER_PROFILE_RADAR_V1.md`
7. `legacy-game-structure/data/system_dependency_calibration_order_v0_30.yaml`
8. `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
9. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
10. `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
11. `legacy-game-structure/79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
12. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
13. `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
14. `legacy-game-structure/135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
15. `legacy-game-structure/137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
16. `legacy-game-structure/139_P5_STAGE48_SIEGER_PROTECTION_TIME_DIAGNOSTIC_V0_1.md`
17. current production/harness heads
18. only then read additional active source/runner files needed for the exact next diagnostic

For broad structural recovery in a genuinely new session, also recover the structural spine from:
- `legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
- `legacy-game-structure/01_META_PROGRESSION.md`
- `legacy-game-structure/02_TIER_SYSTEM.md`
- `legacy-game-structure/03_STAGE_STRUCTURE_50.md`
- `legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`
- `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
- `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`
- `legacy-game-structure/15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`

Do not re-run closed P1/P2/P3/P4 or the full class-identity group just because a new chat started.

---

# 2. Mandatory reasoning process for every new session

Before touching the current micro-task, reconstruct this whole-system frame:

```text
Tier / Stage purpose
-> content novelty / monster role
-> class identity / skills
-> run-state persistence
-> shop/economy growth
-> attack count / EXP / skill-reach feedback
-> encounter chronology / frontmost geometry
-> wall pressure / SIEGER exposure
-> STAGE_SETTLED
-> persistent wall deficit into later Stages
-> downstream P6 / later progression impact
```

Then classify the current problem before changing anything:

```text
source/simulator fidelity?
lifecycle/state semantics?
encounter geometry/chronology/frontmost ordering?
class/package semantics?
shop/feedback interaction?
exact numerical balance?
```

Default repair order:

```text
fidelity
-> lifecycle/state
-> geometry/chronology
-> package/class semantics
-> shop/feedback
-> numerical scalar last
```

Use the **smallest bounded diagnostic that can distinguish the cause**.
Do not use “deep review” as an excuse for unnecessary full-project repetition.

At every material slice, check:
- upstream invariants;
- downstream consumers;
- feedback loops;
- class identity/fairness;
- deterministic attribution;
- scope/cost;
- authority level;
- production boundary;
- whether handoff must be synchronized.

---

# 3. Important-decision approval rule — mandatory

The user explicitly requires:

> Important design/content/numerical decisions must not be applied immediately. Analyze first, explain simply, and obtain user approval before adoption.

This includes at minimum:
- adopting a Stage48/49 packet as the working direction;
- changing Stage cadence as a working design;
- changing class/monster/shop/EXP values;
- changing SIEGER windup or escort durability;
- selecting the Tank damage coefficient;
- changing approved structural contracts;
- production gameplay changes.

Diagnostic/instrumentation work may proceed without interrupting the user when it does not change game semantics.

Before requesting approval, provide enough analysis to explain:
- what decision is actually needed;
- why now;
- evidence;
- constraints;
- alternatives/tradeoffs;
- recommendation;
- risks/reversibility;
- what remains open.

---

# 4. Communication rule — mandatory

Explain findings in **easy Korean first**.

Use this causal order where possible:

```text
무엇이 문제인가
-> 왜 그런가
-> 그래서 다음에 무엇을 확인하는가
-> 무엇은 아직 결정/적용하지 않았는가
```

Technical details may follow, but do not make the user reconstruct the meaning from raw numbers or code terminology.

---

# 5. Branch checkpoints

Planning/canonical:
- branch `timing-defense-workspace`
- always fetch exact live HEAD at session start/end
- never treat the SHA in this file as permanent truth

Production:
- branch `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized

Calibration harness:
- branch `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- unchanged by current P5 planning work

Temporary diagnostic branch used in the latest Stage48 investigation:
- `timing-defense-workspace-temp-check`
- latest diagnostic branch state has **no planning or production authority**
- do not promote temporary scripts/workflows automatically

---

# 6. Current exact phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE / STAGE_SETTLED authority
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 = USER_APPROVED
P5 class identity group = DIRECTIONALLY CLOSED
P5 integrated runner = CHECKOUT-EXACT PASS / DETERMINISTIC
P5 60s backlog-discard model = INVALID for Stage-clear reserve
P5 Stage46-49 interpretation = STAGE_SETTLED REQUIRED
P5 current Stage48 proxy packet = NOT ADMISSION-READY
P5 simple real-monster substitution = INSUFFICIENT
P5 real-monster SIEGER windup/shot result = ZERO in tested chronology families
P5 current root cause = PROTECTED TRAVEL TIME SHORTFALL BEFORE SIEGE LINE
P5 next = LAYERED FRONTMOST-HANDOFF TIMELINE BOUNDED DIAGNOSTIC
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
```

No Stage48 packet is approved.
No Stage48 cadence change is approved.
No SIEGER/escort stat change is approved.
No Tank scalar is selected.
No numerical value is frozen.

---

# 7. Stable P5 truths that must remain in mind

## P5 A2 shop

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
PERSONAL WALLETS
KILLER_ONLY PERSONAL ordinary-monster coin baseline
ALL-HUMAN Stage-clear income-floor candidate
FORTIFICATION = max HP + matched current increase
ATK/CRIT/CRITDMG/KNOCK personal
FORTIFICATION/DEF purchases contribute to shared wall
six categories retained
NO_ROUTINE FULL-SHOP MAXOUT BY STAGE49
```

Diagnostic-only centers:

```text
full-shop Rank10 reference = 16360
spend capacity center = 50%
income source center = 70/30
cross-class ATK/FORT/DEF diagnostic magnitude = 40% legacy-relative
```

Do not reinterpret these as production values or an approved Stage-by-Stage purchase history.

## Stage transition

```text
last authored spawn
+ zero live Stage-owned enemy
+ authorized action/effect drained
+ no unresolved half-Heavy/delayed Stage transient
= STAGE_SETTLED
-> Stage clear / shop
-> reset Stage-local enemy/transient state
-> next Stage
```

Persistent current/max wall HP and absolute damage deficit carry forward.
Stage-local enemy instances do not.

Both are wrong:

```text
60s -> delete live enemies -> next Stage
60s -> carry live enemies directly into next Stage
```

---

# 8. Class-identity guards — do not casually reopen

Radar:

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

Rules:
- high axes must remain real causes of success;
- low axes must remain real limitations after growth;
- `SURVIVAL != CLEAR`;
- Tank solo parity is not required;
- no hard class lockout.

Targeted regressions already passed:

```text
Knight aligned < dispersed
Archer aligned < scatter
Mage cluster < distributed
Tank .20 clear slower than .25, slower than .30
```

Tank `.20/.25/.30` remain diagnostic only; `.25` is only a working center.
Rogue one-dagger ordinary-cleanup breakpoint remains a HIGH watch.
Do not remove deterministic retarget first.
Do not globally nerf Archer or buff Mage to fix Stage48.

---

# 9. Exact Stage48 evidence recovered so far

## 9.1 Proxy contamination

The old repeated Stage48 packet used Knight-only `ARMORED_DURABLE_PROXY` as generic escort.
That caused proxy-threshold pressure, especially against Mage/Tank, rather than clean escorted-SIEGER role pressure.

Therefore the packet is not admission-ready.

## 9.2 Real-monster substitution

Simple BRUTE / SHIELD / mix replacements became nearly harmless and still gave SIEGER zero meaningful role uptime.

## 9.3 Corrected death-position diagnostic

Temporary run:

```text
run id 39954298666
```

Physical/diagnostic anchors:

```text
SIEGER spawnX = 0.92
provisional speed = 0.045
siege threshold = 0.38
straight travel budget to threshold ~= 12.0 s
```

Across tested real-monster screen families:

```text
windups = 0
shots = 0
```

Best observed real-monster SIEGER death X:

```text
Knight ~0.7389
Rogue  ~0.7287
Tank   ~0.4451
Archer ~0.7209
Mage   ~0.7929
```

The contaminated proxy packet allowed Mage-side SIEGER to reach `x=0.38`, producing 3 windups and 1 shot, while the same proxy structure overpressured/buried Mage.

Current causal classification:

```text
REAL_MONSTER_STAGE48_FAILURE
= insufficient protected travel time before SIEGER exposure/death
NOT primarily windup duration
```

Therefore current evidence does **not** justify:
- SIEGER windup change;
- SIEGER HP increase;
- generic escort HP inflation;
- Mage buff;
- Archer/Rogue/Knight nerf;
- Tank scalar selection.

---

# 10. Exact next boundary

Do **not** brute-force a large timing/stat grid.

Next bounded diagnostic question:

> Can existing real monsters create enough SIEGER protection time through **sequential frontmost handoff / layered pulse chronology** while keeping all enemies at the normal right edge and keeping stats unchanged?

Measure directly:

```text
SIEGER spawn time
SIEGER x/time trajectory
SIEGER death / first-windup / first-shot time
frontmost owner timeline
live bodies physically ahead of SIEGER
screen-handoff gaps
SIEGER effective-exposure time
wall-contact source split
class-specific chronology differences
```

Use a few deliberately chosen chronology families, not a broad combinatorial search.

Keep fixed for this diagnostic:

```text
spawnX 0.92
existing real monster stats
current class numerics
current diagnostic shop scale
Tank control package
Rogue deterministic retarget
STAGE_SETTLED lifecycle
```

If a promising diagnostic family appears:
1. replay Stage46→49 with carried wall deficit and STAGE_SETTLED;
2. check Stage46 revelation / Stage47 recovery / Stage48 role pulse / Stage49 escalation;
3. check all five class identities and shop breakpoints;
4. prepare a simple decision packet;
5. **ask the user before adopting the Stage48 working direction or any important numerical/content change.**

Only after user approval:
- refine Stage49 chronology;
- later select Tank scalar on uncontaminated evidence;
- continue KNOCK / CRIT / CRITDMG / real shop acquisition timing / EXP feedback / P10/P10R.

---

# 11. Session-close quality gate

Before handing off to a new session, verify:

```text
1. Did live canonical HEAD get re-fetched?
2. Did we change only evidence, or also semantics/values/order?
3. Did any approved upstream invariant become inconsistent?
4. Did a WATCH become blocker/resolved?
5. What downstream recheck became necessary?
6. Did production remain unchanged unless explicitly authorized?
7. Are PROJECT_STATUS / NEXT_WORK / SESSION_HANDOFF / dependency plan synchronized?
8. Can the next session understand the whole reasoning method without the user explaining it again?
9. Can the next session explain the situation in simple Korean before technical detail?
10. Will the next session ask for user approval before adopting important decisions?
```

If 8–10 are not satisfied, the handoff is incomplete.
