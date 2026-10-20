# Timing Defense v0.33 — Multiplayer Combat Slice Report

Updated: 2026-10-20 KST

## Public build
- Client: `https://timing-defense-v011.onrender.com/v033.html`
- Live source HEAD: `dfb369ed6aaeb8c2768f50e5a2995a7223ac921d`
- Static Render deploy: `dep-dbbkbpks728c738o5feg` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend deploy: `dep-dbbkbno473hc73cldb30` / LIVE

## Purpose
v0.33 is the first real combat-synchronization slice after v0.31/v0.32 waiting-room validation. It deliberately stops at authoritative Stage 1 rather than pretending the full Stage 1–10 run is synchronized.

## Server authority added
`timing-defense-server/server.js` now creates a real run object when the host presses START.

The run owns:
- run id,
- server seed,
- `startAt`,
- Stage 1 intro/combat timing,
- Stage 1 spawn count,
- enemy ids / normalized positions / HP,
- base HP,
- run kills,
- per-human EXP / level / charge / combo / kills / coin / damage,
- AI FILL attack timing,
- passive basic attacks,
- combat event sequence,
- periodic authoritative snapshots.

Server tick:
- 50 ms simulation tick,
- room snapshot broadcast approximately every 100 ms while starting/running.

## Stage 1 scope
For this first slice the authoritative run is intentionally bounded:
- Stage 1 only,
- Stage 1 GRUNT spawn grammar,
- 8 enemies,
- current ordinary-monster +10% HP experiment reflected in server HP,
- current passive attack `40 / 2.0 s`,
- current AI timing probabilities / cadence direction,
- wall damage and Stage 1 clear handled by server.

No numerical values were production-frozen by this implementation.

## Player action authority
The client still owns the local Timing Square interaction and sends only timing judgments plus a monotonic action sequence.

The server resolves:
- whether the attack is normal or charged heavy,
- resulting tier,
- base damage,
- current persistent combo multiplier candidate,
- target selection,
- actual damage,
- knockback,
- kill,
- coin,
- EXP / level,
- charge,
- server combat event.

This is the chosen v0.33 authority split:
- client authority: local timing input/judgment capture,
- server authority: shared world and combat consequences.

## Client integration
New file:
- `timing-defense-v011/v033-combat-sync.js`

On a shared START:
1. client receives server run snapshot,
2. schedules local entry from the server-owned `startAt`,
3. exits waiting room,
4. starts the existing Stage 1 intro locally,
5. disables local enemy spawning / AI combat / passive damage authority,
6. consumes server snapshots for enemy HP/position, base HP and local progression,
7. sends local completed timing attacks to `/action`,
8. renders server-confirmed combat events,
9. keeps remote humans/AI visible in the party area.

## Truth boundary
v0.33 may claim:
- real two-client room,
- shared READY/START,
- shared Stage 1 start,
- server-owned Stage 1 enemy/base state,
- server-resolved human timing attacks,
- server-owned passive/AI Stage 1 effects,
- shared Stage 1 clear/game-over state.

v0.33 must NOT yet claim:
- Stage 2–10 synchronized run,
- synchronized shop/economy decisions,
- full Lv6+ skill combat authority,
- reconnect/rejoin recovery,
- durable room storage,
- complete remote projectile/VFX fidelity,
- production-grade anti-cheat.

## Device validation required
Two independent clients should verify:
1. READY/START still behaves as in v0.32.
2. Both leave the waiting room at the same START.
3. Both enter Stage 1 and see the same enemy count/HP trend.
4. Player A timing attacks reduce the same enemy HP on B.
5. Player B timing attacks reduce the same enemy HP on A.
6. BASE HP remains equal on both clients.
7. local EXP/LV/charge update from the server.
8. AI FILL/passive damage is identical on both clients.
9. Stage 1 clear/game over occurs on both clients.
10. no duplicate local enemy spawn or duplicate AI/passive damage is observed.

## Following slice
After v0.33 two-client Stage 1 validation:
- fix any world/action reconciliation defects,
- add reconnect snapshot recovery,
- extend authoritative state to Stage 2 + shop first,
- then extend through Stage 10,
- then integrate Lv6/Lv11/Lv16/Lv21 multiplayer skill resolution,
- only after network behavior is stable proceed to Lv26/Lv31 implementation and final balance work.
