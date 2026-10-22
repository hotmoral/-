# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Current architecture
Primary lane:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- current validated HEAD `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- health `0.41-cf.1`

Last fully closed checkpoint:
- **v0.41 FLYER authoritative Y capability FULL PASS**
- branch `timing-defense-cloudflare-v041-flyer-pass-20261022`
- HEAD `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- live validation run `39697563460`

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `MONSTER_CAPABILITY_CONTRACT_V1.md`
5. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
6. `CLOUDFLARE_V041_FLYER_CAPABILITY_PASS_2026-10-22.md`
7. `CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`
8. `MONSTER_CAPABILITY_FOUNDATION_PASS_2026-10-22.md`
9. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

---

# Frozen/closed combat foundations

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
- reconnect / READY / START / Team Shop / NEXT

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

---

# Campaign direction correction
Do **not** continue legacy Stage 4 -> Stage 10 reconstruction as the production campaign.

Production direction is approximately 50 stages with:
- tier identities,
- S / E / X pressure grammar,
- 2/3/4-player composition scaling,
- re-authored monster combinations,
- deterministic simulation/calibration before production-number freeze.

Stage 1–3 remain regression fixtures only.
The old `timing-defense-cloudflare-v040-stage4-shield` branch is preflight-only and must not be resumed without a new explicit decision.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN
Ordinary roster:
1. GRUNT — baseline/reference
2. RUNNER — sustained tempo
3. BRUTE — raw durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — authoritative Y/spatial geometry
6. CHARGER — telegraphed interruptible burst dash
7. SPLITTER — parent death -> exactly two non-recursive children
8. SUPPORTER — non-stacking movement-speed aura only
9. SIEGER — standoff + repeated telegraphed wall attacks

Bosses are separate capability compositions.
No hard class lockouts. No manual target-selection requirement. Gameplay state is server authoritative.
Current executable monster coefficients remain provisional unless separately frozen.

---

# Monster Capability Foundation — PASS
- branch `timing-defense-cloudflare-v040-monster-capability-foundation`
- HEAD `68882c2013d1d35aaedbf12e5725fde377795044`
- foundation selftest **22/22 PASS**

---

# v0.40 SHIELD/common armor — FULL PASS
Checkpoint:
- `timing-defense-cloudflare-v040-shield-pass-20261022`
- HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`

Closed:
- SHIELD own speed/size/knock identity
- armor applied once per target
- event `rawDamage` before armor, `damage` after armor
- AI multiplier before armor
- Lv6 secondary derives from pre-armor primary raw damage to prevent double armor
- kill/coin/contribution authoritative

Evidence:
- foundation 22/22
- N3 57/57
- SHIELD 11/11
- full browser/WebSocket regression FINAL PASS

---

# v0.41 FLYER authoritative Y — FULL PASS
Checkpoint:
- branch `timing-defense-cloudflare-v041-flyer-pass-20261022`
- HEAD `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- health `0.41-cf.1`
- live validation run `39697563460`
- evidence artifact `12391810817`

Server model:
- stable `flyerBaseY` + `flyerEpochAt`
- `yAt(monster, at)` is authoritative gameplay Y
- materialization/knockback does not reset Y phase
- public state carries current y + baseY/yEpochAt/yAmp/yOmega
- FLYER uses own speed `.100`, size `.78`, knock `.90`, reward 7
- no ground immunity

Geometry:
- v036/v039 pointAt consumes room.yAt when available
- Lv6 Archer line uses authoritative moving Y
- Lv6 Mage AoE uses authoritative moving Y
- N3 Archer line uses authoritative moving Y
- reconnect reconstruction preserves the same future Y

Client:
- `v041-flyer-authority.js` consumes server phase metadata
- presentation-only extrapolation uses same phase formula
- network FLYER temporarily aliases to `flyer_net` during inherited update to suppress the legacy independent local oscillator
- type restores to `flyer` before rendering
- no client gameplay authority

Validation:
- foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER server **10/10 PASS**
- FLYER client **5/5 PASS**
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- FINAL PASS

No device smoke required because no FLYER is currently placed in a visible authored encounter.

---

# Active next boundary — CHARGER authoritative state machine
Stage-number-independent capability work, not a legacy stage implementation.

Frozen structure:
`ADVANCE -> WINDUP -> CHARGE -> wall/contact resolution`

Provisional sandbox anchors:
- HP 380
- advance speed `.060`
- wall damage 110
- knock resistance `.80`
- armor `1.00`
- reward 8
- windup 650 ms
- charge speed `.210`
- test trigger x `.62`
- re-arm delay 900 ms after interrupt

Required implementation semantics:
- state-aware X/materialization instead of constant-speed assumption,
- exact trigger/windup/charge due times in `processAt/nextDueAt`,
- WINDUP is stationary for deterministic telegraphing in this sandbox capability,
- positive authoritative knockback during WINDUP cancels the pending charge,
- cancel returns to ADVANCE and blocks re-arm until provisional re-arm time,
- CHARGE continues at temporary high speed until wall/contact resolution,
- public state exposes phase/timing metadata for later client telegraph,
- normal/passive/AI/Lv6/N3 reward/damage/contribution remain authoritative,
- no legacy stage recipe is enabled.

Validation:
`state-machine deterministic tests -> prior v0.41/v0.40/v0.39 regression -> live GitHub Actions -> device smoke only if visible CHARGER sandbox presentation is added`.

Following:
SPLITTER -> SUPPORTER -> SIEGER.

After capabilities:
1. remaining player-skill authority needed for calibration,
2. approximately 50-stage tier/S-E-X authoring,
3. large deterministic 2/3/4-player simulation,
4. classify/report/discuss,
5. explicit production numerical freeze.

## Validation policy
Automatable validation must not be delegated to the user unless CI cannot execute it.

## Governance
No numerical change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
