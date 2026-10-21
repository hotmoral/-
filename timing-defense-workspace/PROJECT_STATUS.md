# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
User approved a change in recovery strategy after the Render monthly-quota suspension.

Primary architecture is now:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Canonical decision:
- `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`

PoC closure evidence:
- `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`

Experimental implementation:
- branch: `timing-defense-cloudflare-do-poc`
- directory: `timing-defense-cloudflare-poc/`
- public PoC: `https://timing-defense-do-poc.sktjsek.workers.dev`

The production/live source branch remains intentionally untouched by the PoC.

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / status / handoff branch: `timing-defense-workspace`
- Last verified live source HEAD before this architecture migration: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`
- Latest implemented game prototype: **v0.35**
- Last Android + PC device-validated production multiplayer baseline: **v0.34**

## Render incident remains classified
Old Render services:
- static `srv-dbb1c9mi0phs73b5bao0`
- multiplayer backend `srv-dbbimre1egvs73861d80`

Both were suspended on 2026-10-20 around 12:39 UTC with actor/reason **Monthly Quota Exceeded** after successful v0.35 deployments.

Therefore the old public URL failure remains a hosting outage, not evidence of a v0.35 gameplay/runtime regression.

The previously prepared portable full-stack Node wrapper remains available as a fallback artifact but is no longer the primary execution path.

---

# Validated multiplayer foundation

## v0.31 / v0.32 — device validated
- real FRIEND/LINK room create/join,
- nickname/class/slot sharing,
- READY propagation,
- host-only START after all humans READY,
- synchronized start gate,
- Samsung Browser short-landscape waiting-room clipping fix.

## v0.33 — device validated
- authoritative shared Stage 1,
- server-owned enemy/base state,
- server-resolved human timing attacks,
- remote PC attack reducing the same monster HP on Android.

## v0.34 — device validated
- Android monster movement smoothing,
- remote player projectile VFX,
- server authority preserved.

This remains the stable production behavior baseline.

## v0.35 — implemented, not device-PASS
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

# Cloudflare Durable Objects PoC — PASS

Status: **public two-client device PASS / architecture viability established**.

Validated on the public Workers deployment:
- root/static assets,
- `/api/health`,
- one SQLite-backed Durable Object per room,
- WebSocket Hibernation transport,
- `apac-ne` placement hint,
- six-character room creation,
- two independent clients in one room,
- shared host/participant state,
- READY propagation,
- host START,
- one authoritative diagnostic monster,
- shared HP `300 -> 200 -> 100 -> 0`,
- synchronized `CLEAR`,
- refresh/reconnect preserving shared room/session/slot/state,
- post-refresh continued interaction,
- event-driven execution without the legacy 50 ms always-on loop.

This PASS validates architecture only. It does **not** claim v0.35 Cloudflare parity.

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
The PoC gate is closed. Do not keep expanding the diagnostic PoC.

Next migration slice:
1. port the existing v0.31 authoritative room/session/slot/host/READY/START contract onto Durable Object + WebSocket,
2. preserve existing FRIEND/LINK waiting-room behavior and v0.32 Samsung Browser layout fixes,
3. preserve class/nickname/slot semantics,
4. preserve all-human READY and host-only START behavior,
5. preserve synchronized future start semantics rather than replacing them with a local instant start,
6. validate Android + PC waiting-room parity on the Cloudflare deployment,
7. fix only reproducible migration defects,
8. only after that slice PASS, port v0.33 authoritative Stage 1 consequences,
9. replace continuous server position ticking with event/time-derived state where safe,
10. preserve v0.34 interpolation/projectile presentation,
11. then port v0.35 recovery/shop/Stage 2,
12. only after Cloudflare v0.35 parity is device-PASS proceed to Stage 3–10 and Lv6+ authority.

## Current truth boundary
Safe claims:
- v0.34 Android + PC authoritative Stage 1 is device-PASS.
- v0.34 smoothing and remote projectile VFX are device-PASS.
- v0.35 reconnect/shop/Stage-2 code exists and passed local API/integration checks.
- Render outage is a hosting quota suspension, not proven gameplay regression.
- Cloudflare Workers + Durable Objects isolated multiplayer PoC is public two-client device-PASS including refresh/reconnect.

Do not claim:
- v0.35 Cloudflare parity,
- Stage 3–10 multiplayer,
- complete Lv6+ multiplayer skill authority,
- final production persistence/security/shop/shared-wall semantics,
- final numerical balance.
