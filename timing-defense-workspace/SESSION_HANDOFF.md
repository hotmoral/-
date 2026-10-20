# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.35**
- Public URL: `https://timing-defense-v011.onrender.com/v035.html`
- Live source HEAD: `cdfdb60b4d20047d372316224d5815dc6edd3bef`
- Static Render deploy: `dep-dbblp8s9v7es73flhq40` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service ID: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbblpauq1p3s73d1v2mg` / LIVE

Workspace is canonical for design decisions, simulation interpretation, execution boundary and new-session recovery.

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
- Combo display/size/position/animation is approved; do not change unless explicitly requested.

Experimental, not production-frozen:
- passive 40 raw / 2.0 s,
- ordinary non-boss HP +10%,
- combo persistent 5/8/12/15% candidate,
- combo milestone raw-equivalent 60/90/150/210 cap.

---

# Stable UI/runtime foundation
- Rhythm `X → X → X → X+Y`.
- Local/solo skills through Lv21; Lv26/Lv31 planned.
- Target-gated turns; valid in-progress turns survive target removal.
- Stage intro gated; combo survives downtime/target wait.
- Character select uses animated 5-level 6-axis radar and 3×2 skills.
- BASE HP top-center; top-right STAGE → LV → KILLS.
- Rogue HUD charcoal/black + silver.
- Landscape-only gate validated.
- v0.30 blocks bad v0.27 observer; v0.28/v0.29 viewport forcing is superseded.

Radar: 공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

---

# Validated multiplayer foundation

## v0.31 / v0.32
Two independent clients verified room/join, nickname/class/slot, READY propagation, host-only START, shared RUN STARTING and unclipped FRIEND/LINK waiting rooms.

## v0.33
Read `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`.
Android + PC validated real shared Stage 1. Remote PC attack reduced the same authoritative monster HP on Android.

## v0.34
Read `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`.
User device validation confirmed Android movement became smoother and remote projectiles became visible.

---

# Current implementation — v0.35
Read `V035_RECONNECT_SHOP_STAGE2_REPORT.md` first.

## Client files
- `timing-defense-v011/v034-combat-sync.js`
- `timing-defense-v011/v035-reconnect-shop.js`
- `timing-defense-v011/v035.html`

## Server
- `timing-defense-server/server.js`
- backend health version is `0.3.0` in source.

## Reconnect/reload recovery
- Active run session/room/slot/run id is persisted locally after a real run exists.
- Same room URL reload calls server `/resume`.
- Server retains disconnected session for 180 s in this prototype.
- Resume returns current authoritative state, same slot/session and an event floor.
- Immediate resume state omits old events so historic remote projectiles are not replayed in a burst.
- Resumed client starts heartbeat again.

Limit: room/run state is still in-memory. Backend process restart loses it; this is not durable persistence.

## Stage 1 -> Team Shop
On authoritative Stage 1 clear:
- server opens `shop`,
- each human receives existing clear reward +67,
- each human owns personal coin/ranks,
- purchases are server validated,
- READY locks that player's purchases,
- all humans READY -> shop `canNext`,
- host only may NEXT.

Existing six upgrades/cost grammar is reused. No numerical rebalance was introduced.

Prototype team-wall mapping:
- WALL HP buy adds +100 shared base max/current HP.
- human DEF ranks aggregate for shared incoming wall reduction, capped at 60%.
This mapping is not production frozen.

## Stage 2
Host NEXT creates future Stage 2 transition:
- `stage-starting` -> `intro` -> `combat`,
- count 10,
- gap 1040 ms,
- GRUNT 62% / RUNNER 38%,
- existing stage HP scaling and ordinary +10% experiment,
- server authority remains on enemy/world/progression,
- server applies human ATK/CRIT/CRITDMG/KNOCK ranks,
- server passive and AI FILL continue.

v0.35 stops at `stage2-clear`. Stage 3 is intentionally not enabled yet.

## Validation before deployment
Local API integration PASS:
- create/join/READY/START,
- Stage 1 combat,
- Stage 1 -> shop,
- shop reward/purchase,
- all-human READY / host NEXT,
- Stage 2 combat spawn,
- session `/resume` snapshot recovery.

This does not replace Android + PC validation.

---

# Truth boundary
Current deployed code supports:
- real room/READY/START,
- authoritative Stage 1,
- validated v0.34 smooth remote rendering/VFX,
- prototype reload/session recovery,
- authoritative team shop,
- synchronized shop READY/NEXT,
- authoritative Stage 2 bounded slice.

Until user device test passes, do not label v0.35 reconnect/shop/Stage 2 as device-PASS.

Do not claim:
- durable recovery after Render/backend restart,
- Stage 3–10 multiplayer,
- full multiplayer Lv6/Lv11/Lv16/Lv21 skill authority,
- final production shop/shared-wall policy,
- horizontally scaled/durable room store.

---

# Exact next work boundary
1. Android + PC enter one v0.35 room and complete Stage 1.
2. Verify both enter same Team Shop and see consistent personal coin/ranks.
3. Each buys upgrades; verify server state sync.
4. READY both; verify host-only NEXT STAGE.
5. Verify both clients enter synchronized Stage 2 and share RUNNER/GRUNT HP/deaths/BASE HP.
6. Refresh one client during Stage 1 combat, shop, and Stage 2; verify same slot/run recovery and no old-shot replay.
7. Fix only reproducible v0.35 defects.
8. Generalize stage/shop authority through Stage 3–10.
9. Move Lv6/Lv11/Lv16/Lv21 skill effects under server authority.
10. Then implement Lv26/Lv31 and rerun full Solo/2P/3P/4P simulations.

## Still unresolved
- durable server-restart recovery / persistence,
- horizontal scaling,
- invite token/security policy,
- Stage 3–10 multiplayer,
- final team shop/shared-wall ownership semantics,
- complete Lv6+ multiplayer skill authority,
- duplicate-class policy,
- DUO/TRIPLE/FULL reconciliation,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X/tier values,
- final result metrics.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
4. `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`
5. `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`
6. `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`
7. `V031_MULTIPLAYER_FOUNDATION_REPORT.md`
8. `V030_ROOT_CAUSE_RECOVERY_REPORT.md`
9. `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
10. `V026_HUD_LAYOUT_REPORT.md`
11. `CHARACTER_PROFILE_RADAR_V1.md`
12. `DESIGN_DECISIONS.md`
13. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
14. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
15. `SKILL_PLAN_LV6_31.md`
16. `TIER_PRESSURE_GRAMMAR_V1.md`
17. `PRESSURE_RECIPES_V1.md`
18. `SIMULATION_METHOD.md`
19. `NEXT_WORK.md`
