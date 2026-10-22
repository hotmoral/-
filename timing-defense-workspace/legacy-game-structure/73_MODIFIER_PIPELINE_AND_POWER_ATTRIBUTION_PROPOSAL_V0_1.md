# Timing Defense — Modifier Pipeline & Power Attribution Proposal V0.1

Date: 2026-10-22 KST  
Status: **PROPOSED / AWAITING USER APPROVAL / NO NUMERICAL FREEZE**

Depends on:
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `01_META_PROGRESSION.md`
- `15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `../../DESIGN_DECISIONS.md`
- `../../SKILL_PLAN_LV6_31.md`
- `../../PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
- `../../N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`
- `../../V035_RECONNECT_SHOP_STAGE2_REPORT.md`

---

# 0. Decision boundary

This document does **not** approve or freeze a modifier pipeline.
It records the assistant's P2 analysis and recommendation for user review.

The central problem is that Timing Defense contains multiple power systems with different semantics:
- broad permanent star stats;
- targeted achievement modifiers;
- run-local shop upgrades;
- level/class skills;
- timing judgment / Heavy / P×P;
- persistent combo multiplier;
- N3 milestone burst;
- ordinary proc crit;
- multihit / penetration / splash / chain effects;
- monster armor / boss scalars / capability states;
- wall defense / shields / max-HP changes;
- knockback/control/slow/cadence modifiers.

Treating all of these as one generic percentage multiplier would make later balance unstable and attribution ambiguous.

---

# 1. Key finding — distinguish STAT MODIFIERS from EFFECT RULES

## 1.1 Stat modifiers
These change an effective scalar stat.

Candidate examples:
- attackPct
- attackFlat
- critChancePp
- critDamageBonus
- wallHpFlat
- wallHpPct
- wallDamageReductionPp
- knockbackPct
- cadence/recovery modifiers where represented as a scalar

Potential sources:
- stars
- achievements
- run shop
- some level/class skills

## 1.2 Effect rules
These do not belong in a scalar stat pool.

Examples already present in the design:
- penetration count / penetration decay
- armor ignore
- Mage splash / outer ring / chain explosion
- Rogue extra daggers / tracking targets
- Tank shield / slow zone
- Archer strict-line targeting
- P×P-specific attack replacement
- boss-specific dagger/knockback scalar
- N3 fixed-budget proc isolation

Recommendation:
> Do not represent rule/effect changes as generic stat percentages merely for implementation convenience.

This preserves class identity and prevents unrelated systems from accidentally multiplying effect geometry or proc generation.

---

# 2. Options considered for progression stat stacking

## Option A — every source multiplies independently
Example concept:
`Base × Star × Achievement × Shop × Skill × Combo ...`

Advantages:
- superficially simple formula;
- each source feels independently powerful.

Risks:
- automatic cross-system exponential growth;
- strong snowball when more permanent systems are added;
- same nominal +X% has larger value on already-developed accounts;
- difficult to attribute which subsystem caused late-Tier trivialization.

Verdict: **NOT RECOMMENDED**.

## Option B — every percentage simply adds into one global pool
Advantages:
- very stable;
- easy to reason about.

Risks:
- collapses conditional skill identity into generic progression;
- event-specific mastery bonuses become indistinguishable from passive growth;
- unsuitable for armor ignore, multihit, shields, target geometry, boss scalars and fixed-budget procs.

Verdict: **TOO FLAT / NOT RECOMMENDED AS COMPLETE MODEL**.

## Option C — typed hybrid pipeline
Recommended.

Principle:
1. persistent progression sources that modify the **same scalar stat** aggregate in a controlled stat bucket;
2. action/event-specific skill and mastery effects remain explicit transforms/procs outside that bucket;
3. target mitigation is applied after outgoing attack construction;
4. exact source attribution is retained even when multiple sources share a stat bucket.

This reduces runaway while preserving combat identity.

---

# 3. P2-A recommended stat aggregation semantics

## 3.1 Source scopes
Recommended scope taxonomy:
- `BASE` — class/weapon/objective baseline
- `ACCOUNT` — star broad permanent progression
- `CLASS_PERMANENT` — achievement or other target-class permanent modifier
- `RUN` — coin/shop upgrade
- `LEVEL` — unlocked class skill stat component
- `TEMPORARY` — timed buff/debuff/shield/zone
- `ACTION` — current timing/Heavy/P×P/combo/crit context
- `TARGET` — monster armor/state/boss scalar

Scopes describe ownership/lifetime, not operation order by themselves.

## 3.2 Same-stat progression pool
Recommended default for ordinary scalar growth:

```text
percentBonus(stat) = sum(all approved pct-add modifiers for that stat)
effectiveStat = (baseStat + flatAdd) × (1 + percentBonus)
```

Important:
- STAR + ACHIEVEMENT + SHOP do **not** automatically multiply one another when they modify the same ordinary stat.
- They remain separate source records for attribution despite sharing the additive percentage pool.
- Event-specific skill multipliers are not forced into this pool.

Exact modifier values remain open.

## 3.3 Crit
Recommended semantic form:

```text
critChance = baseCritChance + sum(critChancePp)
critMultiplier = baseCritMultiplier + sum(critDamageBonus)
```

- exact cap remains OPEN;
- class skill such as Rogue +6 percentage points naturally uses `critChancePp`;
- no implicit multiplicative crit-chance stacking.

## 3.4 Wall HP
Recommended operation order if both flat and percentage sources exist later:

```text
wallMaxHp = (baseWallHp + sum(flatHp)) × (1 + sum(wallHpPct))
```

Exact source types/values remain open.

## 3.5 Generic wall defense
Recommended default:

```text
genericWallDR = clamp(sum(wallDamageReductionPp), 0, capTBD)
```

Then explicitly unique class rules such as Tank Iron Wall may apply as a separate unique/non-stacking effect layer if that existing class contract is retained.

Exact cap and final Iron Wall authority remain outside this proposal.

## 3.6 Knockback
Recommended semantic form:

```text
effectiveKnockbackBase = baseKnockback × (1 + sum(knockbackPct))
```

Then apply action-specific skill multipliers and finally target knock-resistance/boss scalar.

---

# 4. P2-B recommended outgoing attack pipeline

Recommended conceptual stages:

```text
A. validate authoritative action / target / timing turn
B. resolve timing result + Heavy/P×P state
C. build attack template / hit plan from class + unlocked skill rules
D. resolve effective persistent/run scalar stats
E. compute parent outgoing raw power
F. apply explicit action-condition multipliers (skill / combo where applicable)
G. resolve crit according to the attack template's crit policy
H. materialize primary/secondary hit coefficients and geometry
I. per target: apply boss/class scalar and target mitigation/armor/state
J. round/apply realized damage or control
K. resolve death/spawn/secondary-trigger consequences
L. emit isolated post-action procs such as N3 according to their own contract
```

Key recommendation:
- generated secondary hits use a pre-target outgoing basis and then each target receives its own mitigation independently;
- one target's armor should not reduce another target's splash/penetration merely because it was the parent target;
- specific skill contracts may override crit inheritance / retargeting / proc eligibility explicitly.

### N3 exception
The frozen N3 contract should remain an isolated fixed raw-equivalent budget proc:
- not boosted by ordinary crit/combo recursion;
- no EXP/charge/combo/skill recursion;
- normal target armor/boss scalar still applies where the existing contract says so.

Therefore N3 should enter at its explicitly approved proc stage rather than being folded into ordinary attackPower.

---

# 5. Crit policy must be explicit per attack template

Multihit introduces an ambiguity that must not be solved implicitly by code order.

Each attack/hit generator should expose a policy such as:
- `PARENT_ROLL_INHERITED`
- `PER_HIT_ROLL`
- `NO_PROC_CRIT`
- `FIXED_BY_CONTRACT`

This proposal does **not** choose the final policy for every Lv11+ multihit skill.
Existing authoritative/frozen contracts take precedence; unresolved later skills require their own decision gate.

---

# 6. Rounding policy recommendation

Do not round at every modifier step.
Repeated intermediate rounding can change class budgets and cause runtime/simulator divergence.

Recommended semantic rule:
- preserve high precision through modifier evaluation;
- round once at each realized hit/control application boundary;
- fixed-budget effects such as N3 use their existing deterministic remainder-safe allocator.

Exact numeric representation (integer fixed-point vs numeric/float implementation) is an engineering choice to validate later, but runtime and simulator must share one deterministic rounding contract.

---

# 7. Incoming wall-damage pipeline proposal

Recommended conceptual order:

```text
A. monster raw wall-damage event
B. monster capability/state outgoing modifier
C. generic wall-damage-reduction stat bucket
D. explicit unique class/team defensive effect (e.g. nonstack Iron Wall, if retained)
E. final incoming damage before shield
F. wall shield absorption
G. Base HP damage
```

Reason:
- generic progression defense remains measurable;
- class-specific defense remains separately attributable;
- shields protect the damage that would otherwise reach Base HP;
- no hidden stacking order.

This ordering is part of the user decision request; it is not yet approved.

---

# 8. Derived stat ownership / snapshot recommendation

Authoritative storage should hold:
- source modifiers / ranks / unlocks / conditions;
- base values / version identifiers;
- temporary effect state.

Derived values such as `effectiveAttack` should normally be **recomputed from authoritative state** or treated as cache with source-version validation, not stored as independent truth.

Reason:
- reconnect/replay consistency;
- prevents stale effective stats after star/shop/skill changes;
- enables deterministic simulation parity.

A Tier-attempt entry snapshot may still capture which account-permanent modifier version entered the run for replay/audit, without making the derived result the only truth.

---

# 9. P2-C power-attribution ledger recommendation

Every authoritative damage/control/wall event should be explainable.

Candidate debug/simulation structure:

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
    scope
    statId
    operation
    value
  actionTransforms[]
    timingTier
    heavyOrPxP
    combo
    skillId
    critPolicy / critResult
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

Production network payload need not expose the full ledger every frame.
The authoritative simulator/test path must be able to emit it deterministically.

Benefits:
- when a Tier becomes too easy, identify whether STAR/ACHIEVEMENT/SHOP/SKILL/COMBO/CRIT caused it;
- compare class value of the same nominal stat;
- audit N3 and multihit budgets;
- debug multiplayer wall-defense stacking;
- preserve simulation/runtime parity.

---

# 10. Proposed canonical modifier schema

If the user approves the direction, P2 should author a machine-readable schema approximately like:

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
- `PCT_MULT_EXPLICIT` is opt-in, not default;
- a modifier may not silently choose multiplication because it comes from a different subsystem;
- `UNIQUE/MAX/OVERRIDE` must name a stack group;
- effect rules may carry `effectId` rather than pretending to be scalar stats;
- exact values may remain null/parameterized until their later calibration phase.

---

# 11. Options / recommendation summary

## Recommendation R1 — typed hybrid stacking
- ordinary same-stat progression bonuses aggregate additively;
- explicit action/effect multipliers remain separate;
- multiplication is opt-in by an approved contract, not an implicit subsystem boundary.

## Recommendation R2 — stat/effect separation
- scalar stats and mechanics/geometry/procs use different schema paths.

## Recommendation R3 — outgoing pipeline above
- construct attack first;
- apply persistent stats and action transforms;
- materialize hits;
- each target mitigates independently;
- isolated procs remain isolated.

## Recommendation R4 — defensive pipeline above
- generic DR -> unique class/team defense -> shield -> Base HP.

## Recommendation R5 — derived stats are derived
- source state authoritative;
- effective values recomputable / cache only.

## Recommendation R6 — attribution ledger mandatory for simulator/test
- production UI exposure optional;
- deterministic explanation path required.

## Recommendation R7 — delayed rounding
- one realized-hit rounding boundary;
- existing fixed-budget allocators preserved.

---

# 12. Risks / reversibility

### Benefits
- prevents automatic stars × achievements × shop snowball;
- preserves class-skill identity;
- supports exact cross-system sensitivity analysis;
- keeps future modifiers extensible;
- makes late balance defects attributable rather than mysterious.

### Costs
- more structured combat pipeline than one-line multiplier code;
- attack templates need explicit policies for multihit/crit/secondary effects;
- attribution instrumentation adds internal data volume.

### Reversibility
- schema/pipeline semantics become expensive to change after P3+ simulator and production data depend on them.
- therefore P2 should be structurally approved before P3.
- exact values, caps and reward magnitudes remain cheap to tune later because they are parameters.

---

# 13. Explicitly remains OPEN even if this proposal is approved

Approval of this architecture would **not** approve:
- exact star bonuses;
- exact achievement bonuses;
- exact shop values/prices/cadence;
- crit chance cap;
- generic defense cap;
- exact Base HP;
- exact Lv11+ production coefficients not already frozen;
- final Lv26/Lv31 contracts;
- exact per-skill crit inheritance where unresolved;
- exact boss values;
- multiplayer scaling values;
- exact modifier numeric representation.

Those remain downstream decision/calibration gates.

---

# 14. Requested user decision

Approve the recommended P2 architecture as a structural direction, or request changes to one or more of:
1. ordinary same-stat bonuses additive vs multiplicative;
2. stat/effect separation;
3. outgoing attack order;
4. defense-before-shield order;
5. derived-stat ownership;
6. mandatory attribution ledger;
7. delayed rounding policy.

Only after approval should this proposal be promoted into a structural contract and P3 unblocked.
