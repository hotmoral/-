# Timing Defense — P5 Knight Penetration Robust Identity Probe V0.1

Date: 2026-10-23 KST  
Status: **DIRECTIONAL ROBUSTNESS REFINEMENT / KNIGHT DEFECT NOT ESTABLISHED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `131_P5_CLASS_IDENTITY_FIRST_DIRECTIONAL_RESULT_V0_1.md`
- `data/p5_class_identity_refinement_fixture_v0_1.json`

## 1. Why the first Knight pair was insufficient

The first aligned-vs-dispersed packet used bodies that could cross death thresholds around the two-wave Lv31 package.
That made the result sensitive to:
- which target died on wave 1;
- who became frontmost for wave 2;
- shop ATK breakpoint chronology.

Therefore the first pair was not robust enough to judge Knight penetration identity.

## 2. Refined packet

Use five identical durable proxy bodies:

```text
HP 1600
armor 0.55
```

They are intentionally durable enough that one wave does not simply erase the packet.

Compare only geometry:

```text
ALIGNED   = [0, 0, 0, 0, 0]
DISPERSED = [-2, -1, 0, 1, 2]
```

Same body count, same durability family, same short spawn offsets.

## 3. Directional formula-fidelity result

Reference clear times:

| shop state | aligned | dispersed | dispersed/aligned |
|---|---:|---:|---:|
| no shop | 12.575 s | 15.950 s | 1.268x |
| BALANCED @ 40% diagnostic | 9.200 s | 12.575 s | 1.367x |
| DEFENSE_HEAVY @ 40% diagnostic | 11.450 s | 12.575 s | 1.098x |

Interpretation:
- aligned frontline geometry remains beneficial;
- the benefit survives shop growth directionally;
- defense-heavy specialization naturally compresses the difference because offense is lower;
- the result is no longer dominated by one-shot/second-wave retarget breakpoints.

## 4. Identity conclusion

Current evidence supports:

```text
Knight = frontline / penetration generalist
```

No Knight structural defect is established.

The remaining defense-heavy Knight watch belongs to late-stage encounter pressure, not to the class's penetration identity itself.

## 5. Boundary

This is a directional formula-fidelity refinement.
Committed full-kernel replay remains pending and no exact ratio is frozen.

Do not buff Knight penetration merely to widen this one paired-test ratio.

## 6. Classification

```text
KNIGHT_PENETRATION_CAUSALITY = DIRECTIONALLY_SUPPORTED
KNIGHT_STRUCTURAL_IDENTITY_DEFECT = NO_EVIDENCE
FIRST_PAIR_RETARGET_CHRONOLOGY_PROBLEM = RESOLVED_BY_REFINED_FIXTURE_DIRECTION
DEFENSE_HEAVY_LATE_PRESSURE_WATCH = KEEP
NUMERICAL_FREEZE = NO
```
