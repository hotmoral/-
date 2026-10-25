# T1 Mage Stage50 P×P and Settlement-Tail Attribution v0.1

Date: 2026-10-25 KST

Status:
**ATTRIBUTION PASS / CURRENT STAGGER1800 CANDIDATE RETAINED / CLUSTER-FINAL REJECTION CONFIRMED / NO SCALAR CHANGE / NO AUTHORING ADOPTION**

## 1. Purpose

Resolve the residual question from docs171-172:
- the admitted candidate gives Mage a positive Stage50 CLUSTER role signal;
- whole Stage50 settle is nevertheless slightly slower with Lv31 ON;
- moving CLUSTER to the final grammar did not improve that whole-stage metric.

The goal was attribution only, before any additional encounter or scalar change.

## 2. Exact evidence

Workflow:
`.github/workflows/timing-defense-t1-mage-stage50-pxp-attribution.yml`

```text
run      40157463857
artifact 12584527727
head     d2fc1c3e85b32012edcfdf8f7db49032ea802671
artifact digest sha256 78ae92b8f948a0824d94a33dc34091c6f74eb904645bfe4a5de016a289338c8a
seeds    101,211,307,409,503
```

Source identity:
```text
trace sha256      234b2f9b8a782e33bb53d2fc88f1aa58669143d83d992f69ea35b69b72cb5a95
candidate sha256  c1bd5f45fb3cbdff6efa45b90f34e20bbc303a94d089564abf62523e15425bc3
base sha256       3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf
Mage bridge       31a463ccc6aca78314d6800a137abc17872dc4f1d054856de81c340b31cba358
settlement bridge 1926ee88bed061bca76840446c73d0b33710915aaf9d19b238d9fd0c09505e4f
```

Execution:
```text
status = ATTRIBUTION_PASS
fidelityErrors = []
```

## 3. Stage49 -> Stage50 persistent state is not the primary cause

For both the admitted candidate and the rejected CLUSTER-final variant, Stage50 entry state is the same for a given side/seed.

Mage entry charge arrays:
```text
OFF = [0,0,0,0,0]
ON  = [0,0,0,3,0]
```

Mage entry combo arrays:
```text
OFF = [44,50,43,1,13]
ON  = [44,50,43,1,8]
```

The rejected chronology move does not alter those entry states, so the failure of CLUSTER-final cannot be attributed to a Stage49->50 state mismatch.

## 4. Admitted candidate: Mage P×P is genuinely expressed inside CLUSTER

Current Stage50 order:
```text
DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE -> LINE_REPRISE
```

Across five seeds:
```text
CLUSTER P×P cases = 4/5
CLUSTER P×P opportunities = 4
ON primary target from CLUSTER = 4/4
ON mean CLUSTER spawn fraction at P×P = 1.0
ON mean Lv31 unique targets = 4.0
ON mean Lv31 damage = 1342.5
ON mean CLUSTER-origin unique targets in root payload = 4.0
```

Representative ON cases:
```text
seed101: P×P 14300ms, CLUSTER+3300ms, 6/6 spawned, Lv31 hits 4 CLUSTER targets
seed211: same shape, Lv31 hits 4
seed409: P×P 14300ms, Lv31 hits 4
seed503: P×P 14300ms, Lv31 hits 4
seed307: no CLUSTER P×P in this seed
```

Therefore the Stage50 durable/staggered CLUSTER is not merely nominal. It creates a real four-target Lv31 density-collapse opportunity in most tested seeds.

## 5. Why CLUSTER-final was worse

Rejected Stage50 order:
```text
DURABLE_SCATTER -> FRONTLINE -> LINE -> LINE_REPRISE -> CLUSTER
```

It still produced CLUSTER P×P in 4/5 seeds, but the P×P arrived later within the final CLUSTER lifecycle:

```text
mean time since CLUSTER start:
admitted = 3300ms ON
cluster-final = 3850ms ON

mean Lv31 unique targets:
admitted = 4.0
cluster-final = 3.25

mean Lv31 damage:
admitted = 1342.5
cluster-final = 1078.75
```

Seed307 is the clearest failure:
```text
P×P at CLUSTER+5500ms
only 1 CLUSTER target remains in the payload
```

Therefore moving the same CLUSTER later does not solve phase alignment; it reduces useful target availability.

This confirms doc172's rejection.

## 6. Settlement-tail attribution

The admitted candidate's mean Stage50 settle was:
```text
OFF = 26.800s
ON  = 26.908s
ON appears 0.108s slower
```

However the last P×P / settlement relation explains this small inversion.

For seeds 101, 211, 307 and 503:
```text
last Stage50 P×P is in LINE_REPRISE
OFF: STAGE_SETTLED 180ms after the final P×P
ON : STAGE_SETTLED 360ms after the final P×P
```

The ON package has the approved staged Lv31 delayed-collapse tail. Settlement correctly waits for authorized delayed combat events to drain.

Seed409 behaves oppositely at combat level:
```text
OFF settle = 29.88s
ON  settle = 29.70s
ON is 180ms faster
```

Across the five seeds:
```text
4 × (+180ms ON settlement tail) + 1 × (-180ms combat improvement)
= +540ms total
= +108ms mean
```

This exactly matches the observed mean Stage50 settle inversion in this sample.

Interpretation:
```text
MAGE_STAGE50_SETTLE_INVERSION = DELAYED_PACKAGE_TAIL_EFFECT_IN_THIS_SAMPLE
NOT EVIDENCE OF LV31 DAMAGE/ROLE FAILURE
```

This tail is not a lifecycle bug: `STAGE_SETTLED` is correctly required to wait for authorized delayed combat events.

## 7. Consequence for evaluation methodology

For delayed multi-stage packages near the Stage boundary, `stageSettledTime` alone can conflate:
1. enemy-control/clear performance;
2. the legitimate post-action delayed-effect drain tail.

Therefore Mage mastery evaluation should read together:
- target-grammar clear latency;
- target-origin payload / unique targets;
- backline exposure;
- wall outcome;
- Stage settle;
- final delayed-event tail when the last action is an Lv31 staged package.

Do not normalize the lifecycle by dropping delayed events merely to improve the metric.

## 8. Current Stage49-50 candidate assessment

Combined evidence from docs169-173:

```text
static authoring legality = PASS
exact materialization fidelity = PASS
dynamic reproduction = PASS
five-class role-facing direction = POSITIVE
Mage Stage50 role expression = REAL / 4-target average in 4/5 CLUSTER-P×P cases
Mage small whole-settle inversion = EXPLAINED BY VALID SETTLEMENT TAIL
CLUSTER-final chronology variant = REJECTED
objective wall pressure = STILL TANK-SKEWED
scalar change required = NOT SHOWN
```

The remaining Tank-skewed wall-pressure fact is a watch, not proof of a defect. Equal wall damage across classes is not an authoring goal, and Tank's approved identity is control/defense/objective protection rather than kill parity.

Archer's role signal remains modest but positive; exact Archer Lv31 corridor width remains diagnostic/unfrozen and must not be numerically adopted from this slice.

## 9. Recommended boundary

Further Stage49-50 chronology search is not justified by the current evidence.

The bounded candidate is ready for an **authoring adoption decision gate with watches**, while remaining:
- non-production;
- non-numerically-frozen;
- not a full T1 Stage1-50 recipe freeze.

If approved, promote the current Stage49-50 structure as the canonical T1 late-authoring baseline with the existing objective-pressure and Archer-width watches, then proceed to the next wider T1 authoring planning/preflight boundary rather than continuing local scalar tuning.
