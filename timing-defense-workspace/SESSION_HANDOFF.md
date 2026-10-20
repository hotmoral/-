# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.25**
- Public URL: `https://timing-defense-v011.onrender.com/v025.html`
- Live source HEAD: `fce42eb1261ff43277c27d844617b96a546d6d1a`
- Render deploy: `dep-dbbga8c9v7es73f567b0` / LIVE

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

Passive auto-attack interval is currently common across all classes at `2.0 s`; class projectile visual travel times differ.

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
- approved five-level six-axis class radar added,
- axes: 공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역,
- profiles: Knight 4/2/3/3/4/2; Rogue 2/5/5/1/1/1; Tank 2/1/1/5/1/3; Archer 3/2/4/1/5/2; Mage 4/2/2/1/1/5,
- right skill layout becomes 3×2,
- TEAM SUMMARY removed; class buttons wrap to two rows,
- Rogue HUD becomes charcoal/black + silver,
- projectile contrast/trails strengthened without travel-time changes.

---

# Current implementation — v0.25
Files:
- `timing-defense-v011/v025-layout.js`
- `timing-defense-v011/v025.html`

See `V025_LAYOUT_POLISH_REPORT.md`.

## Why v0.25 exists
Android screen recording showed a real-device layout issue: v0.24 still left too much apparent vertical whitespace above the character-selection window because the top brand/nickname region remained too tall at device/browser scale. The left radar labels were also too small and the class-description flavor had been over-compressed.

## Vertical reclaim
v0.25 fixes the structural spacing:
- top header reduced again,
- nickname row moved upward/compressed,
- footer reduced,
- reclaimed height is assigned directly to the carousel/profile window,
- center hero maximum height increased.

## Left combat profile restored
The left panel now contains:
- COMBAT PROFILE,
- Korean class name,
- larger English class name,
- class tag,
- animated radar,
- role line,
- fuller one-sentence class/play-style description.

Radar axis labels are significantly larger than v0.24.
Animation remains premium/staggered:
- center-out scan,
- six delayed vertex expansions,
- class-color polygon fill/glow,
- landing node pulses,
- final breathing ripple,
- stale animation cancellation on class change.

## Skill panel
Six skills stay in the approved `3 × 2` layout. The extra height is used to increase card/icon/text breathing room rather than reverting to a single strip.

## Radar presentation contract
Five visual levels, no need to print numeric 1–5 values in the UI.
Equal levels between classes are allowed. Radar is a class-identity graphic, not a literal raw-stat dump.

Approved values remain:
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

---

# Network truth boundary
Actual multiplayer is **not yet implemented**.
FRIEND/LINK/RANDOM remain selection states only.
Do not claim a remote player joined until two independent clients share authoritative room/game state.

TEAM slot rule:
- SOLO: AI 0–3
- TEAM: AI FILL 0–2, preserving at least one human slot.

The waiting-room slice remains next after v0.25 device validation.

---

# Exact next work boundary
1. Device-test public v0.25 on the same Android landscape setup.
2. Verify top whitespace is materially reduced.
3. Verify character-selection panel is visibly taller.
4. Verify radar labels are clearly readable.
5. Verify restored role/description copy feels rich enough without crowding the radar.
6. Verify center hero and right 3×2 skill panel remain separated.
7. Recheck TEAM lineup class buttons for clipping.
8. Recheck Rogue black/silver HUD and projectile visibility.
9. Fix visual/implementation defects only.
10. Then implement FRIEND/LINK/RANDOM waiting-room UX without faking connectivity.
11. After waiting UX, design/wire actual room/invite/random network architecture.
12. Continue full-run progression simulation before freezing passive/HP/combo values.

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
3. `V025_LAYOUT_POLISH_REPORT.md`
4. `V024_RADAR_READABILITY_REPORT.md`
5. `CHARACTER_PROFILE_RADAR_V1.md`
6. `V023_LOBBY_POLISH_REPORT.md`
7. `V022_LOBBY_IMPLEMENTATION_REPORT.md`
8. `V021_IMPLEMENTATION_REPORT.md`
9. `V020_IMPLEMENTATION_REPORT.md`
10. `DESIGN_DECISIONS.md`
11. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
12. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
13. `SKILL_PLAN_LV6_31.md`
14. `TIER_PRESSURE_GRAMMAR_V1.md`
15. `PRESSURE_RECIPES_V1.md`
16. `SIMULATION_METHOD.md`
17. `NEXT_WORK.md`
