# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Current architecture
Primary lane: **Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- current validated HEAD `d1bac2effbd866aa221d55829678f959bc099b82`
- health `0.43-cf.1`

Last fully closed checkpoint:
- **v0.43 SPLITTER authoritative child-spawn capability FULL PASS**
- branch `timing-defense-cloudflare-v043-splitter-pass-20261022`
- HEAD `d1bac2effbd866aa221d55829678f959bc099b82`
- live validation run `39705143877`
- live validation job `119583316125`

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `MONSTER_CAPABILITY_CONTRACT_V1.md`
5. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
6. `CLOUDFLARE_V043_SPLITTER_CAPABILITY_PASS_2026-10-22.md`
7. `CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`
8. `CLOUDFLARE_V041_FLYER_CAPABILITY_PASS_2026-10-22.md`
9. `CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`
10. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

---

# Frozen/closed combat foundations

## v0.36
- exact EXP: NORMAL8 / GOOD12 / PERFECT18 / HEAVY10 / HEAVY+14 / GREAT18 / SUPER23 / CRITICAL28
- AI stage multiplier: `1 + (stage - 1) * 0.035`
- Lv6: Knight +12%; Rogue +55 ms second dagger at55%; Tank +30% knock; Archer up to2 strict-line52%; Mage up to3 nearby50%.

## v0.38 event/multiplayer kernel
- 512 retained events
- per-WebSocket event cursor
- monotonic event-batch
- explicit event-gap
- resume/eventFloor replay suppression
- 3H / 4H / 2H+2AI / 3H+1AI
- host reconnect / READY / START / Team Shop / NEXT validated.

## v0.39 N3 — FROZEN
- milestones 5 / 10 / 20 / 30 / every +10
- budgets 60 / 90 / 150 / 210
- Rogue 2/3/4/5; Knight67/33; Tank60/20/20; Archer70/30 strict line; Mage55/15/15/15
- no generated EXP/charge/combo/ordinary crit/recursive skill/recursive N3
- normal armor / kill / kill coin / contribution
- boss scalars retained
- NORMAL-equivalent generic N3 knockback.

---

# Campaign direction
Do **not** resume legacy Stage 4 -> Stage 10 reconstruction as the production campaign.

Production direction:
- approximately 50 stages
- tier identities
- S / E / X pressure grammar
- 2/3/4-player composition scaling
- re-authored monster combinations
- deterministic simulation/calibration before production-number freeze.

Stage 1–3 remain regression fixtures only.
Old branch `timing-defense-cloudflare-v040-stage4-shield` remains preflight-only.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN
Nine ordinary archetypes:
1. GRUNT — baseline
2. RUNNER — sustained tempo
3. BRUTE — durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — authoritative Y geometry
6. CHARGER — telegraphed interruptible burst dash
7. SPLITTER — parent death -> exactly two non-recursive children
8. SUPPORTER — non-stacking movement-speed aura only
9. SIEGER — standoff + repeated telegraphed wall attack

Bosses are separate capability compositions.
No hard class lockouts. No manual target-selection requirement. Relevant gameplay state is server authoritative.
Current capability coefficients remain **PROVISIONAL** unless separately frozen.

---

# Capability checkpoint chain

## Foundation
- branch `timing-defense-cloudflare-v040-monster-capability-foundation`
- HEAD `68882c2013d1d35aaedbf12e5725fde377795044`
- **22/22 PASS**

## v0.40 SHIELD — FULL PASS
- branch `timing-defense-cloudflare-v040-shield-pass-20261022`
- HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`
- common armor/rawDamage path and SHIELD identity validated.

## v0.41 FLYER — FULL PASS
- branch `timing-defense-cloudflare-v041-flyer-pass-20261022`
- HEAD `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- health `0.41-cf.1`
- authoritative Y phase, moving-Y Lv6/N3 geometry and network presentation contract validated.

## v0.42 CHARGER — FULL PASS
- branch `timing-defense-cloudflare-v042-charger-pass-20261022`
- HEAD `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- health `0.42-cf.1`
- authoritative `ADVANCE -> WINDUP -> CHARGE`, interrupt/re-arm, state-aware movement/wall/reconnect and chronological replay validated.

## v0.43 SPLITTER — FULL PASS
- branch `timing-defense-cloudflare-v043-splitter-pass-20261022`
- HEAD `d1bac2effbd866aa221d55829678f959bc099b82`
- health `0.43-cf.1`
- live run `39705143877`
- live job `119583316125`
- report `CLOUDFLARE_V043_SPLITTER_CAPABILITY_PASS_2026-10-22.md`

Authoritative semantics:
- parent death creates exactly two deterministic children at death timestamp
- authoritative child IDs/order and fixed Y offsets
- children persist `canSplit=false` and never recursively split
- parent and children share a package attribution ID
- explicit parent/child movement, wall, size and knock identity
- no extra immediate split event; split metadata rides on the damage event to preserve earlier annotation ordering
- simultaneous splits deterministic
- spawned children prevent premature stage clear
- Rogue N3 parent-kill -> deterministic child retarget validated
- Tank N3 child knock metadata validated
- reconnect and event-ID monotonicity validated.

Provisional sandbox accounting currently uses parent4 + child2 + child2 = total8. **This is test accounting only and is NOT the production reward/economy freeze.**

Validation evidence:
- foundation **22/22**
- N3 **57/57**
- SHIELD **11/11**
- FLYER **10/10**
- CHARGER **17/17**
- SPLITTER **14/14**
- root-loader PASS
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- **FINAL PASS**

No Samsung Browser smoke: SPLITTER has no visible authored encounter/final split VFX yet.

---

# Active next boundary — SUPPORTER authoritative dynamic movement-speed aura
Stage-number-independent capability work; not a legacy stage implementation.

Frozen V1 structure:
- aura modifies nearby monster **movement speed only**
- SUPPORTER never buffs itself
- multiple SUPPORTER auras do not stack
- no heal / armor / damage / wall-damage / knock-resistance buff
- no manual target-selection requirement
- no legacy stage recipe enabled.

Provisional sandbox anchors:
- HP280 / speed `.055` / wall70 / knock `.90` / armor1 / reward8
- aura radius `.18`
- aura speed multiplier `1.18`

These are **not production frozen**.

Critical architecture risk:
aura membership changes continuously as monsters move relative to one another. A naive snapshot/tick check can make movement depend on poll frequency and create authoritative timestamp drift.

Required before live implementation:
1. define exact enter/leave crossing semantics,
2. integrate movement deterministically across crossings,
3. supporter death/wall removal changes affected speeds at the exact event timestamp,
4. multi-supporter overlap remains non-stacking,
5. CHARGER phase speed composition is deterministic,
6. SPLITTER children can enter/leave aura deterministically after spawn,
7. FLYER aura affects X only; Y phase remains independent,
8. `wallAt` / `nextDueAt` remain exact enough for alarm scheduling,
9. reconnect reconstructs the same movement state.

Do not silently adopt tick-based approximation if it changes motion semantics. If exact continuous crossing creates disproportionate complexity, classify alternatives and obtain an explicit architecture/product decision first.

Following:
SIEGER.

After capabilities:
1. remaining player-skill authority needed for calibration,
2. approximately 50-stage tier/S-E-X authoring,
3. large deterministic 2/3/4-player simulation,
4. classify/report/discuss,
5. explicit production numerical freeze.

## Validation policy
Automatable validation must not be delegated to the user when CI can execute it.

## Governance
No numerical change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
