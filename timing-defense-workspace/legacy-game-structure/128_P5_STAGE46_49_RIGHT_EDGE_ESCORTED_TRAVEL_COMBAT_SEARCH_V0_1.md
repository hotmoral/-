# Timing Defense — P5 Stage46–49 Right-Edge Escorted-Travel Combat Search V0.1

Date: 2026-10-23 KST  
Status: **DIRECTIONAL COMBAT SEARCH / NORMAL RIGHT-EDGE ENTRY PRESERVED / ESCORTED LATE-PULSE PROMISING / TWO ACTIVE BUILD WATCHES / NO NUMERICAL FREEZE**

Depends on:
- `127_P5_STAGE46_49_RIGHT_EDGE_TRAVEL_LEAD_PREFLIGHT_V0_1.md`
- `126_P5_POST_SHOP_STAGE49_ENTRY_DEPTH_RECONVERGENCE_V0_1.md`
- `124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`

Fixture:
- `data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json`

---

## 0. Plain design question

Can the prior promising late pressure be reproduced **without spawning enemies in the middle of the field**?

Required implementation-facing rule:

```text
all enemies enter from the normal right edge
```

Difficulty may come from:
- when a threat enters;
- which front-line bodies enter before/with it;
- relative band/spacing;
- overlap between the first and second pressure pulse.

---

## 1. First rejection — earlier SIEGER alone

The kinematic preflight already showed that an isolated SIEGER appearing 8–10 seconds earlier is exposed to many extra ordinary attacks.

Combat search confirmed the same structural problem:

```text
earlier SIEGER alone
-> more time visible to the player
-> SIEGER dies before its intended pressure moment
-> encounter can become easier
```

Therefore:

```text
NAKED_EARLY_SIEGER = REJECTED AS PRIMARY REPAIR
```

---

## 2. Second rejection — simply add many durable blockers

Adding multiple high-durability bodies in front does protect the SIEGER, but it creates a new failure mode:

```text
too many durable blockers
-> lower-ATK / defense-heavy Knight spends too long clearing the front line
-> normal successful play loses excessive wall reserve
```

This violates the goal of preserving legitimate shop specialization.

Therefore:

```text
MORE_DURABLE_BODIES = NOT A UNIVERSAL FIX
```

Durable pressure remains useful, but count/timing must be bounded.

---

## 3. Third finding — weak escort trains are also not a complete fix

A chain of weak bodies can consume frontmost attack actions, but high-ATK Archer can clear them very quickly and regain access to the SIEGER.

So:

```text
weak escort only
-> does not reliably preserve the role threat across shop policies
```

This means the repair problem is primarily **packet chronology**, not raw monster count.

---

## 4. Best current Stage46–49 direction

The most stable directional structure is:

```text
Stage46
Lv31 power revelation; no aggressive early-travel manipulation.

Stage47
transition; still leave recovery room.

Stage48
first protected role pulse: separated durable bodies + one timed SIEGER.

Stage49
stronger escorted second pulse: front-line bodies enter earlier and SIEGERs follow from the right edge while the front line is still relevant.
```

A first useful cadence direction was:

```text
Stage46 pressure cycle ~5.8s
Stage47 ~5.3s
Stage48 ~4.9s
Stage49 ~4.6s
```

These are diagnostics only, not production values.

---

## 5. Directional sequential result

An independent deterministic reconstruction was used only as **directional search evidence**. It is not exact replay authority and must not replace committed source-patched runners.

At the current P5 40%-legacy ATK/FORT/DEF diagnostic center:

### Normal successful mastery
Representative BALANCED / ATTACK_HEAVY / DEFENSE_HEAVY shop directions all retained Stage46–49 survivability in the best current packet family.

Important low-side example:
- DEFENSE_HEAVY Knight still survived the four-stage chain, but with materially less reserve than other classes/builds.

Therefore the packet is not yet ready for numerical freeze, but it does not require class/Lv31 nerfs to create pressure.

### Repeated final failure
The same chain produced the intended general shape:
- Knight / Rogue / Tank collapse quickly when finals are repeatedly abandoned;
- Mage accumulates severe late damage and can collapse by Stage49;
- Archer accumulates substantial Stage48–49 damage rather than remaining completely safe.

However one material outlier remains:

```text
ATK_HEAVY Archer can still retain too much reserve after sustained final failure in some packet chronologies.
```

This is a **HIGH watch**, not evidence for hidden Archer shop penalties.

---

## 6. Why the remaining Archer case should not be solved by a direct nerf

Prior tracing already established that Archer is sensitive to exact kill/frontmost breakpoints.

Increasing ATK can change:

```text
one-hit threshold
-> frontmost target removed earlier
-> strict-line access changes
-> later SIEGER exposure changes
```

The new right-edge search shows the same phenomenon with escort packets.

Therefore repair order remains:

1. relative packet timing;
2. which body is frontmost when the SIEGER is traveling;
3. band separation / line alignment;
4. second-pulse spacing;
5. only after those, durability sensitivity;
6. class/shop coefficients last.

Do not add a hidden Archer penalty or cut Lv31 power merely to force one stress result.

---

## 7. Active watches

```text
P5_ATK_HEAVY_ARCHER_REPEATED_FAILURE_MARGIN_WATCH = HIGH
P5_DEFENSE_HEAVY_KNIGHT_OVERPRESSURE_WATCH = HIGH
P5_RIGHT_EDGE_ESCORT_PACKET_CHRONOLOGY_WATCH = HIGH
```

Interpretation:
- Archer watch: attack-heavy build must not turn sustained mastery failure into a healthy Stage50 entry.
- Knight watch: solving Archer/Mage pressure must not turn defense-heavy Knight into a trap build under successful play.
- chronology watch: attack power may alter role exposure nonlinearly; compare event order, not just end wall HP.

---

## 8. Current classification

```text
MIDFIELD_POP_IN = REJECTED
NORMAL_RIGHT_EDGE_ENTRY = REQUIRED
NAKED_EARLY_SIEGER = REJECTED
ESCORTED_EARLY_ROLE_TRAVEL = PROMISING
STAGE46_47_POWER_REVELATION_ROOM = SUPPORTED
STAGE48_PROTECTED_ROLE_PULSE = PROMISING
STAGE49_ESCORTED_SECOND_PULSE = PROMISING
GLOBAL_SHOP_NERF_REQUIRED = NO
LV31_POWER_NERF_REQUIRED = NO
EXACT_AUTHORING_READY = NO
```

---

## 9. Exact next work

1. implement a source-patched diagnostic schedule using `spawnLeadSeconds` while keeping every mob at normal `spawnX=0.92`;
2. exact/directional replay Stage46→49 with shop power and carried wall deficit;
3. refine Stage49 packet timing specifically against ATK-heavy Archer without breaking defense-heavy Knight;
4. preserve one/two-miss recovery checks;
5. then return to KNOCK and CRIT/CRITDMG fidelity lanes.

No production implementation or numerical freeze is authorized.
