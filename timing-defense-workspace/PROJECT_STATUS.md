# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
Primary architecture is now:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Canonical decision:
- `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`

Closed validation gates:
- `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`
- `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`

Public Cloudflare deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Cloudflare deployment pointer:
- branch: `timing-defense-cloudflare-do-poc`
- validated v0.31/v0.32 parity deployment pointer HEAD: `e6db85f22f04b2566960c98867c19cebf8fc1a4b`

Preserved architecture PoC checkpoint:
- branch: `timing-defense-cloudflare-do-poc-pass-20261021`

Dedicated v0.31/v0.32 implementation branch:
- `timing-defense-cloudflare-v031-parity`

The production/live source branch remains intentionally separate from the Cloudflare migration lane.

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / status / handoff branch: `timing-defense-workspace`
- Last verified live source HEAD before this architecture migration: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`
- Latest implemented game prototype: **v0.35**
- Last Android + PC device-validated legacy production multiplayer baseline: **v0.34**

## Render incident remains classified
Old Render services:
- static `srv-dbb1c9mi0phs73b5bao0`
- multiplayer backend `srv-dbbimre1egvs73861d80`

Both were suspended on 2026-10-20 around 12:39 UTC with actor/reason **Monthly Quota Exceeded** after successful v0.35 deployments.

Therefore the old public URL failure remains a hosting outage, not evidence of a v0.35 gameplay/runtime regression.

The previously prepared portable full-stack Node wrapper remains available as a fallback artifact but is no longer the primary execution path.

---

# Validated multiplayer foundation

## Legacy v0.31 / v0.32 — device validated
- real FRIEND/LINK room create/join,
- nickname/class/slot sharing,
- READY propagation,
- host-only START after all humans READY,
- synchronized start gate,
- Samsung Browser short-landscape waiting-room clipping fix.

## Legacy v0.33 — device validated
- authoritative shared Stage 1,
- server-owned enemy/base state,
- server-resolved human timing attacks,
- remote PC attack reducing the same monster HP on Android.

## Legacy v0.34 — device validated
- Android monster movement smoothing,
- remote player projectile VFX,
- server authority preserved.

## Legacy v0.35 — implemented, not device-PASS
Implemented and locally API/integration checked:
- same-server session/reload recovery,
- authoritative Stage 1 -> Team Shop,
- per-human server-owned coin/ranks/purchases,
- shop READY synchronization,
- all-human READY gate,
- host-only NEXT STAGE,
- synchronized Stage 2 GRUNT/RUNNER combat,
- Stage 2 bounded `stage2-clear` endpoint.

Android + PC v0.35 validation did not complete because Render suspended both services.

---

# Cloudflare migration validation

## Durable Objects viability PoC — PASS
Validated publicly with two independent clients:
- Worker/static assets,
- `/api/health`,
- one SQLite-backed Durable Object per room,
- WebSocket Hibernation,
- `apac-ne` placement hint,
- shared authoritative diagnostic state,
- refresh/reconnect preserving room/session/slot/state,
- event-driven execution without the legacy 50 ms always-on loop.

This PASS established architecture viability only.

## v0.31 / v0.32 Cloudflare parity — PASS
Status: **public Android + PC device PASS**.

Validated on the real game lobby/waiting-room UI:
- FRIEND room creation and invite join,
- nickname/class/slot parity,
- authoritative AI FILL reservation,
- READY propagation both ways,
- READY cancel propagation,
- all-human READY gate,
- non-host START unavailable,
- host-only START,
- one shared future `startAt`,
- synchronized `RUN GATE OPEN` boundary,
- WAITING refresh/reconnect preserving the same room/session/slot,
- host refresh preserving host ownership,
- other client remaining online,
- Samsung Browser short-landscape layout remaining usable without the old clipping regression.

Read:
- `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`

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
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Numerical findings require report/discussion/explicit decision before patching.
- Current combo display/size/position/animation remains approved and frozen unless explicitly requested.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`,
- ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` cap.

Approved radar axes: 공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

---

# Immediate next boundary
The v0.31/v0.32 Cloudflare parity gate is closed.

Next migration slice: **v0.33 authoritative Stage 1**.

Required migration scope:
1. recover the exact existing v0.33 authoritative combat contract from live code and canonical report,
2. add shared authoritative run id / seed / start state to the Durable Object room,
3. port Stage 1 spawn identity and schedule,
4. port authoritative monster HP/death and BASE HP,
5. port human timing-result actions with monotonic action sequence protection,
6. port passive and AI attack consequences,
7. port EXP / LV / coin / charge / combo candidate state owned by server authority,
8. preserve the established v0.31/v0.32 room/session/slot/host/READY/START behavior,
9. avoid recreating the legacy 50 ms always-on position loop where event/time-derived authoritative movement state is sufficient,
10. validate Android + PC against the legacy v0.33 behavior contract,
11. only after Stage 1 parity PASS, port v0.34 smoothing/extrapolation and remote projectile presentation,
12. only after that, port v0.35 reconnect/shop/Stage 2.

No numerical combat balance changes are authorized in this migration slice.

## Current truth boundary
Safe claims:
- legacy v0.34 Android + PC authoritative Stage 1 is device-PASS,
- legacy v0.34 smoothing and remote projectile VFX are device-PASS,
- legacy v0.35 reconnect/shop/Stage-2 code exists and passed local API/integration checks,
- Render outage is a hosting quota suspension, not proven gameplay regression,
- Cloudflare Workers + Durable Objects isolated multiplayer PoC is public two-client device-PASS,
- Cloudflare v0.31/v0.32 waiting-room parity is public Android + PC device-PASS including READY cancel, host-only START, synchronized start gate and WAITING refresh/reconnect.

Do not claim:
- Cloudflare v0.33 Stage 1 combat parity yet,
- Cloudflare v0.34 smoothing/projectile parity yet,
- Cloudflare v0.35 parity,
- Stage 3–10 multiplayer,
- complete Lv6+ multiplayer skill authority,
- final production persistence/security/shop/shared-wall semantics,
- final numerical balance.
