# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- Cloudflare watched branch: `timing-defense-cloudflare-do-poc`
- current watched HEAD: `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- candidate health version: `0.35-cf.7`

Closed Cloudflare validation gates:
1. isolated Durable Objects viability PoC — **PASS**
2. real-game v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**

Preserved migration checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 Stage 1 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 render PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 cf.3 Stage 2 flow PASS: `timing-defense-cloudflare-v035-cf3-stage2-flow-pass-20261021`

## Legacy baseline
- Repository: `hotmoral/-`
- live source branch: `timing-defense-live-v011`
- planning/status branch: `timing-defense-workspace`
- latest implemented legacy prototype: **v0.35**
- last Android + PC device-PASS legacy prototype: **v0.34**
- last verified legacy live HEAD before migration: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`

Legacy v0.35 passed local/API integration for reconnect, Team Shop and Stage 2, but was not device-PASS on Render because both services were suspended for Monthly Quota Exceeded. That outage remains hosting-related, not gameplay-regression evidence.

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
- cross-device attacks affect same monster state,
- same BASE HP,
- same EXP / charge,
- shared Stage 1 clear,
- no duplicate local spawn/wall-damage authority observed.

## v0.34 render parity — PASS
Validated Android + PC:
- remote human projectile visible,
- local projectile immediate visual impact,
- server HP/EXP/coin/kills authority retained,
- monster smoothing acceptable.

## v0.35 — DEVICE VALIDATION PARTIAL PASS / cf.7 visual candidate
Confirmed on Android + PC:
- Stage 1 -> shared Team Shop,
- shop purchase and authoritative rank/coin update,
- purchase button immediate `처리중…` feedback and duplicate-tap blocking — **PASS**,
- both-human shop READY,
- host NEXT STAGE,
- synchronized Stage 2 transition,
- `STAGE 2 / READY / START` presentation,
- Timing Square and direct tap attacks active,
- remote projectile visibility,
- bounded Stage 2 clear,
- authoritative Stage 2 result board with real human/AI participants and populated KILLS / DMG / KILL COIN / LV / MAX COMBO — **PASS on supplied recording**,
- reconnect validated by user — **PASS**.

Remaining visual defects identified from cf.6 recording:
1. Rogue Timing Square CHARGE intermittently leaked Knight/yellow palette and flickered.
   - root cause: inherited v0.24 Rogue Timing Square wrapper temporarily set `S.playerClass='knight'` while drawing the base square.
2. Remote human timing attacks used the same simplified remote projectile renderer as passive/automatic attacks.
   - required contract: human timing attack projectile should use the same class/tier visual language whether local or remote; passive/automatic attack may remain visually distinct.

cf.7 candidate fixes exactly these two presentation defects. No combat-balance coefficients or server authority were changed.

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
**Validate cf.7 visual parity only.**

Required short multiplayer test:
1. Rogue local player: CHARGE dots/text/square must not leak yellow Knight palette or flicker incorrectly.
2. Remote human timing attacks must visually match the normal class timing projectile family rather than passive/automatic shot visuals.

Already closed; do not retest unless regression appears:
- Team Shop pending UX,
- reconnect,
- Stage 2 transition/input,
- Stage 2 result board.

If cf.7 passes, close Cloudflare v0.35, create preserved v0.35 PASS checkpoint, sync status/handoff, then proceed to the next migration boundary. Do not start Stage 3–10 or numerical changes before closure.

## Current truth boundary
Safe claims:
- Cloudflare PoC, v0.31/v0.32, v0.33 and v0.34 are device-PASS,
- v0.35 Stage 1/shop/Stage 2/clear/result/reconnect core flow is device-confirmed,
- cf.7 visual parity patch is deployed for device validation.

Do not claim:
- full Cloudflare v0.35 PASS until cf.7 visual checks pass,
- Stage 3–10 multiplayer,
- complete Lv6+ multiplayer skill authority,
- final persistence/security/shop/shared-wall semantics,
- final numerical balance.
