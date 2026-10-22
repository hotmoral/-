# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes remain unauthorized during planning/calibration

---

# ACTIVE PHASE — P4-B REVISED EXP ROUTING DECISION

Completed evidence chain:

```text
P0 Foundation
 -> P1 Run-State Lifecycle
 -> P2 Modifier / Attribution Pipeline
 -> P3 Persistent 10-Stage Kernel PASS
 -> P4 methodology USER APPROVED
 -> P4-A Marker-Only 50-Stage Inverse Design PASS
 -> P4-B Solo Lv6→Lv21 feedback diagnostic COMPLETE
 -> P4-B Multiplayer / Timebase bounded precheck COMPLETE
```

Current evidence:
- `legacy-game-structure/81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p4b_combat_feedback_divergence_v0_1.json`
- `legacy-game-structure/83_P4B_MULTIPLAYER_TIMEBASE_PRECHECK_V0_1.md`
- `legacy-game-structure/data/p4b_multiplayer_timebase_precheck_v0_1.json`

Revised decision proposal:
- `legacy-game-structure/84_P4B_EXP_DECISION_REASSESSMENT_PROPOSAL_V0_1.md`

The existing dependency plan `system_dependency_calibration_order_v0_5.yaml` predates the multiplayer/timebase precheck. Its immediate Option-D recommendation must not be executed without the revised decision.

---

# What the comparison established

## Solo
Pure per-turn EXP can create a large class-specific reach split after Lv6–21 skill power changes timing-turn opportunity.

## Multiplayer
That solo split is **partially compressed**, because team members share the same enemy pool and Stage duration.

But it is not eliminated:
- mixed-team players still show different XP/min;
- the same class changes XP/min with different teammates;
- player-count encounter scaling changes per-player XP opportunity;
- faster team damage does not always create proportionally more Stages/min because spawn/cadence creates a duration floor;
- more attack opportunity can coexist with worse clear/failure performance.

Therefore neither of these conclusions is justified yet:

```text
"pure per-turn EXP is definitely broken"
"pure per-turn EXP is definitely fine"
```

---

# EXACT NEXT DECISION

Choose one revised route.

## R1 — Stage Quality Budget now
Adopt the previously proposed normalization direction immediately.

**Not recommended now** because current-roster multiplayer scaling is not yet authoritative.

## R2 — provisional pure per-turn + split final convergence — RECOMMENDED
Keep the currently approved pure per-valid-turn semantics as the provisional measurement baseline, but do not freeze it as final.

Then:
1. proceed to a separate Lv26 structural contract decision;
2. after approval, run bounded Lv26 power feedback;
3. later review Lv31 structural contract and mastery behavior;
4. close the player-power spine only provisionally with explicit EXP watches;
5. after credible current-roster 2P/3P/4P scaling exists, run a mandatory EXP/timebase reconvergence before permanent progression is allowed to depend on the curve.

This keeps skill-design work moving without pretending the multiplayer progression problem is already solved.

## R3 — freeze pure per-turn now
**Not recommended.** Solo divergence and team-composition/player-count dependencies remain unresolved.

---

# If R2 is approved

Immediate next boundary becomes:

```text
P4-C1 — LV26 STRUCTURAL SIMULATION CONTRACT DECISION
```

Important:
- first review the five Lv26 skill identities and unresolved implementation semantics;
- do not invent generic Lv26 power proxies;
- do not claim final Lv26/Lv31 Stage reach from the provisional EXP baseline;
- keep Solo / team-composition / player-count progression watches active.

A future dependency-plan revision should split P4 skill-contract work from post-multiplayer EXP reconvergence. That plan revision is not activated before user approval of R2.

---

# Do not yet

- activate Option D / Stage Quality Budget
- freeze pure per-turn EXP as final
- start Lv26 simulation power before its contract decision
- add class-specific or Tier-specific XP correction
- change production v0.45 gameplay
- freeze P4-A anchors or visible EXP values
- homogenize Tier encounter flow for progression
- author exact 200 launch Stages
- freeze multiplayer scaling or permanent progression values
