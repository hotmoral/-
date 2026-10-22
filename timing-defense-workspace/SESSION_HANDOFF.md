# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Current architecture
Primary lane: **Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- current validated HEAD `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- health `0.42-cf.1`

Last fully closed checkpoint:
- **v0.42 CHARGER authoritative state-machine capability FULL PASS**
- branch `timing-defense-cloudflare-v042-charger-pass-20261022`
- HEAD `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- live validation run `39703741827`

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `MONSTER_CAPABILITY_CONTRACT_V1.md`
5. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
6. `CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`
7. `CLOUDFLARE_V041_FLYER_CAPABILITY_PASS_2026-10-22.md`
8. `CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`
9. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

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
- common single-application armor path, rawDamage, AI-before-armor, Lv6 secondary raw hardening, own SHIELD movement/knock/reward identity.

## v0.41 FLYER — FULL PASS
- branch `timing-defense-cloudflare-v041-flyer-pass-20261022`
- HEAD `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- health `0.41-cf.1`
- stable baseY/epoch, `yAt()` authority, phase-preserving materialization/reconnect, Lv6/N3 moving-Y geometry, client local oscillator suppression.

## v0.42 CHARGER — FULL PASS
- branch `timing-defense-cloudflare-v042-charger-pass-20261022`
- HEAD `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- health `0.42-cf.1`
- live run `39703741827`
- report `CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`

Authoritative semantics:
- `ADVANCE -> WINDUP -> CHARGE`
- ADVANCE `.060`, WINDUP stationary, CHARGE `.210` are provisional capability-test values
- state-aware X/materialization/wall timing
- positive knockback during WINDUP interrupts
- interrupt -> ADVANCE + provisional 900 ms re-arm
- scheduler sees transition/wall due times
- persisted phase/refAt/rearm reconstructs after reconnect
- public state exposes phase/timing metadata
- Tank Lv6 knock, AI multiplier, kill/reward/contribution, team-DEF wall mitigation retained
- late `advanceTo()` chronological replay explicitly tested.

Provisional CHARGER anchors: HP380 / wall110 / knock.80 / armor1 / reward8 / windup650ms / trigger x.62. **Not production frozen.**

Validation evidence:
- foundation **22/22**
- N3 **57/57**
- SHIELD **11/11**
- FLYER **10/10**
- CHARGER **17/17**
- root-loader PASS
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- **FINAL PASS**

No Samsung Browser smoke: CHARGER has no visible authored encounter/telegraph yet.

---

# Active next boundary — SPLITTER authoritative child-spawn kernel
Stage-number-independent capability work; not a legacy stage implementation.

Frozen structure:
`SPLITTER parent death -> exactly two deterministic children -> children never split again`

Provisional sandbox anchors:
- parent HP420 / speed `.065` / wall100 / knock `.82` / armor1
- package reward budget8
- child HP120 / speed `.115` / wall40
- child Y offsets `-.018 / +.018`

Required semantics:
- spawn exactly two children at parent-death timestamp,
- authoritative deterministic IDs/order from `nextMonsterId`,
- persisted `canSplit=false`,
- explicit child movement/wall/combat identity; no GRUNT fallback,
- safe mutation under ordinary hit/passive/AI/Lv6/N3 loops,
- deterministic simultaneous parent deaths,
- child targeting/knock/wall/event/reconnect support,
- killing children never recursively spawns more children,
- no legacy stage recipe enabled.

Important unresolved semantic:
- provisional reward package budget is 8, but exact parent/child reward allocation is **not production frozen**. Do not silently turn a sandbox accounting choice into the final economy.

Validation sequence:
`kill-path audit -> deterministic split/non-recursion tests -> simultaneous/multi-target stress -> event/reconnect regression -> prior capability regression -> GitHub Actions live validation -> device smoke only if visible presentation is introduced`.

Following:
SUPPORTER -> SIEGER.

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
