# Timing Defense — Modifier Pipeline & Power Attribution Approved Contract V0.1

Date: 2026-10-23 KST  
Status: **USER_APPROVED_DIRECTION / STRUCTURAL CONTRACT / NO NUMERICAL FREEZE**

Depends on:
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `73_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_PROPOSAL_V0_1.md`
- `01_META_PROGRESSION.md`
- `15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `../../DESIGN_DECISIONS.md`
- `../../SKILL_PLAN_LV6_31.md`
- `../../PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
- `../../N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`

Machine-readable companion:
- `data/modifier_pipeline_contract_v0_1.yaml`

---

# 0. Approval boundary

The user explicitly approved all seven recommendations in document 73.

This document promotes those recommendations into the P2 structural contract.
It freezes **semantics and ordering**, not downstream numerical balance values.

Approved package:
1. typed hybrid same-stat stacking;
2. scalar stat vs effect-rule separation;
3. authoritative outgoing attack pipeline order;
4. incoming wall-defense pipeline order;
5. derived-stat ownership model;
6. deterministic power-attribution ledger requirement for simulator/test paths;
7. delayed rounding at realized-effect boundaries.

---

# 1. Typed hybrid stacking — USER APPROVED

## 1.1 Ordinary same-stat progression
When multiple ordinary progression sources modify the same scalar stat, their approved percentage-add components aggregate additively by default.

Canonical semantic form:

```text
percentBonus(stat) = sum(PCT_ADD modifiers for that stat)
effectiveStat = (baseStat + sum(FLAT_ADD)) × (1 + percentBonus)
```

Consequences:
- STAR, ACHIEVEMENT and RUN SHOP do not automatically multiply one another merely because they come from different subsystems.
- explicit multiplication is opt-in and must be authorized by a specific skill/effect contract.
- source identity is retained for attribution even when values share one stat bucket.

This contract does not freeze any modifier value.

## 1.2 Crit semantic family
Structural form:

```text
critChance = baseCritChance + sum(critChancePp)
critMultiplier = baseCritMultiplier + sum(critDamageBonus)
```

Exact caps and values remain OPEN.

## 1.3 Wall HP semantic family
If both flat and percentage sources exist:

```text
wallMaxHp = (baseWallHp + sum(wallHpFlat)) × (1 + sum(wallHpPct))
```

Exact source set and values remain OPEN.

## 1.4 Generic wall defense semantic family
Structural form:

```text
genericWallDR = clamp(sum(wallDamageReductionPp), 0, capTBD)
```

The cap remains OPEN.
Unique class/team defenses are not silently merged into this bucket.

## 1.5 Knockback scalar family
Structural form:

```text
effectiveKnockbackBase = baseKnockback × (1 + sum(knockbackPct))
```

Action-specific class multipliers and target resistance/boss scalars apply in their explicit later stages.

---

# 2. Scalar stat and effect-rule separation — USER APPROVED

Scalar stat modifiers and mechanics/effect rules use different semantic paths.

Examples of scalar stats:
- attackPct / attackFlat
- critChancePp
- critDamageBonus
- wallHpFlat / wallHpPct
- wallDamageReductionPp
- knockbackPct
- approved scalar cadence/recovery modifiers

Examples that must remain effect rules rather than fake scalar stats:
- penetration count / penetration decay
- armor ignore
- splash / outer ring / chain explosion
- tracking or secondary-target creation
- wall shields
- slow/control zones
- strict-line targeting
- Heavy/P×P attack replacement
- boss-specific scalar contracts
- N3 fixed-budget proc isolation

Implementation convenience does not authorize converting an effect rule into a generic percentage stat.

---

# 3. Authoritative outgoing attack pipeline — USER APPROVED

Canonical conceptual order:

```text
A. validate authoritative action / target / timing turn
B. resolve timing judgment + Heavy/P×P state
C. build attack template / hit plan from class + unlocked skill rules
D. resolve effective persistent/run scalar stats
E. compute parent outgoing raw power
F. apply explicit action-condition transforms/multipliers where authorized
   - skill condition
   - combo
   - other approved action transforms
G. resolve crit according to the attack template's explicit crit policy
H. materialize primary/secondary hit coefficients and geometry
I. per target: apply boss/class scalar and target mitigation/armor/state
J. round/apply realized damage or control
K. resolve death/spawn/secondary-trigger consequences
L. emit isolated post-action procs such as N3 according to their own contract
```

Key invariants:
- generated secondary hits derive from a pre-target outgoing basis;
- each target applies its own mitigation independently;
- one target's armor does not automatically reduce another target's splash/penetration damage;
- specific frozen skill contracts may override inheritance/retarget/proc rules explicitly;
- unresolved later-skill semantics remain separate decision gates.

---

# 4. Crit policy ownership — STRUCTURAL REQUIREMENT

Every attack template / hit generator that can interact with ordinary proc crit must expose an explicit policy.

Allowed structural policy vocabulary includes:
- `PARENT_ROLL_INHERITED`
- `PER_HIT_ROLL`
- `NO_PROC_CRIT`
- `FIXED_BY_CONTRACT`

P2 does **not** assign a final policy to every unresolved Lv11+ multihit skill.
Existing authoritative/frozen contracts take precedence.
Unresolved skills require their own approval gate before production authority.

---

# 5. N3 isolation — PRESERVED

The frozen N3 contract remains a separate post-action proc path.

N3:
- grants no EXP;
- grants no charge;
- does not increment combo;
- does not roll ordinary proc crit;
- does not recursively trigger class skills;
- does not recursively trigger N3;
- retains existing target armor/boss-scalar behavior where already frozen.

N3 fixed raw-equivalent budgets are not folded into ordinary `effectiveAttack` and do not inherit ordinary STAR/SHOP/COMBO/CRIT multiplication unless a later explicit contract changes that frozen rule.

---

# 6. Incoming wall-damage pipeline — USER APPROVED

Canonical conceptual order:

```text
A. monster raw wall-damage event
B. monster capability/state outgoing modifier
C. generic wall-damage-reduction stat bucket
D. explicit unique class/team defensive effect
E. final incoming damage before shield
F. wall shield absorption
G. Base HP damage
```

Consequences:
- generic progression defense remains separately measurable;
- unique class/team defense remains separately attributable;
- a non-stacking rule such as Tank Iron Wall is represented explicitly, not hidden inside the generic bucket;
- wall shields absorb damage that would otherwise reach Base HP.

Exact generic-DR cap, exact shield values and downstream coefficients remain OPEN unless already independently frozen.

---

# 7. Derived-stat ownership — USER APPROVED

Authoritative state stores source truth:
- base values / version identifiers;
- star/account modifiers;
- achievement modifiers;
- shop ranks/modifiers;
- level and unlocked skill state;
- temporary effects;
- conditions needed for deterministic evaluation.

Values such as `effectiveAttack`, `effectiveCritChance`, `effectiveWallDR` are **derived results**, not independent authoritative truth.

They may be cached only if the cache is invalidated/versioned against its authoritative source state.

A run may snapshot account modifier/version identity for replay/audit, but the derived effective value must remain reproducible from authoritative inputs.

---

# 8. Deterministic power-attribution ledger — USER APPROVED

The simulator/test authority must be able to explain each material damage/control/wall event deterministically.

Minimum conceptual record:

```text
PowerAttribution
  actionId
  parentActionId|null
  sourcePlayerId|system
  sourceClass
  effectId
  targetId
  baseAmount
  statContributions[]
    sourceId
    sourceVersion
    scope
    statId
    operation
    value
  actionTransforms[]
    timingTier
    heavyOrPxP
    combo
    skillId
    critPolicy
    critResult
  targetTransforms[]
    bossScalar
    armor
    mitigation
    resistance
  preMitigationAmount
  finalAmount
  shieldAbsorbed
  hpDamage
```

The full ledger is an internal simulation/test requirement.
Production UI/network payloads are not required to expose the entire structure every frame.

Primary purpose:
- isolate STAR vs ACHIEVEMENT vs SHOP vs SKILL vs COMBO vs CRIT leverage;
- compare nominal stat value by class;
- audit N3/multihit budgets;
- diagnose wall-defense stacking;
- preserve simulator/runtime parity.

---

# 9. Delayed rounding — USER APPROVED

Do not repeatedly round after each intermediate modifier stage.

Structural rule:
- maintain sufficient deterministic precision through modifier evaluation;
- perform rounding at each realized damage/control application boundary;
- runtime and simulator must share one deterministic rounding contract;
- fixed-budget systems such as N3 preserve their existing deterministic remainder-safe allocation rules.

Whether implementation uses integer fixed-point or another deterministic numeric representation remains an engineering choice, not a P2 balance decision.

---

# 10. Canonical modifier record schema

Approved structural fields:

```yaml
modifier:
  sourceId: string
  sourceVersion: string
  statId: string|null
  effectId: string|null
  scope: BASE|ACCOUNT|CLASS_PERMANENT|RUN|LEVEL|TEMPORARY|ACTION|TARGET
  operation: FLAT_ADD|PCT_ADD|PCT_MULT_EXPLICIT|PP_ADD|UNIQUE|MAX|OVERRIDE|PROC
  value: number|null
  stackGroup: string|null
  condition: object|null
  ownerClass: classId|null
  targetClass: classId|null
```

Rules:
- `PCT_MULT_EXPLICIT` is opt-in, never the default merely because a source belongs to a different subsystem;
- `UNIQUE`, `MAX` and `OVERRIDE` must name/own an explicit stack group where relevant;
- effect rules may use `effectId` instead of pretending to be scalar stats;
- values may remain null/parameterized until the downstream numerical calibration phase.

---

# 11. P2 closure criteria

P2 is structurally complete when:
- this approved contract exists;
- the machine-readable companion schema exists;
- P1/P2 together provide enough state and modifier semantics for a deterministic persistent-run kernel;
- no downstream numerical value is silently frozen by P2.

P3 may now begin as an integration/simulation slice.

---

# 12. Explicitly remains OPEN

Approval of P2 does not approve:
- exact star bonus values;
- exact achievement bonus values;
- exact shop value/price/cadence;
- crit chance cap;
- generic defense cap;
- exact Base HP;
- exact Lv11+ production coefficients not already frozen elsewhere;
- final Lv26/Lv31 contracts;
- unresolved per-skill crit inheritance;
- exact boss values;
- multiplayer scaling values;
- exact modifier numeric representation;
- production implementation/deployment.

These remain downstream analysis -> proposal -> user approval gates.

---

# 13. Next boundary

P2 = `USER_APPROVED_STRUCTURAL_COMPLETE`.

Next work package:
`P3 TEN_STAGE_PERSISTENT_RUN_KERNEL`.

P3 must use P1/P2 semantics to test deterministic multi-stage state continuity.
P3 must not silently freeze final EXP, shop, stars, achievements, boss, multiplayer progression or exact launch-stage content.
