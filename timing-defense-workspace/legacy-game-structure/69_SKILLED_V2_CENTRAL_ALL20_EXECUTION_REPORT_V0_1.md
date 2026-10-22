# Timing Defense — SKILLED_V2 Central All-20 Execution Report V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL PASS WITH WATCHES / CENTRAL 540 OF 540 / HISTORICAL 540 OF 540 RETAINED / NOT PRODUCTION CALIBRATION**

Depends on:
- `67_SKILLED_V2_CENTRAL_SEQUENCE_MODEL_V0_1.md`
- `68_SKILLED_V2_CENTRAL_ALL20_INTEGRATION_PREFLIGHT_V0_1.md`
- `54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
- `data/skilled_v2_central_sequence_candidate_v0_1.yaml`
- `data/model_a_critical_role_expression_candidates_v0_1.yaml`
- `data/model_a_additional10_role_expression_candidates_v0_1.yaml` — content V0.2 after this execution
- `tools/run_skilled_v2_central_role_probe.py`
- `tools/simulate_class_aware_role_metrics_v0_2.py`
- `tools/evaluate_role_expression_v0_2.py`

---

## 0. Admission question

Can the 20-recipe representative Model-A library retain the Monster Role Expression Contract when the historical perfect-streak sensitivity brackets are replaced by the provisional streak-aware `SKILLED_V2_CENTRAL` design-prior sequence?

The central sequence is still a **user-authorized design prior**, not empirical population telemetry:

- PERFECT 70%
- GOOD 20%
- NORMAL 10%
- streak-aware two-state sequence
- combo40 remains structurally achievable in sufficiently long concentration windows

The current execution also retains the bounded `1100ms` action interval only as a simulation control. It is **not** promoted to fitted skilled cadence.

## Result

**YES, after two localized SPLITTER encounter refinements.**

Final result:

```text
20 recipes × 3 base seeds × 5 classes = 300 combat rows
36 designated role pairs × 3 base seeds × 5 classes = 540 role checks

CENTRAL:    540 / 540 PASS
HISTORICAL: 540 / 540 PASS
```

This is a structural admission result only.
It is not a production clear-rate claim and does not satisfy the later non-T1 `<60%` full-Tier difficulty gate.

---

## 1. Execution provenance

The execution environment did not have authenticated shell access to the private repository.

To avoid using stale local files, the required inputs and simulator sources were reconstructed from the current private GitHub `timing-defense-workspace` branch using their live blob contents, then executed in an isolated local scratch directory.

Production branch/source was read only for semantic verification and was not modified.

Base central seeds:

```text
101
211
307
```

Power mode:

```text
CURRENT_AUTHORITY_LV6
```

Action interval control:

```text
1100ms
status = BOUNDED_CURRENT_MECHANIC_SIMULATION_CONTROL_NOT_SKILL_FIT
```

---

## 2. First execution rejected — seed-prefix defect

The first implemented runner restarted the exact same sequence seed for every recipe/class row.

Because the representative encounters are short and all three selected seeds began inside long FOCUS prefixes, the aggregate consumed sequence was:

```text
PERFECT = 3033
GOOD    = 0
NORMAL  = 0
```

That run happened to report:

```text
540 / 540 role checks PASS
```

but the result was **rejected**.

It was not a valid 70/20/10 central-skilled probe; it was effectively a high-PERFECT prefix probe.

No balance or role conclusion from that first result is admitted.

---

## 3. Deterministic row-seed correction

The runner now derives a deterministic per-row seed from:

```text
FNV1A32(baseSeed | recipeId | classId)
```

The base seed still identifies the scenario bracket, while every recipe/class row gets a stable but distinct sequence prefix.

The runner now records both:

- `sequenceBaseSeed`
- `sequenceRowSeed`

This preserves deterministic replay without repeatedly sampling the same short FOCUS prefix.

---

## 4. Corrected pre-refinement result

After the row-seed correction, the central aggregate became materially representative of the provisional sequence instead of 100% PERFECT:

```text
PERFECT = 2297
GOOD    = 747
NORMAL  = 339
```

The role audit then exposed two real failures:

1. `T3_E20_L` / Mage / base seed 101 / SPLITTER
2. `T3_E08_M` / Mage / base seed 307 / SPLITTER

Both failed with:

```text
split-consequence-not-observed
```

The two failures were therefore investigated instead of weakening the player model or globally inflating monster HP.

---

## 5. SPLITTER same-action child erasure is current-authority behavior

The failing pattern was:

1. Mage base attack kills a SPLITTER parent.
2. SPLITTER children are spawned immediately at the parent's death position and timestamp.
3. Mage Lv6 splash processing for the same player action then queries the current monster list.
4. The newborn children can therefore be selected and killed by that same action.

This was checked against the current production-source capability chain:

- `v043-splitter-entry.js` immediately inserts children into `run.monsters` when a parent dies.
- `v036-entry.js` resolves Mage Lv6 splash after the base player action and enumerates the then-current `run.monsters` list.

Therefore the simulator behavior was not treated as an instrumentation bug.

The current combat ordering was preserved; encounter authoring was refined instead.

---

## 6. T3_E08_M localized refinement

Base representative timings contained SPLITTER insertions at:

```text
250ms
1750ms
```

The smallest common timing shift found that passed both the new central probe and the historical three-bracket audit was:

```text
SPLITTER #1 = 500ms
SPLITTER #2 = 2000ms
```

No global SPLITTER coefficient was changed.

Cross-check minima:

```text
central 3-seed × 5-class:
  minimum child-alive time ~= 2200ms

historical 3-bracket × 5-class:
  minimum child-alive time ~= 1200ms
```

The historical structural role gate remains intact.

---

## 7. T3_E20_L bounded re-author

E20 could not be repaired by a single small scalar change while preserving both central and historical gates.

No common pass region was found under isolated sweeps of:

- SPLITTER spawn time only
- SPLITTER X depth only
- CHARGER X depth only
- CHARGER time + X depth only
- second GRUNT time only
- GRUNT X depth only
- first-GRUNT phase shift only

This is therefore treated as a genuine bounded encounter re-author rather than a one-number patch.

Accepted diagnostic candidate:

```text
SPLITTER spawn       = 0ms
SPLITTER relative X  = -0.02
CHARGER spawn        = 2000ms
CHARGER relative X   = -0.50
```

Cross-check minima:

```text
central 3-seed × 5-class:
  SPLITTER child-alive minimum ~= 2200ms
  CHARGER visible-windup minimum ~= 400ms
  sampled wall damage = 0

historical 3-bracket × 5-class:
  SPLITTER child-alive minimum ~= 1200ms
  CHARGER visible-windup minimum ~= 250ms
  sampled wall damage = 0
```

The historical E20 CHARGER lower-tail readability WATCH therefore remains approximately where it was rather than being silently worsened.

These coordinates/timings remain diagnostic candidates, not production-frozen encounter authoring.

---

## 8. Final central all-20 result

After applying the E08 and E20 localized candidates, the corrected row-seed central probe produced:

```text
combat rows                 = 300
role checks                 = 540
role-expression failures    = 0
role-expression result      = 540 / 540 PASS
resolved within horizon     = 300 / 300
wall-damage rows            = 98 / 300
maximum sampled wall damage = 690
front reorders total        = 1908
```

`resolved within horizon` means the bounded encounter simulator reached an empty/resolved state.

It **does not** mean 300 production campaign clears. The current role simulator does not apply the complete campaign base-HP/failure/star model.

### Consumed judgment events

```text
PERFECT = 2308
GOOD    = 744
NORMAL  = 339
total   = 3391
```

Approximate finite-sample shares:

```text
PERFECT ~= 68.06%
GOOD    ~= 21.94%
NORMAL  ~= 10.00%
```

This finite aggregate is not fitted back into the player model.
Short correlated encounter samples are not expected to equal the exact stationary 70/20/10 marginal on every bounded run set.

### Heavy / P×P

```text
Heavy completions = 610
P×P completions   = 328
P×P rate          ~= 53.77%
```

### Combo peaks

Across these short encounter rows:

```text
minimum = 1
median  = 4
maximum = 20
```

This does not contradict the combo40 anchor.
The representative encounters are too short to provide the same streak opportunity as a multi-stage or full-Tier run.
Combo40 must be checked again under a persistent multi-stage simulation.

---

## 9. Historical all-20 regression cross-check

The updated E08/E20 overlay was then re-run against the original historical deterministic brackets:

```text
20 recipes × 3 historical brackets × 5 classes = 300 combat rows
36 designated pairs × 3 brackets × 5 classes   = 540 role checks
```

Result:

```text
540 / 540 PASS
0 role failures
wall-damage rows = 52
maximum sampled wall damage = 450
```

Therefore the central-skilled refinements did not regress the previously admitted all-20 structural role-expression set.

---

## 10. Difficulty WATCHES surfaced by the central probe

The structural role result is PASS, but the central run exposes useful downstream pressure signals.

### W1 — T4 siege pressure

The following representative recipes produced wall damage in all 15 central rows:

```text
T4_E10_M
T4_E11_M
T4_E18_M
T4_E19_M
```

This is not a role-expression failure; SIEGER response states remain visible.
It is a strong difficulty WATCH for the synthetic multi-stage/base-HP layer.

### W2 — T3_E13_H

`T3_E13_H` produced wall damage in 14/15 central rows.

This should be inspected as an upper T3 pressure candidate once persistent base HP and stage ordering are modeled.

### W3 — E20 CHARGER lower tail

Historical minimum visible windup remains around `~250ms`.

The central candidate improved that sampled minimum to about `~400ms`, but the historical lower tail remains a readability WATCH rather than a frozen threshold.

### W4 — finite marginal drift

The all-20 aggregate was approximately `68.06 / 21.94 / 10.00`, not exactly `70 / 20 / 10`.

Do not modify the sequence model merely to force this short, correlated sample to match the stationary prior exactly.

### W5 — combo40 not measurable here

The maximum combo observed in these representative encounter rows was 20 because individual encounters are short.

The combo40 ordinary-skilled anchor must be evaluated in persistent multi-stage/Tier context, not invalidated from these rows.

---

## 11. Admission consequence

Current pipeline state is now:

```text
all-20 historical role expression
  PASS_WITH_WATCHES

provisional SKILLED_V2_CENTRAL sequence
  admitted as design-prior simulation candidate

all-20 central role integration
  PASS_WITH_WATCHES / 540 OF 540

historical regression after localized re-author
  PASS / 540 OF 540
```

There is no remaining representative-role blocker before multi-stage simulation.

However:

- `SKILLED_V2_CENTRAL` is still not an empirical population fit.
- no production clear-rate has been measured.
- no final monster coefficients are frozen.
- no exact launch campaign has been authored.
- no production gameplay source was changed by this execution.

---

## 12. Exact next boundary

Next work is a **10-stage synthetic Tier** using the current provisional central sequence and the admitted representative encounter library.

The synthetic-Tier layer must add state that the current per-encounter probe does not preserve:

1. persistent base HP across stages;
2. actual fail/continue semantics;
3. persistent combo across encounter boundaries where game rules permit;
4. persistent charge/Heavy state where game rules permit;
5. stage-to-stage encounter ordering and pressure accumulation;
6. class comparison across all five classes;
7. wall-pressure localization, especially T3_E13 and T4 siege cases;
8. combo40 opportunity over a sufficiently long run;
9. deterministic replay under multiple sequence seeds.

Only after that layer is structurally coherent should full 50-stage Tier clear/failure/star calibration begin.

The later non-T1 `<60%` full-Tier gate remains downstream and must not be inferred from this report.
