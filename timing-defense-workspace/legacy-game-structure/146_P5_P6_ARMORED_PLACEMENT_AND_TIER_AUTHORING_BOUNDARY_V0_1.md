# Timing Defense — P5/P6 Armored Placement Sensitivity & Tier Authoring Boundary V0.1

Date: 2026-10-24 KST  
Status: **DIAGNOSTIC RESULT + AUTHORITY CLARIFICATION / NO CONTENT ADOPTION / NO NUMERICAL FREEZE / NO PRODUCTION AUTHORITY**

Depends on:
- `02_TIER_SYSTEM.md`
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`
- `145_P5_P6_STAGE46_47_ARMORED_MIDWAVE_REPLACEMENT_DIAGNOSTIC_V0_1.md`

---

## 0. User interpretation that changes the diagnostic question

The user explicitly clarified two points.

### Late-run clear level
The current `SKILLED_V2_CENTRAL` late-segment completion level around the mid-40% range is not itself considered obviously too low, especially because the current all-PERFECT controls retain a 100% completion path in the tested Stage46→49 slice.

This does **not** numerically freeze `45%` as a target.
It changes the diagnostic framing from:

```text
raise skilled completion globally
```

to:

```text
understand how encounter composition/distribution exposes different class strengths
while preserving a meaningful skilled-vs-perfect mastery gap
```

### Tier authoring boundary
The current 9 ordinary monsters plus temporary armored proxy are being used to map mechanical interactions and encounter-response effects.
They are **not** a final Tier1 50-Stage roster packet.

When exact Tier1 Stage1→50 authoring begins, the active Tier availability / introduction design must be applied first.

---

# 1. Armored count result — retained from doc145

Existing `ARMORED_DURABLE_PROXY` only; no new monster/scalar authored.

Run:
- `39976475153`
- repeat deterministic bytes: PASS
- SHA256: `99f0c0e6a0137c1919b66754d7714d30b69a60e49cf37422296bff33b580d36c`

Stage46/47 only; GRUNT replacement; total body count unchanged; Stage48/49 unchanged.

Skilled through Stage49:

| Variant | Archer | Mage | Rogue | Knight | Tank | Total |
|---|---:|---:|---:|---:|---:|---:|
| BASELINE | 18/20 | 18/20 | 6/20 | 5/20 | 1/20 | 48/100 |
| 1 armored / Stage | 17/20 | 17/20 | 6/20 | 5/20 | 1/20 | 46/100 |
| 2 armored / Stage | 13/20 | 15/20 | 4/20 | 5/20 | 1/20 | 38/100 |

All-PERFECT: `5/5` classes through Stage49 in every variant.

Interpretation:

```text
ONE_SPARSE_ARMORED_BODY = selective pressure signal
MORE_ARMORED_COUNT       = broad pressure / diminishing balance value
```

Do not escalate armored count as the default repair.

---

# 2. Chronology sensitivity — COMPLETE

Temporary branch:
- `timing-defense-workspace-temp-armored-placement`

Run:
- `39978274698`
- repeat deterministic bytes: PASS
- SHA256: `5ab1f8f1ffe4480d4b3f9706aa3c2484bed718cb9742acf2b8c08ac2c822cfcf`

Rules:
- one armored proxy replaces one GRUNT in Stage46 and one in Stage47;
- total monster count unchanged;
- armored scalar unchanged;
- Stage48/49 unchanged;
- same 20 deterministic SKILLED_V2 seeds × five classes;
- all-PERFECT control retained.

Actual placement:

```text
EARLY
Stage46 15.34s band +2
Stage47 14.34s band +2

MID
Stage46 32.74s band +2
Stage47 30.24s band +2

LATE
Stage46 42.76s band -2
Stage47 46.14s band +2
```

Skilled through Stage49:

| Variant | Archer | Mage | Rogue | Knight | Tank | Total |
|---|---:|---:|---:|---:|---:|---:|
| BASELINE | 18 | 18 | 6 | 5 | 1 | 48 |
| EARLY | 16 | 16 | 6 | 4 | 1 | 43 |
| MID | 17 | 17 | 6 | 5 | 1 | 46 |
| LATE | 18 | 16 | 7 | 5 | 1 | 47 |

All-PERFECT: `5/5` in every variant.

Important isolation:
- EARLY and MID use the same `band +2` in both stages;
- therefore the EARLY→MID difference is a real chronology signal, not a band artifact;
- EARLY over-pressures Knight as well as Mage/Archer;
- MID produces the cleanest observed selective trim;
- LATE is mixed with a Stage46 band change and therefore was not accepted as pure chronology evidence.

Conclusion:

```text
ARMORED_CHRONOLOGY_IS_CAUSAL
EARLY_INSERTION = TOO_BROAD_IN_CURRENT_SAMPLE
MID_INSERTION   = CLEANEST_CURRENT_DIRECTIONAL_CENTER
```

This is not launch authoring.

---

# 3. Band sensitivity at fixed MID chronology — COMPLETE

Temporary branch:
- `timing-defense-workspace-temp-armored-band`

Run:
- `39978899281`
- repeat deterministic bytes: PASS
- SHA256: `f38153e883b03eb80991e08cf68beb9454e3d99d94bb14d4b50157c5cd34df50`

Fixed chronology:

```text
Stage46 32.74s
Stage47 30.24s
```

The same selected GRUNT was replaced, but the armored proxy band alone was forced to `-2 / 0 / +2`.

Skilled through Stage49:

| Variant | Archer | Mage | Rogue | Knight | Tank | Total |
|---|---:|---:|---:|---:|---:|---:|
| BASELINE | 18 | 18 | 6 | 5 | 1 | 48 |
| BAND -2 | 16 | 17 | 6 | 4 | 1 | 44 |
| BAND 0 | 18 | 17 | 6 | 5 | 1 | 47 |
| BAND +2 | 17 | 17 | 6 | 5 | 1 | 46 |

All-PERFECT: `5/5` in every variant.

Interpretation:
- `band -2` is too broad in the current abstraction because Archer and Knight both lose additional completion;
- `band 0` mainly trims Mage;
- `band +2` trims Mage and Archer while leaving Rogue/Knight/Tank unchanged in this 20-seed sample;
- therefore `MID + band +2` is the cleanest **diagnostic center** among the tested sparse placements.

Do not interpret one-case differences as final statistical balance authority.
The result is directional class-response evidence.

---

# 4. Stop rule — do not micro-optimize the proxy now

The current diagnostic axes are sufficiently separated:

```text
COUNT
0 / 1 / 2

CHRONOLOGY
EARLY / MID / LATE

GEOMETRY
band -2 / 0 / +2
```

Continuing to search exact seconds/bands before real Tier authoring would overfit a temporary Stage46–49 diagnostic fixture.

Therefore:

```text
ARMORED_COORDINATE_MICROTUNING = STOP
MID +2 = REFERENCE_DIAGNOSTIC_CENTER_ONLY
```

No exact armored placement or scalar is adopted.

---

# 5. What the current class split means

The current late-run class divergence must not automatically be translated into class buffs/nerfs.

Evidence now supports this interpretation:
- high-volume / clustered / aligned pressure naturally exposes Mage AoE and Archer penetration strengths;
- sparse hardened bodies can selectively trim those advantages;
- placement chronology and geometry materially alter which class is pressured;
- the same class may therefore look strong or weak depending on encounter composition.

This is consistent with the approved class-opportunity philosophy:

```text
Knight = mixed/reorder/generalist penetration
Rogue  = durable/high-value target focus
Tank   = control / wall-pressure management
Archer = aligned-line penetration
Mage   = cluster/density AoE
```

The project should map encounter-response surfaces before deciding that any class itself is numerically wrong.

---

# 6. Tier availability authority clarification

There is an old structural candidate:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`

It contains an earlier proposal that Tier1 would teach all nine ordinary monsters by Stage29.
That proposal is **not active authority**.

The later/higher authority documents are:
- `02_TIER_SYSTEM.md`
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

Their current direction is:

```text
T1 starts with a limited subset
-> higher Tier(s) introduce new monster archetypes
-> returning monsters are reinterpreted via formation/cadence/composition
-> current 9-monster foundation is not the final lifetime roster
```

Therefore any future session must treat the conflicting `09` all-nine-in-T1 sections as:

```text
SUPERSEDED_LEGACY_CANDIDATE
NOT_ACTIVE_TIER_AVAILABILITY_AUTHORITY
```

Exact Tier count and exact monster unlock ladder remain OPEN.

---

# 7. Current diagnostic vs future real Stage authoring

Current work:

```text
foundation roster + diagnostic proxy
-> learn distribution/composition/chronology/geometry effects
-> build reusable encounter-response knowledge
```

Future exact Tier1 Stage1→50 authoring:

```text
active Tier availability ladder
-> T1 introduced/available/returning monster set
-> Tier novelty budget and identity
-> Stage1..50 macro flow
-> only then exact frequency/count/composition/formation/cadence
```

The current Stage46–49 fixture must never be copied wholesale into Tier1 merely because it was useful for diagnostics.

`ARMORED_DURABLE_PROXY` remains a diagnostic proxy and is not automatically a new ordinary monster.

---

# 8. Next low-cost boundary

Do **not** continue armored second-by-second coordinate tuning.

Next diagnostic step should be an **encounter-composition class-response matrix** using already-existing evidence first:
- FLOOD / density;
- LINE / penetration;
- BULWARK / durable targets;
- control-sensitive pressure;
- protected SIEGE;
- chronology-sensitive Mage chain cases.

Goal:

```text
separate
CLASS_NUMERIC_PROBLEM
from
ENCOUNTER_COMPOSITION_ADVANTAGE
```

Only missing matrix cells should receive a new bounded simulation.
Do not rerun already-closed evidence.

This matrix work remains diagnostic/analysis work and does not formally enter P6 or adopt production values.

---

# 9. Authority boundary

Not approved by this document:
- exact `45%` skilled target;
- Stage46/47 armored insertion as final content;
- `MID + band +2` as launch placement;
- current proxy HP/armor/knock/speed/wall values;
- new monster identity / elite system;
- class buff or nerf;
- Tier1 exact monster roster;
- exact Tier count;
- exact Tier unlock ladder;
- Stage1→50 exact authoring;
- formal P6 start;
- any production gameplay/numerical change.

Production remains unchanged and unauthorized.
