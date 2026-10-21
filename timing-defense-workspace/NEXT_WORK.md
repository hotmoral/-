# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**
6. v0.36 Slice A N1/N2 + Lv6 authority — **PASS**
7. v0.37 Slice B Stage 3 + BRUTE — **PASS**
8. v0.38 Slice C larger-party/event kernel — **FULL PASS**
9. v0.39 N3 authority — **FULL PASS**

Exact v0.39 full-PASS checkpoint:
- branch `timing-defense-cloudflare-v039-pass-20261022`
- HEAD `911dd67cf4bb4d704e050f8e3a92cb34c48deb3a`
- health `0.39-cf.1`

Closure evidence:
- GitHub Actions live Chromium/WebSocket suite FINAL PASS
- N3 server 57/57 PASS
- N3 client PASS
- synchronized 4H N3 stress PASS
- Samsung Browser presentation/input smoke PASS from `Screen_Recording_20261022_074414_Samsung Browser.mp4`

Full report:
`CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

## N3 product contract — CLOSED / FROZEN
- combo 5 / 10 / 20 / 30 / every +10 after 30
- exact max raw-equivalent budgets 60 / 90 / 150 / 210
- class geometry retained
- deterministic remainder-safe allocation
- no N3-generated EXP / charge / combo increment / ordinary crit / recursive skill / recursive N3
- normal armor / kill / kill coin / contribution
- frozen boss scalars
- generic N3 knockback NORMAL-equivalent
- Tank retains class/Lv6 knockback identity

---

# Campaign-direction correction

Do **not** continue reconstructing legacy Stage 4 -> Stage 10 as if those encounter recipes were the final campaign.

The final direction is a broader approximately 50-stage campaign with:
- tier identities,
- S / E / X pressure grammar,
- 2/3/4-player composition scaling,
- authored monster combinations,
- later production calibration by deterministic simulation.

The existing Stage 1–3 implementation remains useful as a **regression fixture for the validated combat/network kernel**, not as a requirement that the final campaign preserve those stage recipes.

The previously created `timing-defense-cloudflare-v040-stage4-shield` branch is preflight-only. Do not treat it as an approved Stage 4 production direction.

---

# Monster roster — STRUCTURE FROZEN V1

Canonical capability contract:
`MONSTER_CAPABILITY_CONTRACT_V1.md`

Nine ordinary archetypes:
1. GRUNT — baseline/reference
2. RUNNER — sustained high-speed pressure
3. BRUTE — raw durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — Y/spatial geometry
6. CHARGER — telegraphed, interruptible burst dash
7. SPLITTER — death -> exactly two non-splitting children
8. SUPPORTER — non-stacking nearby movement-speed aura only
9. SIEGER — standoff + telegraphed repeated wall attacks

Bosses remain a separate capability-composition layer and are not counted as an ordinary tenth archetype.

Production monster numbers are **NOT FROZEN** here.

Legacy coefficients may be used only as provisional/reference anchors for capability testing unless explicitly re-approved during final 50-stage calibration.

---

# Active next slice — Monster Capability Layer

## Phase A — capability sandbox / provisional test envelope
Create a stage-number-independent test harness so monster mechanics can be verified without authoring the final 50-stage campaign first.

Required properties:
- all gameplay-relevant monster state server-authoritative,
- small deterministic encounters,
- forced monster/state setup for tests,
- compatible with current human/AI/passive/Lv6/N3 authority,
- event/reconnect regression retained,
- no production balance claim.

Provisional values must be labelled:
**PROVISIONAL — NOT BALANCE FROZEN**.

## Recommended implementation order
1. SHIELD / common armor layer
2. FLYER / authoritative Y geometry
3. CHARGER state machine
4. SPLITTER child-spawn kernel
5. SUPPORTER dynamic movement-speed aura
6. SIEGER repeated wall-attack kernel

This order is intentional: low architectural novelty first, highest novelty last.

## Capability-specific acceptance examples
- SHIELD: all damage sources use explicit armor semantics; no GRUNT fallback.
- FLYER: server/client agree on authoritative Y geometry used by line/AoE skills.
- CHARGER: advance -> telegraph -> charge; authoritative knockback can cancel windup.
- SPLITTER: parent death creates exactly two deterministic non-recursive children.
- SUPPORTER: speed aura changes movement without timestamp drift; aura never stacks with itself.
- SIEGER: standoff -> windup -> repeated wall attack; knockback can force reposition.

Do not introduce manual target selection as a monster feature.

---

# After capability completion

1. Implement remaining player-skill authority needed for calibration.
2. Build the real 50-stage tier / S-E-X authoring model.
3. Generate candidate encounter recipes for 2/3/4-player teams.
4. Run large deterministic simulation for density, pressure, clear envelope and role opportunity.
5. Classify suspicious stages/parameters.
6. Discuss before numerical balance changes.
7. Explicitly freeze production monster/stage values.
8. Perform targeted Samsung Browser readability/input tests only where automation cannot judge presentation.

## Validation policy
Default:
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`.

Do not ask the user to manually open validation suites when CI can execute them.

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains deferred as one shared responsive layer.

## Governance
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
