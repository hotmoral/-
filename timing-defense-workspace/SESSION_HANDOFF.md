# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.24**
- Public URL: `https://timing-defense-v011.onrender.com/v024.html`
- Live source HEAD: `61ad74d833148d409dc65292f302bb9086c4e7c9`
- Render deploy: `dep-dbbg528m7kps73esejbg` / LIVE

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

---

# Current implementation — v0.24
Files:
- `timing-defense-v011/v024-polish.js`
- `timing-defense-v011/v024.html`

See:
- `V024_RADAR_READABILITY_REPORT.md`
- `CHARACTER_PROFILE_RADAR_V1.md`

## Character-selection hierarchy
Three-zone landscape presentation is now:
- **left** = animated combat-profile radar,
- **center** = larger/taller hero only,
- **right** = six skill cards arranged `3 × 2`.

Hero navigation remains arrow + horizontal swipe. Arrows sit closer to the hero. Header/nickname/footer heights are reduced on short landscape displays to free more hero height.

## Approved profile radar
Six axes:
`공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`.

Five visual levels. The UI does not need to print 1–5 values.

Approved class profiles:
- Knight `4 / 2 / 3 / 3 / 4 / 2`
- Rogue `2 / 5 / 5 / 1 / 1 / 1`
- Tank `2 / 1 / 1 / 5 / 1 / 3`
- Archer `3 / 2 / 4 / 1 / 5 / 2`
- Mage `4 / 2 / 2 / 1 / 1 / 5`

Equal values are allowed. The radar is a class-identity graphic, not a forced class ranking.

Animation contract:
- five-ring hex web,
- center-out class-color scan,
- staggered six-vertex outward growth (`띠리리릭` feel),
- class-color polygon fill/glow,
- vertex landing pulse,
- short settling pulse,
- roughly one-second total transition.

## Skill roadmap
The prior six-icon strip + one selected detail is replaced with six direct cards in `3 × 2`.
Each card contains icon, skill name, unlock level and description. Mechanic-specific icon semantics remain frozen direction.

## TEAM lineup
- redundant bottom SUMMARY removed,
- right lineup panel receives more width,
- five class buttons wrap into two rows for each AI unit,
- AI row height increased,
- TEAM AI FILL max remains +2; SOLO AI max remains +3.

## Rogue HUD identity
Rogue HUD changes from v0.23 red/silver to **charcoal/black + silver**:
- Timing Square,
- charge pips,
- charge/heavy text,
- EXP gauge,
- LV/EXP labels,
- `+EXP N` popup.

This is presentation-only. Rogue damage/crit/skill coefficients are unchanged.

## Projectile readability
Natural scenery made attack projectiles too faint/blur-like.
v0.24 does **not** slow travel numerically. It adds visual contrast/trails over the existing renderer:
- Knight: deep amber + bright gold edge,
- Rogue: charcoal blade + silver edge/trail,
- Tank: dark navy + cyan edge,
- Archer: forest green + pale edge/trail,
- Mage: deep purple + pale violet ring/trail.

If device validation still finds projectiles hard to read, discuss a small travel-time change before applying it.

---

# Network truth boundary
Actual multiplayer is **not yet implemented**.
FRIEND/LINK/RANDOM remain selection states only.
Do not claim a remote player joined until two independent clients share authoritative room/game state.

The waiting-room slice has been deferred again because v0.24 was used for the approved radar/readability patch. It becomes the next version after v0.24 device validation.

---

# Exact next work boundary
1. Device-test public v0.24.
2. Verify radar labels/rings do not clip on short Android landscape.
3. Verify radar animation replays cleanly per class switch and stale animations cancel.
4. Verify center hero gets visibly more vertical presence and no longer collides with right panel.
5. Verify six skill cards in 3×2 remain readable.
6. Verify TEAM lineup shows all five class choices without clipping.
7. Verify Rogue Timing Square/charge/EXP read as black/charcoal + silver, not red.
8. Verify projectiles are recognizable objects rather than only fast blur streaks.
9. If still weak, report/discuss whether a small projectile travel-time adjustment is needed.
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
3. `V024_RADAR_READABILITY_REPORT.md`
4. `CHARACTER_PROFILE_RADAR_V1.md`
5. `V023_LOBBY_POLISH_REPORT.md`
6. `V022_LOBBY_IMPLEMENTATION_REPORT.md`
7. `V021_IMPLEMENTATION_REPORT.md`
8. `V020_IMPLEMENTATION_REPORT.md`
9. `DESIGN_DECISIONS.md`
10. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
11. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
12. `SKILL_PLAN_LV6_31.md`
13. `TIER_PRESSURE_GRAMMAR_V1.md`
14. `PRESSURE_RECIPES_V1.md`
15. `SIMULATION_METHOD.md`
16. `NEXT_WORK.md`
