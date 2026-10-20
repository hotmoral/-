# Timing Defense — v0.31 Multiplayer Foundation Report

Updated: 2026-10-20 KST

## Public build
- Client: `https://timing-defense-v011.onrender.com/v031.html`
- Client live branch: `timing-defense-live-v011`
- Client HEAD: `714e1e3060cbbd2c20a65114d2152b37f861ef22`
- Client Render deploy: `dep-dbbioegae00c73dd8cn0` / LIVE

## Backend
- Render web service: `timing-defense-mp`
- Service ID: `srv-dbbimre1egvs73861d80`
- Region: Singapore
- URL: `https://timing-defense-mp.onrender.com`
- Server source: `timing-defense-server/server.js`
- Package: `timing-defense-server/package.json`
- Initial backend deploy: `dep-dbbims61egvs73861f10` / LIVE

## Architecture decision
v0.31 uses an authoritative HTTP + Server-Sent Events room service rather than client-only fake state.

Reasoning:
- current game is a static-site client,
- lobby synchronization is mostly state broadcast rather than high-frequency physics,
- SSE keeps implementation small and dependency-free for the first network slice,
- authoritative POST endpoints own mutations,
- combat synchronization can later add a dedicated high-frequency channel if measurements justify it.

The backend currently keeps room state in process memory. Therefore this is a prototype networking foundation, not yet horizontally scalable or durable across service restarts.

## Implemented authoritative room state
Server owns:
- room code,
- TEAM method (`friend` / `link` / `random`),
- host session,
- participant slots,
- nickname,
- selected class,
- READY state,
- AI FILL slots/classes,
- room status,
- synchronized `startAt` gate,
- room revision.

TEAM rules retained:
- maximum 4 total slots,
- TEAM AI FILL maximum 2,
- human slots remain available,
- host authority is server-owned.

## Endpoints
- `GET /health`
- `POST /api/room/create`
- `POST /api/room/join`
- `GET /api/room/:code/state`
- `GET /api/room/:code/stream?session=...`
- `POST /api/room/:code/update`
- `POST /api/room/:code/heartbeat`
- `POST /api/room/:code/leave`
- `POST /api/room/:code/start`
- `POST /api/random/search`
- `GET /api/random/status?ticket=...`
- `POST /api/random/cancel`

## Client behavior
`v031-network.js` upgrades the v0.27 waiting room from local-only presentation to server-backed state.

FRIEND / LINK:
- first client creates an authoritative room,
- room code is visible,
- invite/copy uses a real URL with `?room=<CODE>`,
- second client opening the URL is guided to TEAM/LINK,
- when it enters the waiting room it joins the same server room,
- participant slots, nickname, class, host and READY states come from server state,
- SSE broadcasts room updates to connected clients.

READY / START:
- each human client changes its own READY state through the server,
- host START is enabled only when at least two human participants are present and all humans are READY,
- START creates a server-owned future `startAt` timestamp approximately 2.5 seconds ahead,
- every client receives the same starting state through the room stream.

RANDOM:
- backend has a real search queue,
- two searching tickets are paired into one authoritative room,
- the client polls ticket state until matched, then attaches to the shared room stream.

## Important truth boundary
v0.31 is the first build with a real shared multiplayer waiting-room backend, but **combat synchronization is not yet implemented**.

Do not describe the full game as multiplayer-complete yet.

The current valid claim is:
- two clients can share one authoritative room,
- see synchronized participant/READY state,
- receive one authoritative START gate.

The next slice must synchronize the actual run/combat state before multiplayer gameplay can be considered real end-to-end.

## Validation required
On two independent browser sessions/devices:
1. Client A opens v0.31, selects TEAM + FRIEND/LINK, then START RUN.
2. A receives a six-character room code and real invite URL.
3. Client B opens that invite URL, selects/keeps nickname and class, opens TEAM waiting room.
4. Both clients show the same participants and classes.
5. READY changes on either client appear on the other client without reload.
6. Host START stays disabled until all humans are READY.
7. Host START changes both clients to the same `starting` state/start timestamp.
8. Back/leave removes the participant from the authoritative room.
9. RANDOM can be tested with two independent searches.

## Next implementation boundary
1. two-client v0.31 room validation,
2. fix any room/session/UI defects,
3. define authoritative run snapshot,
4. synchronized run start at `startAt`,
5. synchronize Attack Round/timing-result events,
6. synchronize enemy/wall/coin/progression state,
7. reconnect + snapshot recovery,
8. shop/economy authority,
9. desync detection/reconciliation.

No numerical combat balance changes are authorized by this networking work.
