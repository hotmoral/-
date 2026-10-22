# Timing Defense — SKILLED_V2 Harness Implementation Preflight V0.1

Date: 2026-10-22 KST  
Status: **IMPLEMENTATION PREFLIGHT PASS / ISOLATED HARNESS ONLY / NO LIVE DEPLOYMENT AUTHORITY**

Depends on:
- `55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
- `56_SKILLED_V2_TRACE_COLLECTION_PIPELINE_V0_1.md`
- `57_SKILLED_V2_COLLECTION_READINESS_REVIEW_V0_1.md`
- `58_SKILLED_V2_PLAYABLE_HARNESS_IMPLEMENTATION_CONTRACT_V0_1.md`

Executable source baseline checked live:
- branch: `timing-defense-cloudflare-do-poc`
- HEAD: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- status: validated v0.45 SIEGER endpoint baseline

---

# 0. Decision

Implementation may proceed only as an isolated calibration surface.

Implementation branch:
`timing-defense-skilled-v2-harness-v01`

It must branch from the validated v0.45 source HEAD above, but it must not modify or deploy the production worker.

---

# 1. Reused timing semantics

The playable legacy/current source audit confirms the following input semantics to preserve:

- normalized sweep span: `.06 .. .94`
- one-way normal timing sweep: `1100ms`
- input lock: `100ms`
- GOOD window width: `.42`
- PERFECT window width: `.17`
- charge increments on non-heavy actions and heavy opportunity occurs after charge reaches 3
- heavy uses X then Y judgment
- heavy Y phase starts `85ms` after X lock
- normal recovery baseline: `390ms`
- PERFECT-only combo maintenance; non-PERFECT breaks the combo
- heavy consumes two judgment events
- P×P maps to CRITICAL

These are input/judgment semantics, not authorization to copy legacy campaign balance or progression.

---

# 2. Isolation requirements

The harness implementation must:
- use a separate directory/project
- use a distinct Cloudflare Worker name if later deployed
- not route through the production campaign worker
- not write campaign stars, Tier records, achievements, titles, EXP, coin, shop state, or multiplayer state
- store anonymous calibration identity only locally unless a later explicit telemetry backend is authorized
- export raw traces locally as schema-compatible JSONL
- visibly label all runs `HARNESS_ONLY / CALIBRATION`

No analytics service or production persistence is authorized.

---

# 3. H0–H5 implementation scope

Required selectable cases:
- H0 `TIMING_BASELINE`
- H1 `SUSTAINED_TEMPO`
- H2 `DURABLE_RHYTHM`
- H3 `TURNOVER_DENSITY`
- H4 `STATEFUL_READ`
- H5 `MIXED_PRESSURE`

The first implementation may use harness-local visual targets/monsters, but the measured timing/judgment/combo semantics must remain faithful to the audited game semantics.

H4 must expose a readable CHARGER-style WINDUP state and response opportunity; it must not use the old geometry where the CHARGER disappears before windup.

---

# 4. Trace contract

Every completed/aborted run must be exportable as JSONL compatible with:
`data/skilled_v2_trace_schema_v0_1.yaml`

Record families:
- `SESSION_START`
- `ACTION`
- `STATE`
- `SESSION_END`

Required properties:
- strict increasing action seq
- pressure context matches harness ID
- heavy/P×P logical fields consistent
- combo break cause populated
- H3 includes turnover evidence
- H4 includes stateful readable evidence
- H0 supports >=40 action opportunities

---

# 5. Local validation gates

Before any deployment or real collection:
1. H0 can reach 40+ action opportunities.
2. H3 produces `TARGET_REORDER` and reacquisition fields.
3. H4 produces `WINDUP_START` and response linkage.
4. JSONL validates structurally.
5. changing harness runs cannot mutate campaign progression because the harness has no campaign persistence path.
6. reload/restart does not accidentally submit data externally.

---

# 6. Non-goals

This implementation does not:
- fit `SKILLED_V2` numerically
- set the <60% Tier clear rate
- freeze production monster balance
- freeze campaign entry coordinates
- implement 200 stages
- alter live v0.45
- deploy a public calibration URL without a later explicit deployment step

---

# 7. Admission

```text
IMPLEMENTATION_PREFLIGHT = PASS
SOURCE_BASELINE = ea22cc279603394dc4b439b6fdbb0c83aff4299a
ISOLATED_BRANCH_REQUIRED = true
LIVE_DEPLOYMENT_AUTHORIZED = false
```

Next:
create the isolated branch and implement the smallest H0–H5 playable harness plus local JSONL export and self-validation.
