# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Current architecture
Primary lane:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- current validated HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`
- health `0.40-cf.2`

Last fully closed checkpoint:
- **v0.40 SHIELD/common armor capability FULL PASS**
- branch `timing-defense-cloudflare-v040-shield-pass-20261022`
- HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `MONSTER_CAPABILITY_CONTRACT_V1.md`
5. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
6. `CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`
7. `MONSTER_CAPABILITY_FOUNDATION_PASS_2026-10-22.md`
8. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

---

# Closed authoritative foundations

## v0.36
N1 exact EXP:
- NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28

N2 exact AI stage multiplier:
`1 + (stage - 1) * 0.035`

Lv6 authority:
- Knight +12% damage
- Rogue 55% second dagger after +55 ms
- Tank +30% knockback
- Archer up to two strict-line 52% secondary hits
- Mage up to three nearby 50% splash hits

## v0.38 event/multiplayer kernel
- 512 retained authoritative events
- per-WebSocket event cursor
- monotonic event-batch
- explicit event-gap
- resume/eventFloor replay suppression
- 3H / 4H / 2H+2AI / 3H+1AI coverage
- host reconnect / READY / START / Team Shop / NEXT coverage

## v0.39 N3
Frozen:
- combo 5 / 10 / 20 / 30 / every +10
- budgets 60 / 90 / 150 / 210
- Rogue 2/3/4/5 daggers
- Knight 67/33
- Tank 60/20/20
- Archer 70/30 strict line
- Mage 55/15/15/15
- no N3-generated EXP / charge / combo / ordinary crit / recursive skill / recursive N3
- normal armor / kill / kill coin / contribution
- boss scalars retained
- NORMAL-equivalent generic N3 knockback

v0.39 automation and Samsung Browser N3 smoke PASS.

---

# Campaign direction correction

Do **not** continue legacy Stage 4 -> Stage 10 reconstruction as the production campaign.

The intended campaign is approximately 50 stages with:
- tier identities,
- S / E / X pressure grammar,
- 2/3/4-player composition scaling,
- re-authored monster combinations,
- deterministic simulation/calibration before production number freeze.

Stage 1–3 remain regression fixtures for the current combat/network kernel only.

The old branch `timing-defense-cloudflare-v040-stage4-shield` is preflight-only and must not be resumed as production direction without a new explicit decision.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN

Ordinary roster:
1. GRUNT — baseline/reference
2. RUNNER — sustained tempo
3. BRUTE — raw durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — authoritative Y/spatial geometry
6. CHARGER — telegraphed interruptible burst dash
7. SPLITTER — parent death creates exactly two non-recursive children
8. SUPPORTER — non-stacking nearby movement-speed aura only
9. SIEGER — standoff + repeated telegraphed wall attacks

Bosses are separate capability compositions.

Global constraints:
- no hard class lockouts,
- no manual target selection smuggled in as a monster feature,
- gameplay state server-authoritative,
- exceptional actions telegraphed,
- SPLITTER children never split,
- SUPPORTER V1 aura speed-only and non-stacking,
- production coefficients not frozen.

Provisional executable values live in `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md` and are explicitly NOT production balance commitments.

---

# Monster Capability Foundation — PASS

Branch:
`timing-defense-cloudflare-v040-monster-capability-foundation`

Validated HEAD:
`68882c2013d1d35aaedbf12e5725fde377795044`

Foundation CI:
**22/22 PASS**.

---

# v0.40 SHIELD/common armor — FULL PASS

Exact checkpoint:
- branch `timing-defense-cloudflare-v040-shield-pass-20261022`
- HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`
- health `0.40-cf.2`
- live validation run `39696308376`

Authoritative behavior:
- SHIELD speed/wall timing uses SHIELD metadata rather than GRUNT fallback,
- common server damage path applies SHIELD armor once,
- events expose pre-armor `rawDamage` and post-armor `damage`,
- AI stage scaling occurs before armor,
- human / passive / AI / Lv6 / N3 all respect the same armor policy,
- SHIELD size `1.08` and knock resistance `.62` are used by Lv6/N3 geometry/knock paths,
- kill / coin / killCoinEarned / contribution remain authoritative.

Armor compatibility hardening:
- Lv6 secondary damage now derives from the primary event's pre-armor `rawDamage`, then each actual target applies its own armor exactly once.
- prevents SHIELD double-armor while leaving armor=1 legacy outcomes unchanged.

Validation:
- capability foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- FINAL PASS

Intermediate validation incidents were test/deployment-gate defects, not gameplay regressions:
- combo5 primary correctly includes existing +5% persistent combo bonus,
- live gate now requires a unique deployment marker (`0.40-cf.2`) before diagnostics to avoid stale-deployment acceptance.

No Samsung Browser smoke was needed because SHIELD was not added to a visible public encounter.

---

# Active next boundary — FLYER authoritative Y geometry

This is stage-number-independent capability work, **not legacy Stage 5/6 implementation**.

Required work:
- audit current monster code for X-only assumptions,
- define authoritative FLYER Y position/state semantics,
- ensure server targeting / Archer strict-line / Mage AoE consume the same Y truth,
- ensure reconnect/state reconstruction produces the same Y without phase jump,
- preserve normal/passive/AI/Lv6/N3 attribution,
- do not introduce ground immunity,
- do not enable a legacy encounter recipe,
- keep FLYER values provisional until final 50-stage calibration.

Validation:
`deterministic Y/geometry tests -> v0.40/v0.39 regression -> GitHub Actions live Chromium/WebSocket -> only necessary device visual smoke`

Following capability order:
CHARGER -> SPLITTER -> SUPPORTER -> SIEGER.

After capability completion:
1. remaining player-skill authority needed for calibration,
2. approximately 50-stage tier/S-E-X authoring model,
3. large deterministic 2/3/4-player simulation,
4. classify/report/discuss,
5. explicit production numerical freeze.

## AI FILL semantic
Configured AI filler positions remain fixed occupied positions. Humans do not dynamically displace them.

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred as one shared responsive layer.

## Validation policy
Automatable validation must not be delegated to the user unless CI cannot execute it.

## Governance
No numerical change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
