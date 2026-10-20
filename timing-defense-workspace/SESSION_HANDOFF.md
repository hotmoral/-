# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.23**
- Public URL: `https://timing-defense-v011.onrender.com/v023.html`
- Live source HEAD: `6a7a4acafda9fe7dc405455c73adc3d7065f1285`
- Render deploy: `dep-dbbfierrjlhs73e3mfeg` / LIVE

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

---

# Current implementation — v0.23
Files:
- `timing-defense-v011/v023-polish.js`
- `timing-defense-v011/v023-results.js`
- `timing-defense-v011/v023.html`

See `V023_LOBBY_POLISH_REPORT.md`.

## Character selection
User feedback changed the layout from `character-left + skill-cards-right` to a landscape three-zone hierarchy:
- left fixed info = class name/role/play style,
- center = only the hero slides horizontally,
- right fixed info = six skill icons + selected skill full detail.

Arrow + swipe navigation remains.
All six milestones `6/11/16/21/26/31` are visible simultaneously.
Skill descriptions are no longer intentionally truncated.

## Character/icon direction
- Geometric prototype characters remain, with a second small detail pass for silhouette/gear readability.
- Skill icons stay mechanic-specific: multiple blades/daggers/arrows where the mechanic contains multiples; shields, cracks, shockwaves, linked orbs etc. must visually indicate the effect.

## Rogue HUD contrast
Natural scenery made Rogue's gray HUD too weak.
v0.23 adds a brighter red/silver **HUD-only** contrast accent to Timing Square edge + charge pips. No Rogue numerical buff.

## EXP popup integrity
Every valid local `awardXP(amount)` now independently arms `+EXP N` beside the gauge, including gains between level-ups.
Lower-left EXP float stays removed.

## TEAM slot semantics
TEAM must reserve at least one human participant slot.
- SOLO: AI 0–3.
- TEAM: AI FILL 0–2 only.
- Switching TEAM while +3 AI is active falls back to +2 AI.

This does not implement networking yet.

## AI setting readability
K/R/T/A/M-only controls replaced visually by compact role glyph + `KNI/ROG/TNK/ARC/MAG` labels.
Layout spacing compressed to reduce the previous short-landscape clipping.

## Result board
- centered final redraw,
- larger row spacing,
- local nickname used when available,
- metrics remain KILLS / DMG / COIN / LV / MAX COMBO,
- per-column rank colors retained.

## Debug cleanup
The battle `CLASS · ATTACK N · RESULT · AXIS` label is hidden.

---

# Network truth boundary
Actual multiplayer is **not yet implemented**.
FRIEND/LINK/RANDOM remain selection states only.
Do not claim a remote player joined until two independent clients share authoritative room/game state.

The originally planned v0.23 waiting-room slice is deferred one version because v0.23 was used for device-feedback polish.
Next waiting-room target is **v0.24**.

---

# Exact next work boundary
1. Device-test public v0.23.
2. Check center-only hero slide and fixed left/right information wings.
3. Check all six skill icons/full descriptions on short Android landscape.
4. Check Rogue square/charge readability over natural background.
5. Verify every local timing EXP event shows `+EXP N`.
6. Verify TEAM cannot select +3 AI; at least one human slot remains.
7. Verify result table no longer has player/class row collisions.
8. Fix visual/implementation defects only.
9. Implement v0.24 waiting-room UX for FRIEND / LINK / RANDOM.
10. After waiting UX, design/wire actual room/invite/random network architecture.
11. Continue full-run progression simulation before freezing passive/HP/combo values.

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
