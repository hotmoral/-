# Timing Defense — v0.35 Reconnect / Team Shop / Stage 2 Report

Updated: 2026-10-20 KST

## Scope
v0.35 extends the validated v0.34 shared-combat slice in three bounded directions:
1. reconnect/reload recovery from the authoritative room/run snapshot,
2. authoritative Stage 1 -> team shop transition,
3. authoritative shop READY/NEXT -> synchronized Stage 2 combat.

It does **not** generalize multiplayer through Stage 10 yet and does not add multiplayer Lv6+ skill consequences.

## Live artifacts
Client:
- `timing-defense-v011/v034-combat-sync.js` — validated smoothing + remote projectile layer
- `timing-defense-v011/v035-reconnect-shop.js` — recovery/shop/stage-transition layer
- `timing-defense-v011/v035.html`

Server:
- `timing-defense-server/server.js`

Public:
- `https://timing-defense-v011.onrender.com/v035.html`
- backend: `https://timing-defense-mp.onrender.com`

## Reconnect contract
- Once a real run exists, the client stores room/session/slot/run identity locally.
- Reloading the same room URL attempts `/resume` with the prior session.
- Server reconnect grace is 180 s for the in-memory prototype.
- Resume returns current authoritative snapshot, same slot/session and an event floor.
- Old combat events are suppressed on the immediate recovery response so refresh does not replay a burst of historical projectile VFX.
- A resumed client restores heartbeat independently.

Important limit:
- room/run storage is still in-memory. A Render process restart loses the room/run; v0.35 is session recovery, not durable persistence.

## Authoritative Stage 1 -> shop
When Stage 1 is cleared:
- server changes run status to `shop`,
- every human receives the existing Stage-clear reward `55 + stage*12` (67 after Stage 1),
- combat spawning/input authority is paused,
- each human buys upgrades using that player's server-owned coin,
- the server owns rank/cost/coin validation.

Existing upgrade grammar is reused without rebalancing:
- ATK +8% / rank
- CRIT +2pp / rank
- CRIT DMG +15% proc damage / rank
- WALL HP +100 / rank
- DEF -2.5% wall damage / rank
- KNOCKBACK +10% / rank
- base costs `[40,65,100,145,200,265,340,425,520,625]` with existing category multipliers.

## Team shop READY/NEXT
- Each human has a shop READY toggle.
- READY locks that player's further purchases until they un-READY.
- NEXT is enabled only when every human is READY.
- Only the current host can trigger NEXT STAGE.
- READY/purchases/coin/ranks are shared through the authoritative room state.

Prototype shared-wall semantics:
- WALL HP purchase immediately adds +100 shared max/current base HP.
- DEF ranks across human players currently aggregate for shared incoming-wall reduction, capped at 60%.
- These mappings are an implementation contract for this prototype slice, **not production-frozen balance/design decisions**.

## Stage 2 authority
After host NEXT:
- server publishes future `stage-starting`, then `intro`, then `combat`,
- Stage 2 uses the existing local progression grammar:
  - 10 enemies,
  - 1040 ms base gap,
  - GRUNT 62% / RUNNER 38%,
  - stage HP scaling `(1 + (stage-1)*0.13)` plus current ordinary non-boss +10% experiment.
- authoritative world ownership remains server-side for enemy HP/position, BASE HP, kills and progression.
- human ATK/CRIT/CRIT DMG/KNOCKBACK shop ranks are applied by the server to attacks.
- server-owned passive and AI FILL behavior continues.

v0.35 deliberately stops at `stage2-clear`; Stage 3 is not yet enabled.

## Validation performed before deployment
Local API integration test passed:
- two-human room create/join/READY/START,
- Stage 1 combat actions,
- Stage 1 -> shop transition,
- server shop reward/coin,
- purchase validation,
- two-human READY -> `canNext`,
- host NEXT -> Stage 2 future start,
- Stage 2 combat spawn/authority,
- `/resume` returns same slot/current snapshot without old-event replay payload.

This is server/API validation, not a substitute for Android + PC device validation.

## Device validation required
Using Android + PC:
1. Complete Stage 1 and confirm both clients enter the same shop.
2. Buy upgrades independently and confirm rank/coin changes are reflected consistently.
3. READY both clients; confirm only host gets active NEXT STAGE.
4. Confirm both enter Stage 2 after the shared transition.
5. Confirm Stage 2 monster HP/death/BASE HP and remote VFX stay synchronized.
6. Refresh one client during Stage 1 combat, shop, and Stage 2; confirm same slot/run is recovered.
7. Confirm reload does not replay a burst of old remote shots.

## Truth boundary after v0.35
Safe to claim after device PASS:
- real shared room/READY/START,
- authoritative Stage 1 combat,
- smoothed remote world and remote projectiles,
- bounded reconnect/reload recovery while the server process retains the room,
- authoritative Stage 1 team shop,
- synchronized shop READY/NEXT,
- authoritative Stage 2 combat.

Do not claim yet:
- durable reconnect after server restart,
- Stage 3–10 multiplayer,
- full multiplayer Lv6/Lv11/Lv16/Lv21 skill authority,
- production shop ownership semantics,
- production anti-cheat or horizontally scaled room storage.

No combo presentation or numerical balance coefficient was changed for v0.35.