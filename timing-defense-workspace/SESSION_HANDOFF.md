# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.32**
- Public URL: `https://timing-defense-v011.onrender.com/v032.html`
- Live source HEAD: `16b602221caf1d19c062e17363ac786d2bd20d18`
- Static Render deploy: `dep-dbbivgjrjlhs73ee5bm0` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service ID: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbbims61egvs73861f10` / LIVE

Workspace remains canonical for design decisions, simulation interpretation, and new-session recovery.

---

# Frozen combat / role decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank: team-specialist / knockback / wall protection.
- Archer: strict straight-line trajectory; no bending/seeking.
- Mage: density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Balance gaps must be reported/discussed before numerical patching.
- Current combo display/size/position/animation is approved; do not change unless explicitly requested.

Experimental values remain not production-frozen:
- passive 40 raw / 2.0 s,
- ordinary non-boss HP +10%,
- combo persistent 5/8/12/15% candidate,
- combo milestone raw-equivalent 60/90/150/210 cap.

---

# Core combat state
- Rhythm `X → X → X → X+Y`.
- Skills implemented through Lv21; Lv26/Lv31 planned.
- New timing turn starts only with a visible target.
- Empty-target turns do not grant EXP.
- Already-started valid turns survive target disappearance.
- Heavy X→Y can finish after target disappearance.
- Target wait/stage downtime do not break combo.
- Stage intro: `STAGE N / READY → fade → START! + combat`.
- Passive auto-attack interval remains common across classes at 2.0 s.

---

# Approved class radar
Axes: `공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`

Values:
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

Five visual levels. Equal levels allowed. Radar is presentation data, not literal raw-stat output.

---

# Stable UI/runtime foundation
- v0.26 provides the stable lobby/combat HUD foundation.
- v0.27 desired UX: one-line skill headers, radar aspect fix, Android swipe, result class badges, TEAM waiting UI.
- v0.27 contained a self-retriggering skill-level MutationObserver regression.
- v0.30 blocks only that defective observer and restores stable device rendering.
- v0.28/v0.29 viewport-forcing experiments are superseded and not loaded.
- Device validation after v0.30 confirmed portrait gate, full-width landscape lobby, and full-width combat.

Read:
- `V030_ROOT_CAUSE_RECOVERY_REPORT.md`
- `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
- `V026_HUD_LAYOUT_REPORT.md`

---

# Current implementation — v0.32 multiplayer waiting-room foundation + layout hotfix
Read in order:
1. `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`
2. `V031_MULTIPLAYER_FOUNDATION_REPORT.md`

## Client
Files:
- `timing-defense-v011/v031-network.js`
- `timing-defense-v011/v032-waiting-layout.js`
- `timing-defense-v011/v032.html`

v0.31 upgraded the TEAM waiting room from local-only presentation to a real server-backed room state. v0.32 fixes FRIEND/LINK left-panel clipping on short Android landscape viewports without changing networking semantics.

## Server
Files:
- `timing-defense-server/server.js`
- `timing-defense-server/package.json`

Render service:
- `timing-defense-mp`
- Singapore
- public backend URL: `https://timing-defense-mp.onrender.com`

Transport/design:
- authoritative HTTP POST mutations,
- SSE room-state stream,
- heartbeat/session expiry,
- in-memory room/ticket state for prototype phase,
- no external runtime dependency.

## Real shared state implemented
- room code,
- FRIEND/LINK room create/join,
- invite URL with `?room=<CODE>`,
- participant slots,
- nickname/class,
- host ownership,
- READY state,
- TEAM AI FILL state,
- leave/host reassignment,
- RANDOM matchmaking queue,
- server-authoritative future `startAt` gate.

START policy:
- at least two human participants,
- every human READY,
- only server-recognized host may START,
- server publishes one future `startAt` to all clients.

## v0.32 presentation fix
- invite URL is one-line with ellipsis,
- READY / INVITE / COPY LINK remain visible,
- local card/status spacing is compacted,
- extra compact rules apply on short landscape height,
- RANDOM flow is unchanged.

## Truth boundary
**Actual shared combat is not yet implemented.**

Safe claim:
- real authoritative shared room exists,
- two clients can share participant/READY state,
- START gate is authoritative and synchronized.

Do not claim full multiplayer gameplay until actual run/combat state is synchronized.

---

# Exact next work boundary
1. On the same Samsung Browser device, verify FRIEND/LINK v0.32 no longer clip lower content.
2. Two independent clients/device sessions test room create/join.
3. Verify participant/class/READY changes propagate without reload.
4. Verify host-only START and common `startAt`.
5. Verify leave and host reassignment.
6. Verify RANDOM matching with two searches.
7. Fix only reproducible room/session/UI defects.
8. Then implement authoritative run snapshot and synchronized run start.
9. Synchronize Attack Round/timing-result events.
10. Synchronize enemies, wall, coin, EXP/level and stage transitions.
11. Add disconnect/reconnect snapshot recovery and desync reconciliation.
12. Add multiplayer shop/economy authority.
13. After networking stabilizes, implement Lv26/Lv31 and rerun Solo/2P/3P/4P balance simulations.

## Still unresolved
- durable/persistent multiplayer room store,
- horizontal scaling strategy,
- reconnect grace/session recovery contract,
- invite-link security/token policy,
- combat-event authority/reconciliation,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL combat synchronization,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X/tier values,
- final result metric policy.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`
4. `V031_MULTIPLAYER_FOUNDATION_REPORT.md`
5. `V030_ROOT_CAUSE_RECOVERY_REPORT.md`
6. `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
7. `V026_HUD_LAYOUT_REPORT.md`
8. `CHARACTER_PROFILE_RADAR_V1.md`
9. `DESIGN_DECISIONS.md`
10. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
11. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
12. `SKILL_PLAN_LV6_31.md`
13. `TIER_PRESSURE_GRAMMAR_V1.md`
14. `PRESSURE_RECIPES_V1.md`
15. `SIMULATION_METHOD.md`
16. `NEXT_WORK.md`
