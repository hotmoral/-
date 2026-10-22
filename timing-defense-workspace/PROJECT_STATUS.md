# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Current validated deployment
Primary architecture: **Cloudflare Workers + Durable Objects event-driven multiplayer**.

- public: `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- validated HEAD: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health: `0.45-cf.1`
- last closed checkpoint: **v0.45 SIEGER authoritative standoff/repeated wall-attack FULL PASS**
- checkpoint branch: `timing-defense-cloudflare-v045-sieger-pass-20261022`
- live validation run/job: `39725993894` / `119649887564`

Read first:
1. `NEXT_WORK.md`
2. `MONSTER_CAPABILITY_CONTRACT_V1.md`
3. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
4. `CLOUDFLARE_V045_SIEGER_CAPABILITY_PASS_2026-10-22.md`
5. `CLOUDFLARE_V044_SUPPORTER_CAPABILITY_PASS_2026-10-22.md`
6. `CLOUDFLARE_V043_SPLITTER_CAPABILITY_PASS_2026-10-22.md`
7. `CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`
8. `CLOUDFLARE_V041_FLYER_CAPABILITY_PASS_2026-10-22.md`
9. `CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`
10. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

---

# Frozen/closed combat foundations

## v0.36
- EXP: NORMAL8 / GOOD12 / PERFECT18 / HEAVY10 / HEAVY+14 / GREAT18 / SUPER23 / CRITICAL28
- AI stage multiplier: `1 + (stage - 1) * 0.035`
- Lv6: Knight +12%; Rogue second dagger +55ms at55%; Tank +30% knock; Archer up to2 strict-line52%; Mage up to3 nearby50%.

## v0.38 event/multiplayer kernel
- 512 retained authoritative events
- per-WebSocket cursor / monotonic event-batch / explicit event-gap
- resume/eventFloor suppression
- 3H / 4H / 2H+2AI / 3H+1AI, reconnect, READY/START, Team Shop/NEXT validated.

## v0.39 N3 — FROZEN PRODUCT CONTRACT
- milestones 5 / 10 / 20 / 30 / every +10 thereafter
- raw-equivalent budgets 60 / 90 / 150 / 210
- Rogue2/3/4/5; Knight67/33; Tank60/20/20; Archer70/30 strict line; Mage55/15/15/15
- no generated EXP/charge/combo/ordinary crit/recursive skill/recursive N3
- normal armor / kill / kill coin / contribution
- frozen boss scalars retained
- generic N3 knockback NORMAL-equivalent; Tank identity retained.

Stage 1–3 remain **regression fixtures**, not final campaign encounter commitments.

---

# Campaign direction
Do **not** reconstruct legacy Stage 4 -> Stage 10 as production campaign content.

Production direction remains approximately 50 stages with:
- tier identities,
- S / E / X pressure grammar,
- 2/3/4-player composition scaling,
- re-authored monster combinations,
- deterministic simulation/calibration before explicit production-number freeze.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN
Ordinary roster:
1. GRUNT — baseline/reference
2. RUNNER — sustained tempo
3. BRUTE — raw durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — authoritative Y/spatial geometry
6. CHARGER — telegraphed interruptible burst dash
7. SPLITTER — death -> exactly two non-recursive children
8. SUPPORTER — non-stacking movement-speed aura only
9. SIEGER — standoff + repeated telegraphed wall attack

Bosses are separate capability compositions. No hard class lockouts. No manual target-selection requirement. Gameplay-relevant state is server authoritative.

Current executable capability coefficients are **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN** unless separately approved.

---

# Capability checkpoint chain

## Foundation — PASS
- `timing-defense-cloudflare-v040-monster-capability-foundation`
- HEAD `68882c2013d1d35aaedbf12e5725fde377795044`
- **22/22 PASS**

## v0.40 SHIELD — FULL PASS
- checkpoint `timing-defense-cloudflare-v040-shield-pass-20261022`
- HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`
- common single-application armor path / explicit rawDamage / own speed-size-knock-reward identity.

## v0.41 FLYER — FULL PASS
- checkpoint `timing-defense-cloudflare-v041-flyer-pass-20261022`
- HEAD `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- authoritative baseY/epoch and `yAt()`; materialize/knock/reconnect preserve phase; Lv6/N3 use moving Y; client local oscillator suppressed.

## v0.42 CHARGER — FULL PASS
- checkpoint `timing-defense-cloudflare-v042-charger-pass-20261022`
- HEAD `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- authoritative `ADVANCE -> WINDUP -> CHARGE`, exact due timing, WINDUP knock interruption/re-arm, reconnect and chronological replay validated.

## v0.43 SPLITTER — FULL PASS
- checkpoint `timing-defense-cloudflare-v043-splitter-pass-20261022`
- HEAD `d1bac2effbd866aa221d55829678f959bc099b82`
- exact two-child deterministic spawn; child `canSplit=false`; explicit parent/child identity; shared package attribution; N3 retarget; reconnect/event monotonicity.
- provisional reward accounting `4 + 2 + 2 = 8` is test accounting only, **not production economy freeze**.

## v0.44 SUPPORTER — FULL PASS
- checkpoint `timing-defense-cloudflare-v044-supporter-pass-20261022`
- HEAD `b2dc0269e144d9fa13ee490bba36ae93839f6a20`
- authoritative movement-speed aura only; self excluded; non-stacking; exact event-driven topology crossings; FLYER/CHARGER/SPLITTER composition; reconnect/nextDueAt validated.
- provisional HP280 / speed.055 / wall70 / knock.90 / reward8 / radius.18 / speed×1.18 and Euclidean sandbox geometry remain **not production frozen**.

## v0.45 SIEGER — FULL PASS
Exact checkpoint:
- branch `timing-defense-cloudflare-v045-sieger-pass-20261022`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`
- live run/job `39725993894` / `119649887564`

Closed semantics:
- authoritative standoff arrival
- persistent phases `ADVANCE / WINDUP / COOLDOWN`; FIRE is instantaneous event
- repeated ranged wall shots while SIEGER remains alive
- team DEF applies to siege wall damage
- WINDUP/COOLDOWN knockback can force reposition and fresh windup
- SUPPORTER affects approach only, not siege cadence/damage
- no ordinary direct-contact wall resolution while correctly sieging
- surviving SIEGER blocks premature stage clear
- reconnect / late-advance chronology / event monotonicity validated
- public phase metadata supports reconstruction.

Provisional test anchors: HP520 / speed.045 / knock.55 / armor1 / reward11 / standoffX.38 / windup800ms / shot75 / repeat2200ms. **Not production frozen.**

Live evidence:
- foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER **10/10 PASS**
- CHARGER **17/17 PASS**
- SPLITTER **14/14 PASS**
- SUPPORTER **17/17 PASS**
- SIEGER **20/20 PASS**
- exact deployment marker PASS
- root-loader PASS
- prior browser/WebSocket full regression PASS
- live validation job SUCCESS.

First live gate failure was only an outdated workflow expectation of 18 SIEGER checks while the final suite contained 20; gameplay diagnostics were already 20/20. Gate expectation was corrected with **no gameplay or numerical change**, then the full live gate passed.

No Samsung Browser smoke required because no visible authored SIEGER encounter/final telegraph presentation was introduced.

Exact report: `CLOUDFLARE_V045_SIEGER_CAPABILITY_PASS_2026-10-22.md`

---

# Monster Capability V1 milestone — ALL NINE ORDINARY ARCHETYPES MECHANICALLY CLOSED
The server-authoritative mechanical foundation now covers all nine ordinary archetypes. This closes the Monster Capability Layer implementation sequence started after v0.39.

This does **not** freeze final HP/speed/damage/reward/timing values and does **not** define final 50-stage encounter recipes.

---

# Active next bounded work — remaining player-skill authority review
Before approximately-50-stage authoring/calibration, recover the remaining player-skill progression contracts from live repository/canonical/legacy source.

Do not invent new values.

Required classification:
1. already frozen + authoritative,
2. designed/planned but not yet authoritative,
3. legacy/provisional behavior that needs explicit re-approval,
4. unresolved design choices requiring discussion before implementation.

Search/recover especially any post-Lv6 progression such as Lv11 / Lv16 / Lv21 and class-specific growth/skill contracts, then report the exact calibration blockers before coding.

After player-skill authority needed for calibration is resolved:
1. build the approximately-50-stage tier / S-E-X authoring model,
2. generate 2/3/4-player candidate recipes,
3. run large deterministic simulation,
4. classify pressure/density/role issues,
5. report/discuss before numerical patches,
6. explicitly freeze production monster/stage values.

# Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`

# Governance
No unapproved numerical change:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
