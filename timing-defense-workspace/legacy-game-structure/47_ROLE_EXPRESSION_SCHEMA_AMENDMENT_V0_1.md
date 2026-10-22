# Timing Defense — Role Expression Schema Amendment V0.1

Date: 2026-10-22 KST  
Status: **AUTHORING/Simulation SCHEMA AMENDMENT / NO NUMERIC FREEZE**

Depends on:
- `07_AUTHORING_DATA_SCHEMA.md`
- `43_ABSOLUTE_ENTRY_DEPTH_AMENDMENT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`

---

# 0. Purpose

Add a first-class representation for:
- what role a monster is supposed to express
- whether an encounter is teaching/testing that role
- whether the player received a readable counterplay opportunity
- whether the ability actually completed

These are separate concepts.

---

# 1. Monster registry extension

Candidate extension:

```yaml
monsterRegistry:
  version: string
  roleExpressionContractVersion: string
  monsters:
    - id: string
      roleExpressionId: string
      capabilityContractVersion: string|null
```

Future monsters cannot omit `roleExpressionId` once admitted to the active encounter library.

---

# 2. Encounter event extension

```yaml
encounterEvent:
  id: string
  archetypeId: string
  expressionPurpose: none|teach|standard|mastery
  requiredRoleExpressionMonsterIds: [monsterId]
  entryBaseXOffsetOverride: number|null
  formationId: string
  cadenceId: string
```

Semantics:

## none
The encounter is not being used to judge that monster's core identity.

## teach
Strong readability protection. The minimum role expression should be clearly observable before skilled counterplay can end the mechanic.

## standard
Role remains reliably present, but skilled counterplay may suppress full activation.

## mastery
Preemption can be more aggressive, but default authoring still must not reduce the monster to a spawn-and-delete no-op.

---

# 3. Formation integration

Role expression uses both:

```yaml
formation:
  baseSpawnXOffset: number|null
  slots:
    - spawnXOffset: number|null
```

And optional encounter override:

```yaml
entryBaseXOffsetOverride: number|null
```

Rules:
- absolute entry depth controls encounter arrival timing
- slot depth controls front/back relation
- neither overrides target selection
- actual frontmost geometry remains authoritative

---

# 4. Simulation output extension

Candidate normalized structure:

```yaml
roleExpression:
  monsterId: string
  expressionPurpose: none|teach|standard|mastery
  spawnedCount: integer
  preExpressionDeaths: integer
  minimumExpressionCount: integer
  readableCounterplayCount: integer
  fullActivationCount: integer
  playerPreventedActivationCount: integer
  structuralOpportunityByClass:
    knight: boolean|null
    rogue: boolean|null
    tank: boolean|null
    archer: boolean|null
    mage: boolean|null
  firstExpressionAtMs: number|null
  firstCounterplayWindowAtMs: number|null
  failureClass: string|null
```

Important:
- `minimumExpressionCount` is not the same as `fullActivationCount`
- `playerPreventedActivationCount` can be a successful gameplay outcome
- `preExpressionDeaths` is the key spawn-delete diagnostic

---

# 5. Stateful mapping

## CHARGER
```text
minimumExpression = enter windup
readableCounterplay = visible windup interval exists
fullActivation = transition to charge
playerPreventedActivation = interrupt/delete after windup entry
preExpressionDeath = death before first windup
```

## SIEGER
```text
minimumExpression = reach standoff + enter first-shot windup
readableCounterplay = first-shot windup exists
fullActivation = wall shot fires
playerPreventedActivation = reposition/delete during readable windup
preExpressionDeath = death before first-shot opportunity
```

## SUPPORTER
```text
minimumExpression = aura reaches >=1 non-self target
fullActivation = sustained aura is encounter-dependent; no single universal endpoint
preExpressionDeath = death without any non-self aura interval
```

## SPLITTER
```text
minimumExpression = parent death creates exactly two children and changes post-death state
fullActivation = not defined as wall hit; use child lifetime/frontline/population metrics
preExpressionDeath = not generally applicable to parent because death triggers mechanic
identity failure = children are created but disappear with no meaningful post-split state
```

---

# 6. Passive-role mapping

## RUNNER
Minimum expression is speed-caused arrival/front-order difference.

## BRUTE
Minimum expression is meaningful frontline holding / damage absorption / screening.

## SHIELD
Minimum expression is mitigation changing effective incoming damage or required hit investment.

## FLYER
Minimum expression is vertical geometry creating a real line/splash/target-order opportunity difference.

These require new simulator instrumentation rather than a one-frame state transition.

---

# 7. Validation rules

For `expressionPurpose != none`:

1. every `requiredRoleExpressionMonsterId` must exist in the active monster registry
2. every required monster must have a role-expression contract
3. five-class structural opportunity must be measurable
4. guaranteed pre-expression deletion is invalid
5. counterplay after minimum expression is allowed and should be measured separately
6. unavoidable wall damage before a meaningful player response is invalid
7. TEACH encounters have stricter readability expectations than STANDARD/MASTERY

Exact probabilities/ms thresholds remain OPEN pending fitted SKILLED_V2 evidence.

---

# 8. Versioning

Add:

```text
monster-role-expression-contract-v0.x
role-expression-schema-v0.x
```

Simulation reports should record both versions once integrated.

---

# 9. Implementation boundary

This amendment affects planning/simulation authoring only.

Do not wire it into live gameplay before:
- critical representative set PASS
- all-20 representative role audit
- fitted player-model review
- explicit production freeze
