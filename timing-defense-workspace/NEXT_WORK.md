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
11. v0.40 SHIELD/common armor — **FULL PASS**
12. v0.41 FLYER authoritative Y — **FULL PASS**
13. v0.42 CHARGER authoritative state machine — **FULL PASS**
14. v0.43 SPLITTER authoritative child-spawn kernel — **FULL PASS**

## Exact latest checkpoint
- branch `timing-defense-cloudflare-v043-splitter-pass-20261022`
- HEAD `d1bac2effbd866aa221d55829678f959bc099b82`
- public health `0.43-cf.1`
- live validation run `39705143877`
- live job `119583316125`

Closure report:
`CLOUDFLARE_V043_SPLITTER_CAPABILITY_PASS_2026-10-22.md`

v0.43 evidence:
- Foundation **22/22 PASS**
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

No Samsung Browser smoke was required because SPLITTER is not inserted into a visible authored encounter and final split VFX is not part of this slice.

Important: SPLITTER reward accounting `4 + 2 + 2 = 8` is **PROVISIONAL TEST ACCOUNTING ONLY**, not production economy freeze.

---

# Campaign-direction rule
Do **not** reconstruct legacy Stage 4 -> Stage 10 as the production campaign.

Final direction remains an approximately 50-stage campaign with:
- tier identities,
- S / E / X pressure grammar,
- 2/3/4-player composition scaling,
- re-authored monster combinations,
- deterministic simulation/calibration before numerical freeze.

Stage 1–3 remain regression fixtures only.

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
9. SIEGER — standoff + repeated telegraphed wall attacks

All current executable monster coefficients remain **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN** unless separately approved.

---

# Closed capability summaries

## SHIELD
Common one-time armor path, explicit `rawDamage`, AI-before-armor, Lv6 raw-secondary hardening, own movement/knock/reward identity.

## FLYER
Stable authoritative baseY/epoch, `yAt()` gameplay truth, phase-preserving materialization/reconnect, Lv6/N3 moving-Y geometry, client local oscillator suppression.

## CHARGER
Authoritative `ADVANCE -> WINDUP -> CHARGE`, state-aware nonconstant X/wall timing, WINDUP interruption/re-arm, scheduler/reconnect chronology validated.

## SPLITTER
- exact two-child authoritative spawn on parent death
- deterministic IDs/order/offsets
- child `canSplit=false`
- explicit parent/child movement/wall/size/knock identity
- shared package attribution
- split metadata stays on existing damage event to preserve event ordering
- simultaneous split, N3 retarget, reconnect, event monotonicity validated.

---

# Active next bounded slice — SUPPORTER authoritative dynamic movement-speed aura
This remains stage-number-independent capability work, not production encounter authoring.

Frozen structural behavior:
- nearby monsters receive a movement-speed multiplier while inside aura range,
- SUPPORTER does not buff itself,
- multiple SUPPORTER auras do **not** stack,
- V1 changes movement speed only,
- no heal / armor / outgoing damage / wall damage / knock-resistance buff,
- no manual target selection requirement,
- no legacy stage recipe enabled.

Provisional sandbox anchors already approved for capability testing only:
- HP 280
- speed `.055`
- wall damage 70
- knock resistance `.90`
- armor `1.00`
- reward 8
- aura radius `.18`
- aura speed multiplier `1.18`

These are **NOT production balance frozen**.

## Critical architecture question before implementation
Aura membership changes with relative motion. A naive `distance <= .18 ? 1.18 : 1` calculation only when a snapshot/action occurs can make X integration depend on polling frequency, creating timestamp drift.

Before coding the live path, audit and explicitly define:
1. the exact authoritative timestamp at which a monster enters/leaves an aura,
2. how X movement is integrated across aura-boundary crossings,
3. how SUPPORTER death/wall removal changes speed at that exact timestamp,
4. how multiple SUPPORTERs remain non-stacking while membership changes,
5. interaction with CHARGER phase speeds,
6. interaction with SPLITTER child spawn/death,
7. FLYER: aura affects X speed only; Y phase remains independent,
8. `wallAt()` and `nextDueAt()` consistency under dynamic aura membership,
9. reconnect reconstruction from persisted state without phase/time drift.

Do **not** silently choose a tick-based approximation if that changes authoritative motion semantics. If an exact continuous solution would materially increase complexity, classify alternatives and make an explicit product/architecture decision first.

## Validation sequence
1. movement/aura topology audit,
2. deterministic single-supporter crossing tests,
3. non-stacking multi-supporter tests,
4. supporter death/wall-removal boundary tests,
5. CHARGER/SPLITTER/FLYER interaction tests,
6. reconnect/wallAt/nextDueAt regression,
7. prior capability regression,
8. GitHub Actions live validation,
9. device smoke only if visible aura presentation is introduced.

## Following capability slice
SIEGER repeated wall-attack kernel.

After capabilities:
- remaining player-skill authority needed for calibration,
- approximately 50-stage tier/S-E-X authoring,
- large deterministic 2/3/4-player simulation,
- classify/report/discuss,
- explicit production numerical freeze.

## Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`

Do not delegate automatable validation to the user.

## Governance
No unapproved numerical change:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
