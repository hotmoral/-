# Timing Defense — Public Workspace

Persistent planning / balance / simulation / handoff workspace for Timing Defense.

## Repository layout
- Live playable branch: `timing-defense-live-v011`
- Workspace branch: `timing-defense-workspace`
- Public service: `https://timing-defense-v011.onrender.com`
- Current playable prototype: **v0.23**
- Current play page: `https://timing-defense-v011.onrender.com/v023.html`
- Live HEAD: `6a7a4acafda9fe7dc405455c73adc3d7065f1285`
- Render deploy: `dep-dbbfierrjlhs73e3mfeg` / LIVE

Workspace is separate from deployment so planning/simulation work does not publish the game.

## New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V023_LOBBY_POLISH_REPORT.md`
4. `V022_LOBBY_IMPLEMENTATION_REPORT.md`
5. `V021_IMPLEMENTATION_REPORT.md`
6. `V020_IMPLEMENTATION_REPORT.md`
7. `DESIGN_DECISIONS.md`
8. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
9. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
10. `SKILL_PLAN_LV6_31.md`
11. `TIER_PRESSURE_GRAMMAR_V1.md`
12. `PRESSURE_RECIPES_V1.md`
13. `SIMULATION_METHOD.md`
14. `NEXT_WORK.md`

---

# Current game
Landscape timing-action side defense with five classes: Knight / Rogue / Tank / Archer / Mage.
Core rhythm: `X → X → X → X+Y`.
Implemented class growth: Lv6 / 11 / 16 / 21; future Lv26 / Lv31.

Role rules:
- Knight generalist,
- Rogue durable-normal multihit execution,
- Tank team-specialist/control,
- Archer strict straight-line penetration,
- Mage density/AoE.

---

# Combat foundation
- Off-screen targets cannot be damaged/rewarded.
- New timing turns start only with a visible enemy.
- Already-started valid turns survive target disappearance.
- Heavy X→Y may finish.
- Stage flow: `STAGE N / READY → START! + combat`.
- Natural landscape background.
- Judgment pop inside Timing Square.
- PERFECT-only unbounded combo.
- Passive A/B 40 raw / 2.0 s; ordinary non-boss HP +10%; values not frozen.

---

# v0.22 lobby foundation
Entry flow:
`nickname + class carousel → play settings → run / future team waiting → combat`.

- five classes,
- arrow + swipe navigation,
- mechanic-specific Lv6/11/16/21/26/31 icons,
- button/segmented settings,
- custom AI class/position,
- old in-battle configuration controls hidden,
- FRIEND/LINK/RANDOM front-end only; no real network yet.

---

# v0.23 current polish
See `V023_LOBBY_POLISH_REPORT.md`.

## Character selection
Three-zone landscape hierarchy:
- left = class identity/role/play style,
- center = sliding hero,
- right = six skill icons + selected full detail.

Skill descriptions are displayed in a dedicated detail panel instead of truncated cards.

## Readability
- Rogue Timing Square/charge pips receive a brighter red/silver HUD accent over natural scenery.
- Every valid local EXP event independently shows `+EXP N` beside the gauge.
- Battle attack/debug line hidden.
- Result rows get more spacing and use local nickname.

## Play settings
- SOLO AI 0–3.
- TEAM uses `AI FILL` 0–2 only and must reserve at least one human slot.
- AI class choice uses role glyph + KNI/ROG/TNK/ARC/MAG rather than only one-letter codes.
- Landscape spacing tightened to reduce overflow.

---

# Encounter framework
Pressure families: S Swarm / E Elite-Heavy / X Special-Mixed.
Tier identity comes from varied pattern count, timing and geometry.

Current Swarm candidates:
- line 2P/3P/4P = 8 / 11 / 14
- cluster = 7 / 10 / 13
- scatter = 9 / 12 / 16.

---

# Working principle
Simulation is diagnostic, not self-authorizing. Numerical balance changes require report/discussion/explicit decision.
Human/device testing is authoritative for feel, visual hierarchy, lobby/settings usability and VFX readability.

## Current next boundary
- device-validate v0.23,
- fix visual/implementation defects only,
- implement **v0.24** FRIEND/LINK/RANDOM waiting-room UX,
- then design/wire real multiplayer room/match networking,
- continue full-run progression simulation before freezing passive/combo/HP values.
