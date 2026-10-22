# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Closed implementation gates
1. Cloudflare DO PoC — **PASS**
2. v0.31/v0.32 waiting room — **PASS**
3. v0.33 Stage1 authority — **PASS**
4. v0.34 render/remote projectile parity — **PASS**
5. v0.35 reconnect/Team Shop/Stage2 — **PASS**
6. v0.36 N1/N2 + Lv6 — **FULL PASS**
7. v0.37 Stage3 + BRUTE regression fixture — **FULL PASS**
8. v0.38 larger-party/event kernel — **FULL PASS**
9. v0.39 N3 — **FULL PASS**
10. Monster Capability Foundation V1 — **PASS**
11. v0.40 SHIELD — **FULL PASS**
12. v0.41 FLYER — **FULL PASS**
13. v0.42 CHARGER — **FULL PASS**
14. v0.43 SPLITTER — **FULL PASS**
15. v0.44 SUPPORTER — **FULL PASS**

## Exact latest checkpoint
- branch `timing-defense-cloudflare-v044-supporter-pass-20261022`
- HEAD `b2dc0269e144d9fa13ee490bba36ae93839f6a20`
- health `0.44-cf.1`
- live run/job `39706896662` / `119588945997`

Closure report:
`CLOUDFLARE_V044_SUPPORTER_CAPABILITY_PASS_2026-10-22.md`

Evidence:
- Foundation **22/22 PASS**
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

No Samsung Browser smoke required: no visible SUPPORTER encounter/final aura presentation exists yet.

---

# Campaign direction
Do **not** reconstruct legacy Stage4→10 as production content.

Final direction remains approximately 50 stages with tier identities, S/E/X pressure grammar, 2/3/4-player composition scaling, re-authored monster combinations, and deterministic simulation before production balance freeze.

Stage1–3 remain regression fixtures only.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN
Ordinary roster:
1. GRUNT — baseline
2. RUNNER — sustained tempo
3. BRUTE — durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — authoritative Y geometry
6. CHARGER — telegraphed interruptible burst
7. SPLITTER — exact two-child non-recursive split
8. SUPPORTER — non-stacking movement-speed aura
9. SIEGER — standoff + repeated telegraphed wall attack

Current executable capability coefficients are **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN** unless separately approved.

---

# Closed capability notes

## SHIELD
Common single-application armor / explicit rawDamage / own movement-knock-reward identity.

## FLYER
Stable authoritative Y phase / moving-Y Lv6+N3 geometry / reconnect/client parity.

## CHARGER
Authoritative ADVANCE→WINDUP→CHARGE / exact scheduler chronology / knock interruption and re-arm.

## SPLITTER
Exact two-child spawn / deterministic IDs-offsets / no recursive child split / N3 retarget / explicit child identity / provisional reward accounting only.

## SUPPORTER
- event-driven aura boundary crossings, no fixed gameplay tick
- persisted source IDs / non-stacking
- self-exclusion
- exact materialize-before-membership-change
- FLYER Y-aware 2D geometry
- CHARGER phase composition
- SPLITTER child immediate reconciliation
- death/wall/knock topology updates at exact timestamp
- reconnect and nextDueAt validated
- provisional HP280/speed.055/wall70/knock.90/reward8/radius.18/speed×1.18 and Euclidean sandbox geometry are **not production frozen**.

---

# Active bounded slice — SIEGER authoritative standoff/repeated wall-attack kernel
This is stage-number-independent capability work, not final encounter authoring.

Frozen structural behavior:
`ADVANCE -> arrive at standoff -> WINDUP -> FIRE -> COOLDOWN -> WINDUP -> ...`

Required semantics:
- exact authoritative arrival at standoff,
- no direct wall contact while correctly sieging,
- 800ms provisional windup before first shot,
- repeated provisional 75 wall damage on 2200ms cadence,
- team DEF must apply through the same wall-damage policy unless audit shows an explicit prior exception,
- SIEGER remains alive after a siege shot,
- knockback during WINDUP/COOLDOWN/SIEGE can push it outside standoff and force ADVANCE/reposition,
- SUPPORTER aura may affect ADVANCE movement only; it must never alter windup/repeat cadence or shot damage,
- FLYER/SPLITTER/etc. behavior unchanged,
- persisted phase/timestamps reconstruct after reconnect,
- `nextDueAt()` includes standoff arrival, windup completion and subsequent cycle events,
- repeated shots must not break event cursor/history semantics,
- no production stage recipe enabled.

Provisional capability-test anchors:
- HP520
- approach speed `.045`
- knock resistance `.55`
- armor `1.00`
- reward11
- standoff X `.38`
- windup800ms
- siege shot75
- repeat2200ms

These values remain **NOT production frozen**.

## Preflight questions to resolve before live implementation
1. exact phase definitions and whether FIRE is instantaneous or represented as a state marker,
2. whether repeated shots reuse `wall` events with `siegeShot=true` while keeping the monster alive,
3. knockback threshold/reposition rule relative to standoff X,
4. team-DEF application order,
5. SUPPORTER aura integration in approach only,
6. stage clear behavior while a SIEGER remains alive,
7. reconnect/late-alarm chronological replay.

## Validation sequence
1. preflight/code audit,
2. deterministic state-machine tests,
3. DEF/repeated-shot/knockback/reposition tests,
4. SUPPORTER aura composition test,
5. reconnect/late-advance chronology,
6. prior capability regressions,
7. GitHub Actions live validation,
8. device smoke only if visible final SIEGER telegraph/presentation is introduced.

After SIEGER closes:
1. review remaining player-skill authority required for calibration,
2. build approximately 50-stage tier/S-E-X authoring model,
3. large deterministic 2/3/4-player simulation,
4. classify/report/discuss,
5. explicit production numerical freeze.

## Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`

## Governance
No unapproved numerical change:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
