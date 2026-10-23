# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes unauthorized

## Mandatory authority
Read structure before local tuning:
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- **`legacy-game-structure/138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`**
- `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- active plan `legacy-game-structure/data/system_dependency_calibration_order_v0_31.yaml`
- `CHARACTER_PROFILE_RADAR_V1.md`
- `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `legacy-game-structure/128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
- `legacy-game-structure/135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
- `legacy-game-structure/137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
- `legacy-game-structure/139_P5_STAGE48_SIEGER_PROTECTION_TIME_DIAGNOSTIC_V0_1.md`
- **`legacy-game-structure/140_P5_STAGE48_THREE_AXIS_COMPARISON_DECISION_GATE_V0_1.md`**

Live remote wins.

---

# ACTIVE PACKAGE — P5

**A2 APPROVED / CLASS IDENTITY GROUP CLOSED DIRECTIONALLY / STAGE_SETTLED REQUIRED / STAGE48 THREE-AXIS COMPARISON COMPLETE / USER DECISION GATE ACTIVE**

No new Stage48 packet is approved.
No armored monster/elite is approved.
No Stage48 cadence is approved.
No SIEGER/escort stat or standoff value is approved.
No Tank scalar is selected.
No numerical value is frozen.

---

# Mandatory working method

A new session must first recover the **whole coupled reasoning frame**, not only the latest micro-task.

Before each material slice, ask:

```text
What is the gameplay/progression purpose?
What upstream contracts constrain it?
What downstream systems consume it?
What feedback loops can move?
What class identities can be distorted?
Is this a structural/chronology/simulator/economy/numerical defect?
Can a smaller bounded probe answer it?
Does adoption require user approval?
```

Repair/diagnosis order where applicable:

```text
source/simulator fidelity
-> lifecycle/state semantics
-> encounter geometry/chronology/frontmost order
-> class/package semantics
-> shop/feedback interaction
-> exact scalar values last
```

Explain conclusions to the user simply:

```text
problem -> cause -> next check -> what is NOT yet decided/applied
```

Important design/content/numerical decisions must be presented and approved before adoption.
Diagnostic measurements may continue independently only while they do not silently choose the working design direction.

---

# Do not repeat

Already closed/admitted unless a concrete trigger appears:
- P1/P2/P3 structural foundations;
- P4 closed/provisional groups without a relevant source mismatch;
- five-class identity group wholesale re-analysis;
- integrated runner import/source-patch/determinism admission;
- proof that 60 s backlog discard is material;
- proof that STAGE_SETTLED is the correct Stage transition model;
- proof that the old repeated Knight-only proxy contaminates Stage48;
- proof that simple proxy->BRUTE/SHIELD substitution is insufficient;
- proof that existing-real-monster layered handoff alone is insufficient;
- proof that standoff-only repair is insufficient even near the spawn edge.

New work must start from doc140's decision gate.

---

# Latest Stage48 comparison

## Axis A — real BRUTE/SHIELD only

Strongest tested layered handoff still gave:

```text
Knight SIEGER lifetime 2.325 s
Rogue  1.950 s
Tank   11.325 s
Archer 4.575 s
Mage   3.450 s
windups/shots = 0/0 for all five
```

Verdict:

```text
REAL_ONLY_STANDALONE = INSUFFICIENT
```

## Axis B — limited armored-durable concept

The user's original intent for this concept is broader than SIEGER escort:
- slow the tendency for Mage/Archer to erase late-stage volume too quickly;
- potentially create a durable frontline that can also protect role monsters such as SIEGER.

Temporary comparison run `39958245978` used the old proxy anchor only as an **upper-bound limited heavy-body diagnostic**, not as a production monster.

With **2** limited heavy bodies:

```text
Knight 2.325 s
Rogue  2.350 s
Tank   5.700 s
Archer 6.825 s
Mage   7.200 s
```

Archer/Mage receive a material SIEGER-lifetime increase.
With **3** heavy bodies, the result becomes non-monotonic and Mage falls back to `3.45 s`.

Meaning:

```text
MORE DURABILITY / MORE BODIES != AUTOMATIC IMPROVEMENT
FORMATION + DENSITY + TIMING ARE THE KEY VARIABLES
```

Verdict:

```text
LIMITED_ARMORED_AXIS = MOST PROMISING PRIMARY EXPLORATION CANDIDATE
BUT NOT APPROVED
BUT NOT A COMPLETE SIEGER FIX YET
```

## Axis C — SIEGER standoff only

Temporary run `39958394484` showed:

```text
x=0.78 -> Tank 2 shots; other four 0 shots
x=0.84 -> Tank 2 shots; other four 0 shots
x=0.88 -> Rogue 1 windup/0 shots; Tank 2 shots; others 0 shots
x=0.90 -> Knight/Rogue/Archer/Mage 1 windup/0 shots each; Tank 2 shots
```

At `x=0.90`, SIEGER travels only ~0.44 s from spawnX `0.92` before attempting siege.
Even this near-entry behavior still does not create meaningful all-class firing.

Verdict:

```text
STANDOFF_ONLY = POOR PRIMARY FIT
MODEST STANDOFF AS SECONDARY = STILL OPEN
```

## Deferred fourth axis — buff/resistance/skill-like monster mechanics

This remains a valid future option, but it is deferred because it adds more relationships:

```text
source / duration / stacking
-> class penetration/AoE/crit/knock interactions
-> telegraph/readability
-> targeting/frontmost behavior
-> reward/economy
-> Stage/Tier frequency
-> multiplayer scaling
-> deterministic attribution
```

Do not introduce that complexity until the simpler formation/content axes are exhausted.

---

# Immediate next work — USER DECISION GATE

Recommended direction, **not yet adopted**:

> Keep ordinary BRUTE/SHIELD as baseline vocabulary. Use a **limited armored-durable / hardened-frontline concept** as the primary Stage48 exploration axis. Keep only a modest SIEGER-standoff change as a possible secondary axis. Defer new buff/resistance mechanics for now.

Why this is recommended:
- it is the only tested axis that materially slows both Archer and Mage pressure against SIEGER;
- it matches the user's original late-stage anti-wipe design purpose;
- it avoids turning SIEGER into an almost immediate spawn-edge artillery unit;
- it introduces less coupling than a new buff/resistance subsystem;
- but it still requires careful formation/geometry work because 2-body vs 3-body behavior is non-monotonic.

**Ask the user before adopting this working direction.**

---

# If the user approves the recommended diagnostic direction

Do not start with a broad HP/armor grid.

First test only a few deliberately different **limited-heavy formation/chronology layouts** while keeping the old proxy numbers as an upper-bound diagnostic anchor only.

Measure:

```text
Mage/Archer packet-clear delay
Knight penetration leakage
Rogue front-clear / deterministic-retarget leakage
Tank slow-clear/control behavior
SIEGER first windup / first shot
wall loss / wall-contact source
STAGE_SETTLED tail
formation density/alignment sensitivity
```

Goal:

> Find one common all-class formation direction that gives late-stage durable pressure without a class lockout and without recreating the old Mage collapse.

Only after a promising common layout exists:
1. replay Stage46→49 with `STAGE_SETTLED` and carried wall deficit;
2. check Stage46 revelation / Stage47 recovery / Stage48 role pulse / Stage49 escalation;
3. check shop/kill-order/EXP feedback and class identities;
4. prepare exact choices for heavy-body status, HP/armor/knock profile, frequency, standoff range and Stage48 packet;
5. **ask the user again before adopting any important numerical/content decision.**

Only after Stage48 direction is approved:
- refine Stage49 chronology;
- return to Tank `0.20 / 0.25 / 0.30` selection on uncontaminated late pressure;
- continue Rogue broad-cleanup policy if still material;
- later KNOCK, CRIT/CRITDMG, real shop acquisition timing/EXP feedback, P10/P10R.

---

# Fixed guards

```text
SURVIVAL != CLEAR
TANK SOLO PARITY NOT REQUIRED
NO ABSOLUTE CLASS LOCKOUT
NO TANK CONTROL NERF AS FIRST REPAIR
NO ROGUE RETARGET REMOVAL AS FIRST REPAIR
NO GLOBAL ARCHER NERF
NO MAGE BUFF TO FIX A BAD ENCOUNTER TEST
NO SIEGER WINDUP CHANGE WITHOUT EVIDENCE
NO GLOBAL ESCORT DURABILITY INFLATION
NO OLD REPEATED PROXY PACKET
NO NEW BUFF/RESISTANCE SUBSYSTEM BEFORE SIMPLER AXES ARE EXHAUSTED
```

---

# Decision / production boundary

Ask the user before:
- adopting limited armored/hardened frontline as the working Stage48 direction;
- defining it as a new ordinary monster, elite, variant, buff, resistance package, or other formal content type;
- adopting a new Stage48 packet/cadence;
- changing SIEGER/escort stats or selecting a standoff range;
- introducing buff/resistance mechanics;
- selecting/fixing Tank damage scalar;
- changing class, monster, shop or EXP numerical values;
- changing an approved structural contract;
- modifying/deploying production gameplay.

P6 remains blocked pending P5 closure.
