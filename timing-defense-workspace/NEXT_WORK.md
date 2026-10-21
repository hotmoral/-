# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Architecture gate status
The isolated Cloudflare Workers + Durable Objects viability PoC is now **PASS**.

Read before execution:
1. `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`
2. `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`
3. `PROJECT_STATUS.md`

Public PoC:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Validated PoC properties:
- public Worker/static route,
- SQLite-backed Durable Object room,
- WebSocket Hibernation,
- `apac-ne` location hint,
- two independent clients,
- READY synchronization,
- host START,
- shared authoritative monster HP,
- `CLEAR`,
- refresh/reconnect preserving shared state,
- event-driven execution without the legacy 50 ms always-on loop.

The portable Node host remains a fallback artifact only.

## Current production baseline
- Latest implemented game prototype: **v0.35**.
- Last Android + PC device-PASS production multiplayer baseline: **v0.34**.
- Render static/backend services remain suspended for **Monthly Quota Exceeded**.
- Live source branch remains `timing-defense-live-v011` at the last verified HEAD `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a` unless later verification proves otherwise.
- The PoC branch is `timing-defense-cloudflare-do-poc`.
- The PoC is isolated and has not modified production balance/gameplay values.

## Balance / UI guard
Do not numerically patch or production-freeze attack damage, monster HP, passive interval, combo coefficients, EXP, shop costs, knockback, stage count/gaps or class balance during this architecture migration.

Required numerical workflow remains:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> numerical patch/freeze`.

Current combo display/size/position/animation remains approved and frozen unless explicitly requested.

---

# Immediate execution group — v0.31 room/READY/START parity migration

Do not add Stage 1 combat yet.

## A. Source-of-truth recovery before implementation
Read the existing v0.31/v0.32 production implementation and reports directly from `timing-defense-live-v011` / workspace before writing the migration.

Recover exact existing semantics for:
- FRIEND/LINK room creation and joining,
- nickname/class selection,
- slot allocation,
- host identity,
- READY propagation,
- all-human READY gate,
- host-only START,
- shared future start time / RUN STARTING state,
- invite/link behavior,
- waiting-room UI behavior,
- v0.32 Samsung Browser short-landscape fixes.

Do not infer these from memory if repository code differs.

## B. Migration implementation boundary
Port only the waiting-room/session contract onto Cloudflare Durable Object + WebSocket transport.

Server/DO owns:
- room identity,
- session identity,
- slot,
- host,
- participant nickname/class,
- READY state,
- start eligibility,
- shared authoritative future start time.

Client owns:
- waiting-room presentation,
- local form input before authoritative acceptance,
- rendering of participant/READY/START state.

Preserve:
- existing v0.31 behavior,
- v0.32 layout fix,
- no balance changes,
- no combat migration in this slice.

## C. Public device validation gate
Android + PC must validate:
1. FRIEND/LINK create/join equivalent behavior,
2. both clients see identical participant/slot/class/nickname state,
3. READY propagates both ways,
4. READY cancel propagates,
5. non-host cannot START,
6. host cannot START before all humans READY,
7. host START after all READY creates one shared future start time,
8. both clients enter the same starting/running boundary,
9. refresh/reconnect in waiting state preserves the same session/slot/room,
10. disconnect/reconnect does not corrupt host/online ownership,
11. v0.32 short-landscape waiting-room behavior remains usable on Samsung Browser.

## D. Closure rule
This slice closes only when:
- public Cloudflare deployment succeeds,
- Android + PC waiting-room parity is device-PASS,
- reproducible migration defects are fixed,
- canonical docs are synchronized.

A PASS authorizes the next slice only: v0.33 authoritative Stage 1 migration.

---

# Following migration slice — only after v0.31/v0.32 parity PASS

Port v0.33 Stage 1 authoritative consequences:
- shared run id/seed/start state,
- enemy spawn identity,
- authoritative HP/death,
- BASE HP,
- human timing actions,
- passive/AI consequences,
- EXP/LV/coin/charge/combo candidate state.

Architecture requirement:
- avoid reproducing the legacy 50 ms always-on position integration where event/time-derived authoritative state is sufficient,
- preserve server authority,
- preserve v0.34 interpolation/extrapolation and remote projectile VFX as presentation-only behavior.

Then validate Android + PC Stage 1 parity before porting v0.35.

---

# v0.35 parity migration — only after Stage 1 parity PASS

Port:
- production reconnect/session recovery semantics,
- Stage 1 -> Team Shop,
- authoritative coin/ranks/purchase validation,
- shop READY,
- all-human READY gate,
- host-only NEXT,
- synchronized Stage 2 GRUNT/RUNNER combat,
- bounded Stage 2 clear.

Then device-test through Stage 2 and reconnect.

---

# Following game implementation — only after Cloudflare v0.35 parity PASS

1. Generalize the authoritative stage/shop state machine through Stage 10.
2. Add GRUNT / RUNNER / BRUTE / SHIELD / FLYER plus Stage 5/10 bosses.
3. Validate DUO / TRIPLE / FULL room/shop/READY/NEXT behavior.
4. Move Lv6/Lv11/Lv16/Lv21 multiplayer skill consequences under server authority.
5. Strengthen revision/desync diagnostics and reconciliation.
6. Decide durable room lifetime, cleanup and invite-token policy.
7. Implement Lv26/Lv31 only after networking stabilizes.
8. Rerun Solo/2P/3P/4P simulations before numerical freeze.

## Current truth boundary
Safe claims:
- v0.34 Android + PC authoritative Stage 1 is device-PASS.
- v0.34 smoothing and remote projectile VFX are device-PASS.
- v0.35 reconnect/shop/Stage-2 code exists and passed local API/integration checks.
- Render outage is a hosting quota suspension, not proven gameplay regression.
- Cloudflare Workers + Durable Objects isolated PoC is public two-client device-PASS, including refresh/reconnect.

Do not claim:
- v0.31 production parity on Cloudflare yet,
- v0.35 Cloudflare parity,
- Stage 3–10 multiplayer,
- complete Lv6+ multiplayer skill authority,
- final production persistence/security/balance semantics.
