# Timing Defense — Cloudflare v0.40 SHIELD Capability PASS

Date: 2026-10-22 KST
Status: **FULL PASS — CAPABILITY ONLY / NO LEGACY STAGE 4 AUTHORING**

## Exact checkpoint
- pass branch: `timing-defense-cloudflare-v040-shield-pass-20261022`
- validated/live HEAD: `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`
- watched branch: `timing-defense-cloudflare-do-poc`
- health: `0.40-cf.2`
- live validation run: `39696308376`

## Scope
Stage-number-independent SHIELD/common-armor capability only.

Explicitly **not** included:
- legacy Stage 4 encounter reconstruction,
- final 50-stage SHIELD placement/frequency,
- production balance freeze for SHIELD coefficients,
- new visual-art pass.

The current `.72` armor / `.62` knock resistance / `1.08` size / `.057` speed / reward `10` are executable provisional/reference anchors for capability validation. Final production calibration remains deferred.

## Authoritative integration
- SHIELD movement/wall timing uses its own speed instead of GRUNT fallback.
- SHIELD damage resolution applies armor once in the authoritative server path.
- event carries both pre-armor `rawDamage` and post-armor `damage`.
- AI stage multiplier is applied before armor.
- passive, human, AI, Lv6 secondary and N3 all route through the same SHIELD armor policy.
- kill / coin / killCoinEarned / contribution attribution remains authoritative.
- Lv6 and N3 geometry/knock metadata includes SHIELD size `1.08` and knock resistance `.62` rather than GRUNT fallback.

## Important compatibility hardening
The introduction of armor exposed a pre-existing assumption in Lv6 secondary calculation: secondary damage had been derived from the primary event's actual damage. With armor=1 this was harmless; on SHIELD it would cause the primary armor reduction to be inherited and then armor to be applied again to the secondary target.

The authoritative path now exposes `rawDamage` and Lv6 secondary calculations derive from pre-armor raw damage before each target applies its own armor exactly once.

This does not change prior armor=1 Stage 1–3 outcomes.

## Validation evidence
Candidate CI:
- syntax checks PASS
- pure capability foundation PASS
- Wrangler worker bundle dry-run PASS

Live diagnostics on exact cf.2 deployment:
- Monster Capability Foundation: **22/22 PASS**
- v0.39 N3 regression: **57/57 PASS**
- v0.40 SHIELD authority: **11/11 PASS**

SHIELD-specific checks include:
- 100 raw -> 72 actual
- minimum damage 1
- AI Stage 3 multiplier before armor: 100 -> 107 -> 77
- passive 40 -> 29
- kill/reward/contribution
- Tank Lv6 knock resistance semantics
- N3 raw budget remains pre-armor
- Lv6 Archer secondary derives from raw primary damage, preventing double armor
- Archer/N3 geometry uses size 1.08
- authoritative movement speed .057
- non-SHIELD delegation regression

Live Playwright/WebSocket regression:
- V038 FULL REGRESSION PASS
- N3 SERVER 57/57 PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- **FINAL PASS**

## Validation incident classification
Two failed intermediate live runs did not reveal gameplay regressions:
1. first failure: self-test incorrectly expected a 5-combo PERFECT primary to remain 200 raw; existing +5% combo bonus correctly made it 210 raw before armor.
2. second failure: deployment marker remained `0.40-cf.1`, so CI accepted the previous deployment before the corrected test reached Cloudflare.

Resolution:
- test expectation corrected to existing combo semantics,
- exact deployment marker advanced to `0.40-cf.2`,
- live validation now waits for the exact marker before diagnostics.

## Device smoke decision
No Samsung Browser smoke is required for this slice because SHIELD was not inserted into a public stage/encounter and no new player-visible presentation was introduced. A visual/readability smoke belongs to a later capability sandbox/encounter presentation gate.

## Next bounded work
**FLYER / authoritative Y geometry**, stage-number-independent.

Do not resume legacy Stage 4 -> Stage 10 reconstruction.
