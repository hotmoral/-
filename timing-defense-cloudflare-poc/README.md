# Timing Defense — Cloudflare Durable Objects PoC

## Purpose
This branch proves the replacement architecture before any v0.35 gameplay migration.

Target slice only:
1. create one authoritative room,
2. connect two independent browser clients,
3. synchronize READY,
4. host-only START,
5. create one authoritative monster with 300 HP,
6. each accepted ATTACK deals fixed 100 HP on the Durable Object,
7. both clients receive the same HP/state over WebSocket.

This PoC is intentionally separate from the production game UI and does not change any Timing Defense balance values.

## Architecture
- Cloudflare Worker: public router + static asset delivery.
- One `TimingDefenseRoom` Durable Object per six-character room code.
- SQLite-backed Durable Object storage.
- WebSocket Hibernation API through `ctx.acceptWebSocket()`.
- Northeast Asia placement hint: `apac-ne`.
- No 50 ms server tick.
- No periodic authoritative snapshots.
- State changes only on events: join/reconnect, READY, START, ATTACK, disconnect.

## Files
- `wrangler.jsonc` — Worker/static assets/Durable Object declaration.
- `src/index.js` — Worker router and authoritative room object.
- `public/index.html` — isolated two-client diagnostic UI.

## Local check
From this directory:

```bash
npm install
npm run dev
```

Open two independent browser sessions. Create a room in client A, copy the room link/code into client B, connect both, READY both, START from the host, then attack from either side.

Expected:
- both clients show the same participant list,
- READY propagates both ways,
- only the host can START,
- both clients show one monster at 300 HP,
- one ATTACK changes 300 -> 200 on both,
- another client ATTACK changes 200 -> 100 on both,
- third accepted ATTACK changes 100 -> 0 and state becomes `clear`.

## Cloudflare deploy
After account authentication:

```bash
npm install
npx wrangler deploy
```

The Worker uses the current declarative Durable Object `exports` configuration and SQLite storage.

## Explicit non-goals
This PoC does **not** yet contain:
- existing v0.35 UI,
- timing-square X/Y judgment,
- real class damage,
- monster movement,
- wall damage,
- EXP/level/coin,
- Team Shop,
- Stage 2,
- production reconnect grace/TTL,
- Stage 3–10,
- balance changes.

## Promotion gate
Do not migrate the real v0.35 flow until the public Cloudflare PoC passes on Android + PC with two independent clients.

After PoC PASS, the next migration slice is:
`v0.31 room/READY/START contract -> Durable Object/WebSocket`, followed by the v0.33/v0.34 authoritative Stage 1 state and rendering contract.
