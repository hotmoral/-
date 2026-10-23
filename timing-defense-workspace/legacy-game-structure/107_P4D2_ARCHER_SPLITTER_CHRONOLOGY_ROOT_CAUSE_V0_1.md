# Timing Defense — P4-D2 Archer SPLITTER Chronology Root Cause V0.1

Date: 2026-10-23 KST  
Status: **ROOT CAUSE EXPLAINED / AUTHORING WATCH RETAINED / NO ARCHER NERF / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Authority / context:
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`
- `95_P4D2_STAGE46_STATEFUL_TEMPORAL_PRESSURE_PROBE_V0_1.md`
- `tools/run_p4d2_stage46_temporal_pressure_probe_v0_1.py`

---

# 0. Question

Previous temporal probes occasionally showed a non-monotonic Archer result:

```text
successful Lv31 P×P
-> lower final wall HP than an otherwise comparable missed P×P path
```

The concern was whether the wider / stronger `Sky-Piercing Arrow` itself was structurally wrong.

Result:

**No. The mechanism is explained by transformation chronology and finite-horizon encounter ordering.**

---

# 1. Exact kernel behavior

The Archer final takes a snapshot of current corridor targets before resolving the hit loop:

```text
for target in list(lane_targets(...)):
    hit(...)
```

When a `SPLITTER` parent dies inside `hit(...)`, its two children are appended immediately to the live mob list.

However, those newborn children were not members of the already-materialized `list(lane_targets(...))` snapshot.

Therefore:

```text
one Sky-Piercing Arrow
-> may kill SPLITTER parent
-> children spawn immediately
-> same arrow does NOT retroactively hit those newborn children
```

This is deterministic and consistent with one locked straight projectile package. It is not recursion or random retargeting.

---

# 2. Why a successful final can worsen a finite-horizon wall result

The user-approved wider Lv31 corridor can hit an adjacent-band SPLITTER that a missed Lv31 path falls back to the narrower Lv21 trajectory and does not hit at that moment.

Using current diagnostic anchors:

```text
SPLITTER parent speed = 0.065
SPLITTER child speed  = 0.115
wall contact x        = 0.155
example parent x      = 0.500
common root interval  = 1.125s diagnostic lane
```

If the successful wider final kills the parent immediately at x=0.500:

```text
child time to wall = (0.500 - 0.155) / 0.115
                   = 3.000s
```

If the missed-final path leaves that adjacent parent alive until the next ordinary root opportunity, the parent advances first:

```text
parent x after 1.125s = 0.500 - 0.065*1.125
                      = 0.426875

child wall time from original comparison origin
= 1.125 + (0.426875 - 0.155)/0.115
= 3.48913s
```

So the stronger successful final can start the child-pressure clock about:

```text
3.48913 - 3.00000 = 0.48913s earlier
```

If the parent survives two or three later root opportunities before dying, the child-pressure clock can shift by roughly:

```text
2.25s delayed parent kill -> ~0.978s later child arrival
3.375s delayed parent kill -> ~1.467s later child arrival
```

That difference can change:
- which body becomes `nearest()` next;
- whether a CHARGER reaches WINDUP before the next reset;
- whether a SIEGER survives into its firing window;
- whether a child reaches the wall before the 60s diagnostic horizon;
- subsequent target/band ordering.

Therefore a finite-horizon wall metric can occasionally improve when a final is missed, even though the missed action is not actually stronger.

---

# 3. Interpretation

Classification:

```text
ARCHER_POWER_DEFECT = NO
ARCHER_WIDER_CORRIDOR_DEFECT = NO
DETERMINISM_DEFECT = NO
SPLITTER_TRANSFORM_CHRONOLOGY_EFFECT = CONFIRMED
FINITE_HORIZON_TARGET_ORDER_EFFECT = CONFIRMED
```

This explains the earlier non-monotonicity watch at the causal layer.

Do not repair this by:
- reducing Archer Lv31 damage;
- narrowing the user-approved wider corridor;
- preventing the final from killing SPLITTER parents;
- adding hidden target exceptions.

---

# 4. Authoring safeguard

The remaining watch is encounter-authoring, not Archer balance.

Late-stage authoring should avoid repeatedly placing an adjacent-band SPLITTER such that:

```text
successful wide final
-> immediate parent transform
-> newborn children get a uniquely dangerous uncontestable wall timing
```

without a readable follow-up opportunity.

Good patterns may deliberately use this interaction if the player has a fair next-action response, but it should not become an invisible penalty for landing P×P.

Keep:

`LV31_ARCHER_SUCCESS_MONOTONICITY_CHRONOLOGY_WATCH`

but reclassify it from `UNKNOWN_HIGH` to:

`ROOT_CAUSE_EXPLAINED / AUTHORING_MONOTONICITY_WATCH`

---

# 5. P4-D2 consequence

The chronology issue does **not** block the approved Archer structural direction.

Current Archer structural direction remains:
- one huge locked straight final arrow;
- wider gameplay corridor than ordinary/Lv26 arrows;
- unlimited target depth inside the real corridor;
- armor ignore;
- no homing / bending / off-line retarget.

Exact width and coefficient remain provisional.
