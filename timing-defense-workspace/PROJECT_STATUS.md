# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Active architecture lane
Primary architecture: **Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch `timing-defense-cloudflare-do-poc`
- validated HEAD `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- health `0.42-cf.1`

Last fully closed checkpoint:
- **v0.42 CHARGER authoritative state-machine capability FULL PASS**
- branch `timing-defense-cloudflare-v042-charger-pass-20261022`
- HEAD `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- live validation run `39703741827`

Read first:
1. `NEXT_WORK.md`
2. `MONSTER_CAPABILITY_CONTRACT_V1.md`
3. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
4. `CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`
5. `CLOUDFLARE_V041_FLYER_CAPABILITY_PASS_2026-10-22.md`
6. `CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`
7. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

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
Exact checkpoint:
- branch `timing-defense-cloudflare-v042-charger-pass-20261022`
- HEAD `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- health `0.42-cf.1`
- live run `39703741827`

Closed semantics:
- authoritative `ADVANCE -> WINDUP -> CHARGE`
- non-constant-speed `xAt/materialize/wallAt`
- WINDUP stationary
- positive authoritative knockback during WINDUP interrupts and returns to ADVANCE
- provisional 900 ms re-arm after interrupt
- `nextDueAt()` includes state transitions/wall timing
- persisted phase/refAt/rearm state reconstructs after reconnect
- public phase/timing/speed metadata exposed
- Tank Lv6 knock, AI stage multiplier, reward/contribution and team-DEF wall damage retained
- late `advanceTo()` chronological replay explicitly validated.

Provisional CHARGER test anchors: HP380 / speed .060 / wall110 / knock .80 / armor1 / reward8 / windup650ms / charge .210 / trigger x .62 / re-arm900ms. **Not production frozen.**

Live evidence:
- foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER **10/10 PASS**
- CHARGER **17/17 PASS**
- root-loader PASS
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- **FINAL PASS**

No Samsung Browser smoke required: CHARGER is not yet placed in a visible authored encounter and final telegraph presentation is not part of this slice.

Exact report: `CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`

---

# Active next bounded work
**SPLITTER authoritative child-spawn kernel**, stage-number-independent.

Required focus:
- parent death creates exactly two children deterministically,
- children never split again,
- child IDs/order are deterministic,
- child movement/wall/damage identity must not fall back to GRUNT,
- simultaneous split deaths and Lv6/N3 multi-target mutation must remain deterministic,
- event/reconnect integrity retained,
- no legacy stage recipe enabled.

Important unresolved product semantic before production freeze:
- how the provisional SPLITTER reward budget is allocated between parent and children. Do not silently freeze this as production economy.

Following: SUPPORTER -> SIEGER.

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
