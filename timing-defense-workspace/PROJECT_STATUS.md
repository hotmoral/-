# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.32**
- Public URL: `https://timing-defense-v011.onrender.com/v032.html`
- Live source HEAD: `16b602221caf1d19c062e17363ac786d2bd20d18`
- Static Render deploy: `dep-dbbivgjrjlhs73ee5bm0` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbbims61egvs73861f10` / LIVE

## Core playable scope
- Landscape timing-action side defense.
- Rhythm: `X → X → X → X+Y`.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Stage 1–10 run with EXP / level / coin / shop.
- Class skills implemented through Lv21; Lv26/Lv31 planned.
- AI teammates use internal timing/EXP/level/skills without visible AI Timing Squares.

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

## v0.30 runtime recovery
Read `V030_ROOT_CAUSE_RECOVERY_REPORT.md`.

- v0.27 introduced a self-retriggering skill-level MutationObserver.
- v0.30 blocks only that defective observer while preserving intended v0.27 UX.
- v0.28/v0.29 viewport-forcing experiments are superseded and are not loaded.
- Samsung Browser device validation confirmed portrait gate, full-width landscape lobby, and full-width combat were restored.

---

# v0.31 — authoritative multiplayer-room foundation
Read `V031_MULTIPLAYER_FOUNDATION_REPORT.md`.

## Backend
Source:
- `timing-defense-server/server.js`
- `timing-defense-server/package.json`

Transport:
- authoritative HTTP mutation endpoints,
- Server-Sent Events for shared room state,
- heartbeat/session expiry,
- in-memory prototype room store.

Server currently owns:
- room code/method,
- host session,
- participant slots,
- nickname/class,
- READY state,
- AI FILL positions/classes,
- room status,
- future synchronized `startAt`,
- room revision.

Implemented:
- FRIEND/LINK room creation and join,
- real invite URL `?room=<CODE>`,
- shared participant/READY state,
- server-authoritative host START gate,
- RANDOM matchmaking queue,
- leave/host reassignment,
- room heartbeat/cleanup.

TEAM rule remains:
- SOLO AI 0–3,
- TEAM AI FILL 0–2,
- 4 total slots maximum,
- at least one human slot preserved when configuring TEAM AI FILL.

## Multiplayer truth boundary
**Full multiplayer gameplay is not yet complete.**

v0.31/v0.32 can legitimately claim a real shared authoritative waiting room and synchronized START gate.
They must not yet claim synchronized combat.

Required next network slice:
- authoritative run snapshot,
- synchronized local run start at `startAt`,
- Attack Round/timing-result event synchronization,
- enemy/wall/coin/EXP/level state ownership,
- disconnect/reconnect snapshot recovery,
- shop/economy authority,
- desync detection/reconciliation.

---

# v0.32 — waiting-room layout hotfix
Read `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`.

Samsung Browser device feedback showed FRIEND/LINK left-panel clipping while networking itself remained functional.

Fixed:
- invite URL is one-line with ellipsis,
- READY / INVITE / COPY LINK action row gets reserved space,
- local-player card/status spacing is compacted,
- short landscape height receives an extra compact layout,
- footer space is explicitly reserved,
- RANDOM networking flow is unchanged.

No networking semantics, combat, combo, or numerical balance changed.

---

# Immediate next boundary
1. Device-test v0.32 FRIEND and LINK waiting rooms on the same Samsung Browser device.
2. Confirm READY + INVITE/COPY LINK + lower status/link content are all visible without clipping.
3. With two independent clients, verify participant/class/READY propagation both directions.
4. Verify host-only START and common `startAt`.
5. Verify leave/host reassignment.
6. Verify RANDOM pairing with two independent searches.
7. Fix only reproducible room/session/UI defects.
8. Then implement synchronized combat/run state.
9. After network foundation stabilizes, implement Lv26/Lv31 skills.
10. Then rerun full-run Solo/2P/3P/4P simulations before numerical balance freeze.

## Still unresolved / not production-frozen
- combat-state network authority,
- reconnect grace and durable session recovery,
- invite-link security/token contract,
- persistent/horizontally-scaled room storage,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL combat synchronization details,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X pressure values and tier structure,
- final result-board metric policy.
