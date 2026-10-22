# Cloudflare v0.42 — CHARGER Capability PASS

Date: 2026-10-22 KST

## Exact checkpoint
- branch: `timing-defense-cloudflare-v042-charger-pass-20261022`
- HEAD: `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- public health: `0.42-cf.1`
- live validation run: `39703741827`
- live validation job: `119578761943`

## Scope
This slice implements the CHARGER as a stage-number-independent authoritative capability. It does **not** author or restore a legacy Stage 4–10 recipe, and it does not freeze production balance.

Provisional capability-test anchors only:
- HP 380
- ADVANCE speed `.060`
- wall damage 110
- knock resistance `.80`
- armor `1.00`
- reward 8
- WINDUP 650 ms
- CHARGE speed `.210`
- sandbox trigger x `.62`
- interrupt re-arm 900 ms

These coefficients remain **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN**.

## Closed authoritative behavior
State machine:
`ADVANCE -> WINDUP -> CHARGE -> wall/contact resolution`

Validated semantics:
- non-constant-speed X movement is authoritative,
- WINDUP is stationary,
- exact transition timestamps participate in `nextDueAt`,
- future wall time predicts trigger -> windup -> charge correctly,
- positive authoritative knockback during WINDUP cancels the pending charge,
- interrupt returns to ADVANCE and applies the provisional re-arm delay,
- CHARGE uses temporary burst speed distinct from RUNNER sustained speed,
- Tank Lv6 knockback identity is retained,
- AI stage multiplier, kill/reward/contribution and team DEF wall mitigation remain authoritative,
- persisted phase/refAt/rearm state reconstructs the same future movement after reconnect,
- public state exposes phase/timing/speed metadata for later telegraph presentation.

## Chronological replay hardening
A late `advanceTo()` regression test proves due events are replayed in timestamp order:
- CHARGER trigger at ~2000 ms,
- queued Rogue second dagger at 2050 ms interrupts WINDUP,
- re-arm completes and CHARGER re-enters WINDUP at 2950 ms.

This guards against an alarm waking late and incorrectly applying a later CHARGE transition before an earlier attack event.

## Candidate validation
Final candidate CI run:
- run `39703589461`
- job `119578264575`
- result: SUCCESS

Diagnostics:
- Monster Capability Foundation: **22/22 PASS**
- v0.39 N3: **57/57 PASS**
- v0.40 SHIELD: **11/11 PASS**
- v0.41 FLYER: **10/10 PASS**
- v0.42 CHARGER: **17/17 PASS**

Earlier candidate failures were validation-harness defects only:
- direct Node import could not resolve the Cloudflare Worker `cloudflare:` module,
- an HTTP-500 diagnostics body was initially hidden by `curl -f`,
- four self-test failures were strict floating-point equality / one missing test argument.
No production numerical patch was made in response to those harness failures.

## Live validation
GitHub Actions run `39703741827` validated the exact deployed candidate.

PASS evidence:
- exact deployment marker `0.42-cf.1`
- foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER **10/10 PASS**
- CHARGER **17/17 PASS**
- root-loader smoke PASS
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- **FINAL PASS**

## Device-smoke decision
No Samsung Browser smoke is required for this slice because CHARGER is not yet inserted into a visible authored encounter and no final telegraph presentation was introduced. Device presentation/readability validation is deferred until a visible CHARGER sandbox or production encounter exists.

## Closure
v0.42 CHARGER authoritative state-machine capability is **FULL PASS**.

Next bounded capability:
**SPLITTER child-spawn kernel**, still stage-number-independent.

Do not interpret v0.42 provisional CHARGER values as final approximately-50-stage campaign balance.
