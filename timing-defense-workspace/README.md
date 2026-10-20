# Timing Defense — Public Workspace

Persistent planning / balance / simulation / handoff workspace for Timing Defense.

## Repository layout
- Live playable branch: `timing-defense-live-v011`
- Workspace branch: `timing-defense-workspace`
- Public service: `https://timing-defense-v011.onrender.com`
- Current playable prototype: **v0.22**
- Current play page: `https://timing-defense-v011.onrender.com/v022.html`
- Live HEAD: `7a321d021cafbfc32749b4e8b9421b2bf908826a`
- Render deploy: `dep-dbbef5s9v7es73eupvlg` / LIVE

The workspace branch is separate from the deployment branch so documentation/simulation work does not publish the game.

## New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V022_LOBBY_IMPLEMENTATION_REPORT.md`
4. `V021_IMPLEMENTATION_REPORT.md`
5. `V020_IMPLEMENTATION_REPORT.md`
6. `DESIGN_DECISIONS.md`
7. `V019_IMPLEMENTATION_REPORT.md`
8. `V018_IMPLEMENTATION_REPORT.md`
9. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
10. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
11. `SKILL_PLAN_LV6_31.md`
12. `TIER_PRESSURE_GRAMMAR_V1.md`
13. `PRESSURE_RECIPES_V1.md`
14. `SIMULATION_METHOD.md`
15. `NEXT_WORK.md`

Older reports remain for numerical provenance.

---

# Core game
Landscape timing-action side defense with five classes:
- Knight
- Rogue
- Tank
- Archer
- Mage

Core rhythm: `X → X → X → X+Y`.
Implemented class growth: Lv6 / 11 / 16 / 21.
Future reserved: Lv26 / Lv31.

Key role rules:
- Knight generalist,
- Rogue durable-normal multihit execution,
- Tank team-specialist/control,
- Archer strict straight-line penetration,
- Mage density/AoE.

---

# Current combat foundation

## Target integrity
- off-screen enemies cannot be targeted/damaged,
- new timing turns start only with a visible target,
- if no target exists at the next-turn boundary the square waits,
- AI/passive attacks wait too,
- no empty EXP turns.

An already-started valid turn survives target disappearance:
- current X remains tappable,
- heavy X→Y may finish fully,
- normal EXP remains valid for that turn,
- next turn waits.

## Stage boundary
`STAGE N / READY → fade → START! + combat`

## Passive/Combo A/B
Passive:
- 40 raw / 2.0 s
- no EXP/charge/crit/skill/combo
- non-boss HP +10%

Combo:
- PERFECT-only unbounded streak,
- transient popup from 1 combo,
- 5/8/12/15% persistent A/B tiers,
- class-specific milestone follow-ups.

Numbers remain experimental.

---

# v0.21 presentation layer
See `V021_IMPLEMENTATION_REPORT.md`.

- natural geometric landscape replaces black grid,
- lower-left EXP float removed,
- `+EXP N` beside gauge,
- judgment results pop quickly inside Timing Square with tier-specific color/size,
- START cue added,
- results centered,
- debug stats/hint hidden.

---

# v0.22 pre-game lobby
See `V022_LOBBY_IMPLEMENTATION_REPORT.md`.

Entry flow:
`nickname + class carousel → play settings → run / future team waiting → combat`

## Character carousel
- five classes,
- arrow + swipe horizontal navigation,
- large geometric class visual,
- clothing/weapon identity,
- role summary,
- Lv6/11/16/21/26/31 roadmap.

## Skill icons
Icons use mechanic-specific shape + color rather than generic/recolored symbols.
Examples include:
- dual blade waves / double slash,
- multiple daggers / dagger rain,
- shields / shockwaves / ground cracks,
- line penetration / triple arrows,
- burst / resonance / chain explosion rings.

## Play settings
Button/segmented controls are preferred over dropdowns for small fixed option sets.
Current controls:
- SOLO / TEAM
- AI 0–3
- AI class + P2/P3/P4 position
- FRIEND / LINK / RANDOM team method
- Tier1

Defaults:
- SOLO
- no AI
- highest available tier (currently Tier1)

Solo + selected AI starts the real current combat immediately.
TEAM networking is **not yet connected**; v0.22 does not pretend remote players joined.

Old in-combat class selection and bottom prototype settings controls are hidden.

---

# Encounter framework
Pressure families:
- S = Swarm
- E = Elite/Heavy
- X = Special/Mixed

Tier identity comes from different 1/2/3-pattern distributions and timing/geometry, not forcing all three into every stage.

Current Swarm candidates:
- line 2P/3P/4P = 8 / 11 / 14
- cluster = 7 / 10 / 13
- scatter = 9 / 12 / 16

---

# Working principle
Simulation is diagnostic, not self-authorizing.
Large balance gaps must be explained and discussed before numerical live changes.

Human/device testing is authoritative for:
- feel,
- visual hierarchy,
- readability,
- carousel/settings usability,
- icon legibility,
- impact/VFX density.

## Current next boundary
- validate v0.22 on Android landscape,
- then implement v0.23 FRIEND/LINK/RANDOM waiting-room UX,
- then design/wire real multiplayer room/match networking,
- continue full-run progression simulation before freezing passive/combo/HP coefficients.
