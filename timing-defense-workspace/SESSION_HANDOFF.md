# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.28**
- Public URL: `https://timing-defense-v011.onrender.com/v028.html`
- Live source HEAD: `df6a18a2722e42e4e4046ff4e6c0b4fb44af894d`
- Render deploy: `dep-dbbhkonavr4c73dtoe0g` / LIVE

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

# v0.27 retained foundation
Read `V027_DEVICE_FIX_WAITING_UX_REPORT.md`.

Character select:
- skill names one line,
- `습득 LV N` one line,
- radar intrinsic aspect ratio `330:280`,
- Android swipe = pointer capture + horizontal-intent detection,
- fixed independent arrows.

Combat HUD retained from v0.26:
- combat title removed,
- combo unchanged,
- BASE HP top-center,
- top-right STAGE → LV → KILLS,
- fortified home-base art,
- combat skill strip reuses lobby skill artwork.

Result board:
- PLAYER / CLASS collision fixed via same-row class badge.

TEAM waiting UX:
- local waiting state for FRIEND/LINK/RANDOM,
- nickname/class/AI FILL preserved,
- READY/back controls,
- no fake link/match/remote participant,
- START disabled until real authority exists.

---

# Current implementation — v0.28
Files:
- `timing-defense-v011/v028-orientation.js`
- `timing-defense-v011/v028.html`

Read:
- `V028_ORIENTATION_HOTFIX_REPORT.md`
- `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
- `V026_HUD_LAYOUT_REPORT.md`
- `CHARACTER_PROFILE_RADAR_V1.md`

## Why v0.28 exists
Samsung Browser device feedback showed a severe orientation/viewport regression: while the phone was physically landscape, the page could retain a portrait-width visual viewport. The game then occupied only the left portion of the physical screen and the right side remained black.

Timing Defense is landscape-only. The broken half-width state must never be treated as a supported layout.

## Orientation / viewport behavior
- Portrait mode is fully blocked by a full-screen orientation gate.
- Underlying lobby/combat/result surfaces are hidden/non-interactive while blocked.
- State is rechecked on orientation change, window resize, VisualViewport resize, and Screen Orientation API change.
- If the device is physically landscape but the visual viewport still behaves portrait-width, v0.28 attempts a viewport-meta reset to the current landscape screen width and forces reflow.
- If the mismatch persists after the repair attempt, the broken game surface remains hidden and a recovery screen is shown.
- Recovery screen offers `가로 상태에서 새로고침` rather than exposing a malformed lobby.
- When landscape becomes valid again, main surfaces are returned to full `100vw` width.

## Non-goals
- no combat change,
- no combo change,
- no radar/skill/waiting-room logic change,
- no balance change,
- no actual networking.

---

# Network truth boundary
Actual multiplayer is still **not implemented**.
Do not claim multiplayer is live until two independent clients join the same authoritative room and synchronize game state.

TEAM slot rule:
- SOLO: AI 0–3
- TEAM: AI FILL 0–2, leaving at least one human slot.

---

# Exact next work boundary
1. Device-test public v0.28 on the same Samsung Browser/Android device.
2. Confirm direct landscape load occupies full width.
3. Rotate to portrait and confirm only the orientation gate is visible.
4. Rotate back to landscape and confirm the lobby returns full-width.
5. If a stale portrait-width viewport occurs in physical landscape, confirm the half-width lobby is hidden and the safe recovery screen appears.
6. Recheck v0.27 items: skill title/level one-line, radar proportions, swipe + arrows, result rows, FRIEND/LINK/RANDOM waiting screens.
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
3. `V028_ORIENTATION_HOTFIX_REPORT.md`
4. `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
5. `V026_HUD_LAYOUT_REPORT.md`
6. `V025_LAYOUT_POLISH_REPORT.md`
7. `V024_RADAR_READABILITY_REPORT.md`
8. `CHARACTER_PROFILE_RADAR_V1.md`
9. `DESIGN_DECISIONS.md`
10. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
11. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
12. `SKILL_PLAN_LV6_31.md`
13. `TIER_PRESSURE_GRAMMAR_V1.md`
14. `PRESSURE_RECIPES_V1.md`
15. `SIMULATION_METHOD.md`
16. `NEXT_WORK.md`
