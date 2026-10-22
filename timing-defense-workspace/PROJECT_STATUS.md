# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# Current planning phase

**SKILLED_V2 Controlled Harness / Player-Model Fitting**

Upstream campaign structure and representative role-expression authoring are sufficiently closed for player-model calibration.
Model A remains the default bounded simulation spine, not a production freeze.

Primary campaign authority:
- `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Current lower-layer evidence:
- `53_CRITICAL_ROLE_EXPRESSION_V0_2_RERUN_REPORT_V0_1.md`
- `54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `52_ROLE_METRICS_V0_2_INSTRUMENTATION.md`

---

# Core user-confirmed truth

- 5 classes progress independently through Tiers.
- Same Tier/Stage combat content is shared across classes.
- Tier = exactly 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intentional; hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 does not teach all 9; higher Tiers introduce new species.
- future T5/T6/T7+ and additional monsters remain open.
- fitted non-T1 `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60%.
- combo40 is skilled-achievable, not high-mastery-only.
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

Fallback Model B remains available only if T4 lower-layer evidence later reopens a structural failure.

---

# Validation chain

- Master Campaign Layer-0: PASS
- Encounter Envelope Layer-A0: PASS
- Representative static recipe preflight: PASS
- Kinematic preflight: PASS WITH WATCHES
- Generic DPS sensitivity: COMPLETE
- Class-aware CURRENT_AUTHORITY V0.1: COMPLETE
- Monster Role Expression Contract: ESTABLISHED
- Fine activation calibration: COMPLETE
- Passive-role structural anchors: COMPLETE
- Role Metrics V0.2: READY
- Critical 10 role-expression audit: PASS_WITH_WATCHES
- Full 20 representative role-expression audit: PASS_WITH_WATCHES

All-20 audit population:
```text
300 combat rows
36 designated recipe-role pairs
540 structural role checks
540 / 540 PASS
```

No production difficulty claim follows because the player brackets are still unfitted.

---

# Important refined role candidates

Diagnostic only; not production coordinates/timings.

## CHARGER
- E07: entry shift ~0.44, CHARGER spawn ~1550ms, min current visible windup ~435ms
- E13: entry shift ~0.425, CHARGER spawns ~760/1960ms, min visible windup ~430ms
- E17: entry shift ~0.49, CHARGER relative depth ~+0.10, min visible windup ~445ms
- E20: base formation preserved; SPLITTER ~1400ms, CHARGER late-insert ~2350ms with relative X ~-0.46; min CHARGER visible window ~250ms WATCH

## SUPPORTER
- E09: SUPPORTER ~800ms, total relative X 0.00; min aura ~1005ms, screened ratio ~0.735
- E12: SUPPORTER ~1050ms, total relative X ~+0.02; min aura ~755ms, screened ratio ~0.827
- E16: SUPPORTER ~2800ms, total relative X 0.00; min aura ~955ms, screened ratio ~0.389
- E19 remains strong support candidate

## SIEGER
- E10 focused siege: entry shift ~0.70, SIEGER total relative depth 0.00, spawn ~900ms; min current windup opportunity ~1275ms
- E11 escort siege: entry shift ~0.70, GRUNTs 750/1000ms, SIEGER 1250ms; min windup opportunity ~470ms
- E18 dual-axis: entry shift ~0.685, SIEGER total relative depth 0.00, spawn ~2300ms; min windup ~1230ms
- E19 fortress: entry shift ~0.70, min current windup ~535ms

All remain simulation candidates only.

---

# Role opportunity vs full activation

For stateful monsters:

```text
role opportunity != full ability success
```

Examples:
- CHARGER visible windup followed by interrupt/deletion = valid skilled counterplay
- SIEGER standoff/windup followed by kill before shot = valid skilled counterplay

Do not inflate HP merely to force ability completion against STRONG traces.

---

# Current WATCHES

- E20 CHARGER lower-tail visible window ~250ms
- FLYER geometry opportunity lower tails ~255–325ms
- some RUNNER lower-tail advance remains modest
- some CONSERVATIVE siege recipes allow ordinary wall contact only after the response state begins
- exact minimum readable-time thresholds remain open
- current trace brackets remain deterministic mechanics probes, not fitted player distributions

These watches should now be resolved through player-model fitting rather than more broad geometry tuning.

---

# Current exact work

Now work on:
**SKILLED_V2 controlled harness and fitting preparation**.

Required next outputs:
- machine-readable H0–H5 harness definitions
- timing/combo/heavy/turnover/pressure telemetry schema
- fit/bounded Conservative/Central/Strong profiles
- explicit HIGH_MASTERY_STRESS separation
- validation that combo40 is ordinary skilled-achievable
- context-sensitive pressure and turnover degradation
- role-expression regression under fitted traces

After the player model is sufficiently fitted/bounded:
- 10-Stage synthetic Tier slice
- then full Tier simulation
- then skilled-clear / failure-location / star-progression calibration

---

# Still not frozen

- final launch Tier count
- exact Tier unlock policy
- production monster coefficients
- production entry coordinates/timings
- exact 200-Stage schedule
- exact EXP formula
- Lv11+ production coefficients
- permanent star reward values
- achievement reward graph/value
- boss cadence/design
- shop cadence/economy
- detailed multiplayer balance

No live gameplay code or production balance value was changed by the current planning tranche.
