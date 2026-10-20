# Timing Defense — Cloudflare Durable Objects Migration Decision

Date: 2026-10-21 KST
Status: APPROVED DIRECTION / PoC FIRST

## Decision
Do not continue treating replacement always-on Node hosting as the primary recovery path for the Render quota outage.

The approved next architecture is a Cloudflare Workers + Durable Objects proof of concept, with the long-term goal of replacing the always-on authoritative Node process with room-scoped event-driven authoritative objects.

This decision does **not** invalidate the v0.34 or v0.35 gameplay/network work. It changes the hosting/execution model first.

## Frozen baselines preserved
- v0.34 remains the last Android + PC device-PASS multiplayer baseline.
- v0.35 remains implemented and locally API/integration validated but not device-PASS.
- No combat/balance coefficient is changed by this architecture decision.
- Current combo presentation remains frozen unless explicitly requested.
- Existing Render outage remains classified as hosting quota suspension, not proven v0.35 code regression.

## Experimental implementation branch
- Branch: `timing-defense-cloudflare-do-poc`
- Base: live HEAD `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`
- Directory: `timing-defense-cloudflare-poc/`

The existing `timing-defense-live-v011` branch is not modified by the PoC.

## PoC slice
The first public Cloudflare validation must prove only:
1. create an authoritative room,
2. connect two independent clients,
3. synchronize READY,
4. enforce host-only START,
5. create one server-authoritative test monster,
6. accept an authoritative attack from either client,
7. broadcast the same monster HP to both clients,
8. reconnect the same stored session without corrupting connection ownership.

PoC test constants such as 300 monster HP / 100 attack damage are diagnostic-only and are **not** Timing Defense balance changes.

## Target architecture
- Static frontend: Cloudflare Workers Static Assets.
- Room authority: one SQLite-backed Durable Object per room code.
- Transport: WebSocket Hibernation API.
- Placement hint for the current Korea-centered test group: `apac-ne`.
- Execution model: event-driven; do not reproduce the existing 50 ms always-on server loop in the final architecture.

## Why this path
The current authoritative state model is room-scoped and therefore maps naturally to one Durable Object per game room. WebSocket Hibernation allows connections to remain established while the object can hibernate during idle periods. The architecture removes dependence on a continuously running free Node instance and its monthly runtime quota.

## Migration order after PoC PASS
1. Port v0.31 room/session/READY/START contract.
2. Port v0.33 authoritative Stage 1 combat consequences.
3. Preserve v0.34 client interpolation and remote projectile rendering as presentation-only behavior.
4. Port v0.35 session recovery and Team Shop contract.
5. Port synchronized Stage 2.
6. Device-test Android + PC through Stage 2 and reconnect.
7. Only after parity PASS, retire the old Node-host recovery lane and continue Stage 3–10 authority work.

## Explicit non-goals before PoC PASS
Do not:
- modify `timing-defense-live-v011`,
- rebalance attacks/monster HP/passive/combo/shop costs,
- implement Stage 3–10 on the new backend,
- port Lv6+ multiplayer skill authority,
- declare v0.35 Cloudflare device-PASS,
- delete the existing Node server implementation.

## Promotion gate
The architecture is promoted beyond PoC only after a public Cloudflare URL is reachable and Android + PC independently demonstrate:
`same room -> READY -> host START -> same monster -> attack on A changes HP on B -> attack on B changes HP on A`.

If this minimal slice fails due to a Cloudflare platform constraint, stop and classify the constraint before migrating any production game logic.
