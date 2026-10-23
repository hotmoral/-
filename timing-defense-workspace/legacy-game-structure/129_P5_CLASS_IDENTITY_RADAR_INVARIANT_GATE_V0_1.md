# Timing Defense — P5 Class Identity Radar Invariant Gate V0.1

Date: 2026-10-23 KST  
Status: **USER-DIRECTED STRUCTURAL IDENTITY GATE / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `../CHARACTER_PROFILE_RADAR_V1.md`
- `../DESIGN_DECISIONS.md`
- `../SKILL_PLAN_LV6_31.md`
- `41_CLASS_AWARE_ACTION_TRACE_MODEL_V0_1.md`
- `102_P4D2_DURABLE_TEMPORAL_PRESSURE_DIRECTIONAL_PROBE_V0_1.md`
- `124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`

Machine-readable companion:
- `data/p5_class_identity_radar_invariants_v0_1.yaml`

---

# 0. User direction

The user explicitly requested that current and future balance work be checked against the class identity already communicated in the character-selection radar.

The user also clarified Tank identity more strongly:

```text
Tank solo parity is not a target.
Tank should be very poor at solo clearing late content,
or clear so slowly / with so much backlog that solo play frequently feels inefficient.
```

This does **not** authorize a hard mechanical lockout, enemy immunity, or an impossible matchup.
The intended distinction is:

```text
Tank survival / wall protection = excellent
Tank enemy-removal throughput = poor
Tank solo clear time / backlog = materially worse than damage classes
```

A high-mastery Tank may eventually clear, but `survived the stress horizon` must never be interpreted as `healthy solo clear performance`.

---

# 1. Canonical radar profile

The approved V1 radar is a readability/identity graphic, not literal hidden coefficients.

| Class | ATK | CRIT | AGILITY | KNOCK | PEN | AOE |
|---|---:|---:|---:|---:|---:|---:|
| Knight | 4 | 2 | 3 | 3 | 4 | 2 |
| Rogue | 2 | 5 | 5 | 1 | 1 | 1 |
| Tank | 2 | 1 | 1 | 5 | 1 | 3 |
| Archer | 3 | 2 | 4 | 1 | 5 | 2 |
| Mage | 4 | 2 | 2 | 1 | 1 | 5 |

Interpretation for balance governance:
- level `5` = defining specialty must remain causally visible in gameplay;
- level `4` = strong supporting identity;
- level `3` = competent/neutral band;
- level `1` = intended weakness must not disappear through skill/shop/encounter interactions;
- equal radar values are allowed and do not imply exact numerical equality.

Do **not** derive production coefficients directly from these 1–5 values.

---

# 2. New invariant rule

Every P5+ combat/balance change must pass both:

```text
POSITIVE IDENTITY CHECK
Does the class win for the reason its high radar axes say it should?

NEGATIVE IDENTITY CHECK
Do the low radar axes still create a real limitation after skills/shop growth?
```

A class is not identity-valid merely because its win rate or wall survival is acceptable.

Examples of invalid conclusions:
- Tank survived 60 s -> therefore Tank solo balance is good.
- Archer cleared quickly -> therefore Archer is healthy, even if line geometry did not matter.
- Mage cleared quickly -> therefore Mage is healthy, even if dispersed enemies were no harder than clustered enemies.

---

# 3. Class-specific invariants

## Knight — frontline penetration generalist

Radar spine:
```text
ATK4 / PEN4 / AGILITY3 / KNOCK3
AOE2 / CRIT2
```

Must remain true:
- line/frontline penetration materially contributes to damage and target removal;
- broad blade waves may destabilize a front line but must not become Mage-like radial AoE;
- Knight should remain comparatively stable across formations without becoming best-in-class at every formation;
- defensive shop specialization may reduce clear speed, but successful defense-heavy Knight must not become a trap solely because Archer pressure was repaired.

Required paired probes:
- aligned/frontline vs dispersed/off-axis;
- penetration damage share / extra targets hit;
- active backlog and clear time under offense-heavy vs defense-heavy shop.

Current classification:
`STRUCTURALLY ALIGNED / DEFENSE_HEAVY_OVERPRESSURE_WATCH ACTIVE`.

## Rogue — crit/agility single-durable execution

Radar spine:
```text
CRIT5 / AGILITY5
ATK2 / KNOCK1 / PEN1 / AOE1
```

Must remain true:
- power comes from fast repeated hits, crit, cadence and durable-normal target execution;
- same-target multihit may be extreme;
- low AOE/PEN/KNOCK must remain real weaknesses;
- Dagger Storm / generated daggers must not silently turn into general wave-wide cleanup through unlimited retarget chaining.

Required paired probes:
- one durable normal target vs dense weak cluster;
- damage concentration on primary/durable target;
- number of distinct targets reached by one root package;
- clear time and backlog in multi-direction swarm pressure;
- crit/cadence contribution once CRIT/CRITDMG policy lane exists.

Current classification:
`STRUCTURALLY ALIGNED / LV31_WAVE_CLEANUP_LEAKAGE_WATCH`.

## Tank — team-specialist time buyer / wall protector

Radar spine:
```text
KNOCK5 / AOE3
ATK2 / CRIT1 / AGILITY1 / PEN1
```

Must remain true:
- survival advantage comes from displacement, slow, barrier and wall mitigation;
- enemy removal throughput remains poor relative to damage classes;
- Tank may preserve the wall while leaving a large enemy backlog;
- solo parity is not required;
- late solo clear should be near-impractical under ordinary tempo or materially slower/frustrating than damage classes, while avoiding absolute class lockout.

Critical interpretation rule:
```text
SURVIVAL != CLEAR
WALL PRESERVATION != DAMAGE THROUGHPUT
```

Required metrics:
- wall reserve;
- displacement / slowed time;
- enemy wall contacts prevented;
- kills and damage;
- active backlog at stress-horizon end;
- actual time-to-last-enemy / stage completion;
- unfinished-at-horizon rate;
- relative solo clear-time ratio vs damage classes.

Current evidence:
- control ablation strongly confirms Tank survival is control-driven;
- current P5 late probes mostly measured wall survival, not full solo clear time.

Current classification:
`POSITIVE IDENTITY CONFIRMED / NEGATIVE IDENTITY VALIDATION GAP`.

No Tank damage nerf is authorized by this classification alone. First measure solo throughput/clear-time correctly.

## Archer — strict-line penetration specialist

Radar spine:
```text
PEN5 / AGILITY4 / ATK3
KNOCK1 / AOE2 / CRIT2
```

Must remain true:
- line alignment and rear-target access materially determine realized power;
- straight-line semantics remain strict: no bending, homing or off-line retarget;
- Archer may erase a well-aligned line spectacularly;
- scattered/off-corridor threats must reduce efficiency materially;
- ordinary ATK growth must not make line geometry irrelevant and turn Archer into a formation-agnostic generalist.

Required paired probes:
- aligned line vs staggered/scatter/off-corridor;
- penetration target count and penetration damage share;
- off-corridor SIEGER exposure;
- repeated-final-failure reserve under ATK-heavy shop;
- breakpoint chronology around one-hit thresholds.

Current classification:
`CORE IDENTITY STRUCTURALLY PRESENT / POST_SHOP GENERALIST-CREEP HIGH WATCH`.

Do not solve with hidden Archer shop penalties before packet chronology and geometry are exhausted.

## Mage — density/AoE specialist

Radar spine:
```text
AOE5 / ATK4
AGILITY2 / CRIT2 / KNOCK1 / PEN1
```

Must remain true:
- clustered density produces very high payoff;
- distributed durable/off-cluster pressure materially reduces efficiency;
- chain/cascade behavior rewards grouping rather than becoming universal single-target DPS;
- low PEN/KNOCK remain real limitations.

Required paired probes:
- clustered durable vs distributed durable;
- secondary/chain damage share;
- unique targets reached per root package;
- clear time/backlog under cluster vs scatter;
- durable single-target time-to-kill.

Current evidence already shows:
- distributed durable pressure strains Mage heavily;
- clustered durable pressure restores Arcane Collapse payoff.

Current classification:
`STRONGLY ALIGNED / POST_SHOP LATE-PRESSURE MARGIN WATCH`.

---

# 4. P5 admission changes

The current Stage46–49 source-patched right-edge runner must no longer report only:
- alive/dead;
- wall reserve;
- final-miss budget.

It must add identity outputs sufficient to answer:

```text
Knight -> did penetration/frontline break cause the result?
Rogue  -> was damage concentrated and fast rather than broad wave cleanup?
Tank   -> how long did it take to actually finish, and how much backlog remained?
Archer -> did straight-line alignment materially matter?
Mage   -> did density materially matter?
```

Minimum additional outputs:
```text
stageClearTime
unfinishedAtHorizon
totalKills
totalDamage
endActiveBacklog
uniqueTargetsPerRootPackage
secondaryDamageShare
penetrationHitCount / penetrationDamageShare when applicable
controlDisplacementOrSlowTime when applicable
wallContactsPrevented when measurable
formationTag / alignmentTag / densityTag
```

No exact numeric pass thresholds are frozen by this document.
First collect comparable distributions under the current deterministic diagnostic brackets.

---

# 5. Stop conditions

Stop packet tuning and report before numerical repair if any of the following appears:

1. Tank has high wall survival **and** damage-class-like solo clear time.
2. Archer performs similarly in aligned and scattered/off-corridor probes.
3. Mage performs similarly in dense and distributed durable probes.
4. Rogue Lv31 root packages routinely clear broad multi-direction waves despite AOE1/PEN1.
5. Knight becomes the best solution to both dense AoE and single-durable execution rather than remaining a stable penetration generalist.
6. A proposed Stage49 repair fixes one class only by destroying another class's intended specialization/weakness.

When triggered, repair order is:
```text
simulator fidelity
-> encounter geometry/timing
-> package semantics
-> shop interaction
-> exact scalar values last
```

---

# 6. Relationship to current P5 watches

Keep existing:
- `P5_ATK_HEAVY_ARCHER_REPEATED_FAILURE_MARGIN_WATCH`
- `P5_DEFENSE_HEAVY_KNIGHT_OVERPRESSURE_WATCH`
- `P5_RIGHT_EDGE_ESCORT_PACKET_CHRONOLOGY_WATCH`

Add:
- `P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE`
- `P5_TANK_SURVIVAL_NOT_CLEAR_WATCH`
- `P5_TANK_SOLO_CLEAR_THROUGHPUT_WATCH`
- `P5_ROGUE_WAVE_CLEANUP_LEAKAGE_WATCH`
- `P5_ARCHER_LINE_DEPENDENCE_WATCH`
- `P5_MAGE_DENSITY_DEPENDENCE_WATCH`
- `P5_KNIGHT_PENETRATION_CAUSALITY_WATCH`

---

# 7. Verdict / next boundary

```text
RADAR_PROFILE = PROMOTED_TO_BALANCE_IDENTITY_GUARD
RADAR_VALUES = NOT DIRECT COMBAT COEFFICIENTS
HIGH_AXES = MUST REMAIN CAUSALLY VISIBLE
LOW_AXES = MUST REMAIN REAL LIMITATIONS
TANK_SURVIVAL_EQUALS_CLEAR = REJECTED
TANK_SOLO_PARITY = NOT REQUIRED
TANK_ABSOLUTE_HARD_LOCKOUT = NOT REQUIRED / NOT AUTHORIZED
CURRENT_KNIGHT = STRUCTURALLY_ALIGNED_WITH_WATCH
CURRENT_ROGUE = STRUCTURALLY_ALIGNED_WITH_WATCH
CURRENT_TANK = POSITIVE_IDENTITY_CONFIRMED_NEGATIVE_IDENTITY_VALIDATION_GAP
CURRENT_ARCHER = HIGH_POST_SHOP_IDENTITY_WATCH
CURRENT_MAGE = STRONGLY_ALIGNED_WITH_WATCH
PRODUCTION_CHANGE = NO
NUMERICAL_FREEZE = NO
```

Next P5 work must integrate these outputs into the source-patched Stage46–49 right-edge lane **before** promoting a Stage49 packet as a balance candidate.
