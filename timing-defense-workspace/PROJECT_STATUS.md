# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- watched HEAD at v0.39 closure: `911dd67cf4bb4d704e050f8e3a92cb34c48deb3a`

Last fully closed checkpoint:
- **v0.39 N3 authority FULL PASS**
- branch `timing-defense-cloudflare-v039-pass-20261022`
- HEAD `911dd67cf4bb4d704e050f8e3a92cb34c48deb3a`
- health `0.39-cf.1`

Preserved checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automation PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`
- v0.36 Slice A full PASS: `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- v0.37 Slice B full PASS: `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- v0.38 automation PASS: `timing-defense-cloudflare-v038-automation-pass-20261022`
- v0.38 Slice C full PASS: `timing-defense-cloudflare-v038-slice-c-pass-20261022`
- v0.39 N3 automation PASS: `timing-defense-cloudflare-v039-automation-pass-20261022`
- v0.39 N3 full PASS: `timing-defense-cloudflare-v039-pass-20261022`

Read first:
- `NEXT_WORK.md`
- `MONSTER_CAPABILITY_CONTRACT_V1.md`
- `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`
- `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`
- `CLOUDFLARE_V038_SLICE_C_PASS_2026-10-22.md`

---

# Closed Cloudflare gates
- v0.31/v0.32 waiting-room parity — PASS
- v0.33 Stage 1 authority — PASS
- v0.34 render/remote projectile parity — PASS
- v0.35 reconnect / Team Shop / Stage 2 — PASS
- v0.36 N1/N2 + Lv6 authority — FULL PASS
- v0.37 Stage 3 + BRUTE — FULL PASS
- v0.38 larger-party/event-delivery kernel — FULL PASS
- v0.39 N3 combo-milestone authority — FULL PASS

## v0.36 frozen parity
N1 exact EXP:
- NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28

N2:
`AI damage × (1 + (stage - 1) * 0.035)`

Lv6 authority:
- Knight +12% damage
- Rogue 55% second dagger after +55 ms
- Tank +30% knockback
- Archer up to two strict-line 52% secondary hits
- Mage up to three nearby 50% splash hits

## v0.37 Stage 3 regression fixture
- 12 enemies / 980 ms
- GRUNT 44% / RUNNER 34% / BRUTE 22%
- BRUTE base HP 900 / speed .040 / wall 180 / knock resist .38 / armor 1 / reward 14
- ordinary Stage 3 BRUTE HP 1247
- Stage 3 clear -> Team Shop

These Stage 1–3 recipes remain useful as regression fixtures for the current kernel. They are **not** a commitment that the final approximately 50-stage campaign will preserve these encounter recipes.

## v0.38 Slice C closure
Event kernel:
- 512 retained authoritative events
- per-WebSocket `eventRunId` + `eventCursor`
- monotonic `event-batch`
- state snapshots do not depend on the old fixed 24-event tail
- explicit `event-gap`
- resume/eventFloor historical replay suppression preserved

Automation PASS:
- SERVER 28/28
- v0.36 client regression PASS
- v0.37 client regression PASS
- event client PASS
- larger-party simulation PASS
- FINAL PASS

Party/device coverage:
- 3H / 4H / 2H+2AI / 3H+1AI
- host reconnect
- READY/START
- Stage 1 -> Shop -> Stage 2
- >24-event delivery without silent loss
- final Samsung Browser 4H smoke user-confirmed PASS

---

# v0.39 N3 — FULL PASS
Frozen contract:
- combo 5 / 10 / 20 / 30 / every +10 after 30
- exact raw-equivalent max budgets 60 / 90 / 150 / 210
- Rogue 2/3/4/5 daggers
- Knight 67/33
- Tank 60/20/20
- Archer 70/30 strict line
- Mage 55/15/15/15
- deterministic remainder-safe allocation
- no EXP / charge / combo / ordinary crit / recursive class skill / recursive N3
- normal armor / kill / kill coin / contribution attribution
- frozen boss scalars retained
- generic N3 knockback uses NORMAL-equivalent semantics
- Tank retains class/Lv6 knockback identity

Automated live validation on deployed Cloudflare through GitHub Actions + Playwright Chromium:
- V038 FULL REGRESSION PASS
- N3 SERVER 57/57 PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- FINAL PASS

Samsung Browser presentation/input smoke:
- user video `Screen_Recording_20261022_074414_Samsung Browser.mp4`
- frame review confirms coherent Rogue N3 multi-dagger burst
- no obvious projectile storm, duplicate cascade, flicker, Canvas corruption or blocked controls
- gameplay continued through later stages/shops without an obvious regression

Exact closure report:
`CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`

---

# Campaign / monster direction — revised after v0.39

Legacy Stage 4 -> Stage 10 reconstruction is **stopped** as a production path.

Reason:
- the intended production campaign is a broader approximately 50-stage structure,
- tier identities and S/E/X pressure composition will be re-authored,
- 2/3/4-player encounter composition will be calibrated later,
- therefore porting every legacy Stage 4–10 recipe before that redesign would create avoidable rework.

The previously created branch `timing-defense-cloudflare-v040-stage4-shield` is **preflight-only / not an approved production direction**.

## Monster Capability Contract V1 — STRUCTURE FROZEN
Canonical document:
`MONSTER_CAPABILITY_CONTRACT_V1.md`

Ordinary roster:
1. GRUNT — baseline/reference
2. RUNNER — sustained speed
3. BRUTE — raw durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — Y/spatial geometry
6. CHARGER — telegraphed interruptible burst dash
7. SPLITTER — death -> two non-recursive children
8. SUPPORTER — non-stacking movement-speed aura only
9. SIEGER — standoff + repeated telegraphed wall attack

Bosses are separate capability compositions, not a tenth ordinary archetype.

Production numerical values for this nine-archetype roster are **not frozen**. Legacy values are reference/provisional anchors only until final campaign calibration explicitly approves production values.

---

# Active next bounded work

Build the **Monster Capability Layer** independently of final stage numbering.

First create a deterministic capability sandbox/harness, then validate mechanics in this order:
1. SHIELD / common armor layer
2. FLYER / authoritative Y geometry
3. CHARGER state machine
4. SPLITTER child-spawn kernel
5. SUPPORTER dynamic movement-speed aura
6. SIEGER repeated wall-attack kernel

All provisional tuning used for the harness must be marked:
**PROVISIONAL — NOT BALANCE FROZEN**.

After capability completion:
- finish player-skill authority required for calibration,
- build the real approximately 50-stage tier / S-E-X authoring model,
- run large deterministic simulation,
- classify suspicious values/stages,
- discuss before changes,
- explicitly freeze production monster/stage numbers.

# Validation policy
Automated validation should not be delegated to the user when GitHub Actions can execute it.

Default sequence:
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred as one shared responsive-safety layer.

## Governance
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
