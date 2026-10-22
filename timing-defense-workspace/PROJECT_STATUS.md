# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Active architecture lane
Primary architecture: **Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch `timing-defense-cloudflare-do-poc`
- validated HEAD `d1bac2effbd866aa221d55829678f959bc099b82`
- health `0.43-cf.1`

Last fully closed checkpoint:
- **v0.43 SPLITTER authoritative child-spawn capability FULL PASS**
- branch `timing-defense-cloudflare-v043-splitter-pass-20261022`
- HEAD `d1bac2effbd866aa221d55829678f959bc099b82`
- live validation run `39705143877`
- live validation job `119583316125`

Read first:
1. `NEXT_WORK.md`
2. `MONSTER_CAPABILITY_CONTRACT_V1.md`
3. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
4. `CLOUDFLARE_V043_SPLITTER_CAPABILITY_PASS_2026-10-22.md`
5. `CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`
6. `CLOUDFLARE_V041_FLYER_CAPABILITY_PASS_2026-10-22.md`
7. `CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`
8. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

---

# Closed authoritative foundations

## v0.36
- EXP: NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28
- AI stage multiplier: `1 + (stage - 1) * 0.035`
- Lv6: Knight +12%; Rogue second dagger +55 ms at 55%; Tank +30% knock; Archer up to 2 strict-line hits at 52%; Mage up to 3 nearby hits at 50%.

## Stage 1–3
Existing Stage 1–3 content is retained as **regression fixture material**, not the final campaign specification.

## v0.38 event/multiplayer kernel
- 512 retained authoritative events
- per-WebSocket event cursor
- monotonic event-batch
- explicit event-gap
- resume/eventFloor suppression
- 3H / 4H / 2H+2AI / 3H+1AI, reconnect, READY/START, Team Shop/NEXT validated.

## v0.39 N3 — FULL PASS / FROZEN PRODUCT CONTRACT
- milestones 5 / 10 / 20 / 30 / every +10 thereafter
- raw-equivalent budgets 60 / 90 / 150 / 210
- Rogue 2/3/4/5; Knight 67/33; Tank 60/20/20; Archer 70/30 strict line; Mage 55/15/15/15
- no N3-generated EXP/charge/combo/ordinary crit/recursive skill/recursive N3
- normal armor / kill / kill coin / contribution
- frozen boss scalars retained
- generic N3 knockback NORMAL-equivalent; Tank identity retained.

---

# Campaign direction
Do **not** reconstruct legacy Stage 4 -> Stage 10 as the production campaign.

Production direction:
- approximately 50 stages,
- tier identities,
- S / E / X pressure grammar,
- 2/3/4-player composition scaling,
- re-authored monster combinations,
- deterministic simulation before production-number freeze.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN
Ordinary archetypes:
1. GRUNT — baseline/reference
2. RUNNER — sustained tempo
3. BRUTE — raw durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — authoritative Y/spatial geometry
6. CHARGER — telegraphed interruptible burst dash
7. SPLITTER — death -> exactly two non-recursive children
8. SUPPORTER — non-stacking movement-speed aura only
9. SIEGER — standoff + repeated telegraphed wall attack

Bosses are separate capability compositions.
No hard class lockouts. No manual target-selection requirement. Gameplay-relevant state is server authoritative.

Current executable coefficients for capability testing remain **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN** unless separately approved.

---

# Capability checkpoint chain

## Foundation — PASS
- branch `timing-defense-cloudflare-v040-monster-capability-foundation`
- HEAD `68882c2013d1d35aaedbf12e5725fde377795044`
- selftest **22/22 PASS**

## v0.40 SHIELD/common armor — FULL PASS
- branch `timing-defense-cloudflare-v040-shield-pass-20261022`
- HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`
- explicit pre-armor `rawDamage`, armor applied once per target, AI-before-armor, Lv6 raw-damage hardening, SHIELD own speed/size/knock/reward identity
- foundation 22/22, N3 57/57, SHIELD 11/11, browser/WebSocket FINAL PASS.

## v0.41 FLYER authoritative Y — FULL PASS
- branch `timing-defense-cloudflare-v041-flyer-pass-20261022`
- HEAD `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- health `0.41-cf.1`
- stable baseY/epoch phase; `yAt()` gameplay truth; materialize/knock/reconnect preserve phase; Lv6/N3 geometry uses moving Y; client legacy local oscillator suppressed in network mode
- foundation 22/22, N3 57/57, SHIELD 11/11, FLYER server 10/10, client 5/5, prior FINAL PASS.

## v0.42 CHARGER authoritative state machine — FULL PASS
- branch `timing-defense-cloudflare-v042-charger-pass-20261022`
- HEAD `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- health `0.42-cf.1`
- live run `39703741827`
- authoritative `ADVANCE -> WINDUP -> CHARGE`, state-aware X/wall timing, WINDUP knock interruption/re-arm, reconnect reconstruction and late-`advanceTo()` chronology validated
- foundation 22/22, N3 57/57, SHIELD 11/11, FLYER 10/10, CHARGER 17/17, prior FINAL PASS.

Exact report: `CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`

## v0.43 SPLITTER authoritative child-spawn kernel — FULL PASS
Exact checkpoint:
- branch `timing-defense-cloudflare-v043-splitter-pass-20261022`
- HEAD `d1bac2effbd866aa221d55829678f959bc099b82`
- health `0.43-cf.1`
- live run `39705143877`
- live job `119583316125`

Closed semantics:
- parent death creates exactly two authoritative children at the death timestamp
- child IDs/order use authoritative `nextMonsterId`
- deterministic Y offsets and shared package attribution
- children persist `canSplit=false`; no recursive splitting
- explicit parent/child movement, wall, size and knock metadata; no GRUNT fallback
- no extra immediate split event: existing damage event carries split metadata, preserving older hit/Lv6/N3 annotation ordering
- simultaneous parent deaths produce deterministic IDs/order
- children prevent premature stage clear
- Rogue N3 retarget after parent death and Tank N3 child knock metadata validated
- reconnect and monotonic event IDs validated.

Provisional sandbox values remain **not production frozen**. The executable reward split `parent4 + child2 + child2 = package8` is **test accounting only** and is not the production economy decision.

Live evidence:
- foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER **10/10 PASS**
- CHARGER **17/17 PASS**
- SPLITTER **14/14 PASS**
- root-loader PASS
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- **FINAL PASS**

No Samsung Browser smoke required: SPLITTER is not yet placed in a visible authored encounter and final split VFX is not part of this slice.

Exact report: `CLOUDFLARE_V043_SPLITTER_CAPABILITY_PASS_2026-10-22.md`

---

# Active next bounded work
**SUPPORTER authoritative dynamic movement-speed aura**, stage-number-independent.

Frozen structural behavior:
- nearby ordinary monsters receive a movement-speed multiplier while within aura range
- SUPPORTER does not buff itself
- multiple SUPPORTER auras do not stack
- V1 aura changes movement speed only; no heal, armor, damage, wall-damage or knock-resistance buff
- no manual target selection requirement
- no legacy stage recipe enabled.

Provisional capability-test anchors:
- HP 280
- base speed `.055`
- wall damage 70
- knock resistance `.90`
- armor `1.00`
- reward 8
- aura radius `.18`
- aura movement multiplier `1.18`

These are **NOT production balance frozen**.

Primary architectural risk:
- aura membership can change continuously as monsters move relative to one another, so simply evaluating `distance <= radius` at arbitrary snapshots can create timestamp drift and client/server disagreement.

Required pre-implementation audit:
1. define authoritative aura topology/crossing semantics,
2. ensure movement integration remains deterministic between event timestamps,
3. preserve CHARGER phase speed, FLYER Y geometry and SPLITTER child identity when aura applies,
4. avoid aura self-buff and aura stacking,
5. ensure supporter death/wall removal immediately changes affected movement from the exact authoritative timestamp,
6. include reconnect and `wallAt/nextDueAt` consistency tests.

Following: SIEGER.

After capability completion:
- remaining player-skill authority needed for calibration,
- approximately 50-stage tier/S-E-X authoring,
- large deterministic 2/3/4-player simulation,
- classify/report/discuss,
- explicit production numerical freeze.

# Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`

# Governance
No unapproved numerical change:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
