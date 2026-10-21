# Timing Defense — Cloudflare Durable Objects PoC device validation

Date: 2026-10-21 KST

## Public deployment
- Worker URL: `https://timing-defense-do-poc.sktjsek.workers.dev`
- Public root UI: PASS
- `/api/health`: PASS
- Reported health fields:
  - `service=timing-defense-do-poc`
  - `version=0.1.0`
  - `transport=websocket-hibernation`
  - `authority=durable-object-event-driven`
  - `locationHint=apac-ne`

## Two-client evidence
Observed on independent clients in room `4NK5T4`:
- both clients connected through WebSocket,
- participant list synchronized,
- host remained P1,
- READY propagated to both clients,
- host START succeeded after both READY,
- one authoritative test monster appeared on both clients,
- authoritative monster HP was synchronized across clients,
- accepted attacks reduced HP `300 -> 200 -> 100 -> 0`,
- `CLEAR` state propagated to both clients.

This proves the core Durable Object/WebSocket authoritative synchronization slice.

## Remaining PoC closure check
PoC is not yet closed as full PASS until reconnect/resume is tested on the public deployment:
1. create/start a fresh room,
2. perform at least one accepted attack,
3. refresh one client,
4. reconnect with the same local session,
5. verify same room/slot/current state is restored,
6. verify the next attack sequence is accepted and synchronized,
7. verify the other client stays in the same room/state throughout.

## Current classification
- Static/public deployment: PASS
- Health/router: PASS
- Two-client READY/START/shared HP/attack/CLEAR: PASS
- Public reconnect: PENDING
- v0.35 migration parity: NOT STARTED

Do not merge the PoC into `timing-defense-live-v011` yet. After reconnect PASS, promote only the next bounded migration slice: existing v0.31 room/READY/START semantics onto Durable Object/WebSocket, then v0.33/v0.34 authoritative Stage 1 state/rendering contract.
