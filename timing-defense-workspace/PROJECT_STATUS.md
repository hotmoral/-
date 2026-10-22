# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production/source branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no production gameplay/numerical implementation authorized after v0.45

---

# Current planning phase

**SKILLED_V2 HARNESS BROWSER/DEVICE VALIDATION + PILOT TRACE READINESS**

Campaign structure and representative monster role-expression are sufficiently closed for observed player-model calibration.
The isolated playable harness source is now implemented, but browser/device evidence and observed H0–H5 traces do not exist yet.

Primary campaign authority:
- `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Current player-model/harness authority:
- `55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
- `56_SKILLED_V2_TRACE_COLLECTION_PIPELINE_V0_1.md`
- `57_SKILLED_V2_COLLECTION_READINESS_REVIEW_V0_1.md`
- `58_SKILLED_V2_PLAYABLE_HARNESS_IMPLEMENTATION_CONTRACT_V0_1.md`
- `59_SKILLED_V2_HARNESS_IMPLEMENTATION_PREFLIGHT_V0_1.md`
- `60_SKILLED_V2_HARNESS_IMPLEMENTATION_STATUS_V0_1.md`

---

# Core user-confirmed truth

- 5 classes progress independently through Tiers.
- same Tier/Stage combat content is shared across classes.
- Tier = exactly 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls are intentional; hard class lockout is forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 does not teach all 9; higher Tiers introduce new species.
- future T5/T6/T7+ and additional monsters remain open.
- fitted non-T1 `SKILLED_V2_CENTRAL` full-Tier clear should normally be **<60%**.
- that <60% gate is evaluated after fitting; it must not be achieved by deliberately fitting a weak player model.
- combo40 is ordinary skilled-achievable, not high-mastery-only.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery.
- Stage50 = final application, not Lv31 tutorial.
- intended monster roles must become perceivable before deletion.
- readable counterplay is required; full enemy ability success is not guaranteed.

---

# Model A

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future expansion
```

Status: default bounded simulation spine / **NOT production freeze**.

---

# Closed validation chain

- Master Campaign Layer-0: PASS
- Encounter Envelope Layer-A0: PASS
- static recipe preflight: PASS
- kinematic preflight: PASS WITH WATCHES
- generic DPS sensitivity: COMPLETE
- class-aware CURRENT_AUTHORITY probe: COMPLETE
- Monster Role Expression Contract: ESTABLISHED
- fine activation calibration: COMPLETE
- Role Metrics V0.2: READY
- Critical 10 role audit: PASS_WITH_WATCHES
- Full 20 representative role audit: PASS_WITH_WATCHES

All-20 evidence:
```text
20 recipes × 3 deterministic brackets × 5 classes = 300 combat rows
36 designated role pairs × 15 rows = 540 structural checks
540 / 540 PASS
```

Remaining role WATCHES:
- E20 CHARGER ~250ms lower-tail window
- FLYER ~255–325ms lower-tail geometry opportunity
- modest RUNNER lower-tail advance in some rows
- some conservative siege contact after response state begins

These are now evaluated against observed/fitted player behavior rather than prompting broad geometry redesign.

---

# SKILLED_V2 evidence boundary

Current deterministic 600/750/900ms brackets remain **analysis probes only**.
They are not fitted `SKILLED_V2` distributions.

Canonical fitting rules:
- preserve raw action/state sequence
- fit by context, not one global iid judgment vector
- measure cadence, P/G/N/MISS, combo survival, heavy/P×P behavior, turnover reacquisition, stateful response, pressure degradation
- keep `HIGH_MASTERY_STRESS` separate from ordinary skilled profiles
- never reverse-fit player weakness to force the game below 60% clear
- missing observations remain `INSUFFICIENT_OBSERVED_TRACE_COVERAGE`, not invented probabilities

---

# Isolated harness implementation

Implementation preflight: PASS.

Implementation branch:
`timing-defense-skilled-v2-harness-v01`

Source baseline:
`ea22cc279603394dc4b439b6fdbb0c83aff4299a`

Last reviewed harness HEAD:
`7c541e3eb1e51ef9788f943e4603debc5a775e79`

Dedicated directory:
`timing-defense-skilled-v2-harness/`

Dedicated Worker name:
`timing-defense-skilled-v2-harness`

Implemented H0–H5:
- H0 TIMING_BASELINE
- H1 SUSTAINED_TEMPO
- H2 DURABLE_RHYTHM
- H3 TURNOVER_DENSITY
- H4 STATEFUL_READ
- H5 MIXED_PRESSURE

Implemented source capabilities:
- audited timing sweep/judgment semantics
- combo and charge/heavy X→Y flow
- P×P tracking
- H3 NO_TARGET/TARGET_REORDER state events + reacquisition timing
- H4/H5 CHARGER-style WINDUP state + response linkage
- local anonymous calibration identity
- local JSONL copy/download
- bounded in-browser validator
- source selftest
- isolated `/api/health`

Source checks:
```text
JS syntax = PASS
source contract selftest = PASS
source isolation comparison = PASS
browser/device smoke = PENDING
canonical sample JSONL validation = PENDING
```

Compared with production baseline, the harness branch only adds the dedicated harness directory. No production gameplay file was modified.

No public calibration deployment has been performed or authorized.

---

# Instrumentation WATCH

The raw H3 interval is preserved by ordered STATE events:
`NO_TARGET_START -> NO_TARGET_END -> TARGET_REORDER -> first post-turnover ACTION`.

The optional convenience ACTION field `noTargetWaitMsBeforeAction` may currently be zero once the target has returned.
The interval remains derivable from raw timestamps, but browser smoke must either confirm/fix the convenience field or formalize derivation in the collection pipeline before broad collection.

---

# Current exact work

Next:
**HARNESS BROWSER/DEVICE SMOKE + SAMPLE TRACE VALIDATION**.

Required:
1. H0 real-browser run: >=40 ACTION records, combo/heavy/P×P trace coherence.
2. H3 run: no-target, reorder, reacquisition truth; inspect the convenience wait field.
3. H4 run: readable WINDUP_START and response linkage.
4. copy/download sample JSONL on target browser/device.
5. pass exported sample through canonical `validate_skilled_v2_trace_dataset.py`.
6. verify no campaign or external telemetry mutation.
7. after PASS only, consider an isolated calibration deployment for small controlled pilot collection.
8. perform pilot data-quality review before numeric fitting.

Numeric `SKILLED_V2` fitting remains blocked until observed data exists.

---

# Still not frozen

- final launch Tier count
- exact Tier unlock policy
- production monster coefficients
- production encounter coordinates/timings
- exact 200-Stage schedule
- exact EXP formula
- Lv11+ production coefficients
- permanent star reward values
- achievement reward graph/value
- boss cadence/design
- shop cadence/economy
- detailed multiplayer balance

No live production gameplay code or production balance value was changed by this planning/harness tranche.
