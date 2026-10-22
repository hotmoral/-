# Timing Defense — Monster Role Expression Contract V0.1

Date: 2026-10-22 KST  
Status: **USER-CONFIRMED STRUCTURAL RULE + NON-NUMERIC CONTRACT / NO PRODUCTION FREEZE**

Depends on:
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`
- `43_ABSOLUTE_ENTRY_DEPTH_AMENDMENT_V0_1.md`
- `44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`

Machine-readable contract:
- `data/monster_role_expression_contract_v0_1.yaml`

---

# 0. User-confirmed design intent

Core rule:

> 의도된 encounter에서 몬스터가 등장하자마자 자기 역할도 보여주지 못하고 삭제되는 구조는 허용하지 않는다.

This does **not** mean every monster must always complete its strongest ability.

Correct distinction:

```text
ROLE-EXPRESSION OPPORTUNITY
  must exist

PLAYER COUNTERPLAY
  may prevent full activation
```

Examples:
- CHARGER enters readable windup -> player knockback cancels charge = VALID
- CHARGER dies before any windup is visible = INVALID authoring for a designated CHARGER role encounter
- SIEGER reaches standoff and presents a readable first-shot windup -> player breaks screen and kills it = VALID
- SIEGER is routinely deleted before any real first-shot opportunity = INVALID authoring

The purpose is not to protect enemies from skilled play.
The purpose is to ensure the player first has something meaningful to read and answer.

---

# 1. Two-layer contract

Every non-baseline monster is evaluated on two different layers.

## A. Minimum Role Expression
The monster must create a perceivable mechanical state that distinguishes it from a GRUNT-like ordinary body.

## B. Full Activation / Outcome
Whether its mechanic actually succeeds is balance- and skill-dependent.

Do not collapse A and B into one percentage.

A skilled player stopping a mechanic after A is desirable counterplay.
A mechanic disappearing before A is generally an authoring defect.

---

# 2. Spawn-delete guard

New structural guard:

`PRE_EXPRESSION_DEATH_WITHOUT_READABLE_COUNTERPLAY = INVALID`

Applies to designated role-expression encounters.

It means:
- spawning farther away is not automatically safer
- spawning closer is not automatically harder
- HP inflation is not the default fix
- formation depth / absolute entry depth / cadence / screen lifetime are first-line authoring controls

GRUNT is exempt because it is the neutral reference body.

Exact milliseconds/probabilities are intentionally OPEN until fitted `SKILLED_V2` evidence exists.

---

# 3. Current nine-monster contract

| Monster | Core identity | Minimum role expression | Valid player counterplay after expression | Structural failure |
|---|---|---|---|---|
| GRUNT | neutral baseline | none beyond ordinary presence | ordinary removal | none; baseline exempt |
| RUNNER | sustained fast approach | speed changes arrival/front-order behavior before death | prioritize/remove before wall pressure | `RUNNER_SPEED_IDENTITY_ERASED` |
| BRUTE | raw durability + knock resistance | meaningfully holds frontline / absorbs attention | sustained focus, heavy/control | `BRUTE_DURABILITY_IDENTITY_ERASED` |
| SHIELD | mitigation frontline | armor changes effective damage or hit requirement | adapt target/time investment | `SHIELD_MITIGATION_IDENTITY_ERASED` |
| FLYER | vertical geometry | Y-position creates actual geometry/targeting opportunity | line/AoE adaptation | `FLYER_GEOMETRY_IDENTITY_ERASED` |
| CHARGER | telegraphed interruptible burst | enters visible windup and presents response window | interrupt/delete during windup | `CHARGER_PRE_WINDUP_ERASURE` |
| SPLITTER | death -> two children | split causes real post-death population/target-state change | adapt to children / AoE / retarget | `SPLITTER_TRANSFORM_IDENTITY_ERASED` |
| SUPPORTER | nonstacking movement aura | at least one other monster receives meaningful aura interval | break screen/remove supporter | `SUPPORTER_AURA_IDENTITY_ERASED` |
| SIEGER | standoff repeated wall attack | reaches standoff, enters readable windup, has real first-shot opportunity | break screen/reposition/delete during windup | `SIEGER_PRE_SHOT_OPPORTUNITY_ERASURE` |

---

# 4. Per-monster metrics

## GRUNT
Reference only:
- `aliveTime`
- `frontlineTime`

No special expression gate.

## RUNNER
Required diagnostics:
- `aliveTime`
- `distanceAdvanced`
- `frontOrderChanges`
- `timeToWallDeltaVsGrunt`

The speed identity must be observable before deletion in encounters authored around RUSH pressure.

## BRUTE
Required diagnostics:
- `frontlineBlockTime`
- `hitsReceived`
- `rawDamageAbsorbed`
- `screenTimeProvided`

Do not judge BRUTE only by time-to-kill. Its purpose includes screening.

## SHIELD
Required diagnostics:
- `mitigatedHits`
- `preventedDamage`
- `effectiveHitCount`
- `frontlineBlockTime`

If armor exists mathematically but never affects a real decision/outcome, the role is not expressed.

## FLYER
Required diagnostics:
- `flyerGeometryOpportunityTime`
- `lineOpportunityChanges`
- `splashOpportunityChanges`
- `targetOrderChanges`

Flying is not considered expressed merely because a sprite has a different Y coordinate.

## CHARGER
Required diagnostics:
- `windupEntries`
- `windupVisibleTime`
- `interrupted`
- `completedCharges`
- `erasedBeforeWindup`

Minimum contract:
`windup entry + readable response window`.

Charge completion is **not** mandatory because successful interruption is valid skilled counterplay.

## SPLITTER
Required diagnostics:
- `parentDeaths`
- `childrenSpawned`
- `childAliveTime`
- `childFrontlineTime`
- `peakActiveDeltaAfterSplit`
- `targetReordersFromSplit`

Parent death can be fast. What cannot disappear is the transformation consequence.

## SUPPORTER
Required diagnostics:
- `auraTargetCount`
- `auraUptime`
- `screenedAuraUptime`
- `screenedAuraRatio`
- `supporterAliveTime`

Minimum contract:
`aura reaches >=1 non-self target for a meaningful observable interval`.

## SIEGER
Required diagnostics:
- `standoffReach`
- `windupEntries`
- `firstShotOpportunity`
- `firstShotAt`
- `shotCount`
- `screenedFirstShot`
- `erasedBeforeFirstShotOpportunity`

Minimum contract:
`standoff -> readable windup -> real first-shot opportunity`.

A first shot does not have to land in every run if the player earns a counterplay kill during the visible windup.

---

# 5. Five-class structural coverage

For any encounter explicitly authored to teach or test a monster's core role:

- all five classes must have a structurally valid path to observe the minimum role expression
- one class may suppress/answer the mechanic more efficiently than another
- class asymmetry is desirable
- a class-specific advantage must not turn the monster into a non-mechanic that disappears at spawn by default

This is especially important for:
- Mage splash deleting a stateful body before activation
- Rogue high frontline throughput
- Archer line access to screened backline
- Tank control extending combat while preventing objective damage

The gate is about **opportunity**, not equal outcome.

---

# 6. Teach / standard / mastery distinction

The same monster may use different expression requirements by encounter purpose.

## TEACH
Strongest protection of readability.
The core mechanic should be very likely to enter its minimum expression state.

## STANDARD
Mechanic should remain reliably present, but skilled counterplay may suppress completion more often.

## MASTERY
The player may preempt the monster more aggressively, provided the encounter does not reduce the monster to an invisible/no-op body by default.

Exact rates remain OPEN.

---

# 7. Current evidence status

Based on current Layer-A V0.1 evidence:

- GRUNT: `BASELINE_EXEMPT`
- RUNNER: `MEASUREMENT_REQUIRED`
- BRUTE: `PRELIMINARY_ROLE_PRESENT / METRIC_EXPANSION_REQUIRED`
- SHIELD: `MEASUREMENT_REQUIRED`
- FLYER: `MEASUREMENT_REQUIRED`
- CHARGER: `FAIL_DEFAULT_GEOMETRY` — current default representative recipes produced 0 windups across the critical class/trace sweep
- SPLITTER: `PARTIAL_PASS` — split occurs; post-split meaningful pressure still needs stronger metrics
- SUPPORTER: `PASS_WITH_WATCH` — aura exists but exposure varies strongly by class/throughput
- SIEGER: `FAIL_DEFAULT_GEOMETRY` — current E11/E19 default geometry produced 0 shots across the critical class/trace sweep

These are recipe/measurement findings, not global monster-stat verdicts.

---

# 8. Authoring response order when expression fails

Do not immediately buff HP.

Preferred correction order:

1. absolute entry depth
2. relative front/back depth
3. spawn order / spawn delay
4. screen lifetime and composition
5. cadence / overlap
6. trigger/standoff exposure timing
7. only then monster durability/speed/capability coefficients if geometry cannot produce a valid window

This order keeps monster identity readable without converting every special into an HP sponge.

---

# 9. Future monster extensibility

Every future monster added to T5/T6/T7+ must declare before admission:

```text
coreMechanic
minimumRoleExpression
readableCounterplay
failureClassification
requiredMetrics
```

No new monster is admitted only with HP/speed/damage values.

This contract is intentionally roster-size agnostic.

---

# 10. Current next boundary

Apply this contract to Layer-A capability-window calibration:

1. CHARGER: find readable windup activation ranges for E07/E17 first
2. SIEGER: find readable first-shot-opportunity ranges for E11/E19
3. reject ranges that create unavoidable early wall damage
4. add missing RUNNER/BRUTE/SHIELD/FLYER/SPLITTER/SUPPORTER role metrics to the simulator
5. rerun five classes under `CURRENT_AUTHORITY_LV6`
6. classify each representative recipe by role-expression PASS/WATCH/FAIL
7. only after critical-set PASS expand to all 20 representative recipes

No production numeric freeze is authorized by this document.
