# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.35**
- URL: `https://timing-defense-v011.onrender.com/v035.html`
- Live source HEAD: `cdfdb60b4d20047d372316224d5815dc6edd3bef`
- Static Render deploy: `dep-dbblp8s9v7es73flhq40` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service ID: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbblpauq1p3s73d1v2mg` / LIVE

## Balance governance
Do not production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify → report → discuss → explicit decision → numerical patch/freeze`.

**Combo guard:** current combo visual/size/position/animation is approved. Do not change it unless explicitly requested.

---

# Immediate validation — v0.35 reconnect / team shop / Stage 2
Use the Android + PC pair that passed v0.34.

## A. Stage 1 -> Team Shop
1. Both clients join the same v0.35 room, READY and START.
2. Complete Stage 1 normally.
3. Both clients must enter the same `TEAM SHOP` state.
4. Each player receives server-owned Stage 1 clear reward (+67) in addition to any kill coin already earned.
5. Each client must display its own authoritative coin and upgrade ranks.

## B. Purchases
Verify independently on both players:
- ATK / CRIT / CRIT DMG / WALL HP / DEF / KNOCKBACK purchase succeeds only when affordable.
- rank and coin changes propagate from server state.
- READY locks further purchases on that player.
- un-READY permits editing/purchases again.
- the other player's independent purchases do not overwrite local personal ranks.

Prototype shared-wall checks:
- WALL HP purchase raises shared BASE HP maximum/current by 100.
- DEF purchases contribute to shared incoming wall reduction.
These are prototype rules, not final production balance/ownership decisions.

## C. Shop READY/NEXT
1. One player READY -> the other sees that READY state.
2. NEXT remains disabled until every human is READY.
3. Only host gets active NEXT STAGE.
4. Host NEXT publishes one shared future Stage 2 start.

## D. Stage 2
Both clients must:
- transition through Stage 2 intro,
- enter the same Stage 2 combat,
- see the same GRUNT/RUNNER population and HP/deaths,
- share BASE HP and kills,
- see remote human/AI/passive projectile VFX,
- keep smooth monster rendering,
- apply purchased human ATK/CRIT/CRITDMG/KNOCK on the server.

Stage 2 bounded endpoint is `STAGE 2 SYNC CLEAR`; Stage 3 is intentionally not enabled in v0.35.

## E. Reconnect/reload recovery
Test three positions independently:
1. during Stage 1 combat,
2. while Team Shop is open,
3. during Stage 2 combat.

Procedure:
- refresh/reload one client's same `?room=CODE` URL,
- client should show RUN RECOVERY briefly,
- same session/slot/run should restore from server snapshot,
- current enemy/base/progression or shop state should match the other client,
- old historical remote projectile events must not replay as a burst.

Reconnect prototype limits:
- server retains stale session for 180 seconds,
- room/run is still in-memory,
- a Render backend restart loses the run and is not recoverable in v0.35.

## F. Regression
Also confirm:
- v0.34 movement remains smooth,
- remote projectiles remain visible,
- no duplicate damage from VFX,
- portrait gate / landscape width remain correct,
- combo visual unchanged,
- waiting room remains unclipped.

Fix only reproducible v0.35 networking/runtime/UI defects before expanding scope.

---

# Following implementation boundary after v0.35 PASS
1. Generalize authoritative stage grammar beyond Stage 2.
2. Add Stage 2 -> shop -> Stage 3 and repeat through Stage 10 using a common stage state machine.
3. Integrate existing monster grammar: GRUNT / RUNNER / BRUTE / SHIELD / FLYER and Stage 5/10 bosses.
4. Validate whole-run shop/READY/NEXT behavior with DUO / TRIPLE / FULL.
5. Move Lv6 / Lv11 / Lv16 / Lv21 skill consequences to server authority by class.
6. Add revision/desync diagnostics and stronger recovery/reconciliation.
7. Decide durable room/run persistence and horizontal-scaling strategy.
8. After multiplayer system stabilization, implement Lv26 / Lv31.
9. Rerun full Solo / 2P / 3P / 4P simulations before numerical balance freeze.

Do not claim full end-to-end Stage 1–10 multiplayer until two independent clients complete a whole authoritative run.

---

# Current authority contract
Client owns:
- local Timing Square movement/input,
- captured X/Y judgment,
- visual interpolation and projectile rendering,
- shop UI intent only.

Server owns:
- room/session/slot/host,
- run id/seed/start times,
- Stage 1 and Stage 2 enemy spawn/id/position/HP,
- BASE HP,
- target/final tier/damage/knockback/kill,
- coin / EXP / LV / charge / combo candidate,
- passive and AI damage,
- shop coin/ranks/purchase validation,
- shop READY/NEXT gate,
- Stage 1 -> shop -> Stage 2 transition.

Current bounded scope:
- Stage 1 + Team Shop + Stage 2,
- Stage 3–10 not yet networked,
- multiplayer Lv6+ skill authority not yet implemented,
- reconnect is same-server in-memory session recovery only.

---

# Later gameplay/system work
After networking stabilizes:
- implement Lv26 / Lv31 skills,
- finalize duplicate-class policy,
- rerun full-run progression/pressure simulation,
- validate Solo / 2P / 3P / 4P,
- finalize passive/ordinary HP/combo coefficients only after report/discussion,
- finalize E/X pressure values/tier progression,
- finalize result-board metric policy.

## Still unresolved
- durable persistence / server restart recovery,
- horizontal scaling strategy,
- invite-link security/token contract,
- Stage 3–10 authority,
- final multiplayer shop/shared-wall ownership semantics,
- complete Lv6+ skill authority,
- duplicate-class rule,
- DUO/TRIPLE/FULL reconciliation,
- Lv26/Lv31 coefficients,
- final passive damage/interval,
- final HP compensation,
- combo/milestone coefficients,
- final E/X/tier values,
- final result metrics.
