# Timing Defense — Encounter Composition × Class Response Matrix V0.1

Date: 2026-10-24 KST  
Status: **DIAGNOSTIC SYNTHESIS / EXISTING-EVIDENCE MATRIX / NO BALANCE ADOPTION / NO NUMERICAL FREEZE / NO PRODUCTION AUTHORITY**

Depends on:
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`
- `44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`
- `89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `131_P5_CLASS_IDENTITY_FIRST_DIRECTIONAL_RESULT_V0_1.md`
- `132_P5_TANK_CONTROL_CLEAR_PARETO_DIRECTION_V0_1.md`
- `133_P5_ROGUE_DAGGER_STORM_BROAD_CLEANUP_BREAKPOINT_V0_1.md`
- `134_P5_KNIGHT_PENETRATION_ROBUST_IDENTITY_PROBE_V0_1.md`
- `135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
- `141_P5_STAGE48_ARMORED_LOW_DENSITY_AND_GLOBAL_STANDOFF_RESULT_V0_1.md`
- `142_P5_STAGE48_FODDER_CHAIN_AND_GLOBAL_STANDOFF_BOUNDARY_RESULT_V0_1.md`
- `145_P5_P6_STAGE46_47_ARMORED_MIDWAVE_REPLACEMENT_DIAGNOSTIC_V0_1.md`
- `146_P5_P6_ARMORED_PLACEMENT_AND_TIER_AUTHORING_BOUNDARY_V0_1.md`

---

# 0. Question

Current Stage46–49 central-skilled diagnostics show a large class spread.
The user correctly questioned whether the late encounter composition itself explains much of this spread because the current late fixture contains sustained high-volume, clustered and aligned pressure.

This matrix asks:

```text
Is the current class spread evidence of intrinsic class numerical imbalance?
OR
Is much of it the expected consequence of encounter-family distribution?
```

This document does not attempt to equalize class clear rates.
It maps which encounter shapes naturally expose each class's approved strengths and weaknesses.

---

# 1. Reading legend

Response classification:

```text
++ = strong structural advantage / defining specialty
 + = directional advantage
 0 = broadly neutral or strongly conditional
 - = directional disadvantage / intended weakness
-- = strong structural disadvantage in the relevant output axis
```

Important:
- Tank frequently has two outputs: `REMOVAL` and `OBJECTIVE/CONTROL`; these must not be collapsed.
- Archer response depends strongly on alignment.
- Mage response depends strongly on density/cluster.
- Rogue can cross a shop breakpoint where Dagger Storm temporarily leaks into broad cleanup; this is a WATCH, not the intended identity.
- these are structural/directional classifications, not frozen production coefficients.

---

# 2. Matrix — current best evidence

| Encounter pressure | Knight | Rogue | Tank | Archer | Mage |
|---|---|---|---|---|---|
| **FLOOD / high-density volume** | `0/+` | `-`* | `REMOVAL -- / CONTROL +` | `+ if aligned / 0 if scattered` | `++` |
| **LINE / aligned depth** | `+` | `-/0` | `-` removal | `++` | `0/+ only if also clustered` |
| **BULWARK / durable frontline** | `+` | `++` durable focus | `REMOVAL - / CONTROL +` | `+ if line access; armor-ignore on qualifying PERFECT` | `- if distributed / + if clustered` |
| **CONTROL-SENSITIVE / CHARGER, knock, wall tempo** | `+` | `0/-` | `++` | `0/-` | `0/-` |
| **PROTECTED SIEGE / screened backline** | `+ / conditional` | `0 / front-clear dependent` | `OBJECTIVE ++ / REMOVAL -` | `++ when line exists` | `+ if clustered; chronology can bypass protection` |
| **LATE-LIVE / chronology-sensitive secondary access** | `0` | `0/+ conditional retarget` | `0` | `0 / strict line only` | `++ confirmed` |

`*` Rogue FLOOD caveat: current Dagger Storm per-dagger damage plus late shop ATK can cross the fresh-GRUNT one-shot breakpoint, letting retargeting serially clean many weak bodies. This is a confirmed leakage watch and should not be mistaken for the intended AOE1 identity.

---

# 3. FLOOD / high-density volume

## Mage — strong expected advantage

Evidence:
- `131`: clustered finite packet `~3.78 s` vs distributed `~8.08 s`, about `2.14x` separation;
- `135`: Mage density identity strongly aligned;
- `145/146`: adding one sparse armored body to Stage46/47 selectively reduced Mage completion without changing class scalar.

Interpretation:

```text
DENSE_CLUSTERED_VOLUME -> MAGE_SPECIALTY_SURFACE
```

Therefore a late fixture dominated by dense mass pressure is not a class-neutral test.

## Archer — conditional advantage

Archer does not inherently love density; it loves **alignment/depth**.
If high-volume pressure forms repeated lines/corridors, density and line access combine into a strong advantage.
If volume is scattered/off-corridor, Archer efficiency falls materially.

## Rogue — intended weakness, with breakpoint leakage

Rogue is supposed to excel at concentrated repeated-hit execution rather than broad wave cleanup.
However `133` confirms current diagnostic shop power can make one Dagger Storm dagger one-shot GRUNT-like bodies, causing serial retarget cleanup.
That is an identity watch, not a reason to call Rogue a FLOOD specialist.

## Tank — survival/control and removal diverge

Tank can slow/push a mass and protect the wall, but low removal throughput means sustained inflow can create backlog.
Thus:

```text
FLOOD survival/control may be viable
while FLOOD clear/removal remains poor
```

This explains why Tank can look extremely weak in a completion-rate-only late-run fixture without proving its core role is numerically broken.

## Knight — stable but not density specialist

Knight penetration/frontline break helps repeated front rows, but AOE is intentionally lower than Mage and line depth lower than Archer specialty.
Expected response is competent/conditional rather than dominant.

---

# 4. LINE / aligned depth

## Archer — defining advantage

`131` finite probe:

```text
aligned ~= 3.58 s
scatter ~= 8.08 s
scatter/aligned ~= 2.26x
```

This is one of the strongest existing geometry signals.
Archer is expected to look very strong when the encounter repeatedly feeds aligned depth.

## Knight — clear supporting advantage

Refined five-durable-body probe `134`:

```text
BALANCED:
aligned   9.20 s
dispersed 12.575 s
ratio ~= 1.367x
```

Penetration causality remains visible without turning Knight into the best specialist.

## Rogue / Tank

Low PEN is an intended limitation. They can still attack the front body, but aligned rear depth does not create the same efficiency multiplier.

## Mage

Alignment itself is not the defining variable. Mage benefits if aligned bodies are also close enough to form cluster/AOE opportunities.

---

# 5. BULWARK / durable frontline

## Rogue — defining positive surface

Existing identity evidence supports:

```text
fast repeated hits + multihit + crit/cadence
-> durable/high-value normal target execution
```

Dagger Storm can concentrate remaining daggers on a surviving durable target.
This is the intended opposite of Rogue's weak broad-AOE identity.

## Knight — positive generalist/penetration surface

The refined durable aligned packet confirmed that Knight remains effective when durable front bodies form a penetrable front line.

## Tank — time buyer, not remover

Tank can displace/slow durable bodies and reduce objective pressure, but should not erase them at damage-class speed.
`131/132` actually found the provisional `0.75` Tank Lv31 shockwave damage too high for this negative identity; the diagnostic `0.20/0.25/0.30` bracket exists to preserve control while reducing removal.
No value is frozen.

## Archer — conditional

Archer can do very well when durable bodies are aligned because line penetration remains valuable and qualifying PERFECT semantics include armor-ignore.
Dispersed durable pressure should reduce this advantage.

## Mage — strongly composition-dependent

`129/131/135` show:
- clustered durable = Arcane Collapse payoff restored;
- distributed durable = material Mage weakness.

Therefore `BULWARK` alone is not enough to predict Mage outcome; spatial distribution matters.

---

# 6. CONTROL-SENSITIVE pressure

Primary examples:
- CHARGER windup/interruption;
- knock-sensitive approach;
- wall-danger time;
- SIEGER reposition/approach control.

## Tank — defining advantage

Tank's high KNOCK/control is expected to produce:
- stronger displacement;
- slow time;
- wall contacts prevented;
- more time before objective damage.

The early Layer-A default CHARGER recipes actually starved this opportunity because CHARGER died before windup. `44` later demonstrated a real activation window where positive knock can interrupt windup once the mechanic is allowed to express.

Tank is not the only class allowed to interrupt; it should be the strongest/most reliable control specialist.

## Knight — supporting advantage

Knight has moderate knock and penetration, so it can contribute meaningfully without owning the specialty.

## Rogue / Archer / Mage

Their main answer is usually removal/preemption rather than dedicated displacement. If an encounter is intentionally authored around sustained control value rather than pure delete speed, these classes should not receive Tank-level benefit for free.

Evidence confidence here is **structurally high, quantitative-central-skilled medium** because many early CHARGER fixtures erased the mechanic before it could be measured.
No new probe is required yet to answer the current Stage46/47 composition question.

---

# 7. PROTECTED SIEGE / screened backline

This row must separate two jobs:

```text
A. reach/remove the protected backline threat
B. protect the wall / buy time if it remains alive
```

## Archer — backline access advantage

Strict-line penetration can reach through a screen when geometry aligns.
`141` showed spatial separation materially changes Archer's ability to reach/protect against SIEGER, proving the interaction is geometry-sensitive rather than generic DPS.

## Tank — objective-control advantage, low removal

Tank can slow approach/reposition and preserve wall reserve, but low removal means it may leave SIEGER or its screen alive longer.
This is a feature/limitation pair, not a contradiction.

## Knight — moderate screen-breaking/reposition contribution

Penetration and moderate knock give Knight more screen interaction than low-PEN classes, but not Archer-level strict backline access or Tank-level control.

## Rogue — front-clear dependent

Rogue can efficiently execute a durable front body, potentially exposing SIEGER, but lacks native penetration/control specialty.
Its value depends on whether removing the screen fast enough creates backline access before objective pressure accumulates.

## Mage — cluster plus chronology

Mage may erase a clustered screen strongly, but Stage48 evidence shows an additional behavior: delayed/chain effects can reach SIEGER according to live chronological target state even when simple spatial screening would protect it from Archer.
Thus Mage's protected-SIEGE interaction is not captured by geometry alone.

---

# 8. LATE-LIVE / chronology-sensitive target access

This row exists because Stage48 diagnostics proved:

```text
SPATIAL_SCREENING != TEMPORAL_SCREENING
```

Mage:
- strongest confirmed chronology-sensitive interaction;
- an already-running bounded package/chain can acquire later live/unhit targets;
- fodder type/order/arrival phase changes whether SIEGER becomes the chain target.

Archer:
- strict line; no homing/off-line retarget; mostly spatial rather than temporal access.

Rogue:
- deterministic retarget after target death can create limited chronology sensitivity while a Dagger Storm package remains active;
- evidence is enough to flag conditional behavior but not enough to call Rogue a late-live specialist.

Knight/Tank:
- no equivalent confirmed late-live secondary-target specialty in current evidence.

`142` confirms for Mage:

```text
FODDER_COUNT_ALONE != SOLUTION
FODDER_TYPE + ORDER + ARRIVAL_PHASE = CAUSAL
```

---

# 9. What the current Stage46/47 class split now means

Current fidelity-bridge central-skilled late slice at entry charge 0:

```text
Archer 18/20
Mage   18/20
Rogue   6/20
Knight  5/20
Tank    1/20
```

The encounter-response matrix shows this ordering is **compatible with the current fixture's pressure shape**:

- high sustained entity volume strongly rewards Mage density clearing;
- repeated alignment/depth strongly rewards Archer penetration;
- Rogue's intended strength is durable/high-value execution, not sustained broad flood;
- Tank's intended strength is objective/control, not solo removal;
- Knight is a stable penetration generalist, not the peak density or line specialist.

The sparse-armored tests then changed only encounter composition and moved Mage/Archer outcomes while leaving class scalars untouched.
This is direct evidence that at least part of the late-run class spread is **encounter-composition induced**.

Therefore:

```text
CURRENT_CLASS_SPREAD
!=
PROOF_OF_INTRINSIC_CLASS_NUMERIC_IMBALANCE
```

and:

```text
ENCOUNTER_COMPOSITION_ADVANTAGE
= MATERIAL_CONFIRMED_CAUSE
```

This does **not** prove every class scalar is perfect.
It means scalar repair is not yet justified from the current Stage46/47 split.

---

# 10. Confidence / missing evidence

## Sufficiently supported for current decision

High confidence:
- Mage cluster/density advantage;
- Mage distributed-durable weakness;
- Archer aligned-line advantage;
- Archer scatter/off-corridor weakness;
- Knight penetration/generalist advantage;
- Rogue durable-target concentration identity;
- Tank control/wall-protection identity vs low removal identity;
- sparse hardened-body composition can selectively change Mage/Archer late outcomes;
- chronology/geometry change class response materially.

Medium confidence / future calibration need:
- exact quantitative Tank advantage in a fully expressed SKILLED_V2 CHARGER encounter;
- exact Rogue value in long protected-SIEGE sequences;
- exact Knight contribution in multi-cycle protected-SIEGE sequences;
- exact Tier-wide opportunity frequency required for each class.

These medium-confidence cells do **not** block the current conclusion that encounter composition materially explains the observed Stage46/47 skew.

Therefore no new simulation is required at this matrix step.

---

# 11. Current design implication

The next balance problem is not:

```text
make every class have the same Stage46-49 clear rate
```

It is:

```text
Across the eventual Tier roster and 50-Stage distribution,
are favorable / neutral / unfavorable encounter families distributed intentionally
so every class has meaningful strengths, real weaknesses and no hard lockout?
```

This is an **authoring-distribution problem first**, then a numerical convergence problem.

A good Tier may intentionally contain:
- Mage-favorable dense stages;
- Archer-favorable line stages;
- Rogue-favorable durable-target stages;
- Tank-favorable control/objective stages;
- Knight-favorable mixed/frontline stages;
- neutral/recovery stages;
- unfavorable mastery checks for each class.

It must not make one favorable family dominate so heavily that one class's specialty becomes the Tier's default answer.

---

# 12. Relationship to future Tier1 authoring

This matrix is reusable authoring knowledge.
It does **not** define the Tier1 monster roster.

Actual Tier1 authoring still requires:

```text
active monster availability/unlock ladder
-> T1 available subset
-> T1 novelty/identity
-> 50-Stage macro flow
-> encounter-family opportunity distribution
-> exact stage composition only after those are chosen
```

If a pressure family needs a monster that is not available in T1, Tier1 must express the intended learning/pressure using its allowed subset or defer that pressure to a later Tier.

---

# 13. Next boundary

The class-response matrix is sufficiently complete for the current diagnostic question.

Do not run broad additional class-balance simulation now.
Do not tune armored coordinates further.
Do not buff/nerf classes from the Stage46/47 aggregate split.

Next useful structural unit is to define an **encounter-opportunity distribution framework** for future Tier authoring:
- how to count favorable / neutral / unfavorable pressure exposure by class;
- how to detect one-family dominance;
- how to preserve class weaknesses without hard lockout;
- how to use recovery/readability stages;
- how this framework plugs into the still-open Tier monster availability ladder.

That framework can be specified diagnostically without selecting the exact Tier1 unlock ladder.

Exact Tier1 roster, exact stage frequency, class/monster numbers and formal P6 entry remain approval-gated.
