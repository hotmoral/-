# Timing Defense — Tier Structure & Monster Availability Candidate Review V0.1

Date: 2026-10-24 KST  
Status: **CANDIDATE REVIEW COMPLETE / USER DECISION REQUIRED / NO TIER OR ROSTER ADOPTION / NO PRODUCTION CHANGE**

Depends on:
- `02_TIER_SYSTEM.md`
- `03_STAGE_STRUCTURE_50.md`
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `19_MODEL_A_B_CLASS_ROLE_AND_VOLUME_AUDIT_V0_1.md`
- `21_MODEL_A_NOVELTY_BUDGET_AND_BOSS_PLACEHOLDERS_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `25_MODEL_A_META_PROGRESS_VOLUME_AND_SOFT_WALL_ENVELOPE_V0_1.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `151_P6_ENCOUNTER_FAMILY_ROTATION_AND_TANK_OBJECTIVE_ATTRIBUTION_RESULT_V0_1.md`
- `152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`
- `156_P6_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`

## 1. Purpose

P6 is now structurally closed with watches. The next question is not exact Stage authoring yet.

The required order is:

```text
Tier count
-> monster availability by Tier
-> introduction/unlock order
-> Tier1 roster constraints
-> only later exact Stage1-50 authoring
```

This review compares bounded candidates. It does not adopt one.

## 2. Constraints that every candidate must satisfy

1. One Tier remains 50 Stages.
2. T1 must not consume all nine current ordinary monsters.
3. Higher Tier(s) must provide new combat vocabulary rather than only larger numbers.
4. Current nine monsters are a mechanical foundation, not the final lifetime roster.
5. New special monsters need readable minimum role expression before full activation/counterplay.
6. Class strengths may rotate by encounter family; equal class clear rate is not a goal.
7. Tank must retain control/defense/objective-protection value; kill parity is not required.
8. Lv31 direction remains Stage41-45 with Stage46-49 as post-Lv31 mastery.
9. No new core ordinary capability should first appear in Stage41-50.
10. Non-T1 difficulty should generally keep intended-entry SKILLED_V2 full-Tier clear below 60%, but difficulty should not be created mainly by 0-star early failure.
11. Shop/EXP feedback remains outcome-conditioned; availability should not be fitted to an exact provisional EXP magnitude.
12. Exact Stage content remains downstream.

## 3. Candidate A — Compact 4-Tier launch

Availability shape:

```text
T1: GRUNT / RUNNER / BRUTE
T2: + SHIELD / FLYER
T3: + CHARGER / SPLITTER
T4: + SUPPORTER / SIEGER
T5+: future monster expansion
```

Novelty density:

```text
3 / 2 / 2 / 2
```

### Why it works

T1 covers three foundational questions:
- baseline reading;
- tempo/speed;
- durable frontline.

That is already enough to create five-class opportunity through formation/geometry:
- Rogue gets durable-target value from BRUTE;
- Tank gets control value against RUNNER/BRUTE;
- Archer can get line/penetration value from formation;
- Mage can get cluster/density value without needing a special monster;
- Knight keeps mixed/generalist value.

T2 then adds mitigation and vertical geometry.
T3 adds two stateful mechanics: telegraphed burst and death transformation.
T4 adds the most advanced formation/objective pair: SUPPORTER and SIEGER.

### Main risk

T4 has the highest learning-density risk because SUPPORTER and SIEGER are both backline/uptime/target-order sensitive.

Required guardrail:

```text
first half: SUPPORTER isolated teach/mix
second middle: SIEGER isolated teach/mix
31+: combined formation/objective pressure
41-50: mastery only, no first teach
```

### Campaign volume

```text
4 Tiers × 5 classes = 20 class×Tier records
successful Stage floor for one full clear each = 1000
max stars = 60
```

With non-T1 skilled full-clear below 60%, actual retry volume is already substantial.

### Classification

```text
PREFERRED CANDIDATE
WATCH = T4 learning density / SUPPORTER-SIEGER role-expression readability
```

This is the previously validated Model A direction, but it is not yet re-adopted as launch authority.

## 4. Candidate B — Split 5-Tier launch

Availability shape:

```text
T1: GRUNT / RUNNER / BRUTE
T2: + SHIELD / FLYER
T3: + CHARGER / SPLITTER
T4: + SUPPORTER
T5: + SIEGER
T6+: future expansion
```

Novelty density:

```text
3 / 2 / 2 / 1 / 1
```

### Benefits

- SUPPORTER and SIEGER each receive a full 50-Stage Tier for teaching and mastery.
- Formation-support and objective-siege identities become very clear.
- Lower risk that two advanced backline mechanics compete for teaching bandwidth.

### Costs

- Adds 250 successful class-stage clears before retries.
- Adds 15 maximum stars and extends permanent progression volume.
- T4 and T5 each have only one new ordinary monster, so 50 Stages must be justified by strong returning-monster reinterpretation, formation/cadence, boss or meta novelty.
- Risk of feeling like the old T4 was stretched into two Tiers rather than adding genuinely new content.

### Classification

```text
VALID FALLBACK
USE IF 4-TIER T4 LEARNING DENSITY OR READABILITY FAILS
```

No current P6 evidence requires this split.

## 5. Candidate C — Extended 6-Tier launch

A current-roster-only shape could be:

```text
T1: GRUNT / RUNNER / BRUTE
T2: + SHIELD / FLYER
T3: + CHARGER
T4: + SPLITTER
T5: + SUPPORTER
T6: + SIEGER
T7+: future expansion
```

Novelty density:

```text
3 / 2 / 1 / 1 / 1 / 1
```

### Benefits

- Maximum teaching separation.
- Every stateful/formation/objective mechanic can receive a very long isolated learning runway.
- Tier identities can be extremely explicit.

### Costs

```text
6 Tiers × 5 classes = 30 class×Tier records
successful Stage floor = 1500
max stars = 90
```

This creates major campaign and retry volume before counting failed attempts.
More importantly, four later Tiers would each introduce only one current ordinary monster.
Without additional approved monster/boss/meta content, novelty density becomes too thin and the campaign risks repetition/padding.
It also delays useful mixed interactions between mechanics that should eventually coexist.

### Classification

```text
STRUCTURALLY POSSIBLE
NOT RECOMMENDED FOR INITIAL LAUNCH WITH CURRENT EVIDENCE
REOPEN IF FUTURE MONSTER ROSTER OR META/BOSS CONTENT EXPANDS ENOUGH TO JUSTIFY IT
```

## 6. Tier1 roster constraint review

### Core-2 candidate: GRUNT / RUNNER

Pros:
- simplest onboarding.

Problems:
- no durable-body problem;
- Rogue durable execution identity receives weak early opportunity;
- Tank/knockback and penetration/AoE differences have less material surface;
- later Tier must absorb too much foundational durability teaching.

Classification: `TOO_NARROW AS CURRENT DEFAULT`.

### Core-3 candidate: GRUNT / RUNNER / BRUTE

Pros:
- baseline + tempo + durability gives three orthogonal foundational problems;
- existing class-role audit shows all five classes can receive meaningful opportunity with only these three, using formation/cadence/geometry rather than more monster types;
- leaves six current monsters for higher-Tier novelty;
- avoids advanced stateful/backline mechanics during onboarding.

Classification: `PREFERRED T1 ROSTER CANDIDATE`.

### Core-4 candidate: + SHIELD in T1

Pros:
- early mitigation contrast.

Problems:
- increases onboarding learning load while class skills are first being learned;
- consumes a strong T2 novelty asset;
- BRUTE already supplies the foundational durable-frontline lesson.

Classification: `NOT PREFERRED WITHOUT NEW EVIDENCE`.

## 7. Monster introduction-order logic

The strongest current structural order is:

```text
FOUNDATION
GRUNT / RUNNER / BRUTE

-> MITIGATION + GEOMETRY
SHIELD / FLYER

-> STATEFUL BURST + TRANSFORMATION
CHARGER / SPLITTER

-> FORMATION + OBJECTIVE PRESSURE
SUPPORTER / SIEGER
```

Reason:
- basic body/tempo/durability is easiest to read first;
- mitigation and geometry add new axes without yet adding complex state machines;
- CHARGER/SPLITTER require readable state transitions and target-order consequences;
- SUPPORTER/SIEGER rely on formation, screening, uptime and objective pressure, so they benefit from the player already understanding prior vocabulary.

This is an availability-order candidate, not exact first-teach Stage adoption.

Within each Tier, exact first appearance / teach / mixed / high-pressure windows remain open until the candidate is selected.

## 8. P6 consequences for Tier choice

P6 changes how the old Tier candidates should be interpreted.

### Encounter-family rotation
A Tier does not need to make every class equally strong.
It needs enough encounter-family diversity that different class strengths receive real opportunities across the Tier.

### Tank objective role
SIEGER/SUPPORTER content should not be used merely as damage checks. It must leave space for Tank control/defense to reduce objective pressure.

### Shop/EXP feedback
Do not select a Tier count by trying to make provisional EXP reach exact milestone numbers. Exact EXP semantics remain open and later reconverge at P10R.

### Fresh-forward magnitude watch
Use current progression models to identify direction and collision risk, not to claim exact Stage unlock counts for the final authored Tier.

## 9. Recommendation

Current evidence supports the following recommendation for user decision:

```text
RECOMMEND A:
4-Tier initial campaign
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future expansion
```

Why:
- strongest novelty-per-Tier efficiency;
- substantial campaign volume already exists before adding a fifth Tier;
- class-opportunity coverage has already passed structural audit;
- P6 does not expose a reason to split the late pair;
- known T4 overload risk has a clear authoring guardrail and is WATCH, not FAIL;
- preserves open-ended future monster expansion.

Fallback:

```text
B = split SUPPORTER and SIEGER into T4/T5
only if later lower-layer authoring/simulation shows the combined T4 cannot remain readable or role-expressive.
```

Candidate C should not be selected for the initial current-roster launch without additional content evidence.

## 10. Decision gate

User approval is required before adopting:
- exact initial Tier count;
- the availability ladder;
- T1 exact roster.

Recommended approval package:

```text
Initial Tier count = 4
T1 = GRUNT / RUNNER / BRUTE
T2 adds SHIELD / FLYER
T3 adds CHARGER / SPLITTER
T4 adds SUPPORTER / SIEGER
T5+ reserved for future monster expansion
```

If approved, the next work is still **not exact Stage1-50 content**.
First define, for the adopted Tier ladder:
- Tier identity and novelty budget;
- available encounter families/archetypes per Tier;
- introduction windows;
- class-opportunity guardrails;
- role-expression guards;
- then author Tier1 Stage1-50.

No production change is authorized by this review.
