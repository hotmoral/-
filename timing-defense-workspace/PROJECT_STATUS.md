# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- Cloudflare watched branch: `timing-defense-cloudflare-do-poc`
- exact validated v0.35 HEAD: `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- validated health version: `0.35-cf.7`

Closed Cloudflare validation gates:
1. isolated Durable Objects viability PoC — **PASS**
2. real-game v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**

Preserved migration checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 Stage 1 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 render PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 cf.3 Stage 2 flow PASS: `timing-defense-cloudflare-v035-cf3-stage2-flow-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`

Read:
- `CLOUDFLARE_V035_PASS_2026-10-21.md`
- `CLOUDFLARE_V034_RENDER_PASS_2026-10-21.md`
- `CLOUDFLARE_V033_STAGE1_PASS_2026-10-21.md`
- `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`
- `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`

## Legacy baseline
- Repository: `hotmoral/-`
- live source branch: `timing-defense-live-v011`
- planning/status branch: `timing-defense-workspace`
- latest implemented legacy prototype: **v0.35**
- last Android + PC device-PASS legacy prototype before migration: **v0.34**
- last verified legacy live HEAD before migration: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`

Legacy v0.35 passed local/API integration for reconnect, Team Shop and Stage 2, but could not receive Render device validation because both Render services were suspended for Monthly Quota Exceeded. That outage remains hosting-related, not gameplay-regression evidence.

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
- same EXP / charge,
- shared Stage 1 clear,
- no duplicate local spawn/wall-damage authority observed.

## v0.34 render parity — PASS
Validated Android + PC:
- remote human projectile visible,
- local projectile immediate visual impact,
- server HP/EXP/coin/kills authority retained,
- no duplicate presentation damage,
- monster smoothing acceptable.

## v0.35 — PASS
Validated Android + PC through cf.7:
- Stage 1 -> shared Team Shop,
- authoritative purchase / coin / rank flow,
- immediate `처리중…` feedback with duplicate-tap blocking while server authority remains intact,
- both-human shop READY gate,
- host NEXT STAGE,
- synchronized Stage 2 transition,
- `STAGE 2 / READY / START` presentation,
- Timing Square and direct timing input active,
- authoritative Stage 2 GRUNT/RUNNER combat,
- bounded Stage 2 clear,
- authoritative result board with actual human/AI participants and populated KILLS / DMG / KILL COIN / LV / MAX COMBO,
- required reconnect gate user-confirmed PASS,
- Rogue CHARGE no longer leaks Knight/yellow palette or the reported flicker,
- remote human timing attacks now use the normal class timing-projectile visual family rather than the passive/automatic-shot visual family.

No numerical balance values were intentionally changed during the v0.35 closure work.

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
**Cloudflare v0.35 is closed. Do not reopen it without a regression.**

Next work must begin as a separately scoped preflight for:
1. Stage 3–10 multiplayer generalization,
2. larger-party validation,
3. Lv6+ multiplayer skill consequence authority.

Before implementation, inspect existing stage-plan and skill contracts and define which consequences remain presentation-only vs require Durable Object authority. Do not make numerical balance changes as part of migration/generalization.

Deferred UX item:
- heterogeneous phone-size/aspect-ratio responsive safety should later be reviewed as a shared responsive-safety layer rather than per-device one-off patches.

## Current truth boundary
Safe claims:
- Cloudflare PoC through v0.35 are public/device-PASS for their scoped gates,
- v0.35 exact validated deployment is preserved,
- Render quota incident is confirmed.

Do not claim yet:
- Stage 3–10 multiplayer parity,
- complete Lv6+ multiplayer skill authority,
- final production persistence/security/anti-cheat architecture,
- final shop/shared-wall semantics beyond the validated v0.35 slice,
- final numerical balance.
