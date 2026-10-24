# Timing Defense — Next Work Boundary

Updated: 2026-10-24 KST

## Mandatory recovery order
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_45.yaml`;
5. read `166_T1_TRANSITION_SLICE_MICROSIM_ADAPTER_IMPLEMENTATION_AND_ADMISSION_PREFLIGHT_V0_1.md`;
6. read `165_T1_REPRESENTATIVE_TRANSITION_SLICE_MICROSIM_CONTRACT_V0_1.md`;
7. inspect exact recipe data `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml`;
8. inspect runner entry `tools/run_t1_transition_slice_microsim_v0_1.py` and its three support modules only as needed;
9. preserve `164` static recipe PASS, `161/162` T1 skeleton result, P6 closure `156`, and active watches;
10. verify production/harness heads before/after execution.

Do not rerun closed P6, Model A Layer-A0, or the full static T1 audit without a concrete trigger.

---

# Current phase

```text
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
Representative recipe materialization = STATIC PASS
Micro-sim contract = COMPLETE
Dedicated transition runner = IMPLEMENTED
Local semantic smoke = PASS / ENGINEERING ONLY
Exact canonical-source dynamic execution = NOT STARTED
CURRENT = EXECUTE EXACT CANONICAL SOURCE THROUGH RUNNER ADMISSION
full 50-Stage exact recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# Exact next action

Execute the committed runner against the exact live canonical files:

```text
python tools/run_t1_transition_slice_microsim_v0_1.py \
  --recipes legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml \
  --p3-fixture legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json \
  --p4d2-base legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json \
  --p4d2-temporal legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json \
  --seeds 101,211,307 \
  --json-out <evidence-path>
```

The execution environment must use the current canonical checkout/bytes. Do not reconstruct or redump the recipe before execution.

Record:
- live canonical HEAD used;
- exact recipe source SHA256 emitted by runner;
- runner code/blob identity;
- admission result;
- evidence file digest if an artifact is retained.

---

# Admission gate — must pass before balance interpretation

Require all:
```text
exactRecipeIdentity evidence
stageSettledOrTerminalFailure
noEnemyCarryAtSettledBoundary
noTransientLeakageAtSettledBoundary
persistentStateContinuity
deterministicReplay
pairedIsolation
explicitSkillStateTrace
```

Also preserve fail-closed behavior:
- no timer-based enemy deletion;
- no forced Stage advance;
- safety cap raises fidelity failure.

If any gate fails:
```text
STOP BALANCE INTERPRETATION
-> classify runner/source or lifecycle failure
-> repair runner only as narrowly as necessary
-> rerun exact-source admission
```

---

# Only after admission PASS

Inspect groups in fixed order:

## A — Stage5 RUNNER teach × Lv6
```text
Lv6 OFF vs ON
same recipe / same deterministic state
```
Question: does Lv6 erase or distort RUNNER teaching?

## B — Stage18 BRUTE first mix × Lv16
```text
Lv16 OFF vs ON
same recipe / same deterministic state
```
Question: does Lv16 prevent BRUTE durability/frontline role from being readable?

## C — Stage20->23
Sequential persistent-state run. Check Star Gate A and first RUNNER/BRUTE high-pressure ramp.

## D — Stage39->45
Sequential runs with Lv31 activation before Stage41 / 43 / 45. This is reach-position sensitivity only, not an EXP freeze.

## E — Stage46->50
Sequential post-Lv31 mastery/final run with Lv31 active throughout.

---

# Required interpretation dimensions

Keep separate:
```text
authored/effective entity count
peak active
4s/6s density
frontline block time
target reorder
backline exposure
spawn-to-first-contact
removal throughput
control value
wall damage/reserve
root timing actions
stage settled time
failure classification
class opportunity / weakness observation
```

For Tank, objective protection/control is the primary attribution lane; low removal alone is not a defect.

Do not collapse results into one fairness score.

---

# Skill authority boundary

```text
Lv6 = current frozen combat authority
Lv11/Lv16/Lv21 = legacy parity diagnostic inputs
Lv26 = user-approved structural contract + provisional diagnostic coefficients
Lv31 = user-approved structural direction + P4D2 provisional diagnostic centers
```

The runner may use these to diagnose the slices. It may not promote provisional values to production freeze.

---

# Root-cause order if exact execution reveals a problem

```text
source / runner fidelity
-> lifecycle / state
-> composition / geometry / chronology
-> skill / class interaction
-> shop / EXP only if actually coupled
-> scalar sensitivity last
```

Repair only the affected slice/neighborhood unless evidence proves a broader dependency problem.

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
LOCAL SEMANTIC SMOKE IS NOT CANONICAL DYNAMIC EVIDENCE
NO FULL-50 EXACT AUTHORING BEFORE REPRESENTATIVE DYNAMIC EVIDENCE
NO CLASS BUFF/NERF FROM ONE SLICE
SURVIVAL != CLEAR
TANK KILL PARITY NOT REQUIRED
NO FLAT SHOP->EXP MULTIPLIER
FINAL EXP ROUTING = P10R
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```
