# Timing Defense — Next Work Boundary

Updated: 2026-10-26 KST

## Mandatory recovery order

1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_61.yaml`;
5. preserve C1 approval `legacy-game-structure/184_T1_STAGE26_28_EXACT_SPAWN_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`;
6. preserve C1 technical closure `183_T1_CONTIGUOUS_15_31_C1_DYNAMIC_ADMISSION_AND_CLOSURE_V0_1.md`;
7. preserve Stage16/17 approval, B1 closure, Wave A approval and Stage49-50 approval;
8. read D1 plan `legacy-game-structure/data/t1_contiguous_32_d1_authoring_plan_v0_1.yaml`.

Do not rerun closed Stage49-50, Wave A, B1 or C1 evidence without a concrete trigger.

## Current state

```text
Stage15-31 = CANONICAL CONTIGUOUS EXACT AUTHORING WINDOW
C1 Stage26-28 = USER APPROVED AUTHORING BASELINE WITH WATCHES
C1 static = PASS
C1 persistent dynamic = PASS_WITH_WATCHES
100/100 complete Stage15->31
terminal failures = 0

full Stage1-50 exact recipe freeze = DEFERRED
production gameplay = UNCHANGED / UNAUTHORIZED

CURRENT = T1_D1_STAGE32_SINGLE_GAP_AUTHORING_PREFLIGHT
```

## Exact next package

```text
T1_D1_STAGE32_SINGLE_GAP_AUTHORING
```

Why Stage32:

```text
Stage31 = exact / approved
Stage32 = missing
Stage33 = exact / approved through Wave A
```

It is the smallest remaining contiguous gap. Future adoption would extend the canonical exact window from Stage15-31 to Stage15-33 with only one newly authored Stage.

Stage32 structural contract:

```text
Band       Pressure / Soft Wall
Archetype  E02
Monsters   GRUNT + RUNNER
Formation  F04
Cadence    CD04
Complexity C2
Pressure   RUSH
Opportunity Rogue / Tank
```

Adjacent Stage33 approved authority is a C2 GRUNT density-pressure stage using F03/CD04, so Stage32 must preserve a readable `durable Stage31 -> tempo Stage32 -> density Stage33` rotation rather than becoming another density package.

## Required D1 order

```text
1. recover exact Stage31 and Stage33 authorities
2. recover CD04/F04 and count/density envelopes
3. define bounded Stage32 exact-authoring contract
4. materialize Stage32 exact spawn candidate
5. run static materialization/admission
6. determine minimum lifecycle-faithful dynamic evidence actually needed
7. any canonical Stage32 adoption requires explicit user approval
```

Do not fabricate skipped-Stage persistent state. If a dynamic run claims contiguous persistence beyond Stage31, execute all required Stages with correct `STAGE_SETTLED` boundaries.

## Fixed guards

```text
LIVE REMOTE WINS
STAGE15-31 CANONICAL EXACT WINDOW
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
AUTHORED 4s NORMAL DENSITY <= 8
NO CLASS OR MONSTER SCALAR CHANGE
NO SHOP/EXP/P×P CHANGE
NO EXACT LV21/LV26 EXP REACH FREEZE
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
NO FULL T1 STAGE1-50 EXACT RECIPE FREEZE
```
