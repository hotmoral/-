# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- watched HEAD: `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`
- health: `0.40-cf.2`

Last fully closed checkpoint:
- **v0.40 SHIELD/common armor capability FULL PASS**
- branch `timing-defense-cloudflare-v040-shield-pass-20261022`
- HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`

Preserved checkpoints include:
- `timing-defense-cloudflare-v038-slice-c-pass-20261022`
- `timing-defense-cloudflare-v039-pass-20261022`
- `timing-defense-cloudflare-v040-shield-pass-20261022`

Read first:
1. `NEXT_WORK.md`
2. `MONSTER_CAPABILITY_CONTRACT_V1.md`
3. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
4. `CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`
5. `MONSTER_CAPABILITY_FOUNDATION_PASS_2026-10-22.md`
6. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

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
These remain useful for regression of the validated kernel but are **not final approximately 50-stage campaign authoring commitments**.

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

v0.39 live automation:
- V038 full regression PASS
- N3 server 57/57
- N3 client PASS
- N3 4H stress PASS
- FINAL PASS

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

Do not promote old stage recipes into production merely because legacy code contains them.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN

Nine ordinary archetypes:
1. GRUNT — baseline/reference
2. RUNNER — sustained tempo
3. BRUTE — raw durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — Y/spatial geometry
6. CHARGER — telegraphed interruptible burst dash
7. SPLITTER — death -> exactly two non-recursive children
8. SUPPORTER — non-stacking movement-speed aura only
9. SIEGER — standoff + repeated telegraphed wall attack

Bosses are separate capability compositions.

Production monster coefficients are **not frozen**. Current executable values are provisional capability-test anchors only.

---

# Monster Capability Foundation — PASS

Branch:
`timing-defense-cloudflare-v040-monster-capability-foundation`

Validated HEAD:
`68882c2013d1d35aaedbf12e5725fde377795044`

GitHub Actions foundation selftest:
**22/22 PASS**.

---

# v0.40 SHIELD/common armor — FULL PASS

Exact closure:
- branch `timing-defense-cloudflare-v040-shield-pass-20261022`
- HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`
- health `0.40-cf.2`
- live Actions run `39696308376`

Validated capability semantics:
- SHIELD movement/wall timing uses SHIELD speed, not GRUNT fallback,
- authoritative armor applies exactly once to each target,
- event exposes pre-armor `rawDamage` and post-armor `damage`,
- AI stage multiplier precedes armor,
- human / AI / passive / Lv6 / N3 use the common armor policy,
- Lv6/N3 geometry uses SHIELD size 1.08,
- knock paths use SHIELD knock resistance .62,
- kill / coin / killCoinEarned / contribution remain authoritative.

Important hardening:
- Lv6 secondary damage now derives from pre-armor primary raw damage before the secondary target applies its own armor. This prevents double-armor behavior while preserving prior armor=1 results.

Live evidence:
- capability foundation 22/22 PASS
- v0.39 N3 57/57 PASS
- SHIELD authority 11/11 PASS
- V038 full browser/WebSocket regression PASS
- N3 client PASS
- N3 4H stress PASS
- FINAL PASS

Current SHIELD `.72` armor and related coefficients are still **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN**.

No device smoke was required because this slice did not place SHIELD into a visible public encounter.

Exact report:
`CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`

---

# Active next bounded work

**FLYER / authoritative Y geometry**, stage-number-independent.

Required focus:
- one authoritative Y truth for server targeting/geometry and client presentation,
- Archer strict-line and Mage AoE consume the same Y state,
- reconnect/state reconstruction remains deterministic,
- no ground-immunity rule,
- no legacy stage recipe enablement,
- preserve all v0.40/v0.39 regressions.

Following capability order:
CHARGER -> SPLITTER -> SUPPORTER -> SIEGER.

After capability completion:
- remaining player-skill authority needed for calibration,
- approximately 50-stage tier/S-E-X authoring,
- large deterministic simulation,
- explicit discussion before production numerical freeze.

# Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`

# Governance
No unapproved numerical change:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
