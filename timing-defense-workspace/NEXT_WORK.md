# Timing Defense — Next Work Boundary

Updated: 2026-10-24 KST

## Mandatory recovery order
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_46.yaml`;
5. read `168_T1_PRESSURE_SHAPE_V0_2_LV31_ABSENCE_AND_DURATION_SENSITIVITY_RESULT_V0_1.md`;
6. read compact summary `legacy-game-structure/data/t1_pressure_shape_v0_2_and_duration_sensitivity_summary_v0_1.json`;
7. inspect v0.2 recipe `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`;
8. preserve exact-source runner contract/result `165` / `167` and settlement bridge;
9. preserve T1 skeleton/static authority `160-164` and P6 closure `156`;
10. verify production/harness heads.

Do not rerun closed P6, the full T1 skeleton audit, or baseline exact-source diagnostics without a concrete trigger.

---

# Current phase

```text
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
baseline representative recipe = STATIC PASS / EXACT-SOURCE EXECUTED
micro-sim runner = EXACT-SOURCE ADMISSION PASS AFTER SETTLEMENT CORRECTION
v0.2 pressure-shape candidate = STATIC PASS / DYNAMIC DIAGNOSTIC ONLY
Stage41 relief = RECONFIRMED
v0.2 Stage46-50 Lv31 absence = TOO SAFE
pressure duration lever = SUPPORTED
uniform pulse repetition = CLASS-SKEWED / NOT ADOPTED
CURRENT = STAGE49-50 CLASS-ROTATION PRESSURE-SHAPE DIAGNOSTIC
full 50-Stage exact recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# Evidence to preserve

## Exact-source runner fidelity
The original exact run exposed a false PASS: Stage-local wall shield/Aftershock incorrectly delayed `STAGE_SETTLED`.

Minimal settlement bridge corrected the ordering. Corrected runs prove:
```text
exact recipe identity = PASS
STAGE_SETTLED/terminal failure = PASS
no enemy carry = PASS
no transient leakage = PASS
persistent state continuity = PASS
deterministic replay = PASS
paired isolation = PASS
explicit skill-state trace = PASS
```

Do not remove or bypass the settlement bridge unless the core engine is equivalently corrected and revalidated.

## v0.2 base
Static:
```text
Stage5 unchanged
Stage18 unchanged
Stage41 unchanged
all representative max4s <= 8
Stage40 max4s 6
Stage41 max4s 3
```

Dynamic:
```text
Stage20-23: 2/60 wall-positive rows / 246 total diagnostic wall damage
Stage39-45: zero wall damage / Stage41 relief remains clear
Stage46-50 Lv31 ON: zero wall damage
Stage46-50 Lv31 OFF: zero wall damage
```

Therefore v0.2 alone is not the intended Stage46+ mastery gate.

## Duration sensitivity
6/8/10-second generic repetition:
```text
REJECTED BY 4s DENSITY GUARD
```

11/12/14/16-second spaced repetition:
```text
legal under max4 <= 8
creates real OFF > ON pressure separation
```

Example only, not adopted:
```text
COPY2_SHIFT11000
OFF wall-positive 5/15 / failures 1 / wall damage 6184
ON  wall-positive 4/15 / failures 0 / wall damage 777
```

This proves duration can matter without scalar inflation, but uniform repetition over-punishes Tank/Rogue while Archer/Mage remain too protected.

---

# Exact next bounded task

Build and test **Stage49-50 only** candidate(s) using distributed durability / split-axis pressure.

Goals:
```text
1. reduce the Tank/Rogue skew of uniform repetition;
2. create real spatial pressure for Archer/Mage rather than a single global line/cluster answer;
3. preserve Rogue durable-normal execution opportunity;
4. preserve Tank control/defense/objective-protection value;
5. keep Knight generalist/frontline usefulness;
6. preserve right-edge spawning;
7. keep authored 4-second density <= 8;
8. use only GRUNT/RUNNER/BRUTE;
9. change composition / geometry / chronology before scalars.
```

Do not change in this task:
```text
Stage5
Stage18
Stage41
monster HP/speed/wall damage
class coefficients
shop/EXP/P×P probabilities
```

Do not simply copy another universal pulse onto every class-facing situation.

---

# Candidate evaluation

Compare candidate Stage49-50 against:
1. v0.2 base;
2. duration-sensitivity envelope;
3. Lv31 OFF vs ON paired state.

At minimum report per class / seed:
```text
wall damage / wall reserve
failure or incomplete status
settled time
root actions
peak active
frontline block time
backline exposure
removal throughput
control value / Tank objective protection
Lv31 OFF vs ON delta
```

Also inspect whether pressure rotates across classes rather than merely shifting all damage to a different single class.

No single fairness score.

---

# Acceptance direction for the next diagnostic

The next candidate does **not** need equal wall damage across classes.

Useful evidence would be:
- Lv31 OFF is materially more pressured than ON in at least part of the late slice;
- ON is not universally buried;
- wall/objective pressure is not concentrated almost entirely in Tank/Rogue;
- Archer/Mage encounter a real spatial/chronological limitation in some cases;
- Tank can convert control/defense into measurable wall protection;
- 4s density and Stage semantics remain legal.

If candidate still cannot create multi-class pressure rotation, continue encounter-shape diagnosis before touching scalars.

---

# Root-cause order

```text
source / runner fidelity
-> lifecycle / state
-> composition / geometry / chronology
-> skill / class interaction
-> shop / EXP only if coupled
-> scalar sensitivity last
```

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE49-50 ONLY FOR NEXT PRESSURE-SHAPE ITERATION
PRESERVE STAGE5 / STAGE18 / STAGE41
NO FULL-50 EXACT AUTHORING YET
NO CLASS BUFF/NERF FROM THIS SLICE
SURVIVAL != CLEAR
TANK KILL PARITY NOT REQUIRED
AUTHORED 4s DENSITY <= 8
NO MONSTER/CLASS SCALAR CHANGE YET
NO FLAT SHOP->EXP MULTIPLIER
FINAL EXP ROUTING = P10R
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```
