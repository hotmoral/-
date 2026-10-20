# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.33**
- Public URL: `https://timing-defense-v011.onrender.com/v033.html`
- Live source HEAD: `dfb369ed6aaeb8c2768f50e5a2995a7223ac921d`
- Static Render deploy: `dep-dbbkbpks728c738o5feg` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbbkbno473hc73cldb30` / LIVE

## Core playable scope
- Landscape timing-action side defense.
- Rhythm: `X → X → X → X+Y`.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Solo prototype: Stage 1–10 with EXP / level / coin / shop.
- Multiplayer prototype: authoritative shared waiting room + **authoritative synchronized Stage 1 slice** in v0.33.
- Class skills implemented locally through Lv21; multiplayer skill authority beyond base Stage 1 is not complete.
- Lv26/Lv31 remain planned.

## Frozen role / combat direction
- Knight = stable generalist / penetration / strong heavy.
- Rogue = fast multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank = knockback / wall protection / team specialist.
- Archer = strict straight-line penetration; no bending/seeking.
- Mage = density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Simulation findings must be reported/discussed before numerical rebalance.
- Combo display/size/position/animation is approved and must not change without explicit user request.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`, ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` cap.

## Approved class radar
Axes: `공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`

Profiles:
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

Five visual levels. Equal levels are allowed. Radar is class-identity presentation, not a literal raw-stat dump.

---

# Presentation / UX foundation
- Animated class radar.
- Character select = left profile / center hero / right `3 × 2` skill roadmap.
- Skill name + `습득 LV N` one-line headers.
- Rich class role/detail copy.
- Rogue HUD charcoal/black + silver.
- Projectile visibility pass without projectile travel-time change.
- BASE HP formal top-center gauge.
- Top-right HUD: STAGE → LV → KILLS.
- Fortified home-base visual.
- Combat six-skill strip reuses lobby skill art.
- Combat title removed; combo untouched.
- Landscape-only orientation gate.

## Runtime recovery
Read `V030_ROOT_CAUSE_RECOVERY_REPORT.md`.
- v0.27 introduced a self-retriggering skill-level MutationObserver.
- v0.30 blocks only that defective observer while preserving intended v0.27 UX.
- v0.28/v0.29 viewport-forcing experiments are superseded and are not loaded.
- Samsung Browser device validation confirmed portrait gate, full-width landscape lobby, and full-width combat were restored.

---

# v0.31 / v0.32 — real waiting-room foundation
Read:
- `V031_MULTIPLAYER_FOUNDATION_REPORT.md`
- `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`

Implemented and device-validated:
- FRIEND/LINK real room creation and join,
- invite URL `?room=<CODE>`,
- participant slots / nickname / class,
- host authority,
- READY synchronization,
- TEAM AI FILL state,
- RANDOM matchmaking queue foundation,
- server-authoritative future `startAt`,
- FRIEND/LINK waiting-room clipping fix.

Two independent-device validation confirmed:
- remote participant appears in the same room,
- READY state propagates,
- START is host-gated and requires all humans READY,
- both clients receive the shared RUN STARTING state.

---

# v0.33 — authoritative multiplayer Stage 1 combat slice
Read `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`.

## Server authority
`timing-defense-server/server.js` now owns a run object created at START.

For the v0.33 bounded slice the server owns:
- run id / seed / `startAt`,
- Stage 1 intro/combat state,
- Stage 1 GRUNT spawning,
- enemy ids / normalized positions / HP,
- BASE HP,
- run kills,
- human EXP / level / charge / combo / kills / coin / damage,
- passive attacks,
- AI FILL attack timing/results,
- ordered combat events,
- Stage 1 clear / game-over.

Server simulation cadence:
- 50 ms tick,
- authoritative room/run snapshots about every 100 ms while starting/running.

## Player action authority split
- Client owns local Timing Square input and captured `NORMAL / GOOD / PERFECT` judgments.
- Client sends a monotonic action sequence plus X/Y judgments.
- Server determines normal vs heavy state, final tier, combo bonus candidate, target, damage, knockback, kill, coin, EXP/level and charge.

This avoids treating each client as an independent combat simulation.

## Client integration
New file:
- `timing-defense-v011/v033-combat-sync.js`

On server START the client:
- schedules actual run entry from server `startAt`,
- exits the waiting room,
- starts Stage 1 intro,
- disables local enemy spawn / local AI authority / local passive authority,
- consumes server world snapshots,
- sends completed local timing attacks to the server,
- reconciles enemy/base/progression state from server snapshots,
- renders remote humans/AI in the party area.

## Multiplayer truth boundary
v0.33 can claim a real server-authoritative **Stage 1 synchronization slice**.

It must NOT yet claim full multiplayer gameplay across Stage 1–10.
Still missing:
- Stage 2–10 network state,
- multiplayer shop/economy authority,
- full Lv6+ skill resolution on server,
- reconnect/rejoin recovery,
- durable room/run persistence,
- full remote projectile/VFX fidelity,
- final desync reconciliation policy.

---

# Immediate next boundary
1. Two independent clients validate v0.33 START -> actual Stage 1 transition.
2. Confirm both see the same enemy count and HP movement.
3. Confirm A timing attack changes enemy HP on B and vice versa.
4. Confirm BASE HP remains equal.
5. Confirm local EXP / LV / charge come back from server correctly.
6. Confirm AI FILL and passive damage occur once, identically on both clients.
7. Confirm Stage 1 clear/game-over occurs on both.
8. Fix only reproducible Stage 1 sync defects.
9. Add reconnect snapshot recovery.
10. Extend authority through Stage 2 + shop before expanding to Stage 10.
11. Then integrate Lv6/Lv11/Lv16/Lv21 multiplayer skill resolution.
12. After networking stabilizes, implement Lv26/Lv31 and rerun full Solo/2P/3P/4P simulations before numerical balance freeze.

## Still unresolved / not production-frozen
- Stage 2–10 multiplayer state,
- reconnect grace/session recovery contract,
- durable/persistent room and run storage,
- horizontal scaling strategy,
- invite-link security/token contract,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL reconciliation details,
- multiplayer Lv6+ skill authority,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X pressure values and tier structure,
- final result-board metric policy.
