# Cloudflare v0.44 — SUPPORTER Capability PASS

Date: 2026-10-22 KST

## Exact checkpoint
- branch: `timing-defense-cloudflare-v044-supporter-pass-20261022`
- HEAD: `b2dc0269e144d9fa13ee490bba36ae93839f6a20`
- public health: `0.44-cf.1`
- live validation run: `39706896662`
- live validation job: `119588945997`

## Scope
Stage-number-independent SUPPORTER movement-speed aura capability. No production encounter recipe or production balance freeze.

Structural contract retained:
- movement speed only,
- no heal / armor / damage / wall-damage / knock-resistance buff,
- SUPPORTER does not buff itself,
- multiple SUPPORTER auras do not stack,
- server authoritative.

## Provisional capability-test anchors
- HP 280
- base speed `.055`
- wall damage 70
- knock resistance `.90`
- armor `1.00`
- reward 8
- aura radius `.18`
- aura speed multiplier `1.18`
- provisional sandbox geometry: authoritative normalized 2D Euclidean distance

These values/geometry remain **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN**.

## Authoritative movement model
No fixed gameplay tick was introduced.

- Persisted `supportAuraSources` defines active source IDs.
- Effective multiplier is boolean: zero sources => `1.00`; one-or-more => `1.18` provisional.
- At exact aura entry/exit/removal timestamp, the target is materialized with the old movement state through that timestamp, then the source set/multiplier changes.
- Static-Y pair crossings use deterministic relative-motion geometry.
- FLYER crossings use deterministic bracket + bisection root refinement; this locates an event boundary and does not tick-simulate movement.
- `nextDueAt()` includes aura crossings.
- SUPPORTER death/wall removal and target knockback reconcile topology immediately at the authoritative event timestamp.

## Cross-capability composition
- FLYER: aura changes X only; authoritative Y oscillator remains independent and participates in 2D distance.
- CHARGER: ADVANCE/CHARGE speeds compose with aura; WINDUP remains zero.
- SPLITTER: children are reconciled immediately at spawn timestamp.
- Overlapping SUPPORTER sources remain non-stacking.
- A SUPPORTER excludes its own source ID; another SUPPORTER can cover it under the literal V1 contract.

## Compatibility defect caught before live promotion
The first candidate implementation overrode `wallAt()` with current-segment prediction for every monster. SUPPORTER's own 17/17 tests passed, but the existing v0.42 CHARGER regression correctly failed `CHARGER_WALL_PREDICTION_CONTINUOUS`.

Classification: **architecture compatibility regression**, not a numerical/balance issue.

Fix:
- when no aura is active, non-SUPPORTER monsters delegate to the already-validated inherited `wallAt()` contract,
- current-segment wall prediction is used only for SUPPORTER or actually aura-modified motion,
- aura/phase boundary events remain scheduled in `nextDueAt()`.

No balance number changed.

## Candidate validation
Final candidate run:
- run `39706684846`
- job `119588252056`
- result SUCCESS

Deterministic diagnostics:
- foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER **10/10 PASS**
- CHARGER **17/17 PASS**
- SPLITTER **14/14 PASS**
- SUPPORTER **17/17 PASS**

Key SUPPORTER checks include:
- deterministic entry/exit crossing timestamps,
- position continuity,
- overlap non-stacking,
- self-exclusion,
- exact supporter-death/removal transition,
- knockback topology reconciliation,
- FLYER Y-driven crossing determinism,
- CHARGER phase composition,
- SPLITTER child immediate reconciliation,
- no poll-frequency drift before crossing,
- reconnect reconstruction,
- `nextDueAt()` crossing inclusion.

## Live validation
GitHub Actions run `39706896662` / job `119588945997` validated the exact public candidate.

PASS evidence:
- exact health `0.44-cf.1`
- foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER **10/10 PASS**
- CHARGER **17/17 PASS**
- SPLITTER **14/14 PASS**
- SUPPORTER **17/17 PASS**
- root-loader smoke PASS
- prior V038 full regression PASS
- N3 client PASS
- N3 4H stress PASS
- **FINAL PASS**

## Device-smoke decision
No Samsung Browser smoke is required because SUPPORTER is not yet inserted into a visible authored encounter and final aura presentation/VFX is out of this capability slice.

## Closure
v0.44 SUPPORTER authoritative dynamic movement-speed aura capability is **FULL PASS**.

Next bounded capability: **SIEGER authoritative standoff/repeated wall-attack kernel**.
