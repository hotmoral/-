# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Current validated deployment
Primary architecture: **Cloudflare Workers + Durable Objects event-driven multiplayer**.

- public: `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- validated HEAD: `b2dc0269e144d9fa13ee490bba36ae93839f6a20`
- health: `0.44-cf.1`
- last closed checkpoint: **v0.44 SUPPORTER authoritative dynamic movement-speed aura FULL PASS**
- checkpoint branch: `timing-defense-cloudflare-v044-supporter-pass-20261022`
- live validation run/job: `39706896662` / `119588945997`

Read first:
1. `NEXT_WORK.md`
2. `MONSTER_CAPABILITY_CONTRACT_V1.md`
3. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
4. `CLOUDFLARE_V044_SUPPORTER_CAPABILITY_PASS_2026-10-22.md`
5. `CLOUDFLARE_V043_SPLITTER_CAPABILITY_PASS_2026-10-22.md`
6. `CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`
7. `CLOUDFLARE_V041_FLYER_CAPABILITY_PASS_2026-10-22.md`
8. `CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`
9. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

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
Exact checkpoint:
- branch `timing-defense-cloudflare-v044-supporter-pass-20261022`
- HEAD `b2dc0269e144d9fa13ee490bba36ae93839f6a20`
- health `0.44-cf.1`
- live run/job `39706896662` / `119588945997`

Closed semantics:
- authoritative movement-speed aura only
- no self-buff
- multiple sources non-stacking
- persisted source-ID membership
- exact materialize-before-membership-change transition
- no fixed gameplay tick
- static-Y boundary solved deterministically; FLYER boundary found by deterministic root refinement
- supporter death/wall removal/knock changes topology at exact authoritative timestamp
- FLYER aura affects X only
- CHARGER ADVANCE/CHARGE compose with aura; WINDUP remains zero
- SPLITTER children reconcile immediately at spawn
- reconnect and `nextDueAt()` crossing semantics validated.

Provisional test anchors: HP280 / speed.055 / wall70 / knock.90 / armor1 / reward8 / radius.18 / speed×1.18; sandbox distance geometry is authoritative normalized 2D Euclidean. **Not production frozen.**

Compatibility regression caught pre-live:
- first implementation weakened no-aura CHARGER full `wallAt()` prediction.
- fixed by delegating inherited `wallAt()` whenever aura is inactive; no numerical change.

Live evidence:
- foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER **10/10 PASS**
- CHARGER **17/17 PASS**
- SPLITTER **14/14 PASS**
- SUPPORTER **17/17 PASS**
- root-loader PASS
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- **FINAL PASS**

No Samsung Browser smoke required because no visible authored SUPPORTER encounter/aura VFX was introduced.

Exact report: `CLOUDFLARE_V044_SUPPORTER_CAPABILITY_PASS_2026-10-22.md`
Preflight: `SUPPORTER_AURA_AUTHORITY_PREFLIGHT_2026-10-22.md`

---

# Active next bounded work
**SIEGER authoritative standoff + repeated ranged wall-attack kernel**, stage-number-independent.

Frozen structural behavior:
- approach normally,
- stop at standoff distance,
- telegraphed windup,
- authoritative repeated wall attacks,
- knockback can force reposition before resuming siege cycle,
- no legacy stage recipe enabled.

Provisional capability-test anchors:
- HP520 / approach speed `.045` / knock `.55` / armor1 / reward11
- standoff X `.38`
- windup 800ms
- ranged wall shot 75
- repeat interval 2200ms

These are **NOT production balance frozen**.

Required preflight:
1. exact arrival-at-standoff timestamp and phase transitions,
2. explicit `ADVANCE -> WINDUP -> FIRE/COOLDOWN -> WINDUP` repeated cycle,
3. team-DEF interaction for siege wall shots,
4. knockback/reposition semantics during windup/cooldown,
5. SUPPORTER aura affects approach speed only, not shot cadence/damage,
6. `nextDueAt()` and reconnect chronology,
7. repeated wall event representation without removing the SIEGER,
8. prior capability regressions remain PASS.

After SIEGER closes, all nine ordinary capability archetypes have a server-authoritative foundation; then review remaining player-skill authority needed for calibration before the real approximately-50-stage authoring/simulation phase.

# Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`

# Governance
No unapproved numerical change:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
