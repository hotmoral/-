# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.34**
- Public URL: `https://timing-defense-v011.onrender.com/v034.html`
- Live source HEAD: `6bfd51d7d496a0151d4448e71533b4e39de8eaa0`
- Static Render deploy: `dep-dbbklbrbc2fs73bgtq70` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service ID: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbbkbno473hc73cldb30` / LIVE

Workspace is canonical for design decisions, simulation interpretation, current execution boundary and new-session recovery.

---

# Frozen combat / role decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank: knockback / wall protection / team specialist.
- Archer: strict straight-line trajectory; no seeking/bending.
- Mage: density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Balance gaps must be reported/discussed before numerical patching.
- Current combo display/size/position/animation is approved; do not change unless explicitly requested.

Experimental, not production-frozen:
- passive 40 raw / 2.0 s,
- ordinary non-boss HP +10%,
- combo persistent 5/8/12/15% candidate,
- combo milestone raw-equivalent 60/90/150/210 cap.

---

# Core combat / UI state
- Rhythm `X → X → X → X+Y`.
- Local/solo skills implemented through Lv21; Lv26/Lv31 planned.
- New timing turn starts only with a visible target.
- Existing valid turn survives target disappearance.
- Target wait/stage downtime do not break combo.
- Stage intro is gated: `STAGE N / READY → START`.
- Passive interval remains common 2.0 s.
- Character select uses animated 5-level 6-axis radar and 3×2 skill roadmap.
- BASE HP is formal top-center HUD; top-right order is STAGE → LV → KILLS.
- Rogue HUD is charcoal/black + silver.
- Landscape-only orientation gate is validated.
- v0.30 blocks the bad v0.27 skill-level MutationObserver; v0.28/v0.29 viewport forcing is superseded.

Approved radar values:
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`
Axes: 공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역.

---

# Multiplayer milestones already validated

## v0.31 / v0.32 waiting room
Two independent clients verified:
- same real room,
- nickname/class/slot sharing,
- READY propagation,
- host-only START gate,
- START enabled only after all humans READY,
- shared RUN STARTING state,
- FRIEND/LINK layout no longer clips on Samsung Browser.

## v0.33 authoritative Stage 1 slice
Read `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`.

Server creates a run at START and owns:
- run id / seed / startAt,
- Stage 1 intro/combat,
- Stage 1 GRUNT spawn/id/position/HP,
- BASE HP,
- human EXP/LV/charge/combo/kills/coin/damage,
- passive attacks,
- AI FILL attacks,
- ordered combat events,
- Stage 1 clear/game-over.

Authority split:
- client owns local Timing Square and captured X/Y judgment,
- server owns heavy state/final tier/target/damage/knockback/kill/coin/EXP/LV/charge/world state.

User verified on real Android + PC:
- both enter shared Stage 1,
- remote PC attack reduces the same monster HP on Android.
This is the first confirmed end-to-end shared combat path.

---

# Current implementation — v0.34 render smoothing / remote VFX
Read `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md` first.

Client file:
- `timing-defense-v011/v034-combat-sync.js`

Loader:
- `timing-defense-v011/v034.html`

v0.34 replaces the v0.33 combat-sync client layer; do not load both.

Changes:
1. Monster objects are reconciled in place by server id instead of recreated each ~100 ms snapshot.
2. Snapshot target positions are interpolated every animation frame with short bounded extrapolation, while server snapshots remain authoritative.
3. Remote human timing attacks now synthesize class-readable visual projectiles.
4. AI FILL attacks and server-owned passive attacks also synthesize visual projectiles.
5. Remote hit particles/damage floats occur when the visual projectile arrives rather than immediately on event receipt.
6. Remote party visual allocation is rebuilt only when room participant/AI configuration changes.

Remote projectile visual grammar:
- Knight amber/gold blade wave,
- Rogue charcoal/silver dagger,
- Tank blue shock arc,
- Archer green straight arrow,
- Mage purple orb.

No numerical combat balance or combo presentation changed in v0.34. Backend remains the v0.33 Stage 1 authority implementation.

---

# Truth boundary
Safe claims:
- real authoritative room/READY/START,
- real server-authoritative synchronized Stage 1 slice,
- shared monster HP and BASE HP,
- server-resolved human timing actions,
- server-owned passive/AI consequences,
- v0.34 client-side render smoothing and remote attack VFX.

Do not yet claim:
- full Stage 1–10 multiplayer,
- synchronized multiplayer shop,
- Stage 2+ server authority,
- full Lv6+ multiplayer skill consequences,
- reconnect/rejoin recovery,
- durable room/run persistence,
- production anti-cheat.

---

# Exact next work boundary
1. Android + PC re-test v0.34.
2. Confirm Android monster movement is smoother than v0.33.
3. Confirm PC attack shows PC class projectile on Android and Android attack shows Android projectile on PC.
4. Confirm AI FILL/passive projectiles are visible but damage is still applied only once.
5. Confirm shared enemy HP/kills/BASE HP and Stage 1 clear/game-over remain identical.
6. Fix only reproducible v0.34 render/runtime defects.
7. Add reconnect/rejoin snapshot recovery and revision/desync diagnostics.
8. Implement authoritative Stage 1 -> shop transition.
9. Implement Stage 2 + synchronized shop/NEXT.
10. Extend contract through Stage 10.
11. Integrate Lv6/Lv11/Lv16/Lv21 multiplayer skill authority.
12. After network stabilization, implement Lv26/Lv31 and rerun Solo/2P/3P/4P balance simulations.

## Still unresolved
- reconnect/session recovery contract,
- durable/persistent room/run store,
- horizontal scaling strategy,
- invite-link security/token policy,
- Stage 2–10 multiplayer authority,
- shop/economy authority,
- complete Lv6+ multiplayer skill authority,
- duplicate-class policy,
- DUO/TRIPLE/FULL reconciliation details,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X/tier values,
- final result metrics.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`
4. `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`
5. `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`
6. `V031_MULTIPLAYER_FOUNDATION_REPORT.md`
7. `V030_ROOT_CAUSE_RECOVERY_REPORT.md`
8. `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
9. `V026_HUD_LAYOUT_REPORT.md`
10. `CHARACTER_PROFILE_RADAR_V1.md`
11. `DESIGN_DECISIONS.md`
12. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
13. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
14. `SKILL_PLAN_LV6_31.md`
15. `TIER_PRESSURE_GRAMMAR_V1.md`
16. `PRESSURE_RECIPES_V1.md`
17. `SIMULATION_METHOD.md`
18. `NEXT_WORK.md`
