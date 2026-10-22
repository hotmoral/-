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

## Exact latest checkpoint
- branch `timing-defense-cloudflare-v042-charger-pass-20261022`
- HEAD `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a`
- public health `0.42-cf.1`
- live validation run `39703741827`

Closure report:
`CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`

v0.42 evidence:
- Foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER **10/10 PASS**
- CHARGER **17/17 PASS**
- root-loader PASS
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- **FINAL PASS**

No Samsung Browser smoke was required because CHARGER is not inserted into a visible authored encounter.

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
- common single-application armor path
- explicit pre-armor `rawDamage`
- AI multiplier before armor
- Lv6 secondaries derive from raw primary damage
- own speed/size/knock/reward identity.

## FLYER
- stable authoritative baseY/epoch phase
- `yAt()` gameplay truth
- materialize/knock/reconnect preserve phase
- Lv6/N3 geometry uses moving Y
- legacy client local oscillator suppressed in network mode.

## CHARGER
- authoritative `ADVANCE -> WINDUP -> CHARGE`
- state-aware non-constant X and wall timing
- WINDUP stationary
- positive knockback during WINDUP interrupts
- provisional re-arm after interrupt
- due timestamps included in scheduler
- reconnect reconstruction and public phase metadata
- late `advanceTo()` chronological replay validated.

CHARGER test coefficients remain provisional: HP380 / advance .060 / wall110 / knock .80 / armor1 / reward8 / windup650ms / charge .210 / trigger x .62 / re-arm900ms.

---

# Active next bounded slice — SPLITTER authoritative child-spawn kernel
This is stage-number-independent capability work, not a production stage recipe.

Frozen structural behavior:
`parent death -> exactly two child monsters -> children cannot split again`

Required implementation boundary:
- children are created by the server at the exact parent-death timestamp,
- exactly two children per parent death,
- deterministic child IDs from authoritative `nextMonsterId`,
- deterministic child ordering/offsets,
- `canSplit=false` is authoritative and persisted,
- SPLITTER children have explicit movement/wall/combat metadata and must never fall back to GRUNT defaults,
- simultaneous parent deaths produce deterministic child order,
- parent removal + child insertion must be safe while Lv6/N3/AI/passive loops are iterating,
- children participate normally in targeting, knockback, wall collision, event delivery and reconnect,
- event history/cursors remain monotonic,
- no recursive child spawning even when a child is killed by Lv6/N3,
- no legacy stage recipe enabled.

Provisional sandbox anchors already approved for capability testing only:
- parent HP 420
- parent speed `.065`
- parent wall damage 100
- parent knock resistance `.82`
- parent armor `1.00`
- package reward budget 8
- child HP 120
- child speed `.115`
- child wall damage 40
- child Y offsets `-0.018 / +0.018`

## Important unresolved economy semantic
The structural contract says the package has provisional reward budget 8, but it has **not** yet frozen how reward is divided between parent and children.

Do not silently convert that into a production economy rule. Capability implementation may use an explicitly provisional accounting rule for tests, but production reward allocation must be discussed/frozen later with campaign calibration.

Validation order:
1. audit kill/removal/iteration paths in ordinary hit, passive, AI, Lv6 and N3,
2. deterministic parent-death/child-ID/non-recursion tests,
3. simultaneous-split and multi-target mutation stress,
4. reconnect/event-stream regression,
5. prior v0.42/v0.41/v0.40/v0.39 regression,
6. GitHub Actions live validation,
7. device smoke only if a visible SPLITTER sandbox presentation is introduced.

## Following capability slices
1. SUPPORTER dynamic movement-speed aura
2. SIEGER repeated wall-attack kernel

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
