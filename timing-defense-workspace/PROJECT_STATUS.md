# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.34**
- Public URL: `https://timing-defense-v011.onrender.com/v034.html`
- Live source HEAD: `6bfd51d7d496a0151d4448e71533b4e39de8eaa0`
- Static Render deploy: `dep-dbbklbrbc2fs73bgtq70` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbbkbno473hc73cldb30` / LIVE

## Core playable scope
- Landscape timing-action side defense.
- Rhythm: `X → X → X → X+Y`.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Solo prototype: Stage 1–10 with EXP / level / coin / shop.
- Multiplayer prototype: real shared waiting room + authoritative synchronized Stage 1 slice.
- Local/solo skills implemented through Lv21; Lv26/Lv31 planned.
- Multiplayer Lv6+ skill authority is not complete.

## Frozen combat / balance governance
- Knight = stable generalist / penetration / strong heavy.
- Rogue = multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank = knockback / wall protection / team specialist.
- Archer = strict straight-line penetration; no seeking/bending.
- Mage = density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Simulation findings must be reported/discussed before numerical rebalance.
- Combo display/size/position/animation is approved and must not change without explicit user request.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`,
- ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` cap.

## Approved class radar
Axes: `공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`
Five visual levels; equal levels allowed; presentation data only.

---

# Stable UI/runtime foundation
- Animated class radar.
- Character select = left profile / center hero / right `3 × 2` skill roadmap.
- Skill name + `습득 LV N` one-line headers.
- Rogue HUD charcoal/black + silver.
- BASE HP formal top-center gauge.
- Top-right HUD: STAGE → LV → KILLS.
- Combat title removed; combo untouched.
- Landscape-only orientation gate.
- v0.30 blocks the v0.27 self-retriggering MutationObserver regression.
- v0.28/v0.29 viewport forcing is superseded and not loaded.
- v0.32 fixed FRIEND/LINK lower-content clipping.

---

# Multiplayer milestones

## v0.31 / v0.32 waiting room — device validated
Implemented and user-tested with two independent clients:
- real FRIEND/LINK room create/join,
- invite URL `?room=<CODE>`,
- participant slot / nickname / class sharing,
- host authority,
- READY sync both directions,
- AI FILL state,
- server-authoritative START gate / shared future `startAt`,
- waiting-room clipping fix.

## v0.33 authoritative Stage 1 combat slice — device validated
Read `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`.

Server owns:
- run id / seed / `startAt`,
- Stage 1 intro/combat state,
- Stage 1 GRUNT spawn/id/normalized position/HP,
- BASE HP,
- human EXP/LV/charge/combo/kills/coin/damage,
- passive attacks,
- AI FILL attacks,
- ordered combat events,
- Stage 1 clear/game-over.

Authority split:
- Client owns Timing Square movement/input and captured X/Y judgment.
- Server owns heavy state, final tier, target, damage, knockback, kill, coin, EXP/LV, charge and world state.

User validation confirmed:
- two independent clients enter the same real Stage 1,
- a PC player's attack reduces the same monster HP on the Android client,
- shared world-state synchronization is actually working.

## v0.34 render smoothing + remote VFX
Read `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`.

Trigger:
- Android showed slight stepped/stuttered monster movement while PC looked smoother,
- remote attacks changed HP but had no projectile on the receiving client.

Changes:
- authoritative monster objects are reconciled in place by id instead of recreated each snapshot,
- 100 ms snapshots are visually interpolated/extrapolated at render-frame cadence,
- remote human / AI FILL / server passive attacks synthesize visual-only class projectiles,
- remote impact particles/damage floats occur when the visual projectile reaches the target,
- remote party visual allocation is rebuilt only when participant/AI configuration changes.

No server-authority or numerical balance changes in v0.34.

---

# Multiplayer truth boundary
Safe claim:
- real authoritative shared room/READY/START,
- real server-authoritative synchronized Stage 1 combat slice,
- shared monster HP and BASE HP,
- server-resolved human timing actions,
- shared passive/AI consequences,
- visual smoothing and remote projectile presentation in v0.34.

Do NOT yet claim full Stage 1–10 multiplayer.
Still missing:
- reconnect/rejoin recovery,
- explicit desync/revision diagnostics,
- Stage 1 -> shop authority,
- Stage 2–10 network authority,
- multiplayer shop/economy,
- full Lv6+ server skill consequences,
- durable room/run persistence,
- final duplicate-class policy.

---

# Immediate next boundary
1. Two independent clients validate v0.34 smoothing and remote projectiles.
2. Confirm remote human, AI FILL and passive projectiles are visible without duplicate damage.
3. Confirm Android movement is smoother than v0.33.
4. Confirm enemy HP/kills/BASE HP/Stage 1 clear remain identical.
5. Fix only reproducible v0.34 presentation/runtime defects.
6. Add reconnect/rejoin snapshot recovery and revision diagnostics.
7. Implement authoritative Stage 1 -> shop transition.
8. Implement Stage 2 + synchronized shop/NEXT.
9. Extend the same contract through Stage 10.
10. Integrate Lv6/Lv11/Lv16/Lv21 multiplayer skill authority.
11. After networking stabilizes, implement Lv26/Lv31 and rerun Solo/2P/3P/4P balance simulations before numerical freeze.

## Still unresolved / not production-frozen
- reconnect grace/session recovery contract,
- durable/persistent multiplayer storage,
- horizontal scaling strategy,
- invite-link security/token policy,
- Stage 2–10 authority,
- multiplayer shop/economy authority,
- complete Lv6+ multiplayer skill authority,
- duplicate-class rule,
- DUO/TRIPLE/FULL reconciliation details,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X pressure values/tier structure,
- final result-board metric policy.
