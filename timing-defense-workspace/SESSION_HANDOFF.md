# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.27**
- Public URL: `https://timing-defense-v011.onrender.com/v027.html`
- Live source HEAD: `6208e5d4665ca6acb6ebbd1105c50c0551c03630`
- Render deploy: `dep-dbbhfp3rjlhs73e9nvp0` / LIVE

Workspace is canonical for design decisions, simulation interpretation, and new-session recovery.

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

Experimental values remain not production-frozen:
- passive 40 raw / 2.0 s, ordinary non-boss HP +10%,
- combo persistent 5/8/12/15% candidate,
- combo milestone raw-equivalent 60/90/150/210 cap.

**Important guard:** combo display/size/position/animation is approved and must not be changed unless explicitly requested. The earlier overlap defect was the combat title, which v0.26 removed.

---

# Core combat state
- Rhythm `X → X → X → X+Y`.
- Skills implemented through Lv21; Lv26/Lv31 remain planned.
- New timing turn starts only with a visible target.
- Target-wait blocks empty-turn EXP farming.
- Already-started valid turns survive target disappearance.
- Heavy X→Y can finish fully after target disappearance.
- Target-wait/stage downtime do not break combo.
- Stage intro: `STAGE N / READY → fade → START! + combat`.
- Passive auto-attack interval remains common across classes at 2.0 s.

---

# Approved class-profile radar
Axes:
`공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`

Values:
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

Five visual levels. Equal levels are allowed. This is class-identity presentation data, not a literal raw-stat dump.

---

# Current implementation — v0.27
Files:
- `timing-defense-v011/v027-polish.js`
- `timing-defense-v011/v027.html`

Read:
- `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
- `V026_HUD_LAYOUT_REPORT.md`
- `CHARACTER_PROFILE_RADAR_V1.md`

## Character-select fixes
- Skill names forced to one line.
- Acquisition level forced to one line as `습득 LV N`.
- Header fonts reduced slightly so Korean names do not wrap.
- Skill descriptions still use the full lower card width.
- Radar canvas now preserves intrinsic `330:280` aspect ratio and no longer squashes vertically.
- Radar values/animation unchanged.
- Swipe is reimplemented using pointer capture + horizontal-intent detection and a ~38 px threshold.
- Arrows remain fixed and continue working independently.

## Combat HUD retained from v0.26
- No combat title.
- Combo unchanged.
- BASE HP formal top-center gauge.
- Top-right icon + STAGE → icon + LV → icon + KILLS.
- Fortified home-base visual.
- Combat six-skill strip reuses character-select artwork.

## Result board
PLAYER / CLASS collision is fixed by placing class in a same-row colored badge instead of a second line. Row spacing is recalculated for four players and the board is shortened to separate RETRY/LOBBY more cleanly.

## TEAM waiting-room UX
TEAM start now opens an actual local waiting screen.

Shared behavior:
- selected nickname/class retained,
- AI FILL positions/classes retained,
- P1 local,
- P2/P3/P4 show AI FILL or HUMAN SLOT,
- local READY toggle,
- return to PLAY SETTING,
- START disabled until real network authority/participant sync exists.

FRIEND:
- INVITE UI exists but truthfully reports transport is not connected.

LINK:
- ROOM LINK UI exists but no fake link is generated.

RANDOM:
- SEARCH / CANCEL SEARCH UI state exists,
- explicitly says NETWORK NOT CONNECTED,
- no fake match success or remote player creation.

---

# Network truth boundary
Actual multiplayer is still **not implemented**.
Do not claim multiplayer is live until two independent clients join the same authoritative room and synchronize game state.

TEAM slot rule:
- SOLO: AI 0–3
- TEAM: AI FILL 0–2, leaving at least one human slot.

---

# Exact next work boundary
1. Device-test public v0.27 on the same Android landscape setup.
2. Verify skill name / acquisition level stay on one line.
3. Verify radar is proportionally correct.
4. Verify both swipe and arrow navigation.
5. Verify result-board labels no longer overlap.
6. Verify TEAM waiting screen for FRIEND/LINK/RANDOM and safe return to settings.
7. Fix implementation/visual defects only.
8. Then design real multiplayer architecture:
   - room authority/backend,
   - invite/link lifecycle,
   - random matchmaking queue,
   - slot/class ownership,
   - synchronized start,
   - combat event synchronization,
   - disconnect/reconnect,
   - reconciliation/desync policy.
9. After network foundation, continue Lv26/Lv31 implementation and full-run balance simulation.

## Still unresolved
- actual room/network backend,
- invite/link security contract,
- matchmaking policy,
- reconnect/reconciliation,
- multiplayer economy/shop ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL synchronization,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X/tier values,
- final result metric policy.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
4. `V026_HUD_LAYOUT_REPORT.md`
5. `V025_LAYOUT_POLISH_REPORT.md`
6. `V024_RADAR_READABILITY_REPORT.md`
7. `CHARACTER_PROFILE_RADAR_V1.md`
8. `DESIGN_DECISIONS.md`
9. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
10. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
11. `SKILL_PLAN_LV6_31.md`
12. `TIER_PRESSURE_GRAMMAR_V1.md`
13. `PRESSURE_RECIPES_V1.md`
14. `SIMULATION_METHOD.md`
15. `NEXT_WORK.md`
