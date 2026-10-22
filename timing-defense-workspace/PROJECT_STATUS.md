# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical implementation remains frozen during calibration

---

# Current phase

**SEPARATE SKILLED_V2/HIGH-MASTERY CALIBRATION DEPLOYMENT + DEVICE SMOKE**

Campaign spine, representative encounter role-expression, harness schema, and isolated harness source are complete enough to move to observed player evidence.

Current planning authority:
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- `54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
- `55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
- `60_SKILLED_V2_HARNESS_IMPLEMENTATION_STATUS_V0_1.md`
- `61_HIGH_MASTERY_PLAYER_ANCHOR_AMENDMENT_V0_1.md`
- `62_SKILLED_V2_CALIBRATION_DEPLOYMENT_READINESS_V0_1.md`

---

# Core structural truth

- 5 classes progress independently through Tiers.
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
- Stage46–49 = post-Lv31 mastery; Stage50 = final application.
- intended monster roles must become perceivable before deletion.

Model A remains the default bounded simulation spine:

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future
```

NOT production frozen.

---

# Closed validation chain

- Master Campaign Layer-0: PASS
- Encounter Envelope Layer-A0: PASS
- static/kinematic preflight: PASS / PASS_WITH_WATCHES
- class-aware role probes: COMPLETE
- Monster Role Expression Contract: ESTABLISHED
- Critical 10: PASS_WITH_WATCHES
- Full 20 representative audit: PASS_WITH_WATCHES

All-20 evidence:
```text
20 recipes × 3 deterministic brackets × 5 classes = 300 combat rows
36 designated role pairs × 15 rows = 540 structural checks
540 / 540 PASS
```

Remaining watches move forward into observed-player validation rather than broad geometry redesign.

---

# Player-model boundary

Historical 600/750/900ms brackets are analysis probes only and are NOT fitted SKILLED_V2.

Required future fitted profiles:
- `SKILLED_V2_CONSERVATIVE`
- `SKILLED_V2_CENTRAL`
- `SKILLED_V2_STRONG`
- `HIGH_MASTERY_STRESS`

The primary user reports that their own play should be treated above ordinary skilled.
Therefore their first observed traces are classified provisionally as:

`HIGH_MASTERY_STRESS_CANDIDATE`

This is a user-supplied calibration classification, not an objective rank certification.
Their traces MUST NOT be promoted directly into `SKILLED_V2_CENTRAL`.

The `<60%` non-T1 difficulty gate remains attached to future fitted `SKILLED_V2_CENTRAL`, not to the high-mastery candidate.

---

# Isolated harness implementation

Harness branch:
`timing-defense-skilled-v2-harness-v01`

Deployment-ready reviewed harness HEAD:
`85396e7da53eee1d64769d76b2a0e9700577aa34`

Dedicated root:
`timing-defense-skilled-v2-harness/`

Dedicated Worker name:
`timing-defense-skilled-v2-harness`

Implemented:
- H0–H5 selector
- audited timing input surface
- combo/charge/heavy/P×P trace
- H3 turnover/no-target evidence
- H4/H5 windup/response evidence
- local JSONL copy/download
- source selftest
- calibration-only health endpoint

Isolation:
- separate directory/project
- production source unchanged
- no production room/WebSocket integration
- no campaign stars/Tier/achievement/EXP/coin/shop persistence
- no external telemetry backend

Source status:
```text
JS syntax PASS
source contract selftest PASS
source isolation PASS
browser/device smoke PENDING
sample JSONL validation PENDING
```

---

# Calibration deployment authority

A separate calibration deployment is now AUTHORIZED for:
- browser/device smoke;
- sample JSONL validation;
- small controlled H0–H5 pilot.

It does NOT authorize production gameplay changes or broad public collection.

Deployment route:
Cloudflare Workers Builds + GitHub integration.

Required project settings:
- repo `hotmoral/-`
- branch `timing-defense-skilled-v2-harness-v01`
- root `timing-defense-skilled-v2-harness`
- Worker `timing-defense-skilled-v2-harness`
- deploy command `npx wrangler deploy`

The remaining blocker is Cloudflare account-side creation/connection of that separate project. The current chat environment has no Cloudflare connector.

---

# Exact next work

After the separate Cloudflare project is connected:
1. health check.
2. H0 mobile smoke.
3. H3 turnover smoke.
4. H4 stateful smoke.
5. JSONL export/copy.
6. canonical dataset validator.
7. verify production untouched.
8. patch only demonstrated harness defects.
9. collect small H0–H5 `HIGH_MASTERY_STRESS_CANDIDATE` pilot.
10. data-quality review.
11. acquire/derive ordinary-skilled evidence separately.
12. fit skilled profiles while keeping high mastery separate.
13. rerun role-expression regression.
14. build 10-Stage synthetic Tier slice.

---

# Still not frozen

- final launch Tier count
- exact Tier unlock policy
- production monster coefficients/coordinates
- exact 200-Stage schedule
- exact EXP formula
- Lv11+ production coefficients
- permanent star/achievement values
- boss/shop cadence
- detailed multiplayer balance

No production gameplay source or production balance value was changed by this calibration tranche.
