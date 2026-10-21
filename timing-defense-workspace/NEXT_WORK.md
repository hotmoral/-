# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Closed implementation gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 Stage 1 authority — **PASS**
4. v0.34 render/remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 — **PASS**
6. v0.36 N1/N2 + Lv6 authority — **FULL PASS**
7. v0.37 Stage 3 + BRUTE regression fixture — **FULL PASS**
8. v0.38 larger-party/event kernel — **FULL PASS**
9. v0.39 N3 authority — **FULL PASS**
10. Monster Capability Foundation V1 — **PASS**
11. v0.40 SHIELD/common armor capability — **FULL PASS**

## Exact latest checkpoint
- branch `timing-defense-cloudflare-v040-shield-pass-20261022`
- HEAD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad`
- public health `0.40-cf.2`
- live validation run `39696308376`

Closure report:
`CLOUDFLARE_V040_SHIELD_CAPABILITY_PASS_2026-10-22.md`

v0.40 evidence:
- Monster Capability Foundation **22/22 PASS**
- v0.39 N3 server regression **57/57 PASS**
- SHIELD authority **11/11 PASS**
- V038 full browser/WebSocket regression PASS
- N3 client PASS
- N3 4H stress PASS
- FINAL PASS

No Samsung Browser smoke was required because SHIELD was not inserted into a public encounter and the slice introduced no new player-visible presentation.

---

# Campaign-direction rule

Do **not** reconstruct legacy Stage 4 -> Stage 10 as the production campaign.

The final direction remains an approximately 50-stage campaign with:
- tier identities,
- S / E / X pressure grammar,
- 2/3/4-player composition scaling,
- re-authored monster combinations,
- later deterministic simulation/calibration.

Existing Stage 1–3 content is retained as regression fixture material for the validated combat/network kernel.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN

Canonical structure:
`MONSTER_CAPABILITY_CONTRACT_V1.md`

Provisional executable values:
`MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`

Those values are explicitly:
**PROVISIONAL — NOT BALANCE FROZEN**.

Ordinary roster:
1. GRUNT — baseline/reference
2. RUNNER — sustained tempo
3. BRUTE — raw durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — Y/spatial geometry
6. CHARGER — telegraphed interruptible burst dash
7. SPLITTER — death -> two non-recursive children
8. SUPPORTER — non-stacking movement-speed aura only
9. SIEGER — standoff + repeated telegraphed wall attacks

Bosses remain a separate capability-composition layer.

---

# Closed capability slice — SHIELD/common armor

Validated stage-independent behavior:
- SHIELD movement and wall timing do not fall back to GRUNT,
- authoritative armor applies once per target,
- `rawDamage` is explicit before armor and event `damage` is post-armor,
- AI stage multiplier occurs before armor,
- passive / human / AI / Lv6 / N3 share the armor policy,
- SHIELD size/knock metadata is available to Lv6/N3 geometry,
- kill / coin / killCoinEarned / contribution stay authoritative,
- prior armor=1 Stage 1–3 behavior remains regression-stable.

The `.72` armor and other current SHIELD coefficients are capability-test anchors, not final production balance freeze.

---

# Active next bounded slice — FLYER / authoritative Y geometry

This is **not Stage 5/6 implementation**. It is a stage-number-independent monster capability slice.

Required boundary:
- authoritative FLYER Y position as a deterministic function/state,
- same Y truth used by targeting, Archer strict-line geometry, Mage AoE geometry and client interpolation,
- reconnect/state reconstruction does not phase-jump or disagree on Y,
- normal / passive / AI / Lv6 / N3 damage attribution remains unchanged,
- no ground-immunity mechanic; every class can attack FLYER,
- no legacy stage recipe is enabled,
- provisional FLYER coefficients remain non-production-frozen.

Validation order:
1. code audit of current X-only movement assumptions,
2. deterministic FLYER Y/geometry selftests,
3. v0.40 SHIELD + v0.39 full regression,
4. live GitHub Actions Chromium/WebSocket validation,
5. only if a visible sandbox encounter is introduced, minimum Samsung Browser visual/readability smoke.

## Following capability slices
1. CHARGER state machine
2. SPLITTER child-spawn kernel
3. SUPPORTER dynamic movement-speed aura
4. SIEGER repeated wall-attack kernel

After capabilities:
- implement remaining player-skill authority needed for calibration,
- build approximately 50-stage tier/S-E-X authoring,
- simulate 2/3/4-player candidate recipes at scale,
- classify and discuss before numerical changes,
- explicitly freeze production monster/stage values.

## Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`

Do not delegate automatable validation to the user.

## Governance
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
