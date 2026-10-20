# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.33**
- URL: `https://timing-defense-v011.onrender.com/v033.html`
- Live source HEAD: `dfb369ed6aaeb8c2768f50e5a2995a7223ac921d`
- Static Render deploy: `dep-dbbkbpks728c738o5feg` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service ID: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbbkbno473hc73cldb30` / LIVE

## Balance governance
Do not production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify → report → discuss → explicit decision → numerical patch/freeze`.

**Combo guard:** current combo visual/size/position/animation is approved. Do not change it unless explicitly requested.

---

# v0.33 validation — authoritative synchronized Stage 1
Use two independent clients/devices.

## Start transition
1. Both clients join the same FRIEND/LINK room.
2. Both READY.
3. Host START.
4. Both clients must leave the waiting room from the same server-owned `startAt` and enter Stage 1.
5. Both must see the normal Stage 1 intro before combat.

## Shared world
Verify continuously:
- enemy count matches,
- enemy HP trend matches,
- enemy deaths match,
- BASE HP matches,
- Stage remains 1 on both,
- server Stage 1 clear/game-over occurs on both.

## Human timing actions
- A performs timing attacks; B must observe the same target HP reduction.
- B performs timing attacks; A must observe the same target HP reduction.
- server charge state must agree with the local 1–3 charge presentation.
- local EXP/LV must update from server state.
- repeated/stale action sequence must not double-apply damage.

## AI / passive
When AI FILL is configured:
- AI damage must occur once on server, not separately per client.
- passive `40 / 2.0s` must occur once per human on server, not separately per client.
- no duplicated kills/coin/base damage from local simulation.

## Runtime regression
Also recheck:
- portrait orientation gate,
- full-width landscape rendering,
- swipe/arrows,
- combo visual unchanged,
- BASE HP top-center HUD,
- STAGE → LV → KILLS HUD,
- FRIEND/LINK waiting-room layout remains unclipped.

Fix only reproducible v0.33 synchronization/runtime defects before expanding scope.

---

# Following network slice
After v0.33 Stage 1 validation passes:
1. Add reconnect/rejoin session recovery using authoritative run snapshot.
2. Add explicit desync/revision diagnostics.
3. Extend the server run state to Stage 2.
4. Implement authoritative Stage 1 → shop transition.
5. Implement multiplayer shop/economy ownership and synchronized NEXT.
6. Validate Stage 2 after shop.
7. Extend same contract through Stage 10.
8. Move Lv6/Lv11/Lv16/Lv21 skill consequences under server authority.
9. Improve remote teammate projectile/VFX fidelity without making VFX authoritative.
10. Validate DUO / TRIPLE / FULL independently.

Do not claim full end-to-end multiplayer Stage 1–10 until two independent clients complete a whole run from the same authoritative state.

---

# Current v0.33 authority contract
Client owns:
- local Timing Square movement/input,
- captured X/Y judgment.

Server owns:
- run id/seed/start time,
- enemy spawn/id/position/HP,
- BASE HP,
- target selection for shared damage,
- normal/heavy state from server charge,
- final attack tier,
- damage/knockback/kill,
- coin,
- EXP/LV,
- charge,
- current combo multiplier candidate,
- passive/AI damage,
- Stage 1 clear/game-over.

Current bounded scope:
- Stage 1 only,
- GRUNT Stage 1 grammar,
- no synchronized shop yet,
- no Lv6+ server skill resolution yet.

---

# Later gameplay/system work
After network foundation stabilizes:
- implement Lv26 / Lv31 skills,
- finalize duplicate-class policy,
- rerun full-run progression/pressure simulation,
- validate Solo / 2P / 3P / 4P,
- finalize passive/ordinary HP/combo coefficients only after report/discussion,
- finalize E/X pressure values and tier progression,
- finalize result-board metric policy.

## Still unresolved
- reconnect/session recovery policy,
- durable multiplayer state store,
- horizontal scaling strategy,
- invite-link security/token contract,
- Stage 2–10 authority,
- multiplayer shop/economy authority,
- complete Lv6+ skill authority,
- duplicate-class rule,
- DUO/TRIPLE/FULL reconciliation details,
- remote projectile/VFX fidelity,
- Lv26/Lv31 coefficients,
- final passive damage/interval,
- final HP compensation,
- combo/milestone coefficients,
- final E/X/tier values,
- final result metrics.
