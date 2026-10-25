# T1 Stage49-50 STAGGER1800 Authoring Candidate Static Preflight v0.1

Date: 2026-10-25 KST

Status:
**STATIC PASS / BOUNDED AUTHORING CANDIDATE / NO DYNAMIC ADOPTION / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

## 1. Purpose

Materialize the Stage49-50 diagnostic center from doc169 into explicit authoring data while preserving the canonical T1 skeleton metadata and every recipe outside Stage49/50.

This step intentionally separates:
- diagnostic encounter evidence;
- authoring-candidate data;
- dynamic admission;
- production/numerical adoption.

Only the first two are completed here.

## 2. Candidate source

Overlay candidate:
`data/t1_stage49_50_stagger1800_authoring_candidate_v0_1.yaml`

Exact base:
`data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`

Base SHA256:
`3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf`

Candidate SHA256:
`c1bd5f45fb3cbdff6efa45b90f34e20bbc303a94d089564abf62523e15425bc3`

Materialized test artifact SHA256:
`de1b5944c560da9c0ea33f6e4dbc88bd898ee66f772a802274c96db4c711b33c`

## 3. Important authority correction applied during materialization

The final sustain diagnostic varies **Stage50 CLUSTER only**.

Canonical materialization therefore preserves:

```text
Stage49 CLUSTER
= distinct-grammar burst
= GRUNT / RUNNER / GRUNT / RUNNER / BRUTE / GRUNT
= offsets 0/120/240/360/480/600 ms within its phase

Stage50 CLUSTER
= DURABLE_CORE_3
= BRUTE / GRUNT / BRUTE / GRUNT / BRUTE / GRUNT
= offsets 0/360/720/1080/1440/1800 ms within its phase
```

Phase gap remains 5500 ms.

This avoids incorrectly projecting the Mage sustain modification onto Stage49.

## 4. Skeleton metadata preservation

A second materialization guard prevented diagnostic-probe metadata from drifting into authoring authority.

The diagnostic probe broadened some metadata for analysis, but the T1 skeleton/v0.2 authoring state remains authoritative.

Preserved exactly from v0.2:

```text
Stage49:
formation F08
formationSet [F08]
cadence CD05
complexity C2
pressureTags [RUSH, BULWARK]

Stage50:
formation F01
formationSet [F01,F02,F03,F08]
cadence CD03
complexity C3
pressureTags [BASELINE]
```

Only Stage49/50 spawn composition/geometry/chronology is changed.

## 5. Exact-source static run

Workflow:
`.github/workflows/timing-defense-t1-stage49-50-authoring-static-preflight.yml`

Exact run:

```text
run      40156618986
artifact 12585015454
head     4a06adbb523dd63e0a2a5fefb31fbb2553c0e4d1
artifact digest sha256 ac2d233af17dd0f5415169d7daec38bfc472c3409bfe626ea756d8e986bd1676
```

Source identity:

```text
preflight script sha256 4c3232eea8242f91a347b31b65b620906c17c786cd4738bc162f070905c2a9d6
candidate sha256        c1bd5f45fb3cbdff6efa45b90f34e20bbc303a94d089564abf62523e15425bc3
base recipe sha256      3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf
settlement bridge       1926ee88bed061bca76840446c73d0b33710915aaf9d19b238d9fd0c09505e4f
core                    fe7a2537215bed9448ad2ec24bab9693dd0901a7dc3431d3b955664ee6e08e7d
skills                  8fd4b29d99bfa7a25473d3e1c543a6769cbc0cd82ea85de25be0029d61f668a7
engine                  74806de62efa1f8494f1b34f39a839fab1f8127f2771b5b61c846b404c45d078
```

## 6. Static result

```text
status = PASS
errors = []
warnings = []
metadataPreservedFromV02 = true
productionGameplayChange = false
numericalFreeze = false
fullT1ExactRecipeFreeze = false
```

Stage49:

```text
authored = 24
max4s = 6
max6s = 11
minY = 0.18
maxY = 0.82
ySpread = 0.64
lastSpawn = 19750 ms
cluster = DISTINCT_GRAMMAR_BURST_0600
```

Stage50:

```text
authored = 30
max4s = 6
max6s = 9
minY = 0.18
maxY = 0.82
ySpread = 0.64
lastSpawn = 25250 ms
cluster = DURABLE_CORE_3_STAGGER_1800
```

## 7. Gates proven

PASS:
1. exact base identity;
2. candidate/schema parse;
3. only Stage49/50 override scope;
4. Stage5/18/41 unchanged;
5. all other recipe objects unchanged;
6. GRUNT/RUNNER/BRUTE only;
7. entryBaseX remains 0.92;
8. no midfield-spawn field introduced;
9. authored 4-second density <= 8;
10. intended Stage49/50 counts;
11. intended Y envelope;
12. exact grammar order/5500ms phase structure;
13. Stage49 burst identity;
14. Stage50 D3/STAGGER1800 identity;
15. Stage49 C2 / Stage50 C3 and skeleton metadata preserved;
16. no scalar-bearing stage field introduced;
17. explicit non-production/non-freeze status.

## 8. Interpretation

This static PASS means the diagnostic center has been transferred into structurally legal authoring-candidate data without the two identified drift risks:
- Stage50-only sustain accidentally leaking into Stage49;
- probe-only metadata accidentally overriding skeleton authority.

It does **not** prove that the materialized authoring data dynamically reproduces doc169. That is the next bounded evidence unit.

## 9. Next boundary

Run a narrow exact-source Stage49-50 dynamic admission on the materialized candidate.

Required checks:
- materialized Stage49/50 spawn lists equal the intended diagnostic center;
- deterministic replay / lifecycle continuity remain PASS;
- same Lv31 OFF/ON pairing;
- Archer diagnostic width and Mage semantic fidelity bridge remain explicitly diagnostic;
- role-facing result remains directionally consistent with doc169;
- objective-pressure skew is not worsened by authoring materialization;
- no full T1 authoring or numerical freeze.
