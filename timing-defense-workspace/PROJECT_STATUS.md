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

Validated v0.34 deployment:
- implementation branch: `timing-defense-cloudflare-v034-render`
- implementation commit: `c78765b2c29b1ab0812e64c6de7a8ca3b379c2cc`
- deployment trigger HEAD: `adc6709d51e9b076498c7c26e172478d24d9f797`
- preserved checkpoint: `timing-defense-cloudflare-v034-pass-20261021`

Preserved migration checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 Stage 1 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 render PASS: `timing-defense-cloudflare-v034-pass-20261021`

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
**Cloudflare v0.35 reconnect / Team Shop / Stage 2 parity migration.**

Required scope:
1. preserve v0.31-v0.34 validated behavior,
2. port same-session/reload recovery,
3. port Stage 1 -> Team Shop transition,
4. port authoritative coin / ranks / purchases,
5. port purchase READY lock/unlock,
6. port all-human shop READY gate,
7. port host-only NEXT STAGE,
8. port synchronized future Stage 2 start,
9. port Stage 2 authoritative GRUNT/RUNNER combat,
10. port bounded Stage 2 clear,
11. validate reconnect in Stage 1 / Team Shop / Stage 2,
12. make no numerical balance changes.

Only after v0.35 device PASS may migration proceed to Stage 3–10, larger party validation and Lv6+ multiplayer authority.

## Current truth boundary
Safe claims:
- Cloudflare PoC is public two-client device-PASS,
- Cloudflare v0.31/v0.32 waiting-room parity is device-PASS,
- Cloudflare v0.33 authoritative Stage 1 parity is device-PASS,
- Cloudflare v0.34 render smoothing / remote projectile parity is device-PASS,
- legacy v0.35 reconnect/shop/Stage-2 code exists and passed local/API integration checks,
- Render quota incident is confirmed.

Do not claim:
- Cloudflare v0.35 parity yet,
- Stage 3–10 multiplayer,
- complete Lv6+ multiplayer skill authority,
- final persistence/security/shop/shared-wall semantics,
- final numerical balance.
