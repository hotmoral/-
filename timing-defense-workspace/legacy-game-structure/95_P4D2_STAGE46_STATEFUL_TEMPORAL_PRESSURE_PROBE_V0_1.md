# Timing Defense — P4-D2 Stage46 Stateful Temporal Pressure Probe V0.1

Date: 2026-10-23 KST  
Status: **BOUNDED STATEFUL STRESS DIAGNOSTIC / CANDIDATE PRESSURE ENVELOPE FOUND / ARCHER GEOMETRY DECISION PENDING / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Authority:
- `88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `92_P4D2_LV31_MASTERY_POWER_AND_STAGE46_PRESSURE_PREFLIGHT_V0_1.md`
- `93_P4D2_FIRST_PASS_LV31_POWER_ENVELOPE_AND_PRESSURE_TARGETS_V0_1.md`
- `94_P4D2_LV31_CURRENT_ROSTER_PRESSURE_RESPONSE_PROBE_V0_1.md`
- `../MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
- `63_HIGH_MASTERY_H0_OBSERVED_TRACE_REPORT_V0_1.md`
- `64_HIGH_MASTERY_H3_OBSERVED_TRACE_REPORT_V0_1.md`

Replay assets:
- `../../tools/run_p4d2_stage46_temporal_pressure_probe_v0_1.py`
- `data/p4d2_lv31_pressure_probe_fixture_v0_1.json`
- `data/p4d2_stage46_temporal_pressure_fixture_v0_1.json`
- `data/p4d2_stage46_temporal_pressure_summary_v0_1.json`

Expected full generated JSON SHA-256:

```text
110ea2beb87dabb41b4d8dd48af61bbe97e21666413481a9f19df95507c75e75
```

Committed runner Git blob SHA:

```text
5965833f80422bd6cae94fea738706baf99a06e8
```

---

# 0. Admission question

Can the user-approved late-run philosophy actually be expressed with the current nine-monster grammar?

Specifically:

> Can a Stage46-like pressure regime bury even all-PERFECT Lv26 play while allowing repeated Lv31 P×P finals to stabilize the same pressure, without adding a code-level Lv31 requirement?

Answer:

**YES — a bounded candidate pressure envelope was found.**

Within the current diagnostic 60-second stress envelope:

```text
all five classes at Lv26 + every input PERFECT -> buried
all five classes at Lv31 + every Heavy completed P×P -> survived
```

Classification:

`CANDIDATE_PRESSURE_ENVELOPE_FOUND`

This is the first direct P4-D2 evidence that the desired design can exist as actual combat pressure rather than an artificial level lock.

It does **not** freeze the exact Stage46 recipe, duration, cadence, monster counts, class coefficients, or final EXP model.

---

# 1. Probe boundary

The temporal fixture deliberately models a stress envelope, not final campaign authoring.

Diagnostic inputs:

```text
duration = 60s
wall = 2000
pressure cycle = 4.6s
12 staggered bodies per cycle
root timing action interval = 1.125s
Heavy/P×P = every 4th root action
current nine monster types all represented
five abstract probe bands for geometry only
RNG = NONE
```

The 4.6s pressure cycle and 1.125s root cadence are motivated by high-mastery H0/H3 evidence, where completed P×P opportunities occurred around every 4.49–4.69 seconds.

Important:
- this player evidence is upper-tail stress evidence, not an ordinary-skilled population fit;
- the five probe bands are not production lanes;
- `12 bodies / 4.6s` is not a Stage46 spawn prescription;
- the purpose is to test whether a gate-separation region exists at all.

---

# 2. Core gate-separation result

## Lv26 + all PERFECT

Even with every timing input treated as PERFECT, all five classes eventually lost the wall:

| Class | Burial time |
|---|---:|
| Rogue | **28.65s** |
| Tank | **33.25s** |
| Knight | **35.80s** |
| Archer | **52.65s** |
| Mage | **56.25s** |

This is the desired qualitative late-band property:

```text
perfect execution of the lower kit
!=
indefinite stabilization of Stage46 pressure
```

The player is not rejected by a level-check condition. The battlefield itself outgrows Lv26 clearing/control capacity.

## Lv31 + every P×P successful

With current P4-D2 Lv31 working centers, all five survived the same 60-second stress:

| Class | Wall HP at 60s | Active enemies at 60s | Max active | Kills |
|---|---:|---:|---:|---:|
| Knight | 1175 | 19 | 24 | 152 |
| Rogue | 1330 | 24 | 28 | 153 |
| Tank | 2000 | 9 | 16 | 174 |
| Archer | 2000 | 9 | 16 | 172 |
| Mage | 2000 | 4 | 13 | 179 |

Thus the desired loop is feasible:

```text
late pressure exceeds Lv26 steady-state capacity
-> Lv31 P×P creates a major reset
-> pressure rebuilds
-> the player must keep executing P×P correctly
```

This supports the user's `Lv31 없으면 파묻히고, 얻으면 시원하게 쓸어버리는` late-run direction.

---

# 3. Rogue — 16-dagger center receives strong support

Temporal sensitivity:

| Dagger count | Result | End wall | End active | Max active | Kills |
|---:|---|---:|---:|---:|---:|
| 12 | **buried at 41.90s** | 0 | 28 | 30 | 82 |
| **16** | **survives under pressure** | 1330 | 24 | 28 | 153 |
| 20 | largely dominates fixture | 2000 | 5 | 11 | 178 |

This is stronger evidence than static package arithmetic alone.

Interpretation:
- 12 is not enough for this candidate Stage46 pressure envelope;
- 16 crosses into survivable but still pressured territory;
- 20 removes most residual pressure and approaches trivialization for this specific stress recipe.

Therefore:

**16 remains the preferred P4-D2 working center.**

This is still not a production freeze.

It also validates the user's design intent: Dagger Storm can remain visually and mechanically abundant without requiring uncontrolled recursion.

---

# 4. Knight — second full wave 1.00 remains a useful center

Sensitivity:

| Second wave | End wall | End active | Max active | Kills |
|---:|---:|---:|---:|---:|
| 0.75 | 345 | 23 | 28 | 138 |
| **1.00** | **1175** | **19** | **24** | **152** |
| 1.25 | 1175 | 19 | 24 | 152 |

The result gives a useful threshold:
- 0.75 is barely holding the pressure;
- 1.00 creates a meaningful final-skill jump;
- 1.25 does not improve this fixture because current provisional targets saturate.

Do not infer that 1.25 is universally useless. It only means the next useful discriminator is state/geometry/replenishment, not another static damage increase.

Working center remains:

`second wave = 1.00 root basis`

Unfrozen.

---

# 5. Tank — control package is already very strong; role-aligned probe still required

Sensitivity at knockback ×2.5:

| Shockwave damage | End wall | End active | Max active | Kills |
|---:|---:|---:|---:|---:|
| 0.50 | 2000 | 18 | 23 | 163 |
| **0.75** | **2000** | **9** | **16** | **174** |
| 1.00 | 2000 | 8 | 15 | 175 |

The .75 center already removes most incremental pressure; 1.00 adds little in this fixture.
Knockback 2.5 also remains adequate; higher values mostly saturate here.

However the generic mixed schedule often lets Tank eliminate CHARGER/SIEGER before their explicit state window begins. Therefore this run cannot prove the actual `WINDUP interrupt` / `SIEGER reposition` value of final knockback.

Next required Tank evidence is **targeted role alignment**, not raw coefficient escalation.

Working center remains provisional:

```text
shockwave damage .75
knockback ×2.5
barrier 250 / 6s candidate
```

---

# 6. Archer — second material finding: magnitude alone is not enough

Document 94 already found a magnitude-continuity defect:
- Lv26 durable aligned-target Triple Shot package = `1.00 + .65 + .65 = 2.30`;
- a Lv31 arrow at only 1.00 per target regresses durable-target burst;
- therefore 2.30 became the non-frozen per-target continuity center.

The temporal probe found a **different** problem.

## Narrow strict-width probe

Keeping the Lv31 gameplay intersection width as narrow as the ordinary line, damage coefficient did not solve the distributed-pressure case:

| Per-target coefficient | Result |
|---:|---|
| 1.00 | buried 52.65s |
| 1.50 | buried 52.65s |
| 2.00 | buried 52.65s |
| 2.30 | buried 52.65s |

Once the arrow already kills what it intersects, more damage cannot solve enemies distributed just outside that narrow line.

This is a geometry limitation, not a raw-damage limitation.

## Modestly wider but still straight corridor candidate

The probe then allowed the **huge final arrow** to intersect the immediately adjacent diagnostic bands while remaining one locked straight, non-homing projectile.

| Width candidate | Coeff | End wall | End active | Max active | Kills |
|---|---:|---:|---:|---:|---:|
| wider straight | 1.00 | 1930 | 10 | 19 | 170 |
| wider straight | 1.50 | 2000 | 9 | 16 | 172 |
| wider straight | 2.00 | 2000 | 9 | 16 | 172 |
| wider straight | 2.30 | 2000 | 9 | 16 | 172 |

The dominant variable is therefore **gameplay width**, not further coefficient inflation.

### Proposed interpretation — NOT YET APPROVED

`Sky-Piercing Arrow` is described as a **huge** high-speed final arrow.
A modestly larger gameplay corridor is thematically coherent if it remains:
- a single locked straight shot;
- no homing;
- no bending;
- no off-line retarget;
- unlimited depth only inside its actual straight corridor.

This would preserve Archer's line-deletion identity while making the word `huge` mechanically meaningful rather than purely visual.

However document 90 originally proposed that visual size should not automatically widen gameplay collision. Changing that clause is a **material structural choice**.

Therefore P4-D2 may test the wider corridor as a candidate, but it must **not be frozen without explicit user approval**.

Archer per-target `2.30` also remains unfrozen.

---

# 7. Mage — .75 / radius1.25 remains a useful center, but geometry/chronology matter more than raw max damage

Sensitivity:

| Stage coeff / radius | End active | Max active | Kills |
|---|---:|---:|---:|
| .55 / 1.25 | 8 | 12 | 175 |
| .75 / 1.00 | 10 | 17 | 171 |
| **.75 / 1.25** | **4** | **13** | **179** |
| .75 / 1.50 | 7 | 13 | 176 |
| 1.00 / 1.25 | 4 | 13 | 179 |

Observations:
- .75 is materially better than .55 in this temporal fixture;
- 1.00 largely saturates against the current provisional anchors;
- larger radius is not monotonically better because death/spawn chronology and target ordering change which enemies are present at later stages.

This is a desirable result for a staged spell.
Do not simply maximize radius/damage.

Working center remains:

```text
stage coefficient .75
radius sensitivity center 1.25
```

Unfrozen, with SPLITTER chronology still an explicit watch.

---

# 8. P×P miss sensitivity — the next Stage48–49 authoring problem

The same fixture injected one missed Heavy/P×P opportunity and two consecutive missed opportunities.

## One miss

| Class | End wall | Burial |
|---|---:|---|
| Knight | 900 | no |
| Rogue | **175** | no, near-terminal |
| Tank | 1981 | no |
| Archer | 2000 | no |
| Mage | 2000 | no |

## Two consecutive misses

| Class | End wall | Burial |
|---|---:|---|
| Knight | **255** | no, near-terminal |
| Rogue | **0** | **49.70s** |
| Tank | 1837 | no |
| Archer | 1940 | no |
| Mage | 2000 | no |

This shows substantial **miss-severity class divergence**.

Interpretation:
- Rogue and Knight depend much more directly on each final reset in this mixed recipe;
- Tank/Archer/Mage retain more recovery margin because of control/geometry/AoE properties;
- this does not justify hidden per-class buffs, hidden XP correction, or automatic nerfs to strong classes.

First repair layer must be encounter grammar:
- rotate line / cluster / frontline / dispersed pressure;
- protect SUPPORTER/SIEGER differently across cycles;
- use CHARGER/SPLITTER rebound windows;
- make Stage48–49 repeated-miss pressure punish all classes through **different vulnerabilities**, not identical raw HP taxes.

Stage46–47 may intentionally allow one miss to remain recoverable.
Stage48–49 can tighten this toward the user-approved burial-cascade mastery requirement.

---

# 9. Monster role-expression watch

In the all-success Lv31 stress run:

| Class | CHARGER windups | CHARGER charges | SIEGER shots |
|---|---:|---:|---:|
| Knight | 10 | 9 | 1 |
| Rogue | 11 | 10 | 6 |
| Tank | 0 | 0 | 0 |
| Archer | 4 | 2 | 0 |
| Mage | 0 | 0 | 0 |

This does **not** automatically mean Tank/Mage/Archer are invalid.
By Stage46+, CHARGER/SIEGER mechanics have already been taught earlier, and a mastered final skill is allowed to preempt some threats.

But the result means exact Stage46–50 authoring must not accidentally eliminate every decision those monsters create whenever certain classes are present.

Next role-alignment probe must deliberately synchronize:
- Tank/Knight final knockback with CHARGER WINDUP;
- Tank/Knight final knockback with SIEGER standoff/windup/reposition;
- Archer line geometry with protected SIEGER/SUPPORTER;
- Mage collapse timing with SPLITTER parent/children.

Do not patch monster HP first.

---

# 10. Cross-stage consistency review

## P1/P2/P3
No contradiction found.
- run-state semantics unchanged;
- one root owns each final package;
- no final hit creates EXP/charge/combo/N3 recursively;
- stateful temporary effects remain Stage-local.

## Lv26 continuity
No Lv26 structural reopen required.
The Stage46 candidate pressure intentionally exceeds Lv26 steady-state capacity; that is now a late-band design requirement, not evidence that Lv26 is defective.

## Class identity
Still distinct:

```text
Knight = bounded frontline two-pass break
Rogue = sustained tracking projectile storm
Tank = global time/control/wall reset
Archer = deep straight-line deletion
Mage = staged density collapse
```

Archer width is the only new material structural candidate.

## EXP
No final EXP conclusion follows.
A Stage46 combat gate becomes acceptable only if intended-skilled players reliably possess Lv31 for skill-related reasons rather than being blocked by class/team/player-count EXP opportunity distortion.
P10R remains mandatory.

## Production
No production gameplay/source change was made.

---

# 11. Verdict

P4-D2 has now shown that the user's intended late-game fantasy is **structurally feasible**:

> Lv26 can be insufficient even under perfect timing, while Lv31 P×P can provide the explosive reset needed to survive the same pressure.

The candidate is not yet final balance.

Current working centers remain:

```text
Knight  second wave 1.00
Rogue   16 daggers × .45
Tank    shockwave .75 / KB ×2.5 / shield 250-for-6s candidate
Archer  per-target 2.30 + WIDTH STRUCTURE DECISION PENDING
Mage    stage .75 / radius1.25 candidate
```

No values are frozen.

---

# 12. Exact next decision / work boundary

One material user decision is now exposed before Archer structure can be frozen:

## Archer A-WIDE candidate

For Lv31 `Sky-Piercing Arrow` only:
- keep one straight locked ray/projectile;
- keep no homing/bending/off-line retarget;
- keep unlimited penetration depth;
- allow the **huge final arrow to use a gameplay collision corridor wider than ordinary/Lv26 arrows**;
- exact width remains P4-D2 numeric/geometry calibration, not frozen by approving the principle.

Why:
- coefficient-only escalation could not solve the dispersed temporal pressure;
- a modest width increase did;
- this makes the roadmap adjective `huge` mechanically meaningful while preserving strict-line identity.

Decision options:

```text
A — approve wider gameplay corridor principle for Lv31 Archer; exact width stays provisional
B — reject gameplay-width increase; keep visual-only huge arrow and solve late pressure another way
C — request another geometry analysis before deciding
```

Until this decision:
- continue to treat wider Archer geometry as a P4-D2 candidate only;
- do not freeze Archer Lv31 structure;
- do not start P4-E;
- do not modify production.
