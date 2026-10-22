# Timing Defense — Passive Role Structural Anchor Report V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL ANCHOR CHECK / NOT CLASS-AWARE ADMISSION**

Tool:
- `tools/probe_passive_role_contract_anchors.py`

Inputs:
- `data/model_a_kinematic_anchor_v0_1.yaml`
- `data/model_a_combat_sensitivity_anchor_v0_1.yaml`

Purpose:
Before adding more expensive class-aware temporal instrumentation, confirm that RUNNER/BRUTE/SHIELD/FLYER have sufficiently distinct underlying mechanics and are not numerically collapsed into GRUNT-like bodies.

---

# 1. RUNNER

Current provisional kinematic anchors:
- GRUNT speed = `0.070`
- RUNNER speed = `0.135`

Derived:
- speed ratio vs GRUNT = `~1.93x`
- common-spawn travel time to wall:
  - GRUNT `~13.14s`
  - RUNNER `~6.81s`
- arrival lead = `~6.33s`

Structural result:
`IDENTITY_ANCHOR_PRESENT`.

This is a large enough mechanical separation that RUNNER can plausibly express speed pressure.
But encounter admission still needs:
- distance advanced before death
- speed-driven front-order changes
- actual time-to-wall pressure under class traces

---

# 2. BRUTE

Current provisional anchors:
- GRUNT HP = `320`
- BRUTE HP = `900`
- HP ratio = `2.8125x`

Current authoritative/reference knock response anchors:
- GRUNT knock resistance factor = `0.85`
- BRUTE = `0.38`
- BRUTE displacement response is only `~44.7%` of GRUNT for the same base knock event

Structural result:
`DURABILITY_AND_KNOCK_IDENTITY_ANCHOR_PRESENT`.

This supports the intended raw-anchor role.
Still required for role-expression admission:
- frontlineBlockTime
- hitsReceived
- rawDamageAbsorbed
- screenTimeProvided

---

# 3. SHIELD

Current provisional anchors:
- HP = `540`
- armor damage multiplier = `0.72`
- per-hit prevented fraction = `28%`

Equivalent raw durability under the current simple armor model:
`540 / 0.72 = 750 raw-damage equivalent`.

Relative to GRUNT HP 320:
`~2.34x` raw-damage equivalent.

Representative hit-count examples:

| Raw hit | GRUNT hits to kill | SHIELD hits to kill |
|---:|---:|---:|
| 100 | 4 | 8 |
| 140 | 3 | 6 |
| 200 | 2 | 4 |
| 600 | 1 | 2 |

Structural result:
`MITIGATION_IDENTITY_ANCHOR_PRESENT`.

This proves armor materially changes hit requirements in the current provisional model.
Still required:
- mitigatedHits
- preventedDamage
- effectiveHitCount under actual action traces
- frontlineBlockTime

---

# 4. FLYER

Current provisional movement anchor:
- speed = `0.100`
- GRUNT speed ratio = `~1.43x`
- Y oscillation amplitude = `0.020`
- peak-to-peak Y movement = `0.040`
- omega = `5.0`

Structural result:
`GEOMETRY_CAPABILITY_ANCHOR_PRESENT`.

However this is the weakest of the four structural checks because a nonzero Y oscillation alone does not prove meaningful combat geometry.

Direct admission still needs:
- actual `flyerGeometryOpportunityTime`
- Archer line-opportunity difference
- Mage splash-opportunity difference
- target-order/secondary-target changes caused by Y geometry

Therefore FLYER remains measurement-blocked despite having a distinct motion model.

---

# 5. Interpretation

No passive monster currently appears structurally collapsed at the raw mechanic level:

```text
RUNNER -> strong speed separation
BRUTE  -> strong HP + knock-response separation
SHIELD -> strong mitigation/hit-count separation
FLYER  -> distinct Y-motion model
```

This means the next step is **measurement**, not redesign.

Do not respond by changing their production coefficients before temporal role-expression metrics are added.

---

# 6. Admission impact

Updated status:

| Monster | Structural anchor | Encounter role-expression admission |
|---|---|---|
| RUNNER | PASS | still metric-blocked |
| BRUTE | PASS | still metric-blocked |
| SHIELD | PASS | still metric-blocked |
| FLYER | PASS/WATCH | still metric-blocked |

The expensive next work is justified because the underlying identities are sufficiently distinct to measure rather than replace.

No live gameplay source or production balance value is changed by this report.
