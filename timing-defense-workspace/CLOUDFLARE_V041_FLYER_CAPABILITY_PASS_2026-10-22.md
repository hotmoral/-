# Timing Defense — Cloudflare v0.41 FLYER Capability PASS

Date: 2026-10-22 KST
Status: **FULL PASS — CAPABILITY ONLY / NO LEGACY STAGE 5–6 AUTHORING**

## Exact checkpoint
- pass branch: `timing-defense-cloudflare-v041-flyer-pass-20261022`
- validated/live HEAD: `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- watched branch: `timing-defense-cloudflare-do-poc`
- health: `0.41-cf.1`
- live validation run: `39697563460`
- evidence artifact: `12391810817`

## Scope
Stage-number-independent FLYER authoritative-Y capability only.

Explicitly not included:
- legacy Stage 5/6 encounter reconstruction,
- final 50-stage FLYER placement/frequency,
- ground immunity,
- production balance freeze,
- new art/readability pass.

Current FLYER coefficients are executable provisional/reference anchors only:
- HP 225
- X speed `.100`
- size `.78`
- wall damage 70
- knock resistance `.90`
- armor `1.00`
- reward 7
- Y amplitude `.020`
- Y angular frequency `5 rad/s`

## Authoritative Y model
FLYER now has one stable server-owned phase definition:
- `flyerBaseY`
- `flyerEpochAt`
- `yAt(monster, at) = baseY + sin((at - epoch)/1000 * omega) * amplitude`

Materialization/knockback may change X reference state but does not reset the Y phase.
Public snapshots expose current Y plus base/epoch/amplitude/frequency metadata so reconnect and presentation can reconstruct the same phase.

## Geometry integration
Lv6 and N3 geometry now consume `room.yAt(monster, at)` when available.
This closes the prior static-`monster.y` assumption for:
- Archer strict-line secondary targeting,
- Mage AoE secondary targeting,
- Archer N3 line targeting.

FLYER also uses its own size `.78` and knock resistance `.90`, rather than GRUNT fallback.

## Client hardening
Existing network rendering already consumed server snapshot Y, but legacy `baseUpdate()` also ran its own local `type==='flyer'` sine oscillator. That would double-apply Y movement once FLYER became network-authoritative.

v0.41 client behavior:
- receives authoritative phase metadata,
- presentation-only extrapolates the same phase between snapshots,
- temporarily aliases network FLYER to `flyer_net` during inherited update so the legacy local oscillator does not run,
- restores `type='flyer'` before rendering.

No client-side gameplay/Y authority is introduced.

## Deterministic validation
FLYER server selftest: **10/10 PASS**
- deterministic base/peak/trough Y
- materialize preserves phase
- public snapshot phase metadata
- FLYER combat/reward identity
- Tank Lv6 knock resistance
- Lv6 Archer uses authoritative dynamic Y
- Lv6 Mage uses authoritative dynamic Y
- Archer N3 uses authoritative dynamic Y
- reconnect reconstruction preserves phase
- non-FLYER Y unchanged

Important geometry boundary tests proved that dynamic Y changes outcomes compared with static base Y:
- Archer case: authoritative moving positions produce a valid straight-line secondary where static base positions would miss.
- Mage case: authoritative moving positions correctly exclude a target that static base positions would incorrectly include.

## Browser/client validation
FLYER client authority selftest: **5/5 PASS**
- API present
- same server/client phase formula
- legacy local oscillator suppressed
- monster type restored after inherited update
- authoritative target Y extrapolated between snapshots

Root loader also confirmed `window.__TDFlyerYV041` is present in the deployed game.

## Full live regression
On exact `0.41-cf.1` deployment:
- Monster Capability Foundation **22/22 PASS**
- v0.39 N3 **57/57 PASS**
- v0.40 SHIELD **11/11 PASS**
- v0.41 FLYER **10/10 PASS**
- FLYER client authority **5/5 PASS**
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- **FINAL PASS**

## Device smoke decision
No Samsung Browser smoke is required for this slice because no FLYER is currently placed into a public authored encounter. Visual/readability validation belongs to a later capability sandbox/encounter presentation gate.

## Next bounded work
**CHARGER authoritative state machine**, stage-number-independent.

Required capability shape remains:
`ADVANCE -> WINDUP -> CHARGE -> wall/contact resolution`, with authoritative positive knockback during WINDUP cancelling the pending charge and applying a provisional re-arm delay for sandbox testing.

Do not resume legacy Stage 4 -> Stage 10 reconstruction.
