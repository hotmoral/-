# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Canonical recovery rule
Always fetch live `timing-defense-workspace` HEAD first.
Live remote wins over memory/chat/handoff.

Also fetch the isolated harness branch before making harness-state claims:
`timing-defense-skilled-v2-harness-v01`.

---

# PRODUCTION CHECKPOINT

- v0.45 SIEGER FULL PASS
- production branch: `timing-defense-cloudflare-do-poc`
- production/source HEAD: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health version historically `0.45-cf.1`
- no production gameplay/numerical implementation authorized after v0.45
- do not deploy or patch the production worker during SKILLED_V2 calibration work

---

# CURRENT PHASE

**SKILLED_V2 HARNESS BROWSER/DEVICE VALIDATION + PILOT TRACE READINESS**

Campaign structure and representative monster role-expression are no longer the current blocker.
The full 20-recipe representative library passed the bounded structural role audit with watches.

The H0–H5 playable calibration harness source now exists on a separate branch and passes source-level isolation checks.
The current evidence gap is **real browser/device traces**.

Do NOT:
- resume broad encounter geometry tuning without fitted evidence,
- invent skilled-player numeric probabilities,
- deploy the harness publicly without an explicit deployment step,
- touch the production v0.45 worker.

---

# READ FIRST

1. `PROJECT_STATUS.md`
2. `NEXT_WORK.md`
3. `legacy-game-structure/60_SKILLED_V2_HARNESS_IMPLEMENTATION_STATUS_V0_1.md`
4. `legacy-game-structure/59_SKILLED_V2_HARNESS_IMPLEMENTATION_PREFLIGHT_V0_1.md`
5. `legacy-game-structure/58_SKILLED_V2_PLAYABLE_HARNESS_IMPLEMENTATION_CONTRACT_V0_1.md`
6. `legacy-game-structure/57_SKILLED_V2_COLLECTION_READINESS_REVIEW_V0_1.md`
7. `legacy-game-structure/56_SKILLED_V2_TRACE_COLLECTION_PIPELINE_V0_1.md`
8. `legacy-game-structure/55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
9. `legacy-game-structure/54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
10. `legacy-game-structure/53_CRITICAL_ROLE_EXPRESSION_V0_2_RERUN_REPORT_V0_1.md`
11. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Machine-readable player-model contracts:
- `legacy-game-structure/data/skilled_v2_controlled_harness_v0_1.yaml`
- `legacy-game-structure/data/skilled_v2_trace_schema_v0_1.yaml`

Validation tools:
- `tools/validate_skilled_v2_harness.py`
- `tools/validate_skilled_v2_trace_dataset.py`
- `tools/summarize_skilled_v2_trace_dataset.py`

Role-expression evidence tools remain available, but are no longer the active work center.

---

# USER-CONFIRMED STRUCTURAL TRUTH

- 5 classes; independent class Tier progress.
- same Tier/Stage combat content across all classes.
- Tier = exactly 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear Stage50=3★.
- stars = broad permanent account growth.
- achievements = targeted cross-class progression.
- recoverable soft walls intended; hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 does not expose all 9; higher Tiers introduce new species.
- future T5/T6/T7+ and additional monsters remain open.
- fitted non-T1 `SKILLED_V2_CENTRAL` full-Tier clear should normally be **<60%**.
- the <60% value is a game-difficulty gate applied after player fitting, not a target used to weaken the player model.
- combo40 belongs inside ordinary skilled play; it must not be assumed high-mastery-only.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery.
- Stage50 = final application, not Lv31 tutorial.
- intended monster roles must become perceivable before deletion.
- minimum expression + readable counterplay required; full enemy activation not guaranteed.

---

# MODEL A

Default bounded simulation spine:

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future expansion
```

NOT production frozen.
Model B remains fallback only if fitted evidence later reopens a genuine T4 structural overload.

---

# ROLE-EXPRESSION AUDIT CLOSED

Critical 10:
`PASS_WITH_WATCHES`.

Full representative 20:
`PASS_WITH_WATCHES`.

Audit scale:
```text
20 recipes × 3 deterministic brackets × 5 classes = 300 combat rows
36 designated recipe-role pairs × 15 rows = 540 structural role checks
540 / 540 PASS
```

Current WATCHES:
- E20 CHARGER minimum current visible window ~250ms
- FLYER lower-tail geometry opportunity ~255–325ms
- modest RUNNER lower-tail advance in some high-pressure rows
- some conservative siege wall contact after the response state begins
- exact minimum readable-time thresholds remain open

Do not tune these further using unfitted synthetic brackets unless observed player evidence demonstrates a real failure.

---

# PLAYER MODEL AUTHORITY BOUNDARY

Historical deterministic probes:
- CONSERVATIVE ~900ms
- CENTRAL ~750ms
- STRONG ~600ms

Status:
**NOT FITTED SKILLED_V2**.

Never cite these as actual skilled-player distributions.

Required observed components before fitting:
- action cadence distribution
- PERFECT/GOOD/NORMAL/MISS by pressure context
- combo reach/survival and break hazard
- heavy attempt/completion
- P×P attempt/completion
- target-turnover reacquisition
- no-target intervals
- stateful response latency
- pressure degradation

Profiles eventually fitted:
- SKILLED_V2_CONSERVATIVE
- SKILLED_V2_CENTRAL
- SKILLED_V2_STRONG
- HIGH_MASTERY_STRESS separately

Missing data must remain `INSUFFICIENT_OBSERVED_TRACE_COVERAGE`.

---

# H0–H5 HARNESS CONTRACT

H0 `TIMING_BASELINE`
- clean timing/combo ceiling
- >=40 action opportunities required

H1 `SUSTAINED_TEMPO`
- sustained tempo degradation

H2 `DURABLE_RHYTHM`
- long-target rhythm and heavy/P×P behavior

H3 `TURNOVER_DENSITY`
- target turnover, no-target interval, reacquisition, post-turnover judgment

H4 `STATEFUL_READ`
- readable CHARGER-style windup, response latency, interrupt/full-activation truth

H5 `MIXED_PRESSURE`
- already-learned mixed pressure transfer

All harnesses are `HARNESS_ONLY` and must not affect campaign progress.

---

# ISOLATED PLAYABLE HARNESS IMPLEMENTATION

Implementation branch:
`timing-defense-skilled-v2-harness-v01`

Created from exact validated production/source baseline:
`ea22cc279603394dc4b439b6fdbb0c83aff4299a`

Last reviewed harness HEAD:
`7c541e3eb1e51ef9788f943e4603debc5a775e79`

Dedicated directory:
`timing-defense-skilled-v2-harness/`

Dedicated Worker name:
`timing-defense-skilled-v2-harness`

Implemented files include:
- `README.md`
- `IMPLEMENTATION_STATUS.md`
- `package.json`
- `wrangler.jsonc`
- `src/index.js`
- `public/index.html`
- `public/styles.css`
- `public/harness.js`
- `test/harness-selftest.mjs`

Implemented behavior:
- H0–H5 selectable
- class tag selectable for grouping only
- audited normalized timing sweep
- input lock 100ms
- normal one-way sweep 1100ms
- GOOD width .42 / PERFECT width .17
- charge 3 -> heavy opportunity
- heavy X -> Y delay 85ms
- normal recovery 390ms
- PERFECT combo continuation
- P×P tracked
- H3 NO_TARGET_START/END + TARGET_REORDER
- H4/H5 WINDUP_START + tactical response linkage
- raw ordered JSONL records
- explicit copy/download, no automatic upload
- local anonymous calibration ID
- local end-of-run bounded validation
- `/api/health` reports HARNESS_ONLY, campaignPersistence=false, externalTelemetry=false

Isolation check:
- harness branch compared to `ea22cc279...`
- only dedicated harness-directory files added
- no existing production gameplay file modified
- no production room/WebSocket integration
- no campaign star/Tier/achievement/EXP/coin/shop persistence
- no external analytics/telemetry backend

Source checks completed:
- JavaScript syntax check PASS
- source selftest PASS
- branch isolation compare PASS

Not yet completed:
- browser/device smoke
- exported sample JSONL canonical validation
- observed H0–H5 traces
- numeric player fitting

No public calibration deployment has been authorized or performed.

---

# INSTRUMENTATION WATCH

Raw H3 ground truth is preserved in ordered STATE records:

```text
NO_TARGET_START
 -> NO_TARGET_END
 -> TARGET_REORDER
 -> first post-turnover ACTION
```

The optional ACTION convenience field `noTargetWaitMsBeforeAction` may currently be 0 because the open interval is cleared when the target returns.

This does not lose the raw interval; it is reconstructable from timestamps.
Before broad collection, browser smoke must decide one of:
1. carry the closed interval into the first post-turnover ACTION, or
2. formally derive it in the collection pipeline.

Do not discard/reorder raw STATE events.

---

# EXACT NEXT BOUNDARY

Proceed with **HARNESS BROWSER/DEVICE SMOKE + SAMPLE TRACE VALIDATION**.

Order:
1. fetch live planning HEAD and harness HEAD.
2. run H0 in a real browser/device.
   - >=40 ACTION records
   - timing surface usability
   - combo sequence
   - heavy/P×P logical fields
3. run H3.
   - NO_TARGET_START/END
   - TARGET_REORDER
   - first post-turnover ACTION
   - reacquireDelayMs
   - inspect `noTargetWaitMsBeforeAction`
4. run H4.
   - visible/readable WINDUP_START
   - response action linkage
   - interrupt/full-activation truth
5. verify JSONL copy/download on target browser/device.
6. validate exported traces with `validate_skilled_v2_trace_dataset.py`.
7. verify no campaign state mutation and no external submission.
8. patch only defects demonstrated by this smoke.
9. after PASS, decide whether to create a separate calibration deployment for a small controlled pilot.
10. collect small H0–H5 pilot traces.
11. run pilot data-quality review before fitting any numeric profile.
12. after sufficient observed coverage, fit/bound Conservative/Central/Strong, keep HIGH_MASTERY_STRESS separate.
13. rerun all-20 role-expression candidates with fitted traces.
14. then build a 10-Stage synthetic Tier slice.
15. only later run full-Tier skilled clear/failure/star calibration against the non-T1 <60% gate.

---

# DO NOT YET

- modify/deploy the production v0.45 worker
- publicly deploy the harness without explicit calibration-deployment authority
- claim numeric SKILLED_V2 from source code or old deterministic brackets
- invent missing observations
- author exact 200 launch Stages
- freeze production monster coefficients/coordinates
- freeze final Tier count
- freeze EXP/star/achievement values
- freeze boss/shop cadence
- start detailed 3P/4P production balance

---

# HANDOFF DISCIPLINE

New session must:
1. fetch live `timing-defense-workspace` HEAD first
2. fetch live `timing-defense-skilled-v2-harness-v01` HEAD
3. read this handoff + PROJECT_STATUS + NEXT_WORK
4. read docs 60 -> 55 and all-20 report 54 as needed
5. verify production branch still at intended protected baseline before any execution claim
6. continue from browser/device harness-validation boundary only

No production gameplay source or production balance value was changed by this work.
