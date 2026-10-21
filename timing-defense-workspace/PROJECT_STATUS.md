# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- Cloudflare watched branch: `timing-defense-cloudflare-do-poc`

Closed Cloudflare validation gates:
1. isolated Durable Objects viability PoC — **PASS**
2. real-game v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**

Read:
- `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`
- `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`
- `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`
- `CLOUDFLARE_V033_STAGE1_PASS_2026-10-21.md`
- `CLOUDFLARE_V034_RENDER_PASS_2026-10-21.md`
- `V035_CF3_STAGE2_FLOW_PASS_CF4_RESULT_CANDIDATE_2026-10-21.md`

Preserved migration checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 Stage 1 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 render PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 cf.3 Stage 2 flow PASS checkpoint: `timing-defense-cloudflare-v035-cf3-stage2-flow-pass-20261021`

## Legacy baseline
- Repository: `hotmoral/-`
- live source branch: `timing-defense-live-v011`
- planning/status branch: `timing-defense-workspace`
- latest implemented legacy prototype: **v0.35**
- last Android + PC device-PASS legacy prototype: **v0.34**
- last verified legacy live HEAD before migration: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`

Legacy v0.35 exists and passed local/API integration checks for reconnect, Team Shop and Stage 2, but was not device-PASS because Render suspended both services for **Monthly Quota Exceeded**. That outage remains hosting-related, not evidence of a gameplay regression.

---

# Cloudflare migration truth

## v0.31/v0.32 — PASS
Validated Android + PC:
- FRIEND invite room create/join,
- nickname/class/slot/AI FILL,
- READY and READY-cancel propagation,
- all-human READY gate,
- non-host START blocked,
- host-only START,
- shared future start gate,
- WAITING refresh/reconnect preserving room/session/slot/host,
- Samsung Browser short-landscape layout retained.

## v0.33 Stage 1 — PASS
Validated Android + PC:
- same authoritative Stage 1 world,
- same monster HP/deaths,
- cross-device attacks affect the same monster state,
- same BASE HP,
- same EXP / charge state,
- shared Stage 1 clear,
- no duplicate local spawn/wall-damage authority observed.

## v0.34 render parity — PASS
Validated Android + PC:
- v0.33 authoritative state remained synchronized,
- remote human projectile VFX is visible,
- local projectile arrival produces immediate hit response,
- no duplicate local gameplay damage observed,
- server authority for HP / EXP / coin / kills remains unchanged,
- monster presentation is acceptably smooth.

## v0.35 — PARTIAL PASS, cf.4 result candidate under validation
Confirmed on Android + PC through cf.3:
- Stage 1 -> shared Team Shop,
- purchase / coin / rank flow,
- both-human shop READY,
- host NEXT STAGE,
- synchronized Stage 2 start,
- `STAGE 2 / READY / START` presentation,
- Timing Square active on both clients,
- direct tap attacks active,
- remote projectile VFX retained,
- Stage 2 bounded clear reached on both clients.

cf.3 remaining defect:
- inherited local result board displayed `STAGE 10 CLEAR`,
- result metrics could differ across clients because they came from per-device local presentation state.

cf.4 candidate:
- health version `0.35-cf.4`,
- deployment trigger HEAD `ce0151894d2a972863bd511ed95a04b808fef941`,
- human contribution values come from authoritative `run.players`,
- AI damage/kills are accumulated server-side and exposed in the public run snapshot,
- result title uses the authoritative current stage,
- no combat-balance values changed.

---

# Frozen combat / balance governance
- Rhythm: `X -> X -> X -> X+Y`.
- Knight = stable generalist / penetration / strong heavy.
- Rogue = multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank = knockback / wall protection / team specialist.
- Archer = strict straight-line trajectory; no seeking/bending.
- Mage = density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP only from valid timing events; passive attacks grant no EXP.
- Current combo display/size/position/animation remains approved and frozen unless explicitly requested.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`,
- ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` cap.

Numerical change workflow remains:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> numerical patch/freeze`.

---

# Immediate next boundary
**Finish Cloudflare v0.35 device validation.**

Remaining gates:
1. cf.4 result board: both clients show `STAGE 2 CLEAR` and identical authoritative contribution values,
2. reconnect in Stage 1,
3. reconnect in Team Shop,
4. reconnect in Stage 2,
5. no historical projectile burst after resume.

Only after those gates pass may v0.35 be closed and migration proceed to Stage 3–10, larger-party validation and Lv6+ multiplayer authority.

## Current truth boundary
Safe claims:
- Cloudflare PoC is public two-client device-PASS,
- Cloudflare v0.31/v0.32 waiting-room parity is device-PASS,
- Cloudflare v0.33 authoritative Stage 1 parity is device-PASS,
- Cloudflare v0.34 render smoothing / remote projectile parity is device-PASS,
- Cloudflare v0.35 cf.3 Stage 2 transition/combat/clear flow is device-confirmed,
- cf.4 authoritative result-board candidate is deployed for validation,
- Render quota incident is confirmed.

Do not claim:
- full Cloudflare v0.35 parity PASS yet,
- Stage 3–10 multiplayer,
- complete Lv6+ multiplayer skill authority,
- final persistence/security/shop/shared-wall semantics,
- final numerical balance.
