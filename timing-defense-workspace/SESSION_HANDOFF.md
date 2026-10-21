# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Current architecture
Primary lane:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- HEAD at v0.39 closure `911dd67cf4bb4d704e050f8e3a92cb34c48deb3a`

Last fully closed checkpoint:
- **v0.39 N3 authority FULL PASS**
- branch `timing-defense-cloudflare-v039-pass-20261022`
- HEAD `911dd67cf4bb4d704e050f8e3a92cb34c48deb3a`
- health `0.39-cf.1`

## Preserved checkpoints
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

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `MONSTER_CAPABILITY_CONTRACT_V1.md`
5. `CLOUDFLARE_V039_N3_FULL_PASS_2026-10-22.md`
6. `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`

## Closed authoritative foundations
### v0.36
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

### v0.37 regression fixture
- Stage 3 = 12 enemies / 980 ms
- GRUNT 44% / RUNNER 34% / BRUTE 22%
- BRUTE base HP 900 / speed .040 / wall 180 / knock resist .38 / armor 1 / reward 14
- ordinary Stage 3 BRUTE HP 1247

Stage 1–3 are now treated as regression fixtures for the validated kernel, not as final approximately 50-stage campaign authoring commitments.

### v0.38 event/multiplayer kernel
- 512 retained authoritative events
- per-WebSocket `eventRunId` + `eventCursor`
- monotonic `event-batch`
- explicit `event-gap`
- resume/eventFloor suppression preserved
- 3H / 4H / 2H+2AI / 3H+1AI validated
- host reconnect / READY / START / Team Shop / NEXT validated
- >24-event delivery validated

### v0.39 N3
Frozen:
- combo milestones 5 / 10 / 20 / 30 / every +10 after 30
- budgets 60 / 90 / 150 / 210
- Rogue 2/3/4/5 daggers
- Knight 67/33
- Tank 60/20/20
- Archer 70/30 strict line
- Mage 55/15/15/15
- no N3-generated EXP / charge / combo / ordinary crit / recursive skill / recursive N3
- normal armor / kill / kill coin / contribution
- frozen boss scalars
- NORMAL-equivalent generic N3 knockback

Automation:
- V038 FULL REGRESSION PASS
- N3 SERVER 57/57 PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- FINAL PASS

Samsung Browser closure smoke also PASS.

---

# Major direction correction after v0.39

Do **not** continue porting legacy Stage 4 -> Stage 10 encounter recipes as the production campaign.

The intended campaign direction is a broader approximately 50-stage structure with:
- tier identities,
- S / E / X pressure grammar,
- 2/3/4-player encounter scaling,
- re-authored monster combinations,
- later deterministic simulation/calibration.

The branch `timing-defense-cloudflare-v040-stage4-shield` was created during Stage 4 preflight but is now **preflight-only / not an approved production direction**. Do not continue that branch as a legacy Stage 4 reconstruction without a new explicit decision.

---

# Monster Capability Contract V1 — STRUCTURE FROZEN

Canonical document:
`MONSTER_CAPABILITY_CONTRACT_V1.md`

Nine ordinary archetypes:
1. GRUNT — baseline/reference
2. RUNNER — sustained high-speed pressure
3. BRUTE — raw durability + knock resistance
4. SHIELD — armor mitigation
5. FLYER — authoritative Y/spatial geometry
6. CHARGER — telegraphed interruptible burst dash
7. SPLITTER — death creates exactly two non-recursive children
8. SUPPORTER — non-stacking nearby movement-speed aura only
9. SIEGER — standoff, telegraph, repeated ranged wall attacks

Bosses are a separate capability-composition layer.

Important global constraints:
- no hard class lockouts,
- no manual target selection introduced as a monster feature,
- all gameplay-relevant monster state server-authoritative,
- exceptional actions must be telegraphed,
- SPLITTER children never split again,
- SUPPORTER V1 aura does not stack and does not heal/armor/damage/knock-buff,
- production monster numbers are NOT frozen yet.

Legacy values may only be used as provisional/reference anchors for capability testing until final production calibration explicitly approves them.

---

# Active next boundary — Monster Capability Layer

Do not bind capability implementation to Stage 4/5/etc.

First create a deterministic stage-number-independent capability sandbox/harness.

Recommended implementation order:
1. SHIELD / common armor layer
2. FLYER / authoritative Y geometry
3. CHARGER state machine
4. SPLITTER child-spawn kernel
5. SUPPORTER dynamic movement-speed aura
6. SIEGER repeated wall-attack kernel

Any temporary HP/speed/armor/reward/ability timings used to make the sandbox executable must be explicitly marked:
**PROVISIONAL — NOT BALANCE FROZEN**.

Required compatibility for each capability:
- human ordinary hit,
- passive,
- AI,
- Lv6 secondary where applicable,
- N3,
- kill/reward/contribution,
- event stream/reconnect,
- client presentation.

After capability completion:
1. implement remaining player-skill authority needed for calibration,
2. build the real approximately 50-stage tier/S-E-X authoring model,
3. simulate candidate recipes at scale,
4. classify pressure/density/role issues,
5. discuss before numerical patches,
6. explicitly freeze production monster/stage values,
7. use Samsung Browser only for presentation/input/readability gates automation cannot judge.

## Validation policy
Default:
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`.

Automatable validation must not be delegated to the user unless CI cannot execute the gate.

## AI FILL semantic
Configured AI filler positions remain fixed occupied positions. Humans do not dynamically displace them.

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred as one shared responsive layer.

## Governance
No numerical change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
