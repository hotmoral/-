# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.26**
- Public URL: `https://timing-defense-v011.onrender.com/v026.html`
- Live source HEAD: `8aee137de2f775cda3537b6cc0b9404f6692a55b`
- Render deploy: `dep-dbbgvjjbc2fs73b657s0` / LIVE

Workspace is canonical for design decisions, simulation interpretation and new-session recovery.

---

# Frozen combat / role decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank: team-specialist / knockback / wall protection; solo parity not required.
- Archer: strict straight-line trajectory; no off-line retarget/bending.
- Mage: density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP remains tied to valid timing events; passive basic attacks grant no EXP.
- Balance gaps are reported/discussed before numerical patching.

Mastery reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.

---

# Core combat state
- Rhythm `X → X → X → X+Y`.
- Skills implemented through Lv21; Lv26/Lv31 planned.
- New timing turn starts only with a visible target.
- If no target exists at turn boundary, square/AI/passive wait.
- Already-started valid turn survives target disappearance; heavy X→Y may finish.
- Target-wait/stage downtime do not break combo.
- Stage intro: `STAGE N / READY → fade → START! + combat`.

Experimental values remain **not production-frozen**:
- passive 40 raw / 2.0 s, no EXP/charge/crit/skill/combo, ordinary non-boss HP +10%,
- combo persistent 5/8/12/15% tiers,
- combo milestone raw-equivalent 60/90/150/210 cap.

Passive auto-attack interval remains common across all classes at `2.0 s`; class projectile visual travel times differ.

**Important v0.26 guard:** do not modify combo presentation from the latest overlap feedback. User explicitly clarified that the combat title was the problem, not combo size/placement.

---

# Presentation history
## v0.21
- natural battlefield,
- `+EXP N` beside gauge,
- judgment pop inside Timing Square,
- START cue,
- debug stats/hint hidden.

## v0.22
- nickname + class carousel + skill roadmap,
- button/segmented play settings,
- custom AI class/position,
- battle class selector and bottom prototype controls hidden,
- FRIEND/LINK/RANDOM front-end choice only; no real remote connectivity.

## v0.23
- left info / center hero / right skill detail hierarchy,
- every valid timing EXP event shows `+EXP N`,
- TEAM reserves at least one human slot; TEAM AI FILL max +2,
- result board row spacing + nickname cleanup,
- attack debug label hidden.

## v0.24
See `V024_RADAR_READABILITY_REPORT.md` and `CHARACTER_PROFILE_RADAR_V1.md`.
- approved five-level six-axis radar,
- axes: 공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역,
- profiles: Knight 4/2/3/3/4/2; Rogue 2/5/5/1/1/1; Tank 2/1/1/5/1/3; Archer 3/2/4/1/5/2; Mage 4/2/2/1/1/5,
- skill layout 3×2,
- TEAM SUMMARY removed; class buttons wrap,
- Rogue HUD charcoal/black + silver,
- projectile contrast strengthened without timing changes.

## v0.25
See `V025_LAYOUT_POLISH_REPORT.md`.
- top/nickname/footer compressed,
- character-selection panel made taller,
- radar labels enlarged,
- richer class role/detail copy restored,
- hero presence increased.

---

# Current implementation — v0.26
Files:
- `timing-defense-v011/v026-hud-layout.js`
- `timing-defense-v011/v026.html`

See `V026_HUD_LAYOUT_REPORT.md`.

## Character select
- Six skills remain `3 × 2`.
- Every card now uses:
  - icon beside skill name,
  - `습득 LV N` directly below the name,
  - full-width description beneath both icon/name columns.
- Radar is moved upward/bounded so the role summary and full class description are visible.
- Hero class name moved above the head.
- Arrow buttons use fixed coordinates, larger hit targets, no active-state jump, and stop pointer/touch propagation before carousel swipe handling.
- Swipe remains available away from arrows.

## Combat HUD
- Legacy combat `TIMING DEFENSE` title is hidden.
- Combo presentation is deliberately unchanged.
- Top-center BASE HP HUD added with icon, current/max value, and long horizontal gauge.
- Top-right run HUD order is fixed:
  1. icon + STAGE,
  2. icon + LV,
  3. icon + KILLS.
- Old bottom canvas status strings are suppressed to avoid duplicate information.

## Home base
The left structure now reads more clearly as a fortified base via:
- armored cap,
- crenellations,
- reinforced columns,
- four recessed character bays,
- four ledges/platforms,
- small central crest.

## Combat skill strip
The six slots below Timing Square now reuse the exact class-select skill canvases.
- learned slots: full artwork,
- locked slots: same artwork dimmed/grayscaled,
- order: Lv6 / 11 / 16 / 21 / 26 / 31.

## Non-goals
- no combo visual/logic change,
- no combat coefficient change,
- no projectile travel-time change,
- no actual networking.

---

# Network truth boundary
Actual multiplayer is **not yet implemented**.
FRIEND/LINK/RANDOM remain selection states only.
Do not claim a remote player joined until two independent clients share authoritative room/game state.

TEAM slot rule:
- SOLO: AI 0–3
- TEAM: AI FILL 0–2, preserving at least one human slot.

---

# Exact next work boundary
1. Device-test public v0.26 on the same Android landscape setup.
2. Verify `습득 LV N` placement and full-width skill descriptions.
3. Verify radar is higher and role/detail copy is fully visible.
4. Verify class name above hero head.
5. Rapidly tap both arrows; verify every tap registers and buttons do not jump. Recheck swipe outside arrows.
6. Verify combo popup remains unchanged.
7. Verify combat title is gone.
8. Verify BASE HP top-center is immediately readable.
9. Verify icon + STAGE → LV → KILLS top-right is stable and readable.
10. Verify improved base art and combat skill icons in motion.
11. Fix implementation/visual defects only from this validation.
12. Then implement FRIEND/LINK/RANDOM waiting-room UX without faking connectivity.
13. After waiting UX, design/wire actual room/invite/random network architecture.
14. Continue full-run progression simulation before freezing passive/HP/combo values.

## Still unresolved
- final passive/HP/combo coefficients,
- final result metrics,
- final E/X and tier structure,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL sync,
- Lv26/Lv31 coefficients,
- network room authority / lifecycle / invite-link / random queue / reconnect / reconciliation.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V026_HUD_LAYOUT_REPORT.md`
4. `V025_LAYOUT_POLISH_REPORT.md`
5. `V024_RADAR_READABILITY_REPORT.md`
6. `CHARACTER_PROFILE_RADAR_V1.md`
7. `V023_LOBBY_POLISH_REPORT.md`
8. `V022_LOBBY_IMPLEMENTATION_REPORT.md`
9. `V021_IMPLEMENTATION_REPORT.md`
10. `V020_IMPLEMENTATION_REPORT.md`
11. `DESIGN_DECISIONS.md`
12. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
13. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
14. `SKILL_PLAN_LV6_31.md`
15. `TIER_PRESSURE_GRAMMAR_V1.md`
16. `PRESSURE_RECIPES_V1.md`
17. `SIMULATION_METHOD.md`
18. `NEXT_WORK.md`