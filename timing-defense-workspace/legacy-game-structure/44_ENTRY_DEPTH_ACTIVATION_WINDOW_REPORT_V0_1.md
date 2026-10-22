# Timing Defense — Entry-Depth Activation Window Report V0.1

Date: 2026-10-22 KST  
Status: **GEOMETRY DIAGNOSTIC / NOT PRODUCTION COORDINATE FREEZE**

Inputs:
- current representative recipes
- CURRENT_AUTHORITY_LV6
- unfitted TRACE_BRACKET_CENTRAL
- current provisional monster capability anchors

Tool:
- `tools/sweep_special_activation_entry_depth.py`

---

# 0. Question

Can CHARGER/SIEGER capability expression be restored through encounter geometry before touching HP/speed coefficients?

---

# 1. Key result — activation is non-monotonic

Moving the whole formation closer to the wall does not monotonically increase capability expression.

Three zones appear:

```text
TOO DEEP/FAR
  -> special dies before trigger/standoff

ACTIVATION WINDOW
  -> special reaches state transition while meaningful screen/exposure still exists

TOO FORWARD
  -> special becomes exposed/frontmost too early or surrounding bodies hit wall/are removed
  -> special may again die before completing windup
```

Therefore the target is an **activation envelope**, not “move closer until it works.”

---

# 2. CHARGER

## T3_E07_M exposed CHARGER
Current default depth:
- 0 windups across the current critical trace/class sweep

CENTRAL depth diagnostic:
- Tank/ Knight first start seeing windup around a whole-formation shift of ~0.25 X
- positive-knock direct hits can interrupt windup; first observed around ~0.30 X in this diagnostic

Important:
CHARGER windup interruption is not Tank-exclusive. Any authoritative positive knock during windup can interrupt.
Tank's advantage is stronger control/knock, not a unique interrupt permission.

## T3_E17_M screened CHARGER
With CHARGER kept ~+0.10 behind the shifted screen:
- windup becomes observable for some classes before all-five coverage
- all five classes observed at least one windup around ~0.45 X forward shift in the current diagnostic

Again, `0.45` is not production authoring data.
It proves geometry can restore the mechanic without first changing HP.

---

# 3. SIEGER — E11

E11 ESCORT_SIEGE with SIEGER kept roughly +0.10 behind the shifted formation:

Current default:
```text
5-class shot exposure = 0/5
```

Diagnostic examples:

| Shift toward wall | Classes seeing >=1 shot | Notes |
|---:|---:|---|
| ~0.70 | 5/5 | first broad activation in current sweep |
| ~0.75 | 5/5 | stronger objective pressure |
| ~0.80 | 5/5 | wall damage rises materially |
| ~0.85 | 0/5 | special becomes too exposed/removed before shot |

At ~0.70:
- Knight/Tank observed 2 shots in this probe
- Rogue/Mage/Archer observed at least 1
- Archer also had extra wall damage from formation pressure

This non-monotonic collapse at ~0.85 is the critical finding.

---

# 4. SIEGER — E19

E19 FORTRESS:

| Shift toward wall | Classes seeing >=1 shot |
|---:|---:|
| ~0.70 | 4/5 |
| ~0.75 | 5/5 |
| ~0.80 | 5/5 |
| ~0.85 | 0/5 |

Thus E19 also has a bounded activation window rather than a simple closer-is-harder curve.

At aggressive forward shifts wall pressure can become large before fitted player-trace validation, so these values cannot be promoted directly.

---

# 5. Structural interpretation

The initial default spawn anchor was suitable for broad kinematic testing but is not automatically suitable for every stateful encounter.

CHARGER/SIEGER authoring must explicitly control:
- absolute formation entry depth
- relative special-unit back depth
- spawn time
- screen lifetime
- trigger/standoff distance
- windup exposure

This should be treated like cadence/formation grammar, not hidden balance math.

---

# 6. New required metrics

For each stateful recipe:
- `activationClassCount`
- `firstActivationTimeByClass`
- `activationWindowMinDepth`
- `activationWindowMaxDepth`
- `screenedActivationByClass`
- `wallDamageBeforeFirstActivation`
- `specialErasedBeforeActivationByClass`

For CHARGER:
- windup -> interrupted/completed by class

For SIEGER:
- standoff reached -> first shot -> repeated shots

---

# 7. Decision

Do **not** change global monster HP yet.

Next candidate-authoring step:
1. introduce absolute entry-depth ranges for stateful recipes
2. select a small readable depth window, not one exact coordinate
3. rerun all five classes
4. reject windows with unavoidable early wall damage or special frontmost exposure
5. only then consider numeric capability tuning

This moves Layer-A from `capability missing` to `capability window calibration`.
