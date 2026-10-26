# Timing Defense — Next Work Boundary

Updated: 2026-10-26 KST

## Mandatory recovery order

1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_59.yaml`;
5. preserve Stage16/17 approval `182_T1_STAGE16_17_EXACT_SPAWN_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`;
6. preserve B1 closure `181_T1_CONTIGUOUS_15_25_B1_DYNAMIC_ADMISSION_AND_CLOSURE_V0_1.md`;
7. preserve Wave A approval `180_T1_WAVE_A_EXACT_SPAWN_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`;
8. preserve Stage49-50 approval `174_T1_STAGE49_50_STRUCTURAL_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`;
9. recover Stage26-28 structural signature authority from the Stage1-50 skeleton and coupled contracts;
10. verify production/harness live heads before any execution that depends on them.

Do not rerun closed Stage49-50, Wave A, or B1 evidence without a concrete trigger.

---

# Current state

```text
Stage49-50 = USER APPROVED STRUCTURAL AUTHORING BASELINE WITH WATCHES
Wave A 13 Stages = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage16/17 = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage15-25 = CANONICAL CONTIGUOUS EXACT AUTHORING WINDOW
B1 persistent dynamic admission = PASS_WITH_WATCHES

full Stage1-50 exact recipe freeze = DEFERRED
production gameplay = UNCHANGED / UNAUTHORIZED
CURRENT = T1_C1_STAGE26_28_CONTIGUOUS_BRIDGE_AUTHORING_PREFLIGHT
```

---

# Closed B1 evidence to preserve

Candidate source:
`legacy-game-structure/data/t1_contiguous_15_25_b1_stage16_17_candidate_v0_1.yaml`

Approval source:
`legacy-game-structure/182_T1_STAGE16_17_EXACT_SPAWN_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`

```text
candidate SHA256
b9abc507c5ccdc20bc19c5681ba92cead920326fa9d04c1acf5b2ed90ff91465

materialized Stage15-25 SHA256
f769dd79e750882a6b7a75dad18bfdbc514da546b183587ec2ed909e50b2ed0f

100/100 persistent cases completed through Stage25
terminal failures = 0
persistent continuity = PASS
deterministic replay = PASS
settlement/carry invariants = PASS
```

Stage16/17 exact spawn count, timestamp, monster type and Y placement are now canonical authoring authority WITH WATCHES.

---

# Progression reach boundary

Do not invent exact unlock Stages.

```text
Lv16 Stage18-21 = calibration-candidate reach band
Lv21 Stage25-28 = calibration-candidate reach band
```

No final EXP semantics or exact milestone threshold is frozen.

---

# Exact next package

```text
T1_C1_STAGE26_28_CONTIGUOUS_BRIDGE_AUTHORING
```

Target:

```text
Stage26
Stage27
Stage28
```

Why this package is next:

```text
left exact anchor  = Stage25
right exact anchor = Stage29-31
smallest gap       = Stage26-28
future contiguous window after adoption = Stage15-31
Lv21 reach band tail = Stage26-28
```

The package is deliberately limited to three Stages. Do not broaden it to unrelated Stage32+ authoring before the C1 evidence closes.

---

# Required C1 order

```text
1. recover Stage26-28 signature-skeleton authority
2. recover relevant pressure/cadence/formation guards
3. identify upstream/downstream exact anchors
4. define bounded C1 authoring contract
5. only then create exact spawn candidates
6. run static materialization/admission
7. if static PASS, determine whether lifecycle-faithful dynamic admission is required
8. exact content authority changes require explicit user adoption
```

Do not fabricate skipped-Stage persistent state. Any dynamic execution that claims Stage15-31 continuity must use every Stage in sequence with correct `STAGE_SETTLED` boundaries.

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE16_17 ARE USER-APPROVED AUTHORING AUTHORITY
WAVE A IS USER-APPROVED AUTHORING AUTHORITY
NO FAKE SKIPPED-STAGE PERSISTENT CHAIN
STAGE_SETTLED REQUIRES DELAYED EVENT QUEUE DRAINAGE
NO FULL-50 EXACT AUTHORING YET
AUTHORED 4s NORMAL DENSITY <= 8
NO CLASS OR MONSTER SCALAR CHANGE
NO SHOP/EXP/P×P CHANGE
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```

Current action: **C1 Stage26-28 structural recovery and bounded authoring preflight.**
