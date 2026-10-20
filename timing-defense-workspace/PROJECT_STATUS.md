# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
User approved a change in recovery strategy after the Render monthly-quota suspension.

Primary next lane is now:
**Cloudflare Workers + Durable Objects event-driven multiplayer PoC.**

Canonical decision:
- `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`

Experimental implementation:
- branch: `timing-defense-cloudflare-do-poc`
- directory: `timing-defense-cloudflare-poc/`

The production/live source branch is intentionally untouched by this PoC.

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / status / handoff branch: `timing-defense-workspace`
- Last verified live source HEAD before this architecture PoC: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`
- Latest implemented game prototype: **v0.35**
- Last Android + PC device-validated multiplayer baseline: **v0.34**

## Render incident remains classified
Old Render services:
- static `srv-dbb1c9mi0phs73b5bao0`
- multiplayer backend `srv-dbbimre1egvs73861d80`

Both were suspended on 2026-10-20 around 12:39 UTC with actor/reason **Monthly Quota Exceeded** after successful v0.35 deployments.

Therefore the old public URL failure remains a hosting outage, not evidence of a v0.35 gameplay/runtime regression.

The previously prepared portable full-stack Node wrapper remains available as a fallback artifact but is no longer the primary next execution path.

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

This remains the stable public behavior baseline.

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

Android + PC validation did not complete because Render suspended both services.

---

# Cloudflare Durable Objects PoC status

The new PoC is deliberately smaller than v0.35.

Current implemented experimental contract:
- one Durable Object per six-character room code,
- SQLite-backed object state,
- WebSocket Hibernation API,
- `apac-ne` location hint,
- static test frontend served through Workers Static Assets,
- room creation,
- up to four participants,
- session/slot identity,
- reconnect replacement ownership guard,
- READY synchronization,
- host-only START,
- one authoritative diagnostic monster,
- fixed diagnostic attack events and shared HP,
- event-driven execution with no 50 ms simulation loop.

PoC constants are diagnostic-only and must not be interpreted as production balance values.

Current PoC truth boundary:
- source implementation exists,
- public Cloudflare deployment has not yet been validated,
- Android + PC public PoC PASS has not yet been established.

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
1. Validate/deploy the isolated Durable Objects PoC without touching live v0.35.
2. Smoke-test health/static/WebSocket/room flow.
3. Android + PC prove same room -> READY -> host START -> same monster -> cross-client HP synchronization.
4. Refresh/reconnect one client and verify active connection ownership remains correct.
5. If PoC PASS, port v0.31 room/READY/START semantics.
6. Then port v0.33 authoritative Stage 1 consequences while replacing always-on position ticking with event/time-derived state where safe.
7. Preserve v0.34 interpolation/projectile rendering.
8. Then port v0.35 recovery/shop/Stage 2.
9. Only after Cloudflare v0.35 parity is device-PASS proceed to Stage 3–10 and Lv6+ multiplayer authority.

## Do not claim yet
- public Cloudflare PoC PASS,
- v0.35 Cloudflare device PASS,
- Stage 3–10 multiplayer,
- full Lv6+ multiplayer skill authority,
- final persistence/security/shop/shared-wall semantics,
- final numerical balance.
