# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Recovery rule
Always fetch live heads before any state claim:
1. `timing-defense-workspace`
2. `timing-defense-skilled-v2-harness-v01`
3. `timing-defense-cloudflare-do-poc`

Live remote wins over memory/chat/handoff.

---

# Production checkpoint

- v0.45 SIEGER FULL PASS
- branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- do not patch/deploy production during calibration

---

# Current phase

**SEPARATE CALIBRATION DEPLOYMENT -> DEVICE SMOKE -> SMALL PILOT**

Campaign structure and representative role-expression are not the blocker.
The isolated H0–H5 harness source is implemented and source-isolated.
Separate calibration deployment is authorized.

Current external blocker:
**Cloudflare account-side creation/connection of the separate Workers Builds project.**

The current chat environment has no Cloudflare connector, so that account-side step cannot be executed directly here.

---

# Read first

1. `PROJECT_STATUS.md`
2. `NEXT_WORK.md`
3. `legacy-game-structure/62_SKILLED_V2_CALIBRATION_DEPLOYMENT_READINESS_V0_1.md`
4. `legacy-game-structure/61_HIGH_MASTERY_PLAYER_ANCHOR_AMENDMENT_V0_1.md`
5. `legacy-game-structure/60_SKILLED_V2_HARNESS_IMPLEMENTATION_STATUS_V0_1.md`
6. `legacy-game-structure/55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
7. `legacy-game-structure/54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
8. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Harness branch deployment guide:
`timing-defense-skilled-v2-harness/DEPLOY_WORKERS_BUILDS.md`

---

# User-confirmed structural truth

- 5 classes; independent class Tier progression.
- same Tier/Stage combat content across classes.
- Tier = 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intended; hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 does not expose all 9; higher Tiers introduce species.
- future T5/T6/T7+ and new monsters remain open.
- fitted non-T1 `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60%.
- combo40 belongs inside ordinary skilled play.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery.
- Stage50 = final application.
- intended monster roles must become perceivable before deletion.

---

# Player calibration classification

The primary user explicitly states that they should not be treated as ordinary skilled and considers their play above that band.

Canonical interpretation before observed review:

`HIGH_MASTERY_STRESS_CANDIDATE`

This is provisional and self-reported, not an objective rank certification.

Rules:
- do not fit their traces directly into `SKILLED_V2_CENTRAL`;
- use them as an upper-tail stress anchor;
- do not tune Tier difficulty until their own clear rate is <60%;
- the `<60%` gate applies to future fitted `SKILLED_V2_CENTRAL` only;
- later ordinary-skilled evidence must be acquired/derived separately.

---

# Role-expression state

Critical 10: `PASS_WITH_WATCHES`.
Full 20 representative recipes: `PASS_WITH_WATCHES`.

Evidence:
```text
20 recipes × 3 deterministic brackets × 5 classes = 300 rows
36 role pairs × 15 rows = 540 structural checks
540 / 540 PASS
```

Historical 600/750/900ms brackets are probes only, not fitted skilled distributions.

---

# Harness implementation

Branch:
`timing-defense-skilled-v2-harness-v01`

Deployment-ready reviewed HEAD:
`85396e7da53eee1d64769d76b2a0e9700577aa34`

Root:
`timing-defense-skilled-v2-harness/`

Worker:
`timing-defense-skilled-v2-harness`

H0–H5 implemented.
Trace includes timing, combo, charge, heavy/P×P, turnover, and stateful response evidence.
Raw traces are copied/downloaded explicitly; no automatic external telemetry exists.

Isolation:
- no production gameplay file modified
- no production room/WebSocket integration
- no campaign persistence
- no external telemetry backend

Source checks PASS:
- JS syntax
- source contract selftest
- production isolation compare

Pending:
- Cloudflare separate project connection
- browser/device smoke
- sample JSONL validator
- observed pilot
- numeric fitting

---

# Cloudflare calibration deployment

Use Workers Builds + GitHub integration.

Settings:
- repository `hotmoral/-`
- branch `timing-defense-skilled-v2-harness-v01`
- root `timing-defense-skilled-v2-harness`
- Worker/project `timing-defense-skilled-v2-harness`
- build command empty unless required
- deploy command `npx wrangler deploy`

Must be a new/separate project from `timing-defense-do-poc`.
Do not paste API credentials into repository files.

---

# Exact next boundary

After account-side project connection:
1. verify calibration `/health`.
2. H0 mobile smoke: >=40 ACTION, combo/heavy/P×P coherence.
3. H3 smoke: no-target/reorder/reacquisition truth; inspect convenience wait field.
4. H4 smoke: readable WINDUP_START + response linkage.
5. export/copy JSONL.
6. canonical dataset validation.
7. confirm production state unchanged.
8. patch only smoke-demonstrated defects.
9. small H0–H5 pilot from user as `HIGH_MASTERY_STRESS_CANDIDATE`.
10. data-quality review.
11. ordinary-skilled evidence separately.
12. fit `SKILLED_V2_CONSERVATIVE/CENTRAL/STRONG`; keep `HIGH_MASTERY_STRESS` separate.
13. rerun All-20 role-expression candidates.
14. build 10-Stage synthetic Tier slice.

---

# Do not yet

- modify/deploy production v0.45
- use user's traces as ordinary-skilled center
- invent missing observations
- freeze production coefficients/coordinates
- author exact 200 launch Stages
- freeze final Tier count
- freeze exact EXP/star/achievement values
- freeze boss/shop cadence
- begin detailed 3P/4P production balance

No production gameplay source or production balance value was changed by this tranche.
