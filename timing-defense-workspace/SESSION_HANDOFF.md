# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.33**
- Public URL: `https://timing-defense-v011.onrender.com/v033.html`
- Live source HEAD: `dfb369ed6aaeb8c2768f50e5a2995a7223ac921d`
- Static Render deploy: `dep-dbbkbpks728c738o5feg` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service ID: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbbkbno473hc73cldb30` / LIVE

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
- Local/solo skills implemented through Lv21; Lv26/Lv31 planned.
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
Five visual levels; equal levels allowed; presentation data only.

---

# Stable UI/runtime foundation
- v0.26 stable lobby/combat HUD foundation.
- v0.27 desired UX: one-line skill headers, radar aspect fix, Android swipe, result badges, TEAM waiting UI.
- v0.27 observer regression is blocked by v0.30 safety layer.
- v0.28/v0.29 viewport forcing is superseded and not loaded.
- Samsung Browser device validation confirmed portrait gate, full-width landscape lobby/combat.
- v0.32 fixes FRIEND/LINK lower-content clipping without changing network semantics.

Read:
- `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`
- `V030_ROOT_CAUSE_RECOVERY_REPORT.md`
- `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
- `V026_HUD_LAYOUT_REPORT.md`

---

# Multiplayer foundation verified before v0.33
v0.31/v0.32 real shared waiting-room behavior was tested with two independent clients.

Verified by user:
- same room participant appears remotely,
- class/nickname/slot shared,
- READY state shared both ways,
- START enables only when all humans READY,
- host presses START,
- both clients receive RUN STARTING / shared server start gate.

This closes the waiting-room START-gate milestone.

---

# Current implementation — v0.33 authoritative Stage 1 combat slice
Read `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md` first.

## Client files
- `timing-defense-v011/v033-combat-sync.js`
- `timing-defense-v011/v033.html`

## Server file
- `timing-defense-server/server.js`

## Server now creates a run at START
Authoritative run state includes:
- run id / seed,
- server `startAt`,
- Stage 1 intro/combat phase,
- Stage 1 GRUNT spawn state,
- enemy ids / normalized position / HP,
- base HP,
- per-human level / EXP / charge / combo / kills / coin / damage,
- passive attacks,
- AI FILL attacks,
- ordered combat events,
- Stage 1 clear / game-over.

Simulation cadence:
- 50 ms server tick,
- approximately 100 ms shared snapshots while run is starting/running.

## Authority split
Client:
- owns local Timing Square interaction,
- captures X/Y NORMAL/GOOD/PERFECT judgments,
- sends monotonic action sequence.

Server:
- validates action sequence,
- decides normal vs charged heavy from server charge,
- derives final tier,
- applies current combo multiplier candidate,
- selects target,
- resolves damage / knockback / kill,
- resolves coin / EXP / level / charge,
- owns enemy/base world state.

## Client runtime behavior
At shared START:
- schedules actual run transition from server `startAt`,
- hides waiting/lobby UI,
- starts existing Stage 1 intro,
- disables local enemy spawn authority,
- disables local AI attack authority,
- disables local passive damage authority,
- reconciles server snapshots into the existing combat renderer,
- sends completed local timing attacks to server,
- shows other humans/AI in the party area.

## v0.33 truth boundary
Safe claim:
- real room/READY/START,
- real shared Stage 1 start,
- server-owned Stage 1 monsters/base HP,
- server-resolved local timing attacks,
- shared passive/AI Stage 1 consequences,
- shared Stage 1 clear/game-over.

Do NOT yet claim:
- synchronized Stage 2–10,
- multiplayer shop/economy,
- full multiplayer Lv6+ skill behavior,
- reconnect/rejoin recovery,
- durable room persistence,
- complete remote projectile/VFX fidelity,
- production anti-cheat.

---

# Exact next work boundary
1. Two independent clients test v0.33 START -> actual Stage 1.
2. Confirm both see same enemy count/HP trend.
3. A attacks -> B sees same HP reduction; B attacks -> A sees same HP reduction.
4. Confirm BASE HP remains identical.
5. Confirm EXP/LV/charge are reconciled from server.
6. Confirm passive/AI damage is not duplicated locally.
7. Confirm Stage 1 clear/game-over occurs on both clients.
8. Fix only reproducible Stage 1 sync defects.
9. Implement reconnect snapshot recovery.
10. Extend authority through Stage 2 + shop, then through Stage 10.
11. Integrate Lv6/Lv11/Lv16/Lv21 multiplayer skill authority.
12. After network stabilization, implement Lv26/Lv31 and rerun Solo/2P/3P/4P balance simulations.

## Still unresolved
- reconnect grace/session recovery contract,
- Stage 2–10 multiplayer state,
- durable/persistent room/run store,
- horizontal scaling strategy,
- invite-link security/token policy,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL reconciliation,
- complete remote projectile/VFX fidelity,
- multiplayer Lv6+ skill authority,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X/tier values,
- final result metric policy.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`
4. `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`
5. `V031_MULTIPLAYER_FOUNDATION_REPORT.md`
6. `V030_ROOT_CAUSE_RECOVERY_REPORT.md`
7. `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
8. `V026_HUD_LAYOUT_REPORT.md`
9. `CHARACTER_PROFILE_RADAR_V1.md`
10. `DESIGN_DECISIONS.md`
11. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
12. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
13. `SKILL_PLAN_LV6_31.md`
14. `TIER_PRESSURE_GRAMMAR_V1.md`
15. `PRESSURE_RECIPES_V1.md`
16. `SIMULATION_METHOD.md`
17. `NEXT_WORK.md`
