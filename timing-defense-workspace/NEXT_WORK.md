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
12. v0.41 FLYER authoritative Y geometry — **FULL PASS**

## Exact latest checkpoint
- branch `timing-defense-cloudflare-v041-flyer-pass-20261022`
- HEAD `7a68ba6d78b3ac8611c815f582e24e871a947f03`
- public health `0.41-cf.1`
- live validation run `39697563460`

Closure report:
`CLOUDFLARE_V041_FLYER_CAPABILITY_PASS_2026-10-22.md`

v0.41 evidence:
- Monster Capability Foundation **22/22 PASS**
- v0.39 N3 **57/57 PASS**
- v0.40 SHIELD **11/11 PASS**
- v0.41 FLYER server **10/10 PASS**
- FLYER client authority **5/5 PASS**
- V038 full browser/WebSocket regression PASS
- N3 client PASS
- N3 4H stress PASS
- FINAL PASS

No Samsung Browser smoke was required because FLYER was not inserted into a public authored encounter.

---

# Campaign-direction rule
Do **not** reconstruct legacy Stage 4 -> Stage 10 as the production campaign.

The final direction remains an approximately 50-stage campaign with:
- tier identities,
- S / E / X pressure grammar,
- 2/3/4-player composition scaling,
- re-authored monster combinations,
- later deterministic simulation/calibration.

Existing Stage 1–3 content is retained as regression fixture material only.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN
Ordinary roster:
1. GRUNT — baseline/reference
2. RUNNER — sustained tempo
3. BRUTE — raw durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — authoritative Y/spatial geometry
6. CHARGER — telegraphed interruptible burst dash
7. SPLITTER — death -> two non-recursive children
8. SUPPORTER — non-stacking movement-speed aura only
9. SIEGER — standoff + repeated telegraphed wall attacks

All current executable monster coefficients remain **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN** unless separately frozen by an explicit decision.

---

# Closed capability — SHIELD/common armor
- stage-independent common armor path
- pre-armor `rawDamage`, post-armor event `damage`
- AI multiplier before armor
- Lv6 secondary raw-damage hardening prevents double armor
- SHIELD own size/knock/speed identity
- full prior regression PASS

# Closed capability — FLYER authoritative Y
- stable server-owned `baseY + epoch` phase
- materialize/knockback does not reset Y phase
- public snapshots expose phase metadata
- Archer Lv6/N3 and Mage Lv6 consume authoritative moving Y
- FLYER own speed/size/knock/reward identity
- client legacy local FLYER oscillator suppressed in network mode
- client extrapolates the same authoritative phase between snapshots
- reconnect reconstructs identical future Y
- no ground immunity

---

# Active next bounded slice — CHARGER authoritative state machine
This is stage-number-independent capability work, not a production stage recipe.

Frozen structural behavior:
`ADVANCE -> WINDUP -> CHARGE -> wall/contact resolution`

Required boundary:
- base movement and charge movement are separate authoritative phases,
- WINDUP is stationary/readable enough to be telegraphed by later presentation,
- positive authoritative knockback during WINDUP cancels the pending charge,
- cancellation returns CHARGER to ADVANCE with a provisional sandbox re-arm delay,
- CHARGE uses its own high temporary speed and must not collapse into RUNNER's always-fast identity,
- wall timing/scheduler must account for state transitions rather than assume one constant speed,
- public state exposes phase/timing metadata for later client telegraphing,
- normal/passive/AI/Lv6/N3 damage/reward/contribution remain authoritative,
- no legacy stage recipe is enabled,
- provisional CHARGER coefficients are not production-frozen.

Provisional sandbox anchors currently approved for capability testing only:
- HP 380
- advance speed `.060`
- wall damage 110
- knock resistance `.80`
- armor `1.00`
- reward 8
- windup 650 ms
- charge speed `.210`
- test trigger x `.62`
- test re-arm delay 900 ms

Validation order:
1. audit existing constant-speed `xAt/wallAt/nextDueAt` assumptions,
2. deterministic state-transition/interrupt/wall-time tests,
3. prior v0.41/v0.40/v0.39 regression,
4. live GitHub Actions Chromium/WebSocket validation,
5. only if a visible CHARGER sandbox encounter is introduced, minimum Samsung Browser telegraph/readability smoke.

## Following capability slices
1. SPLITTER child-spawn kernel
2. SUPPORTER dynamic movement-speed aura
3. SIEGER repeated wall-attack kernel

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
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
