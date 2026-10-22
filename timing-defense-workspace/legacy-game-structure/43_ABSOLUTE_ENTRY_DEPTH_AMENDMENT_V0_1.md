# Timing Defense — Absolute Entry Depth Amendment V0.1

Date: 2026-10-22 KST  
Status: **AUTHORING-SCHEMA AMENDMENT / NUMBERS NOT FROZEN**

Triggered by:
- `42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`

---

# 0. Problem

Earlier formation work added relative X-depth (`spawnXOffset`) because BACK label + delayed spawn was insufficient.

Class-aware micro-sim found a second independent geometry axis:

> the entire encounter can start too far from the wall for CHARGER/SIEGER capability timing to matter before a strong class removes the encounter.

Relative FRONT/MID/BACK can be correct while absolute entry position is still wrong.

---

# 1. New distinction

## Relative depth
Who is in front of whom inside a formation.

Example:
```text
SHIELD x=0.70
SIEGER x=0.80
```

SIEGER is correctly behind SHIELD.

## Absolute entry depth
Where the whole formation enters the battlefield.

Compare:
```text
A: SHIELD 1.05 / SIEGER 1.15
B: SHIELD 0.55 / SIEGER 0.65
```

Both preserve the same +0.10 backline relation.
But B reaches CHARGER/SIEGER trigger/standoff grammar much earlier.

These are separate authoring variables.

---

# 2. Schema candidate

Future integrated schema should support both:

```yaml
formation:
  id: Fxx
  baseSpawnXOffset: number|null
  slots:
    - role: front|mid|back|air|free
      spawnXOffset: number|null
      offsetY: number|null
```

Optional encounter-level override for bounded/special cases:

```yaml
encounterEvent:
  entryBaseXOffsetOverride: number|null
```

Semantics:
- negative offset = closer to wall
- positive offset = farther from wall
- slot spawnXOffset remains relative to the formation base
- neither field overrides targeting

Runtime target selection remains actual frontmost position.

---

# 3. Why this is not a hidden difficulty scalar

Absolute entry depth changes:
- time until CHARGER trigger
- time until SIEGER standoff
- time available to remove screens
- wall-arrival pressure
- duration of SUPPORTER aura interaction

It is therefore real encounter geometry, not an invisible stat multiplier.

It must be authored/read as part of the tactical problem.

---

# 4. Guardrails

Do not solve every difficulty problem by moving monsters closer to the wall.

Required checks:
- enough visual reaction time remains
- first appearance/teaching uses conservative depth
- later high-pressure versions may enter deeper into the field only after grammar is learned
- wall damage cannot become unavoidable before the player receives a meaningful action window
- special unit must not be nominally BACK while actually frontmost at spawn
- class hard lockout remains forbidden

---

# 5. Capability-specific use

## CHARGER
Absolute depth is a first-order variable because trigger occurs at authoritative `triggerX`.

A CHARGER recipe that clears before any unit reaches trigger is not measuring CHARGER.

## SIEGER
Absolute depth is a first-order variable because the unit must:
```text
approach -> reach standoff -> windup -> fire
```

If encounter lifetime is shorter than this path, SIEGER becomes a normal body.

## SUPPORTER
Depth affects how long recipients remain inside aura while the supporter is screened.

## SPLITTER
Depth affects whether children have enough travel time to create a meaningful second frontline before being removed.

---

# 6. First sweep result — diagnostic only

Using the current unfitted CENTRAL trace bracket and preserving a +0.10 relative special-unit back offset:

### T3_E17_M CHARGER
Moving the whole formation toward the wall eventually makes windup observable to all five classes.

First all-five activation in the current diagnostic sweep occurred around:
```text
shiftTowardWall ≈ 0.45 X
```

This is **not a production coordinate recommendation**.
It only proves the capability-disappearance defect can be corrected through geometry without immediately inflating HP.

### T4 E11/E19 SIEGER
The current SIEGER requires a much more aggressive forward-entry shift before first-shot visibility appears across several classes.
A diagnostic threshold around ~0.70 X was needed for broad activation in the unfitted CENTRAL bracket.

That magnitude is a strong WATCH:
- simply moving the entire formation close to the wall may create unacceptable unavoidable objective pressure
- therefore SIEGER may require a combination of entry geometry + spawn timing + later numerical capability calibration

Do not adopt `0.70` as production data.

---

# 7. Design consequence

For CHARGER/SIEGER we now have three distinct adjustment layers:

1. **relative formation depth**
2. **absolute entry depth / spawn timing**
3. **provisional capability numbers**

Adjustment order:
```text
geometry/readability
 -> exposure/protection timing
 -> capability uptime
 -> only then HP/speed/standoff/trigger numerical tuning
```

Global HP inflation remains the last-resort response.

---

# 8. Next

Run bounded entry-depth sweeps to find a **readable activation envelope**, not a single coordinate.

Required next outputs:
- first CHARGER windup by class
- CHARGER interruptability after trigger
- first SIEGER shot by class
- screened vs unscreened first shot
- wall damage before first meaningful player response
- class spread in capability exposure

Then choose revised representative recipe geometry candidates and rerun Layer-A.
