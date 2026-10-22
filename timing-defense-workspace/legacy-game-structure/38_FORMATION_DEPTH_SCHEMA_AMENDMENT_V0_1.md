# Timing Defense — Formation X-Depth Schema Amendment V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL SCHEMA AMENDMENT / DESIGNED_NOT_AUTHORITATIVE**

Applies to:
- `07_AUTHORING_DATA_SCHEMA.md`
- `33_MODEL_A_FORMATION_CADENCE_VOCABULARY_V0_1.md`
- future Tier/Stage/Encounter authoring data

Evidence:
- `37_REPRESENTATIVE_RECIPE_KINEMATIC_PREFLIGHT_REPORT_V0_1.md`

---

# 0. Problem

Existing formation intent can express:
- lane
- FRONT/MID/BACK depth label
- Y offset
- spacing
- arrival timing

But kinematic preflight showed that **spawn delay alone does not preserve backline position** when unit speeds differ.

Example:
- BRUTE speed < SUPPORTER speed
- a later SUPPORTER starting at the same X can overtake the BRUTE
- authoring label `BACK` then disagrees with actual frontmost runtime order

Since runtime targeting correctly follows actual X, the authoring layer needs a way to create real geometric depth rather than a label-only depth.

---

# 1. New field

Formation slot candidate gains:

```yaml
formation:
  id: string
  slots:
    - lane: ground|air
      depth: front|mid|back
      spawnXOffset: number|null
      offsetY: number|null
      spacing: number|null
      arrivalOffsetMs: number|null
```

Semantics:
- positive `spawnXOffset` = farther from wall / deeper backline
- zero = common encounter spawn anchor
- negative values are not required by current Model A and should be separately justified if later used

Name may be revised before production schema freeze, but the capability is required.

---

# 2. Important authority boundary

`spawnXOffset` is **not target-order override**.

It only changes initial authoritative geometry.
After spawn:
- movement speed
- knockback
- aura effects
- state transitions
- death
can reorder units naturally.

The target system continues to select actual frontmost/valid targets.

---

# 3. Why arrivalOffsetMs alone is insufficient

A delayed fast unit can catch and pass an earlier slow unit.
Therefore:

```text
BACK != later spawn time only
```

Backline intent may require both:
```text
arrivalOffsetMs + spawnXOffset
```

or one sufficiently strong geometric control depending on the recipe.

---

# 4. Current simulation-only depth candidates

From first kinematic preflight:

| Formation | Type | spawnXOffset candidate |
|---|---|---:|
| F06 SCREEN_BACKLINE | SUPPORTER | +.030 |
| F06 SCREEN_BACKLINE | SIEGER | +.100 |
| F07 ESCORT_COLUMN | SUPPORTER | +.120 |
| F07 ESCORT_COLUMN | SIEGER | +.120 |
| F08 SPLIT_AXIS | SIEGER | +.080 |
| F09 REPLICATION_CLUSTER | SUPPORTER | +.020 |

These are **not production coordinates**.
They exist only in `model_a_kinematic_anchor_v0_1.yaml` to test whether tactical intent can be realized.

---

# 5. Validator requirement

Future formation/recipe validators should be able to compare:
- intended depth
- actual frontmost sequence
- backline exposure time
- protected capability uptime

Warnings:
- BACK unit becomes frontmost before intended exposure window
- screen never actually exists
- protected unit never enters useful capability range
- depth offset so large that aura/interaction never occurs

---

# 6. Generalization to future monsters

This amendment is not SUPPORTER/SIEGER-specific.
Future monsters may include:
- artillery
- healer/support
- summoner
- objective specialist
- long-range debuffer

Any such unit may need actual geometric depth without manual targeting.

Therefore `spawnXOffset` becomes part of the extensible authoring vocabulary rather than a one-off hack.

---

# 7. Status

Required structural capability: **ACCEPTED AS CURRENT DESIGN DIRECTION**.

Exact field name, units, bounds and production values remain open until authoring-data schema freeze.
