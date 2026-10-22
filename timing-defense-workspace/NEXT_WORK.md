# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Executable production checkpoint
- v0.45 SIEGER FULL PASS
- production/source baseline HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production branch `timing-defense-cloudflare-do-poc`
- no gameplay/numerical implementation authorized after v0.45

---

# ACTIVE PHASE — SKILLED_V2 Harness Browser/Device Validation + Pilot Readiness

Completed chain:

```text
Master Campaign Spine
 -> Layer-0 PASS
 -> encounter envelope PASS
 -> class-aware role-expression calibration
 -> Critical 10 PASS_WITH_WATCHES
 -> All-20 PASS_WITH_WATCHES
 -> SKILLED_V2 measurement/harness schema READY
 -> isolated playable harness preflight PASS
 -> isolated HARNESS_ONLY source implementation V0.1 COMPLETE
 -> source isolation PASS
```

The current blocker is no longer campaign structure, monster role geometry, or harness specification.
The current blocker is **real browser/device evidence from the isolated harness**.

---

# Read first

1. `legacy-game-structure/60_SKILLED_V2_HARNESS_IMPLEMENTATION_STATUS_V0_1.md`
2. `legacy-game-structure/59_SKILLED_V2_HARNESS_IMPLEMENTATION_PREFLIGHT_V0_1.md`
3. `legacy-game-structure/58_SKILLED_V2_PLAYABLE_HARNESS_IMPLEMENTATION_CONTRACT_V0_1.md`
4. `legacy-game-structure/57_SKILLED_V2_COLLECTION_READINESS_REVIEW_V0_1.md`
5. `legacy-game-structure/56_SKILLED_V2_TRACE_COLLECTION_PIPELINE_V0_1.md`
6. `legacy-game-structure/55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
7. `legacy-game-structure/54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
8. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Harness implementation:
- branch `timing-defense-skilled-v2-harness-v01`
- last reviewed HEAD `7c541e3eb1e51ef9788f943e4603debc5a775e79`
- directory `timing-defense-skilled-v2-harness/`
- distinct Worker name `timing-defense-skilled-v2-harness`

Canonical player-model data/tools:
- `legacy-game-structure/data/skilled_v2_controlled_harness_v0_1.yaml`
- `legacy-game-structure/data/skilled_v2_trace_schema_v0_1.yaml`
- `tools/validate_skilled_v2_harness.py`
- `tools/validate_skilled_v2_trace_dataset.py`
- `tools/summarize_skilled_v2_trace_dataset.py`

---

# User-confirmed structural truth

- 5 classes; independent class Tier progression.
- same Tier/Stage combat content across classes.
- Tier = exactly 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intended; hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 does not expose all 9; higher Tiers introduce species.
- future T5/T6/T7+ and new monsters remain open.
- fitted non-T1 `SKILLED_V2_CENTRAL` full-Tier clear should normally be **<60%**.
- the <60% value is a post-fit game-difficulty gate, never a reason to weaken the fitted player model.
- combo40 is ordinary skilled-achievable, not high-mastery-only.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application.
- intended monster roles must become perceivable before deletion; readable counterplay is required, full enemy activation is not guaranteed.

---

# Current Model A

```text
T1: GRUNT / RUNNER / BRUTE
T2: +SHIELD / +FLYER
T3: +CHARGER / +SPLITTER
T4: +SUPPORTER / +SIEGER
T5+: future expansion
```

Status: bounded simulation spine, **not production frozen**.

---

# Role-expression status

Critical 10: `PASS_WITH_WATCHES`.

All 20 representative recipes: `PASS_WITH_WATCHES`.

Evidence volume:
```text
20 recipes × 3 deterministic brackets × 5 classes = 300 combat rows
36 designated recipe-role pairs × 15 rows = 540 role checks
540 / 540 structural role gates PASS
```

Remaining watches are deferred to fitted-player evidence rather than more broad geometry tuning:
- E20 CHARGER ~250ms lower-tail window
- FLYER ~255–325ms lower-tail geometry opportunity
- modest RUNNER lower-tail advance in some rows
- some conservative siege wall pressure after response begins

Do not resume broad encounter geometry tuning unless fitted traces reopen a specific failure.

---

# Isolated harness state

Source baseline:
`ea22cc279603394dc4b439b6fdbb0c83aff4299a`

Implementation branch:
`timing-defense-skilled-v2-harness-v01`

Last reviewed implementation HEAD:
`7c541e3eb1e51ef9788f943e4603debc5a775e79`

Implemented:
- H0 TIMING_BASELINE
- H1 SUSTAINED_TEMPO
- H2 DURABLE_RHYTHM
- H3 TURNOVER_DENSITY
- H4 STATEFUL_READ
- H5 MIXED_PRESSURE
- audited timing/judgment semantics
- combo/charge/heavy/P×P tracing
- H3 target-turnover/no-target state evidence
- H4/H5 CHARGER-style WINDUP evidence
- local anonymous calibration ID
- local JSONL copy/download
- bounded in-browser trace checks
- source selftest

Isolation:
- separate directory/project
- separate Worker name
- no production room/WebSocket integration
- no campaign star/Tier/achievement/EXP/coin/shop persistence
- no external telemetry service
- no public calibration deployment performed

Source checks:
- JS syntax PASS
- source contract selftest PASS
- source isolation comparison PASS

---

# Instrumentation WATCH

`noTargetWaitMsBeforeAction` is optional in schema V0.1.

The raw trace preserves no-target ground truth through ordered:
`NO_TARGET_START -> NO_TARGET_END -> TARGET_REORDER -> first post-turnover ACTION`.

The current convenience ACTION field may be zero after the target returns. Before broad collection, browser smoke must verify this and either:
- carry the closed interval into the first post-turnover ACTION, or
- formally derive it from ordered raw STATE timestamps in the collection pipeline.

Do not discard raw STATE order.

---

# EXACT NEXT BOUNDARY

Next bounded tranche = **HARNESS BROWSER/DEVICE SMOKE + SAMPLE TRACE VALIDATION**.

Required order:
1. H0 smoke in a real browser/device.
   - timing surface usable
   - >=40 ACTION records possible
   - combo sequence recorded
   - heavy/P×P fields coherent
2. H3 smoke.
   - NO_TARGET_START/END
   - TARGET_REORDER
   - first post-turnover action
   - reacquisition delay
   - inspect/fix `noTargetWaitMsBeforeAction` convenience field
3. H4 smoke.
   - readable WINDUP_START
   - response action linkage
   - interrupt/full-activation truth reconstructable
4. verify JSONL copy/download on target browser/device.
5. run exported traces through canonical `validate_skilled_v2_trace_dataset.py`.
6. verify harness activity cannot mutate production campaign state and does not submit data externally.
7. only after smoke PASS, decide whether a **separate calibration deployment** is useful for small controlled pilot collection.
8. collect a small H0–H5 pilot dataset.
9. run data-quality review before any numeric fitting.
10. only then fit/bound `SKILLED_V2_CONSERVATIVE/CENTRAL/STRONG`; keep `HIGH_MASTERY_STRESS` separate.
11. rerun all-20 role-expression candidates under fitted traces.
12. then build the 10-Stage synthetic Tier slice.

Do NOT yet:
- deploy or modify the production v0.45 worker
- publicly deploy the calibration harness without explicit authorization
- invent missing observed player probabilities
- promote old deterministic 600/750/900ms brackets to SKILLED_V2
- author exact 200 launch Stages
- freeze production monster coefficients/entry coordinates
- freeze final Tier count
- freeze exact EXP/star/achievement values
- freeze boss/shop cadence
- start detailed 3P/4P production balance

Governance:
`structure -> role-expression PASS -> observed player harness -> fitted player model -> role regression -> synthetic slice -> full Tier -> soft-wall/meta recovery -> explicit freeze -> implementation`.
