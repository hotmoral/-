# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- watched HEAD: `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- health: `0.41-cf.1`

Last fully closed checkpoint:
- **v0.41 FLYER authoritative Y capability FULL PASS**
- branch `timing-defense-cloudflare-v041-flyer-pass-20261022`
- HEAD `7a68ba6d78b3ac8611c815f582e24e871a947f03`

Preserved checkpoints include:
- `timing-defense-cloudflare-v039-pass-20261022`
- `timing-defense-cloudflare-v040-shield-pass-20261022`
- `timing-defense-cloudflare-v041-flyer-pass-20261022`

Read first:
1. `NEXT_WORK.md`
2. `MONSTER_CAPABILITY_CONTRACT_V1.md`
3. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
4. `CLOUDFLARE_V041_FLYER_CAPABILITY_PASS_2026-10-22.md`
5. `CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`
6. `MONSTER_CAPABILITY_FOUNDATION_PASS_2026-10-22.md`
7. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

---

# Closed authoritative foundations

## v0.36
N1 exact EXP:
- NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28

N2 AI damage stage multiplier:
`1 + (stage - 1) * 0.035`

Lv6 authority:
- Knight +12% damage
- Rogue 55% second dagger after +55 ms
- Tank +30% knockback
- Archer up to two strict-line 52% secondary hits
- Mage up to three nearby 50% splash hits

## Stage 1–3 regression fixtures
Stage 1–3 remain regression fixtures for the validated network/combat kernel. They are not the production approximately-50-stage campaign specification.

## v0.38 event/multiplayer kernel
- 512 retained authoritative events
- per-WebSocket event cursor
- monotonic event-batch
- explicit event-gap
- resume/eventFloor suppression retained
- 3H / 4H / 2H+2AI / 3H+1AI validated
- reconnect / READY / START / Team Shop / NEXT validated

## v0.39 N3 — FULL PASS
Frozen:
- milestones 5 / 10 / 20 / 30 / every +10 after 30
- budgets 60 / 90 / 150 / 210
- Rogue 2/3/4/5
- Knight 67/33
- Tank 60/20/20
- Archer 70/30 strict line
- Mage 55/15/15/15
- no N3-generated EXP / charge / combo / ordinary crit / recursive skill / recursive N3
- normal armor / kill / kill coin / contribution semantics
- boss scalars retained
- NORMAL-equivalent generic N3 knockback

---

# Campaign direction
Legacy Stage 4 -> Stage 10 reconstruction is stopped as a production path.

Production direction:
- approximately 50 stages,
- tier identities,
- S / E / X pressure grammar,
- 2/3/4-player composition scaling,
- re-authored monster combinations,
- deterministic simulation before production numerical freeze.

Do not promote legacy stage recipes merely because they exist in source.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN
Nine ordinary archetypes:
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
Production monster coefficients remain **NOT FROZEN**; current executable values are provisional capability-test anchors.

---

# Monster Capability Foundation — PASS
Branch `timing-defense-cloudflare-v040-monster-capability-foundation`
Validated HEAD `68882c2013d1d35aaedbf12e5725fde377795044`
Foundation selftest **22/22 PASS**.

---

# v0.40 SHIELD/common armor — FULL PASS
Checkpoint:
- `timing-defense-cloudflare-v040-shield-pass-20261022`
- HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`

Closed semantics:
- SHIELD own speed/size/knock identity
- server armor applied once per target
- explicit pre-armor `rawDamage`
- AI multiplier before armor
- human/passive/AI/Lv6/N3 same armor policy
- Lv6 secondary derives from pre-armor primary raw damage
- kill/coin/contribution authoritative

Evidence:
- foundation 22/22
- N3 57/57
- SHIELD 11/11
- full browser/WebSocket regression FINAL PASS

---

# v0.41 FLYER authoritative Y — FULL PASS
Exact closure:
- branch `timing-defense-cloudflare-v041-flyer-pass-20261022`
- HEAD `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- health `0.41-cf.1`
- live Actions run `39697563460`
- artifact `12391810817`

Authoritative behavior:
- stable `flyerBaseY + flyerEpochAt` phase model
- `yAt(monster, at)` is the gameplay Y truth
- X materialization/knockback does not reset Y phase
- public snapshots expose phase metadata
- Lv6 Archer/Mage and N3 Archer geometry consume authoritative moving Y
- FLYER uses own `.100` X speed, `.78` size, `.90` knock resistance, reward 7
- no ground immunity
- reconnect reconstruction preserves identical future Y

Client hardening:
- server phase metadata drives network FLYER presentation
- legacy local `type==='flyer'` oscillator is suppressed in network mode
- same phase is extrapolated presentation-only between snapshots
- no client gameplay authority introduced

Live evidence:
- capability foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER server **10/10 PASS**
- FLYER client authority **5/5 PASS**
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- FINAL PASS

No Samsung Browser smoke was required because no FLYER is yet placed in a visible authored encounter.

Exact report:
`CLOUDFLARE_V041_FLYER_CAPABILITY_PASS_2026-10-22.md`

---

# Active next bounded work
**CHARGER authoritative state machine**, stage-number-independent.

Focus:
- authoritative ADVANCE / WINDUP / CHARGE phases,
- exact transition scheduling under non-constant speed,
- positive knockback during WINDUP cancels charge,
- provisional re-arm delay after cancel,
- CHARGE remains a temporary burst distinct from RUNNER sustained speed,
- public phase/timing metadata for later telegraph presentation,
- preserve v0.41/v0.40/v0.39 regressions,
- do not enable a legacy stage recipe.

Following: SPLITTER -> SUPPORTER -> SIEGER.

After capability completion:
- remaining player-skill authority needed for calibration,
- approximately 50-stage tier/S-E-X authoring,
- large deterministic 2/3/4-player simulation,
- explicit discussion before production numerical freeze.

# Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`

# Governance
No unapproved numerical change:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
