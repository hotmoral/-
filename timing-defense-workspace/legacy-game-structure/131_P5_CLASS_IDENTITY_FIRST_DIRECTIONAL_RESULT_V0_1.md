# Timing Defense — P5 Class Identity First Directional Result V0.1

Date: 2026-10-23 KST  
Status: **DIRECTIONAL RECONSTRUCTION RESULT / TANK NEGATIVE-IDENTITY DEFECT CONFIRMED DIRECTIONALLY / COMMITTED RUNNER EXACT EXECUTION STILL PENDING / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `130_P5_CLASS_IDENTITY_FINITE_PACKET_PROBE_PREFLIGHT_V0_1.md`
- `data/p5_class_identity_radar_probe_fixture_v0_1.json`
- `../tools/run_p5_class_identity_radar_probe_v0_1.py`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`

---

# 0. Authority boundary

This result is an independent deterministic reconstruction of the current committed P4/P5 combat semantics and newly authored finite-packet fixtures.

It is **directional evidence**, not yet exact committed-runner admission.

The current execution environment cannot directly resolve GitHub from the local container, so the committed one-command runner has not yet been executed as a checkout-equivalent artifact.

Therefore:

```text
DIRECTIONAL_CLASS_IDENTITY_FINDINGS = USABLE
EXACT_COMMITTED_RUNNER_RESULT = PENDING
PRODUCTION_NUMERICAL_FREEZE = NO
```

No production source was changed.

---

# 1. Tank — major finding

On the same `TANK_MIXED_SOLO` finite packet at the current P5 40%-legacy ATK/FORT/DEF diagnostic center:

```text
Knight  8.079 s
Rogue   7.581 s
Tank    8.079 s
Archer  6.953 s
Mage    8.079 s
```

Median of the four non-Tank classes:

```text
~7.830 s
```

Tank ratio:

```text
Tank / damage-class median ~= 1.03x
```

This is incompatible with the user-directed negative Tank identity.

The Tank currently does **not** behave like:

```text
excellent survival/control
+ poor enemy-removal throughput
```

in this finite-packet lane.

Instead, with successful Lv31 use, it removes the packet at approximately damage-class speed.

Classification:

```text
P5_TANK_SOLO_CLEAR_THROUGHPUT_WATCH = TRIGGERED DIRECTIONALLY
TANK_NEGATIVE_IDENTITY_CURRENTLY_NOT_PRESERVED = TRUE DIRECTIONALLY
```

---

# 2. Tank root cause — Lv31 battlefield-wide damage contribution

Current P4-D2 working center:

```text
Absolute Barrier shockwaveCoefficient = 0.75
```

The diagnostic kernel applies this to every living enemy in the battlefield-wide Lv31 shockwave.

This matters because the approved structural contract says Tank Absolute Barrier should:
- visibly reset battlefield pressure through **control and wall protection**;
- be extremely strong at pressure reset;
- **not become generic Mage-style damage**.

The finite-packet result shows that the current provisional damage center is large enough that battlefield-wide damage materially erases Tank's intended poor-clear weakness.

This does **not** imply that Absolute Barrier should lose its huge visual/control impact.

Correct repair axis to test:

```text
keep battlefield-wide control / displacement / barrier fantasy
while reducing the final's contribution to enemy-removal throughput
```

No exact damage coefficient is frozen here.

---

# 3. Tank damage sensitivity — direction only

On the same finite `TANK_MIXED_SOLO` packet, changing only the provisional Lv31 shockwave damage coefficient while preserving the rest of the Tank package produced:

| shockwave coefficient | direct clear | vs non-Tank median |
|---:|---:|---:|
| 0.75 | 8.079 s | 1.03x |
| 0.50 | 10.333 s | 1.32x |
| 0.40 | 12.575 s | 1.61x |
| 0.35 | 13.702 s | 1.75x |
| 0.30 | 14.829 s | 1.89x |
| 0.25 | 18.209 s | 2.33x |
| 0.20 | 21.578 s | 2.76x |
| 0.15 | 23.832 s | 3.04x |
| 0.10 | 29.454 s | 3.76x |

At `0.00`, the direct-clear predicate failed because enemies reached the wall rather than all being killed directly.

Interpretation:
- Tank solo-throughput identity can be restored without removing knockback/barrier/control;
- there is a broad sensitivity range where Tank becomes materially slower;
- this table is **not** an authorization to choose `0.25`, `0.20`, etc.;
- the late-pressure stress must also remain survivable through control before any value can be proposed.

A separate Stage49-like 60 s directional stress showed why zero/near-zero damage cannot simply be assumed safe:
- `0.75`: strong survival, small backlog;
- `0.50`: strong survival, larger backlog;
- `0.25`: wall reserve still protected but backlog/wall contacts rise materially;
- `0.10`: backlog overwhelms the current pressure recipe and the wall buries around the low-40-second range.

Therefore the correct next task is a **Tank control-vs-clear Pareto search**, not a blanket damage deletion.

---

# 4. Archer — core identity looks healthier than the prior Stage49 watch implied

Paired finite packet at BALANCED:

```text
aligned line  ~= 3.58 s
scatter       ~= 8.08 s
scatter/aligned ~= 2.26x
```

ATTACK_HEAVY produced essentially the same qualitative separation in this first probe.

Interpretation:
- strict-line geometry remains a very strong determinant of Archer performance;
- Archer has **not** generally collapsed into a formation-agnostic class;
- the prior attack-heavy Stage49 problem is more likely a packet/frontmost/breakpoint chronology problem than a fundamental loss of line identity.

Classification:

```text
P5_ARCHER_LINE_DEPENDENCE = STRONGLY PRESENT IN FIRST FINITE PROBE
P5_ATK_HEAVY_ARCHER_REPEATED_FAILURE_MARGIN_WATCH = KEEP, BUT LOCALIZE TO LATE-PACKET CHRONOLOGY
```

Do not nerf Archer globally from the old Stage49 result.

---

# 5. Mage — density identity remains strong

BALANCED paired finite packet:

```text
clustered   ~= 3.78 s
distributed ~= 8.08 s
distributed/cluster ~= 2.14x
```

This is strongly aligned with the radar/role contract:

```text
dense group -> very high payoff
spread pressure -> materially weaker
```

Classification:

```text
P5_MAGE_DENSITY_DEPENDENCE = STRONGLY PRESENT
```

Current Mage identity does not need a structural redesign from this evidence.

---

# 6. Rogue — new shop breakpoint / identity tension

The first authored Rogue pair was not total-EHP-normalized enough to classify broad-wave leakage cleanly.

A follow-up directional packet was therefore checked with approximately comparable total effective durability:

```text
DURABLE packet:
ARMORED_DURABLE_PROXY + BRUTE

BROAD packet:
8 GRUNT + 8 RUNNER = 16 scattered ordinary bodies
```

Rogue direct-clear times by common shop-effect sensitivity:

| shop effect scale | durable | broad16 |
|---:|---:|---:|
| 0% | 3.828 s | 5.453 s |
| 20% | 3.778 s | 4.406 s |
| 30% | 3.727 s | 3.829 s |
| 40% | 3.727 s | 3.829 s |
| 50% | 3.706 s | 3.829 s |

Root cause:

Current provisional Dagger Storm dagger base:

```text
600 * 0.45 = 270 raw
```

At the BALANCED ATK shop profile, around the 30%-legacy effect scale:

```text
270 * (1 + 0.192) ~= 321.84
```

which crosses the diagnostic GRUNT HP `320`.

Then one remaining storm dagger can kill one GRUNT, retarget, and continue.
Because the approved Dagger Storm contract explicitly permits deterministic retarget after target death, this creates a discrete transition where the storm can serially clean a large weak wave.

New watch:

```text
P5_ROGUE_DAGGER_GRUNT_ONESHOT_BREAKPOINT_WATCH = HIGH
```

Important interpretation:
- this is not yet a request to remove approved retargeting;
- this is not automatically an AoE semantic violation because daggers remain single-target projectiles;
- however the **practical low-AoE weakness may disappear** if each dagger one-shots a new ordinary body;
- future shop/Lv31 calibration must check distinct-target count per storm package, not only total damage.

---

# 7. Knight — first fixture is not robust enough for identity admission

First BALANCED pair:

```text
aligned frontline ~= 3.73 s
dispersed         ~= 5.83 s
```

That superficially supports penetration identity.

However ATK sensitivity exposed a non-monotonic chronology breakpoint:

```text
at lower shop-power scales, aligned and dispersed were both ~=3.73 s
above a later ATK threshold, dispersed became ~=5.83 s
```

A DEFENSE_HEAVY Knight could also produce a different chronology than BALANCED despite having lower offense.

This means the first Knight pair is too sensitive to target-death/second-wave retarget chronology to serve as a clean penetration-causality gate.

Classification:

```text
KNIGHT_IDENTITY_DEFECT = NOT ESTABLISHED
KNIGHT_IDENTITY_FIXTURE_ROBUSTNESS = INSUFFICIENT
```

Next repair is the probe/fixture, not the Knight.

---

# 8. Revised class status after first directional scan

```text
Knight = STRUCTURALLY PLAUSIBLE / PAIRED-PROBE REFINEMENT REQUIRED
Rogue  = CORE MULTIHIT IDENTITY PRESENT / SHOP-DRIVEN BROAD-CLEANUP BREAKPOINT HIGH WATCH
Tank   = POSITIVE CONTROL IDENTITY PRESENT / NEGATIVE SOLO-THROUGHPUT DEFECT DIRECTIONALLY CONFIRMED
Archer = LINE DEPENDENCE STRONGLY CONFIRMED IN FINITE PROBE / STAGE49 CHRONOLOGY WATCH LOCALIZED
Mage   = DENSITY DEPENDENCE STRONGLY CONFIRMED
```

---

# 9. Exact next work

Before returning to Stage49 packet tuning:

1. exact/committed-execute the authored identity runner when the local execution lane can reproduce committed bytes;
2. create a Tank control-vs-clear sensitivity lane that preserves barrier/knock/control while scanning much lower final damage contribution;
3. measure Tank late-pressure wall survival **and** direct enemy-removal throughput together;
4. add Rogue per-storm distinct-target count and the GRUNT one-shot breakpoint to shop sensitivity;
5. replace the first Knight pair with a more robust penetration-causality packet that is not dominated by second-wave retarget chronology;
6. retain Archer and Mage paired probes as strong structural identity anchors;
7. only after that resume Stage49 chronology refinement.

No production change is authorized.
