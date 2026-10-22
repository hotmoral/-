# Timing Defense — Cross-Bracket Role Expression Robustness V0.1

Date: 2026-10-22 KST  
Status: **UNFITTED THREE-BRACKET DIAGNOSTIC / NOT SKILLED_V2 OR PRODUCTION FREEZE**

Depends on:
- `48_ROLE_EXPRESSION_FINE_SCAN_REPORT_V0_1.md`
- `49_E11_SIEGE_TIMING_ADJUSTMENT_REPORT_V0_1.md`
- `data/model_a_role_expression_geometry_overrides_v0_1.yaml`
- `tools/probe_sieger_readability_budget.py`

Profiles:
- `TRACE_BRACKET_CONSERVATIVE`
- `TRACE_BRACKET_CENTRAL`
- `TRACE_BRACKET_STRONG`

All are deterministic calibration brackets, not fitted player distributions.

---

# 0. Purpose

A geometry candidate that only works under CENTRAL is not robust enough even for bounded authoring.

This pass asks:
- does minimum role expression survive weaker/faster deterministic action traces?
- does STRONG erase the mechanic before the player can read it?
- does CONSERVATIVE create excessive wall pressure?

---

# 1. CHARGER E07

Initial lower anchor `~0.53`:
- CONSERVATIVE: 5/5 windup expression
- CENTRAL: 5/5
- STRONG: 4/5

A slight move to approximately `0.54` restores:

```text
CONSERVATIVE 5/5
CENTRAL      5/5
STRONG       5/5
```

All-profile five-class windup expression remains across a broader diagnostic band approximately `0.54..0.64`.

In CONSERVATIVE, some classes allow CHARGER to complete its readable charge cycle and reach the wall for the current 110 damage anchor.
That is **not the same defect as pre-expression deletion**:
- windup was visible
- response opportunity existed
- charge outcome occurred afterward

It therefore becomes a later difficulty/counterplay question, not a spawn-delete failure.

Current structural candidate:
`E07 ~0.54 lower-edge anchor`.

---

# 2. CHARGER E17

At the earlier lower anchor around `0.43`, STRONG can still erase one class's windup opportunity.

The cleanest current three-bracket anchor is approximately:
`shiftTowardWall ~= 0.49`.

At this diagnostic point:

```text
CONSERVATIVE: 5/5 windup expression, 0 wall damage
CENTRAL:      5/5 windup expression, 0 wall damage
STRONG:       5/5 windup expression, 0 wall damage
```

Outcomes remain asymmetric:
- some classes allow charge completion
- some interrupt/delete during the response window

This is the desired structural pattern.

Current status:
`ROBUST_ROLE_EXPRESSION_CANDIDATE`.

---

# 3. SIEGER E11 — actual shot is too strict for minimum expression

E11 adjusted CENTRAL candidate near `0.70` with the two GRUNTs delayed +250ms:
- CONSERVATIVE: all five classes can see actual SIEGER fire
- CENTRAL: all five
- STRONG: only a subset completes an actual shot at the authoritative current 800ms windup

If admission used `shotCount > 0` as the minimum contract, strong play would be incorrectly classified as deleting the role.

But the role contract is:

```text
reach standoff
 -> enter/read windup
 -> player may stop the shot
```

A diagnostic survivable-windup sweep at the same geometry shows STRONG still has bounded post-standoff response-state survival for every class:

| Class | max diagnostic windup still allowing >=1 shot |
|---|---:|
| Knight | ~800ms |
| Rogue | ~500ms |
| Tank | ~800ms |
| Archer | ~800ms |
| Mage | ~200ms |

Interpretation:
- all five classes structurally reach SIEGER's response state
- Mage/Rogue can remove it before an 800ms windup completes
- that is valid strong counterplay, not automatic role erasure

CENTRAL and CONSERVATIVE show >=800ms in this proxy for all five classes at this geometry.

E11 still has a separate CONSERVATIVE wall-pressure WATCH; temporal wall-hit instrumentation is needed to determine whether those ordinary hits occur before or after a meaningful response opportunity.

---

# 4. SIEGER E19

At the lower anchor around `0.70`:
- CONSERVATIVE/CENTRAL actual-shot expression remains broad
- STRONG actual-shot count falls sharply for fast-kill classes

Readability-budget proxy under STRONG:

| Class | max diagnostic windup still allowing >=1 shot |
|---|---:|
| Knight | ~800ms |
| Rogue | ~600ms |
| Tank | ~800ms |
| Archer | ~500ms |
| Mage | ~500ms |

Thus all five classes reach a meaningful SIEGER response state even though not all five allow the full 800ms shot to complete.

This is closer to the desired role-expression contract than an all-five guaranteed-shot rule.

---

# 5. Why `actual activation rate` cannot equal `role expression rate`

For stateful monsters:

```text
role opportunity
 !=
full ability success
```

If a strong player sees the telegraph and kills/interrupts correctly, the encounter has succeeded structurally even though the enemy ability fails.

Required future result fields:
- `roleOpportunityCount`
- `roleOpportunityVisibleMs`
- `counterplayResolvedCount`
- `fullActivationCount`
- `preOpportunityErasureCount`

CHARGER currently approximates this better because windup entry is already measured.
SIEGER still needs direct state-duration instrumentation; the windup-budget tool is only a proxy.

---

# 6. Current candidate state

```text
E07 CHARGER: ~0.54 three-bracket role-expression candidate
E17 CHARGER: ~0.49 strong three-bracket candidate
E11 SIEGER:  ~0.70 + GRUNT +250ms candidate; wall-pressure WATCH
E19 SIEGER:  ~0.70 role-opportunity candidate
```

None are production coordinates.

---

# 7. Remaining blockers

Critical-set role-expression admission is still BLOCKED by:
1. direct SIEGER windup-opportunity duration instrumentation
2. temporal ordinary wall-hit classification for E11/E19 weaker traces
3. RUNNER/BRUTE/SHIELD/FLYER direct metrics
4. SPLITTER child alive/frontline/reorder metrics
5. SUPPORTER alive-time + normalized aura ratio

---

# 8. Design consequence

Do not force SIEGER to always fire for STRONG players.
That would destroy valid mastery reward and likely require artificial HP inflation.

The correct requirement is:
> the player must be able to perceive the SIEGER problem and make a meaningful response before deleting it.

No live gameplay source or production monster value is changed by this diagnostic.
