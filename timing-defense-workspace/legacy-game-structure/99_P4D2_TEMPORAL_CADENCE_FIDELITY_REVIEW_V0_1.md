# Timing Defense — P4-D2 Temporal Cadence Fidelity Review V0.1

Date: 2026-10-23 KST  
Status: **METHODOLOGY CORRECTION REQUIRED BEFORE STAGE48–49 CLASS-FAIRNESS ADMISSION / NO GAME-RULE CHANGE / NO PRODUCTION CHANGE**

Authority:
- `../PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
- `../SKILL_PLAN_LV6_31.md`
- `64_HIGH_MASTERY_H3_OBSERVED_TRACE_REPORT_V0_1.md`
- `95_P4D2_STAGE46_STATEFUL_TEMPORAL_PRESSURE_PROBE_V0_1.md`
- `98_P4D2_STAGE48_49_GRAMMAR_RESET_PROXY_V0_1.md`
- `data/p4d2_stage48_49_dynamic_rotating_grammar_fixture_v0_1.json`
- `../../tools/run_p4d2_stage46_temporal_pressure_probe_v0_1.py`

---

# 0. Finding

Before admitting Stage48–49 dynamic miss-severity results, the temporal kernel needs a cadence-fidelity correction/sensitivity lane.

Current Stage46 temporal fixture uses one common root interval:

```text
rootAttackIntervalSeconds = 1.125
```

for all five classes.

However recovered Lv16 Rogue authority explicitly states:

```text
Assassin Rhythm
PERFECT-containing attack recovery: 390ms -> 312ms
exact reduction: 78ms
```

and the authority review says this requires **authoritative action-cadence eligibility**.

Therefore a common-cadence temporal kernel can be used as a broad pressure-existence stress lane, but it must not by itself authorize conclusions such as:

> Rogue has intrinsically much lower P×P miss tolerance than the other classes.

A second temporal fidelity issue is also present: the old runner leaves an overdue `next_attack` clock untouched while there is no target. When a target returns, that can create artificial catch-up attacks over subsequent short simulation ticks. This is unsuitable for class-fairness admission because classes that clear the screen more often can receive hidden banked action opportunities.

---

# 1. Why this matters specifically now

Document 95 found strong class divergence when one/two P×P opportunities were missed.
The first Stage48–49 rotating-grammar exploratory reconstruction showed that Rogue outcomes move materially when the legacy 78ms recovery reduction is represented as a cadence sensitivity.

That means the divergence is not safely attributable only to:
- Dagger Storm magnitude;
- encounter grammar;
- Rogue fragility.

It is partly entangled with an omitted lower-milestone cadence effect.

Likewise, the old no-target clock can favor classes whose strong Lv31 package creates empty-screen windows, because scheduled attack opportunities can effectively remain overdue and then be consumed in a catch-up burst after new spawns.

User governance requires these upstream simulation inconsistencies to be corrected before downstream balance patches.

---

# 2. Important Rogue semantic boundary

Do **not** reinterpret Assassin Rhythm as a blanket `20% faster whole combat loop` rule.

Recovered authority is narrower:

```text
legacy recovery component: 390ms
qualifying recovery component: 312ms
reduction: 78ms
```

The exact current server/action-cycle composition is not production-frozen.

Therefore P4-D2 should use at least two diagnostic cadence lanes until final action-cycle authority is available:

## Lane U — common-cadence stress

```text
all classes use 1.125s root interval candidate
```

Purpose:
- retain comparability with document 95;
- broad pressure-existence / geometry stress only.

## Lane R — Rogue recovery sensitivity

For qualifying Rogue PERFECT-containing actions, test the legacy-parity recovery delta as a sensitivity:

```text
candidate next-root interval = 1.125s - 0.078s = 1.047s
```

This is **not** a production cadence freeze.
It is the smallest faithful sensitivity that preserves the exact recovered `390 -> 312ms` delta without inventing a new 20%-of-whole-cycle rule.

If later authoritative cycle decomposition shows the 78ms recovery is not on the critical path at the observed player cadence, this lane may collapse back toward Lane U.

---

# 3. Other classes

Do not invent symmetric cadence modifiers merely to make the matrix look balanced.

Current authority review says:
- Archer Lv11 +25% projectile speed is presentation/time-of-flight behavior, not automatically a root action cadence reduction.
- Mage Lv21 slower/larger projectile is presentation/time-of-flight behavior, not automatically a root action cadence penalty.
- Knight/Tank have no corresponding recovered action-recovery modifier at Lv6–21.

Therefore only Rogue requires an explicit cadence sensitivity lane from currently recovered authority.

---

# 4. Effect on already accepted Stage46 evidence

Document 95 remains useful for its primary existence claim:

```text
there exists a current-nine-roster pressure envelope
where lower-kit play can fail
while repeated Lv31 P×P finals can stabilize pressure
```

However the following document-95 numbers must remain **diagnostic**, not class-fairness freeze authority:
- exact per-class burial time;
- one-miss/two-miss severity ranking;
- exact class recovery margin.

No need to reopen the user-approved Stage46 mastery-gate philosophy.
No need to reopen Lv31 identities.

---

# 5. Stage48–49 runner correction required

Before admitting dynamic rotating-grammar results:

1. preserve the existing deterministic combat/effect semantics wherever they are not under correction;
2. make cadence lane explicit in output metadata;
3. run `COMMON_1P125` for continuity;
4. run `ROGUE_RECOVERY_DELTA_78MS` sensitivity for Rogue;
5. label grammar family active at each Heavy/P×P opportunity by **timestamp**, not by assuming a fixed heavy-index-to-grammar mapping;
6. generate miss suites from the actual class-specific Heavy timeline;
7. prevent no-target periods from banking overdue attack opportunities into catch-up bursts;
8. compare successful-P×P vs miss outcomes without assuming monotonicity;
9. keep any `miss produces better end-wall` case as a target-order/authoring WATCH instead of hiding it.

---

# 6. Grammar-timeline execution-quality guard

Hardcoded miss indices such as:

```text
4 = SCATTER
5 = LINE
6 = CLUSTER
7 = FRONTLINE
```

are unsafe once class-specific cadence sensitivity is introduced, because the Heavy timeline can drift relative to the pressure-cycle timeline.

Future Stage48–49 runner must resolve:

```text
Heavy timestamp
-> active pressure-cycle index
-> grammar label
```

and choose the missed Heavy by grammar label/time relation.

This avoids false class comparisons caused by different cadence alignment.

---

# 7. No-target action-clock guard

The old temporal kernel effectively behaves like:

```text
if scheduled attack time arrives but no target exists:
    leave next_attack overdue

when a target later appears:
    attack
    next_attack += interval
    if still overdue, additional near-immediate catch-up attacks can follow
```

That creates a hidden **banked-action** mechanism.
No approved player-skill or run-state contract intentionally grants such banking.

Observed H3 calibration evidence instead shows a real target-reacquisition interval before the first post-turnover action; it does not support instant consumption of multiple stored attacks. The H3 median target-available -> action delay was about 632ms for the high-mastery stress participant, but that value is not a universal player constant and must not be silently frozen into campaign cadence.

Therefore the corrected P4-D2 class-fairness runner must use the structural rule:

```text
NO_TARGET_OPPORTUNITIES_DO_NOT_BANK
```

A minimal diagnostic implementation may drop/advance an expired action opportunity while no target exists, rather than preserving an overdue queue.

If a reacquisition-delay numeric value is needed later, it must be a separate explicit sensitivity lane using calibration authority; do not smuggle 632ms into the core combat model now.

This correction does **not** change production gameplay. It removes an accidental simulator-only advantage.

---

# 8. Current interpretation of class miss tolerance

Do not require identical numbers of tolerated P×P misses across classes.
Class asymmetry is allowed.

The valid late-game requirement is weaker and more useful:

```text
no class may ignore Lv31/P×P indefinitely in Stage48–49 mastery pressure
+
sustained or badly timed P×P failure must eventually produce dangerous backlog/burial
+
that failure path should arise from class/encounter interaction, not an omitted cadence rule or hidden banked-action artifact
```

Exact error-budget targets remain open.

---

# 9. Exact next boundary

`P4-D2 TEMPORAL CADENCE-FIDELITY CORRECTION / GRAMMAR-TIMELINE MAPPING / NO-TARGET CLOCK CORRECTION`

Do this before accepting Stage48–49 dynamic class-fairness results.

No user decision is required because this is a simulation-method fidelity correction, not a change to approved gameplay identity.

Do not:
- nerf Rogue because of the old common-cadence miss result;
- buff/nerf classes to compensate for banked-action artifacts;
- add hidden compensation;
- freeze Stage48–49 mistake budgets;
- modify production gameplay.
