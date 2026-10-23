# Timing Defense — Encounter Opportunity Distribution Framework Proposal V0.1

Date: 2026-10-24 KST  
Status: **STRUCTURAL PROPOSAL / DIAGNOSTIC AUTHORING FRAMEWORK / NO EXACT QUOTA / NO TIER1 ROSTER ADOPTION / NO PRODUCTION AUTHORITY**

Depends on:
- `02_TIER_SYSTEM.md`
- `03_STAGE_STRUCTURE_50.md`
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
- `147_ENCOUNTER_COMPOSITION_CLASS_RESPONSE_MATRIX_V0_1.md`

---

# 0. Purpose

The class-response matrix established that a class can look strong or weak largely because of the encounter families presented to it.

Therefore future Tier authoring needs a guard against this failure mode:

```text
One pressure family dominates the Tier
-> one class specialty becomes the default answer
-> other classes look numerically weak
-> balance work incorrectly buffs/nerfs classes
```

The purpose of this framework is to measure **opportunity distribution** before concluding that class coefficients are wrong.

This is not an equal-win-rate system.
It does not require every Stage to be equally favorable to every class.
It preserves:
- class asymmetry;
- real weaknesses;
- soft walls;
- cross-class/meta progression;
- no hard lockout.

---

# 1. Correct unit of analysis: encounter segment, not only Stage

A Stage may contain multiple distinct pressure sequences.
Therefore a Stage-level tag such as `Mage-favorable` is too coarse.

Use the existing encounter signature:

```text
EncounterSegment
  archetypeId
  composition bucket
  formation
  cadence
  geometry
  timing window
  intensity bucket
```

Each authored Stage contains one or more `EncounterSegment`s.

Example:

```text
Stage 32
  segment A = RUSH / SCATTER / WAVE
  segment B = BULWARK / LINE / STAGGER
  segment C = recovery BASELINE
```

Class opportunity is first classified per segment, then aggregated to Stage band and Tier.

---

# 2. Response classification per class

For each encounter segment and each class, store:

```text
responseClass:
  FAVORABLE
  NEUTRAL
  UNFAVORABLE
  MIXED
```

`MIXED` is required for classes such as Tank where:

```text
enemy-removal throughput = weak
objective control / wall preservation = strong
```

Do not flatten this into a single DPS score.

Optional directional strength annotation:

```text
++ / + / 0 / - / --
```

from the evidence matrix, but exact numeric weights remain open.

---

# 3. Multi-output response dimensions

A single `win/loss` label is insufficient.
For each class × segment, allow the following dimensions:

```text
removalThroughput
controlValue
objectiveProtection
backlineAccess
formationLeverage
roleExpression
riskOfBacklog
```

Examples:

## Tank in FLOOD
```text
removalThroughput = weak
controlValue = strong
objectiveProtection = strong
riskOfBacklog = high
```

## Archer in LINE
```text
removalThroughput = strong
backlineAccess = strong
formationLeverage = strong
```

## Mage in distributed BULWARK
```text
removalThroughput = weak-to-neutral
formationLeverage = poor
```

This prevents `SURVIVAL == CLEAR` and prevents high wall reserve from being mistaken for high damage balance.

---

# 4. Three ledgers — do not use simple Stage counts alone

For each Tier/class, maintain at least three separate opportunity ledgers.

## A. Occurrence ledger
How often a response type appears.

```text
favorableSegmentCount
neutralSegmentCount
unfavorableSegmentCount
mixedSegmentCount
```

Useful for readability, but insufficient by itself.

## B. Threat-time ledger
How much meaningful combat time each response occupies.

A 2-second favorable segment must not cancel a 25-second unfavorable segment merely because both count as one encounter.

Track directionally:

```text
favorableThreatTime
neutralThreatTime
unfavorableThreatTime
mixedThreatTime
```

Exact weighting formula remains open.

## C. Criticality ledger
Where the exposure occurs in the progression.

The same unfavorable segment has different significance at:
- recovery Stage 12;
- 1★/2★ gate band;
- Stage46–49 mastery band;
- Tier final.

Track:

```text
gateExposure
masteryExposure
finalExposure
```

No exact multiplier is frozen now.

---

# 5. Class opportunity guard families

## 5.1 Positive specialty expression guard

Each class must receive meaningful opportunities where its advertised strengths actually matter.

```text
Knight -> mixed/frontline/penetration/reorder
Rogue  -> durable/high-value execution
Tank   -> control/objective/wall-pressure management
Archer -> aligned-line/backline penetration
Mage   -> density/cluster/AOE
```

Failure example:
- Archer exists for 50 Stages but almost no meaningful line geometry occurs.

That is `CLASS_SPECIALTY_STARVATION`, not evidence that Archer damage is too low.

## 5.2 Negative identity expression guard

Each class must also encounter pressure that exposes its weakness.

Examples:
- Mage should not receive dense clusters on nearly every high-pressure segment;
- Archer should face meaningful scatter/off-corridor moments;
- Rogue should face sustained broad volume where single-target execution is not the whole answer;
- Tank should experience backlog/removal pressure;
- Knight should not be best at both specialist extremes.

Failure:

```text
CLASS_WEAKNESS_ERASURE
```

## 5.3 No hard-lockout guard

An unfavorable encounter may be severe.
A contiguous band must not become mechanically impossible for a class solely because its specialty is absent.

Look for:

```text
longestUnfavorableRun
unfavorableGateStack
unfavorableMasteryStack
recoveryOpportunityAfterSoftWall
```

Exact thresholds remain open until Tier authoring exists.

## 5.4 One-family dominance guard

If a Tier's meaningful threat-time is dominated by one family, class results will be biased toward the specialist for that family.

Flag:

```text
PRESSURE_FAMILY_DOMINANCE
```

before changing class numbers.

---

# 6. Contiguous-run checks matter more than only totals

A Tier could have a globally reasonable favorable/unfavorable ratio but still create a bad player experience if all unfavorable encounters are consecutive.

Example:

```text
Stage31-39 = nine straight Mage-unfavorable distributed-durable stages
```

Even if Stage1-30 contained many easy clusters, the late soft-wall band may feel like a class lockout.

Therefore record per class:

```text
longestConsecutiveUnfavorableSegments
longestConsecutiveUnfavorableStages
longestNoSpecialtyExpressionBand
recoveryStageDistanceAfterPressurePeak
```

No exact maximum is frozen here.

---

# 7. Macro-band interpretation

The common 50-Stage macro spine remains useful, but opportunity expectations differ by band.

## Stage 1–10 — establish / introduce
Priority:
- readability;
- mechanic teaching;
- class opportunity balance is secondary to content introduction.

Guard:
- do not introduce a mechanic only through a class-hostile configuration.

## Stage 11–20 — mix / verify
Priority:
- begin showing that one problem can be answered differently by different classes.

## Stage 21–30 — Tier identity establishment
Priority:
- primary Tier pressure family becomes visible;
- start checking class-opportunity skew.

## Stage 31–40 — pressure / soft-wall formation
Priority:
- weaknesses may be intentionally exposed;
- no hard lockout;
- meta/cross-class recovery loop must remain plausible.

## Stage 41–49 — mastery examination
Priority:
- stronger favorable/unfavorable contrasts are acceptable;
- Lv31/P×P mastery becomes relevant;
- one specialist family must not monopolize the whole band unless the Tier identity explicitly justifies it and other classes retain viable paths.

## Stage 50 — final
Priority:
- test the Tier's learned vocabulary;
- not required to give every class its best matchup;
- must not become an unexplained hard counter to one class.

---

# 8. Monster availability comes before opportunity balancing

Do not design a desired class-opportunity table and then force unavailable monsters into the Tier to satisfy it.

Correct order:

```text
Tier availability ladder
-> available monster set
-> available encounter families/archetypes
-> opportunity distribution within that vocabulary
```

If a later pressure family cannot be expressed by T1's monster subset:
- use an allowed simpler analogue if it preserves the learning purpose;
- or defer the family to a later Tier.

Do not violate monster-introduction pacing merely to make a spreadsheet symmetrical.

---

# 9. Player-power / skill-reach coupling

Encounter opportunity depends on when class skills are actually available.

Example:
- an Archer line opportunity before penetration skill reach is not equivalent to the same geometry after Lv26/Lv31;
- a Stage46 density test interacts with Mage Lv31 frequency;
- Tank control value changes after Aftershock/Absolute Barrier.

Therefore future exact authoring should join:

```text
EncounterSegment
× expected class skill state at that Stage band
× expected shop/meta profile
```

This is one reason the framework must feed into P6/P10R later rather than freeze exact Stage frequencies now.

---

# 10. Candidate authoring record

Future Tier data can carry a non-production analysis companion such as:

```yaml
stage: 32
segments:
  - encounterId: E05_MIXED_WALL
    pressureFamilies: [BULWARK]
    formation: LINE
    cadence: STAGGER
    intensity: MEDIUM
    classResponse:
      Knight:  FAVORABLE
      Rogue:   FAVORABLE
      Tank:    MIXED
      Archer:  FAVORABLE
      Mage:    UNFAVORABLE
    evidenceTags:
      - MATRIX_V0_1
```

The labels are authoring diagnostics, not runtime gameplay data.

---

# 11. Tier-level diagnostic outputs

When a candidate Tier exists, generate at least:

```text
per class:
  favorable / neutral / unfavorable / mixed segment counts
  threat-time share by response type
  high-intensity share by response type
  longest unfavorable Stage run
  longest specialty-starvation run
  gate-band response profile
  mastery-band response profile

per pressure family:
  occurrence
  threat-time
  peak-concurrency contribution
  Stage presence
  high-intensity presence

cross-class:
  strongest specialist exposure
  weakest-class exposure
  one-family dominance flags
  potential hard-lockout bands
```

Do not reduce this to one overall fairness score initially; retaining the dimensions makes causal review cheaper.

---

# 12. What counts as a balance defect vs authoring defect

## Likely authoring/distribution defect

```text
A class performs poorly mainly when its unfavorable family dominates the Tier,
and performs correctly in its favorable identity probes.
```

First repair:
- composition/frequency/formation/cadence distribution.

## Possible class/package numerical defect

```text
A class underperforms even in encounter families where its defining specialty should be strong,
or overperforms even in families that should expose its weakness.
```

Then inspect:
- package semantics;
- shop interaction;
- exact scalar last.

This is the key diagnostic separation produced by docs 147–148.

---

# 13. Current evidence application

The current Stage46/47 diagnostic fixture is heavily biased toward:
- sustained volume;
- repeated density;
- frequent line/depth opportunity;
- high Lv31 pressure.

That naturally exposes:
- Mage `AOE5`;
- Archer `PEN5`.

The sparse armored replacement tests reduced Mage/Archer outcomes without changing class values, confirming that encounter distribution is a material lever.

Therefore the current aggregate class split is **not sufficient evidence for class scalar repair**.

---

# 14. What remains open

Not chosen here:
- exact favorable/neutral/unfavorable quota;
- exact threat-time weighting formula;
- exact longest-unfavorable-run limit;
- exact recovery cadence;
- exact Tier1 monster roster;
- exact monster unlock Tier;
- exact pressure-family frequency;
- exact Stage composition;
- exact class clear-rate target;
- any class/monster/shop number;
- formal P6 start;
- production implementation.

These require actual Tier candidates and/or user decisions.

---

# 15. Recommended next decision boundary

The framework is now sufficient to prevent the project from mistaking encounter-distribution skew for class imbalance.

The next **design** decision should return to the Campaign Spine and choose a bounded candidate for:

```text
Tier count candidate
+ monster availability / introduction ladder candidate
```

Only after that should exact Tier1 Stage1→50 authoring begin.

Alternative if the user prefers to stay in calibration first:
- formally enter P6 Joint Run-Power Convergence before campaign authoring.

Neither path is adopted by this proposal.
